import pytest
import sqlalchemy
from async_asgi_testclient import TestClient

from tic_tac_toe.models import metadata
from tic_tac_toe.settings import settings


@pytest.fixture(autouse=True)
def create_test_database():
    engine = sqlalchemy.create_engine(settings.db_url)
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)


@pytest.fixture()
async def client():
    from tic_tac_toe.main import app
    async with TestClient(app) as client:
        yield client


@pytest.fixture
def anyio_backend():
    return 'asyncio'
