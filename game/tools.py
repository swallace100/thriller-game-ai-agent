# game/tools.py
from typing import Literal
from agents import function_tool  # from openai-agents SDK
from .state import GameState, LogCat, ResearchCat

def make_tools(state: GameState):
    @function_tool
    async def update_game_log(new_entry: str, category: Literal["event", "discovery", "decision", "question", "item", "ambient"] = "event") -> str:
        """
        Saves a structured log entry to the game log with a category.
        """
        global GAME_LOG
        GAME_LOG.append({
            "category": category,
            "entry": new_entry
        })
        return f"Game log updated with a {category} entry."

    @function_tool
    async def update_research_log(new_entry: str, category: Literal["info", "symbol", "historical", "technical", "psychological", "warning"] = "info") -> str:
        """
        Saves a structured log entry to the research log with a category.
        """
        global RESEARCH_LOG
        RESEARCH_LOG.append({
            "category": category,
            "entry": new_entry
        })
        return f"Research log updated with a {category} entry."

    @function_tool
    async def add_player_item(item_name: str, description: str = "") -> str:
        """
        Adds a new item to the player's inventory.
        Each item is stored as a dictionary with a name and optional description.
        """
        global PLAYER_ITEMS
        # Prevent duplicate item names
        if any(item["name"] == item_name for item in PLAYER_ITEMS):
            return f"{item_name} is already in your inventory."

        PLAYER_ITEMS.append({
            "name": item_name,
            "description": description
        })
        return f"{item_name} added to your inventory."

    @function_tool
    async def remove_player_item(item_name: str) -> str:
        """
        Removes an item from the player's inventory by name.
        """
        global PLAYER_ITEMS
        for item in PLAYER_ITEMS:
            if item["name"] == item_name:
                PLAYER_ITEMS.remove(item)
                return f"{item_name} removed from your inventory."

        return f"{item_name} not found in your inventory."

    @function_tool
    async def query_web_research_agent(query: str) -> str:
        """
        Allows the narrator agent to query the Web Research Agent for factual information.
        This tool is only for the narrator's use — the player should never see it being called.
        """
        response = await coroutine
        return response

    return [update_game_log, update_research_log, add_player_item, remove_player_item, query_web_research_agent]
