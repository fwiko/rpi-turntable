import pylast

from .config import Config
from .models.track import Track


class LastFm:
    def __init__(self, config: Config):
        self.config = config
        self.network = pylast.LastFMNetwork(
            api_key=config.lastfm_api_key,
            api_secret=config.lastfm_api_secret,
            session_key=config.lastfm_session_key,
        )

    def update_now_playing(self, track: Track):
        try:
            self.network.update_now_playing(
                artist=track.artist,
                title=track.title,
            )
        except Exception as e:
            print(f"Error setting Last.fm now playing: {e}")

    def scrobble(self, track: Track, timestamp: float):
        try:
            self.network.scrobble(
                artist=track.artist,
                title=track.title,
                timestamp=int(timestamp),
            )
            print(f"Scrobbled: {track}")
        except Exception as e:
            print(f"Last.fm scrobble error: {e}")

    def calculate_scrobble_threshold(self, track: Track, config: Config) -> float:
        if track.duration_seconds:
            # Scrobble at 50% of track duration or max scrobble seconds
            return min(track.duration_seconds * 0.5, config.max_scrobble_seconds)
        return config.min_play_seconds
