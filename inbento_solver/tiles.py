"""Enums for various tiles that can appear in a board."""

from enum import Enum, auto


class Tile(Enum):
    """Tile enumerations."""

    EMPTY = auto()
    RICE = auto()
    SALMON = auto()
    EGG = auto()
    EGG_SWIRL = auto()
