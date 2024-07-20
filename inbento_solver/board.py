"""Board class."""

from __future__ import annotations

from typing import List

from pydantic import BaseModel
from typing_extensions import Self

from inbento_solver.tiles import Tile  # noqa: TCH001


class Board(BaseModel):
    """Board class that represents a grid of tiles."""

    tiles: List[List[Tile]]  # noqa: UP006

    def is_valid_position(self: Self, row: int, col: int) -> bool:
        """Determine if a given (row, col) fits within bounds of the board."""
        r = len(self.tiles)
        c = len(self.tiles[0])
        return 0 <= row < r and 0 <= col < c
