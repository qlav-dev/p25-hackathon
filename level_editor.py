import pygame as pg
from game import Sprite
import UI
import level_editor
from numpy import exp

def main():
    
    img_preview_size = (200, 200)

    ui_windows = []

    screen_size = (1200, 700)
    screen = pg.display.set_mode(size = screen_size, flags = pg.RESIZABLE)
    pg.display.set_caption("Slimes With Guns: Level Editor")

    selected_spritesheet_image_preview = UI.Image("sprites/placeholder_texture.png", size = img_preview_size)

    """ -- Level Definition --- """

    level = level_editor.Level(spritesheet = level_editor.SpriteSheet(selected_spritesheet_image_preview._image, cell_size = 16), map_size = (16, 10))
    editor = level_editor.Editor(level)
    
    """ -- UI DEFINITION -- """ 

    ressources_select_window = UI.Window("Ressources")

    def select_spritesheet_dialog(file):
        # Opens a dialog without TK 
        selected_spritesheet_image_preview.path = file
    
    def load_map_dialog(file):
        ...

    def save_map_dialog(file):
        ...

    ressources_select_window.elements = [
        UI.Row(elements = [UI.Button("Load Map", on_click = lambda: ui_windows.append(UI.ExplorerWindow(on_finished= load_map_dialog, position = [screen_size[0] / 2, screen_size[1] / 2]))), 
            UI.Button("Save Map", on_click = lambda: ui_windows.append(UI.ExplorerWindow(on_finished= save_map_dialog, position = [screen_size[0] / 2, screen_size[1] / 2]))),]),
        UI.Text("Current level spritesheet"),
        selected_spritesheet_image_preview,
        UI.Button("Load spritesheet", on_click = lambda: ui_windows.append(UI.ExplorerWindow(on_finished= select_spritesheet_dialog, position = [screen_size[0] / 2, screen_size[1] / 2]))),
        UI.Row(elements=
        [UI.Text("Cell Size:"), UI.TextInput(place_holder=("CellSize"), size = (100, 15), input_type = int)])
    ]

    object_editor_window = UI.Window("Object editor", position = [0, 300])
    object_editor_window.elements = [
        UI.Row(elements = 
            [UI.Column(elements= [UI.Text("Cell X"), UI.Text("Cell Y")]), UI.Column(elements= [UI.TextInput("x", "0", size = (50, 15)), UI.TextInput("y", "0", size = (50, 15))])]
        ),
        UI.Text("Selected sprite:"),
        UI.Image("sprites/placeholder_texture.png", size = (50, 50)) # TEMPORARY
    ]

    level_settings_window = UI.Window("Level settings", position = [0, 600])
    level_settings_window.elements = [
        UI.Row(elements=
        [
        UI.Column(elements= [
            UI.Text("Map width (in cells):"), 
            UI.Text("Map height (in cells):"),
            UI.Spacer(),
            UI.Text("Background color (RGB)")]), 
        UI.Column(elements= [
            UI.TextInput(place_holder=("width") , text = f"{editor.level.map_size[0]}", input_type = int, size = (100, 15), label = "map_width"), 
            UI.TextInput(place_holder=("height"), text = f"{editor.level.map_size[1]}", input_type = int, size = (100, 15), label = "map_height"),
            UI.Spacer(),
            UI.Row(elements= [
                UI.TextInput("r", f"{editor.level.background_color.r}", size = (20, 15), margin = [5, 0], label = "r_background", input_type = int), 
                UI.TextInput("g", f"{editor.level.background_color.g}", size = (20, 15), margin = [5, 0], label = "g_background", input_type = int), 
                UI.TextInput("b", f"{editor.level.background_color.b}", size = (20, 15), margin = [5, 0], label = "b_background", input_type = int)])])]),
        UI.Button("Update level settings", label = "update_level_settings_button")
    ]

    ui_windows += [ressources_select_window, object_editor_window, level_settings_window]

    for w in ui_windows:
        w.propagate_colors()
        w.auto_resize()

    """ -- Editor Environnmenet Definition --- """

    running = True
    while running:
        events = []

        # INPUT
        mouse_buttons = pg.mouse.get_pressed(3)
        mouse_pos = pg.mouse.get_pos()

        for e in pg.event.get():
            events.append(e)

            keyboard_mods = pg.key.get_mods()

            if e.type == pg.MOUSEBUTTONDOWN:
                mouse_press_position = mouse_pos
                editor_position_at_mouse_press = editor.position.copy()

            if e.type == pg.MOUSEWHEEL:
                if keyboard_mods & pg.KMOD_SHIFT: # ZOOM
                    editor.zoom += e.y * .05 - e.x * .05
                    continue

                editor.position[0] += e.x
                editor.position[1] += e.y

            if e.type == pg.QUIT:
                running = False

        if mouse_buttons[1]:
            editor.position[0] = mouse_pos[0] - mouse_press_position[0] + editor_position_at_mouse_press[0]
            editor.position[1] = mouse_pos[1] - mouse_press_position[1] + editor_position_at_mouse_press[1]

        screen.fill(pg.color.Color(200, 200, 200))

        # Editor update

        if (level_settings_window.get_element_by_label("update_level_settings_button").clicked):
            
            editor.level.map_size = (
                int(level_settings_window.get_element_by_label("map_width").text),
                int(level_settings_window.get_element_by_label("map_height").text),
            )

            editor.level.background_color = pg.color.Color(
                int(level_settings_window.get_element_by_label("r_background").text),
                int(level_settings_window.get_element_by_label("g_background").text),
                int(level_settings_window.get_element_by_label("b_background").text),
            )

        editor_surf = editor.render()
        editor_surf_transformed = pg.transform.scale_by(editor_surf, exp(editor.zoom))
        screen.blit(editor_surf_transformed, editor.position)

        # UI update
        windows_to_remove = []
        for w in ui_windows:
            w.update(pg.mouse.get_pressed(3)[0], events)
            screen.blit(w.get_surface(), w.position)
            
            if w._closed:
                windows_to_remove.append(w)

        for w in windows_to_remove:
            ui_windows.remove(w)

        pg.display.flip()
        

if __name__ == "__main__":
    main()