from agents import Agent
from ..content import GAME_STORY
from ..config import MODEL
from ..state import GameState
from ..tools import set_narrator_tools


def make_narrator(state: GameState, web_agent=None) -> Agent:
    instructions = f"""
You are the narrator and game master for a text thriller.

World:
{GAME_STORY}

Current game details (append-only log):
{state.game_log}

Inventory:
{state.items}

If you require real-world facts, call the tool `query_web_research_agent` with a concise question.
Record concise updates with update_game_log after each action. Use add/remove inventory tools on changes.
Do not mention tool usage to the player. Keep responses vivid, cinematic, and grounded.
""".strip()

    return Agent(
        name="Narrator Agent",
        instructions=instructions,
        model=MODEL,
        tools=set_narrator_tools(state, web_agent=web_agent),
    )
