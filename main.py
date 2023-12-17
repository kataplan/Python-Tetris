from settings import *
from tetris import *
from preview import *
from sidebar import *
import sys


class App:
    def __init__(self) -> None:
        pg.init()
        pg.display.set_caption("Tetris")
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        font = ft.Font(FONT_PATH)
        self.preview = Preview(font)
        self.tetris = Tetris(self)
        self.sidebar = Sidebar(self, font)

        # SFX
        self.sfx = {
            "move_piece" :pg.mixer.Sound(os.path.join(os.getcwd(), 'assets/sounds/sfx/move_piece.wav')),
            "rotate_piece" :pg.mixer.Sound(os.path.join(os.getcwd(), 'assets/sounds/sfx/rotate_piece.wav')),
            "line_clear" :pg.mixer.Sound(os.path.join(os.getcwd(), 'assets/sounds/sfx/line_clear.wav')),
            "level_up" :pg.mixer.Sound(os.path.join(os.getcwd(), 'assets/sounds/sfx/level_up.wav')),
            "tetris_4" :pg.mixer.Sound(os.path.join(os.getcwd(), 'assets/sounds/sfx/tetris_4_lines.wav')),
            "game_over" :pg.mixer.Sound(os.path.join(os.getcwd(), 'assets/sounds/sfx/game_over.wav')),
            "piece_landed" :pg.mixer.Sound(os.path.join(os.getcwd(), 'assets/sounds/sfx/piece_landed.wav')),
        }
        

    def update(self):
        self.tetris.update()
        self.clock.tick(FPS)

    def draw(self):
        self.screen.fill(color=BLACK)
        self.screen.fill(color=GREY, rect=(0, 0, *GRID_SIZE))
        self.tetris.draw()
        self.preview.draw()
        self.sidebar.draw()
        pg.display.flip()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.quit or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.tetris.control()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    app = App()
    app.run()
