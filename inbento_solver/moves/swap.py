"""Implementation of a move that swaps two existing tiles."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal

from typing_extensions import Self

from inbento_solver.moves.base import MoveBase
from inbento_solver.tiles import TilePosition

if TYPE_CHECKING:
    from inbento_solver.board import Board
    from inbento_solver.tiles import Tile


class SwapMove(MoveBase):
    """Represents a set of tiles that can swap two existing tiles."""

    move_type: Literal["swap"] = "swap"
    positions: List[TilePosition]  # noqa: UP006

    def __str__(self: Self) -> str:
        """Representation of move."""
        nicer_positions: dict[tuple[int, int], str] = {
            tile_position.pos: tile_position.tile.name
            for tile_position in self.positions
        }
        return f"SwapMove({nicer_positions})"

    def apply(
        self: Self, board: Board, start_pos: tuple[int, int]
    ) -> tuple[Board, MoveBase | None, bool]:
        """Directly apply the move's tile on top of the existing board tiles."""
        board_copy = board.model_copy(deep=True)

        pos1: tuple[int, int] = self.positions[0].pos
        row1: int = pos1[0] + start_pos[0]
        col1: int = pos1[1] + start_pos[1]
        if not board.is_valid_position(row1, col1):
            return board, None, False

        pos2: tuple[int, int] = self.positions[1].pos
        row2: int = pos2[0] + start_pos[0]
        col2: int = pos2[1] + start_pos[1]
        if not board.is_valid_position(row2, col2):
            return board, None, False

        orig: Tile = board_copy.tiles[row1][col1]
        board_copy.tiles[row1][col1] = board_copy.tiles[row2][col2]
        board_copy.tiles[row2][col2] = orig

        return board_copy, None, True

    def rotate_counter_clockwise(self: Self) -> SwapMove:
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

        return SwapMove(positions=new_positions, locked=self.locked)