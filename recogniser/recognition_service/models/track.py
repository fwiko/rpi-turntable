from dataclasses import dataclass
from typing import Optional


@dataclass
class Track:
    artist: str
    title: str
    duration_seconds: Optional[float] = None

    def __eq__(self, other):
        if not isinstance(other, Track):
            return False

        return self.artist == other.artist and self.title == other.title

    def __hash__(self):
        return hash((self.artist, self.title))

    def __str__(self):
        return f"{self.artist} - {self.title}"
