from re import S
from settings import *
from tetromino import *
import pygame.freetype as ft
import math


class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)

    def draw(self):
        self.font.render_to(
            self.app.screen,
            (SCREEN_WIDTH + (MENU_WIDHT * TILE_SIZE // 2) - 50, WIN_HEIGHT * 0.02),
            text="TETRIS",
            fgcolor=WHITE,
            size=TILE_SIZE * 1,
            bgcolor=BLACK,
        )
        self.font.render_to(
            self.app.screen,
            (SCREEN_WIDTH + (MENU_WIDHT * TILE_SIZE // 2) - 40, WIN_HEIGHT * 0.130),
            text="NEXT",
            fgcolor=WHITE,
            size=TILE_SIZE * 0.8,
            bgcolor=BLACK,
        )
        self.font.render_to(
            self.app.screen,
            (SCREEN_WIDTH + (MENU_WIDHT * TILE_SIZE // 2) - 40, WIN_HEIGHT * 0.400),
            text="SCORE",
            fgcolor=WHITE,
            size=TILE_SIZE * 0.8,
            bgcolor=BLACK,
        )
        self.font.render_to(
            self.app.screen,
            (SCREEN_WIDTH + (MENU_WIDHT * TILE_SIZE // 2) - 40, WIN_HEIGHT * 0.440),
            text=f'{self.app.tetris.score}',
            fgcolor=WHITE,
            size=TILE_SIZE * 0.8,
            bgcolor=BLACK,
        )
        self.font.render_to(
            self.app.screen,
            (SCREEN_WIDTH + (MENU_WIDHT * TILE_SIZE // 2) - 40, WIN_HEIGHT * 0.480),
            text='Level',
            fgcolor=WHITE,
            size=TILE_SIZE * 0.8,
            bgcolor=BLACK,
        )
        self.font.render_to(
            self.app.screen,
            (SCREEN_WIDTH + (MENU_WIDHT * TILE_SIZE // 2) - 40, WIN_HEIGHT * 0.520),
            text=f'{self.app.tetris.level}',
            fgcolor=WHITE,
            size=TILE_SIZE * 0.8,
            bgcolor=BLACK,
        )


class Tetris:
    def __init__(self, app):
        self.app = app
        self.sprite_group = pg.sprite.Group()
        self.field_array = self.get_field_array()
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current=False)
        self.speed_up = False

        self.score = 0
        self.level = 1
        self.full_lines = 0
        self.lines_completed = 0
        self.points_per_line = {0:0,1:100, 2:300, 3:500, 4:800}

    def get_score(self):
        self.score += self.points_per_line[self.full_lines] * self.level
        self.full_lines = 0

    

    def check_full_lines(self):
        row = GRID_HEIGHT - 1
        for y in range(GRID_HEIGHT - 1, -1, -1):
            for x in range(GRID_WIDTH):
                self.field_array[row][x] = self.field_array[y][x]
                if self.field_array[y][x]:
                    self.field_array[row][x].pos = vec(x, y)
            if sum(map(bool, self.field_array[y])) < GRID_WIDTH:
                row -= 1
            else:
                for x in range(GRID_WIDTH):
                    self.field_array[row][x].alive = False
                    self.field_array[row][x] = 0
                self.full_lines += 1
                self.lines_completed += 1
                if self.lines_completed >= 10:
                    self.level += 1
                    self.lines_completed -= 10

    def put_tetromino_in_field_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block

    def get_field_array(self):
        return [[0 for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]

    def is_game_over(self):
        if self.tetromino.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            return True

    def check_tetromino_landing(self):
        if self.tetromino.landing:
            if self.is_game_over():
                self.__init__(self.app)
            else:
                self.speed_up = False
                self.next_tetromino.current = True
                self.put_tetromino_in_field_array()
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(self, current=False)

    def control(self, pressed_key):
        if pressed_key == pg.K_LEFT:
            self.tetromino.move(direction="left")
        elif pressed_key == pg.K_RIGHT:
            self.tetromino.move(direction="right")
        elif pressed_key == pg.K_UP:
            self.tetromino.rotate()
        elif pressed_key == pg.K_DOWN:
            self.speed_up = True

    def draw_grid(self):
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                pg.draw.rect(
                    self.app.screen,
                    BLACK,
                    (
                        x * TILE_SIZE,
                        y * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE,
                    ),
                    1,
                )

    def update(self):
        trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.speed_up]
        if trigger:
            self.tetromino.update()
            self.check_full_lines()
            self.check_tetromino_landing()
            self.get_score()
        self.sprite_group.update()

    def draw(self):
        self.draw_grid()
        self.sprite_group.draw(self.app.screen)
