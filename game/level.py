
from game.Player import Player
from game.map import Map
from game.sprites import Sprite

import pygame as pg
from pygame import Vector2

g = 30 # pesanteur
acc = Vector2(0, g)

class Level:
    map: Map = Map(None, None)
    player: Player = None
    other_players = [] # List of other players from online

    def __init__(self):
        self.scale = 5

class Projectiles:

    def __init__(self, sprite : Sprite, emitter : Player, position : Vector2, damage : int, speed : Vector2):
        self.sprite = sprite
        self.emitter = emitter
        self.position = position
        self.damage = damage

    def update_position(self, dt: float) -> Vector2:
        self.speed += acc*dt
        self.position += self.speed*dt + acc * (dt ** 2) / 2

        return self.position

    
