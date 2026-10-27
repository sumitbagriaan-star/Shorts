"""Images + awaaz ko jod kar vertical (1080x1920) video banata hai, halke zoom animation ke saath."""
import os
from moviepy.editor import (
    AudioFileClip, CompositeAudioClip, CompositeVideoClip, ImageClip, concatenate_videoclips,
)
from moviepy.audio.fx.all import audio_loop
import config as C


def make_video(scenes, out_path):
    clips = []
    for i, s in enumerate(scenes):
        audio = AudioFileClip(s["audio"])
        dur = audio.duration + 0.5
        zoom_in = i % 2 == 0

        def scale(t, d=dur, zi=zoom_in):
            p = min(t / d, 1)
            return 1 + 0.07 * p if zi else 1.07 - 0.07 * p

        moving = ImageClip(s["image"]).set_duration(dur).resize(scale).set_position("center")
        clip = CompositeVideoClip([moving], size=(C.WIDTH, C.HEIGHT)).set_duration(dur)
        clips.append(clip.set_audio(audio))

    final = concatenate_videoclips(clips, method="compose")

    if os.path.exists(C.MUSIC_FILE):
        music = audio_loop(AudioFileClip(C.MUSIC_FILE), duration=final.duration).volumex(0.10)
        final = final.set_audio(CompositeAudioClip([final.audio, music]))

    final.write_videofile(
        out_path, fps=C.FPS, codec="libx264", audio_codec="aac", preset="medium", threads=2, logger=None
    )
    duration = final.duration
    final.close()
    return duration
