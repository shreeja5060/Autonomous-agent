import json
import os

class MemoryStore:
    def __init__(self):
        self.filepath = "memory.json"
        self.memory = self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                return json.load(f)
        return {}

    def save(self, key: str, value: str):
        self.memory[key] = value
        with open(self.filepath, "w") as f:
            json.dump(self.memory, f)

    def recall(self, key: str):
        return self.memory.get(key, "No memory found")

    def get_all(self):
        return self.memory