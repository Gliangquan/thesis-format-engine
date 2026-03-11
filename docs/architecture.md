# Architecture

## Core pipeline

1. Input `.docx`
2. OOXML parser extracts structure nodes
3. Style resolver computes effective formatting
4. Rule loader reads template YAML/JSON
5. Detector compares actual style vs expected style
6. Reporter emits JSON/Markdown output
7. Patcher applies safe changes in later versions

## Main concepts

### Document node
Represents a paragraph, table, image caption, reference item, or another structural block.

### Style snapshot
A normalized style object for comparison:
- font family
- font size
- bold/italic
- alignment
- spacing
- indentation
- table borders
- border width
- cell alignment

### Rule set
A region-based template, for example:
- cover
- abstract_zh
- heading1
- body
- table_caption
- reference

## Strategy

- first support `.docx`
- resolve structure and formatting before patching
- keep rule engine separate from repair engine
- preserve explainability and rollback ability
