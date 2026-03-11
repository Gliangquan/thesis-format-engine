from collections import OrderedDict
from pathlib import Path

import yaml

from thesis_format_engine.models.node import DocumentNode


class RuleDraftGenerator:
    def generate(self, docx_path: str, nodes: list[DocumentNode]) -> dict:
        rules: list[dict] = []
        seen: set[tuple[str, str]] = set()

        for node in nodes:
            if node.node_type == "paragraph" and node.paragraph_style:
                paragraph_style = self._clean(node.paragraph_style.model_dump(exclude_none=True))
                if not paragraph_style:
                    continue
                key = self._paragraph_key(node)
                if key in seen:
                    continue
                seen.add(key)
                rules.append(
                    {
                        "id": self._rule_id(node),
                        "name": self._rule_name(node),
                        "match": self._match(node),
                        "target": {"paragraph_style": paragraph_style},
                    }
                )

            if node.node_type == "table" and node.table_style:
                table_style = self._clean(node.table_style.model_dump(exclude_none=True))
                if not table_style:
                    continue
                key = self._table_key(node)
                if key in seen:
                    continue
                seen.add(key)
                rules.append(
                    {
                        "id": self._rule_id(node),
                        "name": self._rule_name(node),
                        "match": self._match(node),
                        "target": {"table_style": table_style},
                    }
                )

        return {
            "metadata": {
                "name": f"{Path(docx_path).stem} Draft Template",
                "version": "0.1-draft",
                "institution": None,
                "description": "Auto-generated rule draft from sample DOCX. Review before production use.",
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
