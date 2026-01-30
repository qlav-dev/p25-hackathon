import pygame as pg
import numpy as np
from sprites import Sprite
from map import Map


def load_map(path : str):
    surf = pg.image.load(path)
    return pg.surfarray.pixels2d(surf)
"""
This code transforms a png file to a 2D array.
Colour code:
0 - empty
1 - grass block
2 - dirt block
"""

def align(positions, cell_size):
    pos1, pos2 = positions[0], positions[1]
    return ((pos1[0] * cell_size, pos1[1] * cell_size), ((pos2[0]+1) * cell_size, (pos2[1] + 1) * cell_size))
"""
Function to transform a tuple of 2 positions in png coordinates to tuple of 2 positions in our grid convention
"""


def distance(pos1, pos2):
    return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def load_hitbox_array(path : str, cell_size):
    surf = pg.image.load(path)
    hitbox = pg.PixelArray(surf)
    n,m = len(hitbox), len(hitbox[0])

    colours = []
    max_distances = []
    positions = []

    for i_0 in range(n):
        for j_0 in range(m):
            for i_1 in range(n):
                for j_1 in range(m):

                    if hitbox[i_0,j_0] == hitbox[i_1, j_1] and hitbox[i_0,j_0] != 0:
                        clr = hitbox[i_0,j_0]

                        if clr in colours:
                            index = colours.index(clr)
                            dist = distance( (i_0, j_0), (i_1, j_1) )
                            if dist > max_distances[index]:
                                positions[index] = ((i_0, j_0), (i_1, j_1))
                                max_distances[index] = dist 
                        else:
                            colours.append(clr)
                            positions.append( ((i_0, j_0), (i_1,j_1)) )
                            max_distances.append(0)

    return [align(pos, cell_size) for pos in positions]
"""
This code transforms a png file to a 2D array, for hitboxes.
Each colour represents a different rectangle for hitboxes.
"""

def array_to_rect(rectangles):
    py_rects = []
    for rect in rectangles:
        x0 = rect[0][0]
        y0 = rect[0][1]
        height = rect[1][1] - rect[0][1]
        width = rect[1][0] - rect[0][0]
        py_rects.append(pg.Rect(x0, y0, width, height))
    return py_rects

def getHitboxRects(path : str, cell_size):
    return array_to_rect(load_hitbox_array(path, cell_size))
"""
Function to load the hitboxes as PyGame rectangles.
"""

def getSurface(path : str, cell_size):
    scale_factor = cell_size / 16

    map_matrix = load_map(path)

    map_height = len(map_matrix)
    map_width = len(map_matrix[0])

    width, height = map_width*cell_size, map_height*cell_size

    terrain_spritesheet = pg.image.load("sprites/terrain-basic-spritesheet.png")
    sprite_grass = Sprite(terrain_spritesheet, (1, 2), (0, 0), scale_factor, hue_offset=0)
    sprite_dirt = Sprite(terrain_spritesheet, (1, 2), (0, 1), scale_factor, hue_offset=0)

    background = pg.Surface((width, height), pg.SRCALPHA)
    for i in range(len(map_matrix)):
        for j in range(len(map_matrix[0])):
            if map_matrix[i,j] == 2:
                background.blit(sprite_dirt.image, (i*cell_size, j*cell_size))
            elif map_matrix[i,j] == 1:
                background.blit(sprite_grass.image, (i*cell_size, j*cell_size))

    return background

"""
cell_size is in terms of coordinates that are used by the physics engine.
"""
def getMap(surface_path : str, collider_path : str, cell_size):
    surface = getSurface(surface_path, cell_size)
    collider = getHitboxRects(collider_path, cell_size)
    return Map(surface, collider)



