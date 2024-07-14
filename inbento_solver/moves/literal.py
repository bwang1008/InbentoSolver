"""Implementation of a move that deposits a specified set of tiles."""


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
