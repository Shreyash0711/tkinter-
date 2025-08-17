import json
import os
from datetime import datetime

class Storage:
    def __init__(self, filename="worklog.json"):
        self.filename = filename
        self._init_file()

    def _init_file(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def load_entries(self):
        with open(self.filename, "r") as f:
            return json.load(f)

    def save_entries(self, entries):
        with open(self.filename, "w") as f:
            json.dump(entries, f, indent=4)

    def add_entry(self, week, tasks, challenges, learnings, goals, notes):
        entries = self.load_entries()
        new_entry = {
            "week": week,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "tasks": tasks,
            "challenges": challenges,
            "learnings": learnings,
            "goals": goals,
            "notes": notes
        }
        entries.append(new_entry)
        self.save_entries(entries)
