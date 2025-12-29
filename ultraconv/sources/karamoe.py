import os
import requests
from ultraconv.models import SearchSong, AbstractSource, SourceType, SourceInfo, UltrastarFile
from ultraconv.processors import download_file, ffmpeg_convert
from ultraconv.converters import AssConverter
from typing import List

API_ENDPOINT = "https://kara.moe/api"
CDN_ENDPOINT = "https://kara.moe/downloads"
COLLECTIONS = "c7db86a0-ff64-4044-9be4-66dd1ef1d1c1,dbcf2c22-524d-4708-99bb-601703633927,f2462778-f986-4844-a4b8-e1d3ccdb861b,efe171c0-e8a1-4d03-98c0-60ecf741ad52"

class KaramoeSource(AbstractSource):
    def __init__(self, config: dict):
        super().__init__(config)

    def search(self, search: str, nb_results: int=-1) -> List[SearchSong]:
        fromNb = 0
        sizeNb = min(20, nb_results) if nb_results > 0 else 20
        songs = []
        while True:
            data = requests.get(f"{API_ENDPOINT}/karas/search?filter={requests.utils.quote(search)}&from={fromNb}&size={sizeNb}&order=recent&collections={COLLECTIONS}").json()
            if data["infos"]["to"] >= data["infos"]["count"]:
                break
            else:
                fromNb += sizeNb
            songs += data["content"]
            if nb_results > 0 and len(songs) >= nb_results:
                break
        
        songs = songs[0:(min(len(songs), nb_results) if nb_results > 0 else len(songs))]

        ret = []
        for s in songs:
            ret.append(SearchSong(
                id=s["kid"],
                track=list(s["titles"].values())[0],
                year=s["year"],
                artist=", ".join([x["name"] for x in s["singergroups"]]),
                duration=s["duration"],
                data={
                    "mediafile": s["mediafile"],
                    "lyricsfile": s["lyrics_infos"][0]["filename"] 
                }
            ))
        return ret
    
    def download(self, item: SearchSong, types: list[SourceType], uf: UltrastarFile) -> UltrastarFile:
        tmp_dir = uf.get_tmp_dir()
        vid = False
        aud = False
        for t in types:
            if t == SourceType.LYRICS:
                ass_file = os.path.join(tmp_dir, "lyrics.ass")
                ass_data = requests.get(f"{CDN_ENDPOINT}/lyrics/{item.data['lyricsfile']}").text
                with open(ass_file, "w", encoding="utf-8") as f:
                    f.write(ass_data)
                uf = AssConverter(bpm=400).convert(ass_file, uf)
            elif t == SourceType.AUDIO:
                aud = True
            elif t == SourceType.VIDEO:
                vid = True
            elif t == SourceType.METADATA:
                uf.tags["TITLE"] = item.track
                uf.tags["ARTIST"] = item.artist
                uf.tags["YEAR"] = item.year
            
        if vid or aud:
            if vid:
                vid_path = os.path.join(uf.get_dir(), "video.mp4")
                uf.tags["VIDEO"] = "video.mp4"
            else:
                vid_path = os.path.join(tmp_dir, "video.mp4")
            download_file(f"{CDN_ENDPOINT}/medias/{item.data['mediafile']}", vid_path)
        
            if aud:
                ffmpeg_convert(vid_path, os.path.join(uf.get_dir(), "audio.mp3"))
                uf.tags["MP3"] = "audio.mp3"
                uf.tags["AUDIO"] = "audio.mp3"
        return uf

    def get_info(self) -> SourceInfo:
        return SourceInfo(
            name="Karamoe",
            description="Download from karaoke mugen api",
            supported_types=[
                SourceType.LYRICS,
                SourceType.AUDIO,
                SourceType.VIDEO,
                SourceType.METADATA,
            ]
        )

    @staticmethod
    def is_available():
        return True
