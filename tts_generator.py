import os
from gtts import gTTS
from config import OUTPUT_DIR


def generate_voiceover(text, filename="voiceover.mp3"):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)
    tts = gTTS(text=text, lang="en", slow=False)
    tts.save(path)
    print("Voiceover saved:", path)
    return path
