from typing import Tuple

# Game configuration
BLOCK_SIZE: int = 30  # pixel size for a single block
COLS: int = 10        # width of the game field in blocks
ROWS: int = 20        # height of the game field in blocks
PLAY_WIDTH: int = COLS * BLOCK_SIZE
PLAY_HEIGHT: int = ROWS * BLOCK_SIZE
SIDE_PANEL: int = 200
SCREEN_WIDTH: int = PLAY_WIDTH + SIDE_PANEL
SCREEN_HEIGHT: int = PLAY_HEIGHT

# Colour definitions (R, G, B)
Color = Tuple[int, int, int]
BLACK: Color   = (0, 0, 0)
WHITE: Color   = (255, 255, 255)
GRAY: Color    = (128, 128, 128)
RED: Color     = (255, 0, 0)
GREEN: Color   = (0, 255, 0)
BLUE: Color    = (0, 0, 255)
CYAN: Color    = (0, 255, 255)
MAGENTA: Color = (255, 0, 255)
YELLOW: Color  = (255, 255, 0)
ORANGE: Color  = (255, 165, 0)
PURPLE: Color  = (160, 32, 240)

# Tetris shapes (4x4 matrix represented with strings)
# "0" represents a filled block, "." represents empty space
SHAPES = {
    "S": [[
        ".....",
        ".....",
        "..00.",
        ".00..",
        "....."],
        [
        ".....",
        "..0..",
        "..00.",
        "...0.",
        "....."]],

    "Z": [[
        ".....",
        ".....",
        ".00..",
        "..00.",
        "....."],
        [
        ".....",
        "..0..",
        ".00..",
        ".0...",
        "....."]],

    "I": [[
        "..0..",
        "..0..",
        "..0..",
        "..0..",
        "....."],
        [
        ".....",
        "0000.",
        ".....",
        ".....",
        "....."]],

    "O": [[
        ".....",
        ".....",
        ".00..",
        ".00..",
        "....."]],

    "J": [[
        ".....",
        ".0...",
        ".000.",
        ".....",
        "....."],
        [
        ".....",
        "..00.",
        "..0..",
        "..0..",
        "....."],
        [
        ".....",
        ".....",
        ".000.",
        "...0.",
        "....."],
        [
        ".....",
        "..0..",
        "..0..",
        ".00..",
        "....."]],

    "L": [[
        ".....",
        "...0.",
        ".000.",
        ".....",
        "....."],
        [
        ".....",
        "..0..",
        "..0..",
        "..00.",
        "....."],
        [
        ".....",
        ".....",
        ".000.",
        ".0...",
        "....."],
        [
        ".....",
        ".00..",
        "..0..",
        "..0..",
        "....."]],

    "T": [[
        ".....",
        "..0..",
        ".000.",
        ".....",
        "....."],
        [
        ".....",
        "..0..",
        "..00.",
        "..0..",
        "....."],
        [
        ".....",
        ".....",
        ".000.",
        "..0..",
        "....."],
        [
        ".....",
        "..0..",
        ".00..",
        "..0..",
        "....."]]
}

# Matching colour for each shape key
SHAPE_COLORS = {
    "S": GREEN,
    "Z": RED,
    "I": CYAN,
    "O": YELLOW,
    "J": BLUE,
    "L": ORANGE,
    "T": PURPLE,
}