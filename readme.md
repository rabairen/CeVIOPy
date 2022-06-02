# CeVIOPy
## 概要
Python上でCeVIO AIのトーク機能を利用するモジュール群です。


## フォルダ構成
- module/
    - cevio_ai.py
        - CeVIO AIを利用する際のモジュール
    - cevio_ccs.py
        - CeVIO Creative Studioを利用する際のモジュール

- sample_code.py
    - サンプルコード
    - CeVIO Creative Studioをご利用の方
        - 2行目を下記のとおりに書き換えてください
        ```py
        from module.cevio_ccs import cevioapi
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
    - CeVIO AIでは、200文字以上のテキストを再生する場合、分割する必要があるため文章の「、」や「。」などが入るところで、文章を区切るよう設計しています。
    - 現在は200文字以上「区切り文字」がない文章を入力するとエラーとなってしまうので、文章を入力する際はご注意ください
        - 現在設定している区切り文字一覧
            - 読点「、」「，」「,」
            - 句点「。」「．」「.」
            - 中点「・」
            - 改行文字
            - タブ文字
            - 空白文字「 」「　」
    - CeVIO Creative Studioをご利用の方は、「cevio_ccs.py」をインポートの上、ご利用ください。

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
        - Cast: キャスト定義
            - sasara:さとうささら
            - tsudumi:すずきつづみ
            - takahashi:タカハシ
            - ia_ccs:IA
            - one_ccs:ONE
            - ia_ai:IA
            - one_ai:ONE
            - rikka:小春六花
            - maki_ja:弦巻マキ (日)
            - maki_en:弦巻マキ (英)
            - fee_chan:フィーちゃん
            - rosa:ロサ (ROSA)
        - Emotion: 感情定義
            - name: 感情名
            - value: 感情の設定値(★ここを変更)
                - nameのStatus0xに対応する箇所に値を設定

## 確認済み動作環境
- Windows 10 Home 21H1

- Python 3.9.2
    - pywin32 301

- CeVIO AI 8.1.8.0
    - さとうささら トークボイス 1.0.0

- CeVIO Creative Studio 7.0.23.1
    - さとうささら トークボイス 1.7.3


## 利用方法

### 依存パッケージ導入
- pywin32
    ```
    pip install pywin32
    ```

### 実行方法(デフォルト設定のまま利用)
1. CeVIO AIを起動

1. 以下のコマンドを実行
    ```
    python sample_code.py
    ```


## 関連リンク
- [pywin32 · PyPI](https://pypi.org/project/pywin32/)

- [CeVIO AI ユーザーズガイド](https://cevio.jp/guide/cevio_ai/)
    - [CeVIO AI ユーザーズガイド ┃ COMコンポーネントとして利用](https://cevio.jp/guide/cevio_ai/interface/com/)