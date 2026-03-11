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

        return issues
