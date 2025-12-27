from ultraconv.models import UltrastarFile, UltrastarText

import icu

class TransliteratorProcessor:
    def __init__(self, language):
        self._trl = icu.Transliterator.createInstance(language)

    def run(self, data: UltrastarFile) -> UltrastarFile:
        for i in range(len(data.events)):
            if isinstance(data.events[i], UltrastarText):
                data.events[i].text = self._trl.transliterate(data.events[i].text)
        return data

    @staticmethod
    def get_languages():
        lst = icu.Transliterator.getAvailableIDs()
        lst = list(lst)
        lst.sort()
        return lst

# https://gist.github.com/dpk/8325992#pyicu-cheat-sheet
