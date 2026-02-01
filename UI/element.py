import pygame as pg
from pygame.color import Color
from UI.anchors import AnchorMode

class Element:
    
    relative_mouse_pos: tuple[int, int] = [0,0]
    
    def __init__(self,
        size: list[int, int] = [1,1], 
        
        color_1 : Color = Color(50, 50, 50, 90),
        color_2 : Color = Color(20, 20, 100, 90),
        color_3 : Color = Color(196, 196, 196, 90),
        color_4 : Color = Color(247, 40, 60, 90),
        
        margin: list[int, int] = [10,0],
        inner_margin: list[int, int] = [2,2],
        anchor_mode: AnchorMode = AnchorMode.DEFAULT # NOT YET IMPLEMENTED
        ):
        
        self.size = size
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.color_4 = color_4
        self.margin = margin
        self.inner_margin = inner_margin
        self.anchor_mode = anchor_mode
    
    def hovered(self) -> bool:
        return (self.relative_mouse_pos[0] >= 0 and self.relative_mouse_pos[0] <= self.size[0]) and\
    (self.relative_mouse_pos[1] >= 0 and self.relative_mouse_pos[1] <= self.size[1])
    
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
        ...
        
    @property
    def surface(self) -> pg.Surface:
        return self._render()