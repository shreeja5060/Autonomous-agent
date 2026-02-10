from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()

class CriticAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    def evaluate(self, original_task: str, output: str) -> dict:
        """Evaluate the quality of the output"""
        print("[CriticAgent] 🎯 Evaluating output quality...")
        
        prompt = f"""Evaluate this task execution:

Original Task: {original_task}
Output: {output}

Evaluate on these criteria (score 0-10 each):
1. Completeness: Did it fully address the task?
2. Accuracy: Is the information correct and factual?
3. Clarity: Is it easy to understand?
4. Usefulness: Is it actionable?

Also provide:
- Overall quality score (0-10)
- Specific strengths (2-3 points)
- Specific weaknesses or improvements needed (2-3 points)
- Should retry? (yes/no)

Return ONLY valid JSON in this format:
{{
    "completeness": 8,
    "accuracy": 9,
    "clarity": 7,
    "usefulness": 8,
    "overall_score": 8.0,
    "strengths": ["strength1", "strength2"],
    "improvements": ["improvement1", "improvement2"],
    "should_retry": false
}}"""
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                max_tokens=500,
            )
            
            response_text = chat_completion.choices[0].message.content
            
            # Clean JSON if wrapped in markdown
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            evaluation = json.loads(response_text)
            
            print(f"[CriticAgent] ✓ Evaluation complete! Overall score: {evaluation['overall_score']}/10")
            
            return evaluation
            
        except Exception as e:
            print(f"[CriticAgent] ✗ Error: {e}")
            return {
                "overall_score": 5.0,
                "should_retry": False,
                "error": str(e)
            }