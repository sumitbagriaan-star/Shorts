"""Gemini se bachon ki chhoti story/rhyme ka script (JSON) banwata hai."""
import json
import os

from google import genai
from google.genai import types

import config as C

SYSTEM = (
    "You write very short, safe, original scripts for cartoon videos for children aged 2-5. "
    "Rules: simple words, positive and gentle tone, nothing scary or violent, no brand names, "
    "no existing cartoon characters (invent original ones), no real people. "
    "Reply with valid JSON only, no markdown."
)


def _parse_json(text):
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("LLM ne JSON nahi diya")
    return json.loads(text[start : end + 1])


def generate_script(category, recent_titles):
    lang = {"hi": "simple Hindi written in Devanagari script", "en": "simple English"}[C.LANG]
    prompt = f"""Create one kids cartoon short about: {category}.
Language of narration, title and description: {lang}.
Exactly {C.SCENES} scenes. Each narration is 12-18 words (about 6-8 seconds when spoken).
Do NOT reuse these recent titles/ideas: {recent_titles[-15:]}

Return JSON with this shape:
{{
  "title": "catchy title under 70 characters",
  "description": "2 short lines for parents",
  "tags": ["kids", "cartoon", "..."],
  "character": "ONE fixed English description of the main character's look (colors, clothes, shape) reused in every scene",
  "scenes": [
    {{"narration": "text to be spoken", "image_prompt": "English description of what is shown in this scene"}}
  ]
}}"""
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    resp = client.models.generate_content(
        model=C.LLM_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM,
            response_mime_type="application/json",
            max_output_tokens=8192,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        ),
    )
    data = _parse_json(resp.text)
    scenes = data.get("scenes") or []
    if len(scenes) < 3 or not all(s.get("narration") and s.get("image_prompt") for s in scenes):
        raise ValueError("Script adhura hai, dobara try karo")
    data.setdefault("character", "a cute friendly little animal")
    data.setdefault("tags", ["kids", "cartoon"])
    data.setdefault("description", "")
    return data
