from thesis_format_engine.models.node import DocumentNode
from thesis_format_engine.models.rule import RuleSet


class DetectionEngine:
    def compare(self, nodes: list[DocumentNode], rules: RuleSet) -> list[dict]:
        rule_map = {rule.region: rule for rule in rules.regions}
        issues: list[dict] = []

        for node in nodes:
            if not node.region:
                continue

            rule = rule_map.get(node.region)
            if not rule:
                issues.append(
                    {
                        "node_id": node.node_id,
                        "region": node.region,
                        "severity": "warning",
                        "message": "No rule matched this region",
                    }
                )
                continue

            if node.node_type == "paragraph" and rule.paragraph_style and node.paragraph_style:
                issues.extend(self._compare_style(node, node.paragraph_style.model_dump(exclude_none=True), rule.paragraph_style.model_dump(exclude_none=True)))

            if node.node_type == "table" and rule.table_style and node.table_style:
                issues.extend(self._compare_style(node, node.table_style.model_dump(exclude_none=True), rule.table_style.model_dump(exclude_none=True)))

        return issues

    def _compare_style(self, node: DocumentNode, actual: dict, expected: dict, prefix: str = "") -> list[dict]:
        issues: list[dict] = []

        for field, expected_value in expected.items():
            actual_value = actual.get(field)
            if actual_value is None:
                continue

            current_field = f"{prefix}.{field}" if prefix else field

            if isinstance(expected_value, dict) and isinstance(actual_value, dict):
                issues.extend(self._compare_style(node, actual_value, expected_value, current_field))
                continue

            if isinstance(expected_value, float):
                if round(float(actual_value), 2) != round(float(expected_value), 2):
                    issues.append(self._issue(node, current_field, actual_value, expected_value))
                continue

            if actual_value != expected_value:
                issues.append(self._issue(node, current_field, actual_value, expected_value))

        return issues

    def _issue(self, node: DocumentNode, field: str, actual, expected) -> dict:
        return {
            "node_id": node.node_id,
            "region": node.region,
            "severity": "error",
            "field": field,
            "actual": actual,
            "expected": expected,
            "message": f"{field} does not match rule",
        }
