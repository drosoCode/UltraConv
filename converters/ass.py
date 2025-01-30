from models.events import *
from models.ultrastar import UltrastarFile

import re
from math import floor
from typing import List

class AssConverter:
    FLAG_REG = re.compile(r"\{\\kf?(\d+)\}([A-zÀ-ú'’,]+)( ?)")
    bpm = 250

    def __init__(self, bpm=250):
        self.bpm = bpm

    def _parse_time(self, time_str):
        # Convert a time string in the format H:MM:SS.MS to the number of beats
        hours, minutes, seconds = time_str.split(":")
        minutes = int(minutes)
        seconds, milliseconds = map(int, seconds.split("."))
        
        total_seconds = int(hours) * 3600 + minutes * 60 + seconds + milliseconds / 100
        return total_seconds
    
    def _sec_to_bpm(self, val):
        return floor(val/60*self.bpm*4) # no idea why, but x4 fixes all sync problems

    def convert(self, lyrics: List[str]) -> UltrastarFile:
        ultrastar = UltrastarFile()
        ultrastar.bpm = self.bpm
        ret = []
        is_gap_set = False
        
        prev_end = 0
        for i in lyrics:
            # iterate over lines of text
            if len(i) > 9 and i[0:9] == "Comment: ":
                s = i.split(",")
                start = self._parse_time(s[1])
                txt = self.FLAG_REG.findall(s[9])
                #example text: {\k21}PLAN{\k18}dae{\k12}ro {\k29}KEEP {\k29}GOING

                # iterate over words to count letters, if empty skip the line
                nb_letters = sum([len(x[1]) for x in txt])
                if nb_letters == 0:
                    continue

                # processing =================
                if not is_gap_set:
                    # if this is the first line, add the GAP
                    is_gap_set = True
                    ultrastar.gap = floor(start)
                else:
                    breakline = self._sec_to_bpm(prev_end) + ((self._sec_to_bpm(start)-self._sec_to_bpm(prev_end))*0.7)
                    ret.append(UltrastarBreak(floor(breakline)))
                
                total_sec = start
                next_space = True
                for w in txt:
                    duration_sec = int(w[0])/100
                    # StartBeat, Length, Pitch, Text
                    ret.append(UltrastarText(time=self._sec_to_bpm(total_sec), length=self._sec_to_bpm(duration_sec), pitch=0, start_space=next_space, text=w[1]))
                    total_sec += duration_sec
                    next_space = (w[2] == " ")

                prev_end = total_sec

        ultrastar.events = ret
        return ultrastar
