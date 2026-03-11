import json
from pathlib import Path


class ReportWriter:
    def write_json(self, path: str, payload: dict) -> None:
        Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
