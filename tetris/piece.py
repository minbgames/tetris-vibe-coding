from __future__ import annotations

import random
from typing import List, Tuple

from .constants import COLS, SHAPES, SHAPE_COLORS


class Piece:
    """Represents a single Tetris piece with rotation support."""

    def __init__(self, x: int, y: int, shape_key: str):
        self.x: int = x
        self.y: int = y
        self.shape_key: str = shape_key
        self.shape_rotations: List[List[str]] = SHAPES[shape_key]
        self.rotation: int = 0  # rotation index
        self.color = SHAPE_COLORS[shape_key]

    # ---------------------------------------------------------------------
    # Computed helpers
    # ---------------------------------------------------------------------
    @property
    def shape(self) -> List[str]:
        """Return the current rotated shape as a list of strings."""
        return self.shape_rotations[self.rotation % len(self.shape_rotations)]


# -------------------------------------------------------------------------
# Convenience factory helpers
# -------------------------------------------------------------------------

def get_random_piece() -> "Piece":
    """Create a new random piece located at the top centre of the board."""
    return Piece(COLS // 2 - 2, 0, random.choice(list(SHAPES.keys())))


# -------------------------------------------------------------------------
# Helper utilities that operate *on* a Piece but aren't methods of Piece
# -------------------------------------------------------------------------

def convert_shape_format(piece: "Piece") -> List[Tuple[int, int]]:
    """Convert a piece's string representation into grid coordinate offsets.

    The coordinates returned are absolute grid positions based on the piece's
    current (x, y) position and rotation. These are useful when checking for
    collisions or drawing the piece on the game grid.
    """
    positions: List[Tuple[int, int]] = []
    shape_matrix = piece.shape

    for i, line in enumerate(shape_matrix):
        row = list(line)
        for j, column in enumerate(row):
            if column == "0":
                # Offset by -2 (x) and -4 (y) to compensate for 4x4 matrix pivot
                positions.append((piece.x + j - 2, piece.y + i - 4))
    return positions