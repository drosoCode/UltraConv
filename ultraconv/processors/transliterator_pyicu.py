from ultraconv.models import UltrastarFile, UltrastarText, AbstractProcessor, ProcessorType, ProcessorInfo
from voluptuous import Schema, In, Required

try:
    import icu
    ICU_AVAILABLE = True
except ImportError:
    ICU_AVAILABLE = False
    icu = None

class TransliteratorICU(AbstractProcessor):
    
    def __init__(self, config):
        super().__init__(config)

        if not ICU_AVAILABLE:
            raise ImportError("PyICU library is required. Install with: pip install PyICU")
        
        self._trl = icu.Transliterator.createInstance(config.get('language'))

    def run(self, data: UltrastarFile) -> UltrastarFile:
        for i in range(len(data.events)):
            if isinstance(data.events[i], UltrastarText):
                data.events[i].text = self._trl.transliterate(data.events[i].text)
        return data

    @staticmethod
    def get_info() -> ProcessorInfo:
        """Return the info of the processor."""
        return ProcessorInfo(
            name="PyICU Transliterator",
            description="Transliterates text using ICU library.",
            processor_type=ProcessorType.TRANSLITERATOR
        )
    
    @staticmethod
    def is_available():
        """Check if the transliterator is available."""
        return ICU_AVAILABLE

    @staticmethod
    def get_options() -> Schema:
        lst = icu.Transliterator.getAvailableIDs()
        lst = list(lst)
        lst.sort()

        return Schema({
            Required('language'): In(lst)
        })

# https://gist.github.com/dpk/8325992#pyicu-cheat-sheet
