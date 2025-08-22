import tkinter as tk
from tkinter import ttk, messagebox
from python_files.widget_files.ButtonClass import MyButton
from python_files.widget_files.LabelClass import MyLabel
from python_files.widget_files.EntryClass import MyEntry

import json
import os

class Search_tab(ttk.Frame):
    def __init__(self, parent, logger):
        super().__init__(parent)

        self.logger = logger
        self.logger.info_logger("Search tab started")

        MyLabel(self, "Search by:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        MyLabel(self, "Value:").grid(row=0, column=2, padx=10, pady=5, sticky="e")

        self.search_type = ttk.Combobox(self, values=["ID", "Name"], state="readonly", width=5)
        self.search_type.current(0)
        self.search_type.grid(row=0, column=1, padx=10, pady=5)

        self.search_entry = MyEntry(self)
        self.search_entry.grid(row=0, column=3, padx=10, pady=5)

        MyButton(self, text="Search", command=self.search).grid(row=1, column=0, columnspan=4, pady=5)
        

        self.result_box = tk.Text(self, width=45, height=8, state="disabled")
        self.result_box.grid(row=2, column=0, columnspan=4, padx=5, pady=5)

    def search(self):

        search_mode = self.search_type.get()
        query = self.search_entry.get().strip()

        if not query:
            messagebox.showwarning("Warning", "Enter value to search")
            return

        if search_mode == "ID" and not query.isdigit():
            messagebox.showwarning("Warning", "ID should be a numeric value")
            return

        filename = os.path.join("data", "db.json")
        if not os.path.exists(filename):
            messagebox.showerror("Error", "Database file not found")
            return

        with open(filename, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Database file is corrupted")
                return

        self.logger.info_logger(f"Searching for '{query}' by {search_mode}")

        results = []
        for book in data:
            if search_mode == "ID":
                if query == str(book.get("id", "")):
                    results.append(book)
            elif search_mode == "Name":
                if query.lower() in book.get("name", "").lower():
                    results.append(book)

        self.result_box.config(state="normal")
        self.result_box.delete(1.0, tk.END)
        if results:
            for b in results:
                self.result_box.insert(
                    tk.END,
                    f"ID: {b.get('id')}\nName: {b.get('name')}\nPrice: {b.get('price')}\nYear: {b.get('year')}\n{'-'*30}\n"
                )
        else:
            self.result_box.insert(tk.END, "No matching books found.")
        self.result_box.config(state="disabled")

        