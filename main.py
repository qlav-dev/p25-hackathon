import pygame as pg
from sys import argv
import online

def main(args, client_mode: online.clientType):
    """
    client_mode: 1 -> client, 2 -> server
    """
    pg.display.init()

    width, height = 500, 500
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("Platformer")

    running = True

    while (running):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False

        screen.fill((0, 0, 0))
        pg.display.flip()

if __name__ == "__main__":
    main(argv[1:])