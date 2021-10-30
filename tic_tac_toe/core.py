"""This module includes logic game functions."""
from __future__ import annotations

from datetime import datetime

from typing_extensions import Literal

from .models import Game
from .schemas import Mark


def get_grid_position_from_mark(mark: Mark) -> int:
    positions = {
        (0, 0): 0,
        (0, 1): 1,
        (0, 2): 2,
        (1, 0): 3,
        (1, 1): 4,
        (1, 2): 5,
        (2, 0): 6,
        (2, 1): 7,
        (2, 2): 8
    }
    return positions[mark.coordinates()]


def extract_player_positions(game: Game, player: Literal['X', 'O']) -> set[int]:
    return {i for i, mark in enumerate(game.grid) if mark == player}


# noinspection PyTypeChecker
def get_next_player(player: Literal['X', 'O']) -> Literal['X', 'O']:
    return 'X' if player == 'O' else 'O'


def player_has_won(game: Game, player: Literal['X', 'O']) -> bool:
    winning_combinations = [
        {0, 1, 2},
        {3, 4, 5},
        {6, 7, 8},
        {0, 3, 6},
        {1, 4, 7},
        {2, 5, 8},
        {0, 4, 8},
        {2, 4, 6}
    ]
    positions = extract_player_positions(game, player)
    for combination in winning_combinations:
        if combination.issubset(positions):
            return True
    return False


async def update_grid(game: Game, position: int, player: Literal['X', 'O']) -> None:
    # grid = game.grid[::]
    # grid[position] = player
    # game.grid = grid
    game.grid[position] = player
    game.next_player = get_next_player(player)

    if player_has_won(game, player):
        game.is_over = True
        game.ended_at = datetime.utcnow()
        game.winner = player
        game.next_player = None

    if all(i in ['X', 'O'] for i in game.grid):
        game.is_over = True
        game.ended_at = datetime.utcnow()
        game.next_player = None

    await game.update()
