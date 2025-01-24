from models.events import UltrastarEvent, UltrastarNote, UltrastarBreak, UltrastarText

from typing import List

class UltrastarFile:
    events: List[UltrastarEvent] = []
    bpm: int = 0
    gap: int = 0
    artist: str = ""
    title: str = ""
    mp3: str = ""

    def __init__(self):
        pass

    def write(self, file_path: str):
        lines = [
            f"#TITLE:{self.title}",
            f"#ARTIST:{self.artist}",
            f"#MP3:{self.mp3}",
            f"#BPM:{self.bpm}",
        ]
        lines.append(f"#GAP:{self.gap}")

        for i in self.events:
            lines.append(i.to_ultrastar())
        lines.append("E")

        with open(file_path, "w+", encoding="utf8") as f:
            f.write("\n".join(lines))

    def read(self, file_path: str):
        with open(file_path, "r", encoding="utf8") as f:
            data = f.readlines()
        
        for l in data:
            if l == "E":
                break
            elif len(l) < 3:
                continue

            if l[0] == "#":
                s = l[1:].split(":")
                value = s[1].strip("\n")
                if len(s) >= 2:
                    if s[0] == "TITLE":
                        self.title = value
                    elif s[0] == "ARTIST":
                        self.artist = value
                    elif s[0] == "MP3":
                        self.mp3 = value
                    elif s[0] == "BPM":
                        self.bpm = int(value)
                    elif s[0] == "GAP":
                        self.gap = int(value)
            
            elif l[0] == "-":
                self.events.append(UltrastarBreak(int(l[2:])))

            elif l[0] != " " and l[1] == " ":
                s = l.split(" ")
                if len(s) >= 5:
                    txt = " ".join(s[4:]).strip("\n")
                    start_space = False
                    if s[3][0] == " ":
                        start_space = True
                        txt = txt[1:]
                    
                    self.events.append(UltrastarText(
                        note=UltrastarNote.parse(s[0]),
                        time=int(s[1]),
                        length=int(s[2]),
                        text=txt,
                        start_space=start_space,
                        pitch=int(s[3])
                    ))
