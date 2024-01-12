from settings import *
from tetris import *
from preview import *
from sidebar import *
import pygame.freetype as ft
import sys


class App:
    def __init__(self) -> None:
        pg.init()
        pg.display.set_caption("Tetris")
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.font = ft.Font(FONT_PATH)
        self.game_start = True

        # Init Game classes
        self.preview = Preview(self.font)
        self.tetris = Tetris(self)
        self.sidebar = Sidebar(self, self.font)

        # Sounds
        self.soundbar = {
            "move_piece": pg.mixer.Sound(
                os.path.join(os.getcwd(), "assets/sounds/sfx/move_piece.wav")
            ),
            "rotate_piece": pg.mixer.Sound(
                os.path.join(os.getcwd(), "assets/sounds/sfx/rotate_piece.wav")
            ),
            "line_clear": pg.mixer.Sound(
                os.path.join(os.getcwd(), "assets/sounds/sfx/line_clear.wav")
            ),
            "level_up": pg.mixer.Sound(
                os.path.join(os.getcwd(), "assets/sounds/sfx/level_up.wav")
            ),
            "tetris_4": pg.mixer.Sound(
                os.path.join(os.getcwd(), "assets/sounds/sfx/tetris_4_lines.wav")
            ),
            "game_over": pg.mixer.Sound(
                os.path.join(os.getcwd(), "assets/sounds/sfx/game_over.wav")
            ),
            "piece_landed": pg.mixer.Sound(
                os.path.join(os.getcwd(), "assets/sounds/sfx/piece_landed.wav")
            ),
        }

    def show_game_over_screen(self):
        """
        Display the game over screen.
        """
        # Fill the screen with a gray background
        self.screen.fill(GREY)

        # Get width of text elements
        game_over_width, _ = self.font.get_rect("Game Over", size=TILE_SIZE * 2).size
        restart_width, _ = self.font.get_rect("Game Over", size=TILE_SIZE * 2).size

        # Render "Game Over" text
        self.font.render_to(
            self.screen,
            ((WIN_WIDTH - game_over_width) // 2, (WIN_HEIGHT // 2) - TILE_SIZE),
            text="Game Over",
            fgcolor=RED,  # Rojo
            size=TILE_SIZE * 2.05,
        )

        # Render "Press 'r' to restart" text
        self.font.render_to(
            self.screen,
            ((WIN_WIDTH - restart_width) // 2, (WIN_HEIGHT // 2) + TILE_SIZE),
            text="Press 'r' to restart",
            fgcolor=(255, 255, 255),  # Blanco
            size=TILE_SIZE,
        )
        # Update the screen
        pg.display.flip()
        self.tetris = None

    def update(self):
        """
        Update the game state.
        """
        if self.game_start:
            self.tetris.update()
            self.clock.tick(FPS)

    def draw(self):
        """
        Draw the game elements on the screen.
        """
        self.screen.fill(color=BLACK)
        self.screen.fill(color=GREY, rect=(0, 0, *GAME_SIZE))

        if self.game_start:
            self.tetris.draw()
            self.preview.draw()
            self.sidebar.draw()
        else:
            self.show_game_over_screen()
        pg.display.flip()

    def check_events(self):
        """
        Check for user input events.
        """
        for event in pg.event.get():
            if event.type == pg.quit or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if self.game_start:
                    self.tetris.control()
                else:
                    if event.key == pg.K_r:
                        self.game_start = True
                        self.tetris = Tetris(self)

    def run(self):
        """
        Main game loop.
        """
        while True:
            self.check_events()
            if not self.game_start:
                self.show_game_over_screen()
            else:
                self.update()
                self.draw()


if __name__ == "__main__":
    app = App()
    app.run()
