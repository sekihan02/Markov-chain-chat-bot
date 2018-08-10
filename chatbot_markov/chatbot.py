'''
マルコフ連鎖の練習
マルコフ連鎖を使用した対話モデル

マルコフ連鎖は確率過程の一つと考えていいのかな
別名マルコフ過程
確率過程を使って文章をつなぎ合わせて文を作る

マルコフ性(次に予測される状態が過去の状態に依存せず、現在の状態によってのみ決まる性質)
を持つ確率過程のうち取り売る値が離散的なもの
(マルコフ性を備えた確率過程を総称したマルコフ過程の中でも取る可能性のある値が連続的でなく離散的)
これを特にマルコフ連鎖という・・・らしいよ

文の類似度を調べるN-gramの基本原理ってことでいいかな

次に来る文字を予測するLSTMでも試したけど、こっちの方が意味が通じる
パラメータ調整をミスってるのもあると思うけど、学習に時間かかりすぎるので却下
'''

# coding:utf-8
from janome.tokenizer import Tokenizer
import os, re, json, random

#　dict_file = 'bot_dic.json'      # ゼロからbot用の辞書を作っていきたい場合はこちらを有効にしてdazai.jsonをコメントアウトする。bot_dic.jsonは作られるから大丈夫
dict_file = 'dazai.json'        # 太宰治bot用の辞書

dic = {}                        # global変数の使い方の練習
tokenizer = Tokenizer()         # janome

# 辞書に単語を記録する
def register_dic(words):
    global dic                  # global変数の使い方の練習
    if len(words) == 0: return
    tmp = ['@']
    for i in words:
        word = i.surface
        if word == '' or word == '\r\n' or word == '\n': continue
        tmp.append(word)
        if len(tmp) < 3: continue
        if len(tmp) > 3: tmp = tmp[1:]
        set_word3(dic, tmp)
        if word == '。' or word == '?':
            tmp = ['@']
            continue
    # 辞書を更新するごとにファイルへ保存
    json.dump(dic, open(dict_file,'w', encoding='utf-8'))

# 三要素のリストを辞書として登録
def set_word3(dic, s3):
    w1, w2, w3 = s3
    if not w1 in dic: dic[w1] = {}
    if not w2 in dic[w1]: dic[w1][w2] = {}
    if not w3 in dic[w1][w2]: dic[w1][w2][w3] = 0
    dic[w1][w2][w3] += 1

# 作文する
def make_sentence(head):
    if not head in dic: return ''
    ret = []
    if head != '@': ret.append(head)        
    top = dic[head]
    w1 = word_choice(top)
    w2 = word_choice(top[w1])
    ret.append(w1)
    ret.append(w2)
    while True:
        if w1 in dic and w2 in dic[w1]:
            w3 = word_choice(dic[w1][w2])
        else:
            w3 = ''
        ret.append(w3)
        if w3 == '。' or w3 == '？' or w3 == '': break
        w1, w2 = w2, w3
    return ''.join(ret)

def word_choice(sel):
    keys = sel.keys()
    return random.choice(list(keys))

# チャットボットに返答させる
def make_reply(text):
    # まず単語を学習する
    if text[-1] != '。': text += '。'
    words = tokenizer.tokenize(text)
    register_dic(words)
    # 辞書に単語があれば、そこから話す
    for w in words:
        face = w.surface
        ps = w.part_of_speech.split(',')[0]
        if ps == '感動詞':
            return face + '。'
        if ps == '名詞' or ps == '形容詞':
            if face in dic: return make_sentence(face)
    return make_sentence('@')

# 辞書があれば最初に読み込む
if os.path.exists(dict_file):
    dic = json.load(open(dict_file,'r'))

# メイン処理
# 入力に対して返答を返す処理
def main():
    print('')
    txt = 'chat_text'
    while txt != 0:
        txt = input('> ')
        # 終了条件
        if txt == 'exit' or txt == 'end' or txt == 'END' or txt == 'EXIT' or txt == '終了':
            return
        res = make_reply(txt)
        print(res)
        
main()