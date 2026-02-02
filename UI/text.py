from UI.element import Element
import pygame as pg


class Text(Element):
    
    text: str = ""
    font_size : int = 12

    def __init__(self, text: str, font: str = 'Segoe UI', font_size = 12, **kwargs):
        
        super().__init__(**kwargs)
        
        if not pg.font.get_init(): # Inits the font module
            pg.font.init()
        
        self.text = str(text)
        self.font_size = font_size
        self.font: pg.font.Font = pg.font.SysFont(font, self.font_size)
    
    def _render(self) -> pg.Surface:
        text_surface = self.font.render(self.text, False, self.colors[1])

        if not self.force_size:
            self.size[0] = 1.5 * text_surface.get_width() + self.inner_margin[0] * 2
            self.size[1] = text_surface.get_height() + self.inner_margin[1] * 2
        
        return text_surface