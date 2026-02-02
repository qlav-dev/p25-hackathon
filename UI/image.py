from UI.element import Element
import pygame as pg

class Image(Element):
    def __init__(self, path: str, **kwargs):
        """
            For this element, the size argument is MENDATORY ! 
        """
        super().__init__(**kwargs)

        self.path = path
        self._loaded_path = path

        self._image = pg.image.load(path).convert()
    
    def update(self, *args, **kwargs):
        if self._loaded_path != self.path:
            self._image = pg.image.load(self.path)
            
            self._loaded_path = self.path
 
    def _render(self) -> pg.Surface:
        surf = pg.Surface(self.size, pg.SRCALPHA, 32)
        surf.blit(pg.transform.scale(self._image, self.size), (0,0))

        return surf