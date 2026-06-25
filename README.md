# IncidentPilot

AI Incident Commander for Backend Failures.

IncidentPilot is a hackathon backend skeleton for investigating backend incidents using CI logs, local incident fixtures, repo search, secret redaction, structured reports, and later ADK multi-agent orchestration.

## Current Scope

This repository currently includes only the local backend foundation:

- FastAPI application
- Health check endpoint
- Mock incident trigger endpoint
- Placeholder structured report endpoint
- Local CI log reader
- Secret redactor
- Demo repository search
- Path traversal guard
- Pytest coverage for core utilities and health endpoint

It does not include AI agents, GitHub write actions, or a frontend.

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
- `GET http://127.0.0.1:8000/incidents/inc_001/report`

Example incident trigger body:

```json
{
  "scenario": "broken_api_route"
}
```

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

## Later Work

- ADK multi-agent orchestration
- GitHub read integration
- GitHub write actions behind explicit dry-run controls
- Richer incident report generation
- Persistent storage
- Frontend workflow for incident review
