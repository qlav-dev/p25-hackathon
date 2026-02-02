import pygame as pg
from game import Sprite
import UI

def main():
    
    img_preview_size = (100, 100)

    ui_windows = []

    screen_size = (1200, 700)
    screen = pg.display.set_mode(size = screen_size, flags = pg.RESIZABLE)
    pg.display.set_caption("Slimes With Guns: Level Editor")
    
    """ -- UI DEFINITION -- """ 

    selected_spritesheet_image_preview = UI.Image("sprites/placeholder_texture.png", size = img_preview_size)
    ressources_select_window = UI.Window("Ressources")

    def select_spritesheet_dialog(file):
        # Opens a dialog without TK 
        selected_spritesheet_image_preview.path = file

    ressources_select_window.elements = [
        UI.Text("Current level spritesheet"),
        selected_spritesheet_image_preview,
        UI.Button("Load spritesheet", on_click = lambda: ui_windows.append(UI.ExplorerWindow(on_finished= select_spritesheet_dialog, position = [screen_size[0] / 2, screen_size[1] / 2]))),
    ]

    object_editor_window = UI.Window("Object editor", position = [0, 300])
    object_editor_window.elements = [
        UI.Text("Placeholder")
    ]

    level_settings_window = UI.Window("Level settings", position = [0, 600])
    level_settings_window.elements = [
        UI.Text("Placeholder")
    ]

    ui_windows += [ressources_select_window, object_editor_window, level_settings_window]

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

            if w._closed: # Closes the windows
                ui_windows.remove(w)

        pg.display.flip()
        

if __name__ == "__main__":
    main()