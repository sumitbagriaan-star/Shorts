"""Saari settings yahan hain. Zyada tar cheezein environment variables se badal sakte ho."""
import os

# --- Language / voice ---
LANG = os.getenv("VIDEO_LANG", "hi")  # "hi" = Hindi, "en" = English
VOICES = {"hi": "hi-IN-SwaraNeural", "en": "en-US-AnaNeural"}
VOICE = os.getenv("TTS_VOICE", VOICES.get(LANG, VOICES["en"]))
TTS_RATE = os.getenv("TTS_RATE", "-8%")    # thoda dheere bolne ke liye
TTS_PITCH = os.getenv("TTS_PITCH", "+4Hz")  # thodi pyaari awaaz

# --- Script (LLM) ---
LLM_MODEL = os.getenv("LLM_MODEL", "claude-sonnet-5-5")
SCENES = int(os.getenv("SCENES", "7"))  # 7 scenes ~ 45-55 sec
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-3.8-flash")
# --- Video ---
WIDTH, HEIGHT, FPS = 1080, 1920, 24
OUT_DIR = "outputs"
WORK_DIR = "work"
MUSIC_FILE = "assets/music.mp3"  # optional: halka background music (royalty-free hi use karo)

STYLE = (
    "cute colorful 2D cartoon illustration for toddlers, soft rounded shapes, "
    "bright cheerful colors, simple clean background, children's picture book style, "
    "friendly smiling characters, no text, no letters, no words, vertical composition"
)

# --- Upload ---
UPLOAD = os.getenv("UPLOAD", "1") == "1"        # UPLOAD=0 => sirf video banega
PRIVACY = os.getenv("PRIVACY", "private")        # private / unlisted / public
CHANNEL_NAME = os.getenv("CHANNEL_NAME", "Little Stars")

# Har weekday ke liye alag category, taaki videos repeat na lagein (Mon..Sun)
CATEGORIES = [
    "a short rhyme or poem with animals",
    "counting numbers 1 to 10 with a fun story",
    "learning colors through a small adventure",
    "a tiny moral story about sharing and kindness",
    "learning alphabets A B C with cute objects",
    "a bedtime story with a sleepy animal",
    "learning shapes (circle, square, triangle) in a playful story",
]
