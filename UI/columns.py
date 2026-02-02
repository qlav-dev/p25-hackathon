import pygame as pg
from UI.element import Element
from copy import copy

class Column(Element):
    """
    A column of elements.
    """

    def __init__(self, *args, vertical_margin: int = 5, elements: list[Element] = None, **kwargs):

        self.elements = elements
        if self.elements == None:
            self.elements = []

        self.size = (0,0)
        self._surf = None
        self.vertical_margin = vertical_margin

    def propagate_colors(self):
        for e in self.elements:
            e.colors = copy(self.colors)
            e.propagate_colors()

    def update(self):

        top = 0
        for e in self.elements:
            e.relative_mouse_pos = [
                self.relative_mouse_pos[0],
                self.relative_mouse_pos[1] - top
            ]

            top += e.size[1] + self.vertical_margin

            e.update()
    
    def _render(self):

        children_surfaces = [i.surface for i in self.elements]
        max_width = max(i.size[0] for i in self.elements)
        height = sum(i.size[1] for i in self.elements)

        if not self.force_size:
            self.size = (max_width, height + self.vertical_margin * (len(self.elements) - 1))

        # Checks if needed to create new surface
        if self._surf == None or self._surf.get_size() != self.size:
            self._surf = pg.surface.Surface(self.size, pg.SRCALPHA, 32)
        else:
            self._surf.fill(pg.color.Color(0, 0, 0, 0)) # Otherwise, clears it

        y = 0
        for i, e in enumerate(self.elements):
            self._surf.blit(children_surfaces[i], (0, y))
            y += self.vertical_margin + e.size[1]
        
        return self._surf

class Columns(Element):
    """
    Allows to put multiple elements side by side.
    columns is a LIST OF COLUMN of elements.

    exemple of usage:
    Columns(
        columns = [
            Column(elements = []), Column(elements = [])
        ]
    )
    """

    def __init__(self, *args, columns: list[Column] = None, col_margin: int = 10, **kwargs):
        super().__init__(*args, **kwargs)

        self.columns = columns
        if self.columns == None:
            self.columns = []
        
        self.col_margin = col_margin
        self.surf = None

    def update(self):

        x = 0
        for e in self.columns:
            e.relative_mouse_pos = [
                    self.relative_mouse_pos[0] - x,
                    self.relative_mouse_pos[1]
                ]
            
            x += e.size[0] + self.col_margin

            e.update()
    
    def propagate_colors(self):
        for e in self.columns:
            e.colors = copy(self.colors)
            e.propagate_colors()

    def _render(self):
        
        child_elements_surfaces = [col.surface for col in self.columns]
        col_widths = [col.size[0] for col in self.columns] # Width of columns
        col_height = max(col.size[1] for col in self.columns) # Max of col height

        if not self.force_size:
            self.size = (
                sum(col_widths) + (len(self.columns) - 1) * self.col_margin,
                col_height,
            ) # Total size

        # Checks if needed to create new surface
        if self.surf == None or self.surf.get_size() != self.size:
            self.surf = pg.surface.Surface(self.size, pg.SRCALPHA, 32)
        else:
            self.surf.fill(pg.color.Color(0, 0, 0, 0)) # Otherwise, clears it

        x = 0   # X Position of col
        for i, col in enumerate(child_elements_surfaces):
            self.surf.blit(col, (x, 0))
            x += col_widths[i] + self.col_margin

        return self.surf