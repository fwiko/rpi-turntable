import os
import audioop
import wave
import time
from pathlib import Path
from typing import List

from .config import Config


class AudioProcessor:
    def __init__(self, config: Config):
        self.config = config

    def is_silent(self, path: str) -> bool:
        try:
            with wave.open(path, "rb") as wf:
                frames = wf.readframes(wf.getnframes())
                rms = audioop.rms(frames, wf.getsampwidth())
                return rms < self.config.silence_rms_threshold
        except Exception as e:
            print(f"Error checking silence: {e}")
            return True

    def get_audio_files(self) -> List[str]:
        audio_dir = Path(self.config.audio_dir)
        if not audio_dir.exists():
            return []

        files = sorted(
            str(audio_dir / f)
            for f in os.listdir(self.config.audio_dir)
            if f.endswith(".wav")
        )
        return files

    def cleanup_old_files(self, files: List[str]):
        while len(files) > self.config.max_snippets:
            try:
                os.remove(files.pop(0))
            except FileNotFoundError:
                pass

    def is_file_ready(self, path: str) -> bool:
        if not os.path.exists(path):
            return False

        if time.time() - os.path.getmtime(path) < self.config.min_file_age:
            return False

        if os.path.getsize(path) < self.config.min_file_size:
            return False

        return True
