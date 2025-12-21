import time

from dataclasses import dataclass
from typing import Optional
from .track import Track


@dataclass
class State:
    current_track: Optional[Track] = None
    start_time: Optional[float] = None
    scrobbled: bool = False
    silent_count: int = 0
    last_detected: Optional[Track] = None
    detect_count: int = 0

    def reset(self):
        self.current_track = None
        self.start_time = None
        self.scrobbled = False

    def get_play_time(self) -> float:
        if self.start_time is None:
            return 0

        return time.time() - self.start_time
