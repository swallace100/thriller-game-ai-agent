from __future__ import annotations

from typing import Callable, List, Optional, Tuple

# Public type for the narrator entrypoint
RespondFn = Callable[[str], str]

# Try to import the real narrator hook; record the import error if any
try:
    from game.engine import respond_narrator as _respond_narrator

    respond_narrator: Optional[RespondFn] = _respond_narrator  # optional, see except path
    _IMPORT_ERR: Optional[Exception] = None
except Exception as e:  # pragma: no cover - exercised only when engine is missing
    respond_narrator = None
    _IMPORT_ERR = e

# Keep tip text aligned with the frontends
try:
    from game.ui_shared import TIP_TEXT
except Exception:
    TIP_TEXT = "“Look around”, “Inventory”, “Open the door”."


class Router:
    def __init__(self) -> None:
        # Explicitly annotate so mypy knows this is a bool (not Any)
        self._ready: bool = callable(respond_narrator)

    @property
    def ready(self) -> bool:
        return self._ready

    def handle(self, message: str, history: List[Tuple[str, str]]) -> str:
        """
        Main entry used by the UI layer. History is provided for future use
        (e.g., you may inspect recent turns for system prompts or state).
        """
        if not self._ready or respond_narrator is None:
            # Log the actual import error to console for debugging
            if _IMPORT_ERR:
                print("[router import error]", repr(_IMPORT_ERR))
            return (
                "⚠️ Dependency missing or not importable: game.engine.respond_narrator.\n"
                "Ensure the agents framework is installed and imports succeed."
            )

        text = (message or "").strip()
        if not text:
            return f"Say something like: {TIP_TEXT}"

        # If you add command handling later, do it here.

        # `respond_narrator` is non-None in this branch (narrowed above)
        return respond_narrator(text)
