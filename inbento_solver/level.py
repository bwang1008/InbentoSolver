"""Utility functions to convert level info."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Dict, List, cast

from inbento_solver.board import Board
from inbento_solver.moves.literal import LiteralMove
from inbento_solver.tiles import Tile

if TYPE_CHECKING:
    from pathlib import Path

    from inbento_solver.moves.base import Move


def parse_level(level_path: Path) -> tuple[str, Board, Board, list[Move]]:
    """Extract level data from JSON file."""
    with level_path.open(mode="r", encoding="utf-8") as level_file:
        level_info = json.load(level_file)

    title: str = level_info["title"]
    start_board: Board = Board(level_info["start"])
    finish_board: Board = Board(level_info["finish"])
    moves_info: list[dict[str, str | dict[str, list[list[str]]] | bool]] = level_info[
        "moves"
    ]

    moves: list[Move] = []

    for move_info in moves_info:
        locked: bool = False
        if "locked" in move_info:
            locked = cast(bool, move_info["locked"])

        if move_info["type"] == "literal":
            move_data: dict[str, list[list[str]]] = cast(
                Dict[str, List[List[str]]], move_info["data"]
            )

            tile_positions: dict[tuple[int, int], Tile] = {}
            for row_index, row in enumerate(move_data["positions"]):
                for col_index, tile_info in enumerate(row):
                    tile_positions[(row_index, col_index)] = Tile[tile_info]

            moves.append(LiteralMove(tile_positions, locked))

    return title, start_board, finish_board, moves
