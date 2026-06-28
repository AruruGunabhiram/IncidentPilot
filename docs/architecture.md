# Architecture

IncidentPilot is organized as a small FastAPI backend with explicit boundaries for API routes, schemas, services, local tools, and storage.

## Current Components

- `app/main.py`: FastAPI app creation and router registration.
- `app/api/`: HTTP route handlers.
- `app/schemas/`: Pydantic request and response models.
- `app/services/`: Business workflow entrypoints.
- `app/tools/`: Deterministic local utilities for logs, redaction, guarded paths, and repo search.
- `app/storage/`: Temporary in-memory report storage and a future reports directory.
- `demo/`: Local fixtures for hackathon demos.

## Safety Defaults

- `GITHUB_DRY_RUN` defaults to `true`.
- GitHub issue creation is the only external write path.
- Real issue creation requires a clean safety review, explicit human approval,
  complete GitHub configuration, and `GITHUB_DRY_RUN=false`.
- Missing GitHub configuration falls back to a dry-run preview with
  `body_preview`, `issue_url`, and `issue_number` fields.
- Local secrets belong only in `.env`, which is ignored by Git.
- CI log output is redacted before returning content.
- File access is guarded to stay under an allowed root.

## Later Design

The next phase is evaluation and demo polish: results, README, demo script,
architecture notes, screenshots, and demo video. Additional GitHub automation,
pull requests, branches, or repository writes are out of scope.
