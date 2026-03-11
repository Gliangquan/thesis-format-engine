from pydantic import BaseModel, Field, model_validator

from thesis_format_engine.models.style import ParagraphStyleSnapshot, TableStyleSnapshot


class RuleMetadata(BaseModel):
    name: str
    version: str = "1.0"
    institution: str | None = None
    description: str | None = None


class RuleMatch(BaseModel):
    region: str | None = None
    logical_role: str | None = None


class RuleTarget(BaseModel):
    paragraph_style: ParagraphStyleSnapshot | None = None
    table_style: TableStyleSnapshot | None = None


class RuleItem(BaseModel):
    id: str | None = None
    name: str | None = None
    match: RuleMatch = Field(default_factory=RuleMatch)
    target: RuleTarget = Field(default_factory=RuleTarget)

    @property
    def region(self) -> str | None:
        return self.match.region

    @property
    def logical_role(self) -> str | None:
        return self.match.logical_role

    @property
    def paragraph_style(self) -> ParagraphStyleSnapshot | None:
        return self.target.paragraph_style

    @property
    def table_style(self) -> TableStyleSnapshot | None:
        return self.target.table_style


class RuleSet(BaseModel):
    metadata: RuleMetadata
    rules: list[RuleItem] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def migrate_legacy_schema(cls, data):
        if not isinstance(data, dict):
            return data
        if "metadata" in data and "rules" in data:
            return data

        legacy_regions = data.get("regions", [])
        return {
            "metadata": {
                "name": data.get("name", "Unnamed Rule Set"),
                "version": data.get("version", "1.0"),
            },
            "rules": [
                {
                    "id": item.get("logical_role") or item.get("region") or "rule",
                    "match": {
                        "region": item.get("region"),
                        "logical_role": item.get("logical_role"),
                    },
                    "target": {
                        "paragraph_style": item.get("paragraph_style"),
                        "table_style": item.get("table_style"),
                    },
                }
                for item in legacy_regions
            ],
        }

    @property
    def name(self) -> str:
        return self.metadata.name

    @property
    def version(self) -> str:
        return self.metadata.version

    @property
    def regions(self) -> list[RuleItem]:
        return self.rules
