from pydantic import BaseModel


class BorderStyle(BaseModel):
    style: str | None = None
    size: int | None = None
    color: str | None = None


class ParagraphStyleSnapshot(BaseModel):
    font_family: str | None = None
    font_size_pt: float | None = None
    bold: bool | None = None
    italic: bool | None = None
    alignment: str | None = None
    line_spacing: float | None = None
    first_line_indent_pt: float | None = None
    first_line_indent_chars: float | None = None
    space_before_pt: float | None = None
    space_after_pt: float | None = None


class TableStyleSnapshot(BaseModel):
    alignment: str | None = None
    width: str | None = None
    top_border: BorderStyle | None = None
    bottom_border: BorderStyle | None = None
    left_border: BorderStyle | None = None
    right_border: BorderStyle | None = None
    inside_h_border: BorderStyle | None = None
    inside_v_border: BorderStyle | None = None
    cell_paragraph_style: ParagraphStyleSnapshot | None = None
