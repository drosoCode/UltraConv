from yt_dlp import YoutubeDL
from models.song import SearchSong
from typing import List
from urllib.parse import urlparse
import os

class YoutubeDLSource:
    # https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#extracting-information
    def __init__(self):
        self._opts = {'format': 'bestaudio+bestvideo', 'noplaylist':'True'}

    def search_songs(self, search: str, nb_results: int=5) -> List[SearchSong]:
        ytdl = YoutubeDL(self._opts)
        videos = None
        try:
            x = urlparse(search)
            if x.netloc != "":
                videos = [ytdl.extract_info(search, download=False)]
        except AttributeError:
            pass

        if videos is None:
            videos = ytdl.extract_info(f"ytsearch{nb_results}:{search}", download=False)['entries']

        ret = []
        for vid in videos:
            ret.append(SearchSong(
                id=vid["original_url"],
                track=vid["title"],
                artist=vid["channel"],
                duration=vid["duration"],
                year=int(vid["upload_date"][0:4]),
                data={}
            ))
        return ret

    def download_video(self, song: SearchSong, path: str):
        self._opts["outtmpl"] = os.path.join(path, "video.webm")
        ytdl = YoutubeDL(self._opts)
        ytdl.download([song.id])
        return os.path.join(path, "video.webm")
