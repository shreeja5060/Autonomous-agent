from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

class SummaryAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    def run(self, research_data: str) -> str:
        print("[SummaryAgent] 📝 Creating executive summary...")
        
        prompt = f"""Summarize this research into a clear, actionable executive summary.

Make it:
- 3-4 sentences maximum
- Easy to understand
- Highlight the most important takeaway

Research data:
{research_data}"""
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.3-70b-versatile",
                max_tokens=300,
            )
            
            summary = chat_completion.choices[0].message.content
            
            print(f"[SummaryAgent] ✓ Summary complete!")
            
            return summary
            
        except Exception as e:
            print(f"[SummaryAgent] ✗ Error: {e}")
            return f"Error during summarization: {e}"