from ultraconv.models import UltrastarFile, UltrastarText, AbstractProcessor, ProcessorType, ProcessorInfo

try:
    import pykakasi
    KAKASI_AVAILABLE = True
except ImportError:
    KAKASI_AVAILABLE = False
    pykakasi = None

class TransliteratorKakasi(AbstractProcessor):
    
    def __init__(self, config):
        super().__init__(config)
        
        if not KAKASI_AVAILABLE:
            raise ImportError("pykakasi library is required. Install with: pip install pykakasi")
        
        self.kakasi = pykakasi.kakasi()
        
        # Configure for romaji output
        self.kakasi.setMode('H', 'a')  # Hiragana to ASCII
        self.kakasi.setMode('K', 'a')  # Katakana to ASCII
        self.kakasi.setMode('J', 'a')  # Kanji to ASCII
        self.conv = self.kakasi.getConverter()

    def run(self, data: UltrastarFile) -> UltrastarFile:
        """
        Transliterate all Japanese text events to Romaji.
        """
        for i in range(len(data.events)):
            if isinstance(data.events[i], UltrastarText):
                try:
                    # Convert to romaji
                    transliterated = self.conv.do(data.events[i].text)
                    data.events[i].text = transliterated
                except Exception as e:
                    # If transliteration fails, keep original text
                    print(f"Warning: Could not transliterate Japanese text '{data.events[i].text}': {e}")
        return data
    
    @staticmethod
    def get_info() -> ProcessorInfo:
        """Return the info of the processor."""
        return ProcessorInfo(
            name="Kakasi Transliterator",
            description="Transliterates Japanese text to Romaji using pykakasi library.",
            processor_type=ProcessorType.TRANSLITERATOR
        )

    @staticmethod
    def is_available():
        """Check if the transliterator is available."""
        return KAKASI_AVAILABLE
