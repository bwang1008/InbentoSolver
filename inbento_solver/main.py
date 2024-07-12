"""Main application code."""

from __future__ import annotations

from typing import TYPE_CHECKING

import typer

from inbento_solver.board import Board
from inbento_solver.move import LiteralMove, Move
from inbento_solver.solver import Solver
from inbento_solver.tiles import Tile

if TYPE_CHECKING:
    from pathlib import Path


app = typer.Typer()


@app.command()
def solve(level_file: Path) -> None:
    """Given a level file, find the list of moves that solve the puzzle."""
    print(f"Searching for file {level_file}")


@app.command()
def test() -> None:
    """Solves a dummy puzzle."""
    initial_board: Board = Board([[Tile.RICE]])
    finish_board: Board = Board([[Tile.SALMON]])
    moves: list[Move] = [LiteralMove({(0, 0): Tile.SALMON}, True)]

    solver: Solver = Solver(initial_board, finish_board, moves)
    history: list[Move] = solver.solve()

    print(f"History: {history}")


if __name__ == "__main__":
    app()
