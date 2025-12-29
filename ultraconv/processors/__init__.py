from ultraconv.processors.utils import *

from ultraconv.processors.aligner_algo import AlignerSimpleAlgo

from ultraconv.processors.pitcher import PitcherUltrastarPitch

from ultraconv.processors.splitter_htdemucs import SplitterDemucs

from ultraconv.processors.transliterator_unidecode import TransliteratorUnidecode
from ultraconv.processors.transliterator_pyicu import TransliteratorICU
from ultraconv.processors.transliterator_kakasi import TransliteratorKakasi
from ultraconv.processors.transliterator_hangul import TransliteratorHangul

PROCESSORS = [AlignerSimpleAlgo, PitcherUltrastarPitch, SplitterDemucs, TransliteratorICU, TransliteratorUnidecode, TransliteratorKakasi, TransliteratorHangul]

def get_available_processors():
    lst = []
    for processor in PROCESSORS:
        if processor.is_available():
            lst.append(processor)
    return lst
