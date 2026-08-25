from ultraconv.models.ultrastar import UltrastarFile
from ultraconv.models import UltrastarFile, UltrastarText, AbstractProcessor, ProcessorType, ProcessorInfo

try:
    from unidecode import unidecode
    UNIDECODE_AVAILABLE = True
except ImportError:
    UNIDECODE_AVAILABLE = False
    unidecode = None

class TransliteratorUnidecode(AbstractProcessor):
    
    def __init__(self, config):
        super().__init__(config)

        if not UNIDECODE_AVAILABLE:
            raise ImportError("unidecode library is required. Install with: pip install unidecode")
    
    def run(self, data: UltrastarFile) -> UltrastarFile:
        """
        Transliterate all text events in the UltrastarFile to ASCII.
        """
        for i in range(len(data.events)):
            if isinstance(data.events[i], UltrastarText):
                data.events[i].text = unidecode(data.events[i].text)
        return data

    @staticmethod
    def get_info() -> ProcessorInfo:
        """Return the info of the processor."""
        return ProcessorInfo(
            name="Unidecode Transliterator",
            description="Transliterates text to ASCII using unidecode library.",
            processor_type=ProcessorType.TRANSLITERATOR
        )
    
    @staticmethod
    def is_available():
        """Check if the transliterator is available."""
        return UNIDECODE_AVAILABLE
