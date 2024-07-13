"""Transformations that act on a Board object."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from typing_extensions import Self

if TYPE_CHECKING:
    from .board import Board
    from .tiles import Tile


class Move:
    """Base class that represents all moves appliable to a board."""

    def __init__(self: Self, locked: bool) -> None:
        """Store information about what a move can do to a board."""
        self.locked: bool = locked

    @abstractmethod
    def apply(
        self: Self, board: Board, start_pos: tuple[int, int]
    ) -> tuple[Board, Move | None, bool]:
        """Return a board that is modified from applying the move.

        The second return value is any move that can be applied later.
        The third return value indicates if the apply operation was successful.
        """
        raise NotImplementedError("Not implemented in base class")

    @abstractmethod
    def rotate_counter_clockwise(self: Self) -> Move:
        """Apply rotation to move."""
        raise NotImplementedError("Not implemented in base class")

    def is_locked(self: Self) -> bool:
        """Return attribute locked."""
        return self.locked


class LiteralMove(Move):
    """Represents a set of tiles that you can place on the board."""

    def __init__(
        self: Self, tile_positions: dict[tuple[int, int], Tile], locked: bool
    ) -> None:
        """Hold which (row, col) positions hold which tiles."""
        self.tile_positions = tile_positions
        self.locked = locked

    def __str__(self: Self) -> str:
        """Representation of move."""
        nicer_tile_positions: dict[tuple[int, int], str] = {
            pos: tile.name for pos, tile in self.tile_positions.items()
        }
        return f"LiteralMove({nicer_tile_positions})"

    def apply(
        self: Self, board: Board, start_pos: tuple[int, int]
    ) -> tuple[Board, Move | None, bool]:
        """Directly apply the move's tile on top of the existing board tiles."""
        board_copy = board.copy()

        for pos, tile in self.tile_positions.items():
            row: int = pos[0] + start_pos[0]
            col: int = pos[1] + start_pos[1]

            if not board.is_valid_position(row, col):
                return board, None, False

            board_copy.tiles[row][col] = tile

        return board_copy, None, True

    def rotate_counter_clockwise(self: Self) -> LiteralMove:
        """Turn the set of tiles in the move."""
        if self.locked:
            return self

        max_col = max(col for _, col in self.tile_positions)

        new_tile_positions: dict[tuple[int, int], Tile] = {
            (max_col - pos[1], pos[0]): tile
            for pos, tile in self.tile_positions.items()
        }

        return LiteralMove(new_tile_positions, self.locked)
