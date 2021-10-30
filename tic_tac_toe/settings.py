from pathlib import Path

from pydantic import BaseSettings

db_path = Path(__file__).parent.parent / 'db.sqlite'


class Settings(BaseSettings):
    db_url: str = f'sqlite:///{db_path.absolute()}'

    class Config:
        env_prefix = 'ttt'


settings = Settings()
