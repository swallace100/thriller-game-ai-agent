import pytest
from game.state import GameLogEntry, InventoryItem

pytestmark = pytest.mark.asyncio

@pytest.fixture
async def clean_state(fresh_thriller_modules):
    """Fixture to provide clean state for each test"""
    _, _, state, tools, _ = fresh_thriller_modules
    state.default_state.game_log.clear()
    state.default_state.items.clear()
    state.default_state.research_log.clear()
    return state, tools

async def test_update_game_log(clean_state):
    state, tools = clean_state
    
    # Test basic log entry
    msg = await tools.update_game_log("I hear footsteps", category="ambient")
    assert "Game log updated" in msg, "Should confirm log update"
    assert len(state.default_state.game_log) == 1, "Should have one entry"
    
    entry = state.default_state.game_log[0]
    assert isinstance(entry, GameLogEntry), "Should create proper GameLogEntry"
    assert entry.category == "ambient", "Should set correct category"
    assert entry.entry == "I hear footsteps", "Should store exact message"

async def test_inventory_management(clean_state):
    state, tools = clean_state
    
    # Test adding item
    msg = await tools.add_player_item("flashlight", description="dim beam")
    assert "added to your inventory" in msg, "Should confirm item addition"
    assert len(state.default_state.items) == 1, "Should have one item"
    
    item = state.default_state.items[0]
    assert isinstance(item, InventoryItem), "Should create proper InventoryItem"
    assert item.name == "flashlight", "Should store item name"
    assert item.description == "dim beam", "Should store item description"
    
    # Test removing item
    msg = await tools.remove_player_item("flashlight")
    assert "removed from your inventory" in msg, "Should confirm item removal"
    assert len(state.default_state.items) == 0, "Should have empty inventory"

async def test_research_log(clean_state):
    state, tools = clean_state
    
    # Test research log entry
    msg = await tools.update_research_log(
        "DNA sequence matches known longevity markers", 
        category="technical"
    )
    assert "Research log updated" in msg, "Should confirm research update"
    assert len(state.default_state.research_log) == 1, "Should have one entry"
    
    entry = state.default_state.research_log[0]
    assert entry.category == "technical", "Should set correct category"
    assert "DNA sequence" in entry.entry, "Should store research info"