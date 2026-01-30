import pygame as pg
from sys import argv
import online
import game

class Entity:
    ...

def main(*args):
    """
    client_mode: 1 -> client, 2 -> server
    """
    pg.display.init()

    width, height = 1000, 1000
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("Slimes with guns")

    basic = game.Sprite(pg.image.load(r"sprites/slime-basic-spritesheet.png").convert_alpha(),
    (5, 1),
    (0, 0),
    10)

    running = True

    while (running):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
    
        screen.fill((255, 255, 255))

        basic.set_texture_coordinates((0,0))

        screen.blit(basic.texture, (10, 10))

        pg.display.flip()

if __name__ == "__main__":
    main(argv[1:])