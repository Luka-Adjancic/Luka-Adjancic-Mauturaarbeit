import tkinter as tk
from tkinter import *
from tkinter import ttk

root = tk.Tk()
root.title("Widgets Demo")

widgets = [
    tk.Label,
    tk.Checkbutton,
    ttk.Combobox,
    tk.Entry,
    tk.Button,
    tk.Radiobutton,
    tk.Scale,
    tk.Spinbox,
]

for widget in widgets:
    try:
        widget = widget(root, text=widget.__name__)
    except tk.TclError:
        widget = widget(root)
    widget.pack(padx=5, pady=5, fill="x")

root.mainloop()

#window = tk.Tk()
#window.title("Hello World")

#def handle_button_press(event):
    #window.destroy()

#button = tk.Button(text="My simple app.")
#button.bind("", handle_button_press)
#button.pack()

# Start the event loop.
#window.mainloop()