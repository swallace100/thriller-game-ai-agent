"""
Structured game state and helpers, now with persistence utilities.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Literal

GameLogCategory = Literal["event", "discovery", "decision", "question", "item", "ambient"]
ResearchCategory = Literal["info", "symbol", "historical", "technical", "psychological", "warning"]


@dataclass
class GameLogEntry:
    category: GameLogCategory
    entry: str
    ts: float = field(default_factory=lambda: time.time())


@dataclass
class ResearchLogEntry:
    category: ResearchCategory
    entry: str
    ts: float = field(default_factory=lambda: time.time())


@dataclass
class InventoryItem:
    name: str
    description: str = ""


@dataclass
class GameState:
    game_log: List[GameLogEntry] = field(default_factory=list)
    research_log: List[ResearchLogEntry] = field(default_factory=list)
    items: List[InventoryItem] = field(default_factory=list)

    # ---------- conversion ----------
    def to_dict(self) -> Dict[str, Any]:
        return {
            "game_log": [asdict(e) for e in self.game_log],
            "research_log": [asdict(e) for e in self.research_log],
            "items": [asdict(i) for i in self.items],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GameState":
        state = cls()
        for e in data.get("game_log", []):
            state.game_log.append(GameLogEntry(**e))
        for e in data.get("research_log", []):
            state.research_log.append(ResearchLogEntry(**e))
        for i in data.get("items", []):
            state.items.append(InventoryItem(**i))
        return state

    # ---------- file I/O ----------
    def save_json(self, path: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    def save(self, path: str | None = None) -> str:
        """Convenience wrapper that picks up the env var at save time."""
        path = path or _get_save_path()
        self.save_json(path)
        return path

    @classmethod
    def load_json(cls, path: str) -> "GameState":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)


# ---------- default global state ----------
default_state = GameState()

# ---------- persistence helpers ----------
DEFAULT_SAVE_PATH = os.getenv("THRILLER_SAVE_PATH", "assets/sample_runs/session_latest.json")


def _get_save_path(path: str | None = None) -> str:
    env = os.getenv("THRILLER_SAVE_PATH")  # type: str | None
    return path or env or "assets/sample_runs/session_latest.json"


def save_state(path: str | None = None) -> None:
    """Saves default_state to disk. Respects THRILLER_SAVE_PATH when path is None."""
    resolved = _get_save_path(path)
    default_state.save_json(resolved)


def load_state(path: str | None = None) -> None:
    """Loads game state from disk into default_state. Respects THRILLER_SAVE_PATH when None."""
    global default_state
    resolved = _get_save_path(path)
    if os.path.exists(resolved):
        default_state = GameState.load_json(resolved)
    else:
        raise FileNotFoundError(f"No saved game found at {resolved}")
