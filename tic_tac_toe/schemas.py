from __future__ import annotations

from pydantic import BaseModel, Field
from typing_extensions import Literal


class Mark(BaseModel):
    row: int = Field(..., gt=-1, lt=3, description='value on the x-axis of the grid')
    col: int = Field(..., gt=-1, lt=3, description='value on the y-axis of the grid')
    player: Literal['X', 'O'] = Field(..., description='the current player')

    def coordinates(self) -> tuple[int, int]:
        return self.row, self.col
