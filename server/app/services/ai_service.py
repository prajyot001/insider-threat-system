import os
import json
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

AI_MODEL = os.getenv("AI_MODEL", "llama-3.1-8b-instant")
AI_COOLDOWN_SECONDS = int(os.getenv("AI_COOLDOWN_SECONDS", 300))

# Track last AI call per device (in-memory for now)
last_ai_call = {}


def is_cooldown_active(device_id):
    now = time.time()
    if device_id not in last_ai_call:
        return False

    return (now - last_ai_call[device_id]) < AI_COOLDOWN_SECONDS


def update_cooldown(device_id):
    last_ai_call[device_id] = time.time()


def call_ai(payload: dict):
    try:
        system_prompt = """
You are a cybersecurity risk scoring engine.

Analyze the behavioral summary.
Return ONLY valid JSON in this format:

{
  "ai_score": number (0-100),
  "severity": "low" | "medium" | "high",
  "reason": "short explanation"
}
No extra text.
"""

        user_prompt = json.dumps(payload)

        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0,
            max_tokens=200
        )

        content = response.choices[0].message.content.strip()

        # Parse JSON safely
        ai_result = json.loads(content)

        return ai_result

    except Exception as e:
        print("AI ERROR:", str(e))
        return {
            "ai_score": None,
            "severity": "unknown",
            "reason": "AI call failed"
        }