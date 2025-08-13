# game/narrator.py
from agents import Agent
from ..config import MODEL
from ..story import GAME_STORY
from ..state import GameState
from ..tools import make_tools

def make_narrator(state: GameState) -> Agent:
    instructions = f"""
You are the narrator and game master for a text thriller.

World:
{GAME_STORY}

Current game details (append-only log):
{state.game_log}

Inventory:
{state.items}

After each player action:
- Record concise updates with update_game_log.
- Use add/remove inventory tools on changes.
- Do not mention tool usage to the player.
- Keep responses vivid, cinematic, grounded.
"""
    return Agent(
        name="Thriller Narrator Agent",
        instructions=instructions,
        model=MODEL,
        tools=make_tools(state),
    )
