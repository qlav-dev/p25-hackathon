from UI.element import Element
import pygame as pg
from pygame import Color

class TextInput(Element):
    """
        The size argument is MENDATORY 

        Uses pygame start_text_input() and stop_text_input()
    """
        
    def __init__(self, place_holder: str = "Enter Your Text", 
                text: str = "", 
                active: bool = False,
                font: str = 'Segoe UI', 
                font_size = 12,
                pressed = lambda: pg.mouse.get_pressed(3)[0], **kwargs):
        """
        The size argument is MENDATORY 
        """

        super().__init__(self, **kwargs)
        
        self.place_holder = place_holder
        self.text = text
        
        self.font_size = font_size
        self.font: pg.font.Font = pg.font.SysFont(font, self.font_size)
        
        self.pressed = pressed
        self.active = active # Whether the text input is listening/waiting for user input
        
        self._last_pressed = False

        self.colors = [Color(50, 50, 50, 90),Color(255, 255, 255, 255) ,Color(196, 196, 196, 150),Color(247, 40, 60, 150)]
    
    def update(self, events: list[pg.event.Event] = []):
        pressed = self.pressed()
        hovered = self.hovered()
        
        if hovered and pressed and not self._last_pressed: #Clicked
            self.active = not self.active

            if self.active:
                pg.key.start_text_input()
            else:
                pg.key.stop_text_input()
        
        # TEXT INPUT
        if self.active:
            for event in events:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        self.text = self.text[:-1]
                    if event.key == pg.K_RETURN:
                        self.active = False

                elif event.type == pg.TEXTINPUT:
                    self.text += event.text
        
        self._last_pressed = pressed
    
    def _render(self):
        
        text_surface = ...
        surface = pg.Surface(self.size, pg.SRCALPHA, 32)

        if len(self.text) == 0:
            #Shows placeholder
            text_surface = self.font.render(self.place_holder, False, self.colors[2])
        else:
            text_surface = self.font.render(self.text, False, self.colors[1])
        
        if self.active:
            surface.fill(self.colors[3])
        else:
            surface.fill(self.colors[0])
        
        surface.blit(text_surface, (0,0))
        
        return surface