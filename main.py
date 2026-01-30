import pygame as pg
from sys import argv

def main(args):
    
    pg.display.init()

    width, height = 300, 300
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