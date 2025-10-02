import pytest
import pytest_asyncio

# Mark all tests in this file as asyncio-enabled
pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def clean_state(fresh_thriller_modules):
    """
    Provides a clean in-memory game state and tools instance for each test.

    Yields:
        (state_module, tools_module): The imported state module (with
        default_state cleared) and the tools module bound to that state.
    """
    _, _, state, tools, _ = fresh_thriller_modules

    # Reset default_state before each test
    state.default_state.game_log.clear()
    state.default_state.items.clear()
    state.default_state.research_log.clear()

    yield state, tools


async def test_update_game_log(clean_state):
    """
    Ensure update_game_log creates a proper GameLogEntry
    and appends it to the default_state.
    """
    state, tools = clean_state

    # Act: update the log
    msg = await tools.update_game_log("I hear footsteps", category="ambient")

    # Assert: return message confirms action
    assert "Game log updated" in msg, "Should confirm log update"

    # Assert: state mutated correctly
    assert len(state.default_state.game_log) == 1, "Should have one entry"
    entry = state.default_state.game_log[0]
    assert isinstance(entry, state.GameLogEntry), "Should create proper GameLogEntry"
    assert entry.category == "ambient", "Should set correct category"
    assert entry.entry == "I hear footsteps", "Should store exact message"


async def test_inventory_management(clean_state):
    """
    Ensure add_player_item and remove_player_item work correctly
    and persist to default_state.items.
    """
    state, tools = clean_state

    # Act: add an item
    msg = await tools.add_player_item("flashlight", description="dim beam")

    # Assert: confirmation and state
    assert "added to your inventory" in msg, "Should confirm item addition"
    assert len(state.default_state.items) == 1, "Should have one item"
    item = state.default_state.items[0]
    assert isinstance(item, state.InventoryItem), "Should create proper InventoryItem"
    assert item.name == "flashlight", "Should store item name"
    assert item.description == "dim beam", "Should store item description"
    # Add duplicate
    msg_dup = await tools.add_player_item("flashlight")
    assert "already in your inventory" in msg_dup
    assert len(state.default_state.items) == 1

    # Act: remove the same item
    msg = await tools.remove_player_item("flashlight")

    # Assert: confirmation and state
    assert "removed from your inventory" in msg, "Should confirm item removal"
    assert len(state.default_state.items) == 0, "Should have empty inventory"


async def test_research_log(clean_state):
    """
    Ensure update_research_log creates an entry in default_state.research_log
    with the correct category and message.
    """
    state, tools = clean_state

    # Act: add research log entry
    msg = await tools.update_research_log(
        "DNA sequence matches known longevity markers", category="technical"
    )

    # Assert: confirmation and state
    assert "Research log updated" in msg, "Should confirm research update"
    assert len(state.default_state.research_log) == 1, "Should have one entry"

    entry = state.default_state.research_log[0]
    assert entry.category == "technical", "Should set correct category"
    assert "DNA sequence" in entry.entry, "Should store research info"


async def test_query_web_research_bridge(clean_state, monkeypatch):
    """
    Ensure the bridge tool calls Runner.run with the injected web agent,
    returns the agent's text, and appends a Q/A entry to research_log.
    """
    state, tools = clean_state

    # Create a fake web agent and a fake Runner.run that returns a rich-ish object
    class FakeAgent: ...

    fake_agent = FakeAgent()

    class FakeResult:
        def __init__(self, text):
            self.final_output = text

    calls = {}

    async def fake_run(agent, query):
        # capture the call for assertions
        calls["agent"] = agent
        calls["query"] = query
        return FakeResult("Longevity markers confirmed")

    # Patch Runner.run
    from agents import Runner

    monkeypatch.setattr(Runner, "run", fake_run, raising=True)

    # Build the bridge tool via the new factory and call it
    bridge = tools.make_query_web_research_tool(fake_agent)
    out = await bridge("What are FOXP2 markers?")

    # Returned text should be the agent's final_output
    assert "Longevity markers confirmed" in out

    # Bridge should have called Runner.run with our fake agent and query
    assert calls["agent"] is fake_agent
    assert calls["query"] == "What are FOXP2 markers?"

    # And persisted a Q/A entry into the research log
    assert len(state.default_state.research_log) == 1
    log_entry = state.default_state.research_log[0]
    assert "Q: What are FOXP2 markers?" in log_entry.entry
    assert "A: Longevity markers confirmed" in log_entry.entry
