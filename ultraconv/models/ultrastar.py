from ultraconv.models import UltrastarEvent, UltrastarNote, UltrastarBreak, UltrastarText

from typing import List

class UltrastarFile:
    events: List[UltrastarEvent] = []
    tags = {}

    file_path: str = ""

    def __init__(self):
        pass

    def get_file_data(self):
        if "MP3" not in self.tags:
            self.tags["MP3"] = self.tags.get("AUDIO")
        
        lines = []
        for t,v in self.tags.items():
            lines.append(f"#{t}:{v}")

        for i in self.events:
            lines.append(i.to_ultrastar())
        lines.append("E")

        return lines

    def write(self, path: str = ""):
        if path == "":
            path = self.file_path
        else:
            self.file_path = path

        lines = self.get_file_data()
    
        with open(path, "w+", encoding="utf8") as f:
            f.write("\n".join(lines))

    def read(self, path: str):
        self.file_path = path
        self.events = []
        with open(path, "r", encoding="utf8") as f:
            data = f.readlines()
        
        for l in data:
            if l == "E":
                break
            elif len(l) < 3:
                continue

            if l[0] == "#":
                s = l[1:].split(":")
                value = s[1].strip("\n")
                if s[0] in ("BPM", "GAP"):
                    value = float(value)
                self.tags[s[0]] = value
            
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

        # for retrocompatibility
        if "AUDIO" not in self.tags:
            self.tags["AUDIO"] = self.tags.get("MP3")
        if "MP3" not in self.tags:
            self.tags["MP3"] = self.tags.get("AUDIO")
