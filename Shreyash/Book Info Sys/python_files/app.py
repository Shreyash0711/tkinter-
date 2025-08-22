from python_files.widget_files.logger import Log
from python_files.save import Save_tab
from python_files.search import Search_tab
from python_files.excel import Excel_tab
from python_files.xml import Xml_tab
from python_files.read import Read_tab
import tkinter as tk
from tkinter import ttk
import os

class App(tk.Tk):
    def __init__(self, logger : Log):
        super().__init__()
        self.logger = logger
        self.title("Book Info")
        self.geometry("420x400")
        self.resizable(False, False)

        notebook = ttk.Notebook()
        notebook.pack(fill="both", expand=True)

        # Create tabs
        self.save_tab = Save_tab(notebook, self.logger)
        self.search_tab = Search_tab(notebook, self.logger)
        self.export_tab = Excel_tab(notebook, self.logger)
        self.xml_tab = Xml_tab(notebook, self.logger)
        self.read_tab = Read_tab(notebook, self.logger)

  
        # add to notebook
        notebook.add(self.save_tab, text="Save")
        notebook.add(self.search_tab, text="Search")
        notebook.add(self.export_tab, text="Export Excel")
        notebook.add(self.xml_tab, text="Export XML")
        notebook.add(self.read_tab, text="Read")

if __name__ == "__main__":
    log_file : str = os.path.join(os.path.dirname(__file__), "log.txt")
    logger = Log(log_file)  
    root = App(logger)
    root.mainloop()
