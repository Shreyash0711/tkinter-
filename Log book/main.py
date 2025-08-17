import tkinter as tk
from tkinter import ttk
from python_files.storage import Storage
from python_files.ui_add_entry import AddEntryFrame
from python_files.ui_view_entry import ViewEntriesFrame

class WorkLogApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Work Log Diary")
        self.geometry("700x600")

        # Storage instance
        self.storage = Storage()

        # Tabs
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both")

        add_tab = AddEntryFrame(notebook, self.storage)
        view_tab = ViewEntriesFrame(notebook, self.storage)

        notebook.add(add_tab, text="➕ Add Entry")
        notebook.add(view_tab, text="📖 View Entries")

if __name__ == "__main__":
    app = WorkLogApp()
    app.mainloop()
