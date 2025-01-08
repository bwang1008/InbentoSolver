"""Represent the 4 cardinal directions."""

from __future__ import annotations

from enum import Enum


class Direction(str, Enum):
    """Cardinal directions enumeration."""

    RIGHT = "RIGHT"
    UP = "UP"
    LEFT = "LEFT"
    DOWN = "DOWN"

    @classmethod
    def get_delta(cls, direction: Direction) -> tuple[int, int]:
        """Retrieve row delta and column delta to move in this direction."""
        if direction == Direction.RIGHT:
            return (0, 1)
        if direction == Direction.UP:
            return (-1, 0)
        if direction == Direction.LEFT:
            return (0, -1)
        return (1, 0)

    @classmethod
    def rotate_counter_clockwise(cls, direction: Direction) -> Direction:
        """Retrieve direction that is 90 degrees counterclockwise."""
        if direction == Direction.RIGHT:
            return Direction.UP
        if direction == Direction.UP:
            return Direction.LEFT
        if direction == Direction.LEFT:
            return Direction.DOWN
        return Direction.RIGHT
