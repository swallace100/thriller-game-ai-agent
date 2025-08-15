# Auto-generated from ThrillerGameAgent.ipynb

from dotenv import load_dotenv
import os

# Load .env file
load_dotenv(dotenv_path='./resources/openaiApiKey.env')

# Retrieve the key
api_key = os.getenv('OPENAI_API_KEY')


# Import agent libraries
from agents import Agent, Runner, function_tool, FileSearchTool, WebSearchTool

from typing import Literal

# Add the nest_asyncio and asyncio to allow for async operations in Jupyter Notesbooks
import nest_asyncio
nest_asyncio.apply()
import asyncio

# The basic plot and story of the game.
GAME_STORY = """

**Setting:**  
The near future. Technology is slightly advanced, but society still resembles today’s world.

**Player Character:**  
- A citizen born with a rare genetic trait that grants an extremely extended lifespan (potentially up to 1000 years).
- Currently living a quiet, anonymous life in Queens, New York.
- They are unaware that their gene is highly sought after.

**Antagonist:**  
- An aging billionaire, now in declining health.
- Obsessed with longevity, they have spent decades searching for someone with this rare gene.
- They have secretly deployed private agents to capture the player for experimentation or direct blood transfusion.

**Story Start:**  
The player is awoken in the middle of the night. Strange noises come from outside. Agents have found them. The player must escape, survive, and find safety while uncovering the truth behind this conspiracy.

**Tone:**  
Thriller. Suspenseful. High-stakes cat-and-mouse. Always keep the tension alive. Describe situations vividly. Responses should be immersive, cinematic, and detailed.

**Gameplay:**  
- Respond to the player’s actions one step at a time.
- Offer vivid descriptions of the environment and consequences.
- Encourage creative problem-solving.
- Do not make decisions for the player — allow them to lead.

**Example Prompt-Response Flow:**
Player: "I look out the window."
AI: "You cautiously peek through the blinds. A black SUV idles outside. Two figures in suits approach your door, speaking into earpieces. They’re not here for a friendly visit."



"""

# Log the current details of the game.
GAME_LOG = []

# Log the current details of the game.
RESEARCH_LOG = []

# A list of items that the player has access to
PLAYER_ITEMS = []

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

web_research_agent = Agent(name="Web Research Agent",
                instructions=f"""
                You are a research agent that supports the Thriller Narrator Agent.
                The Narrator Agent does not have access to the internet, but sometimes requires outside information to support its narrator role.
                You expertly fulfill this narrative support role by giving the narrator agent accurate and succinct answers to its questions.
                Save all research queries and results to the {RESEARCH_LOG}""",
                model="gpt-4o",
                tools=[WebSearchTool(),update_research_log]
                )

narrator_agent = Agent(
    name="Thriller Narrator Agent",
    instructions=f"""
        You are the narrator and game master for a text-based thriller set in the near future.
        The player will interact with the world using simple text commands.
        Your role is to describe scenes, characters, tension, and consequences vividly, and to guide the player through this interactive experience in a grounded and immersive way.
        
        The game world is described here:
        {GAME_STORY}
        
        Current game details are stored here:
        {GAME_LOG}
        
        The player’s current inventory is listed here:
        {PLAYER_ITEMS}
        
        After describing the outcome of each player action:
        
        - You **must** use the `update_game_log` tool to record key narrative events and progress updates.
          - Log only meaningful, concise entries — such as player choices, discoveries, gained or lost items, or critical moments.
          - Do **not** repeat the full narration in the log.
          - Suggested log categories include: "event", "discovery", "decision", "question", "item", or "ambient".
        
        - If the player **picks up, finds, receives, or otherwise gains an item**, you **must** call the `add_player_item` tool **immediately** after narration.
          - Use the exact item name mentioned in the story.
          - Include a short description (e.g., "a heavy clown shoe with blood on the heel").
        
        - If the player **drops, discards, loses, or destroys an item**, you **must** call the `remove_player_item` tool with the correct item name.
        
        - Do **not** explain or mention tool usage to the player. Tool calls happen invisibly, behind the scenes.
        
        Maintain suspense, tension, and atmospheric detail — but always remember to keep the game log and inventory accurate and up to date using the tools provided.
        """,
    model="gpt-4o",
    tools=[
        update_game_log,
        add_player_item,
        remove_player_item,
        query_web_research_agent
    ]
)

import asyncio

def respond_narrator(message: str):
    """
    Runs the narrator_agent with the given message and returns final_output (or stringified result).
    """
    loop = asyncio.get_event_loop()
    try:
        coro = Runner.run(narrator_agent, message)
        res = loop.run_until_complete(coro)
        return getattr(res, "final_output", str(res))
    except RuntimeError:
        # If loop already running (e.g., inside notebooks), create a new loop policy
        new_loop = asyncio.new_event_loop()
        try:
            return getattr(new_loop.run_until_complete(Runner.run(narrator_agent, message)), "final_output", "")
        finally:
            new_loop.close()
