# Filename: hello-drawille.py

from drawille import Canvas

# --- 設定値 ---

# 旗の全体サイズ (ブライユ文字単位)
# 星条旗の公式比率は 10:19 (高さ:幅)
# ここでは、一般的なターミナルで見やすいようにサイズを調整します。
# 13本のストライプを表現するため、高さは13の倍数が扱いやすい。
FLAG_BRAILLE_HEIGHT = 13  # 旗の高さ (ブライユ文字の行数)
PIXELS_PER_BRAILLE_ROW = 4 # ブライユ文字1行あたりのピクセル数

# 高さに合わせて幅を決定 (おおよそ10:19の比率を維持)
FLAG_BRAILLE_WIDTH = 38  # 旗の幅 (ブライユ文字の列数)
PIXELS_PER_BRAILLE_COL = 2 # ブライユ文字1列あたりのピクセル数

# キャンバス全体のピクセルサイズ
CANVAS_HEIGHT_PX = FLAG_BRAILLE_HEIGHT * PIXELS_PER_BRAILLE_ROW  # 13 * 4 = 52 ピクセル
CANVAS_WIDTH_PX = FLAG_BRAILLE_WIDTH * PIXELS_PER_BRAILLE_COL    # 38 * 2 = 76 ピクセル

# ストライプの定義
NUM_STRIPES = 13
STRIPE_HEIGHT_PX = CANVAS_HEIGHT_PX // NUM_STRIPES  # 各ストライプの高さ (52 / 13 = 4 ピクセル)

# カントンの定義 (ピクセル単位)
# カントンの高さ: 旗の高さの 7/13
CANTON_HEIGHT_PX = (CANVAS_HEIGHT_PX * 7) // NUM_STRIPES  # (52 * 7) / 13 = 28 ピクセル
# カントンの幅: 旗の幅の 2/5 (公式比率)
CANTON_WIDTH_PX = round(CANVAS_WIDTH_PX * (2/5))  # 76 * 0.4 = 30.4 -> 30 ピクセル (四捨五入)


def draw_rect_filled(canvas: Canvas, x_start: int, y_start: int, width: int, height: int):
    """
    指定された矩形領域を点で塗りつぶします。
    Args:
        canvas: drawilleのCanvasオブジェクト
        x_start: 矩形の左上のX座標 (ピクセル)
        y_start: 矩形の左上のY座標 (ピクセル)
        width: 矩形の幅 (ピクセル)
        height: 矩形の高さ (ピクセル)
    """
    for r_idx in range(height):
        for c_idx in range(width):
            # 描画範囲チェック (Canvas外への描画を防ぐ)
            abs_x = x_start + c_idx
            abs_y = y_start + r_idx
            # drawilleのCanvasは内部で自身のサイズを持つ。
            # set/unsetはその範囲内でのみ有効。
            # ここでは、意図した描画範囲 (CANVAS_WIDTH_PX, CANVAS_HEIGHT_PX) を超えないようにする。
            if 0 <= abs_x < CANVAS_WIDTH_PX and 0 <= abs_y < CANVAS_HEIGHT_PX:
                 canvas.set(abs_x, abs_y)

def draw_star_at(canvas: Canvas, center_x: float, center_y: float):
    """
    指定された中心に1ピクセルの星（点を消すことで表現）を描画します。
    Args:
        canvas: drawilleのCanvasオブジェクト
        center_x: 星の中心のX座標 (ピクセル)
        center_y: 星の中心のY座標 (ピクセル)
    """
    # 座標を整数に丸めて、描画範囲内か確認
    px = round(center_x)
    py = round(center_y)
    if 0 <= px < CANVAS_WIDTH_PX and 0 <= py < CANVAS_HEIGHT_PX:
        canvas.unset(px, py)

def draw_american_flag():
    """
    星条旗をブライユアートで描画し、コンソールに出力します。
    """
    # Canvasオブジェクトを作成
    c = Canvas()

    # 1. ストライプを描画 (13本)
    #   - 赤いストライプ (奇数番目、0-indexedなので偶数インデックス)
    #   - 白いストライプ (偶数番目、0-indexedなので奇数インデックス) は何もしない（背景色が白と仮定）
    for i in range(NUM_STRIPES):  # 0 から 12
        y_offset_px = i * STRIPE_HEIGHT_PX
        is_red_stripe = (i % 2 == 0)  # 0, 2, 4... が赤

        if is_red_stripe:
            draw_rect_filled(c, 0, y_offset_px, CANVAS_WIDTH_PX, STRIPE_HEIGHT_PX)

    # 2. カントン領域を青地（点の塗りつぶし）で描画
    #    ストライプの上からカントン領域を上書きします。
    draw_rect_filled(c, 0, 0, CANTON_WIDTH_PX, CANTON_HEIGHT_PX)

    # 3. カントン内に星を描画 (点を消すことで白い星を表現)
    #    実際の星の数は50個ですが、ブライユアートでは簡略化します。
    #    星条旗の標準的な星の配置: 9列で、6個の星の列と5個の星の列が交互。
    num_star_cols = 9  # 星の列の数

    # 星の列間の左右のパディングを含む均等な間隔
    x_spacing = CANTON_WIDTH_PX / (num_star_cols + 1) # カントン幅を(列数+1)で割り、各星列の中心x座標の間隔とする

    for col_idx in range(num_star_cols):  # 0 から 8
        current_star_col_x_px = x_spacing * (col_idx + 1)

        # この列の星の数を決定 (6個または5個)
        is_col_of_6_stars = (col_idx % 2 == 0)  # 0, 2, 4, 6, 8 列目 (計5列が6個の星)

        if is_col_of_6_stars:
            num_stars_in_this_col = 6
        else:
            num_stars_in_this_col = 5

        # 星の行間の上下のパディングを含む均等な間隔
        y_spacing = CANTON_HEIGHT_PX / (num_stars_in_this_col + 1) # カントン高さを(行数+1)で割り、各星の中心y座標の間隔とする

        for star_row_idx in range(num_stars_in_this_col):  # 0から5 または 0から4
            current_star_row_y_px = y_spacing * (star_row_idx + 1)
            draw_star_at(c, current_star_col_x_px, current_star_row_y_px)

    # 描画結果をフレームとして取得し、出力 (引数なしで呼び出すように修正)
    output_frame = c.frame()
    print(output_frame)

if __name__ == "__main__":
    draw_american_flag()
