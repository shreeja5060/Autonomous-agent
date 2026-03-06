import json
import os

class FeedbackStore:
    def __init__(self):
        self.filepath = "feedback.json"
        self.feedback = self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                return json.load(f)
        return []

    def save_feedback(self, topic: str, response: str, rating: int, comment: str = ""):
        entry = {
            "topic": topic,
            "response": response[:300],  # save first 300 chars
            "rating": rating,
            "comment": comment
        }
        self.feedback.append(entry)
        with open(self.filepath, "w") as f:
            json.dump(self.feedback, f, indent=2)
        print(f"[FeedbackStore] ✓ Saved rating {rating}/5 for: {topic}")

    def get_best_responses(self) -> list:
        """Return responses rated 4 or 5 stars"""
        return [f for f in self.feedback if f["rating"] >= 4]

    def get_worst_responses(self) -> list:
        """Return responses rated 1 or 2 stars"""
        return [f for f in self.feedback if f["rating"] <= 2]

    def get_stats(self) -> dict:
        if not self.feedback:
            return {"total": 0, "average_rating": 0}
        total = len(self.feedback)
        avg = sum(f["rating"] for f in self.feedback) / total
        return {
            "total": total,
            "average_rating": round(avg, 2),
            "best_count": len(self.get_best_responses()),
            "worst_count": len(self.get_worst_responses())
        }