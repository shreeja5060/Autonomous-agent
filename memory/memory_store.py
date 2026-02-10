class MemoryStore:
    def __init__(self):
        self.memory = {}

    def save(self, key: str, value: str):
        print("[Memory] Saving result")
        self.memory[key] = value

    def recall(self, key: str):
        return self.memory.get(key, "No memory found")