
from game.Player import Player
from game.map import Map

class Level:
    map: Map = Map(None, None)
    player: Player = None
    other_players = [] # List of other players from online

    def __init__(self):
        self.scale = 5
