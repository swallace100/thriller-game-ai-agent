import json
import os

def test_respond_narrator_autosaves(fresh_thriller_modules):
    _, _, state, _, engine = fresh_thriller_modules

    # Ensure clean start
    state.default_state.game_log.clear()
    state.default_state.items.clear()

    # Call the entrypoint
    out = engine.respond_narrator("Look around")
    assert isinstance(out, str)
    assert "Look around" in out  # echoed by the fake Runner

    # Autosave should have happened to THRILLER_SAVE_PATH
    import os
    save_path = os.getenv("THRILLER_SAVE_PATH")
    assert save_path and os.path.exists(save_path)

    data = json.loads(open(save_path, "r", encoding="utf-8").read())
    # Game log might be empty if the LLM didn't call the tool in this stub,
    # but the file should still have structure.
    assert "game_log" in data and "items" in data and "research_log" in data
