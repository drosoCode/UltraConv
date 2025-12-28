from ultraconv.models.ultrastar import UltrastarFile, UltrastarText, AbstractProcessor, ProcessorType, ProcessorInfo

try:
    import cutlet
    CUTLET_AVAILABLE = True
except ImportError:
    CUTLET_AVAILABLE = False
    cutlet = None

class TransliteratorCutlet(AbstractProcessor):
    """
    Modern Japanese transliterator using cutlet library.
    High-quality Kanji/Hiragana/Katakana to Romaji conversion.
    """
    
    def __init__(self, config):
        super().__init__(config)
    
        if not CUTLET_AVAILABLE:
            raise ImportError("cutlet library is required. Install with: pip install cutlet")
        
        self.katsu = cutlet.Cutlet()

    def run(self, data: UltrastarFile) -> UltrastarFile:
        """
        Transliterate all Japanese text events to Romaji using cutlet.
        """
        for i in range(len(data.events)):
            if isinstance(data.events[i], UltrastarText):
                try:
                    # Convert to romaji
                    transliterated = self.katsu.romaji(data.events[i].text)
                    data.events[i].text = transliterated
                except Exception as e:
                    # If transliteration fails, keep original text
                    print(f"Warning: Could not transliterate Japanese text '{data.events[i].text}': {e}")
        return data

    @staticmethod
    def get_info() -> ProcessorInfo:
        """Return the info of the processor."""
        return ProcessorInfo(
            name="Cutlet Transliterator",
            description="Transliterates Japanese text to Romaji using cutlet library.",
            processor_type=ProcessorType.TRANSLITERATOR
        )

    @staticmethod
    def is_available():
        """Check if the transliterator is available."""
        return CUTLET_AVAILABLE