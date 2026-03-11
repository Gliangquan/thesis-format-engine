from collections import Counter, OrderedDict, defaultdict
from pathlib import Path

import yaml

from thesis_format_engine.models.node import DocumentNode


class RuleDraftGenerator:
    def generate(self, docx_path: str, nodes: list[DocumentNode]) -> dict:
        grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
        meta: dict[tuple[str, str], dict] = {}

        for node in nodes:
            if node.node_type == "paragraph" and node.paragraph_style:
                paragraph_style = self._clean(node.paragraph_style.model_dump(exclude_none=True))
                if not paragraph_style:
                    continue
                key = self._paragraph_key(node)
                grouped[key].append(paragraph_style)
                meta.setdefault(
                    key,
                    {
                        "id": self._rule_id(node),
                        "name": self._rule_name(node),
                        "match": self._match(node),
                        "target_key": "paragraph_style",
                        "examples": [],
                    },
                )
                self._push_example(meta[key]["examples"], node.text)

            if node.node_type == "table" and node.table_style:
                table_style = self._clean(node.table_style.model_dump(exclude_none=True))
                if not table_style:
                    continue
                key = self._table_key(node)
                grouped[key].append(table_style)
                meta.setdefault(
                    key,
                    {
                        "id": self._rule_id(node),
                        "name": self._rule_name(node),
                        "match": self._match(node),
                        "target_key": "table_style",
                        "examples": [],
                    },
                )
                self._push_example(meta[key]["examples"], node.text or "[table]")

        rules: list[dict] = []
        for key, samples in grouped.items():
            merged = self._merge_samples(samples)
            if not merged:
                continue
            info = meta[key]
            rules.append(
                {
                    "id": info["id"],
                    "name": info["name"],
                    "match": info["match"],
                    "sample_count": len(samples),
                    "examples": info["examples"],
                    "target": {info["target_key"]: merged},
                }
            )

        return {
            "metadata": {
                "name": f"{Path(docx_path).stem} Draft Template",
                "version": "0.3-draft",
                "institution": None,
                "description": "Auto-generated merged rule draft from sample DOCX. Review before production use.",
            },
            "rules": rules,
        }

    def write_yaml(self, path: str, payload: dict) -> None:
        Path(path).write_text(
            yaml.safe_dump(payload, allow_unicode=True, sort_keys=False, indent=2),
            encoding="utf-8",
        )

    def _paragraph_key(self, node: DocumentNode) -> tuple[str, str]:
        match = "logical_role" if node.logical_role and node.logical_role != "body" else "region"
        value = node.logical_role if match == "logical_role" else (node.region or "paragraph")
        return (match, value or "paragraph")

    def _table_key(self, node: DocumentNode) -> tuple[str, str]:
        return ("region", node.region or "table")

    def _rule_id(self, node: DocumentNode) -> str:
        base = node.logical_role if node.logical_role and node.logical_role != "body" else (node.region or node.node_type)
        return str(base).lower().replace(" ", "-")

    def _rule_name(self, node: DocumentNode) -> str:
        if node.logical_role and node.logical_role != "body":
            return node.logical_role
        return node.region or node.node_type

    def _match(self, node: DocumentNode) -> dict:
        if node.logical_role and node.logical_role != "body":
            return {"logical_role": node.logical_role}
        return {"region": node.region}

    def _merge_samples(self, samples: list[dict]) -> dict:
        merged: OrderedDict[str, object] = OrderedDict()
        keys = sorted({key for sample in samples for key in sample.keys()})

        for key in keys:
            values = [sample[key] for sample in samples if key in sample]
            if not values:
                continue

            if all(isinstance(value, dict) for value in values):
                nested = self._merge_samples(values)
                if nested:
                    merged[key] = nested
                continue

            most_common_value, count = Counter(self._stable_key(value) for value in values).most_common(1)[0]
            if count >= max(2, len(values) // 2 + 1) or len(set(self._stable_key(value) for value in values)) == 1:
                merged[key] = self._recover_value(most_common_value)

        return dict(merged)

    def _push_example(self, examples: list[str], text: str | None) -> None:
        if not text:
            return
        normalized = text.strip().replace("\n", " ")
        if not normalized or normalized in examples:
            return
        if len(normalized) > 60:
            normalized = normalized[:57] + "..."
        if len(examples) < 3:
            examples.append(normalized)

    def _stable_key(self, value):
        if isinstance(value, dict):
            return tuple(sorted((k, self._stable_key(v)) for k, v in value.items()))
        if isinstance(value, list):
            return tuple(self._stable_key(v) for v in value)
        return value

    def _recover_value(self, value):
        if isinstance(value, tuple) and value and all(isinstance(item, tuple) and len(item) == 2 for item in value):
            return {k: self._recover_value(v) for k, v in value}
        if isinstance(value, tuple):
            return [self._recover_value(v) for v in value]
        return value

    def _clean(self, payload: dict) -> dict:
        cleaned = OrderedDict()
        for key, value in payload.items():
            if value is None:
                continue
            if isinstance(value, dict):
                nested = self._clean(value)
                if nested:
                    cleaned[key] = nested
                continue
            cleaned[key] = value
        return dict(cleaned)
