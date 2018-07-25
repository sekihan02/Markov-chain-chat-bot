# utf-8
"""
青空文庫に公開中の作品を作家別に一括ダウンロードできるサイト
http://keison.sakura.ne.jp/index.html
から太宰治の作品一覧をダウンロードする。
"""
import os.path, urllib.request as req
import re, zipfile, sys

# 夏目漱石の作品一覧のダウンロード
local = 'dazai.zip'
url = 'http://keison.sakura.ne.jp/tagyou/dazai.zip'

if not os.path.exists(local):
    print('開始')
    req.urlretrieve(url, local)
    print('終了')

# ZIPファイルの中のテキストファイルを読む
# z = zipfile.ZipFile(local, 'r') # zipファイルを読み込む
# 展開する
# z.extractall(path=os.path.dirname(local))
