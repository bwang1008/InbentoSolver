"""Main application code."""

from __future__ import annotations

from pathlib import Path  # noqa: TCH003
from typing import TYPE_CHECKING

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from inbento_solver.level import parse_level
from inbento_solver.solver import Solver

if TYPE_CHECKING:
    from inbento_solver.moves.base import MoveDescription

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})


@app.command()
def solve(level_file: Path) -> None:
    """Given a level file, find the list of moves that solve the puzzle.

    TODO: Wrap "Path" in Annotated, but currently bug in Python 3.8:
        this will be fixed when https://github.com/tiangolo/typer/pull/814
        is in the next release.
    """
    title, start_board, finish_board, moves = parse_level(level_file)
    solver: Solver = Solver(start_board, finish_board, moves)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="[green]Searching...", total=None)
        history: list[MoveDescription] = solver.solve()

    print(f"Steps to solve level {title}:")
    for index, move_information in enumerate(history):
        print(f"{index + 1}: {move_information}")


if __name__ == "__main__":
    app()
