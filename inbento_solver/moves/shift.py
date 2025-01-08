"""Implementation of a move that shifts existing tiles a space over."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from typing_extensions import Self

from inbento_solver.direction import Direction
from inbento_solver.moves.base import MoveBase
from inbento_solver.tiles import Tile

if TYPE_CHECKING:
    from inbento_solver.board import Board


class ShiftMove(MoveBase):
    """Represents a set of tiles that each move on top of a neighbor."""

    move_type: Literal["shift"] = "shift"

    def __str__(self: Self) -> str:
        """Representation of move."""
        nicer_positions: dict[tuple[int, int], str] = {
            tile_position.pos: tile_position.tile.name
            for tile_position in self.positions
        }
        return f"ShiftMove({nicer_positions})"

    def apply(
        self: Self, board: Board, start_pos: tuple[int, int]
    ) -> tuple[Board, MoveBase | None, bool]:
        """Directly apply the move's tile on top of the existing board tiles."""
        board_copy = board.model_copy(deep=True)

        for tile_position in self.positions:
            pos: tuple[int, int] = tile_position.pos
            direction: Direction | None = tile_position.direction
            if direction is None:
                error_msg: str = (
                    "Cannot have a ShiftMove without a direction to shift in"
                )
                raise RuntimeError(error_msg)
            direction_delta: tuple[int, int] = Direction.get_delta(direction)

            original_row: int = pos[0] + start_pos[0]
            original_col: int = pos[1] + start_pos[1]
            replace_row: int = original_row + direction_delta[0]
            replace_col: int = original_col + direction_delta[1]

            if not board.is_valid_position(
                original_row, original_col
            ) or not board.is_valid_position(replace_row, replace_col):
                return board, None, False

            tile_to_be_moved: Tile = board_copy.tiles[original_row][original_col]
            board_copy.tiles[original_row][original_col] = Tile.EMPTY
            if tile_to_be_moved != Tile.EMPTY:
                board_copy.tiles[replace_row][replace_col] = tile_to_be_moved

        return board_copy, None, True
