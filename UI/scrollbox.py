from copy import copy
import pygame as pg
from UI.element import Element

class ScrollBox(Element):
    """
    A box that can contain elements, and be scrolled into.

    It has a FIXED height
    """

    scroll_position: float = 0 # FROM 0 to 1
    mouse_scrolled: bool = False # Is it being scrolled

    def __init__(self, *args, elements: list[Element] = None, height: int = 300, scrollbar_width: int = 10, margins:int = (10, 2), **kwargs):
        """ 
        Height is fixed
        """

        super().__init__(*args, **kwargs)

        self.elements = elements
        if self.elements == None:
            self.elements = []
    
        self.height = height
        self.scrollbar_width = scrollbar_width
        self.margins = margins

        self.child_total_height = 1 # Total height of child elements. Updated in _render.

        # Rects def:
        self.scrollbar_container_rect = pg.rect.Rect(0, 0, 0, 0)
        self.scrollbar_rect = pg.rect.Rect(0, 0, 0, 0)
        self.scrollbar_rect_height = 1

        self.surf = None

    def propagate_colors(self):
        for e in self.elements:
            e.colors = copy(self.colors)

    def scrollbar_rect_hovered(self):
        return (self.scrollbar_rect.collidepoint(*self.relative_mouse_pos))

    def update(self, *args, events: list[pg.event.Event] = [], **kwargs):

        if (self.scrollbar_rect_hovered() and pg.mouse.get_pressed(3)[0]):
            self.mouse_scrolled = True
        
        if (not pg.mouse.get_pressed(3)[0]):
            self.mouse_scrolled = False
        
        if (self.mouse_scrolled):
            self.scroll_position = min(max(0, (self.relative_mouse_pos[1] - self.scrollbar_rect_height / 2) / (self.size[1] - self.scrollbar_rect_height)), 1)

        # Updating child elements and their relative mouse positions
        top = - self.scroll_position * (self.child_total_height - self.size[1])
        for e in self.elements:
            e.relative_mouse_pos = [
                self.relative_mouse_pos[0] - self.scrollbar_width - self.margins[0],
                self.relative_mouse_pos[1] - top
            ]

            top += e.size[1] + self.margins[1]

            e.update(events = events)
    
    def _render(self) -> pg.Surface:

        child_elements_surfaces = [e.surface for e in self.elements]
        # Calculating total child height
        self.child_total_height = sum(e.size[1] for e in self.elements) + self.margins[1] * (len(self.elements) - 1)

        max_element_width = max(e.size[0] for e in self.elements)

        if not self.force_size:
            self.size = (max_element_width + self.scrollbar_width, self.height)

        # Checks if needed to create new surface
        if self.surf == None or self.surf.get_size() != self.size:
            self.surf = pg.surface.Surface(self.size, pg.SRCALPHA, 32)
        else:
            self.surf.fill(pg.color.Color(0, 0, 0, 0)) # Otherwise, clears it

        # -- ENCAPSULATING RECTANGLE --
        pg.draw.rect(self.surf, self.colors[0], pg.rect.Rect(0, 0, self.size[0], self.size[1]))

        # -- SCROLLBAR -- 
        self.scrollbar_container_rect = pg.rect.Rect(0, 0, self.scrollbar_width, self.size[1])

        self.scrollbar_rect_height =  self.size[1] ** 2 / self.child_total_height
        self.scrollbar_rect = pg.rect.Rect(0, self.scroll_position * (self.size[1] - self.scrollbar_rect_height), self.scrollbar_width, self.scrollbar_rect_height)

        pg.draw.rect(self.surf, self.colors[0], self.scrollbar_container_rect)
        pg.draw.rect(self.surf, self.colors[2] if not self.scrollbar_rect_hovered() else self.colors[1], self.scrollbar_rect)

        # -- ELEMENTS --

        top = - self.scroll_position * (self.child_total_height - self.size[1]) # When at the bottom, there must be the last items

        for i, e in enumerate(self.elements):
            self.surf.blit(child_elements_surfaces[i], (self.scrollbar_width + 10, top))
            top += self.margins[1] + e.size[1]

            if top > self.size[1]:
                break

        return self.surf