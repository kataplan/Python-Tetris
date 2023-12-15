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
        self.set_timer()
        self.sidebar = Sidebar(self, font)

    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.anim_trigger = False
        self.fast_anim_trigger = False
        base_interval = 0.8  # milisegundos (0.8 segundos)
        interval = int(
            ((base_interval - (self.tetris.level - 1) * 0.007)) ** (self.tetris.level - 1)
        ) * 1000
        pg.time.set_timer(self.user_event, interval)
        pg.time.set_timer(self.fast_user_event, int(interval / FAST_ANIM_TIME_MULT))

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
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.quit or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.tetris.control(pressed_key=event.key)
            elif event.type == self.user_event:
                self.anim_trigger = True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    app = App()
    app.run()
