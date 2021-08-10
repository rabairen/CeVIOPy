from win32com import client
import re
import sys

class cevioapi:
    """
    CeVIO AI 外部連携API
    CeVIO Component Object Model -> Python
    """
    talk = client.Dispatch("CeVIO.Talk.RemoteService2.Talker2")
    control = client.Dispatch("CeVIO.Talk.RemoteService2.ServiceControl2")
    def __init__(self):
        # start CeVIO AI
        if (self.start_cevio() != 0):
            sys.exit(1)
        # デフォルトはAvailableCastsの一覧の最初
        self.talk.Cast = self.talk.AvailableCasts.At(0)
        print(f"現在のキャスト : {self.talk.Cast}")
    
    def get_available_cast(self):
        """
        利用可能なキャスト一覧を出力

        Returns:
            result (list): 利用可能なキャスト名
        """
        castlist = self.talk.AvailableCasts
        result = []
        for i in range(0,castlist.Length):
            result.append(castlist.At(i))
        return result

    def set_cast(self, name:str):
        """
        キャストの設定

        Args:
            name (str): キャスト名
        """
        castlist = self.get_available_cast()
        if (name in castlist):
            self.talk.Cast = name
        else:
            print("Castが一覧に含まれていません。以下から選択してください。")
            print(",".join(castlist))

    def get_talk_params(self):
        """
        コンディションを取得(キャストに関わらず共通)
        
        Returns:
            talkparams (dict): コンディション設定一覧
        """
        talkparams = {
            "Volume":self.talk.Volume,  # 音の大きさ(Int)
            "Speed":self.talk.Speed,  # 話す速さ(Int)
            "Tone":self.talk.Tone,  # 音の高さ(Int)
            #"ToneScale":self.talk.ToneScale,  # 抑揚(何故か動かない)
            "Alpha":self.talk.Alpha  # 声質(Int)
        }
        return talkparams

    def set_talk_params(self, talktype:str, value:int):
        """
        コンディションの設定
        
        Args:
            talktype (str): コンディションの指定
            value (int): コンディションの値
        """
        default_params = self.get_talk_params()
        trans_dict = {
            "大きさ":"Volume",
            "速さ":"Speed",
            "高さ":"Tone",
            #"抑揚":"ToneScale",
            "声質":"Alpha"
        }
        changed_params = {}
        # コンディション一覧に含まれているもののみ
        if (talktype in trans_dict):
            # 整数値のみ
            if (self._is_int(value)):
                if (int(value) >= 0 and int(value) <= 100):
                    changed_params[trans_dict[talktype]] = int(value)
                    self._change_talk_param(trans_dict[talktype], changed_params[trans_dict[talktype]])
                else:
                    print("valueは0～100の整数値を渡してください")
            else:
                print("valueは0～100の整数値を渡してください")
        else:
            print("Conditionが一覧に含まれていません。以下から選択してください。")
            print(",".join(default_params.keys()))
        # パラメータ差分表示
        for key in changed_params.keys():
            if (default_params[key] != changed_params[key]):
                print(f"{key}: {default_params[key]} -> {changed_params[key]}")
    
    def _is_int(self, value):
        try:
            # int型かを判定
            int(value)
        except ValueError:
            return False
        else:
            return True

    def _change_talk_param(self, talktype, value):
        # コンディション設定
        if talktype == "Volume":
            self.talk.Volume = value
        elif talktype == "Speed":
            self.talk.Speed = value
        elif talktype == "Tone":
            self.talk.Tone = value
        elif talktype == "ToneScale":
            self.talk.ToneScale = value
        elif talktype == "Alpha":
            self.talk.Alpha = value

    def get_cast_params(self):
        """
        感情パラメータを取得(キャストによって変化)

        Returns:
            emotionparams (dict): コンディション設定一覧
        """
        # 感情パラメータ取得
        castparams = self.talk.Components
        emotionparams = {}
        # ループ内で名前と値の取得
        for i in range(0,castparams.Length):
            tmp = castparams.At(i)
            emotionparams[tmp.Name] = tmp.Value
        return emotionparams

    def set_cast_params(self,emotion,value):
        """
        感情パラメータの設定

        Args:
            emotion (str): 感情(日本語)の指定
            value (int): 感情の値
        """
        default_params = self.get_cast_params()
        # パラメータがあるか判定
        if (emotion in default_params):
            # 整数値のみ
            if (self._is_int(value)):
                if (int(value) >= 0 and int(value) <= 100):
                    self.talk.Components.ByName(emotion).Value = int(value)
                else:
                    print("valueは0～100の整数値を渡してください")
            else:
                print("valueは0～100の整数値を渡してください")
        else:
            print("emotionが一覧に含まれていません。以下から選択してください。")
            print(",".join(default_params.keys()))
        # パラメータ差分表示
        changed_params = self.get_cast_params()
        for key in changed_params.keys():
            if (default_params[key] != changed_params[key]):
                print(f"{key}: {default_params[key]} -> {changed_params[key]}")

    def start_cevio(self):
        """
        CeVIO AI 起動

        Results:
            result (int): 起動結果(0以外はエラー)
        """
        # CeVIO AIが実行中か確認し、起動していない場合のみCeVIO AIを起動
        if not (self.control.IsHostStarted):
            result = self.control.StartHost(False)
            if result == 0:
                print("CeVIO AI Started.")
            elif result == -1:
                print("Error: Installation status is unknown.")
            elif result == -2:
                print("Error: Unable to find executable file.")
            elif result == -3:
                print("Error: Failed to start the process.")
            elif result == -4:
                print("Error: Application terminates with an error after starting.")
            else:
                print(f"Unknown Error: Error code is {result}.")
        else:
            result = 0
        
        return result

    def speak(self,text):
        """
        セリフの再生

        Args:
            text (str): セリフ
        """
        # CeVIO AI は200文字までのため、別途文字の切り詰め
        speech_list = self._text_split(text,200)
        # 出だしは発音が聞こえないため、隠し文字を付加
        speech_list.insert(0, "っ")
        for speech in speech_list:
            print(f"{self.talk.Cast} > {speech}")
            result = self.talk.Speak(speech)
            result.Wait()

    def _text_split(self,text,nums):
        # 文章の切れる部分で分割
        text = re.sub(r"([、|。|，|．|,|.|・|\r\n|\n|\t| |　])",r"\1<SPLITED_TEXT>",text)
        splited_text = re.split("<SPLITED_TEXT>",text)
        return_text = [""]
        # 可能な限り200文字詰め(CeVIO AIの文字数制限)
        # 「、」「。」などで分けられた文章が200文字以上の場合、そのまま渡すため事前に切り詰める必要あり
        for t in splited_text:
            if len(return_text[len(return_text)-1]+t) <= nums:
                return_text[len(return_text)-1] += t
            else:
                return_text.append(t)
        return return_text

    def make_speech_mode(self):
        """
        サンプルスピーチ設定
        """
        # さとうささら用
        self.set_talk_params("速さ", "46")
        self.set_cast_params("元気", 50)
        self.set_cast_params("普通", 70)
        self.set_cast_params("怒り", 72)
        self.set_cast_params("哀しみ", 26)
