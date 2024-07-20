"""Utility functions to convert level info."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, List

from pydantic import BaseModel

from inbento_solver.board import Board  # noqa: TCH001
from inbento_solver.moves import MoveSubtypesT  # noqa: TCH001

if TYPE_CHECKING:
    from pathlib import Path


class Level(BaseModel):
    """Class description of info in a puzzle level."""

    title: str
    start: Board
    finish: Board
    moves: List[MoveSubtypesT]  # noqa: UP006


def parse_level(level_path: Path) -> Level:
    """Extract level data from JSON file."""
    with level_path.open(mode="r", encoding="utf-8") as level_file:
        level_info = json.load(level_file)

    level: Level = Level.model_validate(level_info)
    return level
