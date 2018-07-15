'''
MeCabによる分かち書き
50文の文字数の平均と単語数の分布のヒストグラム
'''

# utf-8
import numpy as np
import matplotlib.pyplot as plt
import re, MeCab

# テキストの読み込み
# open()したファイルオブジェクトはclose()メソッドでクローズする必要がある。
# withブロックを使いブロックの終了時に自動的にクローズする。閉じ忘れがなくなるので便利。
path = 'kingyo_ryoran.txt'

with open(path, 'r') as t:      # テキストを読み込む
    # print(type(t))
    text = t.read()             # 開いたファイル全体を文字列として取得

# 読み込み方法2
# t = open(path, 'r') 
# print(type(t))
# text = t.read()
# t.close()      ＃操作終了時に必要

# 取得の確認
#print(text)

m = MeCab.Tagger('-Ochasen')        # MeCabで品詞分解
# 取得の確認
# print(m.parse(text))

# 除去処理
text = re.sub(' ','',text)
text = re.split('。(?!」)|\n',re.sub(' ','',text))
while '' in text:
    text.remove('')     # 空行を除く

# 先頭50文字について文単位で形態素解析する
# 名詞だけ取り出す
lenghlist = np.array([len(v) for v in text][:50])
print('average', lenghlist.mean())  # 50文の文字数の平均
print('variance', lenghlist.var())      # 分散(データの散らばり具合、平均からどれだけ離れているか)
print('std-deviation',lenghlist.std())  # 標準偏差(分散の正の平方根を標準偏差)

# 50文の文字数のヒストグラム
his = plt.figure()
plt.title('Histogram of number of characters per sentence')
plt.xlabel('length')
plt.ylabel('frequency')
# plt.ylim([0., 5])
plt.hist(lenghlist, color=None ,bins=100)    # bins
plt.show()
