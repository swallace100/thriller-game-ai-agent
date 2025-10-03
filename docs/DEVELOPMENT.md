# Eternal Hunt — Development Guide

This doc covers local setup, commands, and common fixes for running the **Eternal Hunt: AI Agent Powered Game** apps (Gradio & Streamlit) and tests.

---

## Prerequisites

- **Python** 3.13. Verify with:
  - PowerShell (Windows): `python -V`
  - macOS/Linux: `python3 -V`
- **Make** (optional on Windows; we use it to call the venv tools)
  - If `make` isn’t available on Windows, you can run the commands shown in the “What `make` does” notes.

> **OpenAI key:** put `OPENAI_API_KEY` in a `.env` file in `resources/openaiApiKey.env`.

---

## Quickstart

```bash
# one-time
make install         # create venv and install deps
make pc-install      # install pre-commit and set up the git hook

# run pre-commit hooks against the repo
make pc-run

# run tests
make test
Running the apps
bash
Copy code

# Gradio UI
make run

# Streamlit UI
make streamlit
```

Gradio defaults to http://127.0.0.1:7860 and Streamlit to http://localhost:8501.

## Make targets (reference)

| Target               |                            What it does                             |
| :------------------- | :-----------------------------------------------------------------: |
| `make venv`          |                  Create .venv virtual environment.                  |
| `make install`       | Upgrade pip, install requirements\*.txt, optional editable install. |
| `make dev`           |                         Alias for install.                          |
| `make install-tools` |   Ensure pytest/ruff/black/pre-commit are installed in the venv.    |
| `make test`          |            Run tests quietly (sets THRILLER_SAVE_PATH).             |
| `make testv`         |                        Run tests verbosely.                         |
| `make cov`           |            Coverage run (installs coverage if missing).             |
| `make lint`          |                             Ruff check.                             |
| `make fmt`           |                              Ruff fix.                              |
| `make typecheck`     |                 (If you add mypy) run type checks.                  |
| `make run`           |                 Launch Gradio app (app_gradio.py).                  |
| `make streamlit`     |              Launch Streamlit app (app_streamlit.py).               |
| `make reset-state`   |                    Delete the default save file.                    |
| `make pc-install`    |                    Install pre-commit git hook.                     |
| `make pc-run`        |                       Run hooks on all files.                       |
| `make pc-update`     |                        Update hook versions.                        |
| `make clean`         |                   Remove caches/build artifacts.                    |

Windows note: If you see errors like THRILLER_SAVE_PATH is not recognized, use the provided Makefile.win approach (the Makefile already branches to PowerShell-compatible syntax).

## Configuration

Most app/UI constants live in game/config.py.

### Environment variables

- OPENAI_API_KEY – required for live agent runs.

Create a local .env file in `./resources` using the .env_example file:

```env
OPENAI_API_KEY=sk-your-key
```

## Project layout (high level)

```bash
.
├─ app_gradio.py             # Gradio web app (with manifest/robots/sitemap routes)
├─ app_streamlit.py          # Streamlit web app
├─ game/
│  ├─ __init__.py
│  ├─ config.py              # Names, URLs, example commands, model
│  ├─ content.py             # Story text + NARRATOR_INTRO
│  ├─ state.py               # GameState + save/load helpers
│  ├─ tools.py               # function_tool tools (log/inventory/research)
│  ├─ engine.py              # Agent wiring + respond_narrator + output scrubber
│  ├─ narrator.py            # make_narrator(state)
│  ├─ web_research.py        # make_web_research_agent(state)
│  ├─ ui_shared.py           # Shared CSS/HTML helpers for both UIs
│  └─ router.py              # Thin wrapper used by UIs
├─ assets/                   # sample runs, favicon, etc.
├─ docs/
│  └─ DEVELOPMENT.md         # Dev setup, commands, troubleshooting
├─ tests/                    # pytest suite + fixtures
├─ requirements.txt          # runtime deps
├─ requirements-dev.txt      # test/lint/dev deps (optional)
└─ .pre-commit-config.yaml   # formatting/lint hooks

```

## Running without make (manual commands)

Create & use the venv

- Windows (PowerShell):

```powershell
Copy code
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

- macOS/Linux:

```bash
Copy code
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Run apps

```bash
# Gradio
python app_gradio.py

# Streamlit
streamlit run app_streamlit.py
```

## Testing

```bash
Copy code
make test # quick
make testv # verbose
make cov # with coverage
```

Behind the scenes we set THRILLER_SAVE_PATH so tests write to a temp path.
Fixtures also supply a fake agents module so the suite doesn’t need network/model calls.

## Code quality

```bash
   Copy code
   make lint # ruff
   make fmt # ruff --fix
   make pc-run # pre-commit hooks on entire repo
```

Add more hooks in .pre-commit-config.yaml as you like (black, ruff, mypy, etc.).

## Troubleshooting

### “No module named game”

Run from the repo root (so Python sees the package), e.g. python app_gradio.py.

### Streamlit/Gradio shows ‘dependency missing’ warning

The Router checks game.engine.respond_narrator. Ensure openai-agents is installed:

```bash
pip install openai-agents
```

### White/washed-out text in dark mode

We ship a dark-mode CSS override in game/ui_shared.py (GRADIO_CSS & STREAMLIT_CSS).
Hard refresh after changes: Ctrl/Cmd + Shift + R.

Binary wheels fail to import (numpy, Pillow, orjson, \_brotli)
Upgrade pip, then reinstall those packages without cache:

```bash
python -m pip install -U pip
pip install --no-cache-dir --only-binary=:all: numpy pillow orjson brotli
```

### Pydantic / pydantic-core mismatch

Install a known-good version:

```bash
pip install --no-cache-dir "pydantic==2.11.9"
```

Best practice is to install pydantic and let it choose the best pydantic-core version to pair with.

### Reset state / clean run

```bash
make reset-state
```

## Security/Keys

- Never commit .env or keys.
- The game reads OPENAI_API_KEY from resources/openaiApiKey.env.
- Pre-commit has a “detect-private-key” hook enabled by default.

## Release checklist

- `make pc-run` (clean lints)
- `make test`
- Verify both UIs:
  - Intro message seeds correctly
  - Saves occur to THRILLER_SAVE_PATH
  - No tool-call chatter in output (engine scrubber active)
  - Update APP_VERSION in game/config.py if needed
