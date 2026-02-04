from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Idea:
    text: str
    done: bool


class IdeaStore:
    def __init__(self, csv_path: str) -> None:
        self.csv_path = Path(csv_path)

    def load(self) -> list[Idea]:
        ideas: list[Idea] = []
        if not self.csv_path.exists():
            return ideas
        with self.csv_path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                text = (row.get("idea") or "").strip()
                done_raw = (row.get("done") or "false").strip().lower()
                if text:
                    ideas.append(Idea(text=text, done=done_raw == "true"))
        return ideas

    def mark_done(self, idea_text: str) -> None:
        if not self.csv_path.exists():
            return
        with self.csv_path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        for row in rows:
            if (row.get("idea") or "").strip() == idea_text:
                row["done"] = "true"
        with self.csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["idea", "done"])
            writer.writeheader()
            writer.writerows(rows)
