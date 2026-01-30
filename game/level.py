
from game.Player import Player
from game.map import Map

class Level:
    map: Map = None
    player: Player = None

    def __init__(self):
        self.scale = 5
