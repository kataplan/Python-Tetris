from xml.etree.ElementTree import QName
from numpy import True_
from settings import *
import random


class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, pos):
        self.tetromino = tetromino
        self.pos = vec(pos) + INIT_POS_OFFSET
        self.alive = True
        super().__init__(tetromino.tetris.sprite_group)
        self.image = tetromino.image
        self.rect = self.image.get_rect()

        self.sfx_image = self.image.copy()
        self.sfx_image.set_alpha(110)
        self.sfx_speed = random.uniform(0.2, 0.6)
        self.sfx_cycles = random.randrange(6, 8)
        self.sfx_duration = random.uniform(1.0, 2.0)  # Nueva línea

        self.cycle_counter = 0

    def sfx_end_time(self):
        self.cycle_counter += 0.1
        if self.cycle_counter > self.sfx_duration:  # Modificado
            self.cycle_counter = 0
            return True
        return False  # Modificado

    def sfx_run(self):
        self.image = self.sfx_image
        self.pos.y -= self.sfx_speed
        self.image = pg.transform.rotate(
            self.image, pg.time.get_ticks() * self.sfx_speed
        )

    def is_alive(self):
        if not self.alive:
            if not self.sfx_end_time():
                self.sfx_run()
            else:
                self.kill()

    def rotate(self, pivot_pos, clockwise=True):
        translated = self.pos - pivot_pos
        angle = 90 if clockwise else -90
        rotated = translated.rotate(angle)
        return rotated + pivot_pos

    def set_rect_pos(self):
        pos = self.pos
        self.rect.topleft = pos * TILE_SIZE

    def update(self):
        self.is_alive()
        self.set_rect_pos()

    def is_collide(self, pos):
        x, y = int(pos.x), int(pos.y)
        if (
            0 <= x < TETRIS_GRID_W
            and y < TETRIS_GRID_H
            and (y < 0 or not self.tetromino.tetris.field_array[y][x])
        ):
            return False
        return True


class Tetromino:
    def __init__(self, tetris, shape):
        self.tetris = tetris
        self.shape = shape
        self.image = tetris.default_sprites[TETROMINOES_COLORS[shape]]

        self.blocks = [Block(self, pos) for pos in TETROMINOES[shape]]

        self.rotation_state = 0
        self.landing = False

    def get_ghost_positions(self):
        ghost_positions = [block.pos for block in self.blocks]

        while not self.is_collide([pos + vec(0, 1) for pos in ghost_positions]):
            ghost_positions = [pos + vec(0, 1) for pos in ghost_positions]

        # Retrocede una posición para corregir la colisión
        ghost_positions = [pos - vec(0, 1) for pos in ghost_positions]

        return ghost_positions

    def rotate(self, is_clock_wise):
        self.tetris.app.sfx["rotate_piece"].set_volume(0.5)
        self.tetris.app.sfx["rotate_piece"].play()
        if self.shape == "O":
            return
        pivot_pos = self.blocks[0].pos
        new_block_positions = [
            block.rotate(pivot_pos, is_clock_wise) for block in self.blocks
        ]
        new_rotation_state = self.get_new_rotation_state(is_clock_wise)
        wall_kick_data = self.get_wall_kicks(
            ROTATION_STATES[self.rotation_state],
            ROTATION_STATES[new_rotation_state],
        )
        for kick_offset in wall_kick_data:
            kicked_positions = [pos + kick_offset for pos in new_block_positions]
            if not self.is_collide(kicked_positions):
                for i, block in enumerate(self.blocks):
                    block.pos = kicked_positions[i]
                self.rotation_state = new_rotation_state
                break

    def get_new_rotation_state(self, is_clock_wise):
        # Obtén el cambio de estado según la dirección de rotación
        if is_clock_wise:
            rotation_change = 1
        else:
            rotation_change = -1

        # Calcula el nuevo estado de rotación sin modificar el atributo
        new_rotation_state = (self.rotation_state + rotation_change) % 4

        # Si el resultado es -1, conviértelo a 3
        if new_rotation_state == -1:
            new_rotation_state = 3

        return new_rotation_state

    def get_wall_kicks(self, initial_state, final_state):
        key = f"{initial_state}{final_state}"
        if self.shape == "I":
            return I_WALL_KICKS[key]
        return JLSTZ_WALL_KICKS[key]

    def move(self, direction):
        move_direction = MOVE_DIRECTIONS[direction]
        new_block_positions = [block.pos + move_direction for block in self.blocks]
        is_collide = self.is_collide(new_block_positions)
        if not is_collide:
            if direction !="down":
                self.tetris.app.sfx["move_piece"].play()
            for block in self.blocks:
                block.pos += move_direction
            if self.tetris.down_pressed:
                self.tetris.score += 1
        elif direction == "down":
            self.landing = True

    def is_collide(self, block_positions):
        return any(map(Block.is_collide, self.blocks, block_positions))
