'''
N-gramは隣の文字ごの連なりを単位とした分析
つなりの頻度分布を測定する
'''

# utf-8
from collections import Counter
import numpy as np

path = 'kingyo_ryoran.txt'
with open(path, 'r') as t:
    string = t.read()

delimiter = ['[',']', '...', ' ']

doublets = list(zip(string[:-1], string[1:]))
doublets = filter((lambda x: not((x[0] in delimiter) or (x[1] in delimiter)) ), doublets)


triplets = list(zip(string[:-2], string[1:-1], string[2:]))
triplets = filter((lambda x: not((x[0] in delimiter) or (x[1] in delimiter) or (x[2] in delimiter))), triplets)

dic2 = Counter(doublets)
for k,v in sorted(dic2.items(), key=lambda x: x[1], reverse=True)[:50]:
    print(k, v)    

dic3 = Counter(triplets)
for k,v in sorted(dic3.items(), key=lambda x: x[1], reverse=True)[:50]:
    print(k, v)    