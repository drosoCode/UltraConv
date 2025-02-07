from ultrastar_pitch import DetectionPipeline, AudioPreprocessor, PitchClassifier, StochasticPostprocessor, ProjectParser

from pathlib import Path
import os

from ultraconv.models import UltrastarFile

class PitcherProcessor:

    def __init__(self, postproc = True):
        self._postproc = postproc

    def run(self, data: UltrastarFile) -> UltrastarFile:
        if data.tags.get("VOCALS") is None:
            return None
        
        # set mp3 to vocals file
        p = Path(data.file_path)
        filepath_bak = data.file_path
        mp3_bak = data.tags["AUDIO"]
        data.tags["AUDIO"] = data.tags["VOCALS"]
        data.file_path = os.path.join(p.parent, p.stem+"_tmp.txt")
        data.write()

        detection_pipeline = DetectionPipeline(
            ProjectParser(), AudioPreprocessor(stride=128), PitchClassifier(), StochasticPostprocessor()
        )
        detection_pipeline.transform(data.file_path, data.file_path, self._postproc)

        # read new data
        data.read(data.file_path)

        # restore mp3
        data.tags["AUDIO"] = mp3_bak
        os.remove(data.file_path)
        data.file_path = filepath_bak

        return data
