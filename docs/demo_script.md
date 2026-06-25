# Demo Script

## Local Setup

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Start The API

```bash
uvicorn app.main:app --reload
```

## Health Check

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "incidentpilot"
}
```

## Trigger Demo Incident

```bash
curl -X POST http://127.0.0.1:8000/incidents/trigger \
  -H "Content-Type: application/json" \
  -d '{"scenario":"broken_api_route"}'
```

## Read Placeholder Report

```bash
curl http://127.0.0.1:8000/incidents/inc_001/report
```

The report is intentionally placeholder data until agent orchestration is added.
