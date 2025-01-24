from converters.ass import AssConverter
from models.ultrastar import UltrastarFile

cvt = AssConverter(bpm=205)

uf = cvt.convert("./data/skz - chk chk boom/ENG - Stray Kids - MV - Chk Chk Boom.ass")

uf.artist = "Stray Kids"
uf.title = "Chk Chk Boom"
uf.mp3 = "chkchkboom.mp3"

uf.write("./data/chkchkboom/chkchkboom_v2.txt")

#txt = UltrastarFile()
#txt.read("./data/chkchkboom/chkchkboom_v2.txt")
#txt.write("./data/chkchkboom/chkchkboom_v2_2.txt")
