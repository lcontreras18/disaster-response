import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

def classify_incident(location: str, description: str) -> dict:
    prompt = f"""You are an emergency dispatch AI. Analyze this incident and respond ONLY with a JSON object.

Location: {location}
Description: {description}

Respond with ONLY this JSON (no other text, no markdown):
{{
    "severity": "LOW" or "MEDIUM" or "HIGH" or "CRITICAL",
    "category": "FLOOD" or "FIRE" or "MEDICAL" or "STRUCTURAL" or "OTHER",
    "summary": "one sentence description of the emergency"
}}

Severity guide:
- LOW: minor issue, no immediate danger
- MEDIUM: moderate risk, response needed soon
- HIGH: serious danger, urgent response needed
- CRITICAL: life-threatening, immediate response required"""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=256,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    response_text = message.content[0].text
    result = json.loads(response_text)
    return result


def safe_classify(location: str, description: str) -> dict:
    try:
        return classify_incident(location, description)
    except Exception as e:
        print(f"AI classification failed: {e}")
        return {
            "severity": "MEDIUM",
            "category": "OTHER",
            "summary": description[:100]
        }
