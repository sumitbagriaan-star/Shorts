# YouTube Shorts — Fully Automatic Video Generator (GitHub Actions)

Isse setup karne ke baad **kabhi kahi jaana nahi padega** — video roz apne aap ban ke
repo me store hoga. Tumhe bas kabhi kabhi jaake download + YouTube pe upload karna hai
(2 min ka kaam).

Sab kuch **phone browser se** ho sakta hai (Chrome me github.com kholke).

---

## SETUP (ek baar karna hai, ~15-20 min)

### 1. GitHub account banao
- https://github.com/signup pe jaao
- Free account banao (email se)

### 2. Naya repository banao
- Login karne ke baad, top-right **"+"** icon → **"New repository"**
- Naam do: `yt-shorts-bot` (ya jo chaho)
- **Private** select karo (recommended — apna code/key private rahega)
- **"Create repository"** dabao

### 3. Saari files upload karo
- Naye repo page pe **"uploading an existing file"** link dikhega (ya "Add file" → "Upload files")
- In sab files ko ek saath select karke upload karo (Downloads folder se):
  - `config.py`
  - `script_generator.py`
  - `tts_generator.py`
  - `stock_video.py`
  - `video_maker.py`
  - `main_generate.py`
  - `requirements.txt`
- Commit karo ("Commit changes" button)

### 4. Workflow file alag se banao (folder ke saath)
Ye file ek special folder (`.github/workflows/`) me honi chahiye — upload se directly folder nahi banta, isliye "Create new file" use karenge:
1. Repo ke main page pe **"Add file"** → **"Create new file"**
2. File name wale box me **poora path type karo**: `.github/workflows/daily_short.yml`
   (jaise hi `/` type karoge, GitHub apne aap folder bana dega)
3. Neeche wali `daily_short.yml` file ka poora content copy karke paste kar do
4. **"Commit changes"** dabao

### 5. Pexels API key ko "Secret" ke roop me add karo
⚠️ Key ko kabhi code me mat likho — hamesha secret me:
1. Repo ke andar **"Settings"** tab (top menu)
2. Left side **"Secrets and variables"** → **"Actions"**
3. **"New repository secret"** dabao
4. Name: `PEXELS_API_KEY`
5. Value: apni Pexels key paste karo
6. **"Add secret"** dabao

### 6. Workflow ko write-permission do (video commit karne ke liye)
1. **"Settings"** → left side **"Actions"** → **"General"**
2. Neeche **"Workflow permissions"** section dhundo
3. **"Read and write permissions"** select karo
4. **"Save"** dabao

### 7. Pehli baar manually chalao (test)
1. Top menu me **"Actions"** tab pe jaao
2. Left side **"Daily YouTube Short Generator"** workflow pe click karo
3. Right side **"Run workflow"** button dabao → phir se **"Run workflow"** (dropdown ke andar)
4. 2-4 minute wait karo — status **green tick ✅** hone tak refresh karte raho
5. Ho jaye toh repo ke **"outputs"** folder me jaao — wahan `short_YYYY-MM-DD_HHMM.mp4` aur ek `_info.txt` (title/description ke saath) milegi

### 8. Video download karo
- `outputs/` folder me jaake apni video file pe tap karo
- **"Download raw file"** ya "..." menu se download option milega
- Phone me save ho jayegi, phir wahan se seedha YouTube app me upload kar do

---

## Ye roz apne aap kab chalega?
Workflow **roz subah 9:00 AM (IST)** apne aap chalega — koi kaam nahi karna. Bas jab
chaho `outputs/` folder check karke naya video download + upload kar dena.

Time badalna ho toh `daily_short.yml` file me ye line edit karo:
```
- cron: "30 3 * * *"
```
(Ye UTC time hai — IST = UTC + 5:30. Format: minute hour * * *)

---

## Troubleshooting
- **Actions tab me workflow na dikhe**: Settings → Actions → General me "Allow all actions" enabled hona chahiye
- **Run fail ho (red cross)**: us run pe click karke "generate-short" job kholo, laal error line dhundo — screenshot bhej dena
- **outputs folder me video na aaye lekin run green tick ho**: Step 6 (write permissions) shayad set nahi hua — dobara check karo
