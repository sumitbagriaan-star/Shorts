import os
import random
from datetime import datetime

from config import TOPIC_LIST, OUTPUT_DIR
from script_generator import generate_script
from tts_generator import generate_voiceover
from stock_video import fetch_background_video
from video_maker import make_short


def run():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("STEP 1: Generating script...")
    data = generate_script()
    print("Title:", data["title"])
    print("Script:", data["full_script"])

    print("STEP 2: Generating voiceover...")
    voiceover_path = generate_voiceover(data["full_script"])

    print("STEP 3: Fetching background video...")
    search_term = data["topic"].split()[0]
    background_path = fetch_background_video(search_term)

    print("STEP 4: Assembling final video...")
    date_str = datetime.utcnow().strftime("%Y-%m-%d_%H%M")
    output_filename = "short_" + date_str + ".mp4"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    make_short(background_path, voiceover_path, data["script_lines"], output_path)

    # Save title/description alongside, so upload karte waqt copy-paste ho sake
    meta_path = os.path.join(OUTPUT_DIR, "short_" + date_str + "_info.txt")
    with open(meta_path, "w") as f:
        f.write("TITLE:\n" + data["title"] + "\n\nDESCRIPTION:\n" + data["description"] + "\n")

    print("ALL DONE. Video + info saved in outputs/:", output_filename)


if __name__ == "__main__":
    run()
