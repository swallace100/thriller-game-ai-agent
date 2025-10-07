# 🎭 Eternal Hunt: AI Agent-Powered Thriller Game

![Python](https://img.shields.io/badge/Python-3.13+-blue)
![OpenAI Agents](https://img.shields.io/badge/OpenAI-Agents-orange)
![Frameworks](https://img.shields.io/badge/FastAPI%20·%20Gradio%20·%20Streamlit-purple)
![Data Models](https://img.shields.io/badge/Pydantic%20·%20NumPy-lightblue)
![Dev Tools](https://img.shields.io/badge/Pytest%20·%20Ruff%20·%20Precommit-gray)
![License: MIT](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Playable%20Prototype-yellow)

> A near-future **interactive text thriller** powered by an **AI Narrator Agent**.
> Type what you do — the world responds, logs evolve, and your inventory changes in real time.

![Eternal Hunt](assets/EternalHuntTitle.png)

<i>Generated using ChatGPT 5</i>

## 🚀 Features

- Conversational, AI-driven narrative
- Inventory + structured game log + research log
- Autosave after each turn (THRILLER_SAVE_PATH)
- Two UIs: Gradio (1-file, FastAPI routes) & Streamlit
- Shared UI polish (dark/light, intro seed, examples)
- Clean, testable, modular code

## 📁 Project Structure

```
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

## 🚀 Quickstart

Prefer Make? Great—everything below uses it. If you don’t have make, see manual commands in docs/DEVELOPMENT.md.

```bash
# one-time
make install         # create .venv and install deps
make pc-install      # set up pre-commit git hook

# run tests
make test            # or: make testv

# launch a UI
make run             # Gradio (http://127.0.0.1:7860)
# or
make streamlit       # Streamlit (http://localhost:8501)
```

### Environment

Create a .env in resources/openaiApiKey.env:

```txt
OPENAI_API_KEY=sk-...
```

### 🎮 How to Play

Type actions in the chat:

- Look around
- Inventory
- Open the door
- Check phone
- Run outside

The narrator replies cinematically; logs and inventory update silently in the background.

## 🧠 Tech Stack

### Core

- Python 3.13+ — async-first architecture with type safety
- OpenAI Agents 0.3+ — dynamic narrator and reasoning layer
- Pydantic v2 + pydantic-settings — structured state & config validation
- NumPy 2.3+ — lightweight numerical utilities for agent memory and logs

### Web Frameworks

- FastAPI + Uvicorn — lightweight API backend (Gradio mode)
- Gradio 5.43+ — rapid UI prototyping, single-file web interface
- Streamlit 1.50+ — alternate UI for interactive storytelling

### Environment & Utilities

- python-dotenv — environment and key management
- pre-commit + ruff — formatting, linting, and code hygiene
- pytest — full test coverage with isolated agent stubs

## 🧪 Testing & Quality

```bash
make test      # run tests (autosets THRILLER_SAVE_PATH to a temp path)
make lint      # ruff
make fmt       # ruff --fix
make pc-run    # run pre-commit hooks across the repo
```

Tests stub the `agents` library to avoid network calls; runtime uses the real `openai-agents`.

## 📜 License

MIT — see the full text in this repository.

## 🤝 Contributing

PRs welcome! Run make pc-run and make test before opening a PR.
