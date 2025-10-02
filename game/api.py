import asyncio
from agents import Runner
from .state import GameState, save_state
from .agents.narrator import make_narrator

# Default single-user state (preserves current behavior)
_default_state = GameState()
_default_agent = make_narrator(_default_state)


def _sync_run(agent, message: str) -> str:
    """
    Runs the agent and returns final_output as a plain string.
    Use asyncio.run in tests/CLI; for web UIs prefer an async handler.
    """
    try:
        return asyncio.run(Runner.run(agent, message)).final_output
    except RuntimeError:
        # If we're already inside a running loop (e.g., notebooks),
        # fall back to the current loop.
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(Runner.run(agent, message)).final_output


def respond_narrator(message: str) -> str:
    # Run one turn
    result_text = _sync_run(_default_agent, message)

    # Persist AFTER processing – reads THRILLER_SAVE_PATH at call time
    save_state()

    return result_text


# Optional: per-session factory, e.g., for Gradio/Streamlit stateful sessions
def build_session_handler():
    state = GameState()
    agent = make_narrator(state)

    def handle(message: str) -> str:
        text = _sync_run(agent, message)
        # If you want session-specific persistence, pass a path here:
        # state.save("runs/session_<session_id>.json")
        return text

    return handle, state
