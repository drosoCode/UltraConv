# UltraConv

This is a tool to make the process of creating ultrastar files easier.

Features:
- Download Videos and Lyrics from various sources (youtube with [yt-dlp](https://github.com/yt-dlp/yt-dlp), kara.moe with their [API](https://api.karaokes.moe/server) and MusixMatch with [syncedlyrics](https://github.com/moehmeni/syncedlyrics))
- Convert videos and audio to ultrastar-supported formats (using [ffmpeg](https://github.com/yt-dlp/FFmpeg-Builds))
- Convert lrc and ass lyrics files to ultrastar txt format
- Split audio in instrumental and voice tracks (using [demucs](https://github.com/facebookresearch/demucs))
- Automatically pitch the file (using [ultrastar_pitch](https://github.com/paradigmn/ultrastar_pitch))

## Usage (Windows)

Download the zip file in the [releases]() tab, extract it and run `ultraconv.exe` (please keep `ffmpeg.exe` and `ultraconv.exe` in the same folder).

## Usage (other OS) and developement

Prerequisites:
- Install Python (this was tested on Python 3.13)
- Create a virutal env and activate it (ex: `python -m venv .venv`, `.venv\Scripts\Activate.ps1`)
- Install dependencies: `pip install -r requirements.txt`

You can then directly run the program with `python main.py`

To make a single file executable, use pyinstaller (`pip install pyinstaller`): `pyinstaller --onefile main.py --name ultraconv --collect-all sv_ttk --collect-all demucs --collect-all numpy --add-binary .\.venv\Lib\site-packages\ultrastar_pitch\binaries\pitchnet_2020_12_14.onnx:. --add-binary .\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe:.`

## Screenshots

