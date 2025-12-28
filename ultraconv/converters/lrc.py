from ultraconv.models import *

import re
from math import floor
from typing import List

# sometimes lrc are not well synced
# we can use this to check beforehand: https://mikezzb.github.io/lrc-player/
# in the case of non well synced lyrics, use the ignore_words=True flag to ignore this data and use the syncing algorithm

class LrcConverter:
    LRC_REG = re.compile(r"<(\d{2}:\d{2}.\d{2})> +([\w'’,]+)")
    LRC_LINE_REG = re.compile(r"([\w'’,]+) *")
    bpm = 0
    word_length_pct = 0.85 # lrc format only gives start time of words, so we can only use part of the timeframe for the actual word (so we keep some time for the space between words)

    def __init__(self, bpm=400):
        self.bpm = bpm

    def _parse_time(self, time_str):
        # Convert a time string in the format MM:SS.MS to the number of seconds
        minutes, seconds = time_str.split(":")
        minutes = int(minutes)
        seconds, milliseconds = map(int, seconds.split("."))
        
        total_seconds = minutes * 60 + seconds + milliseconds / 100
        return total_seconds
    
    def _sec_to_bpm(self, val):
        return floor(val/60*self.bpm*4) # no idea why, but x4 fixes all sync problems

    def convert(self, lyrics: List[str], ultrastar_file=UltrastarFile()) -> UltrastarFile:
        ultrastar_file.tags["BPM"] = self.bpm
        ret = []
        is_gap_set = False
        
        next_break = 0
        lrc_len = len(lyrics)
        for i in range(lrc_len):
            # iterate over lines of text
            is_word_by_word = True

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

                # processing =================
                if not is_gap_set:
                    # if this is the first line, add the GAP
                    is_gap_set = True
                    ultrastar_file.tags["GAP"] = floor(start)
                        
                txt_len = len(txt)
                next_break = start/(txt_len+1) * txt_len
                for j in range(txt_len):
                    if is_word_by_word:
                        word = txt[j][1]
                        start_sec = self._parse_time(txt[j][0])
                        
                        next_word_available = j+1 < txt_len
                        if next_word_available:
                            # get start of next word
                            next_sec = self._parse_time(txt[j+1][0])
                        else:
                            if i+1 < lrc_len and len(lyrics[i+1]) >= 10 and lyrics[i+1][0] == "[" and lyrics[i+1][9] == "]":
                                # if not available, take start of next line
                                next_sec = self._parse_time(lyrics[i+1][1:9])
                            else:
                                # if not available, use an arbitrary time of 3 sec
                                next_sec = start_sec + 3
                            
                        duration_sec = (next_sec-start_sec)*self.word_length_pct # use only 80% of the timeframe as we also need "blank" space between words
                        if not next_word_available:
                            next_break = start_sec + duration_sec  # use the remaining 20% of the timeframe for the break (see duration_sec below)
                    else:
                        # set arbitrary values since the word timing is not available; it should then be re-aligned using a LYRICS_ALIGNER processor
                        start_sec = start
                        duration_sec = 0.1

                    # StartBeat, Length, Pitch, Text
                    ret.append(UltrastarText(time=self._sec_to_bpm(start_sec), length=self._sec_to_bpm(duration_sec), pitch=0, start_space=True, text=word))
                # add break at end of line
                ret.append(UltrastarBreak(floor(self._sec_to_bpm(next_break))))

        ultrastar_file.events = ret
        return ultrastar_file
