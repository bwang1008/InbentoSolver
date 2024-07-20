"""Enums for various tiles that can appear in a board."""

from __future__ import annotations

from enum import Enum, auto
from typing import Tuple

from pydantic import BaseModel


class Tile(Enum):
    """Tile enumerations."""

    EMPTY = auto()
    RICE = auto()
    SALMON = auto()
    EGG = auto()
    EGG_SWIRL = auto()
    TOMATO = auto()


class TilePosition(BaseModel):
    """Combination of tile and (row, col) position."""

    pos: Tuple[int, int]  # noqa: UP006
    tile: Tile
