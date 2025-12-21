import subprocess
import json
from math import floor, ceil
from ultraconv.processors.downloader import get_ffmpeg_path
import os

from lingua import Language, LanguageDetectorBuilder
languages = [Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.SPANISH, Language.JAPANESE, Language.KOREAN]
detector = LanguageDetectorBuilder.from_languages(*languages).build()

def format_sec(sec):
    # format seconds to mm:ss.milliseconds
    minutes = int(sec // 60)
    seconds = int(sec % 60)
    milliseconds = int((sec - int(sec)) * 1000)
    return f"{minutes:02}:{seconds:02}.{milliseconds:03}"


def forced_alignment(vocals_mp3, start, end, words):
    print(f"Forced alignment from {start} to {end} with words: {words}")
    
    # ffmpeg split vocals_mp3 with start and end
    # Convert milliseconds to seconds for ffmpeg
    audio_path = f"gen/audio_{start}_{end}.mp3"
    print(f"Splitting audio from {start} to {end} seconds")
    if not os.path.exists(audio_path):
        subprocess.run([
            get_ffmpeg_path(),
            "-y",
            "-i", vocals_mp3,
            "-ss", f"00:{format_sec(start)}",
            "-to", f"00:{format_sec(end)}",
            "-c", "copy",
            audio_path
        ])

    # write words to a file
    words_path = f"gen/words_{start}_{end}.txt"
    w = [word.strip() for word in words if word.strip()]  # remove empty words
    with open(words_path, 'w', encoding="utf8") as f:
        f.write("\n".join(w))

    # detect language of the words
    wstr = " ".join(w)
    language = detector.detect_language_of(wstr)
    lang = (language.iso_code_639_1.name).lower()
    print(lang)
    #https://github.com/pemistahl/lingua-py

    # run aeneas forced alignment
    data_path = f"gen/data__{start}_{end}.json"
    subprocess.run([
        "python",
        "-m",
        "aeneas.tools.execute_task",
        audio_path,
        words_path,
        f"task_language={lang}|os_task_file_format=json|is_text_type=plain|preset=w",
        data_path,
        "--presets-word"
    ])

    synced = []
    with open(data_path, 'r') as f:
        data = json.load(f)
        for item in data['fragments']:
            if float(item["end"]) > 0.000:
                synced.append({
                    "start_time": start + float(item['begin']),  
                    "duration": (float(item['end']) - float(item['begin'])),
                })
            else:
                print("Skipping empty fragment")
                synced.append(None)
    print(synced)
    return synced
