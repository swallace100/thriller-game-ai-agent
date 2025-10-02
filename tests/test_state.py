import json
import pytest
from pathlib import Path
from game.state import (
    GameLogEntry,
    InventoryItem,
    ResearchLogEntry,
    GameState,
    GameState,
    default_state,
    save_state,
    load_state,
)
import time
import json
import pytest
from pathlib import Path


@pytest.fixture
def game_save_path(tmp_path) -> Path:
    """Provides a temporary path for save files"""
    return tmp_path / "save.json"


@pytest.fixture
def sample_game_state(fresh_thriller_modules):
    """Creates a sample game state with known data"""
    _, _, state, _, _ = fresh_thriller_modules

    # Start with clean state
    state.default_state.game_log.clear()
    state.default_state.research_log.clear()
    state.default_state.items.clear()

    # Add sample data
    state.default_state.game_log.append(
        GameLogEntry(category="event", entry="Door kicked open")
    )
    state.default_state.items.append(
        InventoryItem(name="keycard", description="Blue access card")
    )
    state.default_state.research_log.append(
        ResearchLogEntry(category="technical", entry="DNA analysis complete")
    )

    return state


def test_state_serialization(sample_game_state, game_save_path):
    """Test that game state can be properly saved to JSON"""
    state = sample_game_state

    # Save state to file
    state.save_state(str(game_save_path))

    # Verify JSON structure
    data = json.loads(game_save_path.read_text(encoding="utf-8"))

    assert "game_log" in data, "Save should contain game_log"
    assert "items" in data, "Save should contain items"
    assert "research_log" in data, "Save should contain research_log"

    assert len(data["game_log"]) == 1, "Should save one game log entry"
    assert len(data["items"]) == 1, "Should save one inventory item"
    assert len(data["research_log"]) == 1, "Should save one research entry"

    assert data["game_log"][0]["entry"] == "Door kicked open"
    assert data["items"][0]["name"] == "keycard"
    assert data["research_log"][0]["entry"] == "DNA analysis complete"


def test_state_deserialization(sample_game_state, game_save_path):
    """Test that game state can be properly loaded from JSON"""
    state = sample_game_state

    # Save and clear state
    state.save_state(str(game_save_path))
    state.default_state.game_log.clear()
    state.default_state.items.clear()
    state.default_state.research_log.clear()

    # Load back and verify
    state.load_state(str(game_save_path))

    assert len(state.default_state.game_log) == 1
    assert len(state.default_state.items) == 1
    assert len(state.default_state.research_log) == 1

    assert state.default_state.game_log[0].entry == "Door kicked open"
    assert state.default_state.game_log[0].category == "event"

    assert state.default_state.items[0].name == "keycard"
    assert state.default_state.items[0].description == "Blue access card"

    assert state.default_state.research_log[0].entry == "DNA analysis complete"
    assert state.default_state.research_log[0].category == "technical"


def test_invalid_save_file(sample_game_state, game_save_path):
    """Test handling of corrupted or invalid save files"""
    # Write invalid JSON
    game_save_path.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        sample_game_state.load_state(str(game_save_path))


def test_to_from_dict_roundtrip(sample_game_state):
    state = sample_game_state.default_state  # the module's default_state instance
    data = state.to_dict()
    restored = GameState.from_dict(data)

    assert len(restored.game_log) == 1
    assert len(restored.items) == 1
    assert len(restored.research_log) == 1
    assert restored.game_log[0].entry == "Door kicked open"
    assert restored.items[0].name == "keycard"
    assert restored.research_log[0].entry == "DNA analysis complete"


def test_timestamps_present_and_reasonable(sample_game_state, game_save_path):
    state_mod = sample_game_state
    # add fresh entries to observe ts
    state_mod.default_state.game_log.append(
        state_mod.GameLogEntry(category="event", entry="test")
    )
    state_mod.default_state.research_log.append(
        state_mod.ResearchLogEntry(category="info", entry="test")
    )
    t0 = time.time()
    state_mod.save_state(str(game_save_path))
    data = json.loads(game_save_path.read_text(encoding="utf-8"))

    gl_ts = data["game_log"][-1]["ts"]
    rl_ts = data["research_log"][-1]["ts"]
    assert isinstance(gl_ts, (int, float))
    assert isinstance(rl_ts, (int, float))
    # timestamps should be within a small window of when we saved
    assert gl_ts <= t0 + 5
    assert rl_ts <= t0 + 5


def test_env_default_save_path(monkeypatch, tmp_path, sample_game_state):
    # Point THRILLER_SAVE_PATH to a temp location and use module-level helpers
    target = tmp_path / "env_save.json"
    monkeypatch.setenv("THRILLER_SAVE_PATH", str(target))

    # module-level helpers should pick up env var via _get_save_path
    from game import state as state_mod

    state_mod.save_state()  # no arg ⇒ uses env path
    assert target.exists(), "save_state() should respect THRILLER_SAVE_PATH"

    # clear & reload via env default
    state_mod.default_state.game_log.clear()
    state_mod.default_state.items.clear()
    state_mod.default_state.research_log.clear()
    state_mod.load_state()  # no arg ⇒ uses env path

    assert len(state_mod.default_state.game_log) >= 1


def test_load_state_missing_file_raises(tmp_path, monkeypatch):
    # Ensure a nonexistent path is used
    missing = tmp_path / "no_such_dir" / "missing.json"
    monkeypatch.setenv("THRILLER_SAVE_PATH", str(missing))

    from game import state as state_mod

    with pytest.raises(FileNotFoundError):
        state_mod.load_state()


def _seed_state(mod_state):
    """Helper to seed default_state deterministically."""
    mod_state.default_state.game_log.clear()
    mod_state.default_state.items.clear()
    mod_state.default_state.research_log.clear()
    mod_state.default_state.game_log.append(
        mod_state.GameLogEntry(category="event", entry="Knock at the door")
    )
    mod_state.default_state.items.append(
        mod_state.InventoryItem(name="flashlight", description="dim beam")
    )
    mod_state.default_state.research_log.append(
        mod_state.ResearchLogEntry(category="info", entry="Unknown symbol: Λ-17")
    )


def test_instance_savejson_then_module_load(sample_game_state, tmp_path):
    """
    Write a state file using the INSTANCE method (save_json),
    then load it using the MODULE helper (load_state).
    """
    state_mod = sample_game_state
    _seed_state(state_mod)
    p = tmp_path / "roundtrip_instance_to_module.json"

    # Instance save_json
    state_mod.default_state.save_json(str(p))

    # Clear default_state and load via module helper
    state_mod.default_state.game_log.clear()
    state_mod.default_state.items.clear()
    state_mod.default_state.research_log.clear()

    load_state(str(p))  # module-level load

    assert len(default_state.game_log) == 1
    assert len(default_state.items) == 1
    assert len(default_state.research_log) == 1
    assert default_state.game_log[0].entry == "Knock at the door"
    assert default_state.items[0].name == "flashlight"
    assert default_state.research_log[0].entry == "Unknown symbol: Λ-17"


def test_module_save_then_instance_loadjson(sample_game_state, tmp_path):
    """
    Write a state file using the MODULE helper (save_state),
    then read it using the CLASS method (GameState.load_json).
    """
    state_mod = sample_game_state
    _seed_state(state_mod)
    p = tmp_path / "roundtrip_module_to_instance.json"

    # Module save_state (operates on module default_state)
    save_state(str(p))

    # Instance/class load_json
    loaded = GameState.load_json(str(p))

    assert len(loaded.game_log) == 1
    assert len(loaded.items) == 1
    assert len(loaded.research_log) == 1
    assert loaded.game_log[0].entry == "Knock at the door"
    assert loaded.items[0].name == "flashlight"
    assert loaded.research_log[0].entry == "Unknown symbol: Λ-17"


def test_instance_save_convenience_honors_env(monkeypatch, sample_game_state, tmp_path):
    """
    GameState.save() without a path should honor THRILLER_SAVE_PATH and return that path.
    """
    state_mod = sample_game_state
    _seed_state(state_mod)

    target = tmp_path / "env_default.json"
    monkeypatch.setenv("THRILLER_SAVE_PATH", str(target))

    # Instance convenience save (no explicit path)
    returned = state_mod.default_state.save()  # should pick up env via _get_save_path
    assert returned == str(target)
    assert target.exists()

    # Sanity: load via module helper and verify content
    state_mod.default_state.game_log.clear()
    state_mod.default_state.items.clear()
    state_mod.default_state.research_log.clear()
    load_state()  # uses env default
    assert len(default_state.game_log) == 1
    assert default_state.game_log[0].entry == "Knock at the door"


def test_save_json_creates_nested_dirs(sample_game_state, tmp_path):
    """
    save_json should create intermediate directories when given a nested path.
    """
    state_mod = sample_game_state
    _seed_state(state_mod)

    nested = tmp_path / "deep" / "nested" / "state.json"
    # Ensure parent doesn't exist yet
    assert not nested.parent.exists()

    state_mod.default_state.save_json(str(nested))
    assert nested.exists(), "save_json should create parent directories and file"

    # Quick load to confirm valid JSON
    loaded = GameState.load_json(str(nested))
    assert len(loaded.game_log) == 1
