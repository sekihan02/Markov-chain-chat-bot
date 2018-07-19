'''
word2vecで使える分かち書きモデル
'''
# from gensim.model import word2vec
import MeCab, re, sys

# テキストファイルの読み込み
path = 'kingyo_ryoran.txt'
with open(path, 'r') as t:
    text = t.read()

# 形態素解析
m = MeCab.Tagger('-Ochasen')       # -Owakati / -Ochasen / -Oyomi / mecabrc で出力形式の変更

'''
解析結果の表示
word = m.parse(text)
print(word)
'''

'''
parseの引数に文字列を入寮すると解析結果がテキストが返ってくる
parse()の代わりにparseToNode()を使うと形態素の詳細情報
parseToNode()は文字列でsurfaceで表層形、featureで形態素情報
'''
# 形態素解析した文章の中から名詞、動詞、形容詞だけを抽出
words = m.parseToNode(text)
keyword = []
while words:
    if words.feature.split(',')[0]==u'名詞' or words.feature.split(',')[0]==u'動詞'or words.feature.split(',')[0]==u'形容詞':
        keyword.append(words.surface)        
    words = words.next
print(keyword)
