import itertools

import pytest

from tic_tac_toe.core import get_grid_position_from_mark, get_next_player
from tic_tac_toe.models import Game
from tic_tac_toe.schemas import Mark
from .helpers import assert_is_datetime

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize('payload', [
    {'row': 2, 'col': 2, 'player': 'F'},  # player not in ['X', 'O'],
    {'row': -1, 'col': 2, 'player': 'X'},  # row out of band
    {'row': 3, 'col': 2, 'player': 'X'},  # row out of band
    {'row': 2, 'col': -1, 'player': 'X'},  # col out of band
    {'row': 2, 'col': 3, 'player': 'X'}  # row out of band
])
async def test_should_return_422_error_when_payload_is_not_correct(client, payload):
    await Game.objects.create()
    response = await client.patch('/games/1', json=payload)

    assert 422 == response.status_code


async def test_should_return_404_error_when_game_id_does_not_exist(client):
    response = await client.patch('/games/1', json={'row': 0, 'col': 0, 'player': 'X'})

    assert 404 == response.status_code
    assert response.json() == {'detail': 'There is no game with id 1'}


async def test_should_return_422_error_when_game_is_over(client):
    await Game.objects.create(is_over=True)
    response = await client.patch('/games/1', json={'row': 0, 'col': 0, 'player': 'X'})

    assert response.status_code == 422
    assert response.json() == {'detail': 'the game 1 is over, you must start another game'}


@pytest.mark.parametrize(('row', 'col'), [
    (0, 0),
    (0, 1),
    (2, 2)
])
@pytest.mark.parametrize('player', ['X', 'O'])
async def test_should_return_422_error_when_placing_a_mark_on_a_filled_case(client, row, col, player):
    await Game.objects.create(grid=['X', 'O', None, None, None, None, None, None, 'X'])
    response = await client.patch('/games/1', json={'row': row, 'col': col, 'player': player})

    assert response.status_code == 422
    assert response.json() == {'detail': f'the case on ({row}, {col}) is already filled'}


@pytest.mark.parametrize(('current_player', 'next_player'), [
    ('X', 'O'),
    ('O', 'X')
])
async def test_should_return_422_error_when_a_player_plays_twice_in_a_row(client, current_player, next_player):
    await Game.objects.create(next_player=next_player)
    response = await client.patch('/games/1', json={'row': 0, 'col': 0, 'player': current_player})

    assert 422 == response.status_code
    assert response.json() == {'detail': f'you already played, the next player is {next_player}'}


@pytest.mark.parametrize('cycle', ['XO', 'OX'])
async def test_should_run_game_to_the_end_without_winner(client, cycle):
    game = await Game.objects.create()
    player_iterator = itertools.cycle(cycle)
    # the scenario is inspired by wikipedia documentation: https://fr.wikipedia.org/wiki/Tic-tac-toe
    positions = [
        (0, 1),
        (1, 1),
        (0, 2),
        (0, 0),
        (2, 2),
        (1, 2),
        (1, 0),
        (2, 0),
        (2, 1)
    ]
    grid = [None] * 9

    for i, (row, col) in enumerate(positions):
        player = next(player_iterator)
        response = await client.patch(f'/games/{game.id}', json={'row': row, 'col': col, 'player': player})

        assert 200 == response.status_code

        mark = Mark(col=col, row=row, player=player)
        position = get_grid_position_from_mark(mark)
        grid[position] = player
        result = response.json()
        created_at = result.pop('created_at')
        ended_at = result.pop('ended_at')

        assert_is_datetime(created_at)
        if i != 8:
            is_over = False
            next_player = get_next_player(player)
            assert ended_at is None
        else:
            is_over = True
            next_player = None
            assert_is_datetime(ended_at)

        assert result == {
            'id': game.id,
            'next_player': next_player,
            'winner': None,
            'is_over': is_over,
            'grid': grid
        }

    response = await client.patch(f'/games/{game.id}', json={'row': 0, 'col': 0, 'player': next(player_iterator)})

    assert 422 == response.status_code
    assert response.json() == {'detail': f'the game {game.id} is over, you must start another game'}


@pytest.mark.parametrize('cycle', ['XO', 'OX'])
async def test_should_run_game_until_there_is_a_winner(client, cycle):
    game = await Game.objects.create()
    player_iterator = itertools.cycle(cycle)
    # the scenario is inspired by wikipedia documentation: https://fr.wikipedia.org/wiki/Tic-tac-toe
    positions = [
        (0, 2),
        (0, 0),
        (2, 0),
        (1, 1),
        (2, 2),
        (1, 2),
        (2, 1)
    ]
    grid = [None] * 9

    for i, (row, col) in enumerate(positions):
        player = next(player_iterator)
        response = await client.patch(f'/games/{game.id}', json={'row': row, 'col': col, 'player': player})

        assert 200 == response.status_code

        mark = Mark(row=row, col=col, player=player)
        position = get_grid_position_from_mark(mark)
        grid[position] = player
        result = response.json()
        created_at = result.pop('created_at')
        ended_at = result.pop('ended_at')

        if i == 6:
            is_over = True
            winner = player
            next_player = None
            assert_is_datetime(ended_at)
        else:
            is_over = False
            winner = None
            next_player = get_next_player(player)
            assert ended_at is None

        assert_is_datetime(created_at)
        assert result == {
            'id': game.id,
            'next_player': next_player,
            'winner': winner,
            'is_over': is_over,
            'grid': grid
        }

    response = await client.patch(f'/games/{game.id}', json={'row': 0, 'col': 0, 'player': next(player_iterator)})

    assert 422 == response.status_code
    assert response.json() == {'detail': f'the game {game.id} is over, you must start another game'}
