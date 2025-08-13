# game/web_research.py
from agents import Agent
from ..config import MODEL
from logs import RESEARCH_LOG
from ..state import GameState
from ..tools import make_tools

def make_web_research_agent(state: GameState) -> Agent:
    instructions=f"""
    You are a research agent that supports the Thriller Narrator Agent.
    The Narrator Agent does not have access to the internet, but sometimes requires outside information to support its narrator role.
    You expertly fulfill this narrative support role by giving the narrator agent accurate and succinct answers to its questions.
    Save all research queries and results to the {RESEARCH_LOG}"""

    return Agent(
        name="Web Research Agent",
        instructions=instructions,
        model=MODEL,
        tools=make_tools(state),
    )