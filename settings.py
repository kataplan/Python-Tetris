import pygame as pg

vec = pg.math.Vector2

# Tile size in pixels
TILE_SIZE = 20

# Padding
PADDING = 10

#Grid size in tiles
TETRIS_GRID_W = 10
TETRIS_GRID_H = 20
MENU_SIZE_W = 8
BOTTOM_SIZE_H = 4

# Game classes sizes
GAME_WIDTH = TETRIS_GRID_W * TILE_SIZE
GAME_HEIGHT = TETRIS_GRID_H * TILE_SIZE
SIDEBAR_WIDTH = MENU_SIZE_W * TILE_SIZE
SIDEBAR_HEIGHT = GAME_HEIGHT
BOTTOM_WIDTH = GAME_WIDTH
BOTTOM_HEIGHT = BOTTOM_SIZE_H * TILE_SIZE

# Game Resolution
GAME_SIZE = GAME_WIDTH, GAME_HEIGHT

#Window Resolution
WIN_WIDTH = GAME_SIZE[0] + SIDEBAR_WIDTH + PADDING
WIN_HEIGHT = GAME_SIZE[1] + BOTTOM_HEIGHT + PADDING
WIN_RES = WIN_WIDTH, WIN_HEIGHT

# Game Time
FPS = 60
UPDATE_START_SPEED = 800
MOVE_WAIT_TIME = 100
ROTATE_WAIT_TIME = 100

#Initial position Offset
INIT_POS_OFFSET = vec((TETRIS_GRID_W // 2 - 1, 0))

#PATH
FONT_PATH = "assets/font/PixelGosub-ZaRz.ttf"
SPRITE_BLOCK_PATH = "assets/sprites/blocks"
SPRITE_TETROMINOES_PATH = "assets/sprites/tetrominoes"


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (32, 32, 32)
RED = (255, 0, 0)


# Tetrominoes
TETROMINOES = {
    "T": [(0, 0), (-1, 0), (1, 0), (0, -1)],
    "O": [(0, 0), (0, -1), (1, 0), (1, -1)],
    "J": [(0, 0), (-1, 0), (0, -1), (0, -2)],
    "L": [(0, 0), (1, 0), (0, -1), (0, -2)],
    "I": [(0, 0), (0, 1), (0, -1), (0, -2)],
    "S": [(0, 0), (-1, 0), (0, -1), (1, -1)],
    "Z": [(0, 0), (1, 0), (0, -1), (-1, -1)],
}

TETROMINOES_COLORS = {
    "T": "MAGENTA",
    "O": "YELLOW",
    "J": "BLUE",
    "L": "ORANGE",
    "I": "CYAN",
    "S": "GREEN",
    "Z": "RED",
}

# Movement
MOVE_DIRECTIONS = {"left": vec(-1, 0), "right": vec(1, 0), "down": vec(0, 1)}

# Rotation
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
