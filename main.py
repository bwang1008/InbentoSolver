"""Main application code."""

from __future__ import annotations

from pathlib import Path  # noqa: TCH003
from typing import TYPE_CHECKING

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from inbento_solver.level import parse_level
from inbento_solver.solver import Solver

if TYPE_CHECKING:
    from inbento_solver.move import Move

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})


@app.command()
def solve(level_file: Path) -> None:
    """Given a level file, find the list of moves that solve the puzzle."""
    title, start_board, finish_board, moves = parse_level(level_file)
    solver: Solver = Solver(start_board, finish_board, moves)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="[green]Searching...", total=None)
        history: list[tuple[Move, Move, int, int]] = solver.solve()

    print(f"Steps to solve level {title}:")
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
