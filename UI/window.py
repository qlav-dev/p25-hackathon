from UI.element import Element
from pygame.color import Color
import pygame as pg

class Window:
    """
    An UI window inside the pygame screen surface.
    Returns a surface with transparent backround, ready to be blit into your project's screen
    
    Everything in your UI is called an element, with some being buttons, text or sliders... 
    """ 
    
    elements: Element = []
    
    position: list[int, int] = [0,0]
    size: list[int, int] = [100, 100]
    
    caption_bar_height: int = 20
    caption_bar_text_size: int = 12
    caption_bar_color: Color = Color(10, 10, 255, 90)
    caption_bar: pg.rect = ...
    
    # Window getting dragged
    dragging = False 

    border_radius: int = 3

    # rendering stuff
    surface = None

    movable = True
    
    def auto_resize(self):
        for e in self.elements:
            e.surface

        if (len(self.elements) == 0):
            return None
        
        self.size[0] = max(E.width + E.margin[0] * 2.0 for E in self.elements)
        self.size[1] = sum(E.height + E.margin[1] * 2.0 for E in self.elements) + self.caption_bar_height
    
    def propagate_colors(self):
        """
        Propagates the window's color to its elements
        """
        for e in self.elements:
            e.color_1 = self.color_1
            e.color_2 = self.color_2
    
    def append(self, item: Element):
        """
            Appends an element.
            Same as Window.element.append()
        """
        self.elements.append(item)
    
    def __init__(self, caption: str = "Window", font: str = "Segoe UI", caption_bar_text_size: int = 12, movable: int = True, position : list = None) -> None:
        if not pg.font.get_init(): # Inits the font module
            pg.font.init()
            
        self.caption = caption
        
        self.caption_bar_text_size = caption_bar_text_size
        self.font = pg.font.SysFont(font, self.caption_bar_text_size)
        
        self.elements: Element = []
        
        self.position: list[int, int] = position
        if self.position == None:
            self.position = [0,0]

        self.size: list[int, int] = [100, 100]

        self.caption_bar_height: int = 20
        self.caption_bar_text_size: int = 12
        self.caption_bar_color: Color = Color(10, 10, 255, 90)
        self.caption_bar: pg.rect = ...

        self.border_radius: int = 3

        self.color_1 : Color = Color(50, 50, 50, 90)
        self.color_2 : Color = Color(255, 255, 255, 255) 
        self.color_3 : Color = Color(196, 196, 196, 150),
        self.color_4 : Color = Color(247, 40, 60, 150),
        
        self._last_pressed = False

    def update(self, mouse_pressed: bool):
        mp = pg.mouse.get_pos() # Mouse position
        
        self.caption_bar = pg.Rect(
            0, 0,
            self.size[0], self.caption_bar_height
        )
        
        if self.movable and self.caption_bar.collidepoint(mp[0] - self.position[0], mp[1] - self.position[1]) and mouse_pressed:
            self.dragging = True
        if not mouse_pressed:
            self.dragging = False

        # Mouves the window if the caption bar is pressed
        if self.dragging: 
            self.position = [mp[0] - self.size[0] / 2.0, mp[1] - self.caption_bar_height / 2.0] # Center
        
        top = None
        if len(self.elements) != 0:
            top = self.position[1] + self.caption_bar_height + self.elements[0].margin[1] # Distance from top of the window

        for e in self.elements:
            
            e.relative_mouse_pos = (
                mp[0] - self.position[0] - e.margin[0],
                mp[1] - top - e.margin[1],
            )
            
            e.update()
            
            top += e.height + e.margin[1]
    
    def get_surface(self) -> pg.surface:
        """
        Builds and returns the surface containing the window
        """
        if self.surface == None or self.surface.get_size() != self.size:
            self.surface = pg.Surface(self.size, pg.SRCALPHA, 32)
        
        main_frame = pg.Rect(
            0, self.caption_bar_height, 
            self.size[0], self.size[1] - self.caption_bar_height)
        
        caption_text = self.font.render(self.caption, False, self.color_2)
        
        # Caption Bar
        pg.draw.rect(surface = self.surface, color = self.caption_bar_color, rect = self.caption_bar,
                   border_top_left_radius = self.border_radius, border_top_right_radius = self.border_radius) # Border radius
        
        self.surface.blit(caption_text, (10, 0))
        
        pg.draw.rect(self.surface, self.color_1, main_frame, # Window body
                    border_bottom_left_radius = self.border_radius, border_bottom_right_radius = self.border_radius) # Border radius
        
        top = None
        if len(self.elements) != 0:
            top = self.caption_bar_height + self.elements[0].margin[1] # Distance from top of the window

        for E in self.elements:
            self.surface.blit(E.surface, (E.margin[0], top + E.margin[1]))
            top += E.height + E.margin[1] * 2
        
        return self.surface
        