from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

class TeachAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def run(self, topic: str) -> str:
        print(f"[TeachAgent]  Teaching: {topic}")

        prompt = f"""You are an expert teacher. Teach this topic clearly.

Topic: {topic}

Structure your response as:
1. Simple explanation (1-2 sentences, no jargon)
2. Real world analogy (relate it to everyday life)
3. Step by step breakdown (3-5 steps)
4. Simple code example (if relevant)
5. Common mistakes to avoid

Teach like you're explaining to a smart beginner."""

        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                max_tokens=800,
            )
            result = response.choices[0].message.content
            print(f"[TeachAgent]  Teaching complete!")
            return result

        except Exception as e:
            print(f"[TeachAgent]  Error: {e}")
            return f"Error: {e}"