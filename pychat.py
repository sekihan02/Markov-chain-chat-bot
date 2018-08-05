# utf-8

import sys, codecs, random

# コマンドライン引数
argvs = sys.argv    # 引数のリスト取得
argc = len(argvs)   # 引数の個数

# HASH関数の添字の上限
HashMax = 14705
# 学習した単語を記憶する数
Elno = 3

KeyWord = {}
Ev = {}
Response = {}
Res4w = {}
LogMan = {}
LogCom = {}

Filename1 = '/home/holy/anchat.dic'
Filename2 = '/home/holy/anchat.bak'
Filename3 = '/home/holy/sample.txt'

'''
最大99回会話をできる
# ムノウの出力:文字列変数 Messageに対して
# 親の入力:文字列変数 Answerを記憶する
# 記憶した(学習した)文を記憶するリスト:KeyWord, Response, Res4wに記憶する
'''
def Chat(HashMax):
    Res = 1
    # ログの初期化
    for i in range(1, 99):
        LogMan[i] = ''
        LogCom[i] = ''
    Message = 'あなたの名前は？相談事は？'
    while Res < 100:
        print('-Py',Message)
        Answer = input('>')
        # 会話(Answer)が99回目か、'exit', 'quit', 'bye'が入力されたら終了
        if Answer == '99' or Answer == 'exit' or Answer == 'bye' or Answer == 'quit':
            Res = 99
            break
        Answer = WordEnd(Answer)
        LearnWord = Learning(Message, HashMax)
        LearnWord = WordEnd(LearnWord)
        Message = Reaction(LearnWord, Answer, HashMax)
        ChatLog(Message, Answer)
        # 親が三回連続同じ返答の時話題を変える
        if LogMan[99] == LogMan[98] and LogMan[98] == LogMan[97]:
            Message = StrChg(HashMax)
            # ムノウが前と同じ回答の時話題を変える
        if LogCom[99] == LogCom[98]:
            Message = StrChg(HashMax)
        Res = Res + 1
    return Res4w

def MakeDic(HashMax):
    try:
        hFile = codecs.open(Filname3,'r')
    except IOError:
        print("* sample.txt is not found.")
        quit()
    else:
        # 文字ストリームが空白になるまで繰り返す。
        for sOneLine in hFile.readlines():
            sOneLine = AozoraRuby(sOneLine)
            print(sOneLine)
            Length = len(sOneLine)
            Message = ""
            PrePos = 0
            MaruPos = sOneLine.find("。")
            # 「。」がなくなるまで繰り返す。
            while MaruPos > 0:
                # 一行の文字数を数える
                Answer = sOneLine[PrePos:MaruPos]
                Answer = WordEnd(Answer)
                LearnWord = Learning(Message, Answer, HashMax)
                LearnWord = WordEnd(LearnWord)
                Message = Reaction(LearnWord, Answer, HashMax)
                Message = AozoraRuby(Message)
                print()
                print("> Answer : ", Answer)
                print('>Message :', Message)
                print()
                # 次の行のためにリセット
                sOneLine = sOneLine[MaruPos + 1:len(sOneLine) -1]
                MaruPos = sOneLine.find('。')
                hFile.close()

def cmdLine(HashMax, Res):
    Message = argvs[1]
    Answer = argvs[1]
    if Res > 2:
        Answer = argvs[2]
    Answer = Answer.replace(',','')
    LearnWord = Learning(Message, Answer, HashMax)
    LearnWord = WordEnd(LearnWord)
    Message = Reaction(LearnWord, Answer, HashMax)
    Message = AozoraRuby(Message)
    print(Message)

# 学習
def Learning(Message, Answer, HashMax):
    SelectWord = WordSelect(Answer)
    Key4w = SelectWord[0:4]
    l = 0
    for i in range(10):
        j = FNK(HASH(Key4w), i, HashMax)
        # 初めてのハッシュ値の場合、そのまま登録
        if not j in KeyWord:
            KeyWord[j] = Key4w
            Ev[j, 0] = l
            Response[j, 0] = Answer
            SelectWord = WordSelect(Answer)
            Res4w[j, 0] = SelectWord[0:4]
            # 後続の項目についても作っておく
            for k in range(1, Elno):
                Ev[j, k] = 0
                Response[j, k] = ""
                Res4w[j, k] = ""
            l = 1
            break
        # すでに登録のあるハッシュ値の場合
        if l == 0:
            # さらにその近傍をテキトーに選ぶ(そのハッシュの返事に凝り固まらないような仕組み)
            j = FNK(HASH(Key4w), int(random.random() * 10), HashMax)
            if not j in KeyWord:
                # まだ全くないなら新た に項目を作る
                KeyWord[j] = Key4w
                Ev[j, 0] = 1
                Response[j, 0] = Answer
                SelectWord = WordSelect(Answer)
                Res4w[j, 0] = SelectWord[0:4]
                for k in range(1,Elno):
                    Ev[j, k] = 0
                    Response[j, k] = ""
                    Res4w[j, k] = ""
                break
                # 何かしら登録されているが評価係数が0である場合、登録
                if Ev[j, 0] == 0 and len(Response[j, 0]) > 0:
                    KeyWord[j] = Key4w
                    Ev[j, 0] = 1 
                    # Response[ j, 0] = Answer
                    SelectWord = WordSelect(Answer)
                    Res4w[j, 0] = SelectWord[0:4]
                    # 評価係数はあるが何も登録されてない場合、登録
                elif Ev[j, 0] > 0 and len( Response[j, 0]) == 0:
                    KeyWord[j] = Key4w
                    Ev[j, 0] = 1
                    Response[j, 0] = Answer
                    SelectWord = WordSelect(Answer)
                    Res4w[j, 0] = SelectWord[0: 3]
                else:
                    # 空きのある(Ev = 0)に入れるようにする。
                    for k in range(0, Elno):
                        if Ev[j, k] == 0 or len(Response[j, k]) == 0:
                            KeyWord[j] = Key4w
                            Ev[j, k] = 1
                            Response[j, k] = Answer
                            SelectWord = WordSelect(Answer)
                            Res4w[j, k] = SelectWord[0: 4]
                            l = 2 # このif文を通過したというフラグ
                            break
                            # Ev値0がなければ最小のEv値(つまり配列No.Elno-1)に入れる
                            if l < 2:
                                KeyWord[j] = Key4w
                                Ev[j, Elno - 1] = 1
                                Response[j, Elno - 1] = Answer
                                SelectWord = WordSelect(Answer)
                                Res4w[j, Elno - 1] = SelectWord[0:4]
                # Evの大きい順にソート
                for m in range( 0, Elno):
                    for n in range(m, Elno):
                        if Ev[j, m] < Ev[ j, n]:
                            itmp = Ev[j, m]
                            stmp = Response[j, m]
                            tmp4 = Res4w[j, m]
                            Ev[j, m] = Ev[j, n]
                            Response[j, m] = Response[j, n]
                            Res4w[j, m] = Res4w[j, n]
                            Ev[j, n] = itmp
                            Response[j, n] = stmp
                            Res4w[j, n] = tmp4
                return SelectWord

# 応答
def Reaction(LearnWord, Answer, HashMax):
    l = -1
    # いい条件がある/なしフラグ(- 1:ヒットなし,0:ランダム選択,+1:妥当な選択)
    k = 0
    Message = ""
    Len4w = LearnWord[0: 4]
    # 第1段階:Hash値のあたりを探す
    for j in range(10):
        i = FNK(HASH(Len4w), j, HashMax)
        # そのハッシュ値の行が存在する場合
        if i in KeyWord:
            try:
                # 中身のある配列Ev()の最大の添値を調べる
                for h in range(Elno - 1, -1, -1):
                    if Ev[ i, h] > 0:
                        k = int(random. random() * (h + 1))
                        Message = Response[i, k]
                        if Message != Answer:
                            # これはという答えなので+1加点しとく
                            Ev[i, k] = Ev[i, k] + 1
                            l = 1
                        break
            except ValueError:
                pass # 何もしない
        if l >= 0:
            break
        # 第2段階:パタンにマッチするKeyWordを探す
        if l < 0 and len(Len4w) > 0:
            # KeyWordそのものを返答するんじゃなくResponseを返すのがコツ
            for i in range(1, HashMax):
                if i in KeyWord:
                    try:
                        KeyWord[i].index(Len4w)
                        # 中身のある配列Ev()の最大の添値を調べる
                        for h in range(Elno):
                            if len( Response[i, h]) > 0:
                                Message = Response[i, h]
                                if Message != Answer:
                                    l = 0
                                    break
                    except ValueError:
                        pass #何もしない
                    if l >= 0:
                        break
        #第3段階:パタンにマッチするResponseを探す
        if l < 0 and len(Len4w) > 0:
            for i in range(1, HashMax):
                if i in KeyWord:
                    for h in range(Elno):
                        try:
                            Response[i, h].index(Len4w)
                            Message = Response[i, h]
                            if Message != Answer:
                                l = 0
                                break
                        except ValueError:
                            pass # 何もしない
                    if l >= 0:
                        break
        # 第4段階:ひっかける要素がない => オウム返し
        k = 0
        if l < 0 and len(LearnWord) <= 4:
            Message = LearnWord + "？"
            # 中身のある配列Responseを適当に選ぶ
            for i in range(int(random.random() * HashMax) - 1, 1, -1):
                if i in KeyWord:
                    for h in range(Elno - 1, 0, -1):
                        if len(Response[i, h]) > 0:
                            k = int(random.random() * h)
                            Message = Message + Response[i, k]
                            l = 0
                            break
                if l >= 0:
                    break
        # 第5段階:覚えた単語が4文字以下なら => 話題を変える
        if l < 0 or not i in KeyWord:
            Message = StrChg(HashMax)
        else: 
        # Evの大きい順にソート。評価係数が大きい方が辞書に残り易い
            for m in range(Elno):
                for n in range(m, Elno):
                    if Ev[i, m] < Ev[i, n]:
                        itmp = Ev[i, m]
                        stmp = Response[i, m]
                        tmp4 = Res4w[i, m]
                        Ev[i, m] = Ev[i, n]
                        Response[i, m] = Response[i, n]
                        Res4w[i, m] = Res4w[i, n]
                        Ev[i, n] = itmp
                        Response[i, n] = stmp
                        Res4w[i, n] = tmp4
        return Message 
#単語選びのサブルーチン
def WordSelect(sWord):
    TempWord = "None"
    SelectWord = "None"
    StaPos = 0
    EndPos = 0
    # マッチング用のひらがな文字列
    sHira = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろがぎぐげござじずぜぞだじづでぞばびぶべぼぱぴぷぺぽをん、！？"
    # 全体の文字数を知っておく。
    Length = len(sWord)
    # 先頭から１文字づつスキャン
    while StaPos < Length:
        # 綴りの開始位置 
        for i in range(StaPos, Length):
            ScanFlag = sHira.find(sWord[i])
            # 全角ひらがな以外ならブレーク 
            if ScanFlag < 0:
                StaPos = i
                break
            StaPos = i
            # 綴りの終了位置
            for i in range(StaPos + 1, Length):
                ScanFlag = sHira.find(sWord[i])
                # 全角ひらがなならブレーク
                if ScanFlag >= 0:
                    EndPos = i
                    break
                EndPos = i
                # 一連の語を記憶しておく
                if (EndPos - StaPos) > 0:
                    TempWord = sWord[StaPos:EndPos]
                # 綴りの長い語を優先する
                if len(SelectWord) < len(TempWord):
                     SelectWord = TempWord
                StaPos = EndPos + 1 
                #何のワードも見つけられなかったなら4文字にする
                if (TempWord == "None") or (SelectWord == "None"):
                    SelectWord = sWord[0: 4]
                    # 新キーワードをリターンする。
                return SelectWord
            # 乱数作成（線形合同法）
            def FNM(M, HashMax):
                return M - int(M / HashMax) * HashMax
            
            def FNK(iHash, N, HashMax):
                return FNM(iHash + N * N, HashMax)
            # ハッシュ関HASH("4"Word)
            def HASH(sWord):
                # 有効な文頭文字の組み合わせ
                fNorm = 1.0
                LenWord = len(sWord)
                for i in range(0, LenWord):
                    iUcode = ord(sWord[i:i + 1])
                    if (iUcode == 0):
                        return 0
                    fNorm = fNorm * (iUcode / 95222)
                # この倍率は経験値！実験して良さそうな値を見切る
                HASH = int(fNorm * 1000000.0)
                return HASH
            
            def ChatLog(Message, Answer):
                for i in range(1, 99):
                    LogMan[i - 1] = LogMan[i]
                    LogCom[i - 1] = LogCom[i]
                    LogMan[99] = Answer
                    LogCom[99] = Message
                    
            # 話題を変える(辞書のテキトーな行のKeyWordについて聞く)
            def StrChg(HashMax):
                Res = ""
                while(len(Res) < 1):
                    i = int(random.random() * HashMax)
                    if i in KeyWord:
                        try:
                            Res = WordSelect(Response[i, 0]) + "の話をしましょう"
                        except ValueError:
                            Res = WordSelect(KeyWord[i]) + "の話を聞かせてください"
                        break
                return Res
            # 《 》で囲まれた箇所は切り捨てる
            def AozoraRuby(sOneLine):
                PosS = 0
                Count = 0
                Length = len(sOneLine)
                PosE = Length
                while Count < Length:
                    PosS = sOneLine.find("《")
                    PosE = sOneLine.find("》")
                    if PosS > 0 and PosS < PosE:
                        ForeWord = sOneLine[0:PosS]
                        BackWord = sOneLine[PosE + 1: Length]
                        sOneLine = ForeWord + BackWord
                        Length = len(sOneLine)
                        PosS = 0
                        PosE = Length
                    Count = Count + 1
                return sOneLine
            
            def ReadDic():
                try:
                    # 辞書の最終行まで繰り返す
                    hFile = codecs.open(Filname1,'r')
                except IOError:
                    print("* pychat.dic cannot open, then cannot read.")
                    quit()
                else:
                    for sOneLine in hFile.readlines():
                        # 文頭から改行箇所までの文字ストリームを一行として取り込む
                        Ele = sOneLine.split(",")
                        Hash = int(Ele[0])
                        KeyWord[Hash] = Ele[1]
                        Ev[Hash, 0] = int(Ele[2])
                        Response[Hash, 0] = Ele[3]
                        Res4w[Hash, 0] = Ele[4]
                        Ev[Hash, 1] = int(Ele[5])
                        Response[Hash, 1] = Ele[6]
                        Res4w[Hash, 1] = Ele[7]
                        Ev[Hash, 2] = int(Ele[8])
                        Response[Hash, 2] = Ele[9]
                        Res4w[Hash, 2] = Ele[10].rstrip("\ n")
                    hFile.close()
                # 辞書ファイルのバックアップを取っておく
                bFile = codecs.open(Filname2,'w+')
                for i in range(0,HashMax):
                    if i in KeyWord:
                        sOneLine = str(i)+","+ KeyWord[i]+","+ str(Ev[i, 0])+","+ Response[i, 0]+","+ Res4w[i, 0]+","+ str(Ev[i, 1])+","+ Response[i, 1]+","+ Res4w[i, 1]+","+ str(Ev[i, 2])+","+ Response[i, 2]+","+ Res4w[i, 2]+"\n"
                        bFile.write(sOneLine)
                bFile.close()
            def WriteDic():
                try:
                    hFile = codecs.open(Filname1,'w+')
                except IOError:
                    print("* pychat.dic cannot open, then cannot write.")
                    quit()
                else:
                    for i in range(0, HashMax):
                        if i in KeyWord:
                            sOneLine = str(i)+","+ KeyWord[i]+","+ str(Ev[i, 0])+","+ Response[i, 0]+","+ Res4w[i, 0]+","+ str(Ev[i, 1])+","+ Response[i, 1]+","+ Res4w[i, 1]+","+ str(Ev[i, 2])+","+ Response[i, 2]+","+ Res4w[i, 2]+"\n"
                            hFile.write(sOneLine)
                            hFile.close()
            # 回答文中＆文末の整理
            def WordEnd(Answer):
                Answer = Answer.replace(",","、")
                if len(Answer) < 2:
                    return Answer
                if Answer[len(Answer) - 1] == "?":
                    Answer = Answer[0:len(Answer) - 1]
                if Answer[len(Answer) - 1] == "「":
                    Answer = Answer[0:len(Answer) - 1]
                if Answer[len(Answer) - 1] == "”":
                    Answer = Answer[0:len(Answer) - 1]
                if Answer[len(Answer) - 1] == "（":
                    Answer = Answer[0:len(Answer) - 1]
                if Answer[len(Answer) - 1] == "《":
                    Answer = Answer[0:len(Answer) - 1]
                if Answer[len(Answer) - 1] == "『":
                    Answer = Answer[0:len(Answer)- 1]
                if Answer[len(Answer) - 1] == "【":
                    Answer = Answer[0:len(Answer) - 1]
                if Answer[len(Answer) - 1] == "？":
                    Answer = Answer[0:len(Answer) - 1]
                if Answer[len(Answer) - 1] == "。":
                    Answer = Answer[0:len(Answer) - 1]
                if Answer[len(Answer) - 1] == "、":
                    Answer = Answer[0:len(Answer) - 1]
                if Answer[len(Answer) - 1] == "～":
                    Answer = Answer[0:len(Answer) - 1]
                if Answer[len(Answer) - 1] == "ー":
                    Answer = Answer[0:len(Answer) - 1]
                if Answer[len(Answer) - 1] == "！":
                    Answer = Answer[0:len(Answer) - 1]
                if Answer[len(Answer) - 1] == "!":
                    Answer = Answer[0:len(Answer) - 1]
                if Answer[len(Answer) - 1] == "ｗ":
                    Answer = Answer[0:len(Answer) - 1]
                if Answer[0] == " ":
                    Answer = Answer[1:len(Answer)]
                if Answer[0] == "?":
                    Answer = Answer[1:len(Answer)]
                if Answer[0] == "　":
                    Answer = Answer[1:len(Answer)]
                if Answer[0] == "」":
                    Answer = Answer[1:len(Answer)]
                if Answer[0] == "”":
                    Answer = Answer[1:len(Answer)]
                if Answer[0] == "）":
                    Answer = Answer[1:len(Answer)]
                if Answer[0] == "》":
                    Answer = Answer[1:len(Answer)]
                if Answer[0] == "』":
                    Answer = Answer[1:len(Answer)]
                if Answer[0] == "】":
                    Answer = Answer[1:len(Answer)]
                if Answer[0] == "？":
                    Answer = Answer[1:len(Answer)]
                if Answer[0] == "。":
                    Answer = Answer[1:len(Answer)]
                if Answer[0] == "、":
                    Answer = Answer[1:len(Answer)]
                if Answer[0] == "～":
                    Answer = Answer[1:len(Answer)]
                if Answer[0] == "ー" :
                    Answer = Answer[1:len(Answer)]
                if Answer[0] == "！":
                    Answer = Answer[1:len(Answer)]
                if Answer[0] == "!":
                    Answer = Answer[1:len(Answer)]
                if Answer[0] == "ｗ":
                    Answer = Answer[1:len(Answer)]
                return Answer
# Main
if (argc < 2):
    # 引数がない場合
    print("--- Talking Machine ---")
    print(" 新しく 始める .... 1")
    print(" 保存 し て た データ を 使う .... 2")
    print(" テキスト を 読み 辞書 生成 .... 3")
    print(" 終了 .... それ 以外")
    print(" Input 1 or 2 ? ")
    sMenu = input(">")
    if sMenu == "1":
        Chat(HashMax)
        WriteDic()
        print("- Py: Bye")
    elif sMenu == "2":
        ReadDic()
        Chat(HashMax)
        WriteDic()
        print("- Py: Bye, Bye")
    elif sMenu == "3":
        print(" (Caution!)辞書をBackupしておくことを勧めます")
        print(" [Go = y /or other] > ")
        Ans = input()
        if Ans == "y" or Ans == "Y":
            ReadDic()
            MakeDic(HashMax)
            WriteDic()
            print("- Py: Complete")
        else:
            print("- Py: See You Again 〜")
    else:
        # 引数がある場合
        ReadDic()
        cmdLine(HashMax, argc)
        # writeDic()
