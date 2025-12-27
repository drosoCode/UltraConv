from ultraconv.models import UltrastarFile, UltrastarText

from polyglot.transliteration import Transliterator
from polyglot.downloader import downloader
from polyglot.text import Text

class TransliteratorProcessor:
    def __init__(self, language):
        self.language = language
        downloader.download("embeddings2." + language)
        downloader.download("transliteration2." + language)
        
    def run(self, data: UltrastarFile) -> UltrastarFile:
        for i in range(len(data.events)):
            if isinstance(data.events[i], UltrastarText):
                data.events[i].text = Text(data.events[i].text).transliterate(self.language)
        return data

    @staticmethod
    def get_languages():
        transliteration = downloader.supported_languages_table("transliteration2")
        embeddings = downloader.supported_languages_table("embeddings2")
        lst = set(transliteration.keys()).intersection(set(embeddings.keys()))
        
        lst = list(lst)
        lst.sort()
        return lst

# https://gist.github.com/dpk/8325992#pyicu-cheat-sheet
