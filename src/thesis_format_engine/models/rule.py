from pydantic import BaseModel, Field

from thesis_format_engine.models.style import ParagraphStyleSnapshot, TableStyleSnapshot


class RegionRule(BaseModel):
    region: str
    paragraph_style: ParagraphStyleSnapshot | None = None
    table_style: TableStyleSnapshot | None = None


class RuleSet(BaseModel):
    name: str
    version: str = "1.0"
    regions: list[RegionRule] = Field(default_factory=list)
