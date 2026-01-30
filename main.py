import pygame as pg

from sys import argv
import online
import game

def main(*args):
    """
    client_mode: 1 -> client, 2 -> server
    """
    pg.display.init()

    width, height = 1000, 1000
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("Slimes with guns")

    # Chargement des ressources
    player_spritesheet = pg.image.load(r"sprites/slime-basic-spritesheet.png").convert_alpha()

    # Creation du jeu:
    level = game.Level()
    level.player = game.Player(
        game.Sprite(player_spritesheet, (5, 1), (0, 0), level.scale, hue_offset=0),
        np.Vector2(0, 0),
        np.Vector2(0, 0)
    )
    
    running = True
    
    i = 0
    while (running):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
    
        screen.fill((255, 255, 255))

        basic.set_texture_coordinates((0,0))

        screen.blit(level.player.sprite.image, (10, 10))

        pg.display.flip()

if __name__ == "__main__":
    main(argv[1:])