from pathlib import Path
import os

from voluptuous import Schema, Required, Boolean

from ultraconv.models import UltrastarFile, AbstractProcessor, ProcessorType, ProcessorInfo

class AlignerSimpleAlgo(AbstractProcessor):

    def __init__(self, config):
        super().__init__(config)

    def run(self, data: UltrastarFile) -> UltrastarFile:
        
        pass

    @staticmethod
    def get_info() -> ProcessorInfo:
        """Return the info of the processor."""
        return ProcessorInfo(
            name="Basic length-based aligner",
            description="Aligns lyrics based on word length. Only works when lines are already time-aligned.",
            processor_type=ProcessorType.LYRICS_ALIGNER
        )
    
    @staticmethod
    def is_available():
        return True

    @staticmethod
    def get_options():
        return Schema({
            Required("postproc", default=True): Boolean()
        })
