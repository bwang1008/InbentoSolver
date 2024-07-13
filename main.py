"""Main application code."""

from __future__ import annotations

from pathlib import Path  # noqa: TCH003

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from inbento_solver.board import Board
from inbento_solver.level import parse_level
from inbento_solver.move import LiteralMove, Move
from inbento_solver.solver import Solver
from inbento_solver.tiles import Tile

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})


@app.command()
def solve(level_file: Path) -> None:
    """Given a level file, find the list of moves that solve the puzzle."""
    print(f"Searching for file {level_file}")

    start_board, finish_board, moves = parse_level(level_file)
    solver: Solver = Solver(start_board, finish_board, moves)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="[green]Searching...", total=None)
        history: list[tuple[Move, Move, int, int]] = solver.solve()

    print("History:")
    for index, move_information in enumerate(history):
        if move_information[0] == move_information[1]:
            print(
                f"{index + 1}: Apply {move_information[1]} at "
                f"({move_information[2]}, {move_information[3]})"
            )
        else:
            print(
                f"{index + 1}: Rotate {move_information[0]} to "
                "{move_information[1]}; apply at ({move_information[2]}, "
                "{move_information[3]})"
            )


@app.command()
def test() -> None:
    """Solves a dummy puzzle."""
    initial_board: Board = Board([[Tile.RICE, Tile.RICE], [Tile.RICE, Tile.RICE]])
    finish_board: Board = Board([[Tile.RICE, Tile.SALMON], [Tile.EGG, Tile.SALMON]])
    moves: list[Move] = [
        LiteralMove({(0, 0): Tile.SALMON, (0, 1): Tile.SALMON}, False),
        LiteralMove({(0, 0): Tile.EGG, (0, 1): Tile.EGG}, False),
    ]

    solver: Solver = Solver(initial_board, finish_board, moves)
    history: list[tuple[Move, Move, int, int]] = solver.solve()

    print("History:")
    for index, move_information in enumerate(history):
        if move_information[0] == move_information[1]:
            print(
                f"{index + 1}: Apply {move_information[1]} at "
                f"({move_information[2]}, {move_information[3]})"
            )
        else:
            print(
                f"{index + 1}: Rotate {move_information[0]} to "
                "{move_information[1]}; apply at ({move_information[2]}, "
                "{move_information[3]})"
            )


if __name__ == "__main__":
    app()
