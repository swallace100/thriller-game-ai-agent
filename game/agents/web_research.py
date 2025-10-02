from agents import Agent
from ..config import MODEL
from ..state import GameState
from ..tools import set_web_researcher_tools


def make_web_research_agent(state: GameState) -> Agent:
    instructions = f"""
You are the Research Agent that supports the Narrator Agent.
The Narrator Agent does not have internet access and sometimes needs outside facts.
Answer accurately and succinctly. Save all research queries and results to the state's research log.
Current research log (append-only view): {state.research_log}
""".strip()

    return Agent(
        name="Web Research Agent",
        instructions=instructions,
        model=MODEL,
        tools=set_web_researcher_tools(state),
    )
