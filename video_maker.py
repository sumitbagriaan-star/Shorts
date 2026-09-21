import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip
from config import VIDEO_WIDTH, VIDEO_HEIGHT, FONT_SIZE


def make_caption_image(text, max_width, font_size=FONT_SIZE):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    font = None
    for fp in font_paths:
        try:
            font = ImageFont.truetype(fp, font_size)
            break
        except Exception:
            pass
    if font is None:
        font = ImageFont.load_default()

    dummy = Image.new("RGBA", (10, 10))
    draw = ImageDraw.Draw(dummy)

    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)

    line_height = font_size + 20
    img_h = line_height * len(lines) + 40
    img_w = max_width + 100
    img = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    y = 20
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_w = bbox[2] - bbox[0]
        x = (img_w - line_w) / 2
        offsets = [(-3, -3), (-3, 3), (3, -3), (3, 3), (0, -3), (0, 3), (-3, 0), (3, 0)]
        for ox, oy in offsets:
            draw.text((x + ox, y + oy), line, font=font, fill="black")
        draw.text((x, y), line, font=font, fill="white")
        y = y + line_height

    return np.array(img)


def make_short(background_path, voiceover_path, script_lines, output_path):
    audio = AudioFileClip(voiceover_path)
    duration = audio.duration

    bg = VideoFileClip(background_path).without_audio()
    if bg.duration < duration:
        bg = bg.loop(n=int(duration // bg.duration) + 1)
    bg = bg.subclip(0, duration)

    bg = bg.resize(height=VIDEO_HEIGHT)
    if bg.w < VIDEO_WIDTH:
        bg = bg.resize(width=VIDEO_WIDTH)
    bg = bg.crop(x_center=bg.w / 2, y_center=bg.h / 2, width=VIDEO_WIDTH, height=VIDEO_HEIGHT)

    n = len(script_lines)
    seg = duration / n
    caption_clips = []
    for i, line in enumerate(script_lines):
        img_array = make_caption_image(line, max_width=VIDEO_WIDTH - 100)
        clip = ImageClip(img_array).set_start(i * seg).set_duration(seg).set_position("center")
        caption_clips.append(clip)

    final = CompositeVideoClip([bg] + caption_clips, size=(VIDEO_WIDTH, VIDEO_HEIGHT))
    final = final.set_audio(audio).set_duration(duration)

    final.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")
    print("DONE! Video ready:", output_path)
    return output_path
