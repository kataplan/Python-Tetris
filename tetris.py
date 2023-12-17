from re import S
from settings import *
from timer import *
from tetromino import *
import pygame.freetype as ft
import pathlib


class Tetris:
    def __init__(self, app):
        self.app = app
        self.sprite_group = pg.sprite.Group()
        self.field_array = self.get_field_array()
        self.speed_up = False

        # Hold Mechanic
        self.can_hold = True
        self.hold_piece = None

        # Sprites
        self.default_sprites = self.load_block_images("default")
        self.remove_sprites = self.load_block_images("remove")

        # 7 Bags
        self.current_bag = list(TETROMINOES.keys())
        random.shuffle(self.current_bag)
        self.next_bag = list(TETROMINOES.keys())
        random.shuffle(self.next_bag)
        self.next_shapes = [self.current_bag.pop(0) for _ in range(3)]
        self.app.preview.set_next_shapes(self.next_shapes)

        self.tetromino = self.create_new_tetromino()

        # Score
        self.score = 0
        self.full_lines = 0
        self.level = 1
        self.lines_completed = 0
        self.combo_counter = -1
        self.is_landed = False
        self.is_row_eliminated = False
        self.points_per_line = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}
        self.perfect_clear_bonus = {1: 800, 2: 1200, 3: 1800, 4: 2000}

        # Time
        self.down_speed = (
            (0.8 - ((self.level - 1) * 0.007)) ** (self.level - 1)
        ) * 1000
        self.down_speed_faster = self.down_speed * 0.3
        self.down_pressed = False
        self.timers = {
            "vertical move": Timer(self.down_speed, True, func=self.move_down),
            "horizontal move": Timer(MOVE_WAIT_TIME),
            "rotate": Timer(ROTATE_WAIT_TIME),
        }
        self.timers["vertical move"].activate()

    def move_down(self):
        self.tetromino.move(direction="down")

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
        lines_cleared = 0
        row = TETRIS_GRID_H - 1
        for y in range(TETRIS_GRID_H - 1, -1, -1):
            for x in range(TETRIS_GRID_W):
                self.field_array[row][x] = self.field_array[y][x]
                if self.field_array[y][x]:
                    self.field_array[row][x].pos = vec(x, y)
            if sum(map(bool, self.field_array[y])) < TETRIS_GRID_W:
                row -= 1
            else:
                lines_cleared += 1
                for x in range(TETRIS_GRID_W):
                    self.field_array[row][x].alive = False
                    self.field_array[row][x] = 0
                self.full_lines += 1
                self.lines_completed += 1
                if self.lines_completed % 10 == 0:
                    self.level += 1
                    self.down_speed = (
                        (0.8 - (self.level - 1) * 0.007) ** (self.level - 1)
                    ) * 1000
                    self.down_speed_faster = self.down_speed * 0.3
                    self.timers["vertical move"].duration = self.down_speed
        if lines_cleared > 0:
            self.is_row_eliminated = True
            self.combo_counter += 1
            score_reward = 50 * self.combo_counter * self.level
            self.score += score_reward
            if self.check_perfect_clear():
                perfect_clear_lines = lines_cleared
                self.score += self.perfect_clear_bonus[perfect_clear_lines] * self.level
            else:
                self.score += self.points_per_line[self.full_lines] * self.level
                self.full_lines = 0

        else:
            self.is_row_eliminated = False

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
            self.is_landed = True
            if self.is_game_over():
                self.__init__(self.app)
            else:
                self.speed_up = False
                self.can_hold = True
                self.put_tetromino_in_field_array()
                self.tetromino = self.create_new_tetromino()
        else:
            self.is_landed = False

    def control(self):
        keys = pg.key.get_pressed()
        if not self.timers["horizontal move"].active:
            if keys[pg.K_LEFT]:
                self.tetromino.move(direction="left")
                self.timers["horizontal move"].activate()
            elif keys[pg.K_RIGHT]:
                self.tetromino.move(direction="right")
                self.timers["horizontal move"].activate()

        if not self.timers["rotate"].active:
            if keys[pg.K_UP]:
                self.tetromino.rotate(is_clock_wise=True)
                self.timers["rotate"].activate()
            elif keys[pg.K_z] or keys[pg.K_LCTRL]:
                self.tetromino.rotate(is_clock_wise=False)
                self.timers["rotate"].activate()

        if not self.down_pressed and keys[pg.K_DOWN]:
            self.down_pressed = True
            self.timers["vertical move"].duration = self.down_speed_faster
        if self.down_pressed and not keys[pg.K_DOWN]:
            self.down_pressed = False
            self.timers["vertical move"].duration = self.down_speed

        if keys[pg.K_SPACE]:
            self.hard_drop()
        if keys[pg.K_LSHIFT] or keys[pg.K_c]:
            if self.can_hold:
                self.hold()

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def hard_drop(self):
        count = 0
        while not self.tetromino.landing:
            self.tetromino.move("down")
            count += 1
        self.is_landed = True
        self.score += count * 2

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

    def check_perfect_clear(self):
        for y in range(TETRIS_GRID_H):
            for x in range(TETRIS_GRID_W):
                if self.field_array[y][x]:
                    return False
        return True

    def update(self):
        self.timer_update()
        self.check_tetromino_landing()
        self.check_full_lines()
        if self.is_landed and not self.is_row_eliminated:
            self.combo_counter = -1
        self.sprite_group.update()

    def draw(self):
        self.draw_grid()
        ghost_positions = self.tetromino.get_ghost_positions()
        for pos in ghost_positions:
            pg.draw.rect(
                self.app.screen,
                WHITE,  # Color del bloque fantasma
                (pos.x * TILE_SIZE, (pos.y + 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                2,  # Grosor del contorno
                2,
            )

        self.sprite_group.draw(self.app.screen)
