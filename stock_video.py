import os
import random
import requests
from config import PEXELS_API_KEY, OUTPUT_DIR


def fetch_background_video(query, filename="background.mp4"):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)

    headers = {"Authorization": PEXELS_API_KEY}
    url = "https://api.pexels.com/videos/search?query=" + query + "&orientation=portrait&per_page=10"
    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()
    videos = resp.json().get("videos", [])
    if not videos:
        raise ValueError("No stock videos found for: " + query)

    video = random.choice(videos)
    video_files = sorted(video["video_files"], key=lambda v: v.get("width", 0))
    best = video_files[0]
    for v in video_files:
        if v.get("width", 0) <= 1080:
            best = v

    with requests.get(best["link"], stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    print("Background video downloaded:", path)
    return path
