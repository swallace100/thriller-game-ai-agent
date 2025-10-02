"""
Agent wiring + response entrypoint, with autosave after each turn.
"""

from __future__ import annotations
import asyncio
from typing import Optional, Dict, Any

from agents import Agent, Runner
from game.agents.web_research import make_web_research_agent
from game.agents.narrator import make_narrator
from game.state import default_state, save_state, load_state, GameState


def autoload_state(path: Optional[str] = None) -> bool:
    try:
        load_state(path) if path else load_state()
        return True
    except FileNotFoundError:
        return False


# Build the shared web research agent once per process
_WEB: Agent = make_web_research_agent(default_state)
# Build narrator (will be rebuilt per-turn with latest state)
_NARRATOR: Agent = make_narrator(default_state, web_agent=_WEB)


def _run_sync(coro):
    try:
        return asyncio.run(coro)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(coro)
        finally:
            loop.close()


def respond_narrator(message: str) -> str:
    """
    - Rebuild narrator with latest state and injected web-agent tool
    - Run one step
    - Autosave state
    """
    global _NARRATOR
    _NARRATOR = make_narrator(default_state, web_agent=_WEB)

    result = _run_sync(Runner.run(_NARRATOR, message))

    try:
        save_state()
    except Exception as e:
        print(f"[autosave warning] {e}")

    return getattr(result, "final_output", str(result))


def get_state_snapshot() -> Dict[str, Any]:
    state: GameState = default_state
    return {
        "game_log": [e.__dict__ for e in state.game_log],
        "items": [i.__dict__ for i in state.items],
        "research_log": [e.__dict__ for e in state.research_log],
    }
