
---

# 🎵 Spotify → YouTube Music Playlist Transfer (Batch + Single)

This project allows you to transfer **one playlist** or **multiple Spotify playlists at once** into **YouTube Music**, while preserving order, logging missing songs, and avoiding rate-limits.

You can choose between:

* **Single playlist transfer**
* **Batch playlist transfer (recommended)**

---

# 📌 Features

✔ Transfers playlists from Spotify to YouTube Music
✔ Keeps the **exact song order**
✔ Handles **any playlist size** (100 → 5000 tracks)
✔ Rate-limit protection to avoid API errors
✔ Logs missing or conflicting tracks
✔ Batch mode transfers **multiple playlists automatically**
✔ Works on Windows, Linux, and macOS

---

# 🧰 Requirements

You need:

* **Python 3.10+**
* A **Spotify Access Token**
* Your YouTube Music **Request Headers** (`headers_auth.json`)
* Installed libraries:

  ```bash
  pip install spotipy ytmusicapi
  ```

---

# 🔑 Step 1 — Get Your Spotify Access Token

1. Open this page:
   [https://developer.spotify.com/console/get-playlist-tracks/](https://developer.spotify.com/console/get-playlist-tracks/)

2. Login with your Spotify account.

3. Scroll down and click **“Get Token”**

4. Check the box:

   ```
   playlist-read-private
   ```

   and click **“Request Token”**

5. Copy the token you receive.

6. Paste it in your script:

```python
SPOTIFY_ACCESS_TOKEN = "YOUR TOKEN HERE"
```

⚠ **Spotify tokens expire after ~1 hour**, so generate a new one whenever needed.

---

# 🎧 Step 2 — Get YouTube Music Headers (`headers_auth.json`)

1. Open [https://music.youtube.com](https://music.youtube.com)

2. Press **F12** → open Developer Tools

3. Go to **Network** tab

4. Refresh the page

5. Click any request starting with:

   ```
   /youtubei/v1
   ```

6. In the **Request Headers**, copy these values:

   * `Authorization`
   * `X-Goog-Visitor-Id`
   * `X-Origin`
   * `Cookie`

7. Create a file named:

   ```
   headers_auth.json
   ```

8. Paste the values into it:

```json
{
  "Authorization": "....",
  "X-Goog-Visitor-Id": "....",
  "X-Origin": "https://music.youtube.com",
  "Cookie": "...."
}
```

---

# 🎵 Step 3 — Single Playlist Transfer

Use this version if you only want to transfer **one** Spotify playlist.

### Edit your settings:

```python
SPOTIFY_ACCESS_TOKEN = "YOUR TOKEN"
SPOTIFY_PLAYLIST_URL = "YOUR SPOTIFY PLAYLIST URL"
YT_HEADERS_FILE = "headers_auth.json"
NEW_PLAYLIST_NAME = "Imported from Spotify"
```

### Run the script:

```bash
python single_transfer.py
```

It will:

* Fetch all Spotify tracks
* Create a new YouTube Music playlist
* Add each song
* Log missing songs in `missing_songs.txt`

---

# 📦 Step 4 — Batch Transfer (Multiple Playlists at Once)

Use this version if you have many playlists and want everything done in **one run**.

### Edit the playlist list:

```python
PLAYLISTS_TO_TRANSFER = [
    ("My Playlist 1", "https://open.spotify.com/playlist/XXXX"),
    ("My Playlist 2", "https://open.spotify.com/playlist/YYYY"),
    ("Anime OST", "https://open.spotify.com/playlist/ZZZZ"),
]
```

### Run the batch script:

```bash
python batch_transfer.py
```

The script will:

* Automatically create each playlist on YouTube Music
* Import every track in order
* Log missing tracks per playlist:

  ```
  missing_songs_My_Playlist_1.txt
  missing_songs_Anime_OST.txt
  ```
* Show success/failure summary

---

# ⚙️ Rate Limit Control

To avoid errors, the script waits between YouTube API calls:

```python
RATE_LIMIT_SLEEP = 0.8
```

Recommended values:

| Playlist Size  | Safe Delay |
| -------------- | ---------- |
| <200 songs     | 0.3s       |
| 200–800 songs  | 0.5s       |
| 800–3000 songs | 0.8s       |
| 3000+ songs    | 1.0s       |

Setting this to `0` may cause:
❌ 429 errors
❌ transfer failing
❌ YouTube blocking requests

---

# 📝 Missing Songs Log

If a track cannot be found or YouTube Music blocks it, it will be written to:

* `missing_songs.txt` (single script)
* `missing_songs_PLAYLIST_NAME.txt` (batch script)

This helps you manually add or replace those tracks later.

---

# 🎉 Done!

You can now transfer any Spotify playlist directly to YouTube Music — automatically, in order, and without data loss.

