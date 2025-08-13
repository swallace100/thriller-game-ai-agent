"""
Agent wiring + response entrypoint, with autosave after each turn.
"""

import asyncio
from typing import Optional

from agents import Agent, Runner, WebSearchTool  # same lib you already use
from thriller import content
from thriller.state import (
    default_state,
    save_state,      # NEW: autosave after each turn
    load_state,      # Optional: for manual/initial load
)
from thriller.tools import (
    update_game_log,
    update_research_log,
    add_player_item,
    remove_player_item,
)


# ---------- optional: preload a saved game at startup ----------
# Call autoload_state() from your app bootstrap if you want to resume.
def autoload_state(path: Optional[str] = None) -> bool:
    """
    Try to load state from disk (returns True if loaded).
    Uses THRILLER_SAVE_PATH env default if path not provided.
    """
    try:
        if path:
            load_state(path)
        else:
            # load_state() without args uses DEFAULT_SAVE_PATH from state.py
            load_state()
        return True
    except FileNotFoundError:
        return False


# ---------- agent builders ----------
def build_web_research_agent() -> Agent:
    return Agent(
        name="Web Research Agent",
        instructions=(
            "You support the Thriller Narrator Agent with concise facts. "
            "Save research queries and results to the research log using update_research_log."
        ),
        model="gpt-4o",
        tools=[WebSearchTool(), update_research_log],
    )


def build_narrator_agent(web_research_agent: Optional[Agent] = None) -> Agent:
    # Snapshot state for instructions (lightweight view only)
    game_log_view = [e.__dict__ for e in default_state.game_log]
    items_view = [i.__dict__ for i in default_state.items]

    instructions = f"""
{content.APP_INSTRUCTIONS_HEADER}

The game world is described here:
{content.GAME_STORY}

Current game details are stored here:
{game_log_view}

The player’s current inventory is listed here:
{items_view}

{content.APP_INSTRUCTIONS_POST}
""".strip()

    tools = [update_game_log, add_player_item, remove_player_item]

    # If you later want cross-agent calls, expose a tool that forwards to `web_research_agent`.
    if web_research_agent is not None:
        pass

    return Agent(
        name="Thriller Narrator Agent",
        instructions=instructions,
        model="gpt-4o",
        tools=tools,
    )


# Build singletons once per process.
_WEB = build_web_research_agent()
_NARRATOR = build_narrator_agent(_WEB)


# ---------- run helpers ----------
def _run_sync(coro):
    """
    Runs an async coroutine in the current or a new event loop.
    """
    try:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coro)
    except RuntimeError:
        new_loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(new_loop)
            return new_loop.run_until_complete(coro)
        finally:
            new_loop.close()


# ---------- public API used by the UI ----------
def respond_narrator(message: str) -> str:
    """
    Main entrypoint called by the UI (Gradio/Streamlit).
    - Rebuilds narrator with the latest state snapshot
    - Runs one step
    - AUTOSAVES state to disk
    """
    global _NARRATOR
    _NARRATOR = build_narrator_agent(_WEB)

    res = _run_sync(Runner.run(_NARRATOR, message))

    # --- AUTOSAVE ---
    try:
        save_state()  # uses DEFAULT_SAVE_PATH from state.py unless overridden by env
    except Exception as e:
        # Don't crash the turn if saving fails
        print(f"[autosave warning] {e}")

    return getattr(res, "final_output", str(res))


def get_state_snapshot():
    """
    Useful for debugging or a future “View State” panel in the UI.
    """
    return {
        "game_log": [e.__dict__ for e in default_state.game_log],
        "items": [i.__dict__ for i in default_state.items],
        "research_log": [e.__dict__ for e in default_state.research_log],
    }
