import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMEngine:
    def __init__(self):
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

    def generate_response(self, user_input):
        prompt = f"""
You are MedSafe AI, a healthcare safety education assistant.

Respond strictly in this format:

### Summary
### Possible Causes
### Risk Level (LOW / MEDIUM / HIGH)
### Home Care Advice
### Warning Signs
### When to Seek Medical Help

User Input:
{user_input}
"""

        completion = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a medical safety assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        return completion.choices[0].message.content