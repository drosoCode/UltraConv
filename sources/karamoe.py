import os
import requests
from models.song import SearchSong
from processors.downloader import download_file
from typing import List

API_ENDPOINT = "https://kara.moe/api"
CDN_ENDPOINT = "https://kara.moe/downloads"
COLLECTIONS = "c7db86a0-ff64-4044-9be4-66dd1ef1d1c1,dbcf2c22-524d-4708-99bb-601703633927,f2462778-f986-4844-a4b8-e1d3ccdb861b,efe171c0-e8a1-4d03-98c0-60ecf741ad52"

class KaramoeSource:
    def __init__(self):
        pass

    def search_songs(self, search: str, nb_results: int=-1) -> List[SearchSong]:
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

    def download_lyrics(self, song: SearchSong) -> List[str]:
        return requests.get(f"{CDN_ENDPOINT}/lyrics/{song.data['lyricsfile']}").text.split("\n")

    def download_video(self, song: SearchSong, path: str):
        download_file(f"{CDN_ENDPOINT}/medias/{song.data['mediafile']}", os.path.join(path, "video.mp4"))
        return os.path.join(path, "video.mp4")

