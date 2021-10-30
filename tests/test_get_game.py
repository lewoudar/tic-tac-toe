import pytest

from .helpers import assert_is_datetime

pytestmark = pytest.mark.anyio


async def test_should_return_422_error_when_game_id_is_not_an_integer(client):
    response = await client.get('/games/foo')

    assert 422 == response.status_code
    assert response.json() == {
        'detail': [
            {
                'loc': ['path', 'game_id'],
                'msg': 'value is not a valid integer',
                'type': 'type_error.integer'
            }
        ]
    }


async def test_should_return_404_error_when_game_id_does_not_exist(client):
    response = await client.get('/games/1')
    assert 404 == response.status_code

    assert response.json() == {'detail': 'There is no game with id 1'}


async def test_should_return_game_info_when_giving_correct_game_id(client):
    await client.post('/games/')
    response = await client.get('/games/1')

    assert 200 == response.status_code
    result = response.json()
    created_at = result.pop('created_at')

    assert_is_datetime(created_at)

    assert result == {
        'id': 1,
        'is_over': False,
        'winner': None,
        'next_player': None,
        'ended_at': None,
        'grid': [None] * 9
    }
