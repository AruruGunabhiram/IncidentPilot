from app.tools.redactor import REDACTION, redact_secrets


def test_redactor_removes_fake_secrets():
    text = (
        "token=ghp_abcdefghijklmnopqrstuvwxyz "
        "pat=github_pat_1234567890abcdef "
        "Authorization: Bearer abc.def.ghi "
        "api_key=secret123 "
        "password=hunter2 "
        "DATABASE_URL=postgres://user:pass@localhost/db"
    )

    redacted = redact_secrets(text)

    assert "ghp_" not in redacted
    assert "github_pat_" not in redacted
    assert "Bearer abc.def.ghi" not in redacted
    assert "secret123" not in redacted
    assert "hunter2" not in redacted
    assert "postgres://user:pass@localhost/db" not in redacted
    assert redacted.count(REDACTION) == 6
