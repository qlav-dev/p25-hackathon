import pygame as pg

from sys import argv
import game

FPS_CAP = 60

def main(*args):

    pg.display.init()

    clock = pg.time.Clock() # Clock init

    # screen init
    width, height = 16 * 16 * 3, 16 * 16 * 3
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("Slimes with guns")

    # Chargement des ressources
    player_spritesheet = pg.image.load(r"sprites/slime-basic-spritesheet.png").convert_alpha()

    # Creation du jeu:
    level = game.Level()
    level.map = game.getMap('sprites/example_map.png', 'sprites/example_hitbox_map.png',16 * level.scale)
    
    #player init
    level.player = game.Player(
        game.Sprite(player_spritesheet, (5, 1), (0, 0), level.scale, hue_offset=0),
        pg.Vector2(10, 0),
        pg.Vector2(0, 0),
        user_name="Username"
    )


    running = True
    dt = 1

    while (running):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
    
        screen.fill((255, 255, 255))

        #   Physics update
        level.player.update(dt)
        level.player.wall_collision_manager(level)

        screen.blit(level.map.map_surf, (0,0))
        screen.blit(level.player.sprite.image, level.player.position)
        

        pg.display.flip()
        dt = clock.tick(FPS_CAP) / 1000 # In s



if __name__ == "__main__":
    main()