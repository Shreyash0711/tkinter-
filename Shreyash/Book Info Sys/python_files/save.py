import tkinter as tk
from tkinter import ttk, messagebox
from python_files.widget_files.ButtonClass import MyButton
from python_files.widget_files.LabelClass import MyLabel
from python_files.widget_files.EntryClass import MyEntry
from python_files.widget_files.logger import Log
from datetime import datetime
import json
import os

class Save_tab(ttk.Frame):
    def __init__(self, parent, logger: Log):
        super().__init__(parent)

        self.logger = logger
        self.logger.info_logger("Save tab started")
        

        MyLabel(self, "Book ID:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        MyLabel(self, "Book Name:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        MyLabel(self, "Author:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        MyLabel(self, "Price:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        MyLabel(self, "Publish Year:").grid(row=4, column=0, padx=10, pady=5, sticky="e")

        self.book_id = MyEntry(self)
        self.book_id.grid(row=0, column=1, padx=10, pady=5)

        self.book_name = MyEntry(self)
        self.book_name.grid(row=1, column=1, padx=10, pady=5)

        self.author = MyEntry(self)
        self.author.grid(row=2, column=1, padx=10, pady=5)

        self.price = MyEntry(self)
        self.price.grid(row=3, column=1, padx=10, pady=5)

        self.publish_year = MyEntry(self)
        self.publish_year.grid(row=4, column=1, padx=10, pady=5)

        MyButton(self, text="SAVE", command=self.save_book).grid(row=5, column=0, padx=10, pady=5)
        MyButton(self, text="CLEAR", command=self.clear_fields).grid(row=5, column=1, padx=10, pady=5)


    def clear_fields(self):
        self.logger.info_logger("Cleared all feilds")
        for entry in [self.book_id, self.book_name, self.author,self.price, self.publish_year]:
            entry.delete(0, tk.END)

    def save_book(self):
        
        book_id = self.book_id.get().strip()
        book_name = self.book_name.get().strip()
        book_author = self.author.get().strip()
        book_price = self.price.get().strip()
        book_year = self.publish_year.get().strip()

        # Validation
        if not book_id or not book_name or not book_author or not book_price or not book_year:
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

        data_dir = "data"
        os.makedirs(data_dir, exist_ok=True)

        filename = os.path.join(data_dir, "db.json")

        if os.path.exists(filename):
            with open(filename, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        # Check duplicates
        for book in data:
            if book.get("id") == book_id:
                self.logger.info_logger(f"Book Id {book_id} already exists")
                messagebox.showerror("Error", "Book ID already exists")
                return
            if book.get("name", "").lower() == book_name.lower():
                self.logger.info_logger(f"Book Name {book_name} already exists")
                messagebox.showerror("Error", "Book Name already exists")
                return
        
        self.logger.info_logger(f"Data saved for Book Id: {book_id}")
        data.append({
            "id": book_id,
            "name": book_name,
            "author": book_author,
            "price": book_price,
            "year": book_year
        })

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        messagebox.showinfo("Success", "Book saved successfully")
        self.logger.info_logger("Book Data Saved")

       

        self.clear_fields()
