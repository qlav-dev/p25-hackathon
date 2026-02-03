import pygame as pg

from level_editor.level import Level
from level_editor.default import DefaultLevel

class Editor:
    """
    Design général: l'éditeur LIT un niveau, et permet de le modifier. Si aucun niveau n'est donné, il LIT un niveau par défaut
    """

    def __init__(self, level: Level = None, grid_color: pg.color.Color = None, position: list[int, int] = None, zoom: float = 1):

        self.level = level if level is not None else DefaultLevel()
        self.grid_color = grid_color if grid_color is not None else pg.color.Color(255, 0, 0)
        
        # NOT USED AT ALL BY THIS OBJECT
        self.position = position if position is not None else [0,0]
        self.zoom = zoom

    def render(self) -> pg.surface.Surface:
        """
            Returns the level editor graphical interface
        """

        cell_size = self.level.spritesheet.cell_size

        # Surf creation
        surf = pg.surface.Surface((self.level.map_size[0] * cell_size, self.level.map_size[1] * cell_size))
        surf.fill(self.level.background_color)

        # Grid drawing
        for i in range(1, self.level.map_size[0]):
            pg.draw.line(surf, self.grid_color, (i * cell_size, 0), (i * cell_size, cell_size * self.level.map_size[1]))
        for j in range(1, self.level.map_size[1]):
            pg.draw.line(surf, self.grid_color, (0, j * cell_size), (cell_size * self.level.map_size[0], j * cell_size))

        return surf