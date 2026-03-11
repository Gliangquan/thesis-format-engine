import json
from collections import Counter
from pathlib import Path


class ReportWriter:
    def write_json(self, path: str, payload: dict) -> None:
        Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def write_markdown(self, path: str, payload: dict) -> None:
        issues = payload.get("issues", [])
        role_counts = Counter(node.get("logical_role") for node in payload.get("nodes", []) if node.get("logical_role"))

        lines = [
            "# Thesis Format Inspection Report",
            "",
            f"- Document: `{payload.get('document', '')}`",
            f"- Rule set: `{payload.get('rules', '')}`",
            f"- Nodes: `{payload.get('node_count', 0)}`",
            f"- Issues: `{payload.get('issue_count', 0)}`",
            "",
            "## Logical role summary",
            "",
        ]

        if role_counts:
            for role, count in role_counts.items():
                lines.append(f"- {role}: {count}")
        else:
            lines.append("- none")

        lines.extend(["", "## Issues", ""])

        if not issues:
            lines.append("- No issues found")
        else:
            for issue in issues:
                field = issue.get("field", "n/a")
                lines.extend(
                    [
                        f"### {issue.get('node_id')} · {issue.get('region')}",
                        f"- Field: `{field}`",
                        f"- Expected: `{issue.get('expected', 'n/a')}`",
                        f"- Actual: `{issue.get('actual', 'n/a')}`",
                        f"- Severity: `{issue.get('severity', 'n/a')}`",
                        f"- Message: {issue.get('message', '')}",
                        "",
                    ]
                )

        Path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
