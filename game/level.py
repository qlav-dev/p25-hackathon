
from game.Player import Player
from game.map import Map
from game.sprites import Sprite

import pygame as pg
from pygame import Vector2

class Level:
    map: Map = Map(None, None)
    player: Player = None
    other_players = [] # List of other players from online
    projectiles = [] # List of projectiles in game
    g: float = 1000 # Pesanteur
    scale = 2



    
