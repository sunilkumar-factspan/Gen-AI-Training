import os
from dotenv import load_dotenv
from groq import Groq

from llm.prompt import SYSTEM_PROMPT

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_code(user_input, history=None):
    try:
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT + """

STRICT:
- Do NOT use os, subprocess, sys
- Only use playwright and time
"""
            }
        ]

        if history:
            for h in history:
                messages.append({"role": "user", "content": h["user"]})
                messages.append({
                    "role": "assistant",
                    "content": f"```python\n{h['assistant']}\n```"
                })

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0,
            max_tokens=1000
        )

        result = response.choices[0].message.content

        if not result:
            return "ERROR: Empty response from LLM"

        return result

    except Exception as e:
        return f"ERROR: {str(e)}"