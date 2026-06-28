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

## Investigate The Incident

```bash
curl -X POST http://127.0.0.1:8000/incidents/inc_001/investigate
```

## Read The Report

```bash
curl http://127.0.0.1:8000/incidents/inc_001/report
```

The clean `broken_api_route` scenario should show that the secret scan ran and
found no secrets:

```json
{
  "safety_review": {
    "secrets_detected": false,
    "redactions_applied": 0,
    "secret_scan_passed": true
  }
}
```

## Approve GitHub Issue Creation

```bash
curl -X POST http://127.0.0.1:8000/incidents/inc_001/approve \
  -H "Content-Type: application/json" \
  -d '{"action":"create_github_issue","approved":true,"approved_by":"demo-operator"}'
```

## Show Dry-Run Issue Preview

```bash
curl -X POST http://127.0.0.1:8000/incidents/inc_001/github/issue \
  -H "Content-Type: application/json" \
  -d '{"dry_run":true}'
```

Expected shape:

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

For real issue creation, use only a test/demo repository and intentionally set
`GITHUB_DRY_RUN=false`, `GITHUB_TOKEN`, `GITHUB_OWNER`, and `GITHUB_REPO`.
