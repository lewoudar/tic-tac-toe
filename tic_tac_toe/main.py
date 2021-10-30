from fastapi import FastAPI

from .api import router
from .models import database


async def start_db_connection():
    if not database.is_connected:
        await database.connect()


async def close_db_connection():
    if database.is_connected:
        await database.disconnect()


app = FastAPI(
    title='Tic Tac Toe api',
    description='An api to play tic tac toe game',
    version='0.1.0',
    licence_info={
        'name': 'MIT',
        'url': 'https://opensource.org/licenses/MIT'
    },
    redoc_url=None,
    on_startup=[start_db_connection],
    on_shutdown=[close_db_connection]
)
app.include_router(router)
