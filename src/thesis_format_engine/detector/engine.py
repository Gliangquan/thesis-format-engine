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
                issues.extend(self._compare_paragraph(node, rule.paragraph_style.model_dump(exclude_none=True)))

        return issues

    def _compare_paragraph(self, node: DocumentNode, expected: dict) -> list[dict]:
        actual = node.paragraph_style.model_dump(exclude_none=True)
        issues: list[dict] = []

        for field, expected_value in expected.items():
            actual_value = actual.get(field)
            if actual_value is None:
                continue

            if isinstance(expected_value, float):
                if round(float(actual_value), 2) != round(float(expected_value), 2):
                    issues.append(self._issue(node, field, actual_value, expected_value))
                continue

            if actual_value != expected_value:
                issues.append(self._issue(node, field, actual_value, expected_value))

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
