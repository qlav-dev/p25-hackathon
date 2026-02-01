from __future__ import annotations

from UI.element import Element
import pygame as pg

class Button(Element):
    text: str = ""
    font_size : int = 12
    
    on_click: function
    on_down: function
    on_release: function
    
    pressed: function # Boolean that triggers the button press if hovered by the mouse
    
    border_radius: int = 2
        
    def __init__(self, 
                text: str = "Button", 
                font: str = 'Segoe UI', 
                font_size = 12,
                on_click: function = lambda: ...,
                on_down: function = lambda: ...,
                on_release: function = lambda: ...,
                pressed = lambda: pg.mouse.get_pressed(3)[0],
                border_radius: int = 2, **kwargs):
        
        if not pg.font.get_init(): # Inits the font module
            pg.font.init()
        
        super().__init__(**kwargs)
        
        self.text = str(text)
        self.font_size = font_size
        self.font: pg.font.Font = pg.font.SysFont(font, self.font_size)
        
        self.on_click = on_click
        self.on_down = on_down
        self.on_release = on_release
        
        self.border_radius = border_radius
        
        self._last_pressed = False
        
        self.pressed = pressed
            
    def update(self):
        pressed = self.pressed()
        hovered = self.hovered()
        
        if hovered and pressed and not self._last_pressed: # Clicked
            self.on_click()
            
        if hovered and pressed: # Down
            self.on_down()
            
        if hovered and not pressed and self._last_pressed: # Released
            self.on_release()
            
        self._last_pressed = pressed
    
    def _render(self) -> pg.Surface:
        text_surface = self.font.render(self.text, False, self.color_2)
                    
        button_rect = pg.Rect(0, 0, text_surface.get_width() + 2.0 * self.inner_margin[0], text_surface.get_height()  + 2.0 * self.inner_margin[1])

        surf = pg.Surface(button_rect.size, pg.SRCALPHA, 32)
        
        pg.draw.rect(surf, self.color_1 if not self.hovered() else self.color_3, button_rect, border_radius = self.border_radius)
        surf.blit(text_surface, self.inner_margin)
        
        self.size = surf.get_size()
        
        return surf