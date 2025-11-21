import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")


def _clean_json_text(text: str) -> str:
    t = text.strip()
    if t.startswith("```"):
        t = t.lstrip("`")
        if t.lower().startswith("json"):
            t = t[4:]
        t = t.rstrip("`")
    return t.strip()


def summarize_and_tag(content: str):
    """
    Summarize international English news + classify topic & sentiment.
    Returns: (summary, topic, sentiment)
    """
    content_short = content[:4000]

    prompt = f"""
You are an expert news analyst with strong skills in summarization, topic classification,
and sentiment detection for international English news.

TASK:
From the news article below, generate a JSON with 3 fields only:
- "summary": A clear and informative summary in English, 3–6 sentences (about 80–150 words).
  Include the context, main actors, what happened, and the impact.
- "topic": One of:
  ["politics", "economy", "technology", "sports", "health", "entertainment", "world", "general"]
- "sentiment": One of ["positive", "negative", "neutral"].


TOPIC DEFINITIONS:
- politics: geopolitics, elections, government policies, diplomacy, conflict, military.
- economy: markets, inflation, trade, business, finance, oil prices, corporate updates.
- technology: AI, cybersecurity, gadgets, startups, software, scientific innovation.
- sports: football, basketball, racing, Olympics, tournaments, player transfers.
- health: disease, medicine, Covid-19, hospital updates, public health policy.
- entertainment: movies, music, celebrities, festivals, cultural events.
- world: global events, disasters, climate emergencies, humanitarian crises.
- general: anything that does not clearly fit other categories.

SENTIMENT RULES:
- positive: progress, recovery, growth, success, diplomatic resolution, positive outcomes.
- negative: conflict, crime, disaster, decline, losses, casualties, severe problems.
- neutral: mainly factual reporting without strong emotional tone.

NOTE:
Ensure the topic matches the dominant theme of the article. If multiple topics appear, choose the most prominent one.
Ensure the sentiment reflects the overall tone and outcome.

ARTICLE:
\"\"\"{content_short}\"\"\"

Return only valid JSON and nothing else.
    """

    try:
        resp = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "num_predict": 512,
                },
            },
            timeout=120,
        )
        resp.raise_for_status()
        raw = resp.json().get("response", "").strip()
        cleaned = _clean_json_text(raw)

        try:
            data = json.loads(cleaned)
            summary = data.get("summary") or content_short[:500]
            topic = (data.get("topic") or "general").lower()
            sentiment = (data.get("sentiment") or "neutral").lower()

            if topic not in [
                "politics",
                "economy",
                "technology",
                "sports",
                "health",
                "entertainment",
                "world",
                "general",
            ]:
                topic = "general"

            if sentiment not in ["positive", "negative", "neutral"]:
                sentiment = "neutral"

            return summary, topic, sentiment
        except Exception as e:
            print("[WARN] Failed to parse JSON, fallback to general/neutral")
            print("Raw partial:", raw[:300])
            return content_short[:500], "general", "neutral"

    except Exception as e:
        print(f"[WARN] summarize_and_tag failed → fallback. error: {e}")
        return content_short[:500], "general", "neutral"
