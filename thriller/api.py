# game/api.py
import asyncio
from agents import Runner
from .state import GameState
from .agents import make_narrator

# Default single-user state (preserves current behavior)
_default_state = GameState()
_default_agent = make_narrator(_default_state)

def _sync_run(agent, message: str) -> str:
    """
    Runs the agent and returns final_output as a plain string.
    Safe to call from sync contexts (Gradio/Streamlit handlers).
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Nested loop case (e.g., notebooks) — create a new task and wait
            return asyncio.run(Runner.run(agent, message)).final_output
        else:
            return loop.run_until_complete(Runner.run(agent, message)).final_output
    except RuntimeError:
        # No running loop
        return asyncio.run(Runner.run(agent, message)).final_output

def respond_narrator(message: str) -> str:
    return _sync_run(_default_agent, message)

# Optional: factory for session isolation (use in future if you want)
def build_session_handler():
    state = GameState()
    agent = make_narrator(state)
    def handle(message: str) -> str:
        return _sync_run(agent, message)
    return handle, state  # handler + access to state if you want to display logs
