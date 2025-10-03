"""
Agent wiring + response entrypoint, with autosave after each turn.
"""

from __future__ import annotations

import asyncio
import re
from typing import Any, Dict, Optional

from agents import Agent, Runner

from game.agents.narrator import make_narrator
from game.agents.web_research import make_web_research_agent
from game.state import GameState, default_state, load_state, save_state


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

_TOOL_LEAK_PATTERNS = (
    # Common function-call “narration”
    r"(?mi)^\s*Functions?\.[\w\.]+\s*-.*$",  # Functions.update_game_log - ...
    r"(?mi)^\s*(?:Tool|Function)\s*(?:Call|Result):.*$",  # Tool Call: ..., Function Result: ...
    # JSON-y function call blobs that sometimes get printed
    r"(?mi)^\s*\{\s*\"(?:tool|function)\".*?\}\s*$",
    r"(?mi)^\s*args\s*:\s*\{.*?\}\s*$",
)


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


def _scrub_tool_meta(text: str) -> str:
    if not text:
        return text
    for pat in _TOOL_LEAK_PATTERNS:
        text = re.sub(pat, "", text)
    # remove stray bracketed asides like “[Assistant has added …]”
    text = re.sub(r"(?mi)^\s*\[.*?(?:added|saved|update).*?\]\s*$", "", text)
    # collapse extra blank lines
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


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

    raw = getattr(result, "final_output", str(result))
    return _scrub_tool_meta(raw)


def get_state_snapshot() -> Dict[str, Any]:
    state: GameState = default_state
    return {
        "game_log": [e.__dict__ for e in state.game_log],
        "items": [i.__dict__ for i in state.items],
        "research_log": [e.__dict__ for e in state.research_log],
    }
