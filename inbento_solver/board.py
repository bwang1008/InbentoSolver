"""Board class."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from typing_extensions import Self

if TYPE_CHECKING:
    from .tiles import Tile


class Board:
    """Board class that represents a grid of tiles."""

    def __init__(self: Self, tiles: list[list[Tile]]) -> None:
        """Create instance of Board class.

        Input is a 2D array of tiles.
        """
        self.R = len(tiles)
        self.C = len(tiles[0])
        self.tiles = tiles

    def __eq__(self: Self, other: object) -> bool:
        """Check equality between Board instances."""
        if not isinstance(other, Board):
            return False

        other = cast(Board, other)
        if self.R != other.R or self.C != other.C:
            return False
        for i in range(self.R):
            for j in range(self.C):
                if self.tiles[i][j] != other.tiles[i][j]:
                    return False

        return True


    def copy(self: Self) -> 'Board':
        tiles: list[list[Tile]] = [[tile for tile in row] for row in self.tiles]
        return Board(tiles)
