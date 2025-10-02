# -------- Cross-platform Makefile for Eternal Hunt --------
# Works on macOS/Linux and Windows (PowerShell/CMD)

ifeq ($(OS),Windows_NT)
  PY        := .venv/Scripts/python.exe
  PIP       := .venv/Scripts/pip.exe
  PYTEST    := .venv/Scripts/pytest.exe
  STREAMLIT := .venv/Scripts/streamlit.exe
  RUFF      := .venv/Scripts/ruff.exe
  BLACK     := .venv/Scripts/black.exe
  PRECOMMIT := .venv/Scripts/pre-commit.exe
  RM        := powershell -NoProfile -Command "Remove-Item -Recurse -Force"
else
  PY        := .venv/bin/python
  PIP       := .venv/bin/pip
  PYTEST    := .venv/bin/pytest
  STREAMLIT := .venv/bin/streamlit
  RUFF      := .venv/bin/ruff
  BLACK     := .venv/bin/black
  PRECOMMIT := .venv/bin/pre-commit
  RM        := rm -rf
endif

SAVE ?= assets/sample_runs/session_latest.json

.PHONY: help install dev test testv cov lint fmt typecheck run gradio streamlit clean clean-venv clean-pyc reset-state check pc-install pc-run pc-update pc-clean hooks

# --- Make venv creation idempotent ---
VENV_FLAG := .venv/pyvenv.cfg

$(VENV_FLAG):
	python -m venv .venv

venv: $(VENV_FLAG)

help:
	@echo "Make targets: venv install dev install-tools test testv cov lint fmt typecheck run gradio streamlit clean reset-state check pc-install pc-run pc-update"

install: venv
	$(PY) -m pip install -U pip
	-$(PIP) install -r requirements.txt
	-$(PIP) install -r requirements-dev.txt
	-$(PIP) install -e .

dev: install

# --- SINGLE install-tools (includes pre-commit) ---
install-tools: venv
	$(PIP) install -U pytest pytest-asyncio ruff black pre-commit

test: install-tools
	$(SETENV) $(PYTEST) -q

testv: install-tools
	$(SETENV) $(PYTEST) -v

cov: install-tools
	$(PIP) install coverage
	$(PY) -m coverage run -m pytest
	$(PY) -m coverage report -m

lint: install-tools
	$(RUFF) check .

fmt: install-tools
	$(RUFF) check . --fix
	$(BLACK) .

typecheck: venv
	@$(PIP) install mypy || true
	@.venv$(if $(filter Windows_NT,$(OS)),/Scripts,/bin)/mypy game app tests || true

run: install
	$(PY) main.py

gradio: install
	$(PY) app_gradio.py

streamlit: install
	$(STREAMLIT) run app_streamlit.py

clean:
	$(RM) __pycache__ .pytest_cache .mypy_cache build dist *.egg-info tests/.pytest_cache || true
	@echo "Cleaned caches."

reset-state:
	@echo "Removing $(SAVE)"
	@$(RM) "$(SAVE)" || true

clean-venv:
	$(RM) .venv || true

check: lint test

# --- pre-commit helpers ---
pc-install: install-tools
	$(PRECOMMIT) install

pc-run: install-tools
	$(PRECOMMIT) run --all-files

pc-update: install-tools
	$(PRECOMMIT) autoupdate

pc-clean:
	@if [ -f .git/hooks/pre-commit ]; then rm .git/hooks/pre-commit; fi || true

hooks: pc-install pc-run
