from __future__ import annotations

import pygame  # type: ignore

from .constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BLACK,
    RED,
)
from .piece import Piece, get_random_piece, convert_shape_format
from .grid_utils import create_grid, valid_space, clear_rows, check_lost
from .draw_utils import draw_window, draw_next_shape, draw_text_middle


class TetrisGame:
    """High-level facade class that manages an entire round of Tetris."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Python Tetris")
        self.clock = pygame.time.Clock()
        self.reset()

    # ------------------------------------------------------------------
    # Game initialisation helpers
    # ------------------------------------------------------------------
    def reset(self):
        self.locked_positions: dict[tuple[int, int], tuple[int, int, int]] = {}
        self.current_piece: Piece = get_random_piece()
        self.next_piece: Piece = get_random_piece()
        self.change_piece: bool = False

        # Timing & difficulty variables
        self.fall_time: float = 0.0
        self.fall_speed: float = 0.5  # smaller -> faster

        # Score tracking
        self.score: int = 0
        self.level: int = 1
        self.lines_cleared: int = 0

    # ------------------------------------------------------------------
    # Main game loop
    # ------------------------------------------------------------------
    def run(self):
        running = True
        while running:
            grid = create_grid(self.locked_positions)
            self.fall_time += self.clock.get_rawtime()
            self.clock.tick()

            # Automatic downward movement
            if self.fall_time / 1000 >= self.fall_speed:
                self.fall_time = 0
                self.current_piece.y += 1
                if not valid_space(self.current_piece, grid) and self.current_piece.y > 0:
                    self.current_piece.y -= 1
                    self.change_piece = True

            # ------------------------------------------------------------------
            # Event handling
            # ------------------------------------------------------------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        self._move_current(dx=-1, grid=grid)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self._move_current(dx=1, grid=grid)
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        self._rotate_current(grid)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self._soft_drop(grid)
                    elif event.key == pygame.K_SPACE:
                        self._hard_drop(grid)
                    elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                        running = False

            # Place the current piece on the grid for rendering
            for x, y in convert_shape_format(self.current_piece):
                if y > -1:
                    grid[y][x] = self.current_piece.color

            # Handle locking & new piece generation
            if self.change_piece:
                for pos in convert_shape_format(self.current_piece):
                    self.locked_positions[pos] = self.current_piece.color
                self.current_piece = self.next_piece
                self.next_piece = get_random_piece()
                self.change_piece = False

                cleared = clear_rows(grid, self.locked_positions)
                if cleared:
                    self.lines_cleared += cleared
                    self.score += cleared * 100
                    if self.lines_cleared // 10 + 1 > self.level:
                        self.level += 1
                        self.fall_speed = max(0.1, self.fall_speed - 0.05)

            # Draw everything
            draw_window(self.screen, grid, self.score, self.level)
            draw_next_shape(self.next_piece, self.screen)
            pygame.display.update()

            # Check for game-over
            if check_lost(self.locked_positions):
                draw_text_middle(self.screen, "GAME OVER", 60, RED)
                pygame.display.update()
                pygame.time.delay(2000)
                running = False

        pygame.display.quit()
        pygame.quit()

    # ------------------------------------------------------------------
    # Piece manipulation helpers
    # ------------------------------------------------------------------
    def _move_current(self, dx: int, grid):
        self.current_piece.x += dx
        if not valid_space(self.current_piece, grid):
            self.current_piece.x -= dx

    def _rotate_current(self, grid):
        self.current_piece.rotation = (self.current_piece.rotation + 1) % len(self.current_piece.shape_rotations)
        if not valid_space(self.current_piece, grid):
            self.current_piece.rotation = (self.current_piece.rotation - 1) % len(self.current_piece.shape_rotations)

    def _soft_drop(self, grid):
        self.current_piece.y += 1
        if not valid_space(self.current_piece, grid):
            self.current_piece.y -= 1

    def _hard_drop(self, grid):
        while valid_space(self.current_piece, grid):
            self.current_piece.y += 1
        self.current_piece.y -= 1
        self.change_piece = True