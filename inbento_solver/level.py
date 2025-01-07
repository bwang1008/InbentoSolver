"""Utility functions to convert level info."""

from __future__ import annotations

from typing import List

from pydantic import BaseModel

from inbento_solver.board import Board  # noqa: TC001
from inbento_solver.moves import MoveSubtypesT  # noqa: TC001


class Level(BaseModel):
    """Class description of info in a puzzle level."""

    title: str
    start: Board
    finish: Board
    moves: List[MoveSubtypesT]  # noqa: UP006
