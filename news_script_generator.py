import os
import re
import json
from groq import Groq
from news_fetcher import get_random_headline

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
MODEL = "openai/gpt-oss-20b"


def _extract_json(text):
    text = text.strip()
    text = re.sub(r"^```json", "", text)
    text = re.sub(r"^```", "", text)
    text = re.sub(r"```$", "", text)
    return json.loads(text.strip())


def generate_news_script():
    headline = get_random_headline()
    print("Selected headline:", headline["title"])
    print("Source URL:", headline["source_url"])

    client = Groq(api_key=GROQ_API_KEY)

    prompt = (
        "You are a factual YouTube Shorts news scriptwriter. Your ONLY job is to rephrase "
        "the following news headline and summary into natural spoken-style sentences for a "
        "30-45 second video.\n\n"
        "STRICT RULES:\n"
        "- Use ONLY the facts given below. Do NOT add any name, number, date, quote, or detail "
        "that is not explicitly present in the headline or summary.\n"
        "- Do NOT guess, speculate, or invent outcomes, reactions, or context.\n"
        "- If the summary is thin, keep the script short rather than filling gaps with invented details.\n"
        "- Rephrase in your own natural words - do not copy the exact sentence structure of the source.\n\n"
        "Headline: " + headline["title"] + "\n"
        "Summary: " + headline["summary"] + "\n\n"
        "Write:\n"
        "1. A short punchy hook (under 10 words) that references this news topic\n"
        "2. 3 to 4 short factual sentences explaining the news, strictly from the facts given\n"
        "3. A short closing line (e.g. Follow for daily news updates)\n\n"
        "Also write:\n"
        "- title: under 100 characters, based only on the given facts\n"
        "- description: 1-2 lines summarizing the news (facts only) plus 3-4 relevant hashtags\n\n"
        "Return ONLY valid JSON, no extra text, no markdown formatting, in exactly this format:\n"
        '{"title": "...", "description": "...", "script_lines": ["...", "...", "...", "..."]}'
    )

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    raw = resp.choices[0].message.content
    data = _extract_json(raw)

    if not data.get("script_lines"):
        raise ValueError("Groq response did not include script_lines")

    # Always attach the original source link so it can be verified before upload
    data["description"] = data.get("description", "") + "\n\nSource: " + headline["source_url"]
    data["full_script"] = " ".join(data["script_lines"])
    data["topic"] = "news"
    data["source_title"] = headline["title"]
    data["source_url"] = headline["source_url"]
    return data


if __name__ == "__main__":
    result = generate_news_script()
    print("TITLE:", result["title"])
    print("SCRIPT:", result["full_script"])
    print("SOURCE:", result["source_url"])
