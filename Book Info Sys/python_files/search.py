import tkinter as tk
from tkinter import ttk,messagebox
from python_files.button import ButtonClass
import json
import os
class Search_tab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Label(self, text="Search by:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.search_type = ttk.Combobox(self, values=["ID", "Name"], state="readonly", width=5)
        self.search_type.grid(row=0, column=1)
        self.search_type.current(0)

        tk.Label(self, text="Value:").grid(row=0, column=2, padx=5, pady=5)
        self.search_entry = tk.Entry(self, width=15)
        self.search_entry.grid(row=0, column=3)

        ButtonClass(self, text="Search", row=1, col=3, command=self.search)

        self.result_box = tk.Text(self, width=45, height=8, state="disabled")
        self.result_box.grid(row=2, column=0, columnspan=4, padx=5, pady=5)

    def search(self):
        search_mode = self.search_type.get()
        query = self.search_entry.get().strip()

        if not query:
            messagebox.showwarning("Warning", "Enter value to search")
            return

        filename = "db.json"
        if not os.path.exists(filename):
            messagebox.showerror("Error", "Database file not found")
            return

        with open(filename, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Database file is corrupted")
                return

        results = []
        for book in data:
            if search_mode == "ID":
                if query in str(book["id"]):
                    results.append(book)
            elif search_mode == "Name":
                if query.lower() in book["name"].lower():
                    results.append(book)

        self.result_box.config(state="normal")
        self.result_box.delete(1.0, tk.END)
        if results:
            for b in results:
                self.result_box.insert(
                    tk.END,
                    f"ID: {b['id']}\nName: {b['name']}\nPrice: {b['price']}\nYear: {b['year']}\n{'-'*30}\n"
                )
        else:
            self.result_box.insert(tk.END, "No matching books found.")
        self.result_box.config(state="disabled")

