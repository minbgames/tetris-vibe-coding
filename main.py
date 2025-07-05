import pygame
import random
from typing import List, Tuple, Any

# 게임 설정
BLOCK_SIZE = 30  # 한 블록의 픽셀 크기
COLS = 10        # 필드의 가로 칸 수
ROWS = 20        # 필드의 세로 칸 수
PLAY_WIDTH = COLS * BLOCK_SIZE
PLAY_HEIGHT = ROWS * BLOCK_SIZE
SIDE_PANEL = 200
SCREEN_WIDTH = PLAY_WIDTH + SIDE_PANEL
SCREEN_HEIGHT = PLAY_HEIGHT

# 색상 정의 (R, G, B)
Color = Tuple[int, int, int]
BLACK: Color  = (  0,   0,   0)
WHITE: Color  = (255, 255, 255)
GRAY: Color   = (128, 128, 128)
RED: Color    = (255,   0,   0)
GREEN: Color  = (  0, 255,   0)
BLUE: Color   = (  0,   0, 255)
CYAN: Color   = (  0, 255, 255)
MAGENTA: Color= (255,   0, 255)
YELLOW: Color = (255, 255,   0)
ORANGE: Color = (255, 165,   0)
PURPLE: Color = (160,  32, 240)

# 각 테트리스 도형 (4x4 매트릭스)
# 1은 블록이 있는 부분, 0은 빈 공간
SHAPES = {
    "S": [[".....",
            ".....",
            "..00.",
            ".00..",
            "....."],
           [".....",
            "..0..",
            "..00.",
            "...0.",
            "....."]],

    "Z": [[".....",
            ".....",
            ".00..",
            "..00.",
            "....."],
           [".....",
            "..0..",
            ".00..",
            ".0...",
            "....."]],

    "I": [["..0..",
            "..0..",
            "..0..",
            "..0..",
            "....."],
           [".....",
            "0000.",
            ".....",
            ".....",
            "....."]],

    "O": [[".....",
            ".....",
            ".00..",
            ".00..",
            "....."]],

    "J": [[".....",
            ".0...",
            ".000.",
            ".....",
            "....."],
           [".....",
            "..00.",
            "..0..",
            "..0..",
            "....."],
           [".....",
            ".....",
            ".000.",
            "...0.",
            "....."],
           [".....",
            "..0..",
            "..0..",
            ".00..",
            "....."]],

    "L": [[".....",
            "...0.",
            ".000.",
            ".....",
            "....."],
           [".....",
            "..0..",
            "..0..",
            "..00.",
            "....."],
           [".....",
            ".....",
            ".000.",
            ".0...",
            "....."],
           [".....",
            ".00..",
            "..0..",
            "..0..",
            "....."]],

    "T": [[".....",
            "..0..",
            ".000.",
            ".....",
            "....."],
           [".....",
            "..0..",
            "..00.",
            "..0..",
            "....."],
           [".....",
            ".....",
            ".000.",
            "..0..",
            "....."],
           [".....",
            "..0..",
            ".00..",
            "..0..",
            "....."]]
}

# 각 도형별 색상 매핑
SHAPE_COLORS = {
    "S": GREEN,
    "Z": RED,
    "I": CYAN,
    "O": YELLOW,
    "J": BLUE,
    "L": ORANGE,
    "T": PURPLE,
}

class Piece:
    def __init__(self, x: int, y: int, shape_key: str):
        self.x = x
        self.y = y
        self.shape_key = shape_key
        self.shape_rotations = SHAPES[shape_key]
        self.rotation = 0  # 현재 회전 상태 인덱스
        self.color = SHAPE_COLORS[shape_key]

    @property
    def shape(self) -> List[str]:
        """현재 회전 상태의 도형 반환"""
        return self.shape_rotations[self.rotation % len(self.shape_rotations)]


def create_grid(locked_positions: dict) -> List[List[Tuple[int, int, int]]]:
    """잠긴 블록 정보를 포함한 그리드를 생성"""
    grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
    for (col, row), color in locked_positions.items():
        if row > -1:
            grid[row][col] = color
    return grid


def convert_shape_format(piece: Piece) -> List[Tuple[int, int]]:
    positions = []
    shape_matrix = piece.shape

    for i, line in enumerate(shape_matrix):
        row = list(line)
        for j, column in enumerate(row):
            if column == "0":
                positions.append((piece.x + j - 2, piece.y + i - 4))
    return positions


def valid_space(piece: Piece, grid: List[List[Tuple[int, int, int]]]) -> bool:
    accepted_positions = [[(j, i) for j in range(COLS) if grid[i][j] == BLACK] for i in range(ROWS)]
    accepted_positions = [pos for sub in accepted_positions for pos in sub]

    formatted = convert_shape_format(piece)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions: dict) -> bool:
    """블록이 생성되는 윗부분에 잠긴 블록이 있다면 게임 오버"""
    for (_, y) in positions.keys():
        if y < 1:
            return True
    return False


def get_shape() -> Piece:
    return Piece(COLS // 2 - 2, 0, random.choice(list(SHAPES.keys())))


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, True, color)

    surface.blit(label, (PLAY_WIDTH/2 - label.get_width()/2, PLAY_HEIGHT/2 - label.get_height()/2))


def draw_grid(surface, grid):
    for i in range(ROWS):
        pygame.draw.line(surface, GRAY, (0, i * BLOCK_SIZE), (PLAY_WIDTH, i * BLOCK_SIZE))
    for j in range(COLS):
        pygame.draw.line(surface, GRAY, (j * BLOCK_SIZE, 0), (j * BLOCK_SIZE, PLAY_HEIGHT))


def clear_rows(grid: List[List[Tuple[int, int, int]]], locked: dict) -> int:
    cleared = 0
    for i in range(ROWS-1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            cleared += 1
            # 해당 줄의 잠긴 블록 제거
            for j in range(COLS):
                try:
                    del locked[(j, i)]
                except KeyError:
                    continue
    if cleared > 0:
        # 위에 있는 블록들을 아래로 이동
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            color = locked[key]
            if y < min([r for (_, r) in locked.keys()]) + cleared:
                continue
            if y < i:
                new_key = (x, y + cleared)
                locked[new_key] = color
                del locked[key]
    return cleared


def draw_next_shape(piece: Piece, surface):
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Next", True, WHITE)
    start_x = PLAY_WIDTH + 20
    start_y = PLAY_HEIGHT // 2 - 100

    surface.blit(label, (start_x + 10, start_y - 30))

    format = piece.shape
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == "0":
                pygame.draw.rect(surface, piece.color,
                                 (start_x + j*BLOCK_SIZE, start_y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    # 그리드 그리기
    for i in range(5):
        for j in range(5):
            pygame.draw.rect(surface, GRAY,
                             (start_x + j*BLOCK_SIZE, start_y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)


def draw_window(surface, grid, score=0, level=1):
    surface.fill(BLACK)

    # 제목
    font = pygame.font.SysFont("comicsans", 50)
    label = font.render("TETRIS", True, WHITE)
    surface.blit(label, (PLAY_WIDTH/2 - label.get_width()/2, 10))

    # 점수
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render(f"Score: {score}", True, WHITE)

    surface.blit(label, (PLAY_WIDTH + 20, 20))

    # 레벨
    label = font.render(f"Level: {level}", True, WHITE)
    surface.blit(label, (PLAY_WIDTH + 20, 60))

    # 게임 영역 그리기
    for i in range(ROWS):
        for j in range(COLS):
            pygame.draw.rect(surface, grid[i][j],
                             (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    draw_grid(surface, grid)
    pygame.draw.rect(surface, RED, (0, 0, PLAY_WIDTH, PLAY_HEIGHT), 4)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Python Tetris")

    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5  # 더 작을수록 빨라짐
    score = 0
    level = 1
    lines_cleared = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # 블록이 밑으로 떨어지는 로직
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key in [pygame.K_UP, pygame.K_w]:
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape_rotations)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape_rotations)
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_SPACE:
                    # Hard drop
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    change_piece = True
                elif event.key in [pygame.K_q, pygame.K_ESCAPE]:
                    run = False

        shape_pos = convert_shape_format(current_piece)

        # 현재 블록 위치를 그리드에 반영
        for x, y in shape_pos:
            if y > -1:
                grid[y][x] = current_piece.color

        # 블록을 잠금 처리
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            cleared = clear_rows(grid, locked_positions)
            if cleared > 0:
                lines_cleared += cleared
                score += cleared * 100
                if lines_cleared // 10 + 1 > level:
                    level += 1
                    fall_speed = max(0.1, fall_speed - 0.05)

        draw_window(screen, grid, score, level)
        draw_next_shape(next_piece, screen)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(screen, "GAME OVER", 60, RED)
            pygame.display.update()
            pygame.time.delay(2000)
            run = False


def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Python Tetris")

    run = True
    while run:
        screen.fill(BLACK)
        draw_text_middle(screen, "Press any key to play", 40, WHITE)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                main()
                run = False

if __name__ == "__main__":
    main_menu()