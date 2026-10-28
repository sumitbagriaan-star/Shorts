"""Har scene ki cartoon image banata hai (Hugging Face, HF_TOKEN se). Fail ho to placeholder."""
import io
import os
import time

import requests
from PIL import Image, ImageDraw

import config as C

HF_MODELS = [
    m.strip()
    for m in os.getenv(
        "HF_MODELS",
        "stabilityai/stable-diffusion-xl-base-1.0,"
        "black-forest-labs/FLUX.1-dev,"
        "stabilityai/stable-diffusion-3.5-large",
    ).split(",")
    if m.strip()
]


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


def _hf_image(model, prompt, seed):
    url = f"https://router.huggingface.co/hf-inference/models/{model}"
    headers = {"Authorization": f"Bearer {os.environ['HF_TOKEN']}"}
    payload = {
        "inputs": prompt,
        "parameters": {"width": 768, "height": 1344, "seed": seed},
    }
    r = requests.post(url, headers=headers, json=payload, timeout=180)
    r.raise_for_status()
    return r.content


def generate_image(prompt, path, seed):
    if os.getenv("HF_TOKEN"):
        for attempt in range(3):
            for model in HF_MODELS:
                try:
