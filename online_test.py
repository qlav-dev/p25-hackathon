import pygame as pg

from sys import argv
import game

FPS_CAP = 60

def main(*args):
    """
    client_mode: 1 -> client, 2 -> server
    """
    pg.display.init()

    clock = pg.time.Clock() # Clock init

    width, height = 1000, 1000
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("Slimes with guns")

    # Chargement des ressources
    player_spritesheet = pg.image.load(r"sprites/slime-basic-spritesheet.png").convert_alpha()

    # Creation du jeu:
    level = game.Level()
    level.player = game.Player(
        game.Sprite(player_spritesheet, (5, 1), (0, 0), level.scale, hue_offset=0),
        pg.Vector2(10, 0),
        pg.Vector2(0, 0)
    )
    
    running = True
    dt = 1

    while (running):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
    
        screen.fill((255, 255, 255))

        level.player.update(dt)

        screen.blit(level.player.sprite.image, level.player.position)

        pg.display.flip()
        dt = clock.tick(FPS_CAP) / 1000 # In s

if __name__ == "__main__":
    main(argv[1:])