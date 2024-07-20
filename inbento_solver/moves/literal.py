"""Implementation of a move that deposits a specified set of tiles."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal

from typing_extensions import Self

from inbento_solver.moves.base import Move
from inbento_solver.tiles import TilePosition

if TYPE_CHECKING:
    from inbento_solver.board import Board
    from inbento_solver.tiles import Tile


class LiteralMove(Move):
    """Represents a set of tiles that you can place on the board."""

    move_kind: Literal["literal"] = "literal"
    positions: List[TilePosition]  # noqa: UP006
    locked: bool = False

    def __str__(self: Self) -> str:
        """Representation of move."""
        nicer_positions: dict[tuple[int, int], str] = {
            tile_position.pos: tile_position.tile.name
            for tile_position in self.positions
        }
        return f"LiteralMove({nicer_positions})"

    def apply(
        self: Self, board: Board, start_pos: tuple[int, int]
    ) -> tuple[Board, Move | None, bool]:
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

    def rotate_counter_clockwise(self: Self) -> LiteralMove:
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

        return LiteralMove(positions=new_positions, locked=self.locked)
