"""
Very small message router: one place to call the narrator function.
If you later add commands (/reset, /help) or pre/post-processing, do it here.
"""

from typing import List, Tuple

# Import the real narrator hook
try:
    from game.engine import respond_narrator  # noqa: F401
except Exception:
    respond_narrator = None  # type: ignore

# Keep tip text aligned with the frontends
try:
    from game.ui_shared import TIP_TEXT
except Exception:
    TIP_TEXT = "Try “Look around”, “Inventory”, “Open the door”."

# Example command hook (stub for future)
# def _handle_command(text: str) -> str | None:
#     if text.lower() == "/help":
#         return "Commands: /help, /reset (coming soon). " + TIP_TEXT
#     return None


class Router:
    def __init__(self):
        self._ready = callable(respond_narrator)

    @property
    def ready(self) -> bool:
        return self._ready

    def handle(self, message: str, history: List[Tuple[str, str]]) -> str:
        """
        Main entry used by the UI layer. History is provided for future use
        (e.g., you may inspect recent turns for system prompts or state).
        """
        if not self._ready:
            return (
                "⚠️ Dependency missing or not importable: game.engine.respond_narrator.\n"
                "Ensure the agents framework is installed and imports succeed."
            )

        try:
            text = (message or "").strip()
            if not text:
                return f"Say something like: {TIP_TEXT}"

            # cmd = _handle_command(text)
            # if cmd is not None:
            #     return cmd

            return respond_narrator(text)  # type: ignore
        except Exception as e:
            return f"⚠️ Error: {e!s}"
