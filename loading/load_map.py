import pygame as pg

"""
This code transforms a png file to a 2D array.
Colour code:
0 - empty
1 - grass block
2 - dirt block
"""
def load_map(path : str):
    surf = pg.image.load(path)
    return pg.surfarray.pixels2d(surf)
