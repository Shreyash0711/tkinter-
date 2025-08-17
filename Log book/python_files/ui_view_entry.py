import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class ViewEntriesFrame(tk.Frame):
    def __init__(self, master, storage):
        super().__init__(master)
        self.storage = storage
        self.entries = []

        # --- Title ---
        title = tk.Label(self, text="Work Log Entries", font=("Arial", 14, "bold"))
        title.pack(pady=(10, 6))

        # --- Container for table + scrollbars ---
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=10)

        # Scrollbars
        self.scroll_y = tk.Scrollbar(table_frame, orient="vertical")
        self.scroll_x = tk.Scrollbar(table_frame, orient="horizontal")

        # --- Treeview (Excel-like table) ---
        self.columns = ("Week", "Date", "Tasks", "Challenges", "Learnings", "Goals", "Notes")
        self.tree = ttk.Treeview(
            table_frame,
            columns=self.columns,
            show="headings",
            yscrollcommand=self.scroll_y.set,
            xscrollcommand=self.scroll_x.set,
            height=12
        )

        # Attach scrollbars
        self.scroll_y.config(command=self.tree.yview)
        self.scroll_x.config(command=self.tree.xview)
        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)

        # Configure headers & columns
        for col in self.columns:
            self.tree.heading(col, text=col)
        # Sensible starting widths; all columns stretch horizontally
        col_widths = {
            "Week": 70,
            "Date": 110,
            "Tasks": 220,
            "Challenges": 220,
            "Learnings": 220,
            "Goals": 220,
            "Notes": 240,
        }
        for col, w in col_widths.items():
            self.tree.column(col, width=w, minwidth=60, stretch=True, anchor="w")

        # Bind selection + double-click
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)
        self.tree.bind("<Double-1>", self.on_row_double_click)

        # --- Controls row ---
        controls = tk.Frame(self)
        controls.pack(fill="x", padx=10, pady=(6, 6))

        tk.Button(controls, text="Refresh", command=self.load_entries).pack(side="left")
        tk.Button(controls, text="Open Full View", command=self.open_full_view).pack(side="left", padx=(8, 0))
        tk.Button(controls, text="Copy Selected to Clipboard", command=self.copy_selected_to_clipboard).pack(side="left", padx=(8, 0))

        # --- Details Panel (always shows full, wrapped text of selection) ---
        details = tk.LabelFrame(self, text="Full Details (Selected Row)")
        details.pack(fill="both", expand=False, padx=10, pady=(0, 10))

        self.detail_widgets = {}
        self._make_detail_row(details, "Week", 0)
        self._make_detail_row(details, "Date", 1)
        self._make_detail_row(details, "Tasks", 2, big=True)
        self._make_detail_row(details, "Challenges", 3, big=True)
        self._make_detail_row(details, "Learnings", 4, big=True)
        self._make_detail_row(details, "Goals", 5, big=True)
        self._make_detail_row(details, "Notes", 6, big=True)

        # Load data initially
        self.load_entries()

    # --------- UI helpers ---------
    def _make_detail_row(self, parent, label, row, big=False):
        tk.Label(parent, text=f"{label}:", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="ne", padx=(8, 6), pady=4)
        if big:
            txt = tk.Text(parent, wrap="word", height=4, width=80)
        else:
            txt = tk.Text(parent, wrap="word", height=1, width=40)
        txt.grid(row=row, column=1, sticky="we", padx=(0, 8), pady=4)
        parent.grid_columnconfigure(1, weight=1)
        txt.configure(state="disabled")
        self.detail_widgets[label] = txt

    def _set_detail(self, label, value):
        widget = self.detail_widgets[label]
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", value if value is not None else "")
        widget.configure(state="disabled")

    def _clear_details(self):
        for label in self.detail_widgets:
            self._set_detail(label, "")

    # --------- Data loading & table population ---------
    def load_entries(self):
        try:
            self.entries = self.storage.load_entries() or []
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load entries:\n{e}")
            self.entries = []

        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert rows (latest first)
        for idx, entry in enumerate(reversed(self.entries)):
            values = (
                entry.get("week", ""),
                entry.get("date", ""),
                entry.get("tasks", ""),
                entry.get("challenges", ""),
                entry.get("learnings", ""),
                entry.get("goals", ""),
                entry.get("notes", ""),
            )
            self.tree.insert("", "end", iid=str(idx), values=values)

        # Auto-select first row if any
        self._clear_details()
        children = self.tree.get_children()
        if children:
            self.tree.selection_set(children[0])
            self.tree.focus(children[0])
            self._update_details_from_item(children[0])

    # --------- Selection handlers ---------
    def on_row_select(self, _event=None):
        selected = self.tree.selection()
        if not selected:
            self._clear_details()
            return
        self._update_details_from_item(selected[0])

    def _update_details_from_item(self, item_id):
        vals = self.tree.item(item_id, "values")
        data = dict(zip(self.columns, vals))
        # Update details pane with wrapped, full text
        for key in self.columns:
            self._set_detail(key, data.get(key, ""))

    def on_row_double_click(self, _event=None):
        self.open_full_view()

    # --------- Actions ---------
    def open_full_view(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Please select a row first.")
            return

        vals = self.tree.item(selected[0], "values")
        data = dict(zip(self.columns, vals))

        top = tk.Toplevel(self)
        top.title(f"Week {data.get('Week', '')} — Full Entry")
        top.geometry("800x600")

        # Make a scrollable detail view
        container = tk.Frame(top)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        scroll_y = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_x = tk.Scrollbar(container, orient="horizontal", command=canvas.xview)

        frame = tk.Frame(canvas)
        frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        canvas.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")

        # Populate fields
        for i, key in enumerate(self.columns):
            tk.Label(frame, text=f"{key}:", font=("Arial", 10, "bold")).grid(row=i, column=0, sticky="ne", padx=8, pady=6)
            txt = tk.Text(frame, wrap="word", height=6 if key not in ("Week", "Date") else 1, width=90)
            txt.grid(row=i, column=1, sticky="we", padx=(0, 12), pady=6)
            txt.insert("1.0", data.get(key, ""))
            txt.configure(state="disabled")
            frame.grid_columnconfigure(1, weight=1)

    def copy_selected_to_clipboard(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Please select a row first.")
            return
        vals = self.tree.item(selected[0], "values")
        data = dict(zip(self.columns, vals))

        # Copy as a neat block of text
        block = []
        for k in self.columns:
            block.append(f"{k}: {data.get(k, '')}")
        text = "\n".join(block)
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("Copied", "Selected entry copied to clipboard.")
