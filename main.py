"""Main application code."""

from __future__ import annotations

import json
from pathlib import Path  # noqa: TC003
from typing import TYPE_CHECKING

import typer
from rich import print as rprint
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing_extensions import Annotated

from inbento_solver.level import Level
from inbento_solver.solver import Solver

if TYPE_CHECKING:
    from inbento_solver.moves.base import MoveDescription

app: typer.Typer = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})


@app.command()
def solve(
    level_path: Annotated[
        Path, typer.Option(help="JSON description of level to solve")
    ],
) -> None:
    """Given a level file, find the list of moves that solve the puzzle."""
    if not level_path.exists():
        rprint(f"Level file {level_path} does not exist")
        raise typer.Abort

    with level_path.open(mode="r", encoding="utf-8") as level_file:
        level_info = json.load(level_file)
    level: Level = Level.model_validate(level_info)
    solver: Solver = Solver(level.start, level.finish, level.moves)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="[green]Searching...", total=None)
        history: list[MoveDescription] = solver.solve()

    rprint(f"Steps to solve level {level.title}:")
    for index, move_information in enumerate(history):
        rprint(f"{index + 1}: {move_information}")


if __name__ == "__main__":
    app()
