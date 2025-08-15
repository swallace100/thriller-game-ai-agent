import json
import pytest
from pathlib import Path
from game.state import GameLogEntry, InventoryItem, ResearchLogEntry

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