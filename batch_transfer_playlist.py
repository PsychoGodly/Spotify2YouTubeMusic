import time
import re
from ytmusicapi import YTMusic
import spotipy

# ---- SETTINGS ----
SPOTIFY_ACCESS_TOKEN = "YOUR SPOTIFY TOKEN"
YT_HEADERS_FILE = "headers_auth.json"
RATE_LIMIT_SLEEP = 0.8   # seconds between YT API calls (recommended for big playlists)
# -------------------

ytmusic = YTMusic(YT_HEADERS_FILE)
sp = spotipy.Spotify(auth=SPOTIFY_ACCESS_TOKEN)

# ---- LIST OF PLAYLISTS ----
# Each playlist: (NEW_PLAYLIST_NAME, SPOTIFY_PLAYLIST_URL)
PLAYLISTS_TO_TRANSFER = [
    ("PLAYLIST NAME", "https://open.spotify.com/playlist/--------"),
    ("PLAYLIST NAME", "https://open.spotify.com/playlist/--------"),
    ("PLAYLIST NAME", "https://open.spotify.com/playlist/--------"),
    ("PLAYLIST NAME", "https://open.spotify.com/playlist/--------"),
    ("PLAYLIST NAME", "https://open.spotify.com/playlist/--------"),
    ("PLAYLIST NAME", "https://open.spotify.com/playlist/https://open.spotify.com/playlist/--------"),
    ("PLAYLIST NAME", "https://open.spotify.com/playlist/--------"),
    ("PLAYLIST NAME", "https://open.spotify.com/playlist/--------"),
    ("PLAYLIST NAME", "https://open.spotify.com/playlist/--------"),
    ("PLAYLIST NAME", "https://open.spotify.com/playlist/--------")
]
# ---------------------------

def search_track(name, artist):
    """Try multiple search patterns with fallback priority."""
    queries = [
        f"{name} {artist}",
        f"{name} - {artist}",
        f"{artist} {name}",
        name
    ]
    for q in queries:
        results = ytmusic.search(q, filter="songs")
        if results:
            return results[0]["videoId"]
        results = ytmusic.search(q, filter="videos")
        if results:
            return results[0]["videoId"]
    return None

def fetch_spotify_tracks(playlist_url):
    """Fetch all tracks from a Spotify playlist (handles pagination)."""
    match = re.search(r"playlist/([A-Za-z0-9]+)", playlist_url)
    playlist_id = match.group(1)
    tracks = []
    results = sp.playlist_tracks(playlist_id, limit=100)
    tracks.extend(results["items"])
    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])
    return tracks

# ---- MAIN BATCH LOOP ----
for playlist_name, playlist_url in PLAYLISTS_TO_TRANSFER:
    print(f"\n==============================")
    print(f"Transferring playlist: {playlist_name}")
    print(f"Spotify URL: {playlist_url}")
    print(f"==============================\n")

    tracks = fetch_spotify_tracks(playlist_url)
    print(f"Found {len(tracks)} tracks in Spotify playlist.")

    # Create YouTube Music playlist
    yt_playlist_id = ytmusic.create_playlist(
        playlist_name,
        ""
    )
    print(f"Created YouTube Music playlist: {yt_playlist_id}\n")

    missing_log = open(f"missing_songs_{playlist_name.replace(' ','_')}.txt", "w", encoding="utf-8")
    success_count = 0
    fail_count = 0

    for index, item in enumerate(tracks, start=1):
        track = item["track"]
        if track is None:
            continue
        name = track["name"]
        artist = track["artists"][0]["name"]

        print(f"[{index}/{len(tracks)}] Searching: {name} by {artist}")
        video_id = search_track(name, artist)

        if not video_id:
            print(f"❌ Not found: {name} - {artist}\n")
            missing_log.write(f"{name} - {artist}\n")
            fail_count += 1
            continue

        try:
            ytmusic.add_playlist_items(yt_playlist_id, [video_id])
            success_count += 1
            print(f"✔ Added: {name} by {artist}\n")
        except Exception as e:
            print(f"⚠️ Conflict/Skip: {name} by {artist}")
            missing_log.write(f"(Conflict) {name} - {artist}\n")
            fail_count += 1
            print("Reason:", e, "\n")

        time.sleep(RATE_LIMIT_SLEEP)

    missing_log.close()

    print("\n----------------------")
    print(f"Finished playlist: {playlist_name}")
    print(f"Total tracks:     {len(tracks)}")
    print(f"Successfully added: {success_count}")
    print(f"Failed to add:      {fail_count}")
    print(f"Missing songs logged in: missing_songs_{playlist_name.replace(' ','_')}.txt")
    print("----------------------\n")

print("🎉 ALL PLAYLISTS TRANSFERRED!")
