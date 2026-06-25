from pydantic import BaseModel


class SafetySummary(BaseModel):
    secrets_redacted: bool = True
    github_dry_run: bool = True
    write_actions_enabled: bool = False
