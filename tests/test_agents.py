import pytest
import sys
import os


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_memory_save_and_recall():
    from memory.memory_store import MemoryStore
    memory = MemoryStore()
    memory.save("test_topic", "test_response")
    result = memory.recall("test_topic")
    assert result == "test_response"

def test_memory_recall_missing():
    from memory.memory_store import MemoryStore
    memory = MemoryStore()
    result = memory.recall("topic_that_does_not_exist_xyz")
    assert result == "No memory found"

def test_feedback_save_and_stats():
    from memory.feedback_store import FeedbackStore
    store = FeedbackStore()
    store.save_feedback("test_topic", "test_response", 5, "great")
    stats = store.get_stats()
    assert stats["total"] > 0
    assert stats["average_rating"] > 0

def test_feedback_best_responses():
    from memory.feedback_store import FeedbackStore
    store = FeedbackStore()
    store.save_feedback("good_topic", "good_response", 5, "excellent")
    best = store.get_best_responses()
    assert len(best) > 0

def test_feedback_worst_responses():
    from memory.feedback_store import FeedbackStore
    store = FeedbackStore()
    store.save_feedback("bad_topic", "bad_response", 1, "terrible")
    worst = store.get_worst_responses()
    assert len(worst) > 0