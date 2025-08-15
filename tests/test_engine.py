import json
import os
import pytest
from typing import Dict, Any

@pytest.fixture
def save_path():
    path = os.getenv("THRILLER_SAVE_PATH")
    assert path is not None, "THRILLER_SAVE_PATH environment variable must be set"
    # Cleanup any existing save file
    if os.path.exists(path):
        os.remove(path)
    return path

@pytest.fixture
def load_save_data(save_path) -> Dict[str, Any]:
    """Helper to load and parse save file"""
    with open(save_path, "r", encoding="utf-8") as f:
        return json.loads(f.read())

def test_respond_narrator_creates_save_file(fresh_thriller_modules, save_path):
    _, _, state, _, engine = fresh_thriller_modules
    
    # Ensure clean start
    state.default_state.game_log.clear()
    state.default_state.items.clear()
    
    # Test basic response
    response = engine.respond_narrator("Look around")
    assert isinstance(response, str), "Response should be a string"
    assert "Look around" in response, "Response should acknowledge the command"
    
    # Verify save file exists
    assert os.path.exists(save_path), f"Save file not created at {save_path}"

def test_save_file_structure(fresh_thriller_modules, save_path, load_save_data):
    _, _, state, _, engine = fresh_thriller_modules
    
    # Generate some game state
    engine.respond_narrator("Look around")
    
    # Check save file structure
    data = load_save_data
    assert "game_log" in data, "Save file missing game_log"
    assert "items" in data, "Save file missing items"
    assert "research_log" in data, "Save file missing research_log"
    assert isinstance(data["game_log"], list), "game_log should be a list"
    assert isinstance(data["items"], list), "items should be a list"
    assert isinstance(data["research_log"], list), "research_log should be a list"

def test_game_state_persistence(fresh_thriller_modules, save_path, load_save_data):
    _, _, state, _, engine = fresh_thriller_modules
    
    # Add some game state
    engine.respond_narrator("Look around")
    engine.respond_narrator("Check inventory")
    
    # Verify state was saved
    data = load_save_data
    assert len(data["game_log"]) > 0, "Game log should record actions"
    
    # Clean up
    if os.path.exists(save_path):
        os.remove(save_path)