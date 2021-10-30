from fastapi import APIRouter, HTTPException, Depends, Path

from .core import get_grid_position_from_mark, update_grid
from .models import Game
from .schemas import Mark

router = APIRouter(
    prefix='/games',
    tags=['games'],
    responses={404: {'description': 'Not found'}},
)


async def get_db_game(game_id: int = Path(..., description='game id', example=1)) -> Game:
    game = await Game.objects.get_or_none(id=game_id)
    if game is None:
        raise HTTPException(status_code=404, detail=f'There is no game with id {game_id}')
    return game


@router.get('/{game_id}', response_model=Game, description='gets information from a game')
async def get_game(game: Game = Depends(get_db_game)):
    return game


@router.post('/', response_model=Game, status_code=201, description='creates a game')
async def create_game():
    game = await Game.objects.create()
    return game


@router.patch('/{game_id}', response_model=Game, description='updates a game')
async def update_game(mark: Mark, game: Game = Depends(get_db_game)):
    if game.is_over:
        raise HTTPException(status_code=422, detail=f'the game {game.id} is over, you must start another game')

    if game.next_player is not None and game.next_player != mark.player:
        raise HTTPException(status_code=422, detail=f'you already played, the next player is {game.next_player}')

    grid_position = get_grid_position_from_mark(mark)
    if game.grid[grid_position] is not None:
        raise HTTPException(status_code=422, detail=f'the case on {mark.coordinates()} is already filled')

    await update_grid(game, grid_position, mark.player)
    return game
