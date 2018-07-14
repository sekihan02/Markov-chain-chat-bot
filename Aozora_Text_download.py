# utf-8
"""
青空文庫からzipをダウンロードし、
中身からヘッダーとフッダー、ルビや脚注を削除して
テキストファイルとして保存する。
"""
"""
青空文庫から以下の内容をダウンロード
作品名：	金魚撩乱
作品名読み：	きんぎょりょうらん
著者名：	岡本 かの子
"""
import os.path, urllib.request as req
from janome.tokenizer import Tokenizer
import zipfile, re

local = '1279_ruby_8230.zip'
url = 'https://www.aozora.gr.jp/cards/000076/files/1279_ruby_8230.zip'
txt_name = 'kingyo_ryoran.txt'

# 吾輩は猫であるの場合
# local = '789_ruby_5639.zip'
# url = 'https://www.aozora.gr.jp/cards/000148/files/789_ruby_5639.zip'
# txt_name = 'wagahaiwa_nekodearu.txt'

# 対象ファイルのダウンロード
# 対象ファイルがすでにダウンロードされている場合は実行しない
if not os.path.exists(local):
    print('ダウンロード開始')
    req.urlretrieve(url, local)
    print('完了')

# ZIPファイルの中のテキストファイルを読む
z = zipfile.ZipFile(local, 'r') # zipファイルを読み込む
t = z.open(txt_name, 'r') # テキストを読み込む
bindata = t.read()
text = bindata.decode('shift_jis') # テキストが Shift_jisでデコード

# テキストの先頭にあるヘッダーとフッターを削除
text = re.split(r'\-{5,}',text)[2]
text = re.split(r'底本：', text)[0]
text = text.strip()
# ルビを削除
text = text.replace('｜', '')
text = re.sub(r'《.+?》', '', text)
# テキスト内の脚注を削除
text = re.sub(r'［＃.+?］', '', text)

# ファイルへ保存
with open(txt_name, "w", encoding="utf-8") as f:
    f.write("".join(text))
    # f.write("/n".join(text)) # 一文字ずつ改行する
    