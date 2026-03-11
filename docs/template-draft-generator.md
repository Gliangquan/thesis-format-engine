# Template Draft Generator

## Purpose

Generate an editable YAML rule draft from a sample `.docx` template or a manually formatted example thesis.

## Command

```bash
thesisfix draft-rules sample-template.docx --output draft-rules.yaml
```

## What it does

- parses document nodes
- infers logical roles
- groups similar nodes by `logical_role` or `region`
- emits a draft rule file in the new schema

## Important note

The generated YAML is a **draft**, not a final production template.
You should review and normalize:

- duplicated or overly specific rules
- missing font family information
- institution-specific paragraph spacing
- table border standards

## Recommended workflow

1. pick a well-formatted sample `.docx`
2. run `draft-rules`
3. manually refine the YAML
4. run `inspect` against a real thesis
5. iterate until report quality is stable
