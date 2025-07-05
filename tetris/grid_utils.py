from typing import List, Tuple

from .constants import COLS, ROWS, BLACK
from .piece import Piece, convert_shape_format


Grid = List[List[Tuple[int, int, int]]]


def create_grid(locked_positions: dict) -> Grid:
    """Return a 2-D grid filled with colour tuples, including locked blocks."""
    grid: Grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
    for (col, row), color in locked_positions.items():
        if row > -1:
            grid[row][col] = color
    return grid


def valid_space(piece: Piece, grid: Grid) -> bool:
    """Check whether the piece can occupy its current position."""
    accepted_positions = [
        (j, i)
        for i in range(ROWS)
        for j in range(COLS)
        if grid[i][j] == BLACK
    ]

    formatted = convert_shape_format(piece)
    for pos in formatted:
        if pos not in accepted_positions and pos[1] > -1:
            return False
    return True


def check_lost(positions: dict) -> bool:
    """Game over when any locked block appears on the first visible row."""
    return any(y < 1 for (_, y) in positions.keys())


def clear_rows(grid: Grid, locked: dict) -> int:
    """Remove every filled row, shift above rows downward, and return count."""
    cleared = 0
    for i in range(ROWS - 1, -1, -1):
        if BLACK not in grid[i]:
            cleared += 1
            for j in range(COLS):
                locked.pop((j, i), None)

    if cleared:
        # Move the remaining rows downwards, starting from the bottom
        for (x, y) in sorted(list(locked.keys()), key=lambda k: k[1])[::-1]:
            new_key = (x, y + cleared)
            if y < ROWS:
                locked[new_key] = locked.pop((x, y))
    return cleared