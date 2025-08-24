# tests/test_engine.py

import os
import time
from game.state import GameState

# --- helpers ---

def _wait_for_file(path: str, timeout: float = 2.0, poll: float = 0.05) -> None:
    """
    Block until the given file path exists, or raise AssertionError after timeout.

    Args:
        path: The file path to wait for.
        timeout: Maximum number of seconds to wait.
        poll: Sleep interval (seconds) between checks.

    Raises:
        AssertionError: If the file does not appear before timeout expires.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        if os.path.exists(path):
            return
        time.sleep(poll)
    raise AssertionError(f"Save file not created at {path}")


def load_save_data(path: str):
    """
    Load and parse a saved GameState from disk as a plain dictionary.

    This helper waits for the file to exist, then calls GameState.load_json()
    to reconstruct the state and converts it to a dict for easier assertions.

    Args:
        path: Path to the saved game JSON file.

    Returns:
        A dict representation of the GameState.
    """
    _wait_for_file(path)
    state = GameState.load_json(path)  # returns a new GameState instance
    return state.to_dict()


# --- tests ---

def test_respond_narrator_creates_save_file(fresh_thriller_modules, save_path):
    """
    Verify that calling respond_narrator creates a save file on disk.
    """
    _, _, state, _, engine = fresh_thriller_modules

    # Ensure a clean state
    state.default_state.game_log.clear()
    state.default_state.items.clear()

    response = engine.respond_narrator("Look around")
    assert isinstance(response, str), "Engine should return a string response"

    # Ensure save file was actually written
    load_save_data(save_path)
    assert os.path.exists(save_path), "Save file should exist after responding"


def test_save_file_structure(fresh_thriller_modules, save_path):
    """
    Verify that the save file contains the expected structure and keys.
    """
    _, _, _state, _, engine = fresh_thriller_modules

    engine.respond_narrator("Look around")        # write state to disk
    data = load_save_data(save_path)              # read state back

    # Verify required keys and types
    assert "game_log" in data
    assert "items" in data
    assert "research_log" in data
    assert isinstance(data["game_log"], list)
    assert isinstance(data["items"], list)
    assert isinstance(data["research_log"], list)


def test_game_state_persistence(fresh_thriller_modules, save_path):
    """
    Verify that multiple turns persist correctly to the save file.
    """
    _, _, _state, _, engine = fresh_thriller_modules

    # Perform two actions that should be logged
    engine.respond_narrator("Look around")
    engine.respond_narrator("Check inventory")
    data = load_save_data(save_path)

    # The game log should contain entries
    assert len(data["game_log"]) > 0, "Game log should record player actions"


def test_force_path_write(fresh_thriller_modules, monkeypatch, save_path):
    """
    Force the engine to write to a known save path via monkeypatching,
    and verify the file is created there.
    """
    _, _, _state, _tools, engine = fresh_thriller_modules

    # Assert engine is using the correct save path
    from game.state import _get_save_path
    assert _get_save_path() == save_path, \
        f"Engine would save to {_get_save_path()} but test expects {save_path}"

    # Monkeypatch save_state so it always writes to save_path
    import game.state as gs
    def forced_save_state(path=None):
        gs.default_state.save_json(save_path)
    monkeypatch.setattr(gs, "save_state", forced_save_state, raising=True)

    # Run one turn to trigger saving
    engine.respond_narrator("ping")

    # Verify the file now exists
    assert os.path.exists(save_path), f"Forced save did not create {save_path}"
