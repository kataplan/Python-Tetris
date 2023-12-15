from re import S
from settings import *
from tetromino import *
import pygame.freetype as ft
import pathlib


class Tetris:
    def __init__(self, app):
        self.app = app
        self.sprite_group = pg.sprite.Group()
        self.field_array = self.get_field_array()
        self.speed_up = False

        #Hold Mechanic
        self.can_hold = True
        self.hold_piece = None

        self.default_sprites = self.load_block_images("default")
        self.remove_sprites = self.load_block_images("remove")

        self.current_bag = list(TETROMINOES.keys())
        random.shuffle(self.current_bag)
        self.next_bag = list(TETROMINOES.keys())
        random.shuffle(self.next_bag)

        self.next_shapes = [self.current_bag.pop(0) for _ in range(3)]
        self.app.preview.set_next_shapes(self.next_shapes)

        self.tetromino = self.create_new_tetromino()

        self.score = 0
        self.level = 1
        self.full_lines = 0
        self.lines_completed = 0
        self.points_per_line = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}

    def hold(self):
        if not self.hold_piece:
            # Si no hay pieza en retención, guarda la pieza actual y obtén la siguiente
            self.hold_piece = self.tetromino.shape
            self.sprite_group.remove(self.tetromino.blocks)
            self.tetromino = self.create_new_tetromino()
        else:
            # Elimina los bloques de la pieza activa del sprite_group
            hold_piece = self.tetromino.shape
            self.sprite_group.remove(self.tetromino.blocks)
            self.tetromino = Tetromino(self, self.hold_piece)
            self.hold_piece = hold_piece
        self.can_hold = False
        self.app.sidebar.set_hold_shape(self.hold_piece)


    def get_score(self):
        self.score += self.points_per_line[self.full_lines] * self.level
        self.full_lines = 0

    def load_block_images(self, folder):
        files = [
            item
            for item in pathlib.Path(SPRITE_BLOCK_PATH + "/" + folder).rglob("*.png")
            if item.is_file()
        ]
        images = {file.stem: pg.image.load(file).convert_alpha() for file in files}
        images = {
            key: pg.transform.scale(image, (TILE_SIZE, TILE_SIZE))
            for key, image in images.items()
        }
        return images

    def create_new_tetromino(self):
        shape = self.get_next_shape()
        return Tetromino(self, shape)
    
    def create_hold_tetromino(self):
        shape = self.hold_piece
        return Tetromino(self, shape)

    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        next_in_bag = self.current_bag.pop(0)
        self.next_shapes.append(next_in_bag)
        self.app.preview.set_next_shapes(self.next_shapes)

        if len(self.current_bag) <= 3:
            self.current_bag.extend(self.next_bag)
            random.shuffle(self.next_bag)

        return next_shape

    def check_full_lines(self):
        row = TETRIS_GRID_H - 1
        for y in range(TETRIS_GRID_H - 1, -1, -1):
            for x in range(TETRIS_GRID_W):
                self.field_array[row][x] = self.field_array[y][x]
                if self.field_array[y][x]:
                    self.field_array[row][x].pos = vec(x, y)
            if sum(map(bool, self.field_array[y])) < TETRIS_GRID_W:
                row -= 1
            else:
                for x in range(TETRIS_GRID_W):
                    self.field_array[row][x].alive = False
                    self.field_array[row][x] = 0
                self.full_lines += 1
                self.lines_completed += 1
                if self.lines_completed % 10 == 0:
                    self.level += 1
                

    def put_tetromino_in_field_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block

    def get_field_array(self):
        return [[0 for x in range(TETRIS_GRID_W)] for y in range(TETRIS_GRID_H)]

    def is_game_over(self):
        if self.tetromino.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            return True

    def check_tetromino_landing(self):
        if self.tetromino.landing:
            if self.is_game_over():
                self.__init__(self.app)
            else:
                self.speed_up = False
                self.can_hold = True
                self.put_tetromino_in_field_array()
                self.tetromino = self.create_new_tetromino()


    def control(self, pressed_key):
        if pressed_key == pg.K_LEFT:
            self.tetromino.move(direction="left")
        elif pressed_key == pg.K_RIGHT:
            self.tetromino.move(direction="right")
        elif pressed_key == pg.K_UP:
            self.tetromino.rotate()
        elif pressed_key == pg.K_DOWN:
            self.speed_up = True
        elif pressed_key == pg.K_SPACE:  # Barra espaciadora para hard drop
            self.hard_drop()
        elif pressed_key == pg.K_LSHIFT or pressed_key == pg.K_c:
            if self.can_hold:
                self.hold()

    def hard_drop(self):
        while not self.tetromino.landing:
            self.tetromino.move("down")
        self.check_tetromino_landing()

    def draw_grid(self):
        for x in range(TETRIS_GRID_W):
            for y in range(TETRIS_GRID_H):
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
