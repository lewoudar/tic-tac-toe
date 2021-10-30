import pytest

from tic_tac_toe.core import get_grid_position_from_mark, get_next_player, extract_player_positions, player_has_won
from tic_tac_toe.models import Game
from tic_tac_toe.schemas import Mark

pytestmark = pytest.mark.anyio


class TestGetGridPositionFromMark:
    """Tests function get_grid_position_from_mark"""

    @pytest.mark.parametrize(('mark', 'position'), [
        (Mark(col=1, row=1, player='X'), 4),
        (Mark(col=0, row=0, player='O'), 0),
        (Mark(col=2, row=2, player='X'), 8)
    ])
    def test_should_return_grid_position_given_row_and_column(self, mark, position):
        assert position == get_grid_position_from_mark(mark)


class TestGetNextPlayer:
    """Tests function get_next_player"""

    @pytest.mark.parametrize(('current', 'following'), [
        ('X', 'O'),
        ('O', 'X')
    ])
    def test_should_return_next_player_given_correct_input(self, current, following):
        assert following == get_next_player(current)


@pytest.mark.usefixtures('client')
class TestExtractPlayerPositions:
    """Tests function extract_player_positions"""

    @pytest.mark.parametrize('player', ['X', 'O'])
    async def test_should_return_empty_set_if_player_has_not_played(self, player):
        game = await Game.objects.create()
        assert set() == extract_player_positions(game, player)  # type: ignore

    @pytest.mark.parametrize('player', ['X', 'O'])
    async def test_should_return_a_set_of_player_positions(self, player):
        expected_positions = {2, 4, 8}
        game = await Game.objects.create()

        for position in expected_positions:
            game.grid[position] = player

        await game.update()

        assert expected_positions == extract_player_positions(game, player)  # type: ignore


@pytest.mark.usefixtures('client')
class TestPlayerHasWon:
    """Tests function player_has_won"""

    @pytest.mark.parametrize('player', ['X', 'O'])
    async def test_should_return_false_when_player_has_not_won(self, player):
        game = await Game.objects.create()

        for position in [0, 1, 5]:
            game.grid[position] = player

        await game.update()

        assert not player_has_won(game, player)  # type: ignore

    @pytest.mark.parametrize('player', ['X', 'O'])
    @pytest.mark.parametrize('positions', [
        [0, 1, 7, 4],
        [2, 6, 4, 3]
    ])
    async def test_should_return_true_when_player_has_won(self, player, positions):
        game = await Game.objects.create()

        for position in positions:
            game.grid[position] = player

        await game.update()

        assert player_has_won(game, player)  # type: ignore
