from ultraconv.models import UltrastarFile, AbstractProcessor, ProcessorType, ProcessorInfo
from pathlib import Path
import os
import shutil
from voluptuous import Schema, Required, In, All, Range

try:
    import demucs.separate
    DEMUCS_AVAILABLE = True
except ImportError:
    DEMUCS_AVAILABLE = False
    demucs = None

MODELS = [
    "htdemucs_mmi",
    "htdemucs_6s",
    "htdemucs_ft",
    "htdemucs",
    "mdx_extra_q",
    "mdx_extra",
    "mdx_q",
    "mdx",
]

class SplitterDemucs(AbstractProcessor):
    def __init__(self, config):
        super().__init__(config)
        self._model = config.get("model", "htdemucs")
        self._jobs = config.get("jobs", 4)
        self._shifts = config.get("shifts", 1)
        
    def run(self, data: UltrastarFile) -> UltrastarFile:
        data.check_fields(["AUDIO"])

        p = Path(data.file_path)
        tmp = os.path.join(os.getcwd(), "tmp")
        os.makedirs(tmp, exist_ok=True)

        demucs.separate.main([
            "--two-stems",
            "vocals",
            "-n",
            self._model,
            "-j",
            str(self._jobs),
            "--shifts",
            str(self._shifts),
            "--mp3", 
            os.path.join(p.parent, data.tags["AUDIO"]),
            "--out",
            tmp
        ])

        tmpm = os.path.join(tmp, self._model, Path(data.tags["AUDIO"]).stem)
        shutil.move(os.path.join(tmpm, "no_vocals.mp3"), os.path.join(p.parent, "no_vocals.mp3"))
        shutil.move(os.path.join(tmpm, "vocals.mp3"), os.path.join(p.parent, "vocals.mp3"))
        shutil.rmtree(tmp)

        data.tags["INSTRUMENTAL"] = "no_vocals.mp3"
        data.tags["VOCALS"] = "vocals.mp3"

        return data
    
    @staticmethod
    def get_info() -> ProcessorInfo:
        return ProcessorInfo(
            name="HT Demucs Splitter",
            description="Splits audio into vocals and instrumental using HT Demucs model.",
            processor_type=ProcessorType.AUDIO_SPLITTER
        )
    
    @staticmethod
    def is_available():
        return DEMUCS_AVAILABLE

    @staticmethod
    def get_options():
        return Schema({
            Required("model", default="htdemucs"): In(MODELS),
            Required("jobs", default=4): All(int, Range(min=1, max=8)),
            Required("shifts", default=1): All(int, Range(min=1, max=8)),
        })
