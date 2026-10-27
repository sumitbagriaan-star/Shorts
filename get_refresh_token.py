"""Sirf EK baar apne computer par chalao, YouTube refresh token nikalne ke liye.
Pehle: set YT_CLIENT_ID aur YT_CLIENT_SECRET (Google Cloud > OAuth client 'Desktop app')."""
import os
from google_auth_oauthlib.flow import InstalledAppFlow

cfg = {
    "installed": {
        "client_id": os.environ["YT_CLIENT_ID"],
        "client_secret": os.environ["YT_CLIENT_SECRET"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["http://localhost"],
    }
}
flow = InstalledAppFlow.from_client_config(cfg, ["https://www.googleapis.com/auth/youtube.upload"])
creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")
print("\nYT_REFRESH_TOKEN =", creds.refresh_token)
