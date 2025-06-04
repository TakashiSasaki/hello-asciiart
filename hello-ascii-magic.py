# coding: utf-8
# 星条旗をテキストアートで描画するスクリプト
# このスクリプトを実行する前に、ascii_magic モジュールをインストールする必要があります。
# pip install ascii_magic

from ascii_magic import AsciiArt
import requests  # URLからの画像取得時のエラーハンドリングのため
from io import BytesIO
from PIL import Image

def draw_star_spangled_banner_ascii(columns=120, char=None):
    """
    星条旗の画像をURLから取得し、テキストアートとして表示します。

    Args:
        columns (int): テキストアートの幅（文字数）。デフォルトは120。
        char (str, optional): アートに使用する文字。デフォルトはNone（ascii_magicのデフォルト文字を使用）。
    """
    # 星条旗の画像URL (Wikimedia Commonsより)
    # 高解像度のものを選ぶと、より詳細なアートが生成される可能性があります。
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Flag_of_the_United_States.svg/1024px-Flag_of_the_United_States.svg.png"

    print(f"{columns}列で星条旗を描画します...")
    print(f"画像URL: {image_url}")

    try:
        # 画像を取得して Pillow イメージとして読み込む
        # requests の timeout を利用して、長時間応答がない場合に備える
        resp = requests.get(image_url, timeout=10)
        resp.raise_for_status()
        img = Image.open(BytesIO(resp.content))
        # 取得したイメージから AsciiArt オブジェクトを生成
        my_art = AsciiArt.from_pillow_image(img)
    except requests.exceptions.RequestException as e:
        print(f"画像の取得に失敗しました: {e}")
        print("インターネット接続を確認するか、別の画像URLを試してください。")
        return
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
        return

    # テキストアートに変換して出力
    # monochrome=True にすると、よりシンプルな白黒のテキストアートになります。
    # char パラメータで描画文字を指定できます。
    # to_ascii() は文字列を返します。
    try:
        if char:
            ascii_text = my_art.to_ascii(columns=columns, char=char, monochrome=True)
        else:
            ascii_text = my_art.to_ascii(columns=columns, monochrome=True)
        
        print("\n" + "="*columns)
        print(ascii_text)
        print("="*columns + "\n")
        print("描画が完了しました。")
        print("ヒント: columnsの値を変更したり、charパラメータに別の文字を指定して試してみてください。")
        print("例: draw_star_spangled_banner_ascii(columns=80, char='*')")

    except Exception as e:
        print(f"テキストアートへの変換中にエラーが発生しました: {e}")


if __name__ == "__main__":
    # 表示するテキストアートの幅を指定できます。
    # ご利用のターミナルの幅に合わせて調整してください。
    # 一般的なターミナルでは80や120が良いでしょう。
    output_columns = 100 
    
    # 使用する文字を指定することもできます。例えば '*' や '.' など。
    # None の場合はライブラリのデフォルト文字が使用されます。
    # custom_char = "*"
    custom_char = None

    draw_star_spangled_banner_ascii(columns=output_columns, char=custom_char)

    # 別の設定で試す場合の例
    # print("\n--- 別の設定での描画例 ---")
    # draw_star_spangled_banner_ascii(columns=80, char='.')
