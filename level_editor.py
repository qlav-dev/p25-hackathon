import pygame as pg
from game import Sprite
import UI

from tkinter import messagebox
import subprocess

def main():
    
    img_preview_size = (100, 100)

    screen_size = (1200, 700)
    screen = pg.display.set_mode(size = screen_size, flags = pg.RESIZABLE)
    pg.display.set_caption("Slimes With Guns: Level Editor")

    selected_spritesheet_image_path = "sprites/placeholder_texture.png"
    def select_spritesheet_dialog():
        # Opens a dialog without TK 
        selected_spritesheet_image_path = subprocess.check_output(["osascript", "-e",'POSIX path of (choose file with prompt "Choose a file")']).decode().strip()
    
    """ -- UI DEFINITION -- """ 

    ressources_select_window = UI.Window("Ressources")
    ressources_select_window.elements = [
        UI.Text("Current level spritesheet"),
        UI.Image(selected_spritesheet_image_path, size = img_preview_size),
        UI.Button("Load spritesheet", on_click = select_spritesheet_dialog),
    ]

    object_editor_window = UI.Window("Object editor", position = [0, 300])
    object_editor_window.elements = [
        UI.Text("Placeholder")
    ]

    level_settings_window = UI.Window("Level settings", position = [0, 600])
    level_settings_window.elements = [
        UI.Text("Placeholder")
    ]

    ressources_select_window.auto_resize()
    ressources_select_window.propagate_colors()

    object_editor_window.auto_resize()
    object_editor_window.propagate_colors()

    level_settings_window.auto_resize()
    level_settings_window.propagate_colors()
    
    """ -- Editor Environnmenet Definition --- """

    running = True
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False

        screen.fill(pg.color.Color(100, 100, 100))

        # UI update
        ressources_select_window.update(pg.mouse.get_pressed(3)[0])
        level_settings_window.update(pg.mouse.get_pressed(3)[0])
        object_editor_window.update(pg.mouse.get_pressed(3)[0])

        ressources_select_window.elements[1].path = selected_spritesheet_image_path

        screen.blit(ressources_select_window.get_surface(),  ressources_select_window.position)
        screen.blit(level_settings_window.get_surface(),  level_settings_window.position)
        screen.blit(object_editor_window.get_surface(),  object_editor_window.position)

        pg.display.flip()
        

if __name__ == "__main__":
    main()