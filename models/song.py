from dataclasses import dataclass
from enum import Enum

@dataclass
class SearchSong:
    id: str
    track: str
    artist: str
    year: int
    duration: int
    data: dict

    def __init__(self, id, track, artist, year, duration, data):
        self.id = id
        self.track = track
        self.artist = artist
        self.year = year
        self.duration = duration
        self.data = data
