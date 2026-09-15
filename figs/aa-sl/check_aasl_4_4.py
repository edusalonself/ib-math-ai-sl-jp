"""AA SL 4.4（相関と回帰）の内容を検算する。

    python3 figs/aa-sl/check_aasl_4_4.py
"""
import glob
import math
import os
import re
import sys
from fractions import Fraction as F

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "04-statistics-and-probability")
QMD = os.path.join(BASE, "aasl-4-4.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_4_4.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def eq(u, v, msg=""):
    chk(sp.simplify(sp.nsimplify(u) - sp.nsimplify(v)) == 0,
        msg + f"  ({u} vs {v})")


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def not_in_body(sub, msg=""):
    chk(sub not in BODY, "例題・演習の答えが本文に漏れている: " + msg + " :: " + sub[:50])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


# ══════════════════════════════════════════════════════════
# 0. 道具 —— 回帰と相関を第一原理から
# ══════════════════════════════════════════════════════════
def stats(xs, ys):
    n = len(xs)
    mx = F(sum(F(v) for v in xs), n)
    my = F(sum(F(v) for v in ys), n)
    sxx = sum((F(v) - mx) ** 2 for v in xs)
    syy = sum((F(v) - my) ** 2 for v in ys)
    sxy = sum((F(a) - mx) * (F(b) - my) for a, b in zip(xs, ys))
    return mx, my, sxx, syy, sxy


def regression(xs, ys):
    mx, my, sxx, _syy, sxy = stats(xs, ys)
    a = sxy / sxx
    return a, my - a * mx


def corr(xs, ys):
    _mx, _my, sxx, syy, sxy = stats(xs, ys)
    return float(sxy) / math.sqrt(float(sxx) * float(syy))


# 道具そのものの検算：完全な直線なら r = 1 で、傾きが出る
chk(abs(corr([1, 2, 3], [3, 5, 7]) - 1) < 1e-12, "道具: 完全な直線なら r = 1")
chk(regression([1, 2, 3], [3, 5, 7]) == (2, 1), "道具: y = 2x + 1")
chk(abs(corr([1, 2, 3], [7, 5, 3]) + 1) < 1e-12, "道具: 下がる直線なら r = -1")

# ══════════════════════════════════════════════════════════
# 1. The idea
# ══════════════════════════════════════════════════════════
in_text("{#eq-aasl44-meanpoint}", "mean point のラベル")
in_text("{#eq-aasl44-line}", "回帰直線のラベル")
in_text("{#tbl-aasl44-r}", "r の目安の表")
in_text("{#tbl-aasl44-ab}", "a と b の表")
chk(TEXT.count("@tbl-aasl44-r") >= 2, "r の表を参照している")
chk(TEXT.count("@tbl-aasl44-ab") >= 2, "a と b の表を参照している")
chk(TEXT.count("@eq-aasl44-meanpoint") >= 2, "mean point を参照している")
in_text("- $-1 \\le r \\le 1$ です（", "r の範囲")
in_text("$r = \\pm 1$ は、**すべての点がちょうど $1$ 本の直線上にある**ときだけです",
        "r = ±1 の意味")
in_text("| $0.8$ 以上 | strong |", "r の目安 strong")
in_text("| $0.5$ 以上 $0.8$ 未満 | moderate |", "r の目安 moderate")
in_text("| $0.5$ 未満 | weak |", "r の目安 weak")
in_text("**$r$ の式は公式集にありません。**", "r は公式集にない")
in_text("**mean point という項目は公式集にありません。**", "mean point は公式集にない")
in_text("式は公式集にありません。", "回帰直線も公式集にない")
# 公式集に Topic 4.4 の欄がないこと（このページに callout-important がない）
chk(TEXT.count("callout-important") == 0, "4.4 に公式集の項目はない")

# ══════════════════════════════════════════════════════════
# 2. Why it works
# ══════════════════════════════════════════════════════════
in_text("\\bar{y} = a\\bar{x} + b", "mean point を通る式")
in_text("$2$ 本が一致するのは、点がちょうど $1$ 本の直線（水平でも垂直でもないもの）に",
        "2 本が一致する条件")
in_text("肥料の量と収穫量", "外挿の例")
# 回帰直線は必ず mean point を通る（いくつかのデータで確かめる）
for _xs, _ys in [([1, 2, 3, 4], [2, 5, 4, 9]),
                 ([2, 4, 6, 8, 10], [1, 8, 3, 9, 4]),
                 ([0, 1, 2, 3, 4, 5], [7, 5, 6, 2, 3, 1])]:
    _a, _b = regression(_xs, _ys)
    _mx, _my, _, _, _ = stats(_xs, _ys)
    chk(sp.simplify(_a * _mx + _b - _my) == 0, f"mean point を通る: {_xs}")
# y on x と x on y はちがう直線（|r| = 1 のときだけ一致）
_xs, _ys = [1, 2, 3, 4, 5], [2, 5, 4, 9, 8]
_a1, _b1 = regression(_xs, _ys)          # y = a1 x + b1
_a2, _b2 = regression(_ys, _xs)          # x = a2 y + b2
chk(_a1 * _a2 != 1, "2 本の回帰直線はちがう")
chk(abs(corr(_xs, _ys) ** 2 - float(_a1 * _a2)) < 1e-12, "a1 a2 = r^2")
_lin = [1, 2, 3, 4]
_la1, _ = regression(_lin, [3, 5, 7, 9])
_la2, _ = regression([3, 5, 7, 9], _lin)
chk(_la1 * _la2 == 1, "|r| = 1 なら 2 本は一致")

# ══════════════════════════════════════════════════════════
# 3. 例題 1  勉強時間と得点
# ══════════════════════════════════════════════════════════
eq(sp.Rational("4.2") * 6 + 38, sp.Rational("63.2"), "例題1(c) の答え")
eq(sp.Rational("4.2") * 6, sp.Rational("25.2"), "4.2×6 = 25.2")
eq(sp.Rational("4.2") * 5 + 38, 59, "x=5 なら 59")
eq(sp.Rational("4.2") * 7 + 38, sp.Rational("67.4"), "x=7 なら 67.4")
eq(sp.Rational("63.2") - 59, sp.Rational("4.2"), "差は gradient")
eq(sp.Rational("67.4") - sp.Rational("63.2"), sp.Rational("4.2"), "差は gradient（上）")
eq(sp.Rational("4.2") * 2 + 38, sp.Rational("46.4"), "x=2 なら 46.4")
chk(2 <= 6 <= 9, "x = 6 はデータの範囲の中")
chk(not (2 <= 0 <= 9), "x = 0 は範囲の外")
chk(sp.Rational("0.87") > sp.Rational("0.8"), "r = 0.87 は strong")
chk(sp.Rational("0.87") > 0 and sp.Rational("4.2") > 0, "r と gradient の符号が一致")
in_text("y = 4.2(6) + 38 = 25.2 + 38 = 63.2", "例題1(c) の計算")
in_text("$4.2(2) + 38 = 46.4$", "例題1 の検算")
in_text("*strong positive correlation*", "例題1(a) の答え")

# ══════════════════════════════════════════════════════════
# 4. 例題 2  mean point
# ══════════════════════════════════════════════════════════
X2 = [1, 2, 3, 4, 5, 6, 7, 8]
Y2 = [6, 6, 8, 12, 14, 14, 16, 20]
chk(len(X2) == 8 and len(Y2) == 8, "例題2 は 8 組")
_mx2, _my2, _sxx2, _syy2, _sxy2 = stats(X2, Y2)
eq(sum(X2), 36, "例題2 の Σx")
eq(sum(Y2), 96, "例題2 の Σy")
eq(_mx2, sp.Rational("4.5"), "例題2 の x の平均")
eq(_my2, 12, "例題2 の y の平均")
_a2b, _b2b = regression(X2, Y2)
eq(_a2b, 2, "例題2 の回帰直線の傾きは 2")
eq(_b2b, 3, "例題2 の切片は 3")
chk(abs(corr(X2, Y2) - 0.977) < 5e-4, f"例題2 の r は 0.977: {corr(X2, Y2)}")
eq(2 * sp.Rational("4.5") + 3, 12, "mean point を通る")
eq(2 * 5 + 3, 13, "x=5 の予測は 13")
chk(Y2[4] == 14, "表の x=5 の値は 14")
eq(14 - 13, 1, "予測は 1 小さい")
eq(2 * 4 + 3, 11, "x=4 の予測は 11")
chk(Y2[3] == 12 and 12 - 11 == 1, "x=4 では +1")
eq(F(1 + 8, 2), sp.Rational("4.5"), "両端の平均でも 4.5")
# 残差の合計は 0
chk(sum(F(y) - (_a2b * F(x) + _b2b) for x, y in zip(X2, Y2)) == 0, "残差の合計は 0")
chk(sorted(Y2) == Y2, "y は下がる場所がない")
in_text("\\bar{x} = \\frac{1+2+3+4+5+6+7+8}{8} = \\frac{36}{8} = 4.5", "例題2(a) の x")
in_text("\\bar{y} = \\frac{6+6+8+12+14+14+16+20}{8} = \\frac{96}{8} = 12", "例題2(a) の y")
in_text("2(4.5) + 3 = 9 + 3 = 12 = \\bar{y}", "例題2(b)")

# ══════════════════════════════════════════════════════════
# 5. 例題 3  アイスと救助
# ══════════════════════════════════════════════════════════
chk(sp.Rational("0.91") > 0, "r = 0.91 は positive")
chk(sp.Rational("0.91") > sp.Rational("0.8"), "0.91 は strong")
chk(sp.Rational("0.05") < sp.Rational("0.5"), "0.05 は weak")
# 放物線なら r = 0 になりうる（第 3 節の主張）
_pX = [1, 2, 3, 4, 5, 6, 7, 8]
_pY = [(F(2 * x - 9, 2)) ** 2 for x in _pX]
chk(abs(corr(_pX, _pY)) < 1e-12, f"対称な放物線なら r = 0: {corr(_pX, _pY)}")
chk(len(set(_pY)) > 1, "放物線の y は一定ではない（関係はある）")
in_text("*positive*", "例題3(a) の答え")
in_text("\\text{little or no linear relationship}", "例題3(d) の答え")

# ══════════════════════════════════════════════════════════
# 6. 例題 4  予測
# ══════════════════════════════════════════════════════════
eq(sp.Rational("0.8") * 45 + 12, 48, "例題4(a) の答え")
eq(sp.Rational("0.8") * 40 + 12, 44, "例題4(d) mean point")
eq(sp.Rational("0.8") * 35 + 12, 40, "x=35 を入れると y=40")
chk(20 <= 45 <= 60, "x = 45 は範囲の中")
chk(not (20 <= 100 <= 60), "x = 100 は範囲の外")
eq(60 - 20, 40, "データの幅は 40")
eq(100 - 60, 40, "x=100 は上端から 40 外")
chk(100 - 60 == 60 - 20, "幅と同じだけ外")
eq(sp.Rational("0.8") * 5, 4, "x が 5 増えると y は 4 増える")
eq(44 + 4, 48, "mean point から 48")
in_text("y = 0.8(45) + 12 = 36 + 12 = 48", "例題4(a) の計算")
in_text("0.8(40) + 12 = 32 + 12 = 44 = \\bar{y}", "例題4(d)")
in_text("$0.8(35) + 12 = 40$ となり、代数としては合っています", "例題4(c) の検算")

# ══════════════════════════════════════════════════════════
# 7. 演習 1〜10
# ══════════════════════════════════════════════════════════
# 1  散布図と、目で引く近似直線
XE1 = [1, 2, 3, 4, 5, 6]
YE1 = [3, 5, 4, 7, 8, 9]
_m1x, _m1y, _s1xx, _s1yy, _s1xy = stats(XE1, YE1)
eq(sum(XE1), 21, "演習1 の Σx")
eq(sum(YE1), 36, "演習1 の Σy")
eq(_m1x, sp.Rational("3.5"), "演習1 の x の平均")
eq(_m1y, 6, "演習1 の y の平均")
chk(abs(corr(XE1, YE1) - 0.9487) < 5e-4, f"演習1 の r: {corr(XE1, YE1)}")
chk(corr(XE1, YE1) > 0.8, "演習1 は strong positive")
_a1e, _b1e = regression(XE1, YE1)
eq(_a1e, sp.Rational("1.2"), "演習1 の回帰の傾き")
eq(_b1e, sp.Rational("1.8"), "演習1 の回帰の切片")
_ab = sum(1 for x, y in zip(XE1, YE1) if F(y) > _a1e * F(x) + _b1e)
_be = sum(1 for x, y in zip(XE1, YE1) if F(y) < _a1e * F(x) + _b1e)
chk(_ab >= 1 and _be >= 1, f"回帰直線の上下に点がある: 上 {_ab} / 下 {_be}")
chk(_ab + _be < len(XE1), "直線上にある点もある")
eq(F(1 + 6, 2), sp.Rational("3.5"), "x の両端の平均も 3.5")
in_text("$$\\bar{x} = \\frac{21}{6} = 3.5, \\qquad \\bar{y} = \\frac{36}{6} = 6$$",
        "演習1 の平均の点")
in_text("*strong positive correlation*", "演習1 の答え")
# 2
eq(sp.Rational("2.5") * 7 + sp.Rational("5.5"), 23, "演習2 の検算")
eq(sp.Rational("17.5") / sp.Rational("2.5"), 7, "逆向きに解くと 7")
in_text("$$2.5(7) + 5.5 = 17.5 + 5.5 = 23 = \\bar{y}$$", "演習2 の答え")
# 3
eq(sp.Rational("1.4") * 18 + 8, sp.Rational("33.2"), "演習3 の x=18")
eq(sp.Rational("1.4") * 40 + 8, 64, "演習3 の x=40")
chk(5 <= 18 <= 25, "18 は範囲の中")
chk(not (5 <= 40 <= 25), "40 は範囲の外")
eq(25 - 5, 20, "データの幅は 20")
eq(40 - 25, 15, "上端から 15 外")
eq(F(15, 20), F(3, 4), "幅の 3/4 ぶん外")
in_text("$$x = 40: \\quad y = 1.4(40) + 8 = 64$$", "演習3 の答え")
in_text("データの幅は $25 - 5 = 20$ で、$x = 40$ は上端から $15$ 外です",
        "演習3 の検算")
# 4
chk(abs(sp.Rational("-0.85")) > sp.Rational("0.72"), "|-0.85| > 0.72")
eq(1 - sp.Rational("0.85"), sp.Rational("0.15"), "1 からの距離 0.15")
eq(1 - sp.Rational("0.72"), sp.Rational("0.28"), "1 からの距離 0.28")
chk(sp.Rational("0.15") < sp.Rational("0.28"), "-0.85 のほうが 1 に近い")
in_text("$$\\lvert -0.85 \\rvert = 0.85 > 0.72$$", "演習4 の答え")
# 5
eq(sp.Rational("2.4") * 20 + 15, 63, "演習5 の C")
eq(sp.Rational("2.4") * 19 + 15, sp.Rational("60.6"), "19 枚なら 60.6")
eq(63 - sp.Rational("60.6"), sp.Rational("2.4"), "差は gradient")
eq(sp.Rational("2.4") * 0 + 15, 15, "n=0 なら 15")
in_text("$2.4(19) + 15 = 60.6$", "演習5 の検算")
in_text("*$2.4$: each extra poster adds $\\$2.4$ to the cost on average*",
        "演習5 の解答例")
not_in_text("51 = 2.4n + 15", "逆向きに解かせる問いは消した")
# 6
chk(sp.Rational("0.31") > 0, "0.31 は positive")
chk(sp.Rational("0.31") < sp.Rational("0.5"), "0.31 は weak")
chk(sp.Rational("0.31") != 0, "0 ではない")
in_text("*weak positive correlation*", "演習6 の答え")
# 7
eq(sp.Rational("0.65") * 2 + sp.Rational("4.2"), sp.Rational("5.5"), "m=2 なら 5.5")
eq(sp.Rational("0.65") * 3 + sp.Rational("4.2"), sp.Rational("6.15"), "m=3 なら 6.15")
eq(sp.Rational("6.15") - sp.Rational("5.5"), sp.Rational("0.65"), "差は 0.65")
in_text("$m = 2$ なら $T = 5.5$、$m = 3$ なら $T = 6.15$", "演習7 の検算")
# 8
eq(50 - 10, 40, "演習8 のデータの幅は 40")
eq(200 - 50, 150, "上端から 150 外")
chk(150 > 3 * 40, "幅の 3 倍以上外")
in_text("データの幅は $40$ で、$x = 200$ は上端から $150$ 外です", "演習8 の検算")
# 10
chk(abs(corr([1, 2, 3, 4], [5, 7, 9, 11]) - 1) < 1e-12, "完全な直線なら r = 1")
in_text("$y = 5x + 2$ から $x = \\dfrac{y - 2}{5}$ と変形すること自体はできます",
        "演習10 の検算")

# ══════════════════════════════════════════════════════════
# 8. 例題・演習の答えが本文に漏れていないか
# ══════════════════════════════════════════════════════════
for _leak, _m in [
        ("63.2", "例題1(c)"),
        ("4.2x + 38", "例題1"),
        ("0.977", "例題2"),
        ("2x + 3", "例題2"),
        ("0.8x + 12", "例題4"),
        ("33.2", "演習3"),
        ("0.65m", "演習7"),
        ("strong positive correlation", "例題1(a)"),
        ("weak positive correlation", "演習6"),
]:
    not_in_body(_leak, _m)

# ══════════════════════════════════════════════════════════
# 9. 公式集とシラバス
# ══════════════════════════════════════════════════════════
_quotes = [l for l in TEXT.splitlines() if l.startswith("> ")]
chk(len(_quotes) == 0, f"シラバスの逐語の引用はない: {_quotes}")
not_in_text("Technology should be used to calculate r", "Guidance は貼らない")
not_in_text("correlation does not imply causation", "Guidance は貼らない")
not_in_text("dangers of extrapolation", "Guidance は貼らない")

# ══════════════════════════════════════════════════════════
# 10. 説明のしかた
# ══════════════════════════════════════════════════════════
in_text("答案では、**この $2$ つを両方書きます**。", "強さと向きの両方")
in_text("**単位を付けて述べます。**", "単位を付ける")
in_text("**どんな第 $3$ の変数がありうるか**を $1$ つ挙げると、説明になります。",
        "第 3 の変数を挙げる")
in_text("**(2) $y$ から $x$ を予測しないでください。**", "逆向きの予測")

# ══════════════════════════════════════════════════════════
# 11. GDC
# ══════════════════════════════════════════════════════════
chk("## Using your GDC (TI-Nspire CX II)" in TEXT, "GDC の節がある")
_gdc = TEXT[TEXT.index("## Using your GDC"):TEXT.index("## Exercises")]
chk("**この節は Paper 2 のためのものです。**" in _gdc, "節の冒頭に Paper 2")
_gnum = [int(v) for v in re.findall(r"^### (\d+)\. ", _gdc, re.M)]
chk(_gnum == [1, 2, 3], f"GDC の ### が 1..3: {_gnum}")
for _op in ["ctrl + doc → Add Lists & Spreadsheet",
            "menu → Statistics → Stat Calculations → Linear Regression (mx+b)",
            "ctrl + doc → Add Data & Statistics",
            "menu → Analyze → Regression → Show Linear (mx+b)"]:
    chk(_op in _gdc, "確認ずみの操作: " + _op)
for _row in ["| `m` | 傾き | $a$ |", "| `b` | $y$ 切片 | $b$ |",
             "| `r` | 相関係数 | $r$ |"]:
    chk(_row in _gdc, "結果の読み方: " + _row[:18])
chk("## `m` が IB の $a$ です" in _gdc, "m と a のちがい")
for _bad in ["Num of Lists", "Plot Type", "solve(", "binomPdf"]:
    chk(_bad not in _gdc, "確認していない操作は書かない: " + _bad)

# ══════════════════════════════════════════════════════════
# 12. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 15,
    f"model-answer が 15: {TEXT.count('{.model-answer}')}")
_asks = len(re.findall(r"\[(?:[^\]]*?)(?:Explain|Justify|Comment|Interpret|Identify"
                       r"|Describe|Suggest)(?:[^\]]*?)\]\{\.q-en\}", TEXT))
chk(_asks == 15, f"説明を求める問いが 15: {_asks}")
chk(len(re.findall(r"^::: \{#exm-aasl44-", TEXT, re.M)) == 4, "例題が 4")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例が 14")
chk(TEXT.count("::: {.callout-warning}") == 8, "Common errors 6 + 本文 1 + GDC 1 で 8")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Worked examples", "Common errors",
         "Using your GDC (TI-Nspire CX II)", "Exercises"]
chk([h_ for h_ in _h2 if h_ in _want] == _want, "6 つの見出しが所定の順")
chk([h_ for h_ in _h2 if h_ in _want][-1] == "Exercises", "Exercises で終わる")
_idea = TEXT[TEXT.index("## The idea"):TEXT.index("## Why it works")]
_inum = [int(v) for v in re.findall(r"^### (\d+)\. ", _idea, re.M)]
chk(_inum == list(range(1, 8)), f"The idea が 1..7 で連番: {_inum}")
chk(TEXT.count("**検算") >= 12, f"検算が十分ある: {TEXT.count('**検算')}")
chk("**確かめ。**" not in TEXT and "**確かめます。**" not in TEXT, "「確かめ。」なし")
for word in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん",
             "当たり前", "そのとおり"]:
    not_in_text(word, "禁止語")
for word in ["得点になりません", "点になりません", "点を落とします",
             "認められません", "減点されます"]:
    not_in_text(word, "採点の断定は避ける")
_MASKED = TEXT.replace("\\$", "")
for _blk in re.findall(r"\$\$(.*?)\$\$", _MASKED, re.S):
    chk("✓" not in _blk and "✗" not in _blk, "表示数式に ✓/✗: " + _blk[:40])
for _blk in re.findall(r"(?<!\$)\$([^$\n]+)\$(?!\$)", _MASKED):
    chk("✓" not in _blk and "✗" not in _blk, "インライン数式に ✓/✗: " + _blk[:40])
_parts = TEXT.split("$$")
chk(all("@eq-" not in _parts[i] for i in range(1, len(_parts), 2)),
    "表示数式の中に @-ref がない")
for _blk in re.findall(r"::: \{\.model-answer\}(.*?):::", TEXT, re.S):
    _bb = _blk.replace("**試験ではこう書く**", "")
    chk(not re.search(r"[ぁ-んァ-ン一-龥]", _bb), "model-answer に日本語")
    chk(len(_blk.split()) <= 115, f"model-answer が長すぎない: {len(_blk.split())} 語")
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a0 in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a0 in _anchors or _a0 in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aasl44", "他ページの @-ref: " + _r0)
# 4.10 はまだ書いていないので、リンクだけ許す（レンダーの警告になる）
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or ".qmd#" in _href
        or _href.startswith("http") or _href.startswith("../"),
        "形の合わないリンク: " + _href)
chk(TEXT.count("@fig-aasl44-idea") >= 2, "図を本文から 2 か所以上参照している")
_head = TEXT[:TEXT.index("## The idea")]
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は What you should be able to do の 1 つだけ")
_open = len(re.findall(r"^::: \{", TEXT, re.M))
_close = len(re.findall(r"^:::$", TEXT, re.M))
chk(_open == _close, f"::: の開閉が合う: 開 {_open} / 閉 {_close}")

# ══════════════════════════════════════════════════════════
# 13. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-4-4-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-4-4-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) Direction and strength", "図(a) の題")
in_fig("strong positive", "図(a) のパネル 1")
in_fig("weak positive", "図(a) のパネル 2")
in_fig("on a curve", "図(a) のパネル 3")
in_fig("strong negative", "図(a) のパネル 4")
in_fig("a value of $r$ near $0$ does not mean there is ", "図(a) の説明")
in_fig("(b) Where the line can be trusted", "図(b) の題")
in_fig("range of the data", "図(b) の範囲")
in_fig("extrapolation", "図(b) の外挿")
in_fig("mean point", "図(b) の平均の点")
in_fig("outside the range of the data, nothing has been ", "図(b) の説明")
# 図のパネルの r を、チェッカーでも計算し直す
_PX = [1, 2, 3, 4, 5, 6, 7, 8]
_PANELS = {
    "strong positive": [2, 3, 3, 5, 6, 6, 8, 9],
    "weak positive": [4, 2, 6, 3, 7, 4, 6, 5],
    "on a curve": [12.25, 6.25, 2.25, 0.25, 0.25, 2.25, 6.25, 12.25],
    "strong negative": [9, 8, 8, 6, 5, 5, 3, 2],
}
for _lab, _ys in _PANELS.items():
    chk(str(_ys) in FIGCODE, "図のデータが一致: " + _lab)
chk(corr(_PX, _PANELS["strong positive"]) > 0.8, "パネル 1 は strong positive")
chk(0 < corr(_PX, _PANELS["weak positive"]) < 0.5,
    f"パネル 2 は表の weak の側: {corr(_PX, _PANELS['weak positive'])}")
chk(abs(corr(_PX, _PANELS["on a curve"])) < 1e-9, "パネル 3 は r = 0")
chk(corr(_PX, _PANELS["strong negative"]) < -0.8, "パネル 4 は strong negative")
# 図の r の値が、問題文に書いた r の値と重なっていないこと（3 桁で比べる）
_stem_r = [0.87, 0.977, 0.91, 0.31, -0.85, 0.72, 0.05]
for _lab, _ys in _PANELS.items():
    _fr = round(corr(_PX, _ys), 3)
    for _v in _stem_r:
        chk(abs(_fr - _v) > 5e-4,
            f"図の r {_fr} が問題文の {_v} と重なる（{_lab}）")
in_text("(a) The direction of a correlation is whether the points rise or fall",
        "キャプションが (a) を説明")
in_text("(b) A regression line passes through the mean point", "キャプションが (b) を説明")

# ══════════════════════════════════════════════════════════
# 14. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/04-statistics-and-probability/aasl-4-4.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-4-3.qmd") < DRAFT.index("aasl-4-4.qmd"), "並びが 4.3 → 4.4")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(04-statistics-and-probability/aasl-4-4.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| correlation |", "| causation |", "| scatter diagram |",
           "| regression line |", "| extrapolation |", "| bivariate data |"]:
    chk(_t in GLO, "対訳表にある: " + _t)

# ══════════════════════════════════════════════════════════
# 15. 査読で直したところ（2026-09-08）
# ══════════════════════════════════════════════════════════

# --- §1 が「原因になりそうなほう」を x の決め方にしていた ----------------
in_text("**「原因のほう」ではありません**", "原因では決めない")
not_in_text("ふつう、「原因になりそうなほう」", "古い言い方は消した")

# --- r の範囲・±1・n = 2 の但し書き --------------------------------------
in_text("$x$ の値がすべて同じ、または $y$ の値がすべて同じ、という場合を除きます",
        "r が定まらない場合")
in_text("**点が $2$ つしかなければ $r$ はかならず $\\pm 1$ になります。**", "n = 2")
in_text("（水平でも垂直でもない直線）", "±1 の但し書き")
in_text("点がちょうど $1$ 本の直線（水平でも垂直でもないもの）に乗っているとき",
        "2 本が一致する条件の但し書き")
# n = 2 なら r = ±1
chk(abs(abs(corr([1, 2], [5, 9])) - 1) < 1e-12, "n=2 では |r| = 1")
chk(abs(abs(corr([1, 2], [9, 5])) - 1) < 1e-12, "n=2 では下がっても |r| = 1")

# --- r の目安の表 -------------------------------------------------------
in_text("| $0.5$ 以上 $0.8$ 未満 | moderate |", "境目が重ならない")
not_in_text("| $0.5$ 〜 $0.8$ | moderate |", "重なる書き方は消した")
in_text("シラバスが使う語は **strong・weak・no correlation** で、", "シラバスの語")
in_text("**critical value が与えられていても、強さの述べ方の線引きではありません。**",
        "critical value の役割")
not_in_text("問題文が critical value を与えていれば、それに従います。", "古い hedge は消した")

# --- mean point の「公式集にない」の書き方 -------------------------------
in_text("平均そのものの式 $\\bar{x} = \\dfrac{\\sum f_i x_i}{n}$ は **4.3** の欄にあります",
        "平均の式は 4.3 にある")
in_text("（[SL 4.3](aasl-4-3.qmd#mean)）", "SL 4.3 を参照")

# --- Why it works の mean point の議論 -----------------------------------
in_text("ずれ（residual）の **$2$ 乗の合計**がいちばん小さくなるように決めます。",
        "2 乗の合計")
in_text("直線を $\\dfrac{S}{n}$ だけ上下に平行移動すると、ずれの $2$ 乗の合計は"
        "**かならず小さくなります**。", "平行移動の議論")
not_in_text("$y$ の方向のずれ（residual）を全体として小さくするように決めます。"
            "そのとき、**ずれの合計がちょうど $0$ になる**ように決まります。",
            "結論を前提にした書き方は消した")
# 平行移動すると 2 乗の合計が減ることを、実データで確かめる
_tx, _ty = [1, 2, 3, 4, 5], [2, 5, 4, 9, 8]
_ta, _tb = regression(_tx, _ty)
def _ss(a, b):
    return sum((F(y) - (a * F(x) + b)) ** 2 for x, y in zip(_tx, _ty))
chk(sum(F(y) - (_ta * F(x) + _tb) for x, y in zip(_tx, _ty)) == 0,
    "最小のところでは残差の合計が 0")
for _d in (F(1, 2), F(-1, 2), 1, -1):
    chk(_ss(_ta, _tb + _d) > _ss(_ta, _tb), f"上下にずらすと増える ({_d})")

# --- 因果を「ない」と断定していた ----------------------------------------
in_text("The temperature would then raise both quantities at once, so a correlation "
        "can appear even if neither one affects the other.", "例題3(c) は仮定法")
not_in_text("The temperature therefore raises both quantities at once",
            "断定は消した（例題3）")
in_text("which is enough to produce a strong positive correlation even if the number "
        "of engines has no effect on the damage at all", "演習9 は even if")
not_in_text("even though neither quantity causes the other", "断定は消した（演習9）")
not_in_text("without one causing the other", "断定は消した（演習9 の解答例）")
in_text("so the two rise together whether or not the engines affect the damage",
        "演習9 の解答例")

# --- 例題2(c) の検算の符号 ------------------------------------------------
in_text("$x = 2$ では予測 $7$、表は $6$ で $-1$。$x = 5$ では予測 $13$、表は $14$ で "
        "$+1$ です", "例題2(c) の検算")
not_in_text("$x = 4$ では予測 $11$、表は $12$ で $+1$。$x = 5$ では $-1$ です",
            "符号をまちがえた検算は消した")
# 残差の符号を実際に確かめる
_res = [y - (2 * x + 3) for x, y in zip(X2, Y2)]
chk(_res == [1, -1, -1, 1, 1, -1, -1, 1], f"残差: {_res}")
chk(_res[1] == -1 and _res[4] == 1, "x=2 は -1、x=5 は +1")
chk(_res[3] == 1 and _res[4] == 1, "x=4 と x=5 は同じ符号（だから対比にならない）")

# --- 例題2(b)・演習2 の検算を、傾きを使うものにした ----------------------
in_text("**平均の点から $1$ つ動かして見ます。** $x$ が $4.5$ から $5.5$ へ $1$ 増えると、"
        "直線は $y$ を $2$ 増やして $14$ と予測します", "例題2(b) の検算")
eq(2 * sp.Rational("5.5") + 3, 14, "x=5.5 なら 14")
in_text("$\\bar{x} = 7$ から $x = 9$ へ $2$ 増えると、$y$ は $2.5 \\times 2 = 5$ 増えて "
        "$28$ になるはずです。", "演習2 の検算")
eq(sp.Rational("2.5") * 9 + sp.Rational("5.5"), 28, "2.5(9)+5.5 = 28")
eq(23 + sp.Rational("2.5") * 2, 28, "平均から 2 増やしても 28")
not_in_text("$12 = 2\\bar{x} + 3$ を解くと $\\bar{x} = 4.5$", "解き直す検算は消した")
not_in_text("$23 = 2.5x + 5.5$ から $2.5x = 17.5$", "解き直す検算は消した（演習2）")

# --- 例題2(d) の検算を、直線への近さにした -------------------------------
in_text("$y = 2x + 3$ が予測する値は $5, 7, 9, 11, 13, 15, 17, 19$ で、表との差は"
        "どれも $1$ です", "例題2(d) の検算")
chk([2 * x + 3 for x in X2] == [5, 7, 9, 11, 13, 15, 17, 19], "予測値")
chk(all(abs(v) == 1 for v in _res), "差はどれも 1")
eq(max(Y2) - min(Y2), 14, "y の幅は 14")
not_in_text("$y$ は $6$ から $20$ まで、下がる場所がなく増えています", "単調性の検算は消した")
# 単調でも r が 1 に近くない例（この検算が必要だった理由）
chk(corr([1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 4, 8, 16, 32, 64, 128]) < 0.9,
    "単調でも r は 1 に近くない")

# --- 演習9 の検算を、交絡をそろえるものにした ----------------------------
in_text("**第 $3$ の変数をそろえてみます。** 同じ規模の火災どうしだけで比べたら、",
        "演習9 の検算")
not_in_text("被害が先に決まり、それを見て消防車が送られます", "根拠のない順序は消した")

# --- 演習1 を、散布図と目で引く直線にした --------------------------------
in_text("Draw a scatter diagram, mark the mean point on it, and draw a line of best "
        "fit by eye through the mean point.", "演習1 は作図")
in_text("**目で引く直線に、$1$ つの正解はありません。** ただし、"
        "**平均の点は必ず通します**。", "目で引く直線の注意")
in_text("引いた直線の上と下のどちらにも点があれば", "上下に点がある")
not_in_text("The regression line of $y$ on $x$ for a set of data is $y = -3x + 50$",
            "古い演習1 は消した")
# 目標に対応する問いができたこと
chk("Draw a scatter diagram" in TEXT, "散布図をかかせる問いがある")
chk("line of best fit by eye" in TEXT, "目で引く直線の問いがある")

# --- 演習4 に model answer を足し、検算を入れかえた ----------------------
in_text("State which shows the stronger correlation. Justify your answer.",
        "演習4 は Justify を独立させた")
in_text("**符号だけ入れかえて考えます。** もし $2$ つ目が $-0.72$ だったら、",
        "演習4 の検算")
in_text("The negative sign only tells us that one variable decreases as the other "
        "increases; it does not make the correlation weaker.", "演習4 の model answer")
not_in_text("$0.85$ は $1$ まで $0.15$、$0.72$ は $0.28$ です", "循環した検算は消した")
chk(abs(sp.Rational("-0.72")) < abs(sp.Rational("-0.85")), "符号を変えても結論は同じ")

# --- 演習5 が、第 7 節が禁じていることをやらせていた ---------------------
in_text("Find the cost of printing $20$ posters. Interpret the value $2.4$ in the "
        "context of the question.", "演習5 は逆向きに解かせない")
in_text("**逆に「$51$ ドルで何枚か」を求めるのは、別の話です。**", "逆向きは別の話と明記")
not_in_text("find how many posters can be printed for", "逆向きの問いは消した")
not_in_text("**ここは $x$ から $y$ を出しているのではありません。**", "誤った区別は消した")

# --- 演習6 の検算を、境目と比べるものにした ------------------------------
in_text("**境目と比べます。** weak と moderate の境目は $0.5$ です", "演習6 の検算")
not_in_text("符号は $+$ なので positive、$\\lvert r \\rvert = 0.31$ は $0$ に近いので weak",
            "言い直しの検算は消した")

# --- GDC の欄の名前 -----------------------------------------------------
in_text("$x$ の列と $y$ の列を、$x$・$y$ の順に指定します。", "欄の名前は書かない")
not_in_text("`X List` に $x$ の列", "確認していない欄の名前は消した")

# --- 図 (a) のパネル 2 が、表の weak と食いちがっていた ------------------
chk(abs(corr(_PX, [4, 2, 6, 3, 7, 4, 6, 5]) - 0.433) < 5e-4,
    f"新しいパネル 2 の r: {corr(_PX, [4, 2, 6, 3, 7, 4, 6, 5])}")
chk(corr(_PX, [4, 2, 6, 3, 7, 4, 6, 5]) < 0.5, "表の weak の側に入る")
in_fig("[4, 2, 6, 3, 7, 4, 6, 5]", "新しいパネル 2 のデータ")
chk("[4, 2, 6, 3, 7, 4, 8, 5]" not in FIGCODE, "古いパネル 2 のデータは消した")


# ══════════════════════════════════════════════════════════
# E08・E09  演習1 — 散布図の完成図と、GDC で r・y on x
# ══════════════════════════════════════════════════════════
in_text("[Use your calculator to find Pearson's product-moment correlation "
        "coefficient $r$, correct to three significant figures.]",
        "E08 演習1(b) は r")
in_text("[Use your calculator to find the equation of the regression line "
        "of $y$ on $x$. State how you check that six pairs of values have "
        "been entered.]", "E08 演習1(c) は y on x")
in_text("$$r = 0.949 \\quad (3 \\text{ s.f.})$$", "E08 r の答え")
in_text("$$y = 1.2x + 1.8$$", "E08 回帰直線の答え")
in_text("**入力の数は、画面の $n$ で確かめます。**", "E08 入力件数の確認")
in_text("(img/aasl-4-4-ex1.svg){#fig-aasl44-ex1 width=100%}",
        "E09 演習1 の解答図")
# x = 1..6, y = 3,5,4,7,8,9 から r と y on x を出し直す
_xs = [1, 2, 3, 4, 5, 6]
_ys = [3, 5, 4, 7, 8, 9]
_n8 = len(_xs)
_mx = sp.Rational(sum(_xs), _n8)
_my = sp.Rational(sum(_ys), _n8)
_sxy = sum(_a * _b for _a, _b in zip(_xs, _ys)) - _n8 * _mx * _my
_sxx = sum(_a ** 2 for _a in _xs) - _n8 * _mx ** 2
_syy = sum(_b ** 2 for _b in _ys) - _n8 * _my ** 2
chk(_mx == sp.Rational(7, 2) and _my == 6, "E08 平均の点は (3.5, 6)")
chk(sp.simplify(_sxy / _sxx - sp.Rational(6, 5)) == 0, "E08 傾きは 1.2")
chk(sp.simplify(_my - (_sxy / _sxx) * _mx - sp.Rational(9, 5)) == 0,
    "E08 切片は 1.8")
_r8 = _sxy / sp.sqrt(_sxx * _syy)
chk(float("%.3g" % float(_r8)) == 0.949, "E08 r は 3 有効数字で 0.949")
chk(0 < float(_r8) < 1, "E08 r は 0 と 1 のあいだ")
chk(sp.simplify(sp.Rational(6, 5) * _mx + sp.Rational(9, 5) - _my) == 0,
    "E08 回帰直線は平均の点を通る")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
