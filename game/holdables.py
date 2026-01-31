
from game.sprites import Sprite

import pygame as pg
from pygame import Vector2

class Holdables:
    def __init__(self, sprite: Sprite):
        self.sprite = sprite

class Gun(Holdables):
    def __init__(self, sprite: Sprite, power: float, recoil: float):
        """
        The gun "power" is the factor. (power in )
        player.acceleration += direction * power. (Power in N.m^-1)
        """
        super().__init__(sprite)
        self.power = power
        self.recoil = recoil
    
    def fire(self, player, fire_direction):
        """
            Player fired the gun. Fire direction must be normalised
        """
        player.acc += self.power * fire_direction 


