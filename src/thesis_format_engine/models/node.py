from pydantic import BaseModel

from thesis_format_engine.models.style import ParagraphStyleSnapshot, TableStyleSnapshot


class DocumentNode(BaseModel):
    node_id: str
    node_type: str
    region: str | None = None
    text: str | None = None
    paragraph_style: ParagraphStyleSnapshot | None = None
    table_style: TableStyleSnapshot | None = None
