import tkinter as tk
class MyEntry(tk.Entry):
    def __init__(self, master, **kwargs):
        kwargs.setdefault("font", ("Arial", 10))
        super().__init__(master, **kwargs)
