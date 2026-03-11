from docx import Document

from thesis_format_engine.models.node import DocumentNode
from thesis_format_engine.models.style import ParagraphStyleSnapshot, TableStyleSnapshot


class DocxParser:
    def parse(self, path: str) -> list[DocumentNode]:
        document = Document(path)
        nodes: list[DocumentNode] = []

        for index, paragraph in enumerate(document.paragraphs):
            style_name = paragraph.style.name if paragraph.style else None
            nodes.append(
                DocumentNode(
                    node_id=f"p-{index}",
                    node_type="paragraph",
                    region=style_name,
                    text=paragraph.text,
                    paragraph_style=self._extract_paragraph_style(paragraph),
                )
            )

        for index, table in enumerate(document.tables):
            nodes.append(
                DocumentNode(
                    node_id=f"t-{index}",
                    node_type="table",
                    region=table.style.name if table.style else "Table",
                    table_style=TableStyleSnapshot(),
                )
            )

        return nodes

    def _extract_paragraph_style(self, paragraph) -> ParagraphStyleSnapshot:
        first_run = paragraph.runs[0] if paragraph.runs else None
        style_font = paragraph.style.font if paragraph.style else None
        fmt = paragraph.paragraph_format

        return ParagraphStyleSnapshot(
            font_family=(first_run.font.name if first_run and first_run.font.name else None)
            or (style_font.name if style_font and style_font.name else None),
            font_size_pt=(first_run.font.size.pt if first_run and first_run.font.size else None)
            or (style_font.size.pt if style_font and style_font.size else None),
            bold=(first_run.font.bold if first_run and first_run.font.bold is not None else None)
            if first_run
            else (style_font.bold if style_font and style_font.bold is not None else None),
            italic=(first_run.font.italic if first_run and first_run.font.italic is not None else None)
            if first_run
            else (style_font.italic if style_font and style_font.italic is not None else None),
            alignment=paragraph.alignment.name if paragraph.alignment is not None else None,
            line_spacing=float(fmt.line_spacing) if fmt.line_spacing is not None else None,
            space_before_pt=fmt.space_before.pt if fmt.space_before is not None else None,
            space_after_pt=fmt.space_after.pt if fmt.space_after is not None else None,
        )
