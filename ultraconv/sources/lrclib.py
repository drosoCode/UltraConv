import requests
from typing import List
from ultraconv.models import SearchSong

class LrcLibSource:
    API_ENDPOINT = "https://lrclib.net/api"

    def search_songs(self, search_term: str, nb_results: int=-1) -> List[SearchSong]:
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

    def download_lyrics(self, song: SearchSong) -> List[str]:
        resp = requests.get(f"{self.API_ENDPOINT}/get/{song.id}")
        if resp.status_code != 200:
            raise Exception(f"Error: Received status code {resp.status_code}: {resp.text}")
        lyrics_data = resp.json()
        lrc = lyrics_data.get("syncedLyrics", "").splitlines()
        return lrc
