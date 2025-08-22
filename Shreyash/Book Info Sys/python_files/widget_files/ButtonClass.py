import tkinter as tk
class MyButton(tk.Button):
    def __init__(self, master, **kwargs):
        kwargs.setdefault("font", ("Arial", 10)) 
        super().__init__(master, **kwargs)