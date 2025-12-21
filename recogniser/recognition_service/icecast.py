import requests
from typing import Optional

from .config import Config
from .models.track import Track


class Icecast:
    def __init__(self, config: Config):
        self.config = config

    def update_metadata(self, track: Optional[Track]):
        try:
            song = str(track) if track else ""
            url = self.config.icecast_admin_url + song
            requests.get(url, auth=self.config.icecast_auth, timeout=5)
        except Exception as e:
            print(f"Icecast update error: {e}")
