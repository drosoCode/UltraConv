import demucs.separate
from models.ultrastar import UltrastarFile
from pathlib import Path
import os
import shutil

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

class SplitterProcessor:
    def __init__(self, model="htdemucs", jobs = 4, shifts = 1):
        self._model = model
        self._jobs = jobs
        self._shifts = shifts

    def run(self, data: UltrastarFile) -> UltrastarFile:
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
            os.path.join(p.parent, data.mp3),
            "--out",
            tmp
        ])

        tmpm = os.path.join(tmp, self._model, Path(data.mp3).stem)
        shutil.move(os.path.join(tmpm, "no_vocals.mp3"), os.path.join(p.parent, "no_vocals.mp3"))
        shutil.move(os.path.join(tmpm, "vocals.mp3"), os.path.join(p.parent, "vocals.mp3"))
        shutil.rmtree(tmp)

        data.instrumental = "no_vocals.mp3"
        data.vocals = "vocals.mp3"

        return data

    @staticmethod
    def get_models():
        return MODELS
