# IncidentPilot

AI Incident Commander for Backend Failures.

IncidentPilot is a hackathon backend skeleton for investigating backend incidents using CI logs, local incident fixtures, repo search, secret redaction, structured reports, and later ADK multi-agent orchestration.

## Current Scope

This repository currently includes only the local backend foundation:

- FastAPI application
- Health check endpoint
- Local incident trigger endpoint
- Deterministic investigation endpoint
- Structured report retrieval endpoint
- Human approval endpoint
- GitHub issue endpoint, gated by safety review, human approval, and dry-run by default
- Local CI log reader
- Secret redactor
- Demo repository search
- Path traversal guard
- Pytest coverage for API routes, schemas, safety behavior, and deterministic tools

It does not include a frontend. GitHub issue creation is the only external
write path, and it is disabled unless safety passes, a human approves, GitHub is
fully configured, and `GITHUB_DRY_RUN=false`.

## Setup

Use Python 3.11 or newer.

Create and activate a virtual environment with Python 3.11 or newer:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your local environment file from the example:

```bash
cp .env.example .env
```

Do not commit `.env`.

## Run The API

```bash
uvicorn app.main:app --reload
```

Open:

- `GET http://127.0.0.1:8000/health`
- `POST http://127.0.0.1:8000/incidents/trigger`
- `POST http://127.0.0.1:8000/incidents/inc_001/investigate`
- `GET http://127.0.0.1:8000/incidents/inc_001/report`
- `POST http://127.0.0.1:8000/incidents/inc_001/approve`
- `POST http://127.0.0.1:8000/incidents/inc_001/github/issue`

Example incident trigger body:

```json
{
  "scenario": "broken_api_route"
}
```

Safety reports expose the secret scan result explicitly:

```json
{
  "secrets_detected": false,
  "redactions_applied": 0,
  "secret_scan_passed": true
}
```

The GitHub issue endpoint returns a dry-run preview by default:

```json
{
  "created": false,
  "dry_run": true,
  "title": "IncidentPilot: POST /payments fails due to unchecked missing user",
  "body_preview": "...",
  "issue_url": null,
  "issue_number": null
}
```

For a real issue, use only a test/demo repository and set `GITHUB_DRY_RUN=false`
with `GITHUB_TOKEN`, `GITHUB_OWNER`, and `GITHUB_REPO`.

## Run Tests

```bash
pytest
```

Or use:

```bash
make test
```

## Make Targets

```bash
make setup
make dev
make test
make clean
```

## Architecture Graph

This repository includes Graphify-generated architecture artifacts:

- `graphify-out/GRAPH_REPORT.md`
- `graphify-out/graph.html`
- `graphify-out/graph.json`

Graphify was used as a development-time codebase mapping tool to inspect module boundaries, identify central modules, and reduce AI coding context waste during development.

Graphify is not part of the runtime incident investigation pipeline. IncidentPilot performs runtime evidence extraction through its own deterministic tools: CI log parser, repo search, path guard, redactor, structured report builder, safety reviewer, and approval gate.

## Later Work

- ADK multi-agent orchestration
- GitHub read integration
- Evaluation results and demo polish
- Richer incident report generation
- Persistent storage
- Frontend workflow for incident review
