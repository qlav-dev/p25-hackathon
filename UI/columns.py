import pygame as pg
from UI.element import Element
from copy import copy

class Column(Element):
    """
    A column of elements.
    """

    def __init__(self, *args, elements: list[Element] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.elements = elements
        if self.elements == None:
            self.elements = []

        self.size = (0,0)
        self._surf = None

    def propagate_colors(self):
        for e in self.elements:
            e.colors = copy(self.colors)
            e.propagate_colors()

    def update(self, *args, events: list[pg.event.Event] = [], **kwargs):

        top = self.margin[1]
        for e in self.elements:
            e.relative_mouse_pos = [
                self.relative_mouse_pos[0] - self.margin[0],
                self.relative_mouse_pos[1] - top
            ]

            e.update(events = events)
            top += e.size[1]
    
    def _render(self):

        children_surfaces = [i.surface for i in self.elements]
        max_width = max(i.size[0] for i in self.elements)
        height = sum(i.size[1] for i in self.elements)

        # -- UPDATE SIZE -- 
        if not self.force_size:
            self.size = (max_width + self.margin[0] * 2, height + self.margin[1] * 2)

        # Checks if needed to create new surface
        if self._surf == None or self._surf.get_size() != self.size:
            self._surf = pg.surface.Surface(self.size, pg.SRCALPHA, 32)
        else:
            self._surf.fill(pg.color.Color(0, 0, 0, 0)) # Otherwise, clears it
            
        # RENDERING
        y = self.margin[1]
        for i, e in enumerate(self.elements):
            self._surf.blit(children_surfaces[i], (self.margin[0], y))
            y += e.size[1]

        #pg.draw.circle(self._surf, pg.color.Color(0, 0, 255), self.relative_mouse_pos, 3)
        
        return self._surf

class Row(Element):
    """
    Allows to put multiple elements side by side.

    exemple of usage:
    Row(
        elements = [
            Column(elements = []), Column(elements = [])
        ]
    ) For a grid

    or as well, 
    
        Row(
        elements = [
            Element1, Element2
        ]
    ) 
    """

    def __init__(self, *args, elements: list[Element] = None, **kwargs):
        super().__init__(*args, **kwargs)

        self.elements = elements
        if self.elements == None:
            self.elements = []
        
        self.surf = None

    def update(self, *args, events: list[pg.event.Event] = [], **kwargs):

        x = self.margin[0]
        for e in self.elements:
            e.relative_mouse_pos = [
                    self.relative_mouse_pos[0] - x,
                    self.relative_mouse_pos[1] - self.margin[1]
                ]
            
            e.update(events = events)
            x += e.size[0]
    
    def propagate_colors(self):
        for e in self.elements:
            e.colors = copy(self.colors)
            e.propagate_colors()

    def _render(self):
        
        child_elements_surfaces = [col.surface for col in self.elements]
        col_widths = [col.size[0] for col in self.elements] # Width of columns
        col_height = max(col.size[1] for col in self.elements) + self.margin[1] # Max of col height

        # -- SIZE UPDATE --
        if not self.force_size:
            self.size = (
                sum(col_widths) + 2 * self.margin[0],
                col_height + 2 * self.margin[1],
            ) # Total size

        # Checks if needed to create new surface
        if self.surf == None or self.surf.get_size() != self.size:
            self.surf = pg.surface.Surface(self.size, pg.SRCALPHA, 32)
        else:
            self.surf.fill(pg.color.Color(0, 0, 0, 0)) # Otherwise, clears it

        # Rendering
        x = self.margin[0]   # X Position of col
        for i, col in enumerate(child_elements_surfaces):
            self.surf.blit(col, (x, self.margin[1]))
            x += col_widths[i]

        #pg.draw.circle(self.surf, pg.color.Color(0, 255, 0), self.relative_mouse_pos, 3)

        return self.surf