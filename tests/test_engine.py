import os
import time
from game.state import GameState

# --- helpers ---


def _wait_for_file(path: str, timeout: float = 2.0, poll: float = 0.05) -> None:
    """
    Block until the given file path exists, or raise AssertionError after timeout.
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
    """
    _wait_for_file(path)
    state = GameState.load_json(path)  # returns a new GameState instance
    return state.to_dict()


# --- tests ---


def test_respond_narrator_creates_save_file(
    fresh_thriller_modules, save_path, monkeypatch
):
    """
    Verify that calling respond_narrator creates a save file on disk.
    """
    # Ensure engine writes where we expect
    monkeypatch.setenv("THRILLER_SAVE_PATH", str(save_path))

    _, _, state, _, engine = fresh_thriller_modules

    # Ensure a clean state
    state.default_state.game_log.clear()
    state.default_state.items.clear()
    state.default_state.research_log.clear()

    response = engine.respond_narrator("Look around")
    assert isinstance(response, str), "Engine should return a string response"

    # Ensure save file was actually written
    load_save_data(save_path)
    assert os.path.exists(save_path), "Save file should exist after responding"


def test_save_file_structure(fresh_thriller_modules, save_path, monkeypatch):
    """
    Verify that the save file contains the expected structure and keys.
    """
    monkeypatch.setenv("THRILLER_SAVE_PATH", str(save_path))

    _, _, _state, _, engine = fresh_thriller_modules

    engine.respond_narrator("Look around")  # write state to disk
    data = load_save_data(save_path)  # read state back

    # Verify required keys and types
    assert "game_log" in data
    assert "items" in data
    assert "research_log" in data
    assert isinstance(data["game_log"], list)
    assert isinstance(data["items"], list)
    assert isinstance(data["research_log"], list)


def test_game_state_persistence(fresh_thriller_modules, save_path, monkeypatch):
    """
    Verify that multiple turns persist correctly to the save file.
    """
    monkeypatch.setenv("THRILLER_SAVE_PATH", str(save_path))

    _, _, _state, _, engine = fresh_thriller_modules

    # Perform two actions that should be logged
    engine.respond_narrator("Look around")
    engine.respond_narrator("Check inventory")
    data = load_save_data(save_path)

    # The game log should contain entries (>= 2 is a stronger check)
    assert len(data["game_log"]) >= 2, "Game log should record multiple player actions"


def test_force_path_write_via_env(fresh_thriller_modules, monkeypatch, save_path):
    """
    Force the engine to write to a known save path via THRILLER_SAVE_PATH,
    and verify the file is created there.
    """
    monkeypatch.setenv("THRILLER_SAVE_PATH", str(save_path))

    _, _, _state, _tools, engine = fresh_thriller_modules

    # Run one turn to trigger saving
    engine.respond_narrator("ping")

    # Verify the file now exists
    _wait_for_file(save_path)
    assert os.path.exists(save_path), f"Expected save at {save_path}"
