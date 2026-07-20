import tkinter as tk
from tkinter import *
from tkinter import ttk

root = tk.Tk()
root.title("Chat Box")

#widgets = [
    #tk.Label,
    #ttk.Combobox,
    #tk.Entry, 
    #tk.Button,
#]

def get_list():
    send = 'list'
    print(send)

button2 = tk.Button(
    root,
    text="Get List",
    command=get_list,
)
button2.pack(padx=5, pady=5)

combobox = ttk.Combobox(root, values=[1, 2, 3, 4, 5])
combobox.set("")
combobox.pack(padx=5, pady=5, fill="x")

entry = tk.Entry(root)
entry.pack(padx=5, pady=5, fill="x")

def erase(event=None):
    if entry.get() == 'Type here...':
        entry.delete(0,'end')
def add(event=None):
    if entry.get() == '':
        entry.insert(0, 'Type here...')

add()
entry.bind("<FocusIn>", erase)
entry.bind("<FocusOut>", add)

def send():
    send = combobox.get() + ": " + entry.get()
    print(send)
button = tk.Button(
    root,
    text="Send",
    command=send,
)
button.pack(padx=5, pady=5)


#for widget in widgets:
    #try:
        #widget = widget(root, text=widget.__name__)
    #except tk.TclError:
        #widget = widget(root)
    #widget.pack(padx=5, pady=5, fill="x")

root.mainloop()

