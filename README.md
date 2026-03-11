# Thesis Format Engine

A rule-driven engine for inspecting and repairing thesis formatting in `.docx` documents.

## Vision

Turn thesis formatting from manual, error-prone checking into a structured pipeline:

1. parse thesis structure
2. extract effective formatting
3. compare against template rules
4. generate a diff report
5. apply safe formatting patches

## Scope of v0.1

- `.docx` only
- structure extraction for paragraphs and tables
- paragraph style comparison (font, size, bold, alignment, line spacing, first-line indent, spacing)
- table extraction and comparison for borders plus cell text style (font / size / alignment)
- rule-driven inspection
- JSON/Markdown report output
- first-pass auto-fix for paragraph font/alignment and table borders
- JSON + Markdown inspection reports
- logical role inference prototype for abstract / references / captions / heading levels / TOC / numbered headings
- rules can match by style region or inferred logical role

## Rule schema

- current rule schema: `metadata + rules[] + match + target`
- schema guide: `docs/rule-schema.md`
- draft generator guide: `docs/template-draft-generator.md`
- draft generator merges repeated samples and records `sample_count` + `examples` + confidence
- backward compatible with legacy `name/version/regions` files

## Planned modules

- `models/` — data models for nodes, styles, and rules
- `core/` — docx parsing and OOXML helpers
- `rules/` — template rule loading
- `detector/` — format comparison engine
- `patcher/` — safe formatting changes
- `report/` — diff and summary outputs
- `cli/` — command line entrypoints

## Example target workflow

```bash
thesisfix draft-rules sample-template.docx --output draft-rules.yaml
thesisfix inspect paper.docx templates/university.yaml --output report.json
thesisfix patch paper.docx templates/university.yaml --output paper.fixed.docx
```

## Roadmap

### Phase 1
- parse `.docx`
- extract paragraphs and tables
- load structured rules
- emit JSON report

### Phase 2
- compare thesis vs template
- detect violations by region
- emit markdown summary

### Phase 3
- apply minimal patches
- save repaired docx copy
- add rollback strategy

### Phase 4
- template learning from sample thesis
- web UI / API
- support more complex structures
