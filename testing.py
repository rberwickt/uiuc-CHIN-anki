from xpinyin import Pinyin
import opencc
converter = opencc.OpenCC('s2t.json')
p = Pinyin()
inputted = "你"
while inputted != "":
    inputted = input()
    print(p.get_pinyin(inputted, tone_marks="marks",splitter=" "))
    print(converter.convert(inputted))