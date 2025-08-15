import tkinter as tk
from tkinter import messagebox,ttk,filedialog
import openpyxl
import json
import os
import platform
import subprocess
import shutil

class Export_tab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        columns = ("ID", "Name", "Price", "Year")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=6)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80)
        self.tree.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

        tk.Button(self, text="Export to Excel", bg="lightblue", command=self.export_to_excel).grid(row=1, column=0, pady=5)
        tk.Button(self, text="Download Excel", bg="lightblue", command=self.download_excel, state="disabled").grid(row=1, column=1, pady=5)

        self.result_box = tk.Text(self, width=45, height=8, state="disabled")
        self.result_box.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        self.excel_file = None
        self.download_btn = self.grid_slaves(row=1, column=1)[0]  # get download button
        self.load_data()

    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        filename = "db.json"
        if os.path.exists(filename):
            with open(filename, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
            for book in data:
                self.tree.insert("", tk.END, values=(book["id"], book["name"], book["price"], book["year"]))

    def export_to_excel(self):
        filename = "db.json"
        if not os.path.exists(filename):
            messagebox.showerror("Error", "No data to export")
            return

        with open(filename, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Database file is corrupted")
                return

        if not data:
            messagebox.showinfo("Info", "No data available to export")
            return

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["ID", "Name", "Price", "Year"])
        for book in data:
            ws.append([book["id"], book["name"], book["price"], book["year"]])

        self.excel_file = "books.xlsx"
        wb.save(self.excel_file)

        self.result_box.config(state="normal")
        self.result_box.delete(1.0, tk.END)
        for row in ws.iter_rows(values_only=True):
            self.result_box.insert(tk.END, "\t".join(map(str, row)) + "\n")
        self.result_box.config(state="disabled")

        self.download_btn.config(state="normal")
        messagebox.showinfo("Success", f"Data exported to {self.excel_file}")

        # Optional: Auto-open file
        if platform.system() == "Windows":
            os.startfile(self.excel_file)
        elif platform.system() == "Darwin":
            subprocess.call(["open", self.excel_file])
        else:
            subprocess.call(["xdg-open", self.excel_file])

    def download_excel(self):
        if not self.excel_file or not os.path.exists(self.excel_file):
            messagebox.showerror("Error", "No exported file found")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            title="Save Excel File As"
        )
        if save_path:
            shutil.copy(self.excel_file, save_path)
            messagebox.showinfo("Success", f"File downloaded to {save_path}")

