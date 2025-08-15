import os
import sys
import types
import json
import importlib
import tempfile
import shutil
import pytest

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
            # Very small simulation: echo with a prefix
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


@pytest.fixture(scope="function", autouse=True)
def temp_save_path_env(monkeypatch, tmp_path):
    """
    For each test, point THRILLER_SAVE_PATH to a unique temp file under a temp dir.
    """
    save_dir = tmp_path / "runs"
    save_dir.mkdir(parents=True, exist_ok=True)
    save_path = save_dir / "session_latest.json"
    monkeypatch.setenv("THRILLER_SAVE_PATH", str(save_path))
    yield


@pytest.fixture(scope="function")
def fresh_thriller_modules():
    """
    Ensure we load game modules fresh each test so state doesn't leak.
    """
    # Remove any cached imports
    for name in list(sys.modules):
        if name == "game" or name.startswith("game."):
            del sys.modules[name]

    # Import in dependency order
    game = importlib.import_module("game")
    content = importlib.import_module("game.content")
    state = importlib.import_module("game.state")
    tools = importlib.import_module("game.tools")
    api = importlib.import_module("game.api")
    return game, content, state, tools, api
