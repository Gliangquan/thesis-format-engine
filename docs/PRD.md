# PRD — Thesis Format Engine

## Problem

Existing document editing tools are weak at thesis-grade formatting inspection and repair. They often handle basic fonts and paragraphs, but fail on complex regions such as tables, border widths, captions, references, and mixed style inheritance.

## Goal

Build a rule-driven thesis formatting engine that can:

- inspect a `.docx` thesis
- compare it with a structured formatting template
- explain all violations clearly
- later apply safe formatting repairs without changing textual content

## Target users

- students writing theses
- teachers checking thesis format
- academic service teams
- institutions maintaining formatting templates

## Non-goals for v0.1

- `.doc` direct parsing
- OCR / scanned PDF support
- semantic rewriting of thesis content
- full GUI in the first version

## Core user flow

1. User provides a thesis `.docx`
2. User provides a structured rule file (`yaml/json`)
3. Engine parses document into structure nodes
4. Engine extracts effective styles
5. Detector compares nodes to rules
6. Engine outputs inspection report
7. Later versions apply safe formatting patches

## Success criteria

- correctly parse paragraph and table blocks
- correctly detect violations for basic thesis sections
- produce machine-readable and human-readable reports
- preserve original content unchanged
