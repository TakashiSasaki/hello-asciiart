# Filename: hello-plotille
import plotille
import math

# --- 設定値 (ピクセル単位) ---
# 描画ターゲットとするピクセル解像度
# このピクセル解像度をplotille.Canvasの文字数とドット数で近似する
TARGET_PIXEL_HEIGHT = 52
TARGET_PIXEL_WIDTH = 76

# plotille.Canvas の1文字あたりのドット数 (plotilleの内部的なブライユ表現を想定)
# これらは plotille の実装に依存する可能性があるが、一般的なブライユ文字の特性に基づく
DOTS_PER_CHAR_HEIGHT = 4
DOTS_PER_CHAR_WIDTH = 2

# plotille.Canvas の文字数としてのサイズ
# ターゲットピクセル数を1文字あたりのドット数で割って文字数を計算 (切り上げ)
FLAG_CHAR_HEIGHT = math.ceil(TARGET_PIXEL_HEIGHT / DOTS_PER_CHAR_HEIGHT)
FLAG_CHAR_WIDTH = math.ceil(TARGET_PIXEL_WIDTH / DOTS_PER_CHAR_WIDTH)

# plotille.Canvas のデータ座標系として実際に使用するピクセル解像度
# これは (文字数 * 1文字あたりのドット数) となる
PIXEL_HEIGHT = FLAG_CHAR_HEIGHT * DOTS_PER_CHAR_HEIGHT
PIXEL_WIDTH = FLAG_CHAR_WIDTH * DOTS_PER_CHAR_WIDTH


# ストライプの定義
NUM_STRIPES = 13
# 各ストライプのピクセル単位の高さ
STRIPE_HEIGHT_PX = PIXEL_HEIGHT // NUM_STRIPES # 整数除算で均等に分割

# カントンの定義 (ピクセル単位)
# カントンの高さ: 旗の高さの 7/13 (7ストライプ分)
CANTON_HEIGHT_PX = STRIPE_HEIGHT_PX * 7
# カントンの幅: 旗の幅の 2/5 (公式比率)
CANTON_WIDTH_PX = round(PIXEL_WIDTH * (2/5)) # 四捨五入

# 星の数と配置に関する設定 (簡略化)
NUM_STAR_COLS = 9  # 星の列の数
NUM_STARS_COL_TYPE1 = 6 # 星が6個の列
NUM_STARS_COL_TYPE2 = 5 # 星が5個の列


def main():
    """
    plotille.Canvas を使用して星条旗をターミナルに描画します。
    """
    # plotille.Canvas オブジェクトの作成
    # width, height: キャンバスの文字数としての幅と高さ
    # xmin, xmax, ymin, ymax: キャンバスが表現するデータ座標の範囲。
    #                         ここではピクセル座標系 (0 から width-1, 0 から height-1) に合わせる。
    # plotille の Canvas は (xmin, ymin) が左下隅に対応し、Y軸は上向きが正となる。
    canvas = plotille.Canvas(
        FLAG_CHAR_WIDTH,
        FLAG_CHAR_HEIGHT,
        xmin=0,
        xmax=PIXEL_WIDTH -1,
        ymin=0,
        ymax=PIXEL_HEIGHT -1
    )

    # Y座標変換関数:
    # ピクセル座標系 (左上原点, Y軸下向きが正) から
    # plotille.Canvasのデータ座標系 (左下原点, Y軸上向きが正) へ変換する。
    def y_pixel_to_canvas_data(y_pixel_coord):
        return (PIXEL_HEIGHT - 1) - y_pixel_coord

    # 1. ストライプを描画 (赤いストライプのみ)
    #    白いストライプはターミナルの背景色に依存するため、ここでは描画しない。
    for i in range(NUM_STRIPES):  # ストライプのインデックス (0から12)
        stripe_y_start_pixel = i * STRIPE_HEIGHT_PX # 現在のストライプの上端のY座標 (ピクセル)
        is_red_stripe = (i % 2 == 0)  # 偶数インデックス (0, 2, ...) のストライプが赤

        if is_red_stripe:
            # 赤いストライプの各ピクセル行に対して水平線を描画することで「塗りつぶし」を表現
            for r_pixel in range(stripe_y_start_pixel, stripe_y_start_pixel + STRIPE_HEIGHT_PX):
                if PIXEL_WIDTH > 0: # 旗の幅が0より大きい場合のみ描画
                    # ピクセルY座標をCanvasのデータY座標に変換
                    y_canvas_data = y_pixel_to_canvas_data(r_pixel)
                    # canvas.line(x0, y0, x1, y1, color)
                    canvas.line(0, y_canvas_data, PIXEL_WIDTH - 1, y_canvas_data, color='red')

    # 2. カントン領域を青地で描画
    #    既に描画されたストライプの上に青いカントンを上書きする。
    for r_pixel in range(0, CANTON_HEIGHT_PX): # カントンのY座標範囲 (0からカントンの高さまで)
        if CANTON_WIDTH_PX > 0: # カントンの幅が0より大きい場合のみ描画
            y_canvas_data = y_pixel_to_canvas_data(r_pixel)
            canvas.line(0, y_canvas_data, CANTON_WIDTH_PX - 1, y_canvas_data, color='blue')

    # 3. カントン内に星を描画 (白い点として表現)
    stars_pixel_coords_x = [] # 星の中心のX座標 (ピクセル) を格納するリスト
    stars_pixel_coords_y = [] # 星の中心のY座標 (ピクセル) を格納するリスト

    # 星の列間のX方向の間隔を計算 (カントン幅を星の列数+1で均等に分割)
    x_column_spacing_pixel = CANTON_WIDTH_PX / (NUM_STAR_COLS + 1)

    for col_idx in range(NUM_STAR_COLS):  # 星の列のインデックス (0からNUM_STAR_COLS-1)
        # 現在の星の列の中心X座標 (ピクセル)
        current_star_column_center_x_pixel = x_column_spacing_pixel * (col_idx + 1)

        # この列の星の数を決定 (6個の列と5個の列が交互になるように)
        num_stars_in_this_column = NUM_STARS_COL_TYPE1 if (col_idx % 2 == 0) else NUM_STARS_COL_TYPE2

        # 星の行間のY方向の間隔を計算 (カントン高さをこの列の星の数+1で均等に分割)
        y_row_spacing_pixel = CANTON_HEIGHT_PX / (num_stars_in_this_column + 1)

        for star_row_idx in range(num_stars_in_this_column): # 列内の星の行インデックス
            # 現在の星の中心Y座標 (ピクセル)
            current_star_center_y_pixel = y_row_spacing_pixel * (star_row_idx + 1)

            stars_pixel_coords_x.append(round(current_star_column_center_x_pixel))
            stars_pixel_coords_y.append(round(current_star_center_y_pixel))

    # 計算された各星の位置に白い点をプロット
    for x_px, y_px in zip(stars_pixel_coords_x, stars_pixel_coords_y):
        # 念のため、座標が描画範囲内にあるか確認
        if 0 <= x_px < PIXEL_WIDTH and 0 <= y_px < PIXEL_HEIGHT:
            # canvas.point(x_data, y_data, color)
            # ピクセル座標をCanvasのデータ座標に変換して点を打つ
            canvas.point(x_px, y_pixel_to_canvas_data(y_px), color='white')

    # 最終的な描画結果を文字列として取得し、コンソールに出力
    # canvas.plot() は、Canvasの内容をブライユ文字列表現に変換する。
    print(canvas.plot())

if __name__ == "__main__":
    main()
