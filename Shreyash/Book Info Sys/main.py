import os
from python_files.app import App
from python_files.widget_files.logger import Log
import tkinter as tk

if __name__ == "__main__":
    log_file : str = os.path.join(os.path.dirname(__file__), "log.txt")
    logger = Log(log_file)  
    root = App(logger)
    root.mainloop()
