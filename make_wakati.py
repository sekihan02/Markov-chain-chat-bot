'''
分かち書き、辞書生成
'''

# utf-8
import MeCab, os, glob

def wakati(text):
    t = MeCab.Tagger("-Owakati")
    m = t.parse(text)
    result = m.rstrip(" \n").split(" ")
    return result

path = "kingyo_ryoran.txt"
with open(path, 'r') as t:
    text = t.read()

word = wakati(text)
wt = ' '.join(word)
open('kingyo.wakati', 'w', encoding='utf-8').write(wt)
