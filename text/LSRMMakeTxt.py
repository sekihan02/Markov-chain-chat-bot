# utf-8
'''
分かち書きした太宰治の作品一覧を使い
以下のサンプルコード文章に手を加えつつ文章をつくる
https://github.com/keras-team/keras/blob/master/examples/lstm_text_generation.py

参考にした解説
KerasのSingle-LSTM文字生成サンプルコードを解説
https://qiita.com/YankeeDeltaBravo225/items/487dbfa1bef02bcfb84c

https://github.com/YankeeDeltaBravo225/lstm_text_generation_comment/blob/master/lstm_text_generation_refactored.py
'''

from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM
from keras.optimizers import RMSprop        # RMSprop手法名
from keras.utils.data_utils import get_file
import numpy as np
import random, sys                          # 乱数の発生とファイルのパス取得

# 使うファイル名をバイナリデータとして開く
path = "./dazai.wakati"                     # ./が必要な理由がいまいちわからない、macだから？
with open(path, 'rb') as t:
    text = t.read().decode('utf-8')                         # .decode('utf-8') エラーが出た場合は　t.read.().decode('utf-8'とすれば解決するかも

print('コーパスの長さ:', len(text))            # テキストのサイズの取得 文字数の取得

# 1文字を分解して番号をつけ、辞書にする
chars = sorted(list(set(text)))             # 1文字ずつ切り出す
print('使われている文字数', len(chars))        # 重複文字は入らない
char_indices = dict((c, i) for i, c in enumerate(chars))      # 文字から番号 enumerate番号付きのデータを出力する
indices_char = dict((i, c) for i, c in enumerate(chars))      # 番号から文字を引く

# print(char_indices)
# print(indices_char)

'''
多分の理解(間違ってる可能性高い)
この生成ではcharベースで行なっているけど単語ベースで行うことも可能なはず

読み込んだ全テキスト(text) len(text)で取得する。
maxlen 一定の文字数で文字を切り取り、その次に来る文字の関係を(文字がなんなのかを)学習させる。
step 切り取る幅のスライド数

sentences[] 区切った文字数(maxlen)の格納先
next_chars[] 次に来る文字格納する
sentencesとnext_charsをセットで学習させて推定
その際一旦それぞれをベクトル(配列)として格納し、関係性を学習する
'''

# 文と次に来る文字を配列に入れる
maxlen = 20     # テキストをmaaxlen文字で区切る
step = 3        # スライドするステップ数

sentences = []
next_chars = []

# 文章全体についてスライドしながらsentencesとnext_charsを格納する
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])

print('学習する文の数', len(sentences))
# print(len(next_chars))                  # lem(sentences)と同じになるよね

# テキストのベクトル化
# numpyのarray
print('テキストをIDベクトルにします...')

X = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)       # サイズは文章の数, 一つ一つの要素の中にmaxlenのデータを持つ, 各文字に対して辞書のサイズを持つ,データタイプは二つの値しか持たないbool型
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)               # サイズは文章の数, 文章の数分の文字のサイズの指定

# 全ての文章についてarrayの値を更新する
for i, sentence in enumerate(sentences):        # 文章全体についてループする
    for t, char in enumerate(sentence):         # 各文章の中、各文字について処理を行う
        X[i, t, char_indices[char]] = 1         # 文字から番号を引いたところで文字が含む時に1を立てる
    y[i, char_indices[next_chars[i]]] = 1       # 文字が含む時に1を立てる  [ベクトル化処理]

# モデルを定義する(LSTM)
print('モデルを構築します...')
model = Sequential()                        # 連続的なデータを扱うという意味
model.add(LSTM(128, input_shape=(maxlen, len(chars))))          # add : NNのモデルの追加 LSTMのサイズ : 128, shape : 入力するデータの形状は1回の入力のデータと辞書の長さ
model.add(Dense(len(chars)))                # 全結合する(全てのセルを使ったNNを作る。サイズは辞書のサイズ)
model.add(Activation('softmax'))            # 文字の推定をする softmax：出力した値を0〜1に変換する

optimizer = RMSprop(lr=0.01)                # RMSpropアルゴリズムを使用し、学習率は0.01とする
model.compile(loss='categorical_crossentropy', optimizer=optimizer)     # トレーニングの宣言？ 損失関数 categorical_crossentropy：どれくらい離れているか

# トレーニング後、(最後の層を通過した後、)候補の中から値を取り出す
# 選択候補となる配列から値を取り出す
def sample(preds, tempretire=1.0):      # preds : 予想値, 
    preds = np.asarray(preds).astype('float64') # 初期化
    preds = np.log(preds) / tempretire
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)     # 確率
    return np.argmax(probas)                        # もっとも確率の高い(大きな値の)位置の番号を返す

# 学習させて、テキストを生成する・・・を繰り返す
for iteration in range(1, 10):      # 1〜30繰り返す
    print() # 改行の出力
    print('_'*50)
    print('繰り返し回数；',iteration)
    model.fit(X, y, batch_size=128, epochs=1)       # batch_size:1回に挿入するデータの長さ, epoch:全体のデータを何回繰り返すか
    
    # ランダムにテキストのシードを選ぶ
    start_index = random.randint(0, len(text))      # 最初に開始するテキストを決めるための変数の定義  0〜(len(text) - maxlen - 1)の間で決定する

    # 多様性のパラメータごとに文を生成する
    # サンプルデータを出力するためのパラメータを次の四つの中から取り出す
    for diversity in [0.2, 0.5, 1.0, 1.2]:
        print()
        print('-----多様性', diversity)

        # 生成する文章を入れる。最初は空で初期化
        generated = ''
        
        sentence = text[start_index: start_index + maxlen]
        generated += sentence
        print('-----シードを生成しました"' + sentence + '"')
        sys.stdout.write(generated)     # 生成された文章の表示
        
        # シードを元にテキストを自動で生成する
        for i in range(400):            # 順番に文字を足していく
            x = np.zeros((1, maxlen, len(chars)))   # 初期化
            for t, char in enumerate(sentence):
                x[0, t, char_indices[char]] = 1.    # 文字が張っているところのBITを立てる

            # 次に来る文字を予測
            preds = model.predict(x, verbose=0)[0]      # 0番目の予測値を出す
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]        # 番号に相当する文字
            
            # 既存の文に予測した一文字を足す
            generated += next_char
            sentence = sentence[1:] + next_char         # sentenceの更新
            sys.stdout.write(next_char)
            sys.stdout.flush()
        # open('./dazai'+ iteration +'.lstm', 'w', encoding='utf-8').write(sentence)    # 生成結果の出力、いっぱいできるので注意
        # open('./test/dazai.lstm', 'a', encoding='utf-8').write(sentence)     # 事前にこのプログラムファイルと同じ場所にtestディレクトリを作っておけばそこに生成された文章が保存される

        with open('./test/dazaisentence.lstm', "a", encoding="utf-8") as f:
            f.write("".join(sentence))

        with open('./test/dazaigenerated.lstm', "a", encoding="utf-8") as f:
            f.write("".join(generated))

        print() # 改行