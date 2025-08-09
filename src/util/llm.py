import json
from loguru import logger
from ..config import LLM_PROVIDER, OPENAI_API_KEY
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY) if LLM_PROVIDER == "openai" else None

POST_SCHEMA = {
    "type": "object",
    "properties": {
        "platform": {"type": "string", "enum": ["twitter", "linkedin"]},
        "text": {"type": "string", "minLength": 20, "maxLength": 1300},
        "links": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["platform", "text", "links"],
    "additionalProperties": False
}

def summarize_to_post(trend: dict, platform: str) -> dict:
    """
    Deterministic prompt + structured output.
    trend = {"entity": "...", "score": 87, "evidence": [{"title": "...", "url": "..."}]}
    """
    if client is None:
        # Minimal fallback for local dev
        return {
            "platform": platform,
            "text": f"{trend['entity']} is trending (score {trend['score']}). Sources: " +
                    ", ".join([e['url'] for e in trend.get('evidence', [])]),
            "links": [e['url'] for e in trend.get('evidence', [])][:3]
        }

    sys = "You are an assistant that writes concise, source-linked posts."
    prompt = (
        f"Create a {platform} post summarizing why '{trend['entity']}' is trending. "
        "Must include 1-3 source URLs from evidence. Avoid emojis and hashtags unless obvious. "
        "Return JSON strictly matching this schema:\n"
        f"{json.dumps(POST_SCHEMA)}\n"
        "Keep X(Twitter) under 280 chars; LinkedIn can be longer but concise."
    )
    evidence_text = "\n".join([f"- {e['title']} ({e['url']})" for e in trend.get("evidence", [])])

    # Using JSON response format (structured output)
    resp = client.chat.completions.create(
        model="gpt-4o-mini",  # swap as desired
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": sys},
            {"role": "user", "content": prompt},
            {"role": "user", "content": evidence_text}
        ],
        temperature=0.2,
    )
    try:
        data = json.loads(resp.choices[0].message.content)
        return data
    except Exception as e:
        logger.error(f"Failed to parse LLM JSON: {e}")
        return {
            "platform": platform,
            "text": f"{trend['entity']} is trending (score {trend['score']}).",
            "links": [e['url'] for e in trend.get('evidence', [])][:2]
        }