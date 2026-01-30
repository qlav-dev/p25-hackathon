import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import random

def configWindow() -> list[str]:
    """
        Configuration Window.
    """

    configWindow = tk.Tk()
    configWindow.title("Slimes with Guns : Config Window")
    configWindow.geometry()
    configWindow.resizable(False, False)

    global config_inputs
    global config

    global load_path
    global load_path_lbl

    config = [] # The configuration of the window
    config_inputs = []
    load_path = tk.StringVar()

    lbl = tk.Label(configWindow, width = 20, text=f"Username :")
    lbl.grid(row=1, column=0)
    config_inputs.append(tk.Entry(configWindow, width = 20, textvariable=tk.StringVar(value=f"MyUsername{random.randint(1,99)}")))
    config_inputs[-1].grid(row=1, column=1)

    lbl = tk.Label(configWindow, width = 20, text=f"Hostname :")
    lbl.grid(row=1, column=3)
    config_inputs.append(tk.Entry(configWindow, width = 20, textvariable=tk.StringVar(value=f"localhost")))
    config_inputs[-1].grid(row=1, column=4)

    lbl = tk.Label(configWindow, width = 20, text=f"Port :")
    lbl.grid(row=2, column=3)
    config_inputs.append(tk.Entry(configWindow, width = 20, textvariable=tk.StringVar(value=f"6379")))
    config_inputs[-1].grid(row=2, column=4)

    separator = ttk.Separator(configWindow, orient='vertical')
    separator.grid(row=0, column=2, ipady=30, ipadx = 0, rowspan=5, padx = 20)

    def createNew():
        global config
        global config_inputs

        config = [int(i.get()) for i in config_inputs]
        #config.append(save_path.get())

        configWindow.destroy() # Quits the window
    

    createNew = tk.Button(configWindow, text = "Load Game", command = createNew)
    createNew.grid(row=3, column=1)
    
    configWindow.mainloop()

    return config

configWindow()