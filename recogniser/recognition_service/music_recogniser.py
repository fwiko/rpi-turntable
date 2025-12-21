from shazamio import Shazam
from typing import Optional

from .models.track import Track


class MusicRecogniser:
    def __init__(self):
        self.shazam = Shazam()

    async def recognise(self, file_path: str) -> Optional[Track]:
        try:
            result = await self.shazam.recognize(file_path)

            if not result:
                return None

            track_data = result.get("track")
            if not track_data:
                return None

            artist = track_data.get("subtitle")
            title = track_data.get("title")
            duration_ms = track_data.get("duration_ms")

            if not artist or not title:
                return None

            duration_seconds = duration_ms / 1000 if duration_ms else None

            return Track(artist=artist, title=title, duration_seconds=duration_seconds)

        except Exception as e:
            print(f"Recognition error: {e}")
            return None
