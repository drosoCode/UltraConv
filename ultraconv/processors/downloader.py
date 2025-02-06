import requests
import subprocess

def download_file(url: str, out_file: str):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(out_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return out_file

def ffmpeg_convert(src_path, dst_path):
    subprocess.run(["ffmpeg", "-i", src_path, dst_path])
