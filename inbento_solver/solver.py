"""Solver applies remaining moves until the input matches the output."""

from __future__ import annotations

from typing import TYPE_CHECKING

from loguru import logger
from typing_extensions import Self

if TYPE_CHECKING:
    from inbento_solver.board import Board
    from inbento_solver.move import Move


class Solver:
    """Solver class that tries all remaining moves."""

    def __init__(
        self: Self, start_board: Board, finish_board: Board, moves: list[Move]
    ) -> None:
        """Take in a level's inputs.

        Inputs include:
            - Starting board
            - Final board
            - List of moves that should be used to transform initial board
            into the final board
        """
        self.start_board: Board = start_board
        self.finish_board: Board = finish_board
        self.initial_moves: list[Move] = moves
        # scratch variables
        self.current_board: Board = start_board.copy()
        self.unapplied_moves: list[Move] = moves.copy()
        self.history: list[tuple[Move, Move, int, int]] = []

    def solve(self: Self) -> list[tuple[Move, Move, int, int]]:
        """Recursively try any remaining move until a match occurs at the end."""
        result: bool = self._recursively_try_all_unapplied_moves()
        if not result:
            logger.warning("No solution found")
            return []

        return self.history

    def _recursively_try_all_unapplied_moves(self: Self) -> bool:
        """For each available move, apply it and recursve on remaining moves."""
        if not len(self.unapplied_moves):
            return self.current_board == self.finish_board

        for move in self.unapplied_moves.copy():
            self.unapplied_moves.remove(move)

            # try all rotations of move as well
            derivative_moves: list[Move] = [move]
            if not move.is_locked():
                for _ in range(4):
                    rotated_move: Move = derivative_moves[-1].rotate_counter_clockwise()
                    derivative_moves.append(rotated_move)

            for derivative_move in derivative_moves:
                # try all spots in the board to apply the operation
                for row_index in range(self.current_board.R):
                    for col_index in range(self.current_board.C):
                        before_board: Board = self.current_board.copy()
                        new_board, remaining_move, successful = derivative_move.apply(
                            self.current_board,
                            (row_index, col_index),
                        )
                        if not successful:
                            continue

                        self.history.append(
                            (move, derivative_move, row_index, col_index)
                        )

                        self.current_board = new_board
                        search_result: bool = (
                            self._recursively_try_all_unapplied_moves()
                        )
                        if search_result:
                            return True
                        self.current_board = before_board

                        self.history.pop()

            self.unapplied_moves.append(move)

        return False
