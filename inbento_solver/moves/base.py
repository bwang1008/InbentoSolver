"""Transformations that act on a Board object."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from pydantic import BaseModel
from typing_extensions import Self

if TYPE_CHECKING:
    from inbento_solver.board import Board


class Move(ABC, BaseModel):
    """Base class that represents all moves appliable to a board."""

    locked: bool = False

    @abstractmethod
    def apply(
        self: Self, board: Board, start_pos: tuple[int, int]
    ) -> tuple[Board, Move | None, bool]:
        """Return a board that is modified from applying the move.

        The second return value is any move that can be applied later.
        The third return value indicates if the apply operation was successful.
        """
        msg: str = "Not implemented in base class"
        raise NotImplementedError(msg)

    @abstractmethod
    def rotate_counter_clockwise(self: Self) -> Move:
        """Apply rotation to move."""
        msg: str = "Not implemented in base class"
        raise NotImplementedError(msg)

    def is_locked(self: Self) -> bool:
        """Return attribute locked."""
        return bool(self.locked)


class MoveDescription:
    """Struct holding all information related to how a move was specifically applied."""

    def __init__(
        self: Self,
        original_move: Move,
        applied_move: Move,
        num_rotations: int,
        pos: tuple[int, int],
    ) -> None:
        """Take in information on how move was applied.

        For instance, how many times a move/piece was rotated, and which
        row and column to apply the move on the board.
        """
        self.original_move = original_move
        self.applied_move = applied_move
        self.num_rotations = num_rotations
        self.pos = pos

    def __str__(self: Self) -> str:
        """Human-readable text showing how to apply the move."""
        ret: str = ""

        if self.original_move != self.applied_move:
            ret = f"Rotate {self.original_move}"

            num_ccw_turn_1 = 1
            num_ccw_turn_2 = 2
            num_ccw_turn_3 = 3

            if self.num_rotations == num_ccw_turn_1:
                ret += " counterclockwise. "
            elif self.num_rotations == num_ccw_turn_2:
                ret += " clockwise twice. "
            elif self.num_rotations == num_ccw_turn_3:
                ret += " clockwise. "

        ret += f"Apply {self.applied_move} at row {self.pos[0]}, column {self.pos[1]}"

        return ret
