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

    Use get_element_by_{id/ labels} to find an element
    """ 
    
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
        if (len(self.body.elements) == 0):
            return None
        
        self.body.surface
        self.caption_bar.surface
        self.size[0] = self.body.size[0]
        self.size[1] = self.caption_bar_height + (not self.collapsed) * self.body.size[1]
    
    def propagate_colors(self):
        """
        Propagates the window's color to its elements
        """
        self.caption_bar.colors = copy(self.colors)
        self.caption_bar.propagate_colors()
        self.body.colors = copy(self.colors)
        self.body.propagate_colors()

    def append(self, item: Element):
        """
            Appends an element.
            Same as Window.element.append()
        """
        self.body.elements.append(item)

    @property
    def elements(self):
        return self.body.elements

    @elements.setter
    def elements(self, val: list[Element]):
        self.body.elements = val

    @property 
    def margin(self):
        return self.body.margin
    
    @margin.setter
    def margin(self, val):
        self.body.margin = val

    def collapse(self):
        self.collapsed = True - self.collapsed
        self.auto_resize()

    def get_element_by_label(self, label: str):
        return self.body.find_by_label(label)

    def get_element_by_id(self, id: int):
        return self.body.find_by_id(id)
    
    def __init__(self, 
        caption: str = "Window", 
        font: str = "Segoe UI", 
        caption_bar_text_size: int = 12, 
        movable: bool = True, 
        margin: list[int, int] = None, 
        position : list = None, 
        colors: list[Color] = None, 
        size: list[int, int] = None, 
        collapsed: bool = False, 
        collapsable: bool = True, 
        closable: bool = False
    ) -> None:
    
        if not pg.font.get_init(): # Inits the font module
            pg.font.init()        

        self._closed = False

        # Window getting dragged
        self._dragging = False
        self._dragging_from = (0,0)

        # The window body element is by default a column
        self.body = Column()
        self.margin = margin if margin is not None else [10, 10]
        
        self.position: list[int, int] = position
        if self.position == None:
            self.position = [0,0]

        self.size = size
        if self.size == None:
            self.size: list[int, int] = [100, 100]

        # Caption Bar settings
        self.caption_bar_text_size: int = 12
        self.caption_bar_color: Color = Color(10, 10, 255, 90)

        self.caption = caption
        
        self.caption_bar_text_size = caption_bar_text_size
        self.font = pg.font.SysFont(font, self.caption_bar_text_size)
        
        self.collapsed = collapsed
        self._collapse_button = Button(text = "c", font_size = self.caption_bar_text_size, on_click = self.collapse, margin = [0, 0])
        self._close_button = Button(text = "x", font_size = self.caption_bar_text_size, on_click = self.close, margin = [0, 0])
        self._caption_text = Text(text = self.caption, font = font, font_size = self.caption_bar_text_size, margin = [0, 0])

        self.collapsable = collapsable
        self.closable = closable

        # Caption bar definition
        self.caption_bar = Row(elements = [Column(elements = [self._caption_text], margin = [5, 5])])
        if self.collapsable:
            self.caption_bar.elements = [Column(elements = [self._collapse_button])] + self.caption_bar.elements
        if self.closable:
            self.caption_bar.elements = [Column(elements = [self._close_button])] + self.caption_bar.elements

        self.border_radius: int = 3

        self.colors = colors
        if self.colors == None:
            self.colors : list[Color] = [Color(50, 50, 50, 90),Color(255, 255, 255, 255) ,Color(196, 196, 196, 150),Color(247, 40, 60, 150)]
        
        self._last_pressed = False

    def update(self, mouse_pressed: bool, events: list[pg.event.Event]):
        mp = pg.mouse.get_pos() # Mouse position
        
        self.caption_bar_rect = pg.Rect(
            0, 0,
            self.size[0], self.caption_bar.size[1]
        )

        # Updating the caption bar element -- BEFORE the window moves
        self.caption_bar.relative_mouse_pos = (mp[0] - self.position[0], mp[1] - self.position[1])
        self.caption_bar.update()
        
        # window movement
        if self.movable and self.caption_bar_rect.collidepoint(mp[0] - self.position[0], mp[1] - self.position[1]) and pg.MOUSEBUTTONDOWN in [e.type for e in events] and mouse_pressed:
            self._dragging = True
            self._dragging_from = (mp[0] - self.position[0], mp[1] - self.position[1])
        if not mouse_pressed:
            self._dragging = False

        # Moves the window if the caption bar is pressed
        if self._dragging: 
            self.position = [mp[0] - self._dragging_from[0], mp[1] - self._dragging_from[1]] # Center
        
        # Updating everything
            
        self.body.relative_mouse_pos = (
            mp[0] - self.position[0],
            mp[1] - self.position[1] - self.caption_bar.size[1],
        )
            
        self.body.update(events = events)
    
    def get_surface(self) -> pg.surface:
        """
        Builds and returns the surface containing the window
        """
        if self.surface == None or self.surface.get_size() != self.size:
            self.surface = pg.Surface(self.size, pg.SRCALPHA, 32)
        
        main_frame = pg.Rect(
            0, self.caption_bar.size[1], 
            self.size[0], self.size[1] - self.caption_bar.size[1])
        
        # Caption Bar
        pg.draw.rect(surface = self.surface, color = self.caption_bar_color, rect = self.caption_bar_rect,
                   border_top_left_radius = self.border_radius, border_top_right_radius = self.border_radius) # Border radius

        caption_bar = self.caption_bar.surface
        
        self.surface.blit(caption_bar, (0, 0))
        
        # drawing elements
        if not self.collapsed:
            pg.draw.rect(self.surface, self.colors[0], main_frame, # Window body
                border_bottom_left_radius = self.border_radius, border_bottom_right_radius = self.border_radius) # Border radius

            self.surface.blit(self.body.surface, (0, self.caption_bar.size[1]))

        return self.surface
        