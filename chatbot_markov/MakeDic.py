# utf-8
'''
青空文庫に公開中の作品を作家別に一括ダウンロードできるサイト
http://keison.sakura.ne.jp/index.html
から太宰治の作品一覧をダウンロードし、展開したファイルを使用する

ファイルからヘッダーとフッダー、ルビや脚注を削除して
文章janomeで形態素解析する
'''
import os.path, urllib.request as req
from janome.tokenizer import Tokenizer
import os, re, json, sys, random

# マルコフ連鎖の辞書を作成
def make_dic(words):
    tmp = ["@"]
    dic = {}
    for i in words:
        word = i.surface
        if word == "" or word == "\r\n" or word == "\n": continue
        tmp.append(word)
        if len(tmp) < 3: continue
        if len(tmp) > 3: tmp = tmp[1:]
        set_word3(dic, tmp)
        if word == "。":
            tmp = ["@"]
            continue
    return dic

# 三要素のリストを辞書として登録
def set_word3(dic, s3):
    w1, w2, w3 = s3
    if not w1 in dic: dic[w1] = {}
    if not w2 in dic[w1]: dic[w1][w2] = {}
    if not w3 in dic[w1][w2]: dic[w1][w2][w3] = 0
    dic[w1][w2][w3] += 1

# 文章を読み込む
def Read_Sentence(text):
    # テキストの先頭にあるヘッダとフッタを削除
    text = re.split(r'\-{5,}',text)[2]
    text = re.split(r'底本：', text)[0]
    text = text.strip()
    # ルビを削除
    text = text.replace('｜', '')
    text = re.sub(r'《.+?》', '', text)
    # テキスト内の脚注を削除
    text = re.sub(r'［＃.+?］', '', text)
    return text

# 辞書データの作成
person = '太宰治'
All_sakuhin_cnt = 0                                 # 作品数を数えるため
sakuhin_cnt = 0                                     # 作品数を数えるため
results = []

file = 'dazai.json'                                 # ファイルの作成

for sakuhin in  os.listdir(person): # range(len(zipfile)): # os.listdir(ziplist):
    print(sakuhin)                                  # 解析中の作品
    All_sakuhin_cnt += 1
    sakuhin_file = person + '/' + sakuhin
    try:
        # 青空文庫のShift_JISファイルを読み込む
        bindata = open(sakuhin_file, 'rb').read()
        text = bindata.decode('shift_jis')
        lines = Read_Sentence(text)                         # 形態素解析
        results += lines
        print('[解析成功]', sakuhin_file)

        # janomeで形態素解析 
        t = Tokenizer()
        keyword = t.tokenize(text)
        dic = make_dic(keyword)
        json.dump(dic, open(file,"w", encoding="utf-8"))
        sakuhin_cnt += 1

    except Exception as error:
        print('[解析失敗]', sakuhin_file, error)
        continue
print('[全作品数]', All_sakuhin_cnt, '[解析できた作品数]', sakuhin_cnt)

print('モデルできた')