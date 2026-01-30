import pygame as pg
import numpy as np
from sprites import Sprite

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

def load_hitbox_rects(path : str, cell_size):
    return array_to_rect(load_hitbox_array(path, cell_size))
"""
Function to load the hitboxes as PyGame rectangles.
"""

scale_factor = 3




def main(*args):
    """
    client_mode: 1 -> client, 2 -> server
    """
    pg.display.init()

    clock = pg.time.Clock() # Clock init

    width, height = 16*16*scale_factor, 16*16*scale_factor
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("Slimes with guns")

    map_matrix = load_map('sprites/example_map.png')
    print(map_matrix)
    width = 16*16*scale_factor
    height = 16*16*scale_factor
    terrain_spritesheet = pg.image.load("sprites/terrain-basic-spritesheet.png")
    sprite_grass = Sprite(terrain_spritesheet, (1, 2), (0, 0), scale_factor, hue_offset=0)

    background = pg.Surface((width, height), pg.SRCALPHA)
    background.blit(sprite_grass.image, (0,0))

    for i in range(len(map_matrix)):
        for j in range(len(map_matrix[0])):
            if map_matrix[i,j] == 2:
                background.blit(sprite_grass.image, (i*16*scale_factor, j*16*scale_factor))
                
    running = True
    dt = 1

    while (running):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
    
        screen.fill((255, 255, 255))

        screen.blit(background, (0,0))

        pg.display.flip()

if __name__ == "__main__":
    main()

