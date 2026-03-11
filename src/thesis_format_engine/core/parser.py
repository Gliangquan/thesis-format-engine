from docx import Document

from thesis_format_engine.models.node import DocumentNode
from thesis_format_engine.models.style import ParagraphStyleSnapshot


class DocxParser:
    def parse(self, path: str) -> list[DocumentNode]:
        document = Document(path)
        nodes: list[DocumentNode] = []

        for index, paragraph in enumerate(document.paragraphs):
            style = paragraph.style.name if paragraph.style else None
            nodes.append(
                DocumentNode(
                    node_id=f"p-{index}",
                    node_type="paragraph",
                    region=style,
                    text=paragraph.text,
                    paragraph_style=ParagraphStyleSnapshot(
                        alignment=str(paragraph.alignment) if paragraph.alignment is not None else None
                    ),
                )
            )

        return nodes
