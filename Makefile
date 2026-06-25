.PHONY: setup dev test clean

setup:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

dev:
	.venv/bin/uvicorn app.main:app --reload

test:
	.venv/bin/pytest

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	rm -rf reports
