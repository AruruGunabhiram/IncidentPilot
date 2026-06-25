import re

REDACTION = "[REDACTED_SECRET]"

SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]+"),
    re.compile(r"Bearer\s+[A-Za-z0-9._~+/=-]+", re.IGNORECASE),
    re.compile(r"(api_key=)[^\s&]+", re.IGNORECASE),
    re.compile(r"(password=)[^\s&]+", re.IGNORECASE),
    re.compile(r"(DATABASE_URL=)[^\s]+", re.IGNORECASE),
]


def redact_secrets(text: str) -> str:
    redacted = text
    for pattern in SECRET_PATTERNS:
        if pattern.pattern.startswith("("):
            redacted = pattern.sub(lambda match: f"{match.group(1)}{REDACTION}", redacted)
        else:
            redacted = pattern.sub(REDACTION, redacted)
    return redacted
