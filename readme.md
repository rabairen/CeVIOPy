# CeVIOPy
## 概要
Python上でCeVIO AIのトーク機能を利用するモジュール群です。


## フォルダ構成
- ceviopy/ (**推奨**)
    - cevio.py
        - CeVIO AI、CeVIO Creative Studioを利用する際のモジュール

- module/ (**非推奨**)
    - cevio.py(非推奨)
        - 下記2つを1つにまとめたもの
    - cevio_ai.py(非推奨)
        - CeVIO AIを利用する際のモジュール
    - cevio_ccs.py(非推奨)
        - CeVIO Creative Studioを利用する際のモジュール

- sample_code.py
    - サンプルコード
    - CeVIO Creative Studioをご利用の方
        - 9行目を下記のに書き換えてください
        ```py
        t = Cevio(mode="CCS") # AI→CCSに変更
        ```
    - CeVIO AIで「さとうささら」をご利用の方
        - 11行目の`t.make_speech_mode()`のコメントアウトを外していただくと、サンプル設定で読み上げます

- sample_text.txt
    - サンプル文(本説明の機能を読み上げます)


## 機能

1. CeVIO キャスト一覧取得・設定
    - 初期値は、CeVIO AIで追加済みのキャスト一覧を取得し、最初に渡されたキャストを選択しています。

2. コンディション取得・設定
    - 声の「大きさ」、「速さ」、「高さ」、「声質」、「抑揚」を取得・設定します。

3. 感情パラメータ取得・設定
    - 感情パラメータを取得及び設定します。
    - 設定可能な値は、キャラクターごとに異なるので、ユーザーズガイドをご確認ください。

4. セリフ再生
    - 与えられたテキストをもとに、セリフを再生します。
    - CeVIO AIでは200文字、Creative Studioでは100文字以上のテキストを再生する場合、テキストを分割する必要があります。このモジュールでは最大文字数に一番近い部分の文章の「、」や「。」などが入るところで、文章を区切るよう設計しています。
    - 文字数制限以上の「区切り文字」がない文章を入力するとエラーとなってしまうので、文章を入力する際はご注意ください
        - 現在設定している区切り文字一覧
            - 読点「、」「，」「,」
            - 句点「。」「．」「.」
            - 中点「・」
            - 改行文字
            - タブ文字
            - 空白文字「 」「　」

5. パラメータの設定保存
    - パラメータ情報をjson形式で保存可能です。
    - フォーマット
        - talk: コンディション
            - name: コンディション名
            - value: コンディションの設定値(★ここを変更)
                - Volume:大きさ(デフォルト:50)
                - Speed:速さ(デフォルト:50)
                - Tone:高さ(デフォルト:50)
                - ToneScale:抑揚(デフォルト:50)
                - Alpha:声質(デフォルト:50)
        - Cast: キャスト定義(デフォルト:"さとうささら")
        - Emotion: 感情定義
            - 感情名 : 感情の設定値(0～100)

## 確認済み動作環境
- Windows 11 Home 24H2

- Python 3.13.3
    - pywin32 310

- CeVIO AI 9.1.17.0
    - さとうささら トークボイス 2.0.0

- CeVIO Creative Studio 7.0.23.1
    - さとうささら トークボイス 1.7.3


## 利用方法

### 依存パッケージ導入

- リポジトリクローン後、下記コマンドを実行します。

    ```
    py -m pip install --user -r requirements.txt
    ```

    - `Successfully installed pywin32-310`と表示されること

### 動作を確認する場合

- 動作を確認してみたい場合、`py sample_code.py`を実行することで、CeVIO AIが起動し、インストールされているキャラクターの声でサンプルテキスト`sample_text.txt`に記載されている文章を再生します。

### 拡張する場合

- 自分のコードに組み込む、または各種連携(例: ChatGPTのAPIと連携させる)場合、下記の手順でインポートが可能です。

1. インポート
   - CeVIO AIを利用した場合

        ```py
        # 読み込む場合、Cevio(メインの処理クラス)、CevioException(全般エラー)を読み込む
        from ceviopy.cevio import Cevio, CevioException

        # 初期化(この時点でCeVIO AIが起動していない場合、自動で起動)
        talk = Cevio("AI")
        ## > 現在のキャスト : さとうささら(起動時にCeVIOで登録済みのトークボイスからキャラクターを取得)
        ```
    - CeVIO Creative Studioを利用した場合

        ```py
        # 読み込む場合、Cevio(メインの処理クラス)、CevioException(全般エラー)を読み込む
        from ceviopy.cevio import Cevio, CevioException

        # 初期化(この時点でCeVIO Creative Studioが起動していない場合、自動で起動)
        talk = Cevio("CCS")
        ## > 現在のキャスト : さとうささら(起動時にCeVIOで登録済みのトークボイスからキャラクターを取得)
        ```

2. キャラクター設定
   
   - キャラクターの確認

        ```py
        # 利用可能なキャラクター一覧を取得し、List形式で出力
        talk.get_available_cast()
        ## > ['さとうささら', 'すずきつづみ', 'タカハシ']
        
        # 現在のキャラクター設定
        talk.get_cast()
        ## > 'さとうささら'
        ```

   - キャラクターの変更

        ```py
        # キャラクターを設定
        talk.set_cast('すずきつづみ')

        # 存在しないキャラクターをセットした場合
        talk.set_cast('タカハシ')
        ## > Castが一覧に含まれていません。以下から選択してください。
        ## > さとうささら,すずきつづみ,タカハシ
        ```

3. トーク・感情パラメータ設定

    - トーク設定

        ```py
        # トークの設定
        talk.set_talk_param("Speed", 50)
        ## > Speed: 30 -> 50
        # 日本語可(以下の通り変換)
        ## "大きさ" -> "Volume"
        ## "速さ" -> "Speed"
        ## "高さ" -> "Tone"
        ## "抑揚" -> "ToneScale"
        ## "声質" -> "Alpha"
        talk.set_talk_param("速さ", 30)
        ## > Speed: 50 -> 30

        # 存在しない値を入力した場合エラー
        talk.set_talk_param("Speed", 4000) 
        ## > valueは0～100の整数値を渡してください

        # 存在しないパラメータを入力した場合エラー
        talk.set_talk_param("Speedy", 10)  
        ## > Condition is not included in the list. Please select from the following: [Volume,Speed,Tone,ToneScale,Alpha]

        # dict形式で渡す場合、「set_talk_params」を使用
        talk.set_talk_params({"Speed": 60, "Volume": 60})
        ## > Speed: 50 -> 60
        ## > Volume: 50 -> 60
        ```

    - 感情パラメータ設定

        ```py
        # 感情設定
        talk.set_cast_param('元気', 60) 
        ## > 元気: 100 -> 60

        # 存在しない値を入力した場合エラー
        talk.set_cast_param('元気', 600)  
        ## > value must be an integer between 0 and 100.

        # 存在しないパラメータを入力した場合エラー
        talk.set_cast_param('かわいさ', 100) 
        ## > emotion is not included in the list. Please select it below.
        ## > 元気,普通,怒り,哀しみ

        # dict形式で渡す場合、「set_talk_params」を使用
        talk.set_cast_params({"元気": 60, "普通": 60})
        ## > 元気: 100 -> 60
        ## > 普通: 0 -> 60
        ```

4. トーク
   
    ```py
    # 短文の場合、speak()に文章を入力すると音声出力
    # CeVIO AIの場合、「、」「。」などの文章の切れ目が200文字となるところで処理を自動分割(APIの仕様)
    # CeVIO Creative Studioの場合、「、」「。」などの文章の切れ目が100文字となるところで処理を自動分割(APIの仕様)
    # 最初の文は正しく音声出力できないことがあるため、先頭に「っ」が必ず入る
    talk.speak('あーあー、てすとてすと')
    ## > さとうささら > っ
    ## > さとうささら > あーあー、てすとてすと

    # 長文の場合、テキストファイルを入れることでまとめて読み上げ
    with open("sample_text.txt", "r") as f:
        text = f.read()
    talk.speak(text)
    ## > さとうささら > っ
    ## > さとうささら > 1. CeVIO キャスト一覧取得・設定
    ## >     - 初期値は、CeVIO AIで追加済みのキャスト一覧を取得し、最初に渡されたキャストを選択しています。
    ## > 2. コンディション取得・設定
    ## >     - 声の「大きさ」、「速さ」、「高さ」、「声質」、「抑揚」を取得・設定します。
    ## > 3. 感情パラメータ取得・設定
    ## >     - 感情パラメータを取得及び設定します。
    ## >     - 設定可能な値は、
    ## > さとうささら > キャラクターごとに異なるので、ユーザーズガイドをご確認ください。
    ## > 4. セリフ再生
    ## >     - 与えられたテキストをもとに、セリフを再生します。
    ## >     - CeVIO AIでは、200文字以上のテキストを再生する場合、分割する必要があるため文章の「、(読点)」や「。(句点)」などが入るところで、文章を区切るよう設計しています。
    ## >         -
    ## > さとうささら > 現在は200文字以上「区切り文字」がない文章を入力するとエラーとなってしまうので、文章を入力する際はご注意ください。
    ## >     - CeVIO Creative Studioをご利用の方は、「cevio_ccs.py」をインポートの上、ご利用ください。
    ```

## 関連リンク
- [pywin32 · PyPI](https://pypi.org/project/pywin32/)

- [CeVIO AI ユーザーズガイド](https://cevio.jp/guide/cevio_ai/)
    - [CeVIO AI ユーザーズガイド ┃ COMコンポーネントとして利用](https://cevio.jp/guide/cevio_ai/interface/com/)