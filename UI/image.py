from UI.element import Element
import pygame as pg

class Image(Element):
    def __init__(self, path: str, **kwargs):
        super().__init__(**kwargs)

        self.path = path
        self._loaded_path = path

        self.image = pg.image.load(path)
        self.image.convert() # Creates a copy to draw more quicky
    
    def update(self):
        if self._loaded_path != self.path:
            self.image = pg.image.load(self.path)
            
            self._loaded_path = self.path
 
    def _render(self) -> pg.Surface:
        surf = pg.Surface(self.size, pg.SRCALPHA, 32)
        surf.blit(pg.transform.scale(self.image, self.size), (0,0))

        return surf