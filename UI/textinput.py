from UI.element import Element
import pygame as pg

class TextInput(Element):
    
    # Uses pygame start_text_input() and stop_text_input()
        
    def __init__(self, place_holder: str = "Enter Your Text", 
                text: str = "", 
                active: bool = False,
                font: str = 'Segoe UI', 
                font_size = 12,
                size: tuple[int, int] = (100, 25),
                pressed = lambda: pg.mouse.get_pressed(3)[0], **kwargs):
        
        super().__init__(self)
        
        self.place_holder = place_holder
        self.text = text
        
        self.font_size = font_size
        self.font: pg.font.Font = pg.font.SysFont(font, self.font_size)
        
        self.size = size
        
        self.pressed = pressed
        self.active = active # Whether the text input is listening/waiting for user input
        
        self._last_pressed = False
    
    def update(self):
        pressed = self.pressed()
        hovered = self.hovered()
        
        if hovered and pressed and not self._last_pressed: #Clicked
            self.active = not self.active

            if self.active:
                pg.key.start_text_input()
            else:
                pg.key.stop_text_input()
        
        if self.active:
            for event in pg.event.get():
                if event.type == pg.TEXTINPUT:
                    print(event)
                    self.text += event.text
        
        self._last_pressed = pressed
    
    def _render(self):
        
        text_surface = ...
        surface = pg.Surface(self.size, pg.SRCALPHA, 32)
        
        if len(self.text) == 0:
            #Shows placeholder
            text_surface = self.font.render(self.place_holder, False, self.color_3)
        else:
            text_surface = self.font.render(self.text, False, self.color_2)
        
        if self.active:
            surface.fill(self.color_4)
        else:
            surface.fill(self.color_1)
        
        surface.blit(text_surface, (0,0))
        
        return surface