from groq import Groq
from ddgs import DDGS
import os
from dotenv import load_dotenv

load_dotenv()

class ResearchAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.ddgs = DDGS()

    def _search_web(self, topic: str) -> str:
        """Search the web and return results as a string"""
        print(f"[ResearchAgent] 🌐 Searching web for: {topic}")
        
        try:
            results = self.ddgs.text(topic, max_results=5)
            
            # Format results into a readable string for the LLM
            formatted = ""
            for i, r in enumerate(results, 1):
                formatted += f"Result {i}: {r['title']}\n"
                formatted += f"Summary: {r['body']}\n"
                formatted += f"URL: {r['href']}\n\n"
            
            return formatted
        
        except Exception as e:
            return f"Search failed: {e}"

    def run(self, topic: str, past_context: str = "No memory found") -> str:
        print(f"[ResearchAgent] 🔍 Researching topic: {topic}")

        # Step 1 — get real web results
        web_results = self._search_web(topic)

        # Step 2 — build context from memory
        context_block = ""
        if past_context != "No memory found":
            context_block = f"\n\nPrevious research on this topic:\n{past_context}\nBuild on this, don't repeat it."

        # Step 3 — pass BOTH to the LLM
        prompt = f"""You are a research expert. Use these real web search results to answer the topic.
Do NOT use your training data — only use what's in the search results below.

Topic: {topic}

Real web search results:
{web_results}
{context_block}

Based ONLY on the search results above, provide:
1. Key facts (3-5 important points)
2. Current trends and developments
3. Important considerations or challenges

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