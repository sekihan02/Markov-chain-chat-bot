# utf-8
'''
青空文庫に公開中の作品を作家別に一括ダウンロードできるサイト
http://keison.sakura.ne.jp/index.html
から夏目漱石の作品一覧をダウンロードし、展開したファイルを使用する

中身からヘッダーとフッダー、ルビや脚注を削除して
形態素解析した文章の中から名詞、動詞、形容詞だけを抽出。

最後にword2vec用のモデル作成
'''
import os.path, urllib.request as req
from gensim.models import word2vec
import MeCab, re, sys

# 形態素解析
def Wkati(text):
    # 形態素解析
    m = MeCab.Tagger('-Ochasen')

    # テキストの先頭にあるヘッダとフッタを削除
    text = re.split(r'\-{5,}',text)[2]
    text = re.split(r'底本：', text)[0]
    text = text.strip()
    # ルビを削除
    text = text.replace('｜', '')
    text = re.sub(r'《.+?》', '', text)
    # テキスト内の脚注を削除
    text = re.sub(r'［＃.+?］', '', text)

    # 形態素解析した文章の中から名詞、動詞、形容詞だけを抽出
    words = m.parseToNode(text)
    keyword = []
    while words:
        if words.feature.split(',')[0]==u'名詞' or words.feature.split(',')[0]==u'動詞'or words.feature.split(',')[0]==u'形容詞':
            keyword.append(words.surface)
        words = words.next
    # print(keyword)
    return keyword


# 辞書データの作成
person = '夏目漱石'
All_sakuhin_cnt = 0                                 # 作品数を数えるため
sakuhin_cnt = 0                                     # 作品数を数えるため


results = []
for sakuhin in  os.listdir(person): # range(len(zipfile)): # os.listdir(ziplist):
    print(sakuhin)                                  # 解析中の作品
    All_sakuhin_cnt += 1
    sakuhin_file = person + '/' + sakuhin
    try:
        # 青空文庫のShift_JISファイルを読み込む
        bindata = open(sakuhin_file, 'rb').read()
        text = bindata.decode('shift_jis')
        lines = Wkati(text)                         # 形態素解析
        results += lines
        print('[解析成功]', sakuhin_file)
        sakuhin_cnt += 1
    except Exception as error:
        print('[解析失敗]', sakuhin_file, error)
        continue
print('[全作品数]', All_sakuhin_cnt, '[解析できた作品数]', sakuhin_cnt)


# ファイルの作成
file = 'natume.wakati'
wt = ' '.join(results)
with open(file, 'w', encoding='utf-8') as fp:
    fp.write(' '.join(results))


# word2vec用のモデル作成
word2 = word2vec.LineSentence(file)
model = word2vec.Word2Vec(word2, size=100, window=3, hs=1, min_count=1, sg=1)
model.save('natume.model')

print('モデルできた')