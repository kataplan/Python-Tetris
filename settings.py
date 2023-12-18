import pygame as pg

vec = pg.math.Vector2

FPS = 60

FAST_ANIM_TIME_MULT = 2

UPDATE_START_SPEED = 800
MOVE_WAIT_TIME = 10
ROTATE_WAIT_TIME = 10

TETRIS_GRID_W = 10
TETRIS_GRID_H = 20
TILE_SIZE = 32
MENU_SIZE_W = 8
BOTTOM_SIZE_H = 4

TETRIS_WIDTH = TETRIS_GRID_W * TILE_SIZE
TETRIS_HEIGHT = TETRIS_GRID_H * TILE_SIZE

MENU_WIDTH = MENU_SIZE_W * TILE_SIZE
MENU_HEIGHT = TETRIS_HEIGHT

BOTTOM_WIDTH = TETRIS_WIDTH
BOTTOM_HEIGHT = BOTTOM_SIZE_H * TILE_SIZE

GRID_SIZE = TETRIS_WIDTH, TETRIS_HEIGHT

PADDING = 10

WIN_WIDTH = GRID_SIZE[0] + MENU_WIDTH + PADDING
WIN_HEIGHT = GRID_SIZE[1] + BOTTOM_HEIGHT + PADDING
WIN_RES = WIN_WIDTH, WIN_HEIGHT
GRID_START_W = WIN_WIDTH - TETRIS_WIDTH
GRID_START_H = WIN_HEIGHT - TETRIS_HEIGHT

FONT_PATH = "assets/font/PixelGosub-ZaRz.ttf"
SPRITE_BLOCK_PATH = "assets/sprites/blocks"
SPRITE_TETROMINOES_PATH = "assets/sprites/tetrominoes"

INIT_POS_OFFSET = vec((TETRIS_GRID_W // 2 - 1, 0))
NEXT_POS_OFFSET = vec((TETRIS_GRID_W * 1.30, TETRIS_GRID_H * 0.280))

MOVE_DIRECTIONS = {"left": vec(-1, 0), "right": vec(1, 0), "down": vec(0, 1)}

TETROMINOES = {
    "T": [(0, 0), (-1, 0), (1, 0), (0, -1)],
    "O": [(0, 0), (0, -1), (1, 0), (1, -1)],
    "J": [(0, 0), (-1, 0), (0, -1), (0, -2)],
    "L": [(0, 0), (1, 0), (0, -1), (0, -2)],
    "I": [(0, 0), (0, 1), (0, -1), (0, -2)],
    "S": [(0, 0), (-1, 0), (0, -1), (1, -1)],
    "Z": [(0, 0), (1, 0), (0, -1), (-1, -1)],
}

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (32, 32, 32)


TETROMINOES_COLORS = {
    "T": "MAGENTA",
    "O": "YELLOW",
    "J": "BLUE",
    "L": "ORANGE",
    "I": "CYAN",
    "S": "GREEN",
    "Z": "RED",
}
ROTATION_STATES = ["0", "R", "2", "L"]
ROTATION_MAPPING = {"90": 1, "-90": -1}

JLSTZ_WALL_KICKS = {
    "0R": [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    "R0": [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    "R2": [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    "2R": [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    "2L": [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    "L2": [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    "L0": [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    "0L": [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
}

I_WALL_KICKS = {
    "0R": [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    "R0": [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    "R2": [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
    "2R": [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
    "2L": [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    "L2": [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    "L0": [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
    "0L": [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
}
