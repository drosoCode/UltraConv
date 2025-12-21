from ultraconv.models import UltrastarFile, UltrastarEvent, UltrastarNote, UltrastarBreak, UltrastarText
from data.aneas import forced_alignment
import shutil
import os

shutil.rmtree("gen", ignore_errors=True)
os.makedirs("gen", exist_ok=True)


filename = "Falling in Reverse - Watch the world burn"
#filename = "TSS - Killing Me"

f = UltrastarFile()
dirp = f"../ultrastar_custom/{filename}"
f.read(f"{dirp}/{filename}.txt")

words = []
keys = []
start = f.tags.get("GAP", 0)

for i in range(len(f.events)):
    if isinstance(f.events[i], UltrastarText):
        words.append(f.events[i].text)
        keys.append(i)
    elif isinstance(f.events[i], UltrastarBreak):
        # process words
        timed_words = forced_alignment(f"{dirp}/{f.tags['VOCALS']}", f.to_sec(start), f.to_sec(f.events[i].time), words)
        for j in range(len(timed_words)):
            data = timed_words[j]
            if data is None:
                continue
            ev = f.events[keys[j]]
            ev.time = f.to_beat(data["start_time"])
            ev.length = f.to_beat(data["duration"])
            f.events[keys[j]] = ev
        words = []
        keys = []
        start = f.events[i].time

f.write(f"{dirp}/{filename}-aligned.txt")

"""
New tools to implement:
- Forced alignement with multiple backends (+ automatic language detection)
    - Aeneas
    - Montreal Forced Aligner
    - PyTorch + CTC
"""
