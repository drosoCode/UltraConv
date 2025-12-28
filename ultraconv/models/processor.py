from abc import ABC
from enum import Enum
from voluptuous import Schema
from dataclasses import dataclass

from .ultrastar import UltrastarFile

class ProcessorType(Enum):
    TRANSLITERATOR = "transliterator"
    AUDIO_SPLITTER = "audio_splitter"
    LYRICS_ALIGNER = "lyrics_aligner"
    PITCHER = "pitcher"

@dataclass
class ProcessorInfo:
    name: str
    description: str
    processor_type: ProcessorType


class AbstractProcessor(ABC):

    def __init__(self, config: dict):
        self._config = config

    def run(self, uf: UltrastarFile) -> UltrastarFile:
        raise NotImplementedError("Subclasses must implement this method")
    
    @staticmethod
    def is_available():
        """Check if the processor is available. (check dependencies, etc.)"""
        return False
    
    @staticmethod
    def get_info() -> ProcessorInfo:
        """Return the info of the processor."""
        raise NotImplementedError("Subclasses must implement this method")

    @staticmethod
    def get_options() -> Schema:
        """Return the configuration options for this processor."""
        return Schema({})
