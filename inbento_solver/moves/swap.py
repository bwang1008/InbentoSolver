"""Implementation of a move that swaps two existing tiles."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal

from typing_extensions import Self

from inbento_solver.moves.base import MoveBase
from inbento_solver.tiles import TilePosition  # noqa: TC001

if TYPE_CHECKING:
    from inbento_solver.board import Board


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
        raise NotImplementedError

    def rotate_counter_clockwise(self: Self) -> SwapMove:
        """Turn the set of tiles in the move."""
        raise NotImplementedError
