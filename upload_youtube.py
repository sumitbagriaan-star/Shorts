"""YouTube par video upload karta hai (YouTube Data API v3). 'Made for Kids' hamesha ON."""
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import config as C


def _service():
    creds = Credentials(
        None,
        refresh_token=os.environ["YT_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
        scopes=["https://www.googleapis.com/auth/youtube.upload"],
    )
    creds.refresh(Request())
    return build("youtube", "v3", credentials=creds)


def upload_video(path, title, description, tags):
    title = title if "#shorts" in title.lower() else f"{title} #Shorts"
    body = {
        "snippet": {
            "title": title[:100],
            "description": f"{description}\n\n#Shorts #KidsCartoon\nAI ki madad se bana video.",
            "tags": tags[:15],
            "categoryId": "1",  # Film & Animation
        },
        "status": {
            "privacyStatus": C.PRIVACY,
            "selfDeclaredMadeForKids": True,
            "containsSyntheticMedia": True,
        },
    }
    media = MediaFileUpload(path, mimetype="video/mp4", resumable=True)
    req = _service().videos().insert(part="snippet,status", body=body, media_body=media)
    resp = None
    while resp is None:
        _, resp = req.next_chunk()
    return resp["id"]
