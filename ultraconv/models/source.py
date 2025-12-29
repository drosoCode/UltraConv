from abc import ABC
from enum import Enum
from voluptuous import Schema
from dataclasses import dataclass

from .ultrastar import UltrastarFile

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

class SourceType(Enum):
    LYRICS = "lyrics"
    AUDIO = "audio"
    VOICE_AUDIO = "voice_audio"
    INSTRUMENTAL_AUDIO = "instrumental_audio"
    VIDEO = "video"
    METADATA = "metadata" # = title, artist, year

@dataclass
class SourceInfo:
    name: str
    description: str
    supported_types: list[SourceType]

class AbstractSource(ABC):

    def __init__(self, config: dict):
        self._config = config

    def search(self, query: str, nb_results: int=-1) -> list[SearchSong]:
        raise NotImplementedError("Subclasses must implement this method")

    def download(self, item: SearchSong, types: list[SourceType], uf: UltrastarFile) -> UltrastarFile:
        raise NotImplementedError("Subclasses must implement this method")
    
    @staticmethod
    def is_available():
        """Check if the source is available. (check dependencies, etc.)"""
        return False
    
    @staticmethod
    def get_info() -> SourceInfo:
        """Return the info of the source."""
        raise NotImplementedError("Subclasses must implement this method")

    @staticmethod
    def get_options() -> Schema:
        """Return the configuration options for this source (ex: auth)."""
        return Schema({})
