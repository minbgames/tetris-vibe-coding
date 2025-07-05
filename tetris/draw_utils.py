from typing import List, Tuple

import pygame  # type: ignore

from .constants import (
    PLAY_WIDTH,
    PLAY_HEIGHT,
    BLOCK_SIZE,
    COLS,
    ROWS,
    GRAY,
    WHITE,
    RED,
    BLACK,
)
from .piece import Piece


Grid = List[List[Tuple[int, int, int]]]


def draw_text_middle(surface: pygame.Surface, text: str, size: int, color: Tuple[int, int, int]):
    """Draw text centred in the play field."""
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, True, color)
    surface.blit(label, (PLAY_WIDTH / 2 - label.get_width() / 2, PLAY_HEIGHT / 2 - label.get_height() / 2))


def draw_grid(surface: pygame.Surface, grid: Grid):
    """Draw the internal grid lines for visual guidance."""
    for i in range(ROWS):
        pygame.draw.line(surface, GRAY, (0, i * BLOCK_SIZE), (PLAY_WIDTH, i * BLOCK_SIZE))
    for j in range(COLS):
        pygame.draw.line(surface, GRAY, (j * BLOCK_SIZE, 0), (j * BLOCK_SIZE, PLAY_HEIGHT))


def draw_next_shape(piece: Piece, surface: pygame.Surface):
    """Render the upcoming piece on the side panel."""
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Next", True, WHITE)

    start_x = PLAY_WIDTH + 20
    start_y = PLAY_HEIGHT // 2 - 100
    surface.blit(label, (start_x + 10, start_y - 30))

    format_ = piece.shape
    for i, line in enumerate(format_):
        for j, column in enumerate(line):
            if column == "0":
                pygame.draw.rect(
                    surface,
                    piece.color,
                    (start_x + j * BLOCK_SIZE, start_y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    0,
                )

    # outline grid for the preview box
    for i in range(5):
        for j in range(5):
            pygame.draw.rect(
                surface,
                GRAY,
                (start_x + j * BLOCK_SIZE, start_y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                1,
            )


def draw_window(surface: pygame.Surface, grid: Grid, score: int = 0, level: int = 1):
    """Draw the main play field including score/level information."""
    surface.fill(BLACK)

    # Title
    font = pygame.font.SysFont("comicsans", 50)
    label = font.render("TETRIS", True, WHITE)
    surface.blit(label, (PLAY_WIDTH / 2 - label.get_width() / 2, 10))

    # Score & Level
    font_small = pygame.font.SysFont("comicsans", 30)
    label = font_small.render(f"Score: {score}", True, WHITE)
    surface.blit(label, (PLAY_WIDTH + 20, 20))

    label = font_small.render(f"Level: {level}", True, WHITE)
    surface.blit(label, (PLAY_WIDTH + 20, 60))

    # Draw blocks
    for i in range(ROWS):
        for j in range(COLS):
            pygame.draw.rect(
                surface,
                grid[i][j],
                (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                0,
            )

    draw_grid(surface, grid)
    pygame.draw.rect(surface, RED, (0, 0, PLAY_WIDTH, PLAY_HEIGHT), 4)