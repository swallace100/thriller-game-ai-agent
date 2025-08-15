# game/narrator.py
from agents import Agent
from ..content import GAME_STORY
from ..config import MODEL
from ..state import GameState
from ..tools import set_narrator_tools

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
        tools=set_narrator_tools(state),
    )
