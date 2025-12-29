import xml.etree.ElementTree as ET
import os
import requests
import json
import hashlib
import time

from ultraconv.processors.utils import download_file, ffmpeg_convert

class KarafunAPI:

    VERSION = "3.10.7.135"
    API_KEY = "zS@nfy_j"
    HASH_VERSION = "kfun-v1.5"

    HEADERS = {
        "Origin": "https://www.karafun.fr",
        "Referer": "https://www.karafun.fr/web/discover/",
        "User-Agent": "Mozilla/5.0 Firefox/146.0",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept": "*/*"
    }

    def __init__(self):
        self.session = requests.Session()
        self.session_key = None

    def hash_password(self, password):
        char_map = {
            'a': '9', 'b': 'N', 'c': 'p', 'd': 'W', 'e': 'X', 'f': 'k', 'g': 'j', 'h': 'L',
            'i': 'K', 'j': 'I', 'k': 'u', 'l': 'z', 'm': '2', 'n': 'Z', 'o': 'x', 'p': 'y',
            'q': 'H', 'r': 'V', 's': 'Y', 't': 'q', 'u': 'c', 'v': '3', 'w': 'v', 'x': 'd',
            'y': 'M', 'z': 'A', 'A': 'g', 'B': '7', 'C': '6', 'D': 'U', 'E': 'J', 'F': 'a',
            'G': 'S', 'H': 'Q', 'I': 'F', 'J': '8', 'K': '0', 'L': 't', 'M': 'o', 'N': '1',
            'O': 'h', 'P': 'i', 'Q': 'D', 'R': 'm', 'S': 'R', 'T': 'E', 'U': 'w', 'V': 's',
            'W': 'l', 'X': 'e', 'Y': 'P', 'Z': 'n', '0': '5', '1': 'r', '2': 'f', '3': 'O',
            '4': 'T', '5': 'G', '6': 'C', '7': 'B', '8': '4', '9': 'b'
        }
        substituted = ''.join(char_map.get(char, char) for char in password)
        return hashlib.md5(substituted.encode('utf-8')).hexdigest()
    
    def make_request(self, method, url, query=None, data=None) -> str:
        headers = {**self.HEADERS}

        # Create a prepared request to get the full URL with encoded params
        req = requests.Request(
            method=method,
            url=url,
            params=query,
            data=data,
            headers=headers
        )
        prepared_req = req.prepare()

        # compute request hash
        timestamp = int(time.time())
        #timestamp = 1766979748
        # Build the string to hash: version|url|payload|timestamp|sessionKey
        parts = [
            self.HASH_VERSION,
            prepared_req.url,
            prepared_req.body, 
            timestamp,
            self.session_key
        ]
        
        # Filter out None/empty values and join with "|"
        hash_string = "|".join(str(part) for part in parts if part is not None and part != "")
        # Calculate SHA-256 hash
        request_hash = hashlib.sha256(hash_string.encode('utf-8')).hexdigest()

        # Add signature headers to prepared request
        prepared_req.headers['x-request-signature'] = request_hash
        prepared_req.headers['x-request-timestamp'] = str(timestamp)

        # Send the prepared request
        #response = self.session.send(prepared_req)
        response = self.session.send(prepared_req)
        if response.status_code != 200:
            raise Exception(f"error: {response.status_code}: {response.text}")
        return response.text

    def login(self, username: str, password: str):
        data = {
            "backurl": "/web/",
            "frm_login": username,
            "frm_password": password,
            "sbm_signin": "Se+connecter",
            "connect_auto": "1"
        }
        login_req = self.session.post("https://www.karafun.fr/my/loginv.html", data=json.dumps(data), headers=self.HEADERS)
        if login_req.status_code >= 400 or "Set-Cookie" not in login_req.headers:
            raise Exception(f"Login failed: {login_req.status_code}: {login_req.text}")

        params = {
            'client': '7',
            'client_version': self.VERSION,
            'key': self.API_KEY,
            'protocol': '1',
            'login': username,
            'pwd': self.hash_password(password),
            'device_name': 'Firefox 146.0',
            'os': 'Web'
        }
        session_req = self.session.get("https://www.karafun.fr/api/session/open.php", params=params, headers=self.HEADERS)
        if session_req.status_code != 200:
            raise Exception(f"error: {session_req.status_code}: {session_req.text}")
        
        self.session_key = ET.fromstring(session_req.text).find('./session/key').text

        return self.session_key

    def download_kit(self, song_id: str, output_path: str):
        params = {
            'song': song_id,
            'offline': '0',
            'sk': self.session_key  # session key ?
        }
        resp = self.make_request("GET", "https://www.karafun.fr/api/song/request.php", query=params)
        file_url = ET.fromstring(resp).find('./song/stream').text
        download_file(file_url, output_path, req_client=self.session)

    def search_song(self, query: str):
        params = {
            'query': requests.utils.quote(query),
            'offset': '0',
            'sk': self.session_key,
        }
        id_list = self.make_request("GET", "https://www.karafun.fr/api/search/top.php", query=params)
        lst = []
        for song in ET.fromstring(id_list).findall('./list/song'):
            lst.append(song.get('id'))

        content_list = self.make_request("POST", "https://www.karafun.fr/api/song/info.php", query={'sk': self.session_key}, data={"song": ",".join(lst)})

        json_resp = []
        for song in ET.fromstring(content_list).findall('./song'):
            json_resp.append({
                'id': song.get('id'),
                'title': song.find('title').text,
                'artist': song.find('artist').text,
                'year': song.find('year').text,
                'duration': song.get('len'),
            })
        return json_resp


    def extract_kit(self, path, out_dir):
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        with open(path, 'rb') as f:
            file_data = f.read()
        
        magic = file_data[:3]
        if magic != b'\x01\xce\xd7':
            raise ValueError("Invalid file format")
        
        nb_files = file_data[3]
        print(f"Number of files: {nb_files}")

        def write_file(id, out_path):
            with open(out_path, 'wb') as out_f:
                start_offset = 4 + nb_files * 5 # header + file table
                while start_offset < len(file_data):
                    file_id = int.from_bytes(file_data[start_offset:start_offset+1], 'big')
                    file_size = int.from_bytes(file_data[start_offset+2:start_offset+5], 'big')
                    start_offset += 9 # 1 byte for file type, 1 bytes for id, 1 null, 3 bytes for size, 4 null bytes
                    if file_id == id:
                        out_f.write(file_data[start_offset:start_offset+file_size])
                    start_offset += file_size
    
        # first file is the XML file
        xml_path = os.path.join(out_dir, 'output.xml')
        write_file(1, xml_path)

        # read xml to fine the name and type of other files
        xmldoc = ET.parse(xml_path)
        files = xmldoc.getroot().findall('./files/file')
        for f in files:
            id = int(f.get('index'))
            if id != 1:
                out_path = os.path.join(out_dir, f.get('label'))
                write_file(id, out_path)
