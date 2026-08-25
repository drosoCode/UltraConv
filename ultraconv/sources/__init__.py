from ultraconv.sources.karamoe import KaramoeSource
from ultraconv.sources.lrclib import LrcLibSource
from ultraconv.sources.musixmatch import MusixMatchSource
from ultraconv.sources.youtubedl import YoutubeDLSource
from ultraconv.sources.karafun import KarafunSource

SOURCES = [LrcLibSource, KaramoeSource, KarafunSource, MusixMatchSource, YoutubeDLSource]

def get_available_sources():
    lst = []
    for source in SOURCES:
        if source.is_available():
            lst.append(source)
    return lst
