import os
import random
import glob
from datetime import datetime

from config import TOPIC_LIST, OUTPUT_DIR
from script_generator import generate_script as generate_quote_script
from news_script_generator import generate_news_script
from tts_generator import generate_voiceover
from stock_video import fetch_background_video
from video_maker import make_short
from video_analyzer import analyze_video

PHOTOS_DIR = "photos"
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")


def pick_background_source(topic):
    photo_files = []
    if os.path.isdir(PHOTOS_DIR):
        for ext in IMAGE_EXTENSIONS:
            photo_files.extend(glob.glob(os.path.join(PHOTOS_DIR, "*" + ext)))
            photo_files.extend(glob.glob(os.path.join(PHOTOS_DIR, "*" + ext.upper())))

    use_photo = photo_files and random.random() < 0.5

    if use_photo:
        chosen = random.choice(photo_files)
        print("Using uploaded photo as background:", chosen)
        return chosen, "image"
    else:
        search_term = topic.split()[0]
        path = fetch_background_video(search_term)
        return path, "video"


def get_script(video_link):
    if video_link:
        print("STEP 0: Analyzing reference video link (topic/style only, no audio/video reused)...")
        try:
            analysis = analyze_video(video_link)
            print("Source title:", analysis["source_title"])
            print("Detected keywords:", analysis["keywords"])
        except Exception as e:
            print("Could not analyze the link, continuing with news mode. Reason:", e)

    print("STEP 1: Fetching latest news and generating script with AI...")
    try:
        data = generate_news_script()
        print("News script generated successfully.")
        return data
    except Exception as e:
        print("News script generation failed, falling back to motivational quotes. Reason:", e)
        return generate_quote_script()


def run():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    video_link = os.environ.get("VIDEO_LINK", "").strip()

    data = get_script(video_link)
    print("Title:", data["title"])
    print("Script:", data["full_script"])

    print("STEP 2: Generating voiceover...")
    voiceover_path = generate_voiceover(data["full_script"])

    print("STEP 3: Choosing background (photo or stock video)...")
    bg_topic = data.get("topic") or random.choice(TOPIC_LIST)
    if bg_topic == "news":
        bg_topic = random.choice(TOPIC_LIST)
    background_path, background_type = pick_background_source(bg_topic)
    print("Background type:", background_type, "-", background_path)

    print("STEP 4: Assembling final video...")
    date_str = datetime.utcnow().strftime("%Y-%m-%d_%H%M")
    output_filename = "short_" + date_str + ".mp4"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    make_short(background_path, voiceover_path, data["script_lines"], output_path, background_type=background_type)

    meta_path = os.path.join(OUTPUT_DIR, "short_" + date_str + "_info.txt")
    with open(meta_path, "w") as f:
        f.write("TITLE:\n" + data["title"] + "\n\nDESCRIPTION:\n" + data["description"] + "\n")

    print("ALL DONE. Video + info saved in outputs/:", output_filename)


if __name__ == "__main__":
    run()
