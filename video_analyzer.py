import re
import requests
from collections import Counter

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    YouTubeTranscriptApi = None

STOPWORDS = set("""
the a an is are was were to of and or but in on at for with this that these those
you your i we our it its as be by from not so if then than just very really
""".split())


def extract_video_id(url):
    patterns = [r"(?:v=|/shorts/|youtu\.be/|/embed/)([A-Za-z0-9_-]{11})"]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    raise ValueError("Could not find a valid YouTube video ID in this link.")


def get_video_title(video_id):
    url = "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=" + video_id + "&format=json"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            return resp.json().get("title", "")
    except Exception:
        pass
    return ""


def get_transcript_text(video_id):
    if YouTubeTranscriptApi is None:
        return ""
    try:
        segments = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join(seg["text"] for seg in segments)
    except Exception as e:
        print("Transcript not available (captions may be off):", e)
        return ""


def extract_keywords(text, top_n=5):
    words = re.findall(r"[a-zA-Z']+", text.lower())
    words = [w for w in words if w not in STOPWORDS and len(w) > 3]
    common = Counter(words).most_common(top_n)
    return [w for w, _ in common]


def analyze_style(transcript):
    sentences = re.split(r"(?<=[.!?])\s+", transcript.strip()) if transcript else []
    sentences = [s for s in sentences if s]
    avg_len = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
    return {
        "num_beats": len(sentences),
        "avg_sentence_length": round(avg_len, 1),
    }


def analyze_video(url):
    video_id = extract_video_id(url)
    title = get_video_title(video_id)
    transcript = get_transcript_text(video_id)
    keywords = extract_keywords(title + " " + transcript, top_n=5)
    style = analyze_style(transcript)
    return {
        "source_title": title,
        "keywords": keywords,
        "suggested_topic": " ".join(keywords[:3]) if keywords else title,
        **style,
    }
