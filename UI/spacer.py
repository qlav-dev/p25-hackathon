import pygame as pg
from UI.element import Element

class Spacer(Element):
    """
    A spacer element.
    """

    def __init__(self, *args, width: int = 0, height: int = 20, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = width
        self.height = height

        self.size = (width, height)
        self.surf = pg.Surface((self.size), pg.SRCALPHA, 32)
    
    def _render(self):
        if not self.force_size: # Goofy
            self.size = (self.width, self.height)
        
        if self.surf.get_size != self.size:
            self.surf = pg.Surface((self.size), pg.SRCALPHA, 32)
        
        return self.surf