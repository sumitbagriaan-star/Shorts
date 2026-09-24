import re
import random
import feedparser

FEED_URLS = [
    "https://indianexpress.com/section/india/feed/",
    "https://indianexpress.com/feed/",
]


def _clean_html(text):
    return re.sub("<[^<]+?>", "", text or "").strip()


def fetch_top_news(n=8):
    for url in FEED_URLS:
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                items = []
                for entry in feed.entries[:n]:
                    title = entry.get("title", "").strip()
                    summary = entry.get("summary", "") or entry.get("description", "")
                    summary = _clean_html(summary)[:400]
                    link = entry.get("link", "")
                    if title:
                        items.append({"title": title, "summary": summary, "source_url": link})
                if items:
                    print("Fetched", len(items), "headlines from", url)
                    return items
        except Exception as e:
            print("Feed failed:", url, "-", e)
            continue
    return []


def get_random_headline():
    items = fetch_top_news()
    if not items:
        raise RuntimeError("Could not fetch any news headlines from any feed")
    return random.choice(items)
