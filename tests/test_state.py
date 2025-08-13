import json

def test_state_save_and_load(fresh_thriller_modules, tmp_path):
    _, _, state, _, _ = fresh_thriller_modules
    # Mutate default state
    state.default_state.game_log.clear()
    state.default_state.research_log.clear()
    state.default_state.items.clear()

    state.default_state.game_log.append(
        state.GameLogEntry(category="event", entry="Door kicked open")
    )
    state.default_state.items.append(
        state.InventoryItem(name="keycard", description="Blue access card")
    )

    p = tmp_path / "save.json"
    state.save_state(str(p))

    # Sanity check file
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["game_log"][0]["entry"] == "Door kicked open"
    assert data["items"][0]["name"] == "keycard"

    # Load into memory and verify
    state.load_state(str(p))
    assert state.default_state.game_log[0].entry == "Door kicked open"
    assert state.default_state.items[0].name == "keycard"
