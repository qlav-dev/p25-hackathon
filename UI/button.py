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
                border_radius: int = 2, 
                **kwargs):
        
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
        
        self._pressed = pressed
            
    def update(self, *args, **kwargs):
        pressed = self._pressed()
        hovered = self.hovered()
        
        if hovered and pressed and not self._last_pressed: # Clicked
            self.on_click()
            
        if hovered and pressed: # Down
            self.on_down()
            
        if hovered and not pressed and self._last_pressed: # Released
            self.on_release()
            
        self._last_pressed = pressed
    
    def _render(self) -> pg.Surface:
        text_surface = self.font.render(self.text, False, self.colors[1])

        if not self.force_size: # SUSSY
            self.size = text_surface.get_size()
        
        btn_rect_size = (self.size[0] + 2.0 * self.inner_margin[0], self.size[1]  + 2.0 * self.inner_margin[1])
        button_rect = pg.Rect(0, 0, *btn_rect_size)

        surf = pg.Surface(btn_rect_size, pg.SRCALPHA, 32)
        
        pg.draw.rect(surf, self.colors[0] if not self.hovered() else self.colors[2], button_rect, border_radius = self.border_radius)
        surf.blit(text_surface, self.inner_margin)

        if not self.force_size:
            self.size = surf.get_size()
        
        return surf