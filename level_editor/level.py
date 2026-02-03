import pygame as pg

class SpriteSheet:

    def __init__(self, spritesheet_image: pg.image, cell_size: int):
        self.spritesheet_image: pg.Surface = spritesheet_image
        self.cell_size = cell_size

        self.total_size = (
            self.spritesheet_image.get_width() // self.cell_size, 
            self.spritesheet_image.get_height() // self.cell_size
        )# In cells

    def get_sprite(self, coordinates: tuple[int ,int]):
        """ Returns the sprite on the spritesheet at coordinates (int, int), as a pygame surface """
        if coordinates[0] < 0 or coordinates[0] > self.total_size[0] or coordinates[1] < 0 or coordinates[1] > self.total_size[1]:
            raise IndexError("Coordinates index out of range")
        
        return self.spritesheet_image.subsurface(pg.rect.Rect(coordinates[0] * self.cell_size, coordinates[1] * self.cell_size, self.cell_size, self.cell_size))

class Level:

    def __init__(self, spritesheet: SpriteSheet = None, map_size: tuple[int, int] = None, background_color: pg.color.Color = None):
        """
        map size in cells.
        """
        self.spritesheet = spritesheet
        self.map_size = map_size
        self.background_color = background_color if background_color is not None else pg.color.Color(0, 0, 0)

