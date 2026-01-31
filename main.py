import pygame as pg

from sys import argv
import game

from random import randint

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
    gun_sprite = pg.image.load(r"sprites/gun-basic.png").convert_alpha()
    projectile_sprite = pg.image.load(r"sprites/projectile-basic.png").convert_alpha()

    # Creation du jeu:
    level = game.Level()
    level.map = game.getMap('sprites/example_map.png', 'sprites/example_hitbox_map.png',16 * level.scale)
    
    #player init
    level.player = game.Player(
        sprite = game.Sprite(player_spritesheet, (5, 1), (0, 0), level.scale, hue_offset = randint(0, 1000) / 1000),
        position = pg.Vector2(100, 0),
        user_name = "Username",
        mass = 5
    )

    # Default gun
    level.player.inventory = [
        game.prefabs.triple_gun(gun_sprite, projectile_sprite, level.scale),
    ]


    running = True
    dt = 1

    while (running):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            
            if e.type == pg.MOUSEBUTTONDOWN:
                mousePos = pg.Vector2(pg.mouse.get_pos())
                if pg.mouse.get_pressed(3)[0]:
                    fire_direction = (level.player.position + pg.Vector2(level.player.rect.width / 2, level.player.rect.height / 2) - mousePos).normalize()
                    level.player.inventory[level.player.holding].fire(level, fire_direction)
            
        screen.fill((0, 230, 255))

        # Physics update
        level.player.inventory[level.player.holding].update(dt, level.player)
        level.player.update(dt, level)

        for proj in level.projectiles:
            proj.update(dt, level)

        # Kills projectiles that are too far away
        level.projectiles = [i for i in level.projectiles if (i.position - level.player.position).length() < i.despawn_distance]

        # --- RENDER --- #

        # Render player
        screen.blit(level.player.sprite.image, level.player.position)
        
        # Render projectiles
        for proj in level.projectiles:
            screen.blit(proj.sprite.image, proj.position)

        # Render map
        screen.blit(level.map.map_surf, (0,0))

        # Render gun
        screen.blit(pg.transform.rotate(level.player.inventory[level.player.holding].sprite.image, 
            180-(level.player.position + pg.Vector2(level.player.rect.width / 2, level.player.rect.height / 2) - pg.Vector2(pg.mouse.get_pos())).normalize().as_polar()[1])
            , level.player.position)

        pg.display.flip()
        dt = clock.tick(FPS_CAP) / 1000 # In s



if __name__ == "__main__":
    main()