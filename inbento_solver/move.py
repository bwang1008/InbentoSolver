"""Transformations that act on a Board object."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from typing_extensions import Self

from inbento_solver.utils import is_valid_position

if TYPE_CHECKING:
    from .board import Board
    from .tiles import Tile

class Move:
    """Base class that represents all moves appliable to a board."""

    def __init__(self: Self, locked: bool) -> None:
        self.locked: bool = locked

    @abstractmethod
    def apply(self: Self, board: Board, start_pos: Tuple[int, int]) -> Tuple[Board, Move, bool]:
        """Return a board that is modified from applying the move.

        The second return value is any move that can be applied later.
        The third return value indicates if the apply operation was successful.
        """
        raise NotImplementedError("Not implemented in base class")

    @abstractmethod
    def rotate_counter_clockwise(self: Self) -> None:
        raise NotImplementedError("Not implemented in base class")


class LiteralMove:
    """Represents a set of tiles that you can place on the board."""

    def __init__(self: Self, tile_positions: dict[Tuple[int, int], Tile], locked: bool) -> None:
        self.tile_positions = tile_positions
        self.locked = locked

    def apply(self: Self, board: Board, start_pos: Tuple[int, int]) -> Tuple[Board, Move, int]:
        board_copy = board.copy()

        for pos, tile in self.tile_positions.items():
            row: int = pos[0] + start_pos[0]
            col: int = pos[1] + start_pos[1]

            if not is_valid_position(row, col):
                return board, None, False

            board_copy.tiles[row][col] = tile

        return board_copy, None, True


    def rotate_counter_clockwise(self) -> LiteralMove:
        if self.locked:
            return self

        max_col = max(col for _, col in self.tile_positions)

        new_tile_positions: dict[Tuple[int, int], Tile] = {
            (max_col - pos[1], pos[0]): tile for pos, tile in self.tile_positions.items()
        }

        return LiteralMove(new_tile_positions, self.locked)
