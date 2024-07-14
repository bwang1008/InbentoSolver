"""Utility functions to convert level info."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Dict, List, Union, cast

from inbento_solver.board import Board
from inbento_solver.moves.literal import LiteralMove

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
    moves_info: list[dict[str, str | dict[str, bool | list[list[str]]]]] = level_info[
        "moves"
    ]

    moves: list[Move] = []

    for move_info in moves_info:
        if move_info["type"] == "literal":
            move_data: dict[str, bool | list[list[str]]] = cast(
                Dict[str, Union[bool, List[List[str]]]], move_info["data"]
            )

            moves.append(LiteralMove.from_json(move_data))

    return title, start_board, finish_board, moves
