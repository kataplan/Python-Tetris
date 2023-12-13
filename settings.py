from turtle import right
import pygame as pg

vec = pg.math.Vector2

FPS = 60

ANIM_TIME_INTERVAL = 150
FAST_ANIM_TIME_INTERVAL = 15

GRID_WIDTH = 10
GRID_HEIGHT = 20
TILE_SIZE = 35
MENU_WIDHT = 8


SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE
GRID_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT


WIN_WIDTH = GRID_SIZE[0] + MENU_WIDHT * TILE_SIZE
WIN_HEIGHT = GRID_SIZE[1]
WIN_RES = WIN_WIDTH, WIN_HEIGHT
GRID_START_W = WIN_WIDTH - SCREEN_WIDTH
GRID_START_H = WIN_HEIGHT - SCREEN_HEIGHT

FONT_PATH = "assets/font/PixelGosub-ZaRz.ttf"

INIT_POS_OFFSET = vec((GRID_WIDTH // 2 - 1, 0))
NEXT_POS_OFFSET = vec((GRID_WIDTH * 1.35, GRID_HEIGHT * 0.290))

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
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)

TETROMINOES_COLORS = {
    "T": MAGENTA,
    "O": YELLOW,
    "J": BLUE,
    "L": ORANGE,
    "I": CYAN,
    "S": GREEN,
    "Z": RED,
}
