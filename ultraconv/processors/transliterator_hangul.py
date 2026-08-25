from ultraconv.models import UltrastarFile,UltrastarText, AbstractProcessor, ProcessorType, ProcessorInfo

try:
    from hangul_romanize import Transliter
    from hangul_romanize.rule import academic
    HANGUL_AVAILABLE = True
except ImportError:
    HANGUL_AVAILABLE = False
    Transliter = None
    academic = None

class TransliteratorHangul(AbstractProcessor):
    
    def __init__(self, config):
        super().__init__(config)

        if not HANGUL_AVAILABLE:
            raise ImportError("hangul-romanize library is required. Install with: pip install hangul-romanize")
        self.ts = Transliter(academic)

    def run(self, data: UltrastarFile) -> UltrastarFile:
        """
        Transliterate all Korean text events to Latin characters.
        """
        for i in range(len(data.events)):
            if isinstance(data.events[i], UltrastarText):
                try:
                    # Convert Hangul to Latin
                    transliterated = self.ts.translit(data.events[i].text)
                    data.events[i].text = transliterated
                except Exception as e:
                    # If transliteration fails, keep original text
                    print(f"Warning: Could not transliterate Korean text '{data.events[i].text}': {e}")
        return data
    
    @staticmethod
    def get_info() -> ProcessorInfo:
        """Return the info of the processor."""
        return ProcessorInfo(
            name="Hangul Romanize Transliterator",
            description="Transliterates Korean Hangul text to Latin characters using hangul-romanize library.",
            processor_type=ProcessorType.TRANSLITERATOR
        )

    @staticmethod
    def is_available():
        """Check if the transliterator is available."""
        return HANGUL_AVAILABLE
