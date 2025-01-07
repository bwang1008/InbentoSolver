"""Implementation of a move that deposits a specified set of tiles."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from typing_extensions import Self

from inbento_solver.moves.base import MoveBase

if TYPE_CHECKING:
    from inbento_solver.board import Board
    from inbento_solver.tiles import Tile


class LiteralMove(MoveBase):
    """Represents a set of tiles that you can place on the board."""

    move_type: Literal["literal"] = "literal"

    def __str__(self: Self) -> str:
        """Representation of move."""
        nicer_positions: dict[tuple[int, int], str] = {
            tile_position.pos: tile_position.tile.name
            for tile_position in self.positions
        }
        return f"LiteralMove({nicer_positions})"

    def apply(
        self: Self, board: Board, start_pos: tuple[int, int]
    ) -> tuple[Board, MoveBase | None, bool]:
        """Directly apply the move's tile on top of the existing board tiles."""
        board_copy = board.model_copy(deep=True)

        for tile_position in self.positions:
            pos: tuple[int, int] = tile_position.pos
            tile: Tile = tile_position.tile
            row: int = pos[0] + start_pos[0]
            col: int = pos[1] + start_pos[1]

            if not board.is_valid_position(row, col):
                return board, None, False

            board_copy.tiles[row][col] = tile

        return board_copy, None, True
