from re import S
from settings import *
from pygame.image import load
import pygame.freetype as ft
from os import path


class Preview:
    def __init__(self, font):
        self.font = font
        self.display_surface = pg.display.get_surface()
        self.menu_surface = pg.Surface((BOTTOM_WIDTH, BOTTOM_HEIGHT))
        self.menu_rect = self.menu_surface.get_rect(
            topleft=(0, GAME_HEIGHT + PADDING)
        )

        # shapes
        self.next_shapes = []
        self.scale = (TILE_SIZE*0.4)/32
        self.shape_sprites = {
            shape: load(
                path.join(SPRITE_TETROMINOES_PATH, f"{shape}.png")
            ).convert_alpha()
            for shape in TETROMINOES.keys()
        }

        # image position
        self.fragmet_width = self.menu_surface.get_width() / 3

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

            x = self.fragmet_width / 2 + i * self.fragmet_width
            y = self.menu_surface.get_height() / 2
            rect = scaled_surface.get_rect(center=(x, y))
            self.menu_surface.blit(scaled_surface, rect)

    def set_next_shapes(self, next_shapes):
        self.next_shapes = next_shapes

    def draw(self):
        self.menu_surface.fill(GREY)
        self.display_pieces(self.next_shapes)
        pg.draw.rect(
            self.menu_surface,
            WHITE,
            (0, 0, BOTTOM_WIDTH, BOTTOM_HEIGHT),
            2,
            2,
        )
        self.text_draw()
        self.display_surface.blit(self.menu_surface, self.menu_rect)

    def text_draw(self):
        self.font.render_to(
            self.menu_surface,
            (0, 0),
            text="Next",
            fgcolor=WHITE,
            size=TILE_SIZE * 0.8,
            bgcolor=GREY,
        )
