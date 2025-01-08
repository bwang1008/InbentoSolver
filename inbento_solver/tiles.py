"""Enums for various tiles that can appear in a board."""

from __future__ import annotations

from enum import Enum
from typing import Optional, Tuple

from pydantic import BaseModel

from inbento_solver.direction import Direction  # noqa: TC001


class Tile(str, Enum):
    """Tile enumerations."""

    EMPTY = "EMPTY"
    RICE = "RICE"
    SALMON = "SALMON"
    EGG = "EGG"
    EGG_SWIRL = "EGG_SWIRL"
    TOMATO = "TOMATO"
    SPINACH = "SPINACH"
    STICKY_RICE = "STICKY_RICE"
    YELLOWFISH = "YELLOWFISH"
    CHESTNUT = "CHESTNUT"
    SWAP = "SWAP"
    SHIFT = "SHIFT"


class TilePosition(BaseModel):
    """Combination of tile and (row, col) position."""

    pos: Tuple[int, int]  # noqa: UP006
    tile: Tile
    direction: Optional[Direction] = None  # noqa: UP007
