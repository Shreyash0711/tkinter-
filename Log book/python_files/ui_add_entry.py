import tkinter as tk
from tkinter import messagebox

class AddEntryFrame(tk.Frame):
    def __init__(self, master, storage):
        super().__init__(master)
        self.storage = storage

        tk.Label(self, text="Week Number:").grid(row=0, column=0, sticky="w")
        self.week_entry = tk.Entry(self)
        self.week_entry.grid(row=0, column=1, pady=5)

        self.tasks_text = self._create_textbox("Tasks Completed", 1)
        self.challenges_text = self._create_textbox("Challenges Faced", 2)
        self.learnings_text = self._create_textbox("New Learnings", 3)
        self.goals_text = self._create_textbox("Goals for Next Week", 4)
        self.notes_text = self._create_textbox("Personal Notes", 5)

        tk.Button(self, text="Save Entry", command=self.save_entry).grid(row=6, column=1, pady=10)

    def _create_textbox(self, label, row):
        tk.Label(self, text=label).grid(row=row, column=0, sticky="w")
        textbox = tk.Text(self, height=3, width=40)
        textbox.grid(row=row, column=1, pady=5)
        return textbox

    def save_entry(self):
        week = self.week_entry.get()
        tasks = self.tasks_text.get("1.0", "end-1c")
        challenges = self.challenges_text.get("1.0", "end-1c")
        learnings = self.learnings_text.get("1.0", "end-1c")
        goals = self.goals_text.get("1.0", "end-1c")
        notes = self.notes_text.get("1.0", "end-1c")

        if not week.strip():
            messagebox.showwarning("Warning", "Week number is required!")
            return

        self.storage.add_entry(week, tasks, challenges, learnings, goals, notes)
        messagebox.showinfo("Success", "Entry saved successfully!")
        self.clear_fields()

    def clear_fields(self):
        self.week_entry.delete(0, "end")
        for widget in [self.tasks_text, self.challenges_text, self.learnings_text, self.goals_text, self.notes_text]:
            widget.delete("1.0", "end")
