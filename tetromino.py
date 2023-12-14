from numpy import True_
from settings import *
import random


class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, pos, shape):
        self.tetromino = tetromino
        self.pos = vec(pos) + INIT_POS_OFFSET
        self.alive = True
        super().__init__(tetromino.tetris.sprite_group)
        self.image = tetromino.image
        self.rect = self.image.get_rect()

    def is_alive(self):
        if not self.alive:
            self.kill()

    def rotate(self, pivot_poss):
        translated = self.pos - pivot_poss
        rotated = translated.rotate(90)
        return rotated + pivot_poss

    def set_rect_pos(self):
        pos =  self.pos
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

        self.blocks = [Block(self, pos, shape) for pos in TETROMINOES[shape]]

        self.landing = False

    def rotate(self):
        if self.shape == "O":
            return
        pivot_pos = self.blocks[0].pos
        new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]
        if not self.is_collide(new_block_positions):
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]
        
    def get_wall_kicks(self, initial_state, final_state):
        key = f"{initial_state}{final_state}"
        return WALL_KICKS.get(key, [])

    def move(self, direction):
        move_direction = MOVE_DIRECTIONS[direction]
        new_block_positions = [block.pos + move_direction for block in self.blocks]
        is_collide = self.is_collide(new_block_positions)
        if not is_collide:
            for block in self.blocks:
                block.pos += move_direction
        elif direction == "down":
            self.landing = True

    def is_collide(self, block_positions):
        return any(map(Block.is_collide, self.blocks, block_positions))

    def update(self):
        self.move(direction="down")
