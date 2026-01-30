import pygame as pg
from sys import argv
import online

class Entity:
    ...

class Sprite(pg.sprite.Sprite):
    def __init__(self, image: pg.Surface, spritesheet_size):
        super().__init__()

        self.sheet_size_px = (image.get_width(), image.get_height())
        self.sheet_size = ()

        self.sheet = image
        self.sheet = pg.transform.scale(self.sheet, (
            self.sheesheet_size_px[0] * self.sheet_size[0], self.sheet_size_px[1] * self.sheet_size[1])
        )

        self.texture = pg.Surface((64, 64), pg.SRCALPHA)
        self.texture.blit(self.sheet, (0, 0))


def main(*args):
    """
    client_mode: 1 -> client, 2 -> server
    """
    pg.display.init()

    width, height = 1000, 1000
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("Slimes with guns")

    basic = Sprite(pg.image.load(r"sprites/slime-basic-spritesheet.png").convert_alpha())

    running = True

    while (running):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False

        screen.fill((255, 255, 255))
        screen.blit(basic.texture, (10, 10))
        pg.display.flip()

if __name__ == "__main__":
    main(argv[1:])