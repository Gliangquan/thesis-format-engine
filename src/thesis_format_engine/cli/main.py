from pathlib import Path

import typer
from rich import print

from thesis_format_engine.core.parser import DocxParser
from thesis_format_engine.detector.engine import DetectionEngine
from thesis_format_engine.patcher.engine import PatchEngine
from thesis_format_engine.report.writer import ReportWriter
from thesis_format_engine.rules.generator import RuleDraftGenerator
from thesis_format_engine.rules.loader import RuleLoader

app = typer.Typer(help="Inspect thesis DOCX formatting against structured rules.")


@app.command()
def inspect(
    docx_path: str,
    rules_path: str,
    output: str = "report.json",
    markdown_output: str | None = "report.md",
) -> None:
    parser = DocxParser()
    loader = RuleLoader()
    detector = DetectionEngine()
    writer = ReportWriter()

    nodes = parser.parse(docx_path)
    rules = loader.load(rules_path)
    issues = detector.compare(nodes, rules)

    payload = {
        "document": Path(docx_path).name,
        "rules": rules.name,
        "node_count": len(nodes),
        "issue_count": len(issues),
        "issues": issues,
        "nodes": [node.model_dump(exclude_none=True) for node in nodes],
    }
    writer.write_json(output, payload)
    if markdown_output:
        writer.write_markdown(markdown_output, payload)
        print(f"[green]Inspection complete[/green] → {output}, {markdown_output}")
    else:
        print(f"[green]Inspection complete[/green] → {output}")


@app.command()
def patch(docx_path: str, rules_path: str, output: str = "patched.docx") -> None:
    loader = RuleLoader()
    engine = PatchEngine()

    rules = loader.load(rules_path)
    result = engine.apply(docx_path, rules, output)
    print(f"[green]Patch complete[/green] → {result['output']} (changes={result['changes']})")


@app.command("draft-rules")
def draft_rules(docx_path: str, output: str = "draft-rules.yaml") -> None:
    parser = DocxParser()
    generator = RuleDraftGenerator()

    nodes = parser.parse(docx_path)
    payload = generator.generate(docx_path, nodes)
    generator.write_yaml(output, payload)
    print(f"[green]Draft rules generated[/green] → {output}")


if __name__ == "__main__":
    app()
