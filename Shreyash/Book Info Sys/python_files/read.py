import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os

from python_files.widget_files.logger import Log
from python_files.widget_files.ButtonClass import MyButton
from python_files.widget_files.LabelClass import MyLabel
from python_files.widget_files.EntryClass import MyEntry


class Read_tab(ttk.Frame):
    def __init__(self, parent, logger: Log):
        super().__init__(parent)
        self.logger = logger
        self.logger.info_logger("Read tab initialized")

        self.file_entries = []
        self.file_paths = []
        self.dataframes = []
        
        #self.file_label = MyLabel(self,text="Files").grid(row=0,col=0)
        # Scrollable container
        entry_container = ttk.Frame(self)
        entry_container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.canvas = tk.Canvas(entry_container, height=200)
        self.scroll_frame = ttk.Frame(self.canvas)
        self.scrollbar = ttk.Scrollbar(entry_container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Add and Combine Buttons
        MyButton(self, text="➕ Add File", command=self.add_file_entry).grid(row=1, column=0, padx=10, sticky="w")
        MyButton(self, text="🔗 Combine Files", command=self.combine_files).grid(row=1, column=0, padx=10, sticky="e")

        # Treeview to show combined data
        self.tree = ttk.Treeview(self, show="headings", height=15)
        self.tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.tree_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scrollbar.set)
        self.tree_scrollbar.grid(row=2, column=1, sticky="ns")

        # Layout configuration
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def add_file_entry(self):
        row = len(self.file_entries)

        # Entry field for file path
        entry = MyEntry(self.scroll_frame)
        entry.grid(row=row, column=0, padx=5, pady=5, sticky="ew")

        # Browse button
        browse_btn = MyButton(self.scroll_frame, text="Browse", command=lambda e=entry: self.browse_file(e))
        browse_btn.grid(row=row, column=1, padx=5)

        # Delete button
        delete_btn = MyButton(self.scroll_frame, text="❌", command=lambda idx=row: self.delete_file_entry(idx))
        delete_btn.grid(row=row, column=2, padx=5)

        # Save entry and buttons
        self.file_entries.append({
            "entry": entry,
            "browse_btn": browse_btn,
            "delete_btn": delete_btn
        })

    def browse_file(self, entry):
        path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("XML files", "*.xml")]
        )
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)

    def delete_file_entry(self, index):
        try:
            file_entry = self.file_entries.pop(index)

            # Get path BEFORE destroying the widget
            path = file_entry["entry"].get().strip()

            # Destroy widgets
            file_entry["entry"].destroy()
            file_entry["browse_btn"].destroy()
            file_entry["delete_btn"].destroy()

            # Remove from file_paths/dataframes if loaded
            if path in self.file_paths:
                idx = self.file_paths.index(path)
                self.file_paths.pop(idx)
                self.dataframes.pop(idx)

            # Refresh grid layout
            self.refresh_entries()

        except IndexError:
            self.logger.error_logger("Invalid index for deletion")


    def refresh_entries(self):
        for idx, file_entry in enumerate(self.file_entries):
            file_entry["entry"].grid(row=idx, column=0, padx=5, pady=5, sticky="ew")
            file_entry["browse_btn"].grid(row=idx, column=1, padx=5)
            file_entry["delete_btn"].grid(row=idx, column=2, padx=5)
            file_entry["delete_btn"].configure(command=lambda i=idx: self.delete_file_entry(i))

    def combine_files(self):
        self.file_paths.clear()
        self.dataframes.clear()

        # Load each valid file
        for entry in self.file_entries:
            path = entry["entry"].get().strip()
            if path and os.path.exists(path):
                try:
                    df = self.load_file(path)
                    self.file_paths.append(path)
                    self.dataframes.append(df)
                    self.logger.info_logger(f"Loaded file: {path}")
                except Exception as e:
                    self.logger.error_logger(f"Error loading {path}: {e}")
                    messagebox.showerror("Load Error", f"Failed to load:\n{path}\n\n{e}")
                    return
            elif path:
                messagebox.showerror("File Not Found", f"Path does not exist:\n{path}")
                return

        if not self.dataframes:
            messagebox.showinfo("No Files", "No valid files to combine.")
            return

        try:
            combined_df = pd.concat(self.dataframes, ignore_index=True)
            self.display_in_treeview(combined_df)
            messagebox.showinfo("Success", f"Combined {len(self.file_paths)} files with {len(combined_df)} rows.")
            self.logger.info_logger(f"Combined data shape: {combined_df.shape}")
        except Exception as e:
            self.logger.error_logger(f"Combining error: {e}")
            messagebox.showerror("Error", f"Failed to combine files:\n{e}")

    def load_file(self, path):
        ext = os.path.splitext(path)[-1].lower()
        if ext in [".xlsx", ".xls"]:
            return pd.read_excel(path)
        elif ext == ".xml":
            return pd.read_xml(path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    def display_in_treeview(self, df):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(df.columns)

        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        for _, row in df.iterrows():
            self.tree.insert("", tk.END, values=[str(v) for v in row.values])
