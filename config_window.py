import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
import random

from redis import Redis # For the ping
from redis.exceptions import ConnectionError

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
    load_path = tk.StringVar()

    lbl = tk.Label(configWindow, width = 20, text=f"Username :")
    lbl.grid(row=1, column=0)
    username = tk.Entry(configWindow, width = 20, textvariable=tk.StringVar(value=f"MyUsername{random.randint(1,99)}"))
    username.grid(row=1, column=1)

    lbl = tk.Label(configWindow, width = 20, text=f"Hostname :")
    lbl.grid(row=1, column=3)
    hostname = tk.Entry(configWindow, width = 20, textvariable=tk.StringVar(value=f"192.168.153.213"))
    hostname.grid(row=1, column=4)

    lbl = tk.Label(configWindow, width = 20, text=f"Port :")
    lbl.grid(row=2, column=3)
    port = tk.Entry(configWindow, width = 20, textvariable=tk.StringVar(value=f"6379"))
    port.grid(row=2, column=4)

    separator = ttk.Separator(configWindow, orient='vertical')
    separator.grid(row=0, column=2, ipady=30, ipadx = 0, rowspan=5, padx = 20)

    def startgame():
        #config.append(save_path.get())

        configWindow.destroy() # Quits the window
    
    def ping_server():
        r = Redis(host = hostname.get(), port = port.get()) # short timeout for the test

        try:
            r.ping()
            simpledialog.messagebox.showinfo("Ping result:", "Connected successfully !")
        except ConnectionError:
            simpledialog.messagebox.showinfo("Ping result:", "Error ! Could not connect")

    startgame = tk.Button(configWindow, text = "Start Game", command = startgame)
    startgame.grid(row=3, column=1)

    check_server = tk.Button(configWindow, text = "Ping Server", command = ping_server)
    check_server.grid(row = 3, column = 4)
    
    configWindow.mainloop()

    return {"Username" : username.get(), "Hostname" : hostname.get(), "Port": port.get()}

configWindow()