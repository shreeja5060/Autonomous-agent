from agents.research_agent import ResearchAgent
from agents.summary_agent import SummaryAgent
from agents.critic_agent import CriticAgent
from agents.teach_agent import TeachAgent
from agents.code_agent import CodeAgent
from memory.memory_store import MemoryStore
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

class CoordinatorAgent:
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.summary_agent = SummaryAgent()
        self.critic_agent = CriticAgent()
        self.teach_agent = TeachAgent()
        self.code_agent = CodeAgent()
        self.memory = MemoryStore()
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def detect_intent(self, goal: str) -> str:
        """Ask the LLM what type of query this is"""
        print(f"[Coordinator]  Detecting intent...")

        prompt = f"""Classify this query into exactly one of these categories:
- research   (asking about a topic, what is X, how does X work)
- teaching   (teach me X, explain X, how do I learn X)
- coding     (write code, build X, create a function)
- comparison (compare X vs Y, difference between X and Y)

Query: {goal}

Reply with ONE word only: research, teaching, coding, or comparison"""

        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            max_tokens=10,
        )

        intent = response.choices[0].message.content.strip().lower()
        print(f"[Coordinator] ✓ Intent detected: {intent}")

        # Safety check — if LLM returns something unexpected default to research
        if intent not in ["research", "teaching", "coding", "comparison"]:
            intent = "research"

        return intent

    def execute(self, goal: str, max_iterations: int = 2) -> dict:
        # Step 1 — detect what type of query this is
        intent = self.detect_intent(goal)

        results = {
            "goal": goal,
            "intent": intent,
            "iterations": [],
            "final_output": None,
            "final_evaluation": None
        }

        # Step 2 — route to the right pipeline
        if intent == "teaching":
            print(f"[Coordinator] 📚 Routing to Teaching pipeline")
            output = self.teach_agent.run(goal)
            evaluation = self.critic_agent.evaluate(goal, output)
            results["final_output"] = output
            results["final_evaluation"] = evaluation
            self.memory.save(goal, output)
            return results

        elif intent == "coding":
            print(f"[Coordinator]  Routing to Coding pipeline")
            output = self.code_agent.run(goal)
            evaluation = self.critic_agent.evaluate(goal, output)
            results["final_output"] = output
            results["final_evaluation"] = evaluation
            self.memory.save(goal, output)
            return results

        else:
            # research or comparison — use existing pipeline
            print(f"[Coordinator]  Routing to Research pipeline")
            for iteration in range(max_iterations):
                print(f"\n{'='*60}")
                print(f" ITERATION {iteration + 1}/{max_iterations}")
                print(f"{'='*60}\n")

                iteration_data = {
                    "iteration_num": iteration + 1,
                    "steps": []
                }

                past_context = self.memory.recall(goal)
                research_output = self.research_agent.run(goal, past_context)
                iteration_data["steps"].append({
                    "step": "research",
                    "output": research_output
                })

                summary_output = self.summary_agent.run(research_output)
                iteration_data["steps"].append({
                    "step": "summary",
                    "output": summary_output
                })

                evaluation = self.critic_agent.evaluate(goal, summary_output)
                iteration_data["evaluation"] = evaluation
                results["iterations"].append(iteration_data)

                if not evaluation.get("should_retry", False) or iteration == max_iterations - 1:
                    results["final_output"] = summary_output
                    results["final_evaluation"] = evaluation
                    self.memory.save(goal, summary_output)
                    print(f"\n Task complete after {iteration + 1} iteration(s)!")
                    break
                else:
                    print(f"\n Retrying to improve quality...")

        return results