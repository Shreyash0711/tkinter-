import tkinter as tk
from tkinter import ttk
from python_files.save import Save_tab
from python_files.export import Export_tab
from python_files.search import Search_tab



class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Book Info")
        self.geometry("420x400")
        self.resizable(False, False)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        export_tab = Export_tab(notebook)
        notebook.add(Save_tab(notebook, export_tab), text="Save")
        notebook.add(Search_tab(notebook), text="Search")
        notebook.add(export_tab, text="Export")


