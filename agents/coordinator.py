from agents.research_agent import ResearchAgent
from agents.summary_agent import SummaryAgent
from agents.critic_agent import CriticAgent
from memory.memory_store import MemoryStore

class CoordinatorAgent:
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.summary_agent = SummaryAgent()
        self.critic_agent = CriticAgent()
        self.memory = MemoryStore()

    def decide_plan(self, goal: str):
        print("[Coordinator] 📋 Planning task execution...")
        return ["research", "summary", "critique"]

    def execute(self, goal: str, max_iterations: int = 2) -> dict:
        plan = self.decide_plan(goal)

        results = {
            "goal": goal,
            "iterations": [],
            "final_output": None,
            "final_evaluation": None
        }

        for iteration in range(max_iterations):
            print(f"\n{'='*60}")
            print(f"🔄 ITERATION {iteration + 1}/{max_iterations}")
            print(f"{'='*60}\n")

            iteration_data = {
                "iteration_num": iteration + 1,
                "steps": []
            }

            # Research — passes memory context so agent builds on past knowledge
            print(f"[Coordinator] Step 1/{len(plan)}: Research")
            past_context = self.memory.recall(goal)
            research_output = self.research_agent.run(goal, past_context)
            iteration_data["steps"].append({
                "step": "research",
                "output": research_output
            })

            # Summary
            print(f"\n[Coordinator] Step 2/{len(plan)}: Summarize")
            summary_output = self.summary_agent.run(research_output)
            iteration_data["steps"].append({
                "step": "summary",
                "output": summary_output
            })

            # Critique
            print(f"\n[Coordinator] Step 3/{len(plan)}: Evaluate")
            evaluation = self.critic_agent.evaluate(goal, summary_output)
            iteration_data["evaluation"] = evaluation

            results["iterations"].append(iteration_data)

            if not evaluation.get("should_retry", False) or iteration == max_iterations - 1:
                results["final_output"] = summary_output
                results["final_evaluation"] = evaluation
                self.memory.save(goal, summary_output)  # save to disk
                print(f"\n✅ Task complete after {iteration + 1} iteration(s)!")
                break
            else:
                print(f"\n🔁 Retrying to improve quality...")

        return results