from agents.coordinator import CoordinatorAgent
from memory.memory_store import MemoryStore
import time

class TaskPipeline:
    def __init__(self):
        self.coordinator = CoordinatorAgent()
        self.memory = MemoryStore()
        self.metrics = {
            "total_tasks": 0,
            "total_iterations": 0,
            "avg_score": 0.0
        }

    def run(self, task: str, max_iterations: int = 2):
        """Execute task and return results"""
        print(f"\n{'='*70}")
        print(f"🤖 STARTING TASK: {task}")
        print(f"{'='*70}\n")
        
        start_time = time.time()
        
        # Execute task
        result = self.coordinator.execute(task, max_iterations)
        
        # Calculate metrics
        execution_time = time.time() - start_time
        result["execution_time"] = round(execution_time, 2)
        
        # Update global metrics
        self.metrics["total_tasks"] += 1
        self.metrics["total_iterations"] += len(result["iterations"])
        if result["final_evaluation"]:
            current_avg = self.metrics["avg_score"]
            total = self.metrics["total_tasks"]
            new_score = result["final_evaluation"].get("overall_score", 0)
            self.metrics["avg_score"] = ((current_avg * (total - 1)) + new_score) / total
        
        # Save to memory
        self.memory.save(task, result)
        
        print(f"\n{'='*70}")
        print("✅ TASK COMPLETE")
        print(f"⏱️  Execution time: {execution_time:.2f} seconds")
        print(f"{'='*70}\n")
        
        return result
    
    def show_metrics(self):
        """Display performance metrics"""
        print("\n" + "="*70)
        print("📊 SYSTEM PERFORMANCE METRICS")
        print("="*70)
        print(f"Total tasks completed: {self.metrics['total_tasks']}")
        print(f"Total iterations: {self.metrics['total_iterations']}")
        print(f"Average quality score: {self.metrics['avg_score']:.1f}/10")
        print(f"Avg iterations per task: {self.metrics['total_iterations']/max(1, self.metrics['total_tasks']):.1f}")
        print("="*70 + "\n")