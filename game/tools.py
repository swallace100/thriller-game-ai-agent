"""
Function tools used by the agents.
"""

from typing import TYPE_CHECKING, Awaitable, Callable, List, Literal, Optional, cast

from agents import Runner, function_tool

from game.state import GameLogEntry, InventoryItem, ResearchLogEntry, default_state

if TYPE_CHECKING:
    from agents import Agent


@function_tool
async def update_game_log(
    new_entry: str,
    category: Literal["event", "discovery", "decision", "question", "item", "ambient"] = "event",
) -> str:
    """Saves a structured log entry to the game log with a category."""
    default_state.game_log.append(GameLogEntry(category=category, entry=new_entry))
    return f"Game log updated with a {category} entry."


@function_tool
async def update_research_log(
    new_entry: str,
    category: Literal[
        "info", "symbol", "historical", "technical", "psychological", "warning"
    ] = "info",
) -> str:
    """Saves a structured log entry to the research log with a category."""
    default_state.research_log.append(ResearchLogEntry(category=category, entry=new_entry))
    return f"Research log updated with a {category} entry."


@function_tool
async def add_player_item(item_name: str, description: str = "") -> str:
    """Adds a new item to the player's inventory. Prevents duplicates by name."""
    if any(it.name == item_name for it in default_state.items):
        return f"{item_name} is already in your inventory."
    default_state.items.append(InventoryItem(name=item_name, description=description))
    return f"{item_name} added to your inventory."


@function_tool
async def remove_player_item(item_name: str) -> str:
    """Removes an item from the player's inventory by name."""
    for it in list(default_state.items):
        if it.name == item_name:
            default_state.items.remove(it)
            return f"{item_name} removed from your inventory."
    return f"{item_name} not found in your inventory."


# ---------------------------
# Safe bridge tool injection
# ---------------------------


def make_query_web_research_tool(web_agent: "Agent") -> Callable[[str], Awaitable[str]]:
    """
    Returns a function-tool that lets the Narrator query the Web Research Agent.
    Injects `web_agent` via closure to avoid importing from engine.py.
    """

    @function_tool
    async def query_web_research_agent(query: str) -> str:
        """
        Query the Web Research Agent for factual info.
        (For narrator use only; player should never see tool mechanics.)
        """
        try:
            resp = await Runner.run(web_agent, query)
            text = getattr(resp, "final_output", resp)
            # Persist Q&A to the research log for replayability/audit
            default_state.research_log.append(
                ResearchLogEntry(category="info", entry=f"Q: {query}\nA: {text}")
            )
            return str(text)
        except Exception as e:
            return f"[web research error] {e}"

    # function_tool likely returns `Any`; tell mypy what we return:
    return cast(Callable[[str], Awaitable[str]], query_web_research_agent)


def set_narrator_tools(state, web_agent: Optional[object] = None) -> List:
    """
    Creates a list of tools for the narrator agent.
    Only includes tools the narrator should have access to.
    If a web_agent is provided, inject a query bridge tool.
    """
    tools = [update_game_log, add_player_item, remove_player_item]
    if web_agent is not None:
        tools.append(make_query_web_research_tool(web_agent))
    return tools


def set_web_researcher_tools(state) -> List:
    """
    Creates a list of tools for the web researcher agent.
    """
    return [update_research_log]
