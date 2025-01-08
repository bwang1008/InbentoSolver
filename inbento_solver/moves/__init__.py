"""Classes that represent each possible transformation on a Board."""

from __future__ import annotations

from typing import TYPE_CHECKING, Union

from pydantic import Discriminator, Tag
from typing_extensions import Annotated, TypeAlias

from .literal import LiteralMove
from .shift import ShiftMove
from .swap import SwapMove

if TYPE_CHECKING:
    from inbento_solver.moves.base import MoveBase


def get_move_discriminator_value(v: dict | MoveBase) -> str:
    """Retrieve value of v's move_type that distinguishes moves."""
    if isinstance(v, dict):
        return v["move_type"]
    return v.move_type


MoveSubtypesT: TypeAlias = Annotated[
    Union[
        Annotated[LiteralMove, Tag("literal")],
        Annotated[SwapMove, Tag("swap")],
        Annotated[ShiftMove, Tag("shift")],
    ],
    Discriminator(get_move_discriminator_value),
]
