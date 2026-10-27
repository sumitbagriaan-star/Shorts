"""Claude se bachon ki chhoti story/rhyme ka script (JSON) banwata hai."""
import json
import anthropic
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
    msg = anthropic.Anthropic().messages.create(
        model=C.LLM_MODEL,
        max_tokens=2500,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    data = _parse_json(msg.content[0].text)
    scenes = data.get("scenes") or []
    if len(scenes) < 3 or not all(s.get("narration") and s.get("image_prompt") for s in scenes):
        raise ValueError("Script adhura hai, dobara try karo")
    data.setdefault("character", "a cute friendly little animal")
    data.setdefault("tags", ["kids", "cartoon"])
    data.setdefault("description", "")
    return data
