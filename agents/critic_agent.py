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
        
        prompt = f"""You are a STRICT quality evaluator with high standards.

Scoring guidelines:
- 1-4: Poor. Missing key information, factually wrong, or unclear
- 5-6: Average. Addresses topic but lacks depth or has minor errors
- 7-8: Good. Comprehensive and accurate with minor improvements needed
- 9-10: Excellent. Only for truly exceptional responses

Most responses should score 5-7.
Only give 8+ for genuinely excellent responses.
Give 9-10 extremely rarely.

Original Task: {original_task}
Output: {output}

Evaluate STRICTLY on these criteria (score 0-10 each):
1. Completeness: Did it fully address the task?
2. Accuracy: Is the information correct and factual?
3. Clarity: Is it easy to understand?
4. Usefulness: Is it actionable?

Also provide:
- Overall quality score (0-10)
- Specific strengths (2-3 points)
- Specific weaknesses or improvements needed (2-3 points)
- Should retry? (yes if score below 6, no if score 6 or above)

Return ONLY valid JSON in this format:
{{
    "completeness": 6,
    "accuracy": 7,
    "clarity": 5,
    "usefulness": 6,
    "overall_score": 6.0,
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