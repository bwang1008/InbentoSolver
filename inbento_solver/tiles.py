"""Enums for various tiles that can appear in a board."""

from __future__ import annotations

from enum import Enum
from typing import Tuple

from pydantic import BaseModel


class Tile(str, Enum):
    """Tile enumerations."""

    EMPTY = "EMPTY"
    RICE = "RICE"
    SALMON = "SALMON"
    EGG = "EGG"
    EGG_SWIRL = "EGG_SWIRL"
    TOMATO = "TOMATO"


class TilePosition(BaseModel):
    """Combination of tile and (row, col) position."""

    pos: Tuple[int, int]  # noqa: UP006
    tile: Tile
