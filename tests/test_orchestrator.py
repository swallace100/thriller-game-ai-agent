import json
import os
import pytest


class TestEngine:
    """Engine functionality tests"""

    def test_respond_narrator_creates_save_file(
        self,
        fresh_thriller_modules,
        save_path,
        monkeypatch,
    ):
        # Ensure engine autosave writes where we expect
        monkeypatch.setenv("THRILLER_SAVE_PATH", str(save_path))

        _, _, state, _, engine = fresh_thriller_modules
        state.default_state.game_log.clear()
        state.default_state.items.clear()
        state.default_state.research_log.clear()

        response = engine.respond_narrator("Look around")

        assert isinstance(response, str)
        assert response.strip() != ""
        assert os.path.exists(save_path), "Engine should autosave to THRILLER_SAVE_PATH"


class TestState:
    """Game state persistence tests"""

    def test_state_serialization(self, sample_game_state, game_save_path):
        state = sample_game_state
        # Instance convenience method should work and return the path
        written = state.save(str(game_save_path))
        assert str(game_save_path) == written

        data = json.loads(game_save_path.read_text(encoding="utf-8"))
        assert "game_log" in data
        assert "items" in data
        assert "research_log" in data


@pytest.mark.asyncio
class TestTools:
    """Game tools functionality tests"""

    async def test_game_tools(self, clean_state):
        state, tools = clean_state

        # Test game log
        msg = await tools.update_game_log("Test entry", category="event")
        assert "Game log updated" in msg
        assert len(state.default_state.game_log) == 1

        # Test inventory add
        msg = await tools.add_player_item("test_item")
        assert "added to your inventory" in msg
        assert len(state.default_state.items) == 1

        # (Optional) duplicate add guard
        dup = await tools.add_player_item("test_item")
        assert "already in your inventory" in dup
        assert len(state.default_state.items) == 1
