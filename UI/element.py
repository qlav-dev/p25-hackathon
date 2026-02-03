import pygame as pg
from pygame.color import Color
from UI.anchors import AnchorMode

class Element:
    """
    Every inside-window objects is an `Element` object. 
    An class inheriting from element must implement:
    * _render(self) -> Surface, that renders the element into a pygame surface (Local coordinates). It MUST update its size
    * update(self, *...) -> None, that updates the element. 

    The label and id are identifier to the object. 
    By default, label = str(elem) and id = hash(label).
    """
    
    relative_mouse_pos: tuple[int, int] = [0,0] # Modified by the window or the encapsulating element !
    force_size = False

    def find_by_label(self, label: str):
        if self.label == label:
            return self

        if not hasattr(self, "elements"):
            return None # No childrens
        
        # Returns the first element with label.
        for e in self.elements:
            f = e.find_by_label(label)
            if f is not None:
                return f
        return None

    def find_by_id(self, id: int):
        if self.id == id:
            return self

        if not hasattr(self, "elements"):
            return None # No childrens
        
        # Returns the first element with label.
        for e in self.elements:
            f = e.find_by_id(id)
            if f is not None:
                return f
        return None

    def __init__(self,
        colors : list[Color] = None,
        margin: list[int, int] = None,
        #inner_margin: list[int, int] = None,
        anchor_mode: AnchorMode = AnchorMode.DEFAULT, # NOT YET IMPLEMENTED
        force_size: bool = False,
        size: list[int, int] = None,
        id: int = None,
        label: str = None,
        ):
        """  
            force_size: Allows to set a size on creation. The size is set in the argument size, and will not be changed automatically.
            If force_size is false, then the size of the element is calculated dynamically.

            Moreover, some elements need the size arguement to be set. If so, it is written explicitly in the docstring.
        """

        self.force_size = force_size

        self.label = label if label is not None else self.__repr__()
        self.id = id if id is not None else hash(self.label)
        
        self.margin = margin if margin is not None else [5, 0]
        #self.inner_margin = inner_margin if inner_margin is not None else [2,2]

        self.size = size if size is not None else [1, 1]
        self.colors = colors if colors is not None else [Color(50, 50, 50, 90), Color(20, 20, 100, 90), Color(196, 196, 196, 90), Color(247, 40, 60, 90)]

        self.anchor_mode = anchor_mode
    
    def hovered(self) -> bool:
        return pg.rect.Rect(*self.margin, self.size[0] - 2 * self.margin[0], self.size[1] - 2 * self.margin[1]).collidepoint(self.relative_mouse_pos)

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
        # The element MUST render with the margins. I.E, if the margins are margin, self.size = (margin[0] * 2 + x, margin[1] * 2 + x), and the elements blit at (margin[0], margin[1])
        
    def update(self, events: list[pg.event.Event]):
        """
        Must update the elements, as well as its children elements, and update their relative_mouse_pos
        """
        ...
        
    @property
    def surface(self) -> pg.Surface:
        """ 
        Calling this updates self.size 
        """ 
        return self._render()