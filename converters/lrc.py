from models.events import *
from models.ultrastar import UltrastarFile

import re
from math import floor
from typing import List

# sometimes lrc are not well synced
# we can use this to check beforehand: https://mikezzb.github.io/lrc-player/
# in the case of non well synced lyrics, use the ignore_words=True flag to ignore this data and use the syncing algorithm

class LrcConverter:
    LRC_REG = re.compile(r"<(\d{2}:\d{2}.\d{2})> +([A-zÀ-ú'’,]+)")
    LRC_LINE_REG = re.compile(r"([A-zÀ-ú'’,]+) *")
    bpm = 0
    ignore_words = False
    line_length_pct = 0
    word_length_pct = 0

    def __init__(self, bpm=400, ignore_words=False, line_length_pct=0.95, word_length_pct=0.8):
        self.bpm = bpm
        self.ignore_words = ignore_words
        self.line_length_pct = line_length_pct
        self.word_length_pct = word_length_pct

    def _parse_time(self, time_str):
        # Convert a time string in the format MM:SS.MS to the number of seconds
        minutes, seconds = time_str.split(":")
        minutes = int(minutes)
        seconds, milliseconds = map(int, seconds.split("."))
        
        total_seconds = minutes * 60 + seconds + milliseconds / 100
        return total_seconds
    
    def _sec_to_bpm(self, val):
        return floor(val/60*self.bpm*4) # no idea why, but x4 fixes all sync problems

    def convert(self, lyrics: List[str]) -> UltrastarFile:
        ultrastar = UltrastarFile()
        ultrastar.bpm = self.bpm
        ret = []
        is_gap_set = False
        
        next_break = 0
        lrc_len = len(lyrics)
        for i in range(lrc_len):
            # iterate over lines of text
            is_word_by_word = True
            avg_sec_by_word = 0

            if len(lyrics[i]) > 11 and lyrics[i][0] == "[" and lyrics[i][9] == "]":
                start = self._parse_time(lyrics[i][1:9])
                txt = self.LRC_REG.findall(lyrics[i][11:])
                if len(txt) == 0:
                    txt = self.LRC_LINE_REG.findall(lyrics[i][11:])
                    is_word_by_word = False
                #example text: <00:10.91> Yeah, <00:11.18>   <00:11.22> I <00:11.34>   <00:11.48> got <00:11.56>   <00:11.66> voices 

                # iterate over words to count letters, if empty skip the line
                if is_word_by_word:
                    nb_letters = sum([len(x[1]) for x in txt])
                else:
                    nb_letters = sum([len(x) for x in txt])
                if nb_letters == 0:
                    continue

                if not is_word_by_word or self.ignore_words:
                    if i+1 < lrc_len and len(lyrics[i+1]) >= 10 and lyrics[i+1][0] == "[" and lyrics[i+1][9] == "]":
                        next_start = self._parse_time(lyrics[i+1][1:9])
                    line_duration = (next_start-start)*self.line_length_pct # use 90% of line length for word, and keep 10% for the break
                    avg_sec_by_word = line_duration/nb_letters

                # processing =================
                if not is_gap_set:
                    # if this is the first line, add the GAP
                    is_gap_set = True
                    ultrastar.gap = floor(start)
                else:
                    if not is_word_by_word or self.ignore_words:
                        prev_line = self._parse_time(lyrics[i-1][1:9])
                        break_duration = ((start-prev_line)*(1-self.line_length_pct))
                        ret.append(UltrastarBreak(floor(self._sec_to_bpm(start-break_duration))))
                    else:
                        ret.append(UltrastarBreak(floor(self._sec_to_bpm(next_break))))
                
                txt_len = len(txt)
                total_sec = start
                for j in range(txt_len):
                    if is_word_by_word and not self.ignore_words:
                        word = txt[j][1]
                        start_sec = self._parse_time(txt[j][0])
                        if j+1 < txt_len:
                            # get start of next word
                            next_sec = self._parse_time(txt[j+1][0])
                        elif i+1 < lrc_len and len(lyrics[i+1]) >= 10 and lyrics[i+1][0] == "[" and lyrics[i+1][9] == "]":
                            # if not available, take start of next line
                            next_sec = self._parse_time(lyrics[i+1][1:9])
                            word_duration = ((next_sec-start_sec)*self.word_length_pct) # use the remaining 10% of the timeframe for the break (see duration_sec below)
                            next_break = start_sec+word_duration
                        else:
                            # if not available, use an arbitrary time of 3 sec
                            next_sec = start_sec + 3
                        duration_sec = (next_sec-start_sec)*self.word_length_pct # use only 80% of the timeframe as we also need "blank" space between words
                    else:
                        if self.ignore_words:
                            word = txt[j][1]
                        else:
                            word = txt[j]
                        start_sec = total_sec
                        duration_sec = len(word)*avg_sec_by_word
                        total_sec += duration_sec
                        duration_sec *= self.word_length_pct # use only 80% of the timeframe as we also need "blank" space between words
                    
                    # StartBeat, Length, Pitch, Text
                    ret.append(UltrastarText(time=self._sec_to_bpm(start_sec), length=self._sec_to_bpm(duration_sec), pitch=0, start_space=True, text=word))

        ultrastar.events = ret
        return ultrastar
