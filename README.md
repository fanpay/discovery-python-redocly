# testing-redocly

Sample FastAPI project for experimenting with OpenAPI and Redocly.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the API

```bash
uvicorn app.main:app --reload
```

Swagger UI: <http://127.0.0.1:8000/docs>

## Export OpenAPI for Redocly

```bash
python scripts/export_openapi.py
```

This exports the OpenAPI spec to `docs/openapi.yaml`.

You can then validate and render with Redocly CLI, for example:

```bash
redocly lint docs/openapi.yaml
redocly preview-docs docs/openapi.yaml
```
