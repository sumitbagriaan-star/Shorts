# Kids Cartoon Shorts (auto daily/weekly)

Script (Claude) -> cartoon images -> bachon wali awaaz -> vertical video -> YouTube upload.

## Setup (ek baar)
1. In files ko apni repo me daalo. Purani news wali files (`news_fetcher.py`, `news_script_generator.py`,
   `stock_video.py`, `video_analyzer.py`) aur purana workflow hata do.
2. **ANTHROPIC_API_KEY**: console.anthropic.com se key banao.
3. **YouTube**: Google Cloud me project banao > "YouTube Data API v3" ON > OAuth client (type: Desktop app).
   Apne computer par chalao:
   `YT_CLIENT_ID=... YT_CLIENT_SECRET=... python get_refresh_token.py`
   Browser me channel se login karo, jo `YT_REFRESH_TOKEN` print ho use copy karo.
4. GitHub repo > Settings > Secrets and variables > Actions me 4 secrets daalo:
   `ANTHROPIC_API_KEY`, `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN`.
5. Actions tab > "Kids Cartoon Short" > Run workflow. Pehle videos **private** upload honge; dekh kar `PRIVACY: public` karo.

## Badalne ki jagah
- Hindi/English: workflow me `VIDEO_LANG` (hi/en)
- Daily ya weekly: workflow ke `cron`
- Topics: `config.py` me `CATEGORIES`
- Background music: `assets/music.mp3` rakho (royalty-free hi)
- Local test bina upload: `UPLOAD=0 python main_generate.py`

## Zaroori baatein
- Video hamesha "Made for Kids" mark hota hai.
- Naya Google API project unverified ho to uploads private lock reh sakte hain; YouTube ka API audit form bharna pad sakta hai.
- Har video thoda alag hona chahiye (code topic repeat avoid karta hai) warna YouTube "repetitive content" maan sakta hai.
- Shuru me har video khud dekh kar hi public karo.
