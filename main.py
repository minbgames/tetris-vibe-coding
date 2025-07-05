import pygame  # type: ignore

from tetris.constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE
from tetris.draw_utils import draw_text_middle
from tetris.game import TetrisGame


def main_menu():
    """Display the start screen and launch the game when a key is pressed."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Python Tetris")

    running = True
    while running:
        screen.fill(BLACK)
        draw_text_middle(screen, "Press any key to play", 40, WHITE)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                game = TetrisGame()
                game.run()
                running = False

    pygame.quit()


if __name__ == "__main__":
    main_menu()