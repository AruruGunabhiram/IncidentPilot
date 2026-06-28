.PHONY: setup dev test demo eval clean

PYTHON ?= python3
VENV ?= .venv
VENV_PYTHON ?= $(VENV)/bin/python
UVICORN ?= $(PYTHON) -m uvicorn

setup:
	$(PYTHON) -m venv $(VENV)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -r requirements.txt

dev:
	$(UVICORN) app.main:app --reload

test:
	$(PYTHON) -m pytest

demo:
	$(PYTHON) scripts/run_demo.py

eval:
	$(PYTHON) evals/run_evals.py

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	rm -rf reports
	find app/storage/reports -type f ! -name '.gitkeep' -delete
