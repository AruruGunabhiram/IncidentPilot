from pydantic import BaseModel


class Finding(BaseModel):
    title: str
    severity: str
    evidence: list[str] = []
    recommendation: str
