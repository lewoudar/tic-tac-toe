from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional

import databases
import ormar
import sqlalchemy

from .settings import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class PlayerEnum(enum.Enum):
    X = 'X'
    O = 'O'


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Game(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'game'

    id: int = ormar.Integer(primary_key=True)
    winner: str = ormar.String(max_length=1, nullable=True, choices=list(PlayerEnum))
    is_over: bool = ormar.Boolean(default=False)
    next_player: str = ormar.String(max_length=1, nullable=True, choices=list(PlayerEnum))
    grid: list[Optional[str]] = ormar.JSON(default=[None] * 9)
    created_at: datetime = ormar.DateTime(default=datetime.utcnow)
    ended_at: datetime = ormar.DateTime(nullable=True)
