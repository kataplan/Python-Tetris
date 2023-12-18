from re import S
from settings import *
from pygame.image import load
import pygame.freetype as ft
from os import path


class Sidebar:
    def __init__(self, app, font):
        self.app = app
        self.font = font

        self.display_surface = pg.display.get_surface()
        self.menu_surface = pg.Surface((MENU_WIDTH, WIN_HEIGHT))
        self.menu_rect = self.menu_surface.get_rect(topright=(WIN_WIDTH, 0))

        # shapes
        self.hold_shape = None
        self.shape_sprites = {
            shape: load(
                path.join(SPRITE_TETROMINOES_PATH, f"{shape}.png")
            ).convert_alpha()
            for shape in TETROMINOES.keys()
        }

        # image position
        self.fragmet_height = self.menu_surface.get_height() / 4

    def display_hold_piece(self):
        if self.hold_shape:
            shape_surface = self.shape_sprites[self.hold_shape]
            rect = shape_surface.get_rect(
                center=(MENU_WIDTH // 2, self.fragmet_height + self.fragmet_height // 2)
            )
            self.menu_surface.blit(shape_surface, rect)

    def draw(self):
        self.menu_surface.fill(GREY)
        self.display_hold_piece()
        pg.draw.rect(
            self.menu_surface,
            WHITE,
            (10, self.fragmet_height, MENU_WIDTH - 20, self.fragmet_height),
            2,
        )
        self.text_draw()

        self.display_surface.blit(self.menu_surface, self.menu_rect)
        pg.draw.rect(self.display_surface, WHITE, self.menu_rect, 2, 2)

    def set_hold_shape(self, shape):
        self.hold_shape = shape

    def text_draw(self):
        text_width, _ = self.font.get_rect(
            "TETRIS", size=TILE_SIZE * 1.7
        ).size
        text_x = (MENU_WIDTH - text_width) // 2

        self.font.render_to(
            self.menu_surface,
            (text_x, self.fragmet_height * 0 + 50),
            text="TETRIS",
            fgcolor=WHITE,
            size=TILE_SIZE * 1.7,
        )
        self.font.render_to(
            self.menu_surface,
            (10, self.fragmet_height * 1),
            text="HOLD",
            fgcolor=WHITE,
            size=TILE_SIZE * 0.8,
            bgcolor=GREY,
        )
        self.font.render_to(
            self.menu_surface,
            (10, self.fragmet_height * 3),
            text="SCORE",
            fgcolor=WHITE,
            size=TILE_SIZE * 1,
        )
        self.font.render_to(
            self.menu_surface,
            (10, self.fragmet_height * 3 + TILE_SIZE),
            text=f"{self.app.tetris.score}",
            fgcolor=WHITE,
            size=TILE_SIZE * 1,
        )
        self.font.render_to(
            self.menu_surface,
            (10, self.fragmet_height * 3 + TILE_SIZE*2),
            text="Lines",
            fgcolor=WHITE,
            size=TILE_SIZE * 1,
        )
        self.font.render_to(
            self.menu_surface,
            (10, self.fragmet_height * 3 + TILE_SIZE*3),
            text=f"{self.app.tetris.lines_completed}",
            fgcolor=WHITE,
            size=TILE_SIZE * 0.9,
        )
        self.font.render_to(
            self.menu_surface,
            (10, self.fragmet_height * 3 + TILE_SIZE*4),
            text="Level",
            fgcolor=WHITE,
            size=TILE_SIZE * 1,
        )
        self.font.render_to(
            self.menu_surface,
            (10, self.fragmet_height * 3 + TILE_SIZE*5),
            text=f"{self.app.tetris.level}",
            fgcolor=WHITE,
            size=TILE_SIZE * 0.9,
        )
