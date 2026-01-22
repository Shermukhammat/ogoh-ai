import json, os
from google import genai
from dotenv import load_dotenv


load_dotenv()


SCHEMA = {
    "type": "object",
    "properties": {
        "label": {
            "type": "string",
            "enum": ["drug_ad", "drug_related", "benign", "uncertain"],
        },
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "reasons": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
            "maxItems": 6,
        },
        "suspicious_spans": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "why": {"type": "string"},
                },
                "required": ["text", "why"],
            },
            "maxItems": 6,
        },
    },
    "required": ["label", "confidence", "reasons"],
}

SYSTEM = """You are a safety classification engine for Telegram messages.
Goal: detect drug advertisements or trafficking-related promotions.
Return ONLY JSON that matches the schema.
Do NOT include extra keys. Do NOT rewrite the input. Do NOT generate any ad content.
If it looks like selling/ordering/delivery/“закладка”/wholesale/DM-to-buy style, label drug_ad.
If it's discussion/news/jokes without selling intent, label drug_related.
If unclear, label uncertain.
"""

_client = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set")
        _client = genai.Client(api_key=api_key)
    return _client


def classify(text: str) -> dict:
    resp = _get_client().models.generate_content(
        model="gemini-2.5-flash",
        contents=[
        {
            "role": "model",
            "parts": [{"text": SYSTEM}]
        },
        {
            "role": "user",
            "parts": [{"text": text}]
        }
    ],
    config={
        "response_mime_type": "application/json",
        "response_schema": SCHEMA,
        "temperature": 0.0,
    }
    )
    payload = getattr(resp, "parsed", None) or getattr(resp, "text", None)
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return {
                "label": "uncertain",
                "confidence": 0.0,
                "reasons": ["Classifier returned unparseable output."],
                "suspicious_spans": [],
            }
    raise RuntimeError("Classifier returned an unexpected response type.")
