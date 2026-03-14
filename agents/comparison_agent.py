from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

class ComparisonAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def run(self, topic: str) -> str:
        print(f"[ComparisonAgent] ⚖️ Comparing: {topic}")

        prompt = f"""You are an expert analyst.
Compare the two subjects in this query.

Query: {topic}

Structure your response as:
1. Brief overview of each
2. Key similarities
3. Key differences
4. When to use each
5. Final recommendation

Be specific and practical."""

        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                max_tokens=800,
            )
            result = response.choices[0].message.content
            print(f"[ComparisonAgent] ✓ Comparison complete!")
            return result
        except Exception as e:
            print(f"[ComparisonAgent] ✗ Error: {e}")
            return f"Error: {e}"