"""Utility functions to convert level info."""

from typing import List

from pydantic import BaseModel

from inbento_solver.board import Board
from inbento_solver.moves import MoveSubtypesT


class Level(BaseModel):
    """Class description of info in a puzzle level."""

    title: str
    start: Board
    finish: Board
    moves: List[MoveSubtypesT]  # noqa: FA100
