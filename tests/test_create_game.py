import pytest

from .helpers import assert_is_datetime


@pytest.mark.anyio
async def test_create_game_returns_correct_output(client):
    response = await client.post('/games/')
    assert response.status_code == 201
    result = response.json()
    created_at = result.pop('created_at')

    assert_is_datetime(created_at)
    assert result == {
        'id': 1,
        'winner': None,
        'is_over': False,
        'grid': [None] * 9,
        'next_player': None,
        'ended_at': None
    }
