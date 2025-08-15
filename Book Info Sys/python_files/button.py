import tkinter as tk
class ButtonClass:
    def __init__(self, master, text, row, col, command, padx=5, pady=5):
        self.button = tk.Button(master, text=text, font=("Arial", 12), bg="lightblue", command=command)
        self.button.grid(row=row, column=col, padx=padx, pady=pady, sticky="ew")
