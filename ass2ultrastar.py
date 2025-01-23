import sys
import re
from datetime import timedelta
from math import floor, ceil

FLAG_REG = re.compile(r"\{\\kf?(\d+)\}([A-Za-z'’]+)( ?)")

def parse_time(time_str):
    # Convert a time string in the format H:MM:SS.MS to the number of beats
    hours, minutes, seconds = time_str.split(":")
    minutes = int(minutes)
    seconds, milliseconds = map(int, seconds.split("."))
    
    total_seconds = int(hours) * 3600 + minutes * 60 + seconds + milliseconds / 100
    return total_seconds


def convert(src, dst):
    bpm = 205

    out = ["#TITLE:Chk Chk Boom", "#ARTIST:Stray Kids", "#MP3:chkchkboom.mp3", f"#BPM:{bpm}"]
    gap = -1
    
    def sec_to_bpm(val):
        return floor(val/60*bpm*4) # no idea why, but x4 fixes all sync problems
    
    with open(src, "r", encoding="utf8") as f:
        ass_data = f.readlines()


    prev_end = 0
    for i in ass_data:
        # iterate over lines of text
        if len(i) > 9 and i[0:9] == "Comment: ":
            s = i.split(",")
            start = parse_time(s[1])
            txt = FLAG_REG.findall(s[9])
            #{\k21}PLAN{\k18}dae{\k12}ro {\k29}KEEP {\k29}GOING

            nb_space = 0
            nb_letters = 0
            # iterate over words to count letters
            for w in txt:
                if len(w) > 2 and w[2] == " ":
                    nb_space += 1
                nb_letters += len(w[1])
            # if this is empty, skip this line
            if nb_letters == 0:
                continue

            # processing =================
            if gap == -1:
                # if this is the first line, add the GAP
                gap = floor(start)
                out.append(f"#GAP:{floor(start)}")
            else:
                breakline = sec_to_bpm(prev_end) + ((sec_to_bpm(start)-sec_to_bpm(prev_end))*0.7)
                out.append(f"- {floor(breakline)}")
            
            total_sec = start
            next_space = True
            for w in txt:
                #w_duration = float("0."+w[0])
                #b_len = (w_duration)
                #if len(w) > 2 and w[2] == " ":
                 #   b_len *= pct
                #b_len = floor(b_len*mult)
                duration_sec = int(w[0])/100
                # StartBeat, Length, Pitch, Text
                out.append(f": {sec_to_bpm(total_sec)} {sec_to_bpm(duration_sec)} 0 {(" " if next_space else "")+w[1]}")
                total_sec += duration_sec
                next_space = w[2]

            prev_end = total_sec
    
    with open(dst, "w", encoding="utf8") as f:
        out.append("E")
        f.writelines("\n".join(out))


if len(sys.argv) == 3:
    convert(sys.argv[1], sys.argv[2])
else:
    print("usage: ass2ultrastar.py [source_file.ass] [dest_file.txt]")


# https://github.com/adefossez/demucs (https://github.com/fabiogra/moseca)
# https://github.com/spotify/basic-pitch
# https://github.com/paradigmn/ultrastar_pitch
# https://github.com/moehmeni/syncedlyrics
