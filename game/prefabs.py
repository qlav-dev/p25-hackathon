"""
This file contains some pre-fabricated objects (or methods that return pre-fabricated objects).
"""

from game.sprites import Sprite
from game.holdables import *

basic_gun = lambda gun_sprite, projectile_sprite, scale: BasicGun(
    sprite = Sprite(gun_sprite, (1,1), (0,0), scale, hue_offset = 0),
    power = 50000,
    recoil = .5,
    projectile_sprite = Sprite(projectile_sprite, (1,1), (0,0), scale, hue_offset = 0),
    damage = 1,
    projectile_mass = 1
)

triple_gun = lambda gun_sprite, projectile_sprite, scale: MultiGun(
    no_shots = 3,
    shoot_angle_span = 20,
    sprite = Sprite(gun_sprite, (1,1), (0,0), scale, hue_offset = 0),
    power = 120000,
    recoil = 0.3,
    projectile_sprite = Sprite(projectile_sprite, (1,1), (0,0), scale, hue_offset = 0),
    damage = 1,
    projectile_mass = 1
)