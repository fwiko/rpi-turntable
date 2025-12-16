import os
import time
import asyncio
import requests
import wave
import audioop
from shazamio import Shazam

ICECAST_ADMIN_URL = (
    "http://icecast:8000/admin/metadata"
    "?mount=/live.mp3&mode=updinfo&song="
)
ICECAST_AUTH = ("admin", "admin")

AUDIO_DIR = "/audio"

MIN_FILE_SIZE = 200_000 # ~8–10s WAV mono 44.1kHz
MAX_SNIPPETS = 10
PROCESS_INTERVAL = 12
MIN_FILE_AGE = 3
SILENCE_RMS_THRESHOLD = 500 

shazam = Shazam()


def is_silent(path, threshold=SILENCE_RMS_THRESHOLD):
    with wave.open(path, 'rb') as wf:
        frames = wf.readframes(wf.getnframes())
        rms = audioop.rms(frames, wf.getsampwidth())
        return rms < threshold


async def recognise(file_path):
    result = await shazam.recognize(file_path)

    if result is not None:
        return result.get("track", None)


def update_icecast(title, artist):
    song = f"{artist} - {title}"
    requests.get(
        ICECAST_ADMIN_URL + song,
        auth=ICECAST_AUTH,
        timeout=5
    )


def cleanup(files):
    while len(files) > MAX_SNIPPETS:
        oldest = files.pop(0)
        try:
            os.remove(oldest)
        except FileNotFoundError:
            pass


async def main():
    last_song = None

    while True:
        files = sorted(
            os.path.join(AUDIO_DIR, f)
            for f in os.listdir(AUDIO_DIR)
            if f.endswith(".wav")
        )

        if len(files) < 2:
            time.sleep(1)
            continue

        candidate = files[-2] 

        if time.time() - os.path.getmtime(candidate) < MIN_FILE_AGE:
            time.sleep(1)
            continue

        size = os.path.getsize(candidate)
        
        if size < MIN_FILE_SIZE or is_silent(candidate):
            print("Skipping small/silent snippet:", candidate, size)
            cleanup(files)
            time.sleep(PROCESS_INTERVAL)
            continue

        print("Evaluating:", candidate, "size:", size)

        try:
            match = await recognise(candidate)

            if match is not None:
                title = match["title"]
                artist = match["subtitle"]
            else:
                title = artist = "Unknown"
                
            song = f'{title} by {artist}'
            
            if song != last_song:
                update_icecast(title, artist)
                last_song = song

            print("Playing:", song)

        except Exception as e:
            print("Error:", e)

        cleanup(files)
        time.sleep(PROCESS_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
