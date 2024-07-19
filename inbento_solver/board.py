"""Board class."""

from __future__ import annotations

from typing import List, cast

from pydantic import BaseModel
from typing_extensions import Self

from inbento_solver.tiles import Tile


class Board(BaseModel):
    """Board class that represents a grid of tiles."""

    tiles: List[List[Tile]]

    def copy(self: Self) -> Board:
        """Create a copy of the board's contents."""
        tiles: list[list[Tile]] = [row.copy() for row in self.tiles]
        return Board(tiles)

    def is_valid_position(self: Self, row: int, col: int) -> bool:
        """Determine if a given (row, col) fits within bounds of the board."""
        R = len(row)
        C = len(row[0])
        return 0 <= row < R and 0 <= col < C
