from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from thesis_format_engine.models.rule import RuleSet


class PatchEngine:
    def apply(self, docx_path: str, rules: RuleSet, output_path: str) -> dict:
        document = Document(docx_path)
        rule_map = {rule.region: rule for rule in rules.regions}
        changes = 0

        for paragraph in document.paragraphs:
            region = paragraph.style.name if paragraph.style else None
            rule = rule_map.get(region)
            if not rule or not rule.paragraph_style:
                continue
            changes += self._patch_paragraph(paragraph, rule.paragraph_style.model_dump(exclude_none=True))

        for table in document.tables:
            region = table.style.name if table.style else "Table"
            rule = rule_map.get(region)
            if not rule or not rule.table_style:
                continue
            changes += self._patch_table(table, rule.table_style.model_dump(exclude_none=True))

        document.save(output_path)
        return {"output": output_path, "changes": changes}

    def _patch_paragraph(self, paragraph, expected: dict) -> int:
        changes = 0
        for run in paragraph.runs:
            if "font_family" in expected and run.font.name != expected["font_family"]:
                run.font.name = expected["font_family"]
                changes += 1
            if "font_size_pt" in expected:
                target_size = float(expected["font_size_pt"])
                current = run.font.size.pt if run.font.size else None
                if current != target_size:
                    run.font.size = self._pt(target_size)
                    changes += 1
            if "bold" in expected and run.font.bold != expected["bold"]:
                run.font.bold = expected["bold"]
                changes += 1

        if "alignment" in expected:
            current_alignment = paragraph.alignment.name if paragraph.alignment is not None else None
            if current_alignment != expected["alignment"]:
                paragraph.alignment = self._alignment(expected["alignment"])
                changes += 1

        return changes

    def _patch_table(self, table, expected: dict) -> int:
        changes = 0
        border_mapping = {
            "top_border": "top",
            "bottom_border": "bottom",
            "left_border": "left",
            "right_border": "right",
            "inside_h_border": "insideH",
            "inside_v_border": "insideV",
        }

        for field, edge in border_mapping.items():
            if field not in expected:
                continue
            self._set_table_border(table, edge, expected[field])
            changes += 1

        return changes

    def _set_table_border(self, table, edge: str, spec: dict) -> None:
        tbl = table._tbl
        tbl_pr = tbl.tblPr
        tbl_borders = tbl_pr.first_child_found_in("w:tblBorders")
        if tbl_borders is None:
            tbl_borders = OxmlElement("w:tblBorders")
            tbl_pr.append(tbl_borders)

        border = tbl_borders.find(qn(f"w:{edge}"))
        if border is None:
            border = OxmlElement(f"w:{edge}")
            tbl_borders.append(border)

        if "style" in spec:
            border.set(qn("w:val"), str(spec["style"]))
        if "size" in spec:
            border.set(qn("w:sz"), str(spec["size"]))
        if "color" in spec:
            border.set(qn("w:color"), str(spec["color"]))

    def _alignment(self, value: str):
        from docx.enum.text import WD_ALIGN_PARAGRAPH

        return getattr(WD_ALIGN_PARAGRAPH, value)

    def _pt(self, value: float):
        from docx.shared import Pt

        return Pt(value)
