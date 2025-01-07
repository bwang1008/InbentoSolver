"""Transformations that act on a Board object."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

from pydantic import BaseModel
from typing_extensions import Self

from inbento_solver.tiles import TilePosition

if TYPE_CHECKING:
    from inbento_solver.board import Board
    from inbento_solver.tiles import Tile


class MoveBase(ABC, BaseModel):
    """Base class that represents all moves appliable to a board."""

    move_type: str
    positions: List[TilePosition]  # noqa: UP006
    locked: bool = False

    @abstractmethod
    def apply(
        self: Self, board: Board, start_pos: tuple[int, int]
    ) -> tuple[Board, MoveBase | None, bool]:
        """Return a board that is modified from applying the move.

        The second return value is any move that can be applied later.
        The third return value indicates if the apply operation was successful.
        """
        msg: str = "Not implemented in base class"
        raise NotImplementedError(msg)

    def rotate_counter_clockwise(self: Self) -> MoveBase:
        """Turn the set of tiles in the move."""
        if self.locked:
            return self

        max_col: int = max(tile_position.pos[1] for tile_position in self.positions)

        new_positions: list[TilePosition] = []
        for tile_position in self.positions:
            pos: tuple[int, int] = tile_position.pos
            tile: Tile = tile_position.tile

            new_tile_position: TilePosition = TilePosition(
                pos=(max_col - pos[1], pos[0]), tile=tile
            )
            new_positions.append(new_tile_position)

        return type(self)(
            move_type=self.move_type, positions=new_positions, locked=self.locked
        )

    def distinct_rotations(self) -> list[tuple[MoveBase, int]]:
        """Return all rotations of the current move that are distinct."""
        distinct_moves: list[tuple[MoveBase, int]] = [(self, 0)]
        while (
            next_move := distinct_moves[-1][0].rotate_counter_clockwise()
        ) != distinct_moves[0][0]:
            distinct_moves.append((next_move, 1 + distinct_moves[-1][1]))
        return distinct_moves

    def is_locked(self: Self) -> bool:
        """Return attribute locked."""
        return bool(self.locked)


class MoveDescription:
    """Struct holding all information related to how a move was specifically applied."""

    def __init__(
        self: Self,
        original_move: MoveBase,
        applied_move: MoveBase,
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
