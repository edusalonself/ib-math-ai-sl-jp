"""AA SL 1.1（Numbers in standard form）の内容を検算する。

    python3 figs/aa-sl/check_aasl_1_1.py

方針は AI HL のチェッカーと同じです。

  * 数値は sympy で第一原理から出し直す（本文の式を写さない）
  * 「こう間違えたら、こうなる」と書いた検算は、実際にその
    間違いをして、本当に別の値になることを確かめる
  * レビューで直した箇所には not_in_text の見張りを置く
  * 構成の不変量（★AA 版：`##` は 5 つ・例題 4・演習 10）を数える
  * 登録先（_quarto-draft.yml、aa-sl/index.qmd、glossary-aa.qmd）を見る
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "01-number-and-algebra")
QMD = os.path.join(BASE, "aasl-1-1.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aasl_1_1.py"), encoding="utf-8").read()
# 図の中で「実際に紙に出る文字」だけを集める。
# 注意書き（docstring）は紙に出ないので、全部外してから文字列を集める。
FIGCODE = FIG.split('"""', 2)[-1]
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
# 色コード（"#1f2328" など）はラベルではないので外す
# 色コード・ファイル名・キーワードはラベルではないので外す
# （ラベルは必ず空白か $ を含む）
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))

OK = NG = 0


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def _S(x):
    """float を、そのままの値の有理数にする（nsimplify の推測を避ける）。"""
    if isinstance(x, float):
        return sp.Rational(str(x))
    return sp.nsimplify(x, rational=True)


def eq(a, b, msg=""):
    chk(sp.simplify(_S(a) - _S(b)) == 0, msg + f"  ({a} vs {b})")


def ne(a, b, msg=""):
    chk(sp.simplify(_S(a) - _S(b)) != 0, msg + f"  ({a} vs {b})")


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている（直したはず）: " + msg + " :: " + sub[:70])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


def sf(a, k):
    """a × 10^k を、丸め誤差なしの有理数で返す。"""
    return sp.Rational(str(a)) * sp.Integer(10) ** k


def parts(x):
    """正の数 x を standard form にしたときの (a, k)。第一原理から。"""
    x = sp.nsimplify(x)
    k = sp.floor(sp.log(x, 10))
    # log の数値誤差を避けるため、10^k <= x < 10^(k+1) を満たすまで直す。
    k = sp.Integer(k)
    while sp.Integer(10) ** k > x:
        k -= 1
    while sp.Integer(10) ** (k + 1) <= x:
        k += 1
    return sp.nsimplify(x / sp.Integer(10) ** k), k


# ══════════════════════════════════════════════════════════
# 0. standard form そのもの（記号のまま）
# ══════════════════════════════════════════════════════════
# a と k は、ただ 1 通りに決まる（Why it works の主張）。
for x in ["0.000407", "5200000", "1", "9.999", "0.0001", "62400",
          "0.00000091", "3.25/1000"]:
    a, k = parts(sp.nsimplify(x))
    chk(1 <= a < 10, f"a が範囲に入る: {x} -> {a}")
    chk(k.is_Integer, f"k が整数: {x} -> {k}")
    eq(a * sp.Integer(10) ** k, sp.nsimplify(x), f"a×10^k が元の数に戻る: {x}")

# 一意性の証明で使った 2 つの不等式
for d in range(1, 12):
    chk(sp.Integer(10) ** (-d) <= sp.Rational(1, 10),
        f"k>m なら 10^(m-k) <= 1/10 （m-k = -{d}）")
_a, _b = sp.symbols("a b", positive=True)
# a >= 1, b < 10 から a/b > 1/10。境目で確かめる。
chk(sp.Rational(1, 1) / sp.Rational(999, 100) > sp.Rational(1, 10),
    "a=1, b=9.99 でも a/b > 1/10")
chk(sp.limit(1 / _b, _b, 10, "-") == sp.Rational(1, 10),
    "b→10 の極限が 1/10（そこには届かない）")
# 分配法則（足し算の根拠）
_x, _y, _k = sp.symbols("x y k")
chk(sp.simplify(_x * 10 ** _k + _y * 10 ** _k - (_x + _y) * 10 ** _k) == 0,
    "a×10^k + b×10^k = (a+b)×10^k")
# 指数法則（本文が「公式集にない」と書いているもの）
_m, _n = sp.symbols("m n", integer=True)
chk(sp.simplify(sp.Integer(10) ** _m * sp.Integer(10) ** _n
                - sp.Integer(10) ** (_m + _n)) == 0, "10^m × 10^n = 10^(m+n)")
in_text("公式集の Topic 1 は **SL 1.2 から**始まっていて、**1.1 の欄はありません。**",
        "公式集に 1.1 の欄がないこと")
in_text("指数法則も、公式集には印刷されていません", "指数法則が公式集にないこと")

# ══════════════════════════════════════════════════════════
# 1. The idea の中の数
# ══════════════════════════════════════════════════════════
eq(sf("3.2", 6), 3200000, "3 200 000 = 3.2×10^6")
eq(sf("4.7", -5), sp.Rational(47, 1000000), "0.000047 = 4.7×10^-5")
eq(sf("5.09", -3), sp.Rational(509, 100000), "5.09×10^-3 = 0.00509")
eq(sf("32", 4), sf("3.2", 5), "32×10^4 = 3.2×10^5")
eq(sf("0.32", 6), sf("3.2", 5), "0.32×10^6 = 3.2×10^5")
eq(sf("2", 3) * sf("4", 5), sf("8", 8), "(2×10^3)(4×10^5) = 8×10^8")
eq(sf("9", 7) / sf("3", 2), sf("3", 5), "(9×10^7)/(3×10^2) = 3×10^5")
eq(sf("5", 4) * sf("6", 3), sf("30", 7), "(5×10^4)(6×10^3) = 30×10^7")
eq(sf("30", 7), sf("3", 8), "30×10^7 = 3×10^8")
eq(sf("0.6", -3), sf("6", -4), "0.6×10^-3 = 6×10^-4")
ne(sf("30", 7), sf("3", 6), "3×10^6 は誤り（向きを逆にした値）")
eq(sf("3", 6), sf("30", 7) / 100, "その誤りは 1/100 になる")
eq(sf("30", 1), 300, "小さい数で試す: 30×10^1 = 300")
eq(sf("3", 2), 300, "3×10^2 = 300 で合う")
ne(sf("3", 0), 300, "3×10^0 = 3 では合わない")
eq(sf("3.4", 6) + sf("5", 5), sf("3.9", 6), "3.4×10^6 + 5×10^5 = 3.9×10^6")
eq(sf("5", 5), sf("0.5", 6), "5×10^5 = 0.5×10^6")
eq(sf("34", 5) + sf("5", 5), sf("39", 5), "小さいほうにそろえると 39×10^5")
eq(sf("39", 5), sf("3.9", 6), "39×10^5 = 3.9×10^6（同じ値）")
# 見積もりの節
eq(sp.Rational("7.9") * sp.Rational("4.2"), sp.Rational("33.18"), "7.9×4.2 = 33.18")
eq(sf("7.9", -6) * sf("4.2", 3), sf("3.318", -2), "積は 3.318×10^-2")
eq(sf("8", 0) * sf("4", 0), 32, "見積もりは 8×4 = 32")
eq(sf("32", -3), sf("3.2", -2), "32×10^-3 = 3.2×10^-2（見積もりの桁）")
a_est, k_est = parts(sf("3.318", -2))
chk(k_est == -2, "正しい答えの桁は 10^-2")
ne(sf("3.318", -3), sf("3.318", -2), "3.318×10^-3 は別の値")
ne(sf("3.318", -1), sf("3.318", -2), "3.318×10^-1 は別の値")

# ══════════════════════════════════════════════════════════
# 2. 例題 1 — 書き直す
# ══════════════════════════════════════════════════════════
eq(sf("4.07", -4), sp.Rational(407, 1000000), "例題1(a) 0.000407 = 4.07×10^-4")
a1, k1 = parts(sp.Rational(407, 1000000))
eq(a1, sp.Rational("4.07"), "例題1(a) a = 4.07")
chk(k1 == -4, "例題1(a) k = -4")
# 挟み込みの検算
chk(sp.Rational(1, 10000) < sp.Rational(407, 1000000) < sp.Rational(1, 1000),
    "例題1(a) 10^-4 < 0.000407 < 10^-3")
_wrong_a = sf("4.07", -5)
chk(sp.Rational(1, 100000) < _wrong_a < sp.Rational(1, 10000),
    "誤答 4.07×10^-5 は 10^-5 と 10^-4 のあいだ（挟み込みで捕まる）")
eq(_wrong_a, sp.Rational(407, 10000000), "誤答は 0.0000407")
eq(sf("5.2", 6), 5200000, "例題1(b) 5.2×10^6 = 5 200 000")
eq(sf("84", -7), sf("8.4", -6), "例題1(c) 84×10^-7 = 8.4×10^-6")
eq(sf("84", -7), sp.Rational(84, 10000000), "例題1(c) = 0.0000084")
ne(sf("8.4", -8), sf("84", -7), "誤答 8.4×10^-8 は別の値")
eq(sf("8.4", -8), sp.Rational(84, 1000000000), "誤答は 0.000000084")
eq(sf("0.62", 5), sf("6.2", 4), "例題1(d) 0.62×10^5 = 6.2×10^4")
chk(not (1 <= sp.Rational("0.62") < 10), "0.62 は範囲外")
chk(1 <= sp.Rational("6.2") < 10, "6.2 は範囲内")

# ══════════════════════════════════════════════════════════
# 3. 例題 2 — 掛け算・割り算
# ══════════════════════════════════════════════════════════
eq(sf("3", 5) * sf("2.5", -8), sf("7.5", -3), "例題2(a) = 7.5×10^-3")
eq(sf("4", 6) * sf("8", 7), sf("32", 13), "例題2(b) = 32×10^13")
eq(sf("32", 13), sf("3.2", 14), "32×10^13 = 3.2×10^14")
eq(sf("3.2", 14) / sf("8", 7), sf("4", 6), "例題2(b) の検算：割り戻すと 4×10^6")
eq(sf("3.2", 13) / sf("8", 7), sf("4", 5), "誤答なら 4×10^5（検算が効く）")
ne(sf("4", 5), sf("4", 6), "4×10^5 と 4×10^6 はちがう")
eq(sf("7.2", -3) / sf("9", 2), sf("8", -6), "例題2(c) = 8×10^-6")
eq(sp.Rational("7.2") / 9, sp.Rational("0.8"), "7.2/9 = 0.8")
eq(sf("0.8", -5), sf("8", -6), "0.8×10^-5 = 8×10^-6")
eq(sf("8", -6) * sf("9", 2), sf("7.2", -3), "例題2(c) の検算：掛け戻すと 7.2×10^-3")
eq(sf("8", -5) * sf("9", 2), sf("7.2", -2), "誤答なら 7.2×10^-2（検算が効く）")
eq(sf("7.2", -2) / sf("7.2", -3), 10, "その誤りはちょうど 10 倍")

# ══════════════════════════════════════════════════════════
# 4. 例題 3 — 足し算・引き算
# ══════════════════════════════════════════════════════════
eq(sf("4.2", 5) + sf("3", 4), sf("4.5", 5), "例題3(a) = 4.5×10^5")
eq(sf("3", 4), sf("0.3", 5), "3×10^4 = 0.3×10^5")
eq(sf("4.2", 5), 420000, "4.2×10^5 = 420 000")
eq(sf("3", 4), 30000, "3×10^4 = 30 000")
eq(420000 + 30000, 450000, "普通の数で足すと 450 000")
eq(450000, sf("4.5", 5), "450 000 = 4.5×10^5")
ne(sf("7.2", 9), sf("4.5", 5), "指数を足した誤答 7.2×10^9 は別の値")
eq(sf("8", -3) - sf("6", -4), sf("7.4", -3), "例題3(b) = 7.4×10^-3")
eq(sf("6", -4), sf("0.6", -3), "6×10^-4 = 0.6×10^-3")
eq(sp.Rational(8, 1000) - sp.Rational(6, 10000), sp.Rational(74, 10000),
   "0.008 - 0.0006 = 0.0074")
eq(sf("2.5", -3) + sf("7.5", -4), sf("3.25", -3), "例題3(c) = 3.25×10^-3")
eq(sf("7.5", -4), sf("0.75", -3), "7.5×10^-4 = 0.75×10^-3")
chk(sf("2.5", -3) < sf("3.25", -3) < 2 * sf("2.5", -3),
    "例題3(c) の検算：もとの値と、その 2 倍のあいだ")
_bad = sf("2.5", -3) + sf("7.5", -3)
eq(_bad, sf("1", -2), "そろえ違いの誤答は 1×10^-2")
chk(not (sf("2.5", -3) < _bad < 2 * sf("2.5", -3)),
    "その誤答は挟み込みから出る（検算が効く）")

# ══════════════════════════════════════════════════════════
# 5. 例題 4 — 水の分子
# ══════════════════════════════════════════════════════════
eq(sf("6", -5) / sf("3", -26), sf("2", 21), "例題4(a) = 2×10^21")
eq(-5 - (-26), 21, "指数は -5-(-26) = 21")
eq(sf("6", -5) * sf("4", 2), sf("24", -3), "例題4(b) = 24×10^-3")
eq(sf("24", -3), sf("2.4", -2), "24×10^-3 = 2.4×10^-2")
eq(sf("2", 21) * sf("3", -26), sf("6", -5), "例題4(d) の検算：もとの質量に戻る")
eq(sf("2", 20) * sf("3", -26), sf("6", -6), "指数がずれていたら 6×10^-6")
ne(sf("6", -6), sf("6", -5), "6×10^-6 と 6×10^-5 はちがう")
ne(sf("2.4", -4), sf("2.4", -2), "2.4×10^-4 は別の値（見積もりから外れる）")
eq(sf("2.4", -2) / sf("2.4", -4), 100, "その誤りは 100 倍ちがう")

# ══════════════════════════════════════════════════════════
# 6. 演習 1〜10
# ══════════════════════════════════════════════════════════
# 1
eq(sf("9.1", -7), sp.Rational(91, 100000000), "演習1(a) = 9.1×10^-7")
a, k = parts(sp.Rational(91, 100000000))
chk(k == -7 and a == sp.Rational("9.1"), "演習1(a) の a と k")
eq(sf("6.24", 4), 62400, "演習1(b) = 6.24×10^4")
a, k = parts(sp.Integer(62400))
chk(k == 4 and a == sp.Rational("6.24"), "演習1(b) の a と k")
chk(sp.Integer(10) ** -7 < sp.Rational(91, 100000000) < sp.Integer(10) ** -6,
    "演習1(a) の挟み込み")
chk(sp.Integer(10) ** 4 < 62400 < sp.Integer(10) ** 5, "演習1(b) の挟み込み")
eq(sf("9.1", -8), sp.Rational(91, 1000000000), "誤答 9.1×10^-8 = 0.000000091")
chk(not (sp.Integer(10) ** -7 < sf("9.1", -8) < sp.Integer(10) ** -6),
    "誤答は挟み込みから出る（検算が効く）")
# 2
eq(sf("3.06", -4), sp.Rational(306, 1000000), "演習2(a) = 0.000306")
eq(sf("2.5", 6), 2500000, "演習2(b) = 2 500 000")
a, k = parts(sp.Rational(306, 10000000))
chk(k == -5, "0 を 1 個多く書くと k = -5 になる（検算が効く）")
# 3
eq(sf("2", 7) * sf("4.5", -3), sf("9", 4), "演習3 = 9×10^4")
eq(sf("9", 4) / sf("2", 7), sf("4.5", -3), "演習3 の検算：割り戻す")
eq(sf("9", 10) / sf("2", 7), sf("4.5", 3), "指数を引いた誤答なら 4.5×10^3")
ne(sf("4.5", 3), sf("4.5", -3), "4.5×10^3 と 4.5×10^-3 はちがう")
eq(sf("4.5", 3) / sf("4.5", -3), sp.Integer(10) ** 6, "その差は 10 の 6 乗")
# 4
eq(sf("4.8", 5) / sf("6", -2), sf("8", 6), "演習4 = 8×10^6")
eq(sp.Rational("4.8") / 6, sp.Rational("0.8"), "4.8/6 = 0.8")
eq(5 - (-2), 7, "指数は 5-(-2) = 7")
eq(sf("0.8", 7), sf("8", 6), "0.8×10^7 = 8×10^6")
eq(sf("8", 6) * sf("6", -2), sf("4.8", 5), "演習4 の検算：掛け戻す")
eq(sf("8", 8) * sf("6", -2), sf("4.8", 7), "誤答 8×10^8 なら 4.8×10^7")
eq(sf("4.8", 7) / sf("4.8", 5), 100, "それは 100 倍")
# 5
eq(sf("5", -4) + sf("3.2", -3), sf("3.7", -3), "演習5 = 3.7×10^-3")
eq(sf("5", -4), sf("0.5", -3), "5×10^-4 = 0.5×10^-3")
eq(sp.Rational(5, 10000) + sp.Rational(32, 10000), sp.Rational(37, 10000),
   "0.0005 + 0.0032 = 0.0037")
eq(sf("5", -4) + sf("32", -4), sf("37", -4), "小さいほうにそろえると 37×10^-4")
eq(sf("37", -4), sf("3.7", -3), "37×10^-4 = 3.7×10^-3（同じ答え）")
chk(sp.Rational(-3) > sp.Rational(-4), "-3 > -4（大きいほうの指数は -3）")
# 6
eq(sf("9.1", 8) - sf("4", 7), sf("8.7", 8), "演習6 = 8.7×10^8")
eq(sf("4", 7), sf("0.4", 8), "4×10^7 = 0.4×10^8")
eq(sf("8.7", 8) + sf("0.4", 8), sf("9.1", 8), "演習6 の検算：足し戻す")
eq(sf("5.1", 8) + sf("0.4", 8), sf("5.5", 8), "誤答 5.1×10^8 なら 5.5×10^8")
ne(sf("5.5", 8), sf("9.1", 8), "5.5×10^8 は 9.1×10^8 に届かない")
chk(sf("8.7", 8) < sf("9.1", 8), "引き算の答えは、もとより小さい")
# 7
eq(sf("3", 8) * sf("2", 2), sf("6", 10), "演習7(a) = 6×10^10")
eq(sf("1.5", 11) / sf("3", 8), sf("5", 2), "演習7(b) = 5×10^2")
eq(sf("0.5", 3), sf("5", 2), "0.5×10^3 = 5×10^2")
eq(sf("3", 8) * sf("5", 2), sf("1.5", 11), "演習7 の検算：掛け戻す")
eq(sf("15", 10), sf("1.5", 11), "15×10^10 = 1.5×10^11")
chk(480 < 500 < 520, "500 秒はおよそ 8 分（本文の記述）")
# 8
eq(sf("0.7", 5), sf("7", 4), "演習8 0.7×10^5 = 7×10^4")
eq(sf("10", 3), sf("1", 4), "演習8 10×10^3 = 1×10^4")
eq(sf("0.7", 5), 70000, "= 70 000")
eq(sf("10", 3), 10000, "= 10 000")
chk(1 <= sp.Rational("9.99") < 10, "9.99 は範囲内（ぎりぎり）")
chk(1 <= sp.Rational("8") < 10 and sp.Integer(0).is_Integer,
    "8×10^0 も standard form（k=0 は整数）")
eq(sf("8", 0), 8, "8×10^0 = 8")
chk(not (1 <= sp.Rational("0.7") < 10), "0.7 は範囲外")
chk(not (1 <= sp.Rational("10") < 10), "10 は範囲外")
eq(sf("7", 6), 7000000, "誤答 7×10^6 = 7 000 000")
eq(sf("7", 6) / sf("7", 4), 100, "それは 100 倍ちがう")
# 9
eq(sf("4.8", -3) + sf("1.2", -3), sf("6", -3), "演習9(a) = 6×10^-3")
eq(sf("4.8", -3) / sf("1.2", -3), 4, "演習9(b) = 4")
eq(sf("4", 0), 4, "4×10^0 = 4")
chk(sf("4.8", -3) < sf("6", -3) < 2 * sf("4.8", -3),
    "演習9(a) の検算：挟み込み")
eq(4 * sf("1.2", -3), sf("4.8", -3), "演習9(b) の検算：掛け戻す")
eq(sf("4", -3) * sf("1.2", -3), sf("4.8", -6), "誤答 4×10^-3 なら 4.8×10^-6")
eq(sf("4.8", -3) / sf("4.8", -6), 1000, "それは 1000 倍ちがう")
eq(sp.Rational("4.8") / sp.Rational("1.2"), 4, "グラムで測っても比は 4")
# 10
eq(sf("4", 5) * sf("3", -8), sf("1.2", -2), "演習10 の正しい答え = 1.2×10^-2")
eq(sf("12", -3), sf("1.2", -2), "12×10^-3 = 1.2×10^-2")
eq(5 + (-8), -3, "指数は足して -3")
eq(5 * (-8), -40, "生徒は掛けて -40 にした")
eq(sf("12", -40), sf("1.2", -39), "生徒の答えは 1.2×10^-39")
chk(sf("1.2", -39) < sf("3", -8), "生徒の答えは、掛けた 2 数より小さい")
chk(sf("4", 5) > 1, "4×10^5 は 1 より大きい")
chk(sf("4", 5) * sf("3", -8) > sf("3", -8),
    "1 より大きい数を掛けたので、答えは 3×10^-8 より大きい")
chk(sf("1.2", -2) == sp.Rational(12, 1000), "1.2×10^-2 = 0.012")
in_text("**正の数どうしなら、掛けた答えが両方の数より小さくなるのは、$2$ つとも"
        " $1$ より小さいときだけ**です", "掛け算の大小の条件（正の数どうし・両方が 1 未満）")
not_in_text("片方が $1$ より小さいときだけ", "誤りだった条件（レビュー前の文）")
not_in_text("**掛けた答えが、両方の数より小さくなるのは", "正の数の断りがなかった文（レビュー11）")

# ══════════════════════════════════════════════════════════
# 6-B. レビューで直したところの見張り（復活したら落ちる）
# ══════════════════════════════════════════════════════════
# (1) 演習 6：足し戻す検算は、そろえ忘れを素通しする
not_in_text("**検算。** 引いた数を足し戻します。", "循環していた検算（レビュー1）")
in_text("$$\n910\\,000\\,000 - 40\\,000\\,000 = 870\\,000\\,000 = 8.7 \\times 10^{8}\n$$",
        "普通の数に戻す検算（レビュー1）")
eq(910000000 - 40000000, 870000000, "910 000 000 - 40 000 000 = 870 000 000")
eq(870000000, sf("8.7", 8), "= 8.7×10^8")
eq(sf("5.1", 8), 510000000, "誤答は 510 000 000")
ne(510000000, 870000000, "誤答は、普通の数の引き算と合わない（検算が効く）")
# そろえ忘れた生徒が「引いた 4」を足し戻すと、誤答が通ってしまう
eq(sp.Rational("5.1") + 4, sp.Rational("9.1"),
   "5.1 + 4 = 9.1（足し戻す検算では、そろえ忘れが捕まらない）")
# (2) 例題 4(b)：見積もりが解答と同じ計算だった
not_in_text("**検算（(b) について）。** 桁で見積もります", "循環していた検算（レビュー2）")
eq(sp.Rational("0.00006") * 400, sp.Rational("0.024"), "0.00006 × 400 = 0.024")
eq(sp.Rational("0.024"), sf("2.4", -2), "0.024 = 2.4×10^-2")
eq(sf("2.4", -4), sp.Rational("0.00024"), "誤答は 0.00024")
# (3) 演習 10：桁のまちがいと、指数をやり直す検算
not_in_text("$10$ 万くらい", "4×10^5 を 10 万と書いていた（レビュー3）")
eq(sf("4", 5), 400000, "4×10^5 = 400 000（40 万）")
in_text("$4 \\times 10^{5}$ は $40$ 万", "40 万に直っている")
chk(sp.floor(sp.log(sf("1.2", -2) / sf("1.2", -39), 10)) == 37,
    "生徒の答えは 30 桁以上小さい（実際は 37 桁）")
# (4) 「唯一の検算」は言いすぎだった
not_in_text("これが**唯一の検算**", "唯一と書いていた（レビュー6）")
in_text("**手早い検算**", "直した言い方")
not_in_text("いちばん速い検算", "並ぶ／いちばん が噛み合っていなかった（レビュー2-B2）")
# (5) 掛け算・割り算のあとの a は「よくある」
not_in_text("割り算のあとは小さくなりすぎます。", "無条件だった断定（レビュー7）")
in_text("小さくなりすぎることが、よくあります", "直した言い方")
not_in_text("そこに点が付いています", "配点の根拠のない主張（レビュー12）")
# (6) 例題 1(b) は「逆」ではない（(a) も右に動かす）
not_in_text("今度は逆に、小数点を右に", "誤りだった説明（レビュー8）")
# (7) 桁数だけでは k の符号が決まらない
not_in_text("動かした桁数が $k$ です。", "符号が抜けていた主文（レビュー9）")
in_text("動かした桁数が $k$ の大きさを、動かした向きが $k$ の符号を決めます",
        "直した主文")
# (8) 演習 2 の検算は、往きと復りで同じ技能だった
not_in_text("同じことの繰り返しにはなりません", "言いすぎだった検算（レビュー10）")
chk(sp.Integer(10) ** -5 < sp.Rational(306, 10000000) < sp.Integer(10) ** -4,
    "0.0000306 は 10^-5 と 10^-4 のあいだ（挟み込みで捕まる）")
# (9) 指数を見て分かるのは「けた」
not_in_text("**大きさは指数（$10$ の右上の数）を見るだけ**", "言いすぎ（レビュー12）")
# (10) 5.2^30 は電卓の表記ではなく、別の数
not_in_text("`5.2^30` は、どれも", "別の数を電卓表記に混ぜていた（レビュー12）")
in_text("$5.2$ を $30$ 個掛けた数", "別の数だと書いている")
not_in_text("$30$ 回掛けた", "数え方を「個」にそろえた")
chk(sp.floor(sp.log(sp.Rational("5.2") ** 30, 10)) == 21,
    "5.2^30 はおよそ 3×10^21（10^30 ではない）")
chk(abs(float(sp.Rational("5.2") ** 30) / 3e21 - 1) < 0.02,
    "5.2^30 ≒ 3×10^21")
# (11) 負の指数の言い方
not_in_text("**負の指数では、$0$ に近いほうが大きい**", "主語が曖昧だった（レビュー12）")
chk(sf("1", -3) > sf("1", -4), "10^-3 > 10^-4")
# (12) 演習 8 の日本語訳が「上に」になっていた
not_in_text("$4$ つの数が上に書かれています", "位置が逆だった訳（レビュー12）")

# ══════════════════════════════════════════════════════════
# 6-C. 2 回目のレビューで直したところの見張り
# ══════════════════════════════════════════════════════════
not_in_text("## 符号は、$1$ より大きいか小さいかで決まります",
            "1<=x<10 で成り立たない符号ルール（レビュー2-A1）")
in_text("- 元の数が **$1$ 以上 $10$ 未満** なら、$k$ は **$0$**",
        "k=0 の場合を入れた（レビュー2-A1）")
chk(sf("8", 0) == 8 and 1 <= sp.Rational(8) < 10,
    "8 は 1 より大きいが k = 0（旧ルールの反例）")
in_text("ここでは $3$ つのことを確かめます", "Why it works の予告が 3 つ（レビュー2-A2）")
not_in_text("ここでは $2$ つのことを確かめます", "予告が 2 つだった")
in_text("整数の全体を $\\mathbb{Z}$ と書き", "Z の説明を足した（レビュー2-A3）")
chk(TEXT.index("整数の全体を $\\mathbb{Z}$ と書き") < TEXT.index("k \\in \\mathbb{Z}$.]{.q-en}"),
    "Z の説明が、問題文での初出より前にある")
in_text("負の数は、$-3.2 \\times 10^{5}$ のように", "負の数の書き方を足した")
in_text("**「$2$ 通りに書けた」と、いったん認めてしまう**", "背理法の道具立てを説明（レビュー2-A4）")
in_text("**まず、右辺の大きさを見ます。**", "証明に見出しの合図（レビュー2-A4）")
in_text("**次に、左辺の大きさを見ます。**", "証明に見出しの合図（レビュー2-A4）")
not_in_text("一般性を失いません", "無説明の専門語（レビュー2-A4）")
not_in_text("**そのかわり、$10^{m}", "接続詞が逆だった（レビュー2-F2）")
in_text("**小さい目盛り $1$ つで $10$ 倍**", "目盛りの説明（レビュー2-G2）")
not_in_text("**$1$ 目盛りで $10$ 倍**になっています", "ラベル付き目盛りと噛み合わなかった")
chk(TEXT.count("（標準形・指数表記）") == 2 and "（指数表記・標準形）" not in TEXT,
    "standard form の訳は見出しと箇条書きの 2 か所、語順もそろえた（レビュー2-E1）")
not_in_text("Do not use a calculator in this question", "問題文から電卓の断りを外した（レビュー2-C9）")
in_text("**例題も演習も、すべて電卓なしで解けます。**", "案内に 1 回だけ書いた")
# 問題文の form の指定：最初の小問に条件、以降は same form
chk(TEXT.count("where $1 \\leq a < 10$ and $k \\in \\mathbb{Z}$.]{.q-en}") == 13,
    "条件つきの form 指定が 13 か所")
chk(TEXT.count("in the same form.]{.q-en}") == 6, "in the same form が 6 か所")
# 例題 1 は (b) が「普通の数」なので、(c) に same form を使わない（レビュー3）
not_in_text("[Write $84 \\times 10^{-7}$ in the same form.]{.q-en}",
            "same form の先行詞がずれていた（レビュー3-1）")
chk(TEXT.count("**すべて電卓なしで解けます。**") == 0
    and TEXT.count("**例題も演習も、すべて電卓なしで解けます。**") == 1,
    "電卓なしの案内は 1 回だけ（レビュー3-2）")
not_in_text("を求められたら $5 \\times 10^{2}$", "問題文と食いちがう仮定形（レビュー3-3）")
chk(TEXT.count("$n$ is a pure number") == 1 and "the quotient is a pure number" not in TEXT,
    "演習 9 の答えが n を指している（レビュー3-4）")
in_text("**$n = 4$、つまりただの $4$**", "解説も n を指している（レビュー3-4）")
chk("合計の大きさ" not in TEXT and "$n$ 倍の大きさ" not in TEXT,
    "ファイルは「容量」、検算の「大きさ」と区別した（レビュー3-5）")
not_in_text("giving your answer in the form $a \\times 10^{k}$.]{.q-en}",
            "条件なしの form 指定は残っていない（レビュー2-C2）")
not_in_text("in the form $a \\times 10^{k}$ metres", "単位を form の後ろに貼らない（レビュー2-C7）")
not_in_text("in the form $a \\times 10^{k}$ kg", "同上")
not_in_text("A student stops at", "口語だった（レビュー2-C8）")
not_in_text("how many times heavier", "曖昧だった言い方（レビュー2-C6）")
not_in_text("[Justify why", "IB では使わない形（レビュー2-C6）")
in_text("The first file is $n$ times as large as the second", "n を使う言い方に")
not_in_text("Four numbers are written below", "Consider に直した（レビュー2-C10）")
in_text("上の $4$ つの数について答えなさい。", "訳の位置（レビュー2-D1）")
in_text("誤りを**すべて**指摘し", "複数であることを訳に出した（レビュー2-D2）")
not_in_text("Adding requires a common factor", "座りの悪かった英語（レビュー2-C4）")
not_in_text("give back $6", "return に直した")
not_in_text("A quick check on the size", "of に直した")
not_in_text("not acceptable in examinations", "シラバスにない限定（レビュー2-C10）")
not_in_text("$3$ の前に $0$ が $3$ 個です", "数え方が紛らわしかった（レビュー2-H）")
not_in_text("`E` を入力する専用のキー", "未検証の主張（レビュー2-H）")
# 演習 9 は GB（例題 3(c) との文脈の重なりを避けた）
in_text("A memory card holds two files", "演習 9 の文脈を変えた（レビュー2-F4）")
chk(TEXT.count("Two samples have masses") == 1, "「試料の質量」は例題 3(c) だけ")
eq(sf("4.8", -3) + sf("1.2", -3), sf("6", -3), "演習9(a) GB でも同じ数")
in_fig("10 or bigger, so $k$ is positive", "図の注記も k=0 を含む言い方に（レビュー2-A1）")
chk("bigger than 1, so" not in FIG, "図の古い注記が残っていない")

# ══════════════════════════════════════════════════════════
# 7. シラバスと公式集の引用（逐語）
# ══════════════════════════════════════════════════════════
# ★ 末尾の「参考：この項目のシラバス（原文）」は、ユーザーの指示で置きません。
#   本文に残すのは、生徒に直接役立つ Guidance の 1 文だけです。
in_text("Calculator or computer notation is not acceptable.", "Guidance の引用")
in_text("5.2E30 is not acceptable", "Guidance の例")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない（ユーザー指示）")
not_in_text("Operations with numbers in the form", "Content の引用は置かない")
not_in_text("Other contexts: Very large", "Connections の引用は置かない")
not_in_text("Students are not permitted access to any calculator.",
            "Paper 1 の引用は置かない")
not_in_text("原文はページ末尾の折りたたみにあります", "末尾ブロックへの参照が残っていない")
chk("Not required" not in TEXT, "この項目に Not required の行はない")

# ══════════════════════════════════════════════════════════
# 8. GDC の記述（AI SL で検証済みの事実と合っているか）
# ══════════════════════════════════════════════════════════
in_text("doc → Settings → Document Settings", "表示形式の場所")
in_text("`Engineering` は使わないでください", "Engineering の注意")
in_text("右矢印キーで指数のボックスから出る", "^ キーの注意")
for bad in ["nDeriv(", "nDerivative(", "solve("]:
    not_in_text(bad, "非 CAS にない命令")
# GDC の callout は、すべて折りたたみで、Paper 2 で始まる
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h for h in _tips if not h.startswith("解説")]
chk(len(_gdc) == 3, f"GDC の折りたたみは 3 つ: {_gdc}")
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk(len([h for h in _tips if h.startswith("解説")]) == 10,
    "演習の「解説」が 10（折りたたみ）")
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")

# ══════════════════════════════════════════════════════════
# 9. 構成の不変量（★AA 版）
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6,
    "--- は 6 本（front matter 2 + 例題 4）")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 7, "model-answer が 7")
chk(len(re.findall(r"^::: \{#exm-aasl11-", TEXT, re.M)) == 4, "例題が 4")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Worked examples", "Common errors",
         "Exercises"]
chk([h for h in _h2 if h in _want] == _want, "5 つの見出しが所定の順")
_idea = [int(m) for m in re.findall(r"^### (\d+)\. ", TEXT, re.M)]
chk(_idea == list(range(1, 9)), f"The idea が 1..8 で連番: {_idea}")
chk(TEXT.count("**検算") >= 14, f"検算が十分ある: {TEXT.count('**検算')}")
chk("**確かめ。**" not in TEXT and "**確かめます。**" not in TEXT,
    "検算の見出しに「確かめ。」を使っていない")
for word in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん",
             "当たり前", "そのとおり"]:
    not_in_text(word, "禁止語")
# ページは Exercises で終わる（末尾にシラバスのブロックを置かない）
chk(TEXT.rstrip().endswith(":::"), "ページの最後は ::: で終わる")
_sections = [h for h in re.findall(r"^## (.+)$", TEXT, re.M)
             if h in ("The idea", "Why it works", "Worked examples",
                      "Common errors", "Exercises")]
chk(_sections and _sections[-1] == "Exercises",
    "節の見出しは Exercises で終わる（末尾にシラバスを置かない）")
# 冒頭に、公式集の表とシラバスの引用ブロックを置いていない（AA の決まり）
_head = TEXT[:TEXT.index("## The idea")]
chk("シラバスが、この項目に求めていること" not in _head,
    "冒頭にシラバスのブロックを置いていない")
chk("公式集の" not in _head, "冒頭に公式集のブロックを置いていない")
chk(_head.count("::: {.callout-note}") == 1
    and "## What you should be able to do" in _head,
    "冒頭は What you should be able to do だけ")
# ✓ ✗ が数式の中に入っていないか
for _blk in re.findall(r"\$\$(.*?)\$\$", TEXT, re.S):
    chk("✓" not in _blk and "✗" not in _blk,
        "表示数式の中に ✓/✗ がある: " + _blk[:40])
for _blk in re.findall(r"(?<!\$)\$([^$\n]+)\$(?!\$)", TEXT):
    chk("✓" not in _blk and "✗" not in _blk,
        "インライン数式の中に ✓/✗ がある: " + _blk[:40])
# 解答例と model-answer に日本語が混ざっていないか
for _blk in re.findall(r"::: \{\.model-answer\}(.*?):::", TEXT, re.S):
    _body = _blk.replace("**試験ではこう書く**", "")
    chk(not re.search(r"[ぁ-んァ-ン一-龥]", _body),
        "model-answer に日本語が混ざっている: " + _body[:40])
# ページ内アンカーが全部あるか
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a in _anchors or _a in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a)
# 他ページへの @-ref を使っていないか
for _r in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r == "aasl11", "他ページの @-ref を使っている: " + _r)
# 他ページへのリンクは、実在するファイルだけ
for _f in set(re.findall(r"\]\((\.\./)?([a-z0-9/-]+\.qmd)", TEXT)):
    _path = os.path.join(BASE, _f[0] + _f[1]) if _f[0] else \
        os.path.join(BASE, _f[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f[1])

# ══════════════════════════════════════════════════════════
# 10. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-1-1-scale.svg")
chk(os.path.exists(SVG), "図がある: aasl-1-1-scale.svg")
chk("](img/aasl-1-1-scale.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"),
    "目視用の PNG は消してある（リポジトリに入れない）")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("x = math.log10(value_of)", "図(a) は log10 の位置に点を打つ（レビュー4）")
chk("(-6, r\"$8" not in FIG, "指数 k をそのまま位置に使っていない（レビュー4）")
chk(abs(float(sp.log(sp.Rational(8, 1000000), 10)) - (-5.0969100)) < 1e-6,
    "log10(8×10^-6) = -5.0969…（-6 ではない）")
chk(abs((-5.0969100) - (-6)) > 0.9, "指数を使うと 0.9 目盛り（8 倍）ずれる")
in_fig("$1 \\\\leq a < 10$", "図(b) の見出しが 1 <= a < 10（レビュー5）")
# ★ 単位と「何の長さか」を、図の中で言い切る
in_fig("(a) Lengths in metres", "図(a) の見出しに単位がある")
for _lab in ["atom (width)", "red blood cell (width)", "person (height)",
             "Earth (diameter)", "Earth to Sun (distance)"]:
    in_fig(_lab, "図(a) のラベルが、何の長さかを言っている: " + _lab)
chk('"metres", ha="right"' not in FIG, "軸の端の metres は消した（ラベルと重なる）")
in_text("**目盛りはすべてメートル**", "本文でも単位を言っている")
in_text("人のところの $1.7$ は身長", "1.7 が身長だと本文に書いてある")
chk("between 1 and 10" not in FIG, "between 1 and 10 という書き方をやめた（レビュー5）")
in_fig("3200000.", "図(b) の大きい数")
in_fig("0.000047", "図(b) の小さい数")
in_fig("6 places to the left", "図(b) のラベル")
in_fig("5 places to the right", "図(b) のラベル")
# 図の数値が本文と合っているか
eq(sf("1", -10), sp.Integer(10) ** -10, "図: 原子は 1×10^-10 m")
eq(sf("1.5", 11), 150000000000, "図: 太陽までは 1.5×10^11 m")
in_text("1.5 \\times 10^{11} \\ \\text{m}", "本文にも 1.5×10^11 m がある")
# 図が演習の答えを載せていないか
for leak in ["9.1", "6.24", "0.000306", "2500000", "3.7", "8.7", "6.24",
             "1.2 \\times 10^{-2}", "9 \\times 10^{4}", "8 \\times 10^{6}",
             "6 \\times 10^{10}", "5 \\times 10^{2}", "7 \\times 10^{4}",
             "1 \\times 10^{4}", "6 \\times 10^{-3}"]:
    chk(leak not in FIGSTR, "図が演習の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 11. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/01-number-and-algebra/aasl-1-1.qmd" in DRAFT,
    "_quarto-draft.yml に登録されている")
chk("glossary-aa.qmd" in DRAFT, "対訳表も登録されている")
chk("- aa-sl/**/*.qmd" in DRAFT, "render の対象に入っている")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB and "aa-sl" not in PUB,
    "公開用の _quarto.yml は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("[SL 1.1 — Numbers in standard form](01-number-and-algebra/aasl-1-1.qmd)"
    in IDX, "index の「いま読めるページ」にある")
chk("**[Numbers in standard form](01-number-and-algebra/aasl-1-1.qmd)** ✅"
    in IDX, "index の一覧に ✅ が付いている")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written),
    f"✅ の数 {len(_ticked)} と、書けたページ数 {len(_written)} が合う")
_m = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_m is not None, "index に「いまのところ N ページ」がある")
if _m:
    chk(int(_m.group(1)) == len(_written), "その N が、書けたページ数と合う")
    chk(int(_m.group(2)) == 60, "全体は 60 ページ（_AA-SL-PLAN.md と同じ）")
PLAN = open(os.path.join(ROOT, "_AA-SL-PLAN.md"), encoding="utf-8").read()
chk("**ページ数：60**" in PLAN, "計画も 60 ページ")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for term in ["| standard form |", "| ordinary number |", "| integer |",
             "| significant figures |", "| order of magnitude |",
             "| calculator notation |", "| distributive law |",
             "**Write down**", "**Explain**", "**Justify**", "**Identify**"]:
    chk(term in GLO, "対訳表にある: " + term)


# ── 採点の言い方（★2026-09-07 の修正）────────────────────
# シラバスから直接確かめられる規則は、弱めない
in_text("電卓の表記は認められません", "シラバス由来の規則はそのまま")
in_text("`5.2E30` と `5.2e30` は電卓の表記なので、**認められません**。",
        "同上")
# markscheme 次第で変わるものは、弱める
in_text("書き方だけで得点を落とすことがあるのは", "断定を弱めた")
in_text("値が合っていても、ここで得点にならないことがあります。", "同上")
not_in_text("ここで点を落とします。", "古い言い方は残っていない")
not_in_text("いちばんもったいない失点", "同上")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
