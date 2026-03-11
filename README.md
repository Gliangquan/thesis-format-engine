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
- rule-driven inspection
- JSON/Markdown report output
- no auto-fix yet in the first milestone

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
python -m thesis_format_engine.cli.main inspect paper.docx --rules templates/university.yaml
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
