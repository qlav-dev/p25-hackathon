
from game.sprites import Sprite

class Holdables:
    def __init__(self, sprite: Sprite):
        self.sprite = sprite

class Gun(Holdables):
    def __init__(self, sprite: Sprite, power: float, recoil: float):
        super().__init__(sprite)
        self.power = power
        self.recoil = recoil