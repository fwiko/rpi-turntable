import os
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Config:
    icecast_admin_url: str = (
        "http://icecast:8000/admin/metadata?mount=/live.mp3&mode=updinfo&song="
    )
    icecast_auth: Tuple[str, str] = ("admin", "admin")
    audio_dir: str = "/audio"

    lastfm_api_key: str = os.getenv("LASTFM_API_KEY", "")
    lastfm_api_secret: str = os.getenv("LASTFM_API_SECRET", "")
    lastfm_session_key: str = os.getenv("LASTFM_SESSION_KEY", "")

    min_file_size: int = 200_000
    max_snippets: int = 5
    process_interval: int = 12
    min_file_age: int = 3
    silence_rms_threshold: int = 500

    min_play_seconds: int = 30
    max_scrobble_seconds: int = 240
    debounce_required: int = 2

    @property
    def lastfm_enabled(self) -> bool:
        return all(
            [self.lastfm_api_key, self.lastfm_api_secret, self.lastfm_session_key]
        )
