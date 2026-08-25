from yt_dlp import YoutubeDL
from typing import List
from urllib.parse import urlparse
import os

from ultraconv.models import SearchSong, AbstractSource, SourceType, SourceInfo, UltrastarFile
from ultraconv.processors.utils import get_ffmpeg_path, ffmpeg_convert

class YoutubeDLSource(AbstractSource):
    # https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#extracting-information
    def __init__(self, config: dict):
        super().__init__(config)
        self._opts = {'format': 'bestaudio+bestvideo', 'noplaylist':'True', 'extract_flat':'in_playlist', 'ffmpeg_location': get_ffmpeg_path()}

    def search(self, search: str, nb_results: int=5) -> List[SearchSong]:
        ytdl = YoutubeDL(self._opts)
        videos = None
        try:
            x = urlparse(search)
            if x.netloc != "":
                videos = [ytdl.extract_info(search, download=False)]
        except AttributeError:
            pass

        if videos is None:
            videos = ytdl.extract_info(f"ytsearch{nb_results}:'{search}'", download=False)['entries']

        ret = []
        for vid in videos:
            ret.append(SearchSong(
                id=vid["url"],
                track=vid["title"],
                artist=vid["channel"],
                duration=vid.get("duration"),
                year=(int(vid["upload_date"][0:4]) if "upload_date" in vid else -1),
                data={}
            ))
        return ret

    def download(self, ng: SearchSong, types: list[SourceType], uf: UltrastarFile) -> UltrastarFile:
        tmp_dir = uf.get_tmp_dir()

        vid_path = os.path.join(tmp_dir, "video.webm")
        if os.path.exists(vid_path):
            os.remove(vid_path)
        self._opts["outtmpl"] = vid_path
        ytdl = YoutubeDL(self._opts)
        ytdl.download([ng.id])

        for t in types:
            if t == SourceType.VIDEO:
                ffmpeg_convert(vid_path, os.path.join(uf.get_dir(), "video.mp4"))
                uf.tags["VIDEO"] = "video.mp4"
            elif t == SourceType.AUDIO:
                audio_path = os.path.join(uf.get_dir(), "audio.mp3")
                ffmpeg_convert(vid_path, audio_path)
                uf.tags["AUDIO"] = "audio.mp3"
                uf.tags["MP3"] = "audio.mp3"

    @staticmethod
    def get_info() -> SourceInfo:
        return SourceInfo(
            name="YoutubeDL",
            description="Download videos and audio from YouTube and other sites using yt-dlp",
            supported_types=[
                SourceType.VIDEO,
                SourceType.AUDIO,
            ]
        )

    @staticmethod
    def is_available():
        return True
