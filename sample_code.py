from os import read
from src.ceviopy import Cevio, CevioException

def main():
    """
    サンプルテキスト
    cevio.pyをそのまま実行するとサンプルテキストを再生します(さとうささらボイスのみ対応)
    """
    t = Cevio(mode="AI")
    # さとうささらのトークを利用されている方のみ、次行のサンプルを利用可能です。
    # t.make_speech_mode()
    print(t.get_talk_params())
    print(t.get_cast_params())

    # sample_text.txtを書き換えることで、読み上げ文章が変更できます
    with open('sample_text.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    t.speak(text)

if __name__ == "__main__":
    main()