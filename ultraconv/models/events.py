from dataclasses import dataclass
from enum import Enum

class UltrastarNote(Enum):
    NORMAL = 0
    GOLDEN = 1
    FREESTYLE = 2
    RAP = 3
    RAP_GOLDEN = 4
    
    def __str__(self):
        if self.value == UltrastarNote.NORMAL:
            return ":"
        elif self.value == UltrastarNote.GOLDEN:
            return "*"
        elif self.value == UltrastarNote.FREESTYLE:
            return "F"
        elif self.value == UltrastarNote.RAP:
            return "R"
        elif self.value == UltrastarNote.RAP_GOLDEN:
            return "G"
        else:
            return ":"
        
    @staticmethod
    def parse(note):
        if note == ":":
            return UltrastarNote.NORMAL
        elif note == "*":
            return UltrastarNote.GOLDEN
        elif note == "F":
            return UltrastarNote.FREESTYLE
        elif note == "R":
            return UltrastarNote.RAP
        elif note == "G":
            return UltrastarNote.RAP_GOLDEN
        else:
            return UltrastarNote.NORMAL

class UltrastarEvent:
    time: int

    def __init__(self, time):
        self.time = time

    def to_ultrastar(self):
        raise NotImplementedError()


@dataclass
class UltrastarText(UltrastarEvent):
    length: int
    text: str
    start_space: bool
    note: UltrastarNote
    pitch: int

    def __init__(self, time, length, text, start_space=False, note=UltrastarNote.NORMAL, pitch=0):
        super().__init__(time)
        self.length = length
        self.text = text
        self.start_space = start_space
        self.note = note
        self.pitch = pitch

    def to_ultrastar(self):
        return f"{self.note} {self.time} {self.length} {self.pitch} {' ' if self.start_space else ''}{self.text}"

@dataclass
class UltrastarBreak(UltrastarEvent):
    def __init__(self, time):
        return super().__init__(time)

    def to_ultrastar(self):
        return f"- {self.time}"
