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
    - 声の「大きさ」、「速さ」、「高さ」、「声質」を取得及び設定します(「抑揚」は現在未対応です)。

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


## 確認済み動作環境
- Windows 10 Home 21H1

- Python 3.9.2
    - pywin32 301

- CeVIO AI 8.1.8.0
    - さとうささら トークボイス 1.0.0


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