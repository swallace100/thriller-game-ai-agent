"""
Very small message router: one place to call your narrator tool/function.
If you later add commands (/reset, /help) or pre/post-processing, do it here.
"""

from typing import List, Tuple

# Try to import the real narrator hook; fall back with a friendly message.
try:
    # Keep this path aligned with your actual module (you can change it later).
    from thriller.engine import respond_narrator
 # noqa: F401
except Exception:
    respond_narrator = None  # type: ignore


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
                "⚠️ Dependency missing: `openai-agents` (module `agents`). "
                "Please install it and/or ensure `game.thriller_module.respond_narrator` is importable."
            )

        try:
            # You can add lightweight pre-processing here (e.g., trimming).
            text = (message or "").strip()
            if not text:
                return "Say something like: “Look around”, “Inventory”, or “Open the door.”"

            # Call your narrator function directly for now.
            reply = respond_narrator(text)  # type: ignore
            return reply
        except Exception as e:
            return f"⚠️ Error: {e!s}"
