"""Transformations that act on a Board object."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from typing_extensions import Self

if TYPE_CHECKING:
    from inbento_solver.board import Board


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


class MoveDescription:
    """Struct holding all information related to how a move was specifically applied."""

    def __init__(  # noqa: PLR0913
        self: Self,
        original_move: Move,
        applied_move: Move,
        num_rotations: int,
        row_index: int,
        col_index: int,
    ) -> None:
        """Take in information on how move was applied.

        For instance, how many times a move/piece was rotated, and which
        row and column to apply the move on the board.
        """
        self.original_move = original_move
        self.applied_move = applied_move
        self.num_rotations = num_rotations
        self.row_index = row_index
        self.col_index = col_index

    def __str__(self: Self) -> str:
        """Human-readable text showing how to apply the move."""
        ret: str = ""

        if self.original_move != self.applied_move:
            ret = f"Rotate {self.original_move}"

            NUM_CCW_TURN_1 = 1
            NUM_CCW_TURN_2 = 3
            NUM_CCW_TURN_3 = 3

            if self.num_rotations == NUM_CCW_TURN_1:
                ret += " counterclockwise."
            elif self.num_rotations == NUM_CCW_TURN_2:
                ret += " clockwise twice."
            elif self.num_rotations == NUM_CCW_TURN_3:
                ret += " clockwise."

        ret += (
            f"Apply {self.applied_move} at row {self.row_index},"
            f" column {self.col_index}"
        )

        return ret