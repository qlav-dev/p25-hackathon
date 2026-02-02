import pygame as pg
from pygame.color import Color
from UI.anchors import AnchorMode

class Element:
    """
    Every inside-window objects is an `Element` object. 
    An class inheriting from element must implement:
    * _render(self) -> Surface, that renders the element into a pygame surface (Local coordinates). It MUST update its size
    * update(self, *...) -> None, that updates the element. 
    """
    
    relative_mouse_pos: tuple[int, int] = [0,0] # Modified by the window or the encapsulating element !
    force_size = False
    
    def __init__(self,
        colors : list[Color] = None,
        margin: list[int, int] = [10,0],
        inner_margin: list[int, int] = [2,2],
        anchor_mode: AnchorMode = AnchorMode.DEFAULT, # NOT YET IMPLEMENTED
        force_size: bool = False,
        size: list[int, int] = None,
        ):
        """  
            force_size: Allows to set a size on creation. The size is set in the argument size, and will not be changed automatically.
            If force_size is false, then the size of the element is calculated dynamically.

            Moreover, some elements need the size arguement to be set. If so, it is written explicitly in the docstring.
        """

        self.force_size = force_size
        
        self.size = size
        if self.size == None:
            self.size = [1,1]

        self.colors = colors
        if self.colors == None:
            self.colors = [Color(50, 50, 50, 90), Color(20, 20, 100, 90), Color(196, 196, 196, 90), Color(247, 40, 60, 90)]

        self.margin = margin
        self.inner_margin = inner_margin
        self.anchor_mode = anchor_mode
    
    def hovered(self) -> bool:
        return (self.relative_mouse_pos[0] >= 0 and self.relative_mouse_pos[0] <= self.size[0]) and\
    (self.relative_mouse_pos[1] >= 0 and self.relative_mouse_pos[1] <= self.size[1])

    def propagate_colors(self) -> None:
        """ For elements that contains elements """
        ...
    
    # Properties
    @property
    def width(self) -> int:
        return self.size[0]
    
    @width.setter
    def width(self, value: int):
        self.size[0] = value
        
    
    @property
    def height(self) -> int:
        return self.size[1]
    
    @height.setter
    def height(self, value: int):
        self.size[1] = value
    
    def _render(self) -> pg.Surface:
        ...
        # The render function should return a surface representing the final element, and update the size of the element accordingly
        
    def update(self):
        """
        Must update the elements, as well as its children elements, and update their relative_mouse_pos
        """
        ...
        
    @property
    def surface(self) -> pg.Surface:
        """ 
        Calling this updates self.size !
        """ 
        return self._render()