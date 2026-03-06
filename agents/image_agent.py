from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

class ImageAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def run(self, image_base64: str, question: str) -> str:
        print(f"[ImageAgent] 🖼️ Analyzing image...")

        try:
            response = self.client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            },
                            {
                                "type": "text",
                                "text": question if question else "Describe this image in detail."
                            }
                        ]
                    }
                ],
                max_tokens=800,
            )

            result = response.choices[0].message.content
            print(f"[ImageAgent] ✓ Image analysis complete!")
            return result

        except Exception as e:
            print(f"[ImageAgent] ✗ Error: {e}")
            return f"Error analyzing image: {e}"