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

- GitHub write actions are not implemented.
- `GITHUB_DRY_RUN` defaults to `true`.
- Local secrets belong only in `.env`, which is ignored by Git.
- CI log output is redacted before returning content.
- File access is guarded to stay under an allowed root.

## Later Design

The service layer is the intended integration point for future ADK multi-agent orchestration. Agents should call deterministic tools through clear interfaces and return structured report models.
