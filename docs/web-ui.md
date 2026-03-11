# Web UI

## Start

```bash
uvicorn thesis_format_engine.web.app:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## Current features

- upload thesis `.docx`
- upload rule `.yaml`
- run `inspect`
- run `patch`
- view issue list in browser
- download patched `.docx`

## Current scope

This is a minimal MVP web interface intended for validation and demos.
It is not yet optimized for:

- user accounts
- template management
- persistent job history
- concurrent production workloads
