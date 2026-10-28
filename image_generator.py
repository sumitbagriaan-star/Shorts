"""Har scene ki cartoon image banata hai (Hugging Face, HF_TOKEN se). Fail ho to placeholder."""
import io
import os
import time

import requests
from PIL import Image, ImageDraw

import config as C

HF_MODELS = [
    "stabilityai/stable-diffusion-xl-base-1.0",
    "black-forest-labs/FLUX.1-dev",
    "stabilityai/stable-diffusion-3.5-large",
]


def _cover_resize(img):
    img = img.convert("RGB")
    scale = max(C.WIDTH / img.width, C.HEIGHT / img.height)
    img = img.resize((int(img.width * scale) + 1, int(img.height * scale) + 1), Image.LANCZOS)
    left = (img.width - C.WIDTH) // 2
    top = (img.height - C.HEIGHT) // 2
    return img.crop((left, top, left + C.WIDTH, top + C.HEIGHT))


def _placeholder():
    img = Image.new("RGB", (C.WIDTH, C.HEIGHT), (255, 226, 140))
    d = ImageDraw.Draw(img)
    d.ellipse((290, 760, 790, 1260), fill=(255, 170, 120))
    d.ellipse((420, 900, 480, 960), fill=(60, 40, 40))
    d.ellipse((600, 900, 660, 960), fill=(60, 40, 40))
    d.arc((440, 960, 640, 1120), 20, 160, fill=(60, 40, 40), width=10)
    return img


def _hf_image(model, prompt, seed):
    url = "https://router.huggingface.co/hf-inference/models/" + model
    headers = {"Authorization": "Bearer " + os.environ["HF_TOKEN"]}
    payload = {
        "inputs": prompt,
        "parameters": {"width": 768, "height": 1344, "seed": seed},
    }
    r = requests.post(url, headers=headers, json=payload, timeout=180)
    r.raise_for_status()
    return r.content


def _try_model(model, prompt, seed, path):
    try:
        data = _hf_image(model, prompt, seed)
        _cover_resize(Image.open(io.BytesIO(data))).save(path, quality=92)
        return True
    except Exception as e:
        print("  image fail (" + model + "): " + str(e))
        return False


def generate_image(prompt, path, seed):
    if not os.getenv("HF_TOKEN"):
        print("  HF_TOKEN set nahi hai")
    else:
        for attempt in range(3):
            for model in HF_MODELS:
                if _try_model(model, prompt, seed, path):
                    return path
            time.sleep(5 * (attempt + 1))

    print("  image nahi bani, placeholder laga raha hoon")
    _placeholder().save(path, quality=92)
    return path
