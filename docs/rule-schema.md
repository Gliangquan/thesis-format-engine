# Rule Schema

## Overview

The rule file is organized into two top-level sections:

- `metadata`: descriptive information about the template
- `rules`: matching + target formatting rules

## Example

```yaml
metadata:
  name: University Thesis Template
  version: "2.0"
  institution: Demo University

rules:
  - id: body-normal
    name: 正文段落
    match:
      region: Normal
    target:
      paragraph_style:
        font_family: 宋体
        font_size_pt: 12
        alignment: JUSTIFY
```

## Match block

A rule can match by:

- `region`: Word style name, e.g. `Normal`, `Heading 1`
- `logical_role`: inferred role, e.g. `abstract_heading`, `table_caption`

Current engine priority:
1. `logical_role`
2. `region`

## Target block

### paragraph_style

Supported fields:
- `font_family`
- `font_size_pt`
- `bold`
- `italic`
- `alignment`
- `line_spacing`
- `first_line_indent_pt`
- `space_before_pt`
- `space_after_pt`

### table_style

Supported fields:
- `top_border`
- `bottom_border`
- `left_border`
- `right_border`
- `inside_h_border`
- `inside_v_border`

Each border supports:
- `style`
- `size`
- `color`

## Compatibility

The engine still accepts the old `name/version/regions` schema and migrates it internally.
