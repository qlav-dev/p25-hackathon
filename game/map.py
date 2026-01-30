
import pygame as pg



class Map:
    map_surf: pg.Surface = None
    map_collider = None
    map_id: int = 0

    def __init__(self, map_surf: pg.Surface, map_collider):
        self.map_surf = map_surf
        self.map_collider = map_collider
