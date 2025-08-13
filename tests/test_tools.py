import pytest

pytestmark = pytest.mark.asyncio

async def test_update_game_log_and_items(fresh_thriller_modules):
    _, _, state, tools, _ = fresh_thriller_modules

    # Start clean
    state.default_state.game_log.clear()
    state.default_state.items.clear()

    msg = await tools.update_game_log("I hear footsteps", category="ambient")
    assert "Game log updated" in msg
    assert len(state.default_state.game_log) == 1
    assert state.default_state.game_log[0].category == "ambient"

    msg = await tools.add_player_item("flashlight", description="dim beam")
    assert "added to your inventory" in msg
    assert len(state.default_state.items) == 1
    assert state.default_state.items[0].name == "flashlight"

    msg = await tools.remove_player_item("flashlight")
    assert "removed from your inventory" in msg
    assert len(state.default_state.items) == 0
