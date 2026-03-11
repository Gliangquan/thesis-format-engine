from pathlib import Path

import yaml

from thesis_format_engine.models.rule import RuleSet


class RuleLoader:
    def load(self, path: str) -> RuleSet:
        payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        return RuleSet.model_validate(payload)
