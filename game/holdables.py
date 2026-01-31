
from game.sprites import Sprite

import pygame as pg
from pygame import Vector2
import copy

from numpy import cos, sin, deg2rad

class Holdables:
    def __init__(self, sprite: Sprite):
        self.sprite = sprite

class Gun(Holdables):
    def __init__(self, sprite: Sprite, projectile_sprite : Sprite, damage: float, power: float, recoil: float, projectile_mass: float = 1):
        """
        Damage is the amount of damages dealt by the projectiles.

        The gun "power" is the acc factor. (Power in N.m^-1)
        player.acceleration += direction * power. (Power in N.m^-1)
        """
        super().__init__(sprite)
        self.power = power
        self.recoil = recoil
        self.damage = damage
        self.time_since_last_fire = recoil
        self.projectile_sprite = projectile_sprite
        self.projectile_mass = projectile_mass
    
    def fire(self, level, fire_direction):
        ...
    
    def update(self, dt, player):
        self.time_since_last_fire += dt

class BasicGun(Gun):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def fire(self, level, fire_direction):
        """
            Player fired the gun. Fire direction must be normalised
        """
        if self.time_since_last_fire > self.recoil:
            self.time_since_last_fire = 0
            level.player.acc += self.power * fire_direction  / level.player.mass

            level.projectiles.append(
                Projectiles(
                    sprite = self.projectile_sprite,
                    emitter = level.player,
                    position = copy.copy(level.player.position),
                    damage = self.damage,
                    acc = -self.power * fire_direction / self.projectile_mass
                )
            )

class MultiGun(Gun):
    
    def __init__(self, no_shots: int, shoot_angle_span: float, *args, **kwargs):
        """
        shoot_angle_span: float angle in degree < 360.

        The power is the TOTAL power. Meaning, each projectile will get a fraction of the power.
        """
        super().__init__(*args, **kwargs)
        self.no_shots = no_shots
        self.shoot_angle_span = shoot_angle_span

    def fire(self, level, fire_direction):
        """
            Player fired the gun. Fire direction must be normalised
        """
        if self.time_since_last_fire > self.recoil:
            self.time_since_last_fire = 0
            level.player.acc += self.power * fire_direction  / level.player.mass

            for i in range(self.no_shots):
                a = fire_direction.as_polar()[1]
                da = -self.shoot_angle_span / 2 + i * (self.shoot_angle_span) / (self.no_shots - 1)
                angle = Vector2(cos(deg2rad(a + da)), sin(deg2rad(a + da)))

                level.projectiles.append(
                    Projectiles(
                        sprite = self.projectile_sprite,
                        emitter = level.player,
                        position = copy.copy(level.player.position),
                        damage = self.damage,
                        acc = -(self.power / self.no_shots) * angle / self.projectile_mass
                    )
                )

class Projectiles:
    despawn_distance = 1000 # Distance from the player before despawn

    def __init__(self, sprite : Sprite, emitter : "Player", position : Vector2, damage : int, acc : Vector2, mass: float = 1):
        self.sprite = sprite
        self.emitter = emitter
        self.position = position
        self.speed = Vector2(0,0)
        self.acc = acc
        self.damage = damage
        self.mass = mass

    def update(self, dt: float, level):
        self.speed += self.acc * dt
        self.position += self.speed*dt + self.acc * (dt ** 2) / 2

        self.acc = Vector2(0, level.g)

