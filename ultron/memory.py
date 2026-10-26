"""Small JSON-backed memory store for the prototype."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class MemoryStore:
    """Persist short notes without requiring a database or third-party package."""

    def __init__(self, path: str | Path = ".ultron_memory.json") -> None:
        self.path = Path(path)

    def load(self) -> list[str]:
        if not self.path.exists():
            return []
        try:
            data: Any = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"could not read memory store: {exc}") from exc
        if not isinstance(data, list) or not all(isinstance(item, str) for item in data):
            raise RuntimeError("memory store must contain a JSON list of strings")
        return data

    def add(self, note: str) -> None:
        note = note.strip()
        if not note:
            raise ValueError("memory cannot be empty")
        notes = self.load()
        notes.append(note)
        try:
            self.path.write_text(json.dumps(notes, indent=2) + "\n", encoding="utf-8")
        except OSError as exc:
            raise RuntimeError(f"could not save memory store: {exc}") from exc
