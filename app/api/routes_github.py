"""GitHub issue route — approval- and safety-gated, dry-run by default.

This endpoint never writes to GitHub in this phase. It enforces every gate
(incident exists, report exists, safety review allows it, human approval on
file) and then returns a redacted preview of the issue it *would* file. The
actual network write is intentionally not implemented.
"""

from fastapi import APIRouter, Body, Depends

from app.config import Settings
from app.dependencies import settings_dependency
from app.schemas.approval import GitHubIssueOptions, GitHubIssueResult
from app.services import investigation_service

router = APIRouter(prefix="/incidents", tags=["github"])


@router.post("/{incident_id}/github/issue", response_model=GitHubIssueResult)
def create_github_issue(
    incident_id: str,
    options: GitHubIssueOptions | None = Body(default=None),
    settings: Settings = Depends(settings_dependency),
) -> GitHubIssueResult:
    """Preview (never create) the GitHub issue for an approved, grounded report."""
    options = options or GitHubIssueOptions()
    github_configured = bool(
        settings.github_token and settings.github_owner and settings.github_repo
    )
    return investigation_service.create_github_issue(
        incident_id,
        options,
        github_configured=github_configured,
        env_dry_run=settings.github_dry_run,
    )
