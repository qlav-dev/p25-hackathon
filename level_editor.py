import pygame as pg
from game import Sprite
import UI

def main():
    
    img_preview_size = (100, 100)

    ui_windows = []

    screen_size = (1200, 700)
    screen = pg.display.set_mode(size = screen_size, flags = pg.RESIZABLE)
    pg.display.set_caption("Slimes With Guns: Level Editor")

    selected_spritesheet_image_path = "sprites/placeholder_texture.png"
    def select_spritesheet_dialog():
        # Opens a dialog without TK 
        selected_spritesheet_image_path = UI.ExplorerWindow()
        ui_windows.append(UI.ExplorerWindow())
    
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

    ui_windows = [ressources_select_window, object_editor_window, level_settings_window,  UI.ExplorerWindow()]

    for w in ui_windows:
        w.propagate_colors()
        w.auto_resize()

    """ -- Editor Environnmenet Definition --- """

    running = True
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False

        screen.fill(pg.color.Color(100, 100, 100))

        # UI update
        for w in ui_windows:
            w.update(pg.mouse.get_pressed(3)[0])
            screen.blit(w.get_surface(),  w.position)

        ressources_select_window.elements[1].path = selected_spritesheet_image_path

        pg.display.flip()
        

if __name__ == "__main__":
    main()