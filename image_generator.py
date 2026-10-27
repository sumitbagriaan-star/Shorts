"""Har scene ki cartoon image banata hai.
Pehle Hugging Face FLUX (free, HF_TOKEN), phir Google Imagen (GEMINI_API_KEY), warna placeholder."""
import io
import os
import time

import requests
from PIL import Image, ImageDraw

import config as C

HF_MODEL = os.getenv("HF_MODEL", "black-forest-labs/FLUX.1-schnell")
IMAGEN_MODEL = os.getenv("IMAGE_MODEL", "imagen-3.0-generate-002")


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


def _hf_image(prompt, seed):
    url = f"https://router.huggingface.co/hf-inference/models/{HF_MODEL}"
    headers = {"Authorization": f"Bearer {os.environ['HF_TOKEN']}"}
    payload = {
        "inputs": prompt,
        "parameters": {"width": 576, "height": 1024, "seed": seed},
    }
    r = requests.post(url, headers=headers, json=payload, timeout=180)
    r.raise_for_status()
    return r.content


def _imagen_image(prompt):
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    resp = client.models.generate_images(
        model=IMAGEN_MODEL,
        prompt=prompt,
        config=types.GenerateImagesConfig(number_of_images=1, aspect_ratio="9:16"),
    )
    return resp.generated_images[0].image.image_bytes


def generate_image(prompt, path, seed):
    methods = []
    if os.getenv("HF_TOKEN"):
        methods.append(("huggingface", lambda: _hf_image(prompt, seed)))
    if os.getenv("GEMINI_API_KEY"):
        methods.append(("imagen", lambda: _imagen_image(prompt)))

    for attempt in range(4):
        for name, fn in methods:
            try:
                data = fn()
                _cover_resize(Image.open(io.BytesIO(data))).save(path, quality=92)
                return path
            except Exception as e:  # noqa: BLE001
                print(f"  image try {attempt + 1} ({name}) fail: {e}")
        time.sleep(5 * (attempt + 1))

    print("  image nahi bani, placeholder laga raha hoon")
    _placeholder().save(path, quality=92)
    return path
