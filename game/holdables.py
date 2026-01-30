
from game.sprites import Sprite

class Holdables:
    def __init__(self, sprite: Sprite):
        self.sprite = sprite

class Gun(Holdables):
    ...