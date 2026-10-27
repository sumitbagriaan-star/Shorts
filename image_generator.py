"""Har scene ki cartoon image banata hai (free Pollinations service, no API key).
Kisi aur service (OpenAI, Stability, etc.) se badalna ho to sirf generate_image() badlo."""
import io
import time
from urllib.parse import quote

import requests
from PIL import Image, ImageDraw
import config as C


def _cover_resize(img):
    img = img.convert("RGB")
    scale = max(C.WIDTH / img.width, C.HEIGHT / img.height)
    img = img.resize((int(img.width * scale) + 1, int(img.height * scale) + 1), Image.LANCZOS)
    left, top = (img.width - C.WIDTH) // 2, (img.height - C.HEIGHT) // 2
    return img.crop((left, top, left + C.WIDTH, top + C.HEIGHT))


def _placeholder():
    img = Image.new("RGB", (C.WIDTH, C.HEIGHT), (255, 226, 140))
    d = ImageDraw.Draw(img)
    d.ellipse((290, 760, 790, 1260), fill=(255, 170, 120))
    d.ellipse((420, 900, 480, 960), fill=(60, 40, 40))
    d.ellipse((600, 900, 660, 960), fill=(60, 40, 40))
    d.arc((440, 960, 640, 1120), 20, 160, fill=(60, 40, 40), width=10)
    return img


def generate_image(prompt, path, seed):
    url = (
        f"https://image.pollinations.ai/prompt/{quote(prompt)}"
        f"?width={C.WIDTH}&height={C.HEIGHT}&seed={seed}&nologo=true"
    )
    for attempt in range(4):
        try:
            r = requests.get(url, timeout=180)
            r.raise_for_status()
            _cover_resize(Image.open(io.BytesIO(r.content))).save(path, quality=92)
            return path
        except Exception as e:  # noqa: BLE001
            print(f"  image try {attempt + 1} fail: {e}")
            time.sleep(5 * (attempt + 1))
    print("  image nahi bani, placeholder laga raha hoon")
    _placeholder().save(path, quality=92)
    return path
