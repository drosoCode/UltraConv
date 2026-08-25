import requests
import subprocess
import sys
import os

def get_ffmpeg_path():
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, "ffmpeg.exe")
    else:
        # Find ffmpeg.exe in PATH
        ffmpeg_name = "ffmpeg.exe" if os.name == "nt" else "ffmpeg"
        for path_dir in os.environ.get("PATH", "").split(os.pathsep):
            candidate = os.path.join(path_dir, ffmpeg_name)
            if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                return candidate
        return "ffmpeg"


def download_file(url: str, out_file: str, req_client=requests):
    with req_client.get(url, stream=True) as r:
        r.raise_for_status()
        with open(out_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return out_file

def ffmpeg_convert(src_path, dst_path):
    subprocess.run([get_ffmpeg_path(), "-hide_banner", "-loglevel", "error", "-y", "-i", src_path, dst_path])

def ffmpeg_merge_convert(src_paths, dst_path):
    # ffmpeg -i input0.mp3 -i input1.mp3 -filter_complex amerge=inputs=2 -ac 2 output.mp3
    cmd = [get_ffmpeg_path(), "-hide_banner", "-loglevel", "error", "-y"]
    for src in src_paths:
        cmd.extend(["-i", src])
    cmd.extend(["-filter_complex", f"amerge=inputs={len(src_paths)}", "-ac", "2", dst_path])
    subprocess.run(cmd)

def get_yass_path():
    # TODO: do real detection instead of hardcoding
    return "C:\\Program Files (x86)\\Yass Along\\yass.exe"

