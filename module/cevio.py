from win32com import client
import json
import re

class Cevio:
    """
    CeVIO 外部連携API
    CeVIO Component Object Model -> Python
    """

    # CeVIO AI 起動パラメータ
    _ai_params = {
        "name" : "AI",
        "talk_module" : "CeVIO.Talk.RemoteService2.Talker2V40",
        "control_module" : "CeVIO.Talk.RemoteService2.ServiceControl2V40",
        "text_count" : 200 # 最大200文字
    }

    # CeVIO CCS 起動パラメータ
    _ccs_params = {
        "name" : "Creative Studio",
        "talk_module" : "CeVIO.Talk.RemoteService.TalkerV40",
        "control_module" : "CeVIO.Talk.RemoteService.ServiceControlV40",
        "text_count" : 100 # 最大100文字
    }

    def __init__(self, mode:str="AI") -> None:
        """
        CeVIO 起動
        """

        # パラメータ設定
        if (mode == "AI"):
            self._params = self._ai_params
        elif (mode == "CCS"):
            self._params = self._ccs_params
        else:
            raise CevioException("mode must be 'AI' or 'CCS'.")

        # APIオブジェクト生成
        self.talk = client.Dispatch(self._params["talk_module"])
        self.control = client.Dispatch(self._params["control_module"])

        # start CeVIO AI
        self.start_cevio()
        # デフォルトはAvailableCastsの一覧の最初
        self.talk.Cast = self.talk.AvailableCasts.At(0)
        if (self.talk.Cast is None):
           raise CevioException(f"Initial cast cannot be selected. If the specified character does not exist in the following cast list, please check for a license. [{','.join(self.get_available_cast())}]")
        print(f"Cast : {self.talk.Cast}")

    def get_available_cast(self):
        """
        利用可能なキャスト一覧を出力

        Returns:
            result (list): 利用可能なキャスト名

        Raises :
          CevioException : CeVIOが起動していない場合の例外
        """

        # CeVIO起動チェック
        self._check_cevio_status()

        castlist = self.talk.AvailableCasts
        result = []
        for i in range(0,castlist.Length):
            result.append(castlist.At(i))
        return result

    def get_cast(self):
        """
        現在のキャストを出力

        Returns:
            cast (str): 現在のキャスト名

        Raises :
            CevioException : CeVIOが起動していない場合の例外
        """
        return self.talk.Cast

    def set_cast(self, name:str):
        """
        キャストの設定

        Args:
            name (str): キャスト名

        Raises :
          CevioException : CeVIOが起動していない場合の例外
        """

        # CeVIO起動チェック
        self._check_cevio_status()

        castlist = self.get_available_cast()
        if (name in castlist):
            self.talk.Cast = name
        else:
            print(f"Cast is not included in the list. Please select from the following : [{''.join(castlist)}]")

    def get_talk_params(self):
        """
        コンディションを取得(キャストに関わらず共通)

        Returns:
            talkparams (dict): コンディション設定一覧

        Raises :
          CevioException : CeVIOが起動していない場合の例外
        """

        # CeVIO起動チェック
        self._check_cevio_status()

        talkparams = {
            "Volume":self.talk.Volume,  # 音の大きさ(Int)
            "Speed":self.talk.Speed,  # 話す速さ(Int)
            "Tone":self.talk.Tone,  # 音の高さ(Int)
            "ToneScale":self.talk.ToneScale,  # 抑揚(Int)
            "Alpha":self.talk.Alpha  # 声質(Int)
        }
        return talkparams

    def set_talk_params(self, params:dict):
        """
        トークパラメータの設定

        Args:
            params (dict): コンディション設定一覧
        """
        for key in params.keys():
            self.set_talk_param(key, params[key])

    def set_talk_param(self, talktype:str, value:int):
        """
        コンディションの設定

        Args:
            talktype (str): コンディションの指定
            value (int): コンディションの値

        Raises :
            CevioException : CeVIOが起動していない場合の例外
            ValueError : 値が数値でない場合
        """
        default_params = self.get_talk_params()
        trans_dict = {
            "大きさ":"Volume",
            "速さ":"Speed",
            "高さ":"Tone",
            "抑揚":"ToneScale",
            "声質":"Alpha"
        }
        changed_params = {}

        # コンディションに和名が含まれている場合
        if (talktype in trans_dict.keys()):
            # talkTypeを英語名に上書き
            talktype = trans_dict[talktype]
        # コンディション一覧に含まれているもののみ
        if (talktype in trans_dict.values()):
            # 整数値のみ
            if (self._is_int(value)):
                if (int(value) >= 0 and int(value) <= 100):
                    changed_params[talktype] = int(value)
                    self._change_talk_param(talktype, changed_params[talktype])
                else:
                    print("value must be an integer between 0 and 100.")
            else:
                print("value must be an integer between 0 and 100.")
        else:
            print(f"Condition is not included in the list. Please select from the following: [{','.join(trans_dict.values())}]")

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

        Raises :
          CevioException : CeVIOが起動していない場合の例外
        """

        # CeVIO起動チェック
        self._check_cevio_status()

        # 感情パラメータ取得
        castparams = self.talk.Components
        emotionparams = {}
        # ループ内で名前と値の取得
        for i in range(0,castparams.Length):
            tmp = castparams.At(i)
            emotionparams[tmp.Name] = tmp.Value
        return emotionparams

    def set_cast_params(self, emotions:dict):
        for key in emotions.keys():
            self.set_cast_param(key,emotions[key])

    def set_cast_param(self,emotion,value):
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
                    print("value must be an integer between 0 and 100.")
            else:
                print("value must be an integer between 0 and 100.")
        else:
            print("emotion is not included in the list. Please select it below.")
            print(",".join(default_params.keys()))
        # パラメータ差分表示
        changed_params = self.get_cast_params()
        for key in changed_params.keys():
            if (default_params[key] != changed_params[key]):
                print(f"{key}: {default_params[key]} -> {changed_params[key]}")

    def start_cevio(self):
        """
        CeVIO 起動

        Results:
            result (int): 起動結果(0以外はエラー)
        """
        # CeVIO が実行中か確認し、起動していない場合のみCeVIO AI/CCSを起動
        if not (self.control.IsHostStarted):
            result = self.control.StartHost(False)
            if result == 0:
                print(f"CeVIO ${self._params['name']} Started.")
            elif result == -1:
                raise CevioException("Installation status is unknown.")
            elif result == -2:
                raise CevioException("Unable to find executable file.")
            elif result == -3:
                raise CevioException("Failed to start the process.")
            elif result == -4:
                raise CevioException("Application terminates with an error after starting.")
            else:
                raise CevioException(f"Unknown Error code is {result}.")
        else:
            result = 0

        return result

    def speak(self,text):
        """
        セリフの再生

        Args:
            text (str): セリフ

        Raises :
          CevioException : CeVIOが起動していない、もしくは利用可能なキャスト一覧に含まれていない場合の例外
        """

        # CeVIO起動チェック
        self._check_cevio_status()

        # CeVIO AI は200文字、CCS は100文字までのため、別途文字の切り詰め
        speech_list = self._text_split(text,self._params["text_count"])
        for speech in speech_list:
            print(f"{self.talk.Cast} > {speech}")
            result = self.talk.Speak(speech)
            result.Wait()

    def _text_split(self,text,nums):
        # 文章の切れる部分で分割
        text = re.sub(r"([、|。|，|．|,|.|・|\r\n|\n|\t| |　])",r"\1<SPLITED_TEXT>",text)
        splited_text = re.split("<SPLITED_TEXT>",text)
        return_text = [""]
        # 可能な限り文字詰め(CeVIOの文字数制限)
        # 文字数が制限以下ならそのまま、制限以上なら分割
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
        self.set_talk_param("速さ", 46)
        self.set_cast_param("元気", 50)
        self.set_cast_param("普通", 70)
        self.set_cast_param("怒り", 72)
        self.set_cast_param("哀しみ", 26)

    def read_json(self,filepath:str):
        """
        設定ファイル読み込み & キャラクター設定

        Raises :
          CevioException : CeVIOが起動していない、もしくは利用可能なキャスト一覧に含まれていない場合の例外
        """

        # CeVIO起動チェック
        self._check_cevio_status()

        # JSON設定ファイル読み込み
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                params = json.load(f)
        except FileNotFoundError as e:
            raise CevioException(f"'{filepath}'' File not found")
        # 利用可能なキャスト一覧に含まれないキャラクターを選択した場合、エラー
        if params["Cast"] not in self.get_available_cast():
            raise CevioException(f"{params['Cast']} is not included in available cast.")

        # Cast設定
        self.set_cast(params["Cast"])

        # コンディション設定
        try:
            self.set_talk_params(params["talk"])
        except Exception:
            print(f"Condition is an invalid value.")

        # 感情設定
        try:
            self.set_cast_params(params["Emotion"])
        except Exception:
            print(f"Emotion is an invalid value.")

    def _check_cevio_status(self) -> None:
        """
        CeVIO起動状態チェック

        Raises :
          CevioException : CeVIOが起動していない場合の例外
        """
        if not (self.control.IsHostStarted):
            raise CevioException("CeVIO is not running.")

class CevioException(Exception):
    '''
    例外：CeVIO処理全般エラー
    '''
    def __init__(self, message) ->None:
        self._messege = f'Error : {message}'

    def __str__(self) -> None:
        return self._messege