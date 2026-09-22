import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import (
    VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip
)
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


def _prepare_video_background(background_path, duration):
    bg = VideoFileClip(background_path).without_audio()
    if bg.duration < duration:
        bg = bg.loop(n=int(duration // bg.duration) + 1)
    bg = bg.subclip(0, duration)

    bg = bg.resize(height=VIDEO_HEIGHT)
    if bg.w < VIDEO_WIDTH:
        bg = bg.resize(width=VIDEO_WIDTH)
    bg = bg.crop(x_center=bg.w / 2, y_center=bg.h / 2, width=VIDEO_WIDTH, height=VIDEO_HEIGHT)
    return bg


def _prepare_image_background(image_path, duration):
    # Load and scale image so it fully covers the 9:16 frame (like object-fit: cover)
    img_clip = ImageClip(image_path)
    scale = max(VIDEO_WIDTH / img_clip.w, VIDEO_HEIGHT / img_clip.h)
    base_w = int(img_clip.w * scale) + 4
    base_h = int(img_clip.h * scale) + 4
    img_clip = img_clip.resize((base_w, base_h))

    zoom_amount = 1.15  # 15% zoom over the duration - gives a subtle Ken Burns motion

    def zoom_func(t):
        return 1 + (zoom_amount - 1) * (t / duration)

    zoomed = img_clip.resize(zoom_func).set_duration(duration).set_position("center")
    bg = CompositeVideoClip([zoomed], size=(VIDEO_WIDTH, VIDEO_HEIGHT)).set_duration(duration)
    return bg


def make_short(background_path, voiceover_path, script_lines, output_path, background_type="video"):
    audio = AudioFileClip(voiceover_path)
    duration = audio.duration

    if background_type == "image":
        bg = _prepare_image_background(background_path, duration)
    else:
        bg = _prepare_video_background(background_path, duration)

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
