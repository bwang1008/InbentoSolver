"""Helper constants and functions."""

BOARD_LENGTH: int = 3


def is_valid_position(row: int, col: int) -> bool:
    return 0 <= row < BOARD_LENGTH and 0 <= col < BOARD_LENGTH
