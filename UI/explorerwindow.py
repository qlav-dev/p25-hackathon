import pygame as pg
from UI.window import Window
from UI.text import Text
from UI.element import Element
from UI.button import Button
from UI.columns import Columns, Column
from UI.spacer import Spacer
from UI.textinput import TextInput
import os

from copy import copy

class ExplorerWindow(Window):
    """
        An UI window prompt to get file input
        Works without tkinter.
    """

    def load_explorer(self, path):
        """
        Updates explorer to scrollbox element at path path 
        """
        walk = os.walk(path).__next__()
        files = walk[2]
        folders = walk[1]

        print(path)
        
        self.explorer = ScrollBox(
                elements = [
                    Columns(columns = 
                    [
                        Column(elements=
                            [
                                Button(folder.removeprefix(walk[0]), size = [200, 15], force_size=True, pressed = lambda: self.load_explorer(folder)) for folder in folders
                            ] +
                            [
                                Text(file.removeprefix(walk[0])) for file in files
                            ]),
                        Column(elements=
                            [
                                Text("Folder") for _ in folders
                            ] + 
                            [
                                Text("File") for _ in files
                            ])
                    ]
                    )
                ]
            )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, caption = "Select a file", **kwargs)

        self.current_address = os.path.abspath(os.getcwd())
        
        self.explorer = None
        self.load_explorer(os.getcwd())

        self.elements = [
            Columns(columns = 
                [
                    Column(elements=[TextInput(text=self.current_address, size = (400, 25))]), Column(elements=[Button("go to address"), Button("Go to parent")])
                ]
            ),
            Spacer(height = 10),
            self.explorer,
            Spacer(height = 5),
            Columns(columns = 
                [
                    Column(elements = [Button("Close")]), Column(elements = [Spacer(width = 100, height=0)]), Column(elements = [Button("Load file")])
                ]
            )
        ]

        self.propagate_colors()
        self.auto_resize()
        