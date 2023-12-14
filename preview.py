from re import S
from settings import *
from pygame.image import load
import pygame.freetype as ft
from os import path


class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)

    def draw(self):
        self.font.render_to(
            self.app.screen,
            (TETRIS_WIDTH + (MENU_SIZE_W * TILE_SIZE // 2) - 50, WIN_HEIGHT * 0.02),
            text="TETRIS",
            fgcolor=WHITE,
            size=TILE_SIZE * 1,
            bgcolor=BLACK,
        )
        self.font.render_to(
            self.app.screen,
            (TETRIS_WIDTH + (MENU_SIZE_W * TILE_SIZE // 2) - 40, WIN_HEIGHT * 0.130),
            text="NEXT",
            fgcolor=WHITE,
            size=TILE_SIZE * 0.8,
            bgcolor=BLACK,
        )
        self.font.render_to(
            self.app.screen,
            (TETRIS_WIDTH + (MENU_SIZE_W * TILE_SIZE // 2) - 40, WIN_HEIGHT * 0.400),
            text="SCORE",
            fgcolor=WHITE,
            size=TILE_SIZE * 0.8,
            bgcolor=BLACK,
        )
        self.font.render_to(
            self.app.screen,
            (TETRIS_WIDTH + (MENU_SIZE_W * TILE_SIZE // 2) - 40, WIN_HEIGHT * 0.440),
            text=f"{self.app.tetris.score}",
            fgcolor=WHITE,
            size=TILE_SIZE * 0.8,
            bgcolor=BLACK,
        )
        self.font.render_to(
            self.app.screen,
            (TETRIS_WIDTH + (MENU_SIZE_W * TILE_SIZE // 2) - 40, WIN_HEIGHT * 0.480),
            text="Level",
            fgcolor=WHITE,
            size=TILE_SIZE * 0.8,
            bgcolor=BLACK,
        )
        self.font.render_to(
            self.app.screen,
            (TETRIS_WIDTH + (MENU_SIZE_W * TILE_SIZE // 2) - 40, WIN_HEIGHT * 0.520),
            text=f"{self.app.tetris.level}",
            fgcolor=WHITE,
            size=TILE_SIZE * 0.8,
            bgcolor=BLACK,
        )


class Preview:
    def __init__(self):
        self.display_surface = pg.display.get_surface()

        self.menu_surface = pg.Surface((BOTTOM_WIDTH, BOTTOM_HEIGHT))
        self.menu_rect = self.menu_surface.get_rect(topleft=(0, TETRIS_HEIGHT+10))

        # shapes
        self.next_shapes = []
        self.scale = 0.4
        self.shape_sprites = {
            shape: load(
                path.join(SPRITE_TETROMINOES_PATH, f"{shape}.png")
            ).convert_alpha()
            for shape in TETROMINOES.keys()
        }

        # image position
        self.fragmet_width = self.menu_surface.get_width() / 3

    def draw(self):
        self.menu_surface.fill(GREY)
        self.display_pieces(self.next_shapes)
        self.display_surface.blit(self.menu_surface, self.menu_rect)
        pg.draw.rect(self.display_surface, WHITE, self.menu_rect, 2, 2)

    def display_pieces(self, shapes):
        for i, shape in enumerate(shapes):
            shape_surface = self.shape_sprites[shape]
            scaled_surface = pg.transform.scale(
                shape_surface,
                (
                    int(shape_surface.get_width() * self.scale),
                    int(shape_surface.get_height() * self.scale),
                ),
            )

            x = self.fragmet_width / 2+ i * self.fragmet_width
            y = self.menu_surface.get_height() / 2 
            rect = scaled_surface.get_rect(center=(x, y))
            self.menu_surface.blit(scaled_surface, rect)

    def set_next_shapes(self, next_shapes):
        self.next_shapes = next_shapes
