from pathlib import Path
import os

from voluptuous import Schema, Required

from ultraconv.models import UltrastarFile, AbstractProcessor, ProcessorType, ProcessorInfo

try:
    from ultrastar_pitch import DetectionPipeline, ProjectParser, AudioPreprocessor, PitchClassifier, StochasticPostprocessor
    USTAR_PITCH_AVAILABLE = True
except ImportError:
    USTAR_PITCH_AVAILABLE = False

class PitcherUltrastarPitch(AbstractProcessor):

    def __init__(self, config):
        super().__init__(config)
        self._postproc = config.get("postproc", True)

    def run(self, data: UltrastarFile) -> UltrastarFile:
        data.check_fields(["VOCALS", "MP3"])
        
        # set mp3 to vocals file
        p = Path(data.file_path)
        filepath_bak = data.file_path
        mp3_bak = data.tags["MP3"]
        data.tags["MP3"] = data.tags["VOCALS"]
        data.file_path = os.path.join(p.parent, p.stem+"_tmp.txt")
        data.write()

        detection_pipeline = DetectionPipeline(
            ProjectParser(), AudioPreprocessor(stride=128), PitchClassifier(), StochasticPostprocessor()
        )
        detection_pipeline.transform(data.file_path, data.file_path, self._postproc)

        # read new data
        data.read(data.file_path)

        # restore mp3
        data.tags["MP3"] = mp3_bak
        os.remove(data.file_path)
        data.file_path = filepath_bak

        return data

    @staticmethod
    def get_info() -> ProcessorInfo:
        """Return the info of the processor."""
        return ProcessorInfo(
            name="UltrastarPitch Pitcher",
            description="Generates pitch events using UltrastarPitch library.",
            processor_type=ProcessorType.PITCHER
        )
    
    @staticmethod
    def is_available():
        """Check if the pitcher is available."""
        return USTAR_PITCH_AVAILABLE
    
    @staticmethod
    def get_options():
        return Schema({
            Required("postproc", default=True): bool
        })
