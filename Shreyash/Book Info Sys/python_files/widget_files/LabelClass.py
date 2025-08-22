import tkinter as tk

class MyLabel(tk.Label):
    def __init__(self, master, text):
        super().__init__(master, text=text, font=("Arial", 10))
