import asyncio
import time

from .config import Config
from .audio_processor import AudioProcessor
from .music_recogniser import MusicRecogniser
from .icecast import Icecast
from .lastfm import LastFm
from .models.state import State
from .models.track import Track


class RecognitionService:
    def __init__(self, config: Config):
        self.config = config
        self.audio_processor = AudioProcessor(config)
        self.recogniser = MusicRecogniser()
        self.icecast = Icecast(config)
        self.lastfm = LastFm(config)
        self.state = State()

    async def run_blocking(self, func, *args):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, func, *args)

    def handle_silence(self):
        """Handle silent audio detection."""
        self.state.silent_count += 1

        if self.state.silent_count >= 3:
            self.icecast.update_metadata(None)
            self.state.reset()

    def handle_track_detection(self, track: Track):
        if track == self.state.last_detected:
            self.state.detect_count += 1
        else:
            self.state.last_detected = track
            self.state.detect_count = 1

        return self.state.detect_count >= self.config.debounce_required

    async def handle_new_track(self, track: Track):
        await self.run_blocking(self.icecast.update_metadata, track)

        if self.config.lastfm_enabled:
            await self.run_blocking(self.lastfm.update_now_playing, track)

        self.state.current_track = track
        self.state.start_time = time.time()
        self.state.scrobbled = False

        print(f"Now playing: {track}")

    async def check_scrobble(self):
        if (
            not self.config.lastfm_enabled
            or not self.state.current_track
            or self.state.scrobbled
        ):
            return

        play_time = self.state.get_play_time()
        threshold = self.lastfm.calculate_scrobble_threshold(
            self.state.current_track, self.config
        )

        if play_time >= threshold:
            await self.run_blocking(
                self.lastfm.scrobble,
                self.state.current_track,
                self.state.start_time,
            )
            self.state.scrobbled = True

    async def process_audio_file(self, file_path: str) -> bool:
        if self.audio_processor.is_silent(file_path):
            self.handle_silence()
            return False

        self.state.silent_count = 0

        track = await self.recogniser.recognise(file_path)
        if not track:
            return False

        if not self.handle_track_detection(track):
            return False

        if track != self.state.current_track:
            await self.handle_new_track(track)

        await self.check_scrobble()

        return True

    async def run(self):
        while True:
            try:
                files = self.audio_processor.get_audio_files()

                if len(files) < 2:
                    await asyncio.sleep(1)
                    continue

                candidate = files[-2]

                if not self.audio_processor.is_file_ready(candidate):
                    await asyncio.sleep(1)
                    continue

                await self.process_audio_file(candidate)

                self.audio_processor.cleanup_old_files(files)

            except Exception as e:
                print(f"Error in main loop: {e}")

            await asyncio.sleep(self.config.process_interval)
