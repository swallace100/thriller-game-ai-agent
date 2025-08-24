import sys
import types
import importlib
import pytest

@pytest.fixture
def save_path(monkeypatch, tmp_path) -> str:
    """
    Each test gets its own save file path and we export THRILLER_SAVE_PATH so
    the engine writes to this location.
    """
    p = tmp_path / "runs" / "session_latest.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("THRILLER_SAVE_PATH", str(p))
    if p.exists():
        p.unlink()

    print("save path " + str(p))
    return str(p)

@pytest.fixture(scope="session", autouse=True)
def fake_agents_module():
    """
    Provide a fake 'agents' module so thriller.* imports work in tests without the real dependency.
    - function_tool: identity decorator for async functions
    - Agent: simple container
    - Runner.run: returns a stub result object with a final_output attribute
    - WebSearchTool: placeholder
    """
    mod = types.ModuleType("agents")

    def function_tool(fn):
        # Identity decorator: return original async function unchanged
        return fn

    class Agent:
        def __init__(self, name, instructions, model, tools):
            self.name = name
            self.instructions = instructions
            self.model = model
            self.tools = tools

    class _Result:
        def __init__(self, final_output):
            self.final_output = final_output

    class Runner:
        @staticmethod
        async def run(agent, message):
            """
            Simulate a minimal agent step:
            - if a tool named 'update_game_log' exists, call it to record the turn
            - then return a simple final_output
            """
            # Find a tool by name or fallback to the first tool that accepts (new_entry, category)
            tool_fn = None
            for t in getattr(agent, "tools", []):
                name = getattr(t, "__name__", "")
                if name == "update_game_log":
                    tool_fn = t
                    break
            if tool_fn is None and agent.tools:
                # naive heuristic: try the first tool and ignore if it fails
                tool_fn = agent.tools[0]

            # Call the tool to mutate state (best-effort)
            if tool_fn is not None:
                try:
                    await tool_fn(f"Player action: {message}", category="event")
                except TypeError:
                    # tool signature didn't match; ignore
                    pass

            return _Result(f"[{agent.name}] {message}")

    class WebSearchTool:
        pass

    mod.function_tool = function_tool
    mod.Agent = Agent
    mod.Runner = Runner
    mod.WebSearchTool = WebSearchTool

    sys.modules["agents"] = mod
    try:
        yield
    finally:
        # leave the fake module in place for the session
        pass

@pytest.fixture(scope="function")
def fresh_thriller_modules(save_path):  # <-- depend on save_path
    # purge cached game modules so they re-read env
    for name in list(sys.modules):
        if name == "game" or name.startswith("game."):
            del sys.modules[name]

    game = importlib.import_module("game")
    # adjust this to your actual module names:
    # e.g., if it's game.story not game.content, import that.
    content = importlib.import_module("game.content")
    state = importlib.import_module("game.state")
    tools = importlib.import_module("game.tools")
    api = importlib.import_module("game.api")
    return game, content, state, tools, api

@pytest.fixture(scope="function")
def sample_game_state():
    """
    Returns a populated GameState instance (does not touch default_state).
    """
    # Adjust import names to match your codebase:
    from game.state import GameState, GameLogEntry, InventoryItem, ResearchLogEntry

    st = GameState()
    st.game_log.append(GameLogEntry(category="event", entry="Arrived at the scene"))
    st.items.append(InventoryItem(name="keycard", description="A worn corporate keycard"))
    st.research_log.append(ResearchLogEntry(category="info", entry="The logo matches Orpheus Labs"))
    return st

@pytest.fixture(scope="function")
def game_save_path(tmp_path):
    """
    A file path you can pass to state.save_* methods inside tests.
    """
    p = tmp_path / "runs" / "state.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

@pytest.fixture(scope="function")
def clean_state(fresh_thriller_modules):
    """
    Resets in-memory default_state and returns (state_module, tools_module).
    Keep this sync; your async tests can still 'await' tool calls.
    """
    _, _, state_mod, tools_mod, _ = fresh_thriller_modules
    state_mod.default_state.game_log.clear()
    state_mod.default_state.items.clear()
    state_mod.default_state.research_log.clear()
    return state_mod, tools_mod
