import requests
from typing import List
from ultraconv.models import SearchSong, AbstractSource, SourceInfo, SourceType, UltrastarFile
from ultraconv.converters import LrcConverter
import os

class LrcLibSource(AbstractSource):
    API_ENDPOINT = "https://lrclib.net/api"

    def __init__(self, config: dict):
        super().__init__(config)

    def search(self, search_term: str, nb_results: int=-1) -> List[SearchSong]:
        resp = requests.get(f"{self.API_ENDPOINT}/search", params={"q": search_term})
        if resp.status_code != 200:
            raise Exception(f"Error: Received status code {resp.status_code}: {resp.text}")

        ret = []
        for track in resp.json():
            if track.get("syncedLyrics"):
                ret.append(SearchSong(
                    id=track["id"],
                    track=track['trackName'],
                    artist=track['artistName'],
                    duration=round(track.get('duration', 1)/60,2),
                    year=-1,
                    data={}
                ))
        return ret

    def download(self, song: SearchSong, types: list[SourceType], uf: UltrastarFile) -> UltrastarFile:
        tmp_dir = uf.get_tmp_dir()

        for t in types:
            if t == SourceType.LYRICS:
                resp = requests.get(f"{self.API_ENDPOINT}/get/{song.id}")
                if resp.status_code != 200:
                    raise Exception(f"Error: Received status code {resp.status_code}: {resp.text}")
                lyrics_data = resp.json()
                lrc = lyrics_data.get("syncedLyrics")
                if lrc:
                    lrc_path = os.path.join(tmp_dir, "lyrics.lrc")
                    with open(lrc_path, "w", encoding="utf-8") as f:
                        f.write(lrc)
                    uf = LrcConverter(bpm=400).convert(lrc_path, uf)
                else:
                    print("No synced lyrics found.")
            elif t == SourceType.METADATA:
                uf.tags['TITLE'] = song.track
                uf.tags['ARTIST'] = song.artist

    def get_info(self) -> SourceInfo:
        return SourceInfo(
            name="LrcLib",
            description="Download lyrics from lrclib.net",
            supported_types=[
                SourceType.LYRICS,
                SourceType.METADATA,
            ]
        )

    @staticmethod
    def is_available():
        return True
