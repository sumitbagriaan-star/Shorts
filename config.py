import os

# GitHub Actions me ye value automatically "Secrets" se aayegi (PEXELS_API_KEY).
# Local test ke liye chaho to yahan seedha bhi daal sakte ho, lekin GitHub par
# secret hi use hoga — is file me daalna zaroori nahi hai.
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "PASTE_YOUR_PEXELS_KEY_HERE")

TOPIC_LIST = [
    "space facts",
    "human body facts",
    "ocean mysteries",
    "psychology tricks",
    "history facts",
    "animal facts",
    "money habits",
    "science experiments",
]

VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FONT_SIZE = 70
OUTPUT_DIR = "outputs"
