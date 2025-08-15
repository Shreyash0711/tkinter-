import tkinter as tk
from tkinter import ttk, messagebox
from python_files.button import ButtonClass
import datetime
import json
import os
class Save_tab(ttk.Frame):
    def __init__(self, parent, export_tab):
        super().__init__(parent)
        self.export_tab = export_tab

        # Labels & Entries
        tk.Label(self, text="Book ID :").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.book_id_entry = tk.Entry(self, width=20)
        self.book_id_entry.grid(row=0, column=1)

        tk.Label(self, text="Book Name :").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.book_name_entry = tk.Entry(self, width=20)
        self.book_name_entry.grid(row=1, column=1)

        tk.Label(self, text="Price :").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.book_price_entry = tk.Entry(self, width=20)
        self.book_price_entry.grid(row=2, column=1)

        tk.Label(self, text="Publish Year :").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.book_year_entry = tk.Entry(self, width=20)
        self.book_year_entry.grid(row=3, column=1)

        ButtonClass(self, text="Save", row=4, col=1, command=self.save_book)
        
        

    def save_book(self):
        book_id = self.book_id_entry.get().strip()
        book_name = self.book_name_entry.get().strip()
        book_price = self.book_price_entry.get().strip()
        book_year = self.book_year_entry.get().strip()

        # Validation
        if not book_id or not book_name or not book_price or not book_year:
            messagebox.showwarning("ERROR", "Fill all fields")
            return

        try:
            book_id = int(book_id)
        except ValueError:
            messagebox.showerror("ValueError", "Book ID should be integer")
            return

        try:
            book_price = float(book_price)
        except ValueError:
            messagebox.showerror("ValueError", "Book Price should be Integer/Float")
            return

        try:
            book_year = int(book_year)
            current_yr = datetime.now().year
            if book_year > current_yr:
                messagebox.showwarning("ValueError", f"Publish year should be ≤ {current_yr}")
                return
        except ValueError:
            messagebox.showerror("ValueError", "Book Year should be integer")
            return

        filename = "db.json"

        # Load existing data
        if os.path.exists(filename):
            with open(filename, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        # Check for duplicates
        for book in data:
            if book["id"] == book_id:
                messagebox.showerror("Error", "Book ID already exists")
                return
            if book["name"].lower() == book_name.lower():
                messagebox.showerror("Error", "Book Name already exists")
                return

        # Append new book
        data.append({
            "id": book_id,
            "name": book_name,
            "price": book_price,
            "year": book_year
        })

        # Save to file
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        messagebox.showinfo("Success", "Book saved successfully")

        # Refresh export tab after saving
        if self.export_tab:
            self.export_tab.load_data()

        # Clear fields
        self.book_id_entry.delete(0, tk.END)
        self.book_name_entry.delete(0, tk.END)
        self.book_price_entry.delete(0, tk.END)
        self.book_year_entry.delete(0, tk.END)
