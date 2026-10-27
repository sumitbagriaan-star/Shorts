"""Poora pipeline: script -> images -> voice -> video -> (YouTube upload).
Chalane ke liye:  python main_generate.py
Sirf test (upload nahi):  UPLOAD=0 python main_generate.py"""
import datetime
import json
import os
import random

import config as C
from image_generator import generate_image
from script_generator import generate_script
from tts_generator import synthesize
from video_maker import make_video

HISTORY = os.path.join(C.OUT_DIR, "history.json")


def load_history():
    if os.path.exists(HISTORY):
        with open(HISTORY, encoding="utf-8") as f:
            return json.load(f)
    return []


def save_history(hist):
    with open(HISTORY, "w", encoding="utf-8") as f:
        json.dump(hist[-200:], f, ensure_ascii=False, indent=1)


def main():
    os.makedirs(C.OUT_DIR, exist_ok=True)
    os.makedirs(C.WORK_DIR, exist_ok=True)
    hist = load_history()

    today = datetime.date.today()
    category = os.getenv("CATEGORY") or C.CATEGORIES[today.weekday() % len(C.CATEGORIES)]
    print("Category:", category)

    script = generate_script(category, [h["title"] for h in hist])
    print("Title:", script["title"])

    seed = random.randint(1, 10**6)  # same seed => character thoda consistent
    scenes = []
    for i, sc in enumerate(script["scenes"]):
        print(f"Scene {i + 1}/{len(script['scenes'])}")
        img = os.path.join(C.WORK_DIR, f"scene_{i}.jpg")
        aud = os.path.join(C.WORK_DIR, f"scene_{i}.mp3")
        prompt = f"{C.STYLE}, {script['character']}, {sc['image_prompt']}"
        generate_image(prompt, img, seed)
        synthesize(sc["narration"], aud)
        scenes.append({"image": img, "audio": aud})

    out = os.path.join(C.OUT_DIR, f"{today.isoformat()}_{random.randint(100, 999)}.mp4")
    duration = make_video(scenes, out)
    print(f"Video ready: {out} ({duration:.0f}s)")
    if duration > 58:
        print("Dhyan do: 60 sec se zyada hai, Shorts ke bajay normal video ban sakta hai. SCENES kam karo.")

    video_id = None
    if C.UPLOAD:
        from upload_youtube import upload_video  # yahan import taaki UPLOAD=0 par keys na lagein

        video_id = upload_video(out, script["title"], script["description"], script["tags"])
        print("Uploaded: https://youtube.com/watch?v=" + video_id)

    hist.append({"date": today.isoformat(), "title": script["title"], "category": category, "video_id": video_id})
    save_history(hist)


if __name__ == "__main__":
    main()
