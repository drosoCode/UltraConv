import requests
import uuid
import random
from datetime import datetime
import json
from typing import List

from ultraconv.models import SearchSong

class MusixMatchSource:

    def __init__(self, email: str, password: str):
        if MusixMatchSource.client is None:
            MusixMatchSource.client = MusixmatchAPI(email=email, password=password)
            #MusixMatchSource.languages = MusixMatchSource.client.get_languages()
        self.mx = MusixMatchSource.client

    def search_songs(self, search_term: str, nb_results=-1) -> List[SearchSong]:
        resp = self.mx.search_tracks(search_term)
        
        ret = []
        for track in resp:
            ret.append(SearchSong(
                id=track["commontrack_vanity_id"],
                track=track["track_name"],
                artist=track["artist_name"],
                duration=round(track.get("track_length", 1)/60, 2),
                year=-1,
                data={}
            ))
        return ret

    def download_lyrics(self, song: SearchSong) -> List[str]:
        resp = self.mx.get_lyrics(song.id)
        if resp["richsync_lyrics"]:
            ass = resp["richsync_lyrics"]
        else:
            lrc = resp["xml_lyrics"]




class MusixmatchAPI:
    APP_ID = "android-player-v1.0"
    HEADERS = {
        "User-Agent": "okhttp/4.12.0",
        "Accept": "application/json",
        "x-mxm-app-version": "1.37.2"
    }
    
    def __init__(self, email: str=None, password: str=None, token=None):
        self._token = token
        if not self._token:
            self._token = self.get_user_token()
            self.login_token(email, password)

    def get_user_token(self):
        # Generate random parameters
        random_adv_id = str(uuid.uuid4())
        random_guid = ''.join(random.choices('0123456789abcdef', k=16))
        random_build = f"2025{random.randint(1,12):02d}{random.randint(1,31):02d}{random.randint(1,99):02d}"
        random_lang = random.choice(["en_US", "fr_FR", "es_ES", "de_DE", "it_IT", "pt_BR", "ja_JP", "ko_KR"])
        manufacturers = ["Samsung", "Xiaomi", "OnePlus", "Google", "Huawei", "Sony", "LG"]
        models = ["Galaxy S21", "Mi 11", "OnePlus 9", "Pixel 6", "P40 Pro", "Xperia 1", "V60"]
        random_manufacturer = random.choice(manufacturers)
        random_model = random.choice(models)

        params = {
            "adv_id": random_adv_id,
            "root": str(random.randint(0, 1)),
            "sideloaded": str(random.randint(0, 1)),
            "app_id": self.APP_ID,
            "build_number": random_build,
            "guid": random_guid,
            "lang": random_lang,
            "model": f"manufacturer/{random_manufacturer} brand/{random_manufacturer} model/{random_model}",
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "format": "json"
        }
        tok_req = requests.get("https://apic-appmobile.musixmatch.com/ws/1.1/token.get", params=params, headers=self.HEADERS)
        if tok_req.status_code != 200:
            raise Exception(f"Error: Received status code {tok_req.status_code}: {tok_req.text}")
        return tok_req.json()["message"]["body"]["user_token"]

    def login_token(self, email, password):
        params = {
            "app_id": self.APP_ID,
            "usertoken": self._token,
            "format": "json"
        }
        data = {
            "credential_list": [
                {
                    "credential": {
                        "type": "mxm",
                        "action": "login",
                        "email": email,
                        "password": password
                    }
                }
            ]
        }
        login_req = requests.post("https://apic-appmobile.musixmatch.com/ws/1.1/credential.post", params=params, data=json.dumps(data), headers=self.HEADERS)
        if login_req.status_code != 200:
            raise Exception(f"Error: Received status code {login_req.status_code}: {login_req.text}")
        
        return login_req.json()["message"]["body"][0]["credential"]["account"]["user_id"]

    def get_languages(self):
        params = {
            "app_id": self.APP_ID,
            "get_romanized_info": "1",
            "usertoken": self._token,
            "format": "json"
        }
        lang_req = requests.get("https://apic-appmobile.musixmatch.com/ws/1.1/languages.get", params=params, headers=self.HEADERS)
        if lang_req.status_code != 200:
            raise Exception(f"Error: Received status code {lang_req.status_code}: {lang_req.text}")
        
        language_map = {}
        for lang in lang_req.json()["message"]["body"]["language_list"]:
            language_map[lang["language"]["language_iso_code_1"]] = lang["language"]["language_name"]

        return language_map

    def search_tracks(self, query):
        params = {
            "app_id": self.APP_ID,
            "usertoken": self._token,
            "query": query,
        }
        search_req = requests.get("https://apic-appmobile.musixmatch.com/ws/1.1/community/opensearch/tracks", params=params, headers=self.HEADERS)
        if search_req.status_code != 200:
            raise Exception(f"Error: Received status code {search_req.status_code}: {search_req.text}")
        
        print(search_req.json())
        return search_req.json()["data"]["tracks"]

    def get_lyrics(self, track_id):
        parts = [
            "lyrics_crowd",
            "track_lyrics_translation_status",
        ]
        params = {
            "tag": "playing",
            "f_subtitle_length_max_deviation": "1",
            "subtitle_format": "dfxp",
            "page_size": "1",
            "questions_id_list": "",
            "optional_calls": "track.richsync", 
            "commontrack_vanity_id": track_id,
            "usertoken": self._token,
            "app_id": self.APP_ID,
            "country": "",
            "part": ",".join(parts),
            "language_iso_code": "1",
            "format": "json",
        }
        
        lyrics_req = requests.get("https://apic-appmobile.musixmatch.com/ws/1.1/macro.subtitles.get", params=params, headers=self.HEADERS)
        if lyrics_req.status_code != 200:
            raise Exception(f"Error: Received status code {lyrics_req.status_code}: {lyrics_req.text}")

        data = lyrics_req.json()
        xml_lyrics = None
        richsync_lyrics = None
        track_id = None
        translations = []

        try:
            xml_lyrics = data["message"]["body"]["macro_calls"]["track.subtitles.get"]["message"]["body"]["subtitle_list"][0]["subtitle"]["subtitle_body"]
        except KeyError:
            pass
        try:
            richsync_lyrics = data["message"]["body"]["macro_calls"]["track.richsync.get"]["message"]["body"]["richsync"]["richsync_body"]
        except KeyError:
            pass
        try:
            track_id = data["message"]["body"]["macro_calls"]["matcher.track.get"]["message"]["body"]["track"]["track_id"]
            for tr in data["message"]["body"]["macro_calls"]["matcher.track.get"]["message"]["body"]["track"]["track_lyrics_translation_status"]:
                if tr["perc"] == 1:
                    translations.append(tr["to"])
        except KeyError:
            pass

        return {
            "xml_lyrics": xml_lyrics,       
            "richsync_lyrics": richsync_lyrics,
            "translations": translations,
            "track_id": track_id
        }

    def get_translation(self, track_id, to_lang):
        params = {
            "translation_fields_set": "minimal",
            "selected_language": to_lang,
            #"track_id": track_id,
            "comment_format": "text",
            "part": "user",
            "commontrack_vanity_id": track_id,
            "format": "json",
            "usertoken": self._token,
            "app_id": self.APP_ID,
            "tag": "playing"
        }
        
        translation_req = requests.get("https://apic-appmobile.musixmatch.com/ws/1.1/crowd.track.translations.get", params=params, headers=self.HEADERS)
        if translation_req.status_code != 200:
            raise Exception(f"Error: Received status code {translation_req.status_code}: {translation_req.text}")

        data = translation_req.json()
        translation_map = {}
        for tr in data["message"]["body"]["translations_list"]:
            if tr["translation"]["type_id"] == "track_translation":
                # subtitle_matched_line or matched_line ?
                translation_map[tr["translation"]["subtitle_matched_line"]] = tr["translation"]["description"]
        return translation_map


    # token = get_user_token()
    #print(login_token(token, "email", "password"))
    #print(get_languages(token))
    #print(search_tracks(token, "Stray kids chk"))
    #print(get_lyrics(token, "Stray-Kids/Chk-Chk-Boom"))
    #print(get_translation(token, "Stray-Kids/Chk-Chk-Boom", "rk"))
