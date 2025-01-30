import syncedlyrics
from typing import List
from models.song import SearchSong

class MusixMatchSource:
    def __init__(self):
        self._mx = syncedlyrics.Musixmatch(enhanced=True)
        
    def search_songs(self, search: str):
        lrc = syncedlyrics.search(search_term=search, synced_only=True, enhanced=True, providers=["Musixmatch", "lrclib"])
        return lrc

    def search_songs(self, search_term: str, nb_results: int=20) -> List[SearchSong]:
        r = self._mx._get(
            "track.search",
            [
                ("q", search_term),
                ("page_size", str(nb_results)),
                ("page", "1"),
            ],
        )
        status_code = r.json()["message"]["header"]["status_code"]
        if status_code != 200:
            self._mx.logger.warning(f"Got status code {status_code} for {search_term}")
            return []
        body = r.json()["message"]["body"]
        if not isinstance(body, dict):
            return []

        ret = []
        for track in body["track_list"]:
            ret.append(SearchSong(
                id=track["track"]["track_id"],
                track=track['track']['track_name'],
                artist=track['track']['artist_name'],
                duration=-1,
                year=-1,
                data={}
            ))
        return ret

    def download_lyrics(self, song: SearchSong) -> List[str]:
        self._mx = syncedlyrics.Musixmatch(enhanced=True)
        lrc = self._mx.get_lrc_word_by_word(song.id)
        if self._mx.enhanced:
            if lrc and lrc.synced:
                return lrc.to_str(syncedlyrics.TargetType.PREFER_SYNCED).split("\n")
        return self._mx.get_lrc_by_id(song.id).to_str(syncedlyrics.TargetType.PREFER_SYNCED).split("\n")
