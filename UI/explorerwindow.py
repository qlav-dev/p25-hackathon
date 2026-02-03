from __future__ import annotations

import pygame as pg
from UI.window import Window
from UI.text import Text
from UI.element import Element
from UI.button import Button
from UI.columns import Row, Column
from UI.spacer import Spacer
from UI.textinput import TextInput
from UI.scrollbox import ScrollBox
from UI.image import Image
import os


from copy import copy

_COMPATIBLE_IMAGE_TYPES = ("BMP","GIF","JPEG","JPG","LBM", "PBM", "PGM", "PPM","PCX","PNG","PNM","SVG","TGA","XPM","TIFF","WEBP",)

class Explorer(Column):
    
    def select_file(self, path):
        extension = os.path.splitext(path)[1][1:]

        if extension.upper() in _COMPATIBLE_IMAGE_TYPES:
            self.preview_image.path = path
        else:
            self.preview_image.path = os.path.join(os.path.dirname(__file__), "ressources", "placeholder.png")

        self.selected_file = path

    def load_explorer(self, path):
        """
        Updates explorer to scrollbox element at path path 
        """
        walk = os.walk(path).__next__()
        folders = walk[1]
        files = walk[2]

        self.current_address = path
        self.address_input.text = self.current_address
        self.go_to_parent_button.on_click = lambda: self.load_explorer(os.path.normpath(os.path.join(self.current_address, os.pardir)))

        self.explorer.elements = [
                    Row(elements = 
                    [
                        Button(folder.removeprefix(walk[0]), size = [200, 17], force_size=True, on_release = lambda f = os.path.join(walk[0], folder): self.load_explorer(f)),
                        Text("Folder")

                    ]) for folder in folders
                ] + [
                    Row(elements = 
                    [
                        Button(file.removeprefix(walk[0]), size = [200, 17], force_size=True, on_click = lambda f = os.path.join(walk[0], file): self.select_file(f)),
                        Text("file")
                    ]
                    ) for file in files
                ]

        self.explorer.scroll_position = 0
        self.explorer.propagate_colors()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.current_address = os.path.abspath(os.getcwd())

        self.selected_file = None
        
        self.explorer = ScrollBox(elements=[])
        self.address_input = TextInput(text=self.current_address, size = (400, 25))
        self.go_to_parent_button = Button("Go to parent")
        self.load_explorer(os.getcwd())
        self.preview_image = Image(os.path.join(os.path.dirname(__file__), "ressources", "placeholder.png"), size = (100, 100))

        self.elements = [
            Row(elements = 
                [
                    Column(elements=[Spacer(height = 5), self.address_input]), Column(elements=[Button("go to address", on_click = lambda: self.load_explorer(self.address_input.text)), self.go_to_parent_button])
                ]
            ),
            Spacer(height = 10),
            Row(elements = 
                [
                    Column(elements=[self.explorer]), Column(elements=[Text("File preview"), self.preview_image])
                ]
            ),
            Spacer(height = 5),
        ]

        self.propagate_colors()

class ExplorerWindow(Window):
    """
        An UI window prompt to get file input
        Works without tkinter.

        When file is selected, calls on_finished(file)
    """

    def finished(self):
        self._on_finished(self.elements[0].selected_file)
        self._closed = True
    
    def __init__(self, *args, on_finished: function = lambda: ..., **kwargs):
        """
        When file is selected, calls on_finished(file)
        """
        super().__init__(*args, caption = "Select a file", closable = True, **kwargs)
        self._on_finished = on_finished

        self.elements = [Explorer(), Button("Load file", on_click = self.finished)]

        self.propagate_colors()
        self.auto_resize()
        