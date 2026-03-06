from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

class CodeAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def run(self, task: str) -> str:
        print(f"[CodeAgent] 💻 Writing code for: {task}")

        prompt = f"""You are an expert programmer. Write clean working code for this task.

Task: {task}

Structure your response as:
1. Brief explanation of approach (2-3 sentences)
2. Complete working code with comments
3. Example usage showing how to run it
4. Any important notes or edge cases

Write production quality code."""

        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                max_tokens=800,
            )
            result = response.choices[0].message.content
            print(f"[CodeAgent] ✓ Code complete!")
            return result

        except Exception as e:
            print(f"[CodeAgent] ✗ Error: {e}")
            return f"Error: {e}"