"""
Function tools used by the agents.
"""

from typing import Literal, List
from agents import function_tool
from game.state import default_state, GameLogEntry, ResearchLogEntry, InventoryItem


@function_tool
async def update_game_log(new_entry: str, category: Literal["event", "discovery", "decision", "question", "item", "ambient"] = "event") -> str:
    """
    Saves a structured log entry to the game log with a category.
    """
    default_state.game_log.append(GameLogEntry(category=category, entry=new_entry))
    return f"Game log updated with a {category} entry."


@function_tool
async def update_research_log(new_entry: str, category: Literal["info", "symbol", "historical", "technical", "psychological", "warning"] = "info") -> str:
    """
    Saves a structured log entry to the research log with a category.
    """
    default_state.research_log.append(ResearchLogEntry(category=category, entry=new_entry))
    return f"Research log updated with a {category} entry."


@function_tool
async def add_player_item(item_name: str, description: str = "") -> str:
    """
    Adds a new item to the player's inventory. Prevents duplicates by name.
    """
    if any(it.name == item_name for it in default_state.items):
        return f"{item_name} is already in your inventory."

    default_state.items.append(InventoryItem(name=item_name, description=description))
    return f"{item_name} added to your inventory."


@function_tool
async def remove_player_item(item_name: str) -> str:
    """
    Removes an item from the player's inventory by name.
    """
    for it in list(default_state.items):
        if it.name == item_name:
            default_state.items.remove(it)
            return f"{item_name} removed from your inventory."
    return f"{item_name} not found in your inventory."

def set_narrator_tools(state) -> List:
    """
    Creates a list of tools for the narrator agent.
    Only includes tools the narrator should have access to.
    """
    return [
        update_game_log,
        add_player_item,
        remove_player_item
    ]

def set_web_researcher_tools(state) -> List:
    """
    Creates a list of tools for the narrator agent.
    Only includes tools the narrator should have access to.
    """
    return [
        update_research_log
    ]