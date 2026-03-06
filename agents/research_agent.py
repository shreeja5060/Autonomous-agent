from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

class ResearchAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    def run(self, topic: str, past_context: str = "No memory found") -> str:
        print(f"[ResearchAgent] 🔍 Researching topic: {topic}")

        # Only add context block if we actually have past memory
        context_block = ""
        if past_context != "No memory found":
            context_block = f"\n\nPrevious research on this topic:\n{past_context}\nBuild on this, don't repeat it."
        
        prompt = f"""You are a research expert. Research this topic and provide:

1. Key facts (3-5 important points)
2. Current trends and developments
3. Important considerations or challenges

Topic: {topic}{context_block}

Be concise, factual, and well-structured."""
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                max_tokens=600,
            )
            
            research_data = chat_completion.choices[0].message.content
            print(f"[ResearchAgent] ✓ Research complete!")
            return research_data
            
        except Exception as e:
            print(f"[ResearchAgent] ✗ Error: {e}")
            return f"Error during research: {e}"