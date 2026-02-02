from UI.element import Element
from pygame.color import Color
import pygame as pg

from UI.button import Button
from UI.columns import Column, Row
from UI.text import Text

from copy import copy

class Window:
    """
    An UI window inside the pygame screen surface.
    Returns a surface with transparent backround, ready to be blit into your project's screen
    
    Everything in your UI is called an element, with some being buttons, text or sliders... 
    """ 
    
    elements: list[Element] = []
    
    caption_bar_height: int = 20
    caption_bar_text_size: int = 12
    caption_bar_color: Color = Color(10, 10, 255, 90)
    caption_bar: pg.rect = ...

    border_radius: int = 3

    # rendering stuff
    surface = None

    movable = True

    def close(self):
        self._closed = True
    
    def auto_resize(self):
        for e in self.elements:
            e.surface

        if (len(self.elements) == 0):
            return None
        
        self.size[0] = max(E.width + E.margin[0] * 2.0 for E in self.elements)
        self.size[1] = self.caption_bar_height + (not self.collapsed) * sum(E.height + E.margin[1] * 2.0 for E in self.elements)
    
    def propagate_colors(self):
        """
        Propagates the window's color to its elements
        """
        for e in self.elements + [self._caption_bar_element]:
            e.colors = copy(self.colors)
            e.propagate_colors() # For elements that contain elements
    
    def append(self, item: Element):
        """
            Appends an element.
            Same as Window.element.append()
        """
        self.elements.append(item)

    def collapse(self):
        self.collapsed = True - self.collapsed
        self.auto_resize()
    
    def __init__(self, caption: str = "Window", font: str = "Segoe UI", caption_bar_text_size: int = 12, movable: bool = True, position : list = None, colors: list[Color] = None, size: list[int, int] = None, collapsed: bool = False, collapsable: bool = True, closable: bool = False) -> None:
        if not pg.font.get_init(): # Inits the font module
            pg.font.init()
            

        self._closed = False

        # Window getting dragged
        self._dragging = False
        self._dragging_from = (0,0)

        # Elements inside the window
        self.elements: Element = []
        
        self.position: list[int, int] = position
        if self.position == None:
            self.position = [0,0]

        self.size = size
        if self.size == None:
            self.size: list[int, int] = [100, 100]

        # Caption Bar settings
        self.caption_bar_height: int = 20
        self.caption_bar_text_size: int = 12
        self.caption_bar_color: Color = Color(10, 10, 255, 90)
        self.caption_bar: pg.rect = ...

        self.caption = caption
        
        self.caption_bar_text_size = caption_bar_text_size
        self.font = pg.font.SysFont(font, self.caption_bar_text_size)
        
        self.collapsed = collapsed
        self._collapse_button = Button(text = "c", font_size = self.caption_bar_text_size, on_click = self.collapse,)
        self._close_button = Button(text = "x", font_size = self.caption_bar_text_size, on_click = self.close, )
        self._caption_text = Text(text = self.caption, font = font, font_size = self.caption_bar_text_size)

        self.collapsable = collapsable
        self.closable = closable

        # Caption bar definition
        self._caption_bar_element = Row(elements = [Column(elements = [self._caption_text], margin = [5, 3])])
        if self.collapsable:
            self._caption_bar_element.elements = [Column(elements = [self._collapse_button])] + self._caption_bar_element.elements
        if self.closable:
            self._caption_bar_element.elements = [Column(elements = [self._close_button])] + self._caption_bar_element.elements

        self.border_radius: int = 3

        self.colors = colors
        if self.colors == None:
            self.colors : list[Color] = [Color(50, 50, 50, 90),Color(255, 255, 255, 255) ,Color(196, 196, 196, 150),Color(247, 40, 60, 150)]
        
        self._last_pressed = False

    def update(self, mouse_pressed: bool, events: list[pg.event.Event]):
        mp = pg.mouse.get_pos() # Mouse position
        
        self.caption_bar = pg.Rect(
            0, 0,
            self.size[0], self.caption_bar_height
        )

        # Updating the caption bar element -- BEFORE the window moves
        self._caption_bar_element.relative_mouse_pos = (mp[0] - self.position[0] - self._caption_bar_element.margin[0], mp[1] - self.position[1])
        self._caption_bar_element.update()
        
        # window movement
        if self.movable and self.caption_bar.collidepoint(mp[0] - self.position[0], mp[1] - self.position[1]) and mouse_pressed:
            self._dragging = True
            self._dragging_from = (mp[0] - self.position[0], mp[1] - self.position[1])
        if not mouse_pressed:
            self._dragging = False

        # Moves the window if the caption bar is pressed
        if self._dragging: 
            self.position = [mp[0] - self._dragging_from[0], mp[1] - self._dragging_from[1]] # Center
        
        top = None
        if len(self.elements) != 0:
            top = self.position[1] + self.caption_bar_height + self.elements[0].margin[1] # Distance from top of the window

        # Updating everything
        for e in self.elements:
            
            e.relative_mouse_pos = (
                mp[0] - self.position[0] - e.margin[0],
                mp[1] - top - e.margin[1],
            )
            
            e.update(events = events)
            
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
        

        # Caption Bar
        pg.draw.rect(surface = self.surface, color = self.caption_bar_color, rect = self.caption_bar,
                   border_top_left_radius = self.border_radius, border_top_right_radius = self.border_radius) # Border radius

        caption_bar = self._caption_bar_element.surface
        
        self.surface.blit(caption_bar, (10, 0))
        
        # drawing elements
        if not self.collapsed:
            pg.draw.rect(self.surface, self.colors[0], main_frame, # Window body
                border_bottom_left_radius = self.border_radius, border_bottom_right_radius = self.border_radius) # Border radius

            top = None
            if len(self.elements) != 0:
                top = self.caption_bar_height + self.elements[0].margin[1] # Distance from top of the window

            for E in self.elements:
                self.surface.blit(E.surface, (E.margin[0], top + E.margin[1]))
                top += E.height + E.margin[1] * 2
            
        return self.surface
        