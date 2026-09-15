"""AA SL 4.2（データの表し方）の内容を検算する。

    python3 figs/aa-sl/check_aasl_4_2.py
"""
import glob
import os
import re
import sys
from fractions import Fraction as F

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "04-statistics-and-probability")
QMD = os.path.join(BASE, "aasl-4-2.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_4_2.py"), encoding="utf-8").read()
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
# 0. 道具
# ══════════════════════════════════════════════════════════
def med(a):
    a = sorted(a)
    m = len(a)
    return F(a[m // 2]) if m % 2 else (F(a[m // 2 - 1]) + F(a[m // 2])) / 2


def quartiles(d):
    d = sorted(d)
    n = len(d)
    lo = d[:n // 2]
    hi = d[n // 2 + 1:] if n % 2 else d[n // 2:]
    return med(lo), med(d), med(hi)


def expand(x, f):
    return [v for v, c in zip(x, f) for _ in range(c)]


def cumf(f):
    return [sum(f[:i + 1]) for i in range(len(f))]


def interp(bnd, f, pos):
    """累積度数グラフを直線とみなして pos 番目の値を出す。"""
    cf = cumf(f)
    for i in range(len(f)):
        if cf[i] >= pos:
            below = cf[i - 1] if i else 0
            return F(bnd[i]) + F(pos - below, f[i]) * (bnd[i + 1] - bnd[i])
    return None


def fences(q1, q3):
    iqr = q3 - q1
    return q1 - F(3, 2) * iqr, q3 + F(3, 2) * iqr


# 道具そのものの検算
chk(cumf([1, 2, 3]) == [1, 3, 6], "道具: 累積度数")
chk(expand([0, 1], [2, 3]) == [0, 0, 1, 1, 1], "道具: 展開")
eq(interp([0, 10], [10], 5), 5, "道具: 直線での読み")
eq(interp([0, 10, 20], [10, 10], 15), 15, "道具: 2 階級")

# ══════════════════════════════════════════════════════════
# 1. The idea — 本文の表
# ══════════════════════════════════════════════════════════
# 離散の表（n = 24）
eq(7 + 9 + 5 + 3, 24, "本文の離散表の合計は 24")
in_text("離散データの度数分布表（$n = 24$）", "離散表の見出し")
# 累積度数の表（n = 20）
chk(cumf([6, 9, 4, 1]) == [6, 15, 19, 20], "本文の累積度数表")
in_text("| $10 \\le t < 20$ | $9$ | $15$ |", "累積度数表の行")
in_text("累積度数の作り方（$n = 20$）", "累積表の見出し")
in_text("$(20, 15)$ に打ちます。$(10, 15)$ でも $(15, 15)$ でもありません。",
        "点は階級の上の端")
# 読み方の表
for _r in ["| median | $\\dfrac{n}{2}$ |", "| $Q_1$ | $\\dfrac{n}{4}$ |",
           "| $Q_3$ | $\\dfrac{3n}{4}$ |"]:
    in_text(_r, "読み方の表: " + _r[:20])
in_text("{#tbl-aasl42-read}", "読み方の表のラベル")
chk(TEXT.count("@tbl-aasl42-read") >= 3, "読み方の表を参照している")
in_text("ここでは $n$ を使います。$n+1$ ではありません。**", "n を使う（表について）")
in_text("{#eq-aasl42-interp}", "補間の式のラベル")
in_text("{#eq-aasl42-iqr}", "IQR の式のラベル")
# 階級の書き方
in_text("$0$–$9$、$10$–$19$", "すき間のある書き方の例")
in_text("$9.4$ がどこにも入りません", "9.4 が入らない")
in_text("$10 \\le t < 20$ に $20$ は入りません。", "上端は入らない")

# ══════════════════════════════════════════════════════════
# 2. Why it works
# ══════════════════════════════════════════════════════════
in_text("下端に打つと、**階級 $1$ つぶん左にずれます**", "下端に打つとずれる")
in_text("$\\dfrac{n+1}{2}$ を使うのは、**値を $1$ つずつ並べて数えるとき**です。",
        "n+1 はいつ使うか")
in_text("だから、グループ化された表から出した median は、必ず **estimate**（推定値）です。",
        "推定値になる")
in_text("のばすと、**外れ値が図から消えます**", "ひげをのばすと消える")
# n/2 と (n+1)/2 の差は n が大きいほど小さい
for _n in (10, 100, 1000):
    chk(abs(F(_n + 1, 2) - F(_n, 2)) == F(1, 2), f"差はいつも 1/2 ({_n})")
    chk(F(1, 2) / _n < F(1, 2) / (_n // 10 or 1) or _n == 10,
        "n が大きいほど相対的に小さい")

# ══════════════════════════════════════════════════════════
# 3. 例題 1  ペットの数
# ══════════════════════════════════════════════════════════
X1, F1 = [0, 1, 2, 3, 4], [8, 12, 15, 4, 1]
chk(sum(F1) == 40, "例題1 の n は 40")
chk(cumf(F1) == [8, 20, 35, 39, 40], f"例題1 の累積度数: {cumf(F1)}")
D1 = expand(X1, F1)
_q1, _m1, _q3 = quartiles(D1)
eq(_m1, F(3, 2), "例題1 の median は 1.5")
eq(_q1, 1, "例題1 の Q1")
eq(_q3, 2, "例題1 の Q3")
eq(_q3 - _q1, 1, "例題1 の IQR")
eq(max(D1) - min(D1), 4, "例題1 の range")
chk(sorted(D1)[19] == 1 and sorted(D1)[20] == 2, "20 番目と 21 番目は 1 と 2")
chk(sorted(D1)[9] == 1 and sorted(D1)[10] == 1, "10 番目と 11 番目はどちらも 1")
chk(sorted(D1)[29] == 2 and sorted(D1)[30] == 2, "30 番目と 31 番目はどちらも 2")
_lo1, _hi1 = fences(_q1, _q3)
eq(_hi1, F(7, 2), "例題1 の上の境目 3.5")
eq(_lo1, F(-1, 2), "例題1 の下の境目 -0.5")
chk(4 > _hi1, "4 は外れ値")
chk(3 <= _hi1, "3 は外れ値ではない")
chk(min(D1) > _lo1, "小さいほうに外れ値はない")
chk(max(v for v in D1 if v <= _hi1) == 3, "ひげの先は 3")
chk(len([v for v in D1 if v < _q1]) == 8, "Q1 より下は 8 人")
in_text("0, \\quad 1, \\quad 1.5, \\quad 2, \\quad 3", "例題1(d) の 5 つの数")
in_text("$\\times$ で打つのは $4$ です。", "例題1(d) の × ")
in_text("$8 + 12 + 15 + 4 + 1 = 40$", "例題1 の検算")

# ══════════════════════════════════════════════════════════
# 4. 例題 2  グループ化された時間
# ══════════════════════════════════════════════════════════
B2, F2 = [0, 10, 20, 30, 40, 50], [5, 10, 15, 8, 2]
chk(sum(F2) == 40, "例題2 の n は 40")
chk(cumf(F2) == [5, 15, 30, 38, 40], f"例題2 の累積度数: {cumf(F2)}")
eq(interp(B2, F2, F(40, 4)), 15, "例題2 の Q1 は 15")
eq(interp(B2, F2, F(3 * 40, 4)), 30, "例題2 の Q3 は 30")
eq(interp(B2, F2, F(40, 2)), F(70, 3), "例題2 の median は 70/3")
eq(interp(B2, F2, F(3 * 40, 4)) - interp(B2, F2, F(40, 4)), 15, "例題2 の IQR は 15")
chk(abs(float(F(70, 3)) - 23.3) < 0.034, "70/3 は 3 桁で 23.3")
chk(round(float(F(70, 3)), 1) == 23.3, "3 s.f. で 23.3")
eq(10 + F(5, 10) * 10, 15, "Q1 の補間")
eq(20 + F(5, 15) * 10, F(70, 3), "median の補間")
chk(15 < F(70, 3) < 30, "median は Q1 と Q3 のあいだ")
# 階級のまん中（25）と比べる
chk(F(70, 3) < 25, "median は階級のまん中 25 より小さい")
eq(F(20 + 30, 2), 25, "階級のまん中は 25")
in_text("5, \\quad 15, \\quad 30, \\quad 38, \\quad 40", "例題2(a)")
in_text("= \\frac{70}{3} = 23.3 \\ (3 \\text{ s.f.})", "例題2(c) の答え")
in_text("$5 + 10 + 15 + 8 + 2 = 40$", "例題2 の検算")
in_text("$15 < 23.3 < 30$", "median の位置の検算")

# ══════════════════════════════════════════════════════════
# 5. 例題 3  箱ひげ図の比較
# ══════════════════════════════════════════════════════════
A3 = dict(mn=22, q1=38, md=52, q3=61, mx=78)
B3 = dict(mn=35, q1=48, md=54, q3=60, mx=70)
eq(A3["q3"] - A3["q1"], 23, "A の IQR")
eq(B3["q3"] - B3["q1"], 12, "B の IQR")
eq(A3["mx"] - A3["mn"], 56, "A の range")
eq(B3["mx"] - B3["mn"], 35, "B の range")
chk(56 > 35, "range が大きいのは A")
chk(B3["md"] > A3["md"], "median が大きいのは B")
chk(B3["q3"] - B3["q1"] < A3["q3"] - A3["q1"], "IQR が小さいのは B")
eq(B3["md"] - B3["q1"], 6, "B の median - Q1")
eq(B3["q3"] - B3["md"], 6, "B の Q3 - median")
chk(B3["md"] - B3["q1"] == B3["q3"] - B3["md"], "B の箱は対称")
eq(B3["q1"] - B3["mn"], 13, "B の下のひげ")
eq(B3["mx"] - B3["q3"], 10, "B の上のひげ")
eq(A3["md"] - A3["q1"], 14, "A の median - Q1")
eq(A3["q3"] - A3["md"], 9, "A の Q3 - median")
chk(A3["md"] - A3["q1"] != A3["q3"] - A3["md"], "A の箱は対称でない")
eq(14 - 9, 5, "A の差は 5")
chk(B3["q1"] > A3["q1"], "Q1 は B のほうが上")
chk(B3["q3"] < A3["q3"], "Q3 は A のほうが上")
for _d in (A3, B3):
    chk(_d["mn"] <= _d["q1"] <= _d["md"] <= _d["q3"] <= _d["mx"],
        "5 つの数が小さい順")
in_text("$$\\text{A}: \\ 61 - 38 = 23, \\qquad \\text{B}: \\ 60 - 48 = 12$$",
        "例題3(a)")
in_text("$78 - 22 = 56 > 70 - 35 = 35$", "例題3(b) の理由")

# ══════════════════════════════════════════════════════════
# 6. 例題 4  パーセンタイル
# ══════════════════════════════════════════════════════════
B4, F4 = [10, 20, 30, 40, 50, 60], [3, 9, 18, 15, 5]
chk(sum(F4) == 50, "例題4 の n は 50")
chk(cumf(F4) == [3, 12, 30, 45, 50], f"例題4 の累積度数: {cumf(F4)}")
eq(3 + 9 + 18, 30, "40 cm 未満は 30 本")
eq(F(90, 100) * 50, 45, "90 パーセンタイルの位置は 45")
eq(interp(B4, F4, 45), 50, "90 パーセンタイルは 50 cm")
chk(F4[-1] == 5, "上の 10% は 5 本")
eq(F(10, 100) * 50, 5, "50 の 10% は 5")
_med4 = interp(B4, F4, 25)
chk(30 < _med4 < 40, f"median は 30-40 の階級: {_med4}")
chk(50 > 40, "90 パーセンタイルは median より大きい")
in_text("$$3 + 9 + 18 = 30$$", "例題4(a)")
in_text("3, \\quad 12, \\quad 30, \\quad 45, \\quad 50", "例題4(b)")
in_text("90\\text{th percentile} = 50 \\ \\text{cm}", "例題4(c)")
in_text("$3 + 9 + 18 + 15 + 5 = 50$", "例題4 の検算")

# ══════════════════════════════════════════════════════════
# 7. 演習 1〜10
# ══════════════════════════════════════════════════════════
# 1  きょうだいの人数
XE1, FE1 = [0, 1, 2, 3, 4, 5], [4, 7, 9, 6, 3, 1]
chk(sum(FE1) == 30, "演習1 の n は 30")
chk(cumf(FE1) == [4, 11, 20, 26, 29, 30], f"演習1 の累積度数: {cumf(FE1)}")
DE1 = expand(XE1, FE1)
_a, _b, _c = quartiles(DE1)
eq(_b, 2, "演習1 の median")
eq(_a, 1, "演習1 の Q1")
eq(_c, 3, "演習1 の Q3")
eq(_c - _a, 2, "演習1 の IQR")
eq(max(DE1) - min(DE1), 5, "演習1 の range")
chk(sorted(DE1)[14] == 2 and sorted(DE1)[15] == 2, "15 番目と 16 番目はどちらも 2")
chk(sorted(DE1)[7] == 1, "8 番目は 1")
chk(sorted(DE1)[22] == 3, "23 番目は 3")
_lo, _hi = fences(_a, _c)
eq(_lo, -2, "演習1 の下の境目")
eq(_hi, 6, "演習1 の上の境目")
chk([v for v in DE1 if v < _lo or v > _hi] == [], "演習1 に外れ値はない")
in_text("$$\\text{median} = 2, \\qquad Q_1 = 1, \\qquad Q_3 = 3$$", "演習1 の答え")
in_text("$4+7+9+6+3+1 = 30$", "演習1 の検算")
in_text("累積度数が $4$ から $11$ に増えるあいだにあるので $x = 1$", "演習1 の位置の検算")
# 2  りんごの質量
BE2, FE2 = [40, 50, 60, 70, 80, 90], [6, 14, 22, 12, 6]
chk(sum(FE2) == 60, "演習2 の n は 60")
chk(cumf(FE2) == [6, 20, 42, 54, 60], f"演習2 の累積度数: {cumf(FE2)}")
eq(F(60, 2), 30, "演習2 の位置は 30")
chk(cumf(FE2)[1] < 30 <= cumf(FE2)[2], "30 は 3 番目の階級")
chk(interp(BE2, FE2, 30) is not None and 60 < interp(BE2, FE2, 30) < 70,
    "median は 60-70 の中")
in_text("$$60 \\le m < 70$$", "演習2 の答え")
in_text("$$\\text{position} = \\frac{60}{2} = 30$$", "演習2 の位置")
# 3  待ち時間
BE3, FE3 = [0, 5, 10, 15, 20], [8, 20, 16, 6]
chk(sum(FE3) == 50, "演習3 の n は 50")
chk(cumf(FE3) == [8, 28, 44, 50], f"演習3 の累積度数: {cumf(FE3)}")
eq(interp(BE3, FE3, 25), F(37, 4), "演習3 の median は 9.25")
eq(F(37, 4), sp.Rational("9.25"), "37/4 = 9.25")
eq(25 - 8, 17, "階級の中では 17 番目")
eq(5 + F(17, 20) * 5, F(37, 4), "演習3 の補間")
chk(5 < F(37, 4) < 10, "9.25 は階級の中")
chk(F(17, 20) > F(1, 2), "17/20 は 1/2 より大きいので階級の上のほう")
in_text("$$\\text{median} = 5 + \\frac{17}{20} \\times 5 = 9.25 \\text{ minutes}$$",
        "演習3 の答え")
in_text("$5 < 9.25 < 10$", "演習3 の検算")
# 4  Q1 と Q3
BE4, FE4 = [0, 10, 20, 30, 40], [8, 24, 32, 16]
chk(sum(FE4) == 80, "演習4 の n は 80")
chk(cumf(FE4) == [8, 32, 64, 80], f"演習4 の累積度数: {cumf(FE4)}")
eq(F(80, 4), 20, "演習4 の Q1 の位置")
eq(F(3 * 80, 4), 60, "演習4 の Q3 の位置")
eq(interp(BE4, FE4, 20), 15, "演習4 の Q1")
eq(interp(BE4, FE4, 60), F(115, 4), "演習4 の Q3 は 28.75")
eq(F(115, 4), sp.Rational("28.75"), "115/4 = 28.75")
eq(F(115, 4) - 15, F(55, 4), "演習4 の IQR は 13.75")
eq(F(55, 4), sp.Rational("13.75"), "55/4 = 13.75")
eq(10 + F(12, 24) * 10, 15, "Q1 の補間")
eq(20 + F(28, 32) * 10, F(115, 4), "Q3 の補間")
eq(F(12, 24), F(1, 2), "12/24 = 1/2 なので階級のまん中")
chk(15 < F(115, 4), "Q1 < Q3")
in_text("$$\\mathrm{IQR} = 28.75 - 15 = 13.75$$", "演習4 の答え")
# 5  箱ひげ図の 5 つの数
DE5 = [12, 18, 20, 22, 25, 26, 27, 29, 30, 33, 48]
chk(len(DE5) == 11, "演習5 は 11 個")
chk(DE5 == sorted(DE5), "演習5 は小さい順")
_a5, _m5, _c5 = quartiles(DE5)
eq(_a5, 20, "演習5 の Q1")
eq(_m5, 26, "演習5 の median")
eq(_c5, 30, "演習5 の Q3")
eq(_c5 - _a5, 10, "演習5 の IQR")
_lo5, _hi5 = fences(_a5, _c5)
eq(_lo5, 5, "演習5 の下の境目")
eq(_hi5, 45, "演習5 の上の境目")
chk([v for v in DE5 if v < _lo5 or v > _hi5] == [48], "演習5 の外れ値は 48")
chk(max(v for v in DE5 if v <= _hi5) == 33, "ひげの先は 33")
chk(min(DE5) > _lo5, "最小値は境目の内側")
in_text("*five numbers:* $12, \\ 20, \\ 26, \\ 30, \\ 33$", "演習5 の 5 つの数")
in_text("$$Q_3 + 1.5 \\times 10 = 45, \\qquad 48 > 45$$", "演習5 の判定")
# 6  2 つの店
P6 = (2, 5, 8, 12, 20)
Q6 = (4, 7, 9, 11, 15)
eq(P6[3] - P6[1], 7, "P の IQR")
eq(Q6[3] - Q6[1], 4, "Q の IQR")
eq(P6[4] - P6[0], 18, "P の range")
eq(Q6[4] - Q6[0], 11, "Q の range")
chk(P6[2] < Q6[2], "median は P のほうが小さい")
chk(P6[3] - P6[1] > Q6[3] - Q6[1], "散らばりは P のほうが大きい")
chk(P6[4] > Q6[4], "最大値は P のほうが大きい")
in_text("$$\\mathrm{IQR}_P = 12 - 5 = 7, \\qquad \\mathrm{IQR}_Q = 11 - 7 = 4$$",
        "演習6 の IQR")
in_text("$20 - 2 = 18$、Q は $15 - 4 = 11$", "演習6 の range")
# 8  位置と値の取りちがえ
eq(F(3, 4) * 60, 45, "演習8 の位置は 45")
in_text("$\\dfrac{3}{4} \\times 60 = 45$", "演習8 の計算")
# 9  対称性
A9 = dict(mn=30, q1=44, md=47, q3=56, mx=70)
eq(A9["md"] - A9["q1"], 3, "演習9 の median - Q1")
eq(A9["q3"] - A9["md"], 9, "演習9 の Q3 - median")
eq(A9["q1"] - A9["mn"], 14, "演習9 の下のひげ")
eq(A9["mx"] - A9["q3"], 14, "演習9 の上のひげ")
chk(A9["q1"] - A9["mn"] == A9["mx"] - A9["q3"], "ひげは対称")
chk(A9["md"] - A9["q1"] != A9["q3"] - A9["md"], "箱は対称でない")
eq(A9["q3"] - A9["q1"], 12, "演習9 の IQR")
_lo9, _hi9 = fences(A9["q1"], A9["q3"])
eq(_lo9, 26, "演習9 の下の境目")
eq(_hi9, 74, "演習9 の上の境目")
chk(A9["mn"] > _lo9 and A9["mx"] < _hi9, "演習9 に外れ値はない")
in_text("$44 - 30 = 14$ と $70 - 56 = 14$", "演習9 のひげ")
in_text("$44 - 18 = 26$ と $56 + 18 = 74$", "演習9 の境目")
# 10  幅の違うヒストグラム
eq(F(20, 10), 2, "幅 20 は幅 10 の 2 倍")
chk(20 * 2 == 20 * 2, "同じ高さなら面積は 2 倍")

# ══════════════════════════════════════════════════════════
# 8. 例題・演習の答えが本文に漏れていないか
# ══════════════════════════════════════════════════════════
for _leak, _m in [
        ("$8, \\quad 20, \\quad 35", "例題1(a)"),
        ("1.5, \\quad 2, \\quad 3", "例題1(d)"),
        ("23.3", "例題2(c)"),
        ("28.75", "演習4"),
        ("9.25", "演習3"),
        ("$$5, \\quad 15, \\quad 30", "例題2(a)"),
        ("$$3, \\quad 12, \\quad 30", "例題4(b)"),
        ("60 \\le m < 70", "演習2"),
]:
    not_in_body(_leak, _m)

# ══════════════════════════════════════════════════════════
# 9. 公式集とシラバス
# ══════════════════════════════════════════════════════════
chk(TEXT.count("callout-important") == 1, "公式集の callout は 1 つ（IQR）")
in_text("$\\mathrm{IQR} = Q_3 - Q_1$ は、公式集の **4.2** の欄にあります。",
        "IQR は公式集の 4.2")
in_text("**range の式は公式集にありません。**", "range は公式集にない")
_quotes = [l for l in TEXT.splitlines() if l.startswith("> ")]
chk(len(_quotes) == 2, f"シラバスの引用は 2 行: {_quotes}")
chk(_quotes[0] == "> Not required: Frequency density histograms.",
    "引用 1: Not required")
chk(TEXT.index("シラバスは、SL のヒストグラムを") < TEXT.index(_quotes[0]),
    "Not required の前に、幅の話を日本語で書いている")
chk(_quotes[1] == "> Outliers should be indicated with a cross.",
    "引用 2: × で打つ")
not_in_text("Class intervals will be given as inequalities", "Guidance は貼らない")
not_in_text("Frequency histograms with equal class intervals", "Guidance は貼らない")
in_text("**階級の幅がすべて同じもの**に限っています", "幅は同じ")

# ══════════════════════════════════════════════════════════
# 10. 説明のしかた
# ══════════════════════════════════════════════════════════
in_text("**「正規分布である」と断定しないでください。**", "断定しない")
in_text("答案でも `may be` を使います。", "may be を使う")
in_text("ひげの先は、**外れ値でないもののうち、いちばん外側の値**です。", "ひげの先")

# ══════════════════════════════════════════════════════════
# 11. GDC
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h_ for h_ in _tips if not h_.startswith("解説")]
chk(len(_gdc) == 1, f"GDC の折りたたみは 1 つ: {_gdc}")
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "4.2 には GDC の節を置かない")
in_text("ctrl + doc → Add Data & Statistics", "Data & Statistics")
not_in_text("Plot Type", "確認していない操作は書かない")
not_in_text("電卓が自動で $\\times$ にします", "電卓が × にするとは書かない")
in_text("`MedianX`・`Q1X`・`Q3X`", "One-Variable Statistics の読み方")
in_text("**Paper 1 では使えません。**", "Paper 1 では使えない")
not_in_text("solve(", "CAS 前提の solve( は書いていない")

# ══════════════════════════════════════════════════════════
# 12. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 8,
    f"model-answer が 8: {TEXT.count('{.model-answer}')}")
_asks = len(re.findall(r"\[(?:[^\]]*?)(?:Explain|Justify|Comment|Interpret|Identify"
                       r"|Describe|Suggest)(?:[^\]]*?)\]\{\.q-en\}", TEXT))
chk(_asks == 8, f"説明を求める問いが 8: {_asks}")
chk(len(re.findall(r"^::: \{#exm-aasl42-", TEXT, re.M)) == 4, "例題が 4")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例が 14")
chk(TEXT.count("::: {.callout-warning}") == 7, "Common errors 6 + 本文の注意 1 で 7")
chk("**試験ではこう書む**" not in TEXT, "誤字「書む」がない")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Worked examples", "Common errors",
         "Exercises"]
chk([h_ for h_ in _h2 if h_ in _want] == _want, "5 つの見出しが所定の順")
chk([h_ for h_ in _h2 if h_ in _want][-1] == "Exercises", "Exercises で終わる")
_idea = [int(_v) for _v in re.findall(r"^### (\d+)\. ", TEXT, re.M)]
chk(_idea == list(range(1, 8)), f"The idea が 1..7 で連番: {_idea}")
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
    _b = _blk.replace("**試験ではこう書く**", "")
    chk(not re.search(r"[ぁ-んァ-ン一-龥]", _b), "model-answer に日本語")
    chk(len(_blk.split()) <= 115, f"model-answer が長すぎない: {len(_blk.split())} 語")
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a0 in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a0 in _anchors or _a0 in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aasl42", "他ページの @-ref: " + _r0)
for _f0 in set(re.findall(r"\]\((\.\./[a-z0-9-]+/)?([a-z0-9-]+\.qmd)(?:#[a-z0-9-]+)?", TEXT)):
    _path = os.path.join(BASE, _f0[0] + _f0[1]) if _f0[0] else \
        os.path.join(BASE, _f0[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f0[0] + _f0[1])
_T41 = open(os.path.join(BASE, "aasl-4-1.qmd"), encoding="utf-8").read()
for _a2 in set(re.findall(r"\]\(aasl-4-1\.qmd#([a-z0-9-]+)\)", TEXT)):
    chk(("{#" + _a2 + "}") in _T41, "4.1 側に見出しがない: #" + _a2)
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or ".qmd#" in _href
        or _href.startswith("http") or _href.startswith("../"),
        "まだないページへのリンク: " + _href)
chk(TEXT.count("@fig-aasl42-idea") >= 2, "図を本文から 2 か所以上参照している")
_head = TEXT[:TEXT.index("## The idea")]
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は What you should be able to do の 1 つだけ")
_open = len(re.findall(r"^::: \{", TEXT, re.M))
_close = len(re.findall(r"^:::$", TEXT, re.M))
chk(_open == _close, f"::: の開閉が合う: 開 {_open} / 閉 {_close}")

# ══════════════════════════════════════════════════════════
# 13. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-4-2-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-4-2-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) Reading a cumulative frequency graph", "図(a) の題")
in_fig("in on the vertical axis", "図(a) の入り方")
in_fig("out on the", "図(a) の出方")
in_fig("(b) A box and whisker diagram with an outlier", "図(b) の題")
in_fig("the whisker stops at the last value", "図(b) のひげ")
in_fig("$Q_3 + 1.5\\\\,IQR$", "図(b) の境目")
in_fig("the outlier is plotted as a cross and the whisker does ", "図(b) の説明")
# 図の × が本当に境目の外にあること
_m = re.search(r"MN, Q1, MD, Q3, LAST = ([0-9.]+), ([0-9.]+), ([0-9.]+), "
               r"([0-9.]+), ([0-9.]+)", FIGCODE)
chk(_m is not None, "図の 5 つの数が読める")
_v = [float(_m.group(i)) for i in range(1, 6)]
chk(_v[0] < _v[1] < _v[2] < _v[3] < _v[4], f"図の 5 つの数が小さい順: {_v}")
_ffence = _v[3] + 1.5 * (_v[3] - _v[1])
_mc = re.search(r"CROSS = ([0-9.]+)", FIGCODE)
chk(_mc is not None, "図の × の位置が読める")
chk(float(_mc.group(1)) > _ffence,
    f"図の × は境目より外: {_mc.group(1)} vs {_ffence}")
chk(_v[4] < _ffence, f"図のひげの先は境目より内: {_v[4]} vs {_ffence}")
# 図に例題・演習の数値が出ていないこと
for _bad in ["23.3", "28.75", "9.25", "45", "48", "33"]:
    chk(_bad not in FIGSTR, "図に答えの数値: " + _bad)
in_text("(a) A cumulative frequency graph is read by entering on the vertical axis",
        "キャプションが (a) を説明")
in_text("(b) A box and whisker diagram shows five numbers", "キャプションが (b) を説明")

# ══════════════════════════════════════════════════════════
# 14. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/04-statistics-and-probability/aasl-4-2.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-4-1.qmd") < DRAFT.index("aasl-4-2.qmd"), "並びが 4.1 → 4.2")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(04-statistics-and-probability/aasl-4-2.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| histogram |", "| cumulative frequency |",
           "| box and whisker diagram |", "| percentile |"]:
    chk(_t in GLO, "対訳表にある: " + _t)

# ══════════════════════════════════════════════════════════
# 15. 査読で直したところ（2026-09-08）
# ══════════════════════════════════════════════════════════

# --- 位置の出し方が 2 通りあることを書いていなかった --------------------
in_text("**値が $1$ つずつ分かっているときは別です。**", "2 通りあること")
in_text("$n$ が奇数なら median は $\\dfrac{n+1}{2}$ 番目、偶数なら $\\dfrac{n}{2}$ 番目と "
        "$\\dfrac{n}{2}+1$ 番目の平均です。", "数えるときの位置")
in_text("median で下半分と上半分に分け（$n$ が奇数なら median は除く）", "四分位数の分け方")
in_text("**どちらの表なのかを、先に見てください。**", "どちらの表か")
in_text("値が $1$ つずつ分かっている表なので、**小さい順に並べて数える**方法を使います",
        "例題1 が方法を明示")
in_text("## 位置の出し方を取りちがえる", "Common errors も両方向")
not_in_text("## グラフから読むのに $\\dfrac{n+1}{2}$ を使う", "片方向の見出しは消した")
# 2 つの方法が、例題1 で本当にちがう答えを出すこと（だから書く必要がある）
chk(sorted(D1)[int(40 / 2) - 1] == 1, "n/2 番目だと 1 になる")
chk(_m1 == F(3, 2), "数える方法だと 1.5")
chk(sorted(D1)[int(40 / 2) - 1] != _m1, "2 つの方法で答えがちがう（例題1）")
# 演習1 では、たまたま一致する
DE1s = sorted(DE1)
_med_count = quartiles(DE1)[1]
chk(DE1s[int(30 / 2) - 1] == 2 and _med_count == 2,
    f"演習1 ではたまたま一致する: {DE1s[14]} vs {_med_count}")

# --- Why it works が演習5 の答えを出していた ----------------------------
not_in_body("$48$", "演習5 の外れ値は本文に出さない")
not_in_text("ひげの先が $48$ になってしまえば", "48 の例は消した")
in_text("ひげの先が $90$ になってしまえば", "90 に差しかえた")
chk(TEXT.count("$90$") >= 1, "90 を使っている")

# --- histogram の目標に対応する問いを入れた -----------------------------
in_text("State one way in which a histogram differs from a bar chart.",
        "演習10 に棒グラフとのちがい")
in_text("*a histogram has a continuous quantity on the horizontal axis and the bars "
        "touch, while a bar chart shows separate categories with gaps between the bars*",
        "演習10(a) の答え")
in_text("**なぜ棒をくっつけるのか**を説明できる。", "目標の書きかえ")

# --- Why it works の累積度数の定義 --------------------------------------
in_text("階級にまとめた表では、累積度数が「**その階級の上の端より小さいものの個数**」",
        "階級にまとめた表での定義")
not_in_text("累積度数の意味が「**その値より小さいものの個数**」", "誤った定義は消した")
# 離散の表では「以下」であることを、数で確かめる
chk(len([v for v in D1 if v <= 1]) == 20, "x <= 1 が 20 個")
chk(len([v for v in D1 if v < 1]) == 8, "x < 1 は 8 個（20 ではない）")

# --- Not required の引用の使い方 ----------------------------------------
in_text("シラバスは、SL のヒストグラムを**階級の幅がすべて同じもの**に限っています。",
        "幅の話は日本語で")
not_in_text("シラバスは、階級の幅について次のように述べています。", "古い導入は消した")
not_in_text("Frequency histograms with equal class intervals", "Guidance は貼らない")

# --- GDC の記述 ---------------------------------------------------------
in_text("## Paper 2 では、$5$ つの数を電卓で出せます", "GDC の見出し")
in_text("**答案に写すときは、外れ値を自分で $\\times$ にし、ひげをその手前で止めてください。**",
        "答案では自分で × にする")

# --- 例題1(d) の検算 ----------------------------------------------------
in_text("**検算（(d) について）。** **ひげの先を境目と比べます。** $3 < 3.5$",
        "例題1(d) の検算")
not_in_text("$0 \\le 1 \\le 1.5 \\le 2 \\le 3$ ✓ 並んでいなければ", "並び順の検算は消した")
chk(3 < F(7, 2), "3 < 3.5")
chk(4 > F(7, 2), "4 > 3.5 なので 4 にするとひげがのびる")

# --- 演習4 の検算（割合） ------------------------------------------------
in_text("階級の手前までに $8$ 個、階級の中で $\\dfrac{12}{24}$ すなわち $12$ 個なので、"
        "合わせて $20$ 個", "個数で見る検算")
eq(8 + 12, 20, "8 + 12 = 20")
eq(8 + 20, 28, "8 + 20 = 28（誤った側）")
chk(8 + 20 != 20, "誤った側は 20 と合わない")
not_in_text("位置 $20$ が階級の $\\dfrac{12}{24} = \\dfrac{1}{2}$ のところにあることと"
            "合っています", "循環した検算は消した")

# --- 演習1 の検算 -------------------------------------------------------
in_text("**検算（位置）。** **累積度数がまたぐところを見ます。**", "演習1 の検算")
chk(cumf(FE1)[0] < 8 <= cumf(FE1)[1], "位置 8 は x=1 の階級")
chk(cumf(FE1)[2] < 23 <= cumf(FE1)[3], "位置 23 は x=3 の階級")
not_in_text("最大値 $5$ は $6$ より小さいので、外れ値はありません", "外れ値の検算は消した")

# --- 例題2(d) の model answer -------------------------------------------
in_text("The position of the median is $\\dfrac{40}{2} = 20$. Fifteen values lie below "
        "the class", "例題2(d) の model answer")
not_in_text("Here $15$ values lie below the class and $20$ values lie below the median",
            "個数と位置を取りちがえた文は消した")
in_text("中央値の位置は $\\dfrac{40}{2} = 20$ である。", "日本語の説明も直した")
# 実際に、中央値より下にあるのは 19 個ぶんで、20 個ではない
chk(cumf(F2)[1] == 15, "階級より下は 15 個")
chk(20 - 15 == 5, "階級の中では 5 番目")

# --- 演習5 の分け方 -----------------------------------------------------
in_text("$n = 11$ で奇数なので median は $6$ 番目の $26$ です。**median を除いて**",
        "演習5 は median を除く")
in_text("（[SL 4.1](aasl-4-1.qmd#outlier) の手順 $1$）", "4.1 の手順を参照")
# median を含める方法だと別の答えになることを確かめる
_incl_lo = DE5[:6]
_incl_hi = DE5[5:]
chk(med(_incl_lo) != 20 or med(_incl_hi) != 30,
    f"含める方法だと別の値: {med(_incl_lo)}, {med(_incl_hi)}")

# --- 例題2(b) の言い方 --------------------------------------------------
in_text("**(b)** 階級にまとめられた表なので、位置は", "グラフとは書かない")
not_in_text("**(b)** グラフから読むときの位置は", "古い言い方は消した")

# --- 第 6 節の 5 つの数 --------------------------------------------------
in_text("外れ値がないときは、次の $5$ つです。", "外れ値がないとき")
in_text("$5$ つの数のうち両はしの $2$ つが、最小値・最大値からこの値に変わります。",
        "外れ値があるときの 5 つ")

# --- 例題3 の検算 2 つ ---------------------------------------------------
in_text("**検算（(a) について）。** **箱の幅として見ます。**", "例題3(a) の検算")
in_text("$78 - 22$ を使ってしまうと、$\\mathrm{IQR}$ が range に化けます。",
        "誤った側との対比")
eq(78 - 22, 56, "78 - 22 = 56（range）")
chk(78 - 22 != 61 - 38, "range と IQR はちがう")
not_in_text("B は $Q_1$ も $Q_3$ も…", "言いかけの文は消した")
not_in_text("**箱の中に median があるか見ます。**", "順序だけの検算は消した")

# --- 補間の式の書き方 ---------------------------------------------------
in_text("その階級の手前までの累積度数を $c$、その階級の度数を $f$ とすると",
        "c と f で書く")
in_text("\\frac{k - c}{f} \\times (\\text{階級の幅})", "補間の式")
not_in_text("度数 $f$ の階級の中で「下から $j$ 番目」", "j での書き方は消した")
# k = 上端の累積度数 のときも、式が階級の上端を返す（例題2 の Q3）
eq(20 + F(30 - 15, 15) * 10, 30, "k = c + f なら階級の上端")


# ══════════════════════════════════════════════════════════
# C08  演習6 — P を選んでも、数を挙げれば正解
# ══════════════════════════════════════════════════════════
in_text("*(Shop P is also accepted, provided the figures are quoted:",
        "C08 P も正解")
in_text("**どちらの店を選んでも正解になります。**", "C08 どちらでもよい")
not_in_text("答えは Q になります", "C08 旧断定が消えている")
# P: 2,5,8,12,20 / Q: 4,7,9,11,15
_p5 = [2, 5, 8, 12, 20]
_q5 = [4, 7, 9, 11, 15]
chk(_p5[3] - _p5[1] == 7 and _q5[3] - _q5[1] == 4, "C08 IQR は 7 と 4")
chk(_p5[2] < _q5[2], "C08 median は P のほうが小さい")
chk(_p5[1] < _q5[1], "C08 Q1 は P のほうが小さい")
chk(_p5[4] > _q5[4], "C08 最大値は P のほうが大きい")
chk(_p5[3] - _p5[1] > _q5[3] - _q5[1], "C08 散らばりは Q のほうが小さい")


# ══════════════════════════════════════════════════════════
# E07  演習2・3・5 — 図を実際にかかせる
# ══════════════════════════════════════════════════════════
in_text("[Draw a histogram for these data, labelling both axes.]",
        "E07 演習2 はヒストグラム")
in_text("(img/aasl-4-2-ex2.svg){#fig-aasl42-ex2 width=100%}",
        "E07 演習2 の解答図")
in_text("[Draw a cumulative frequency graph for these data.]",
        "E07 演習3 は累積度数グラフ")
in_text("(img/aasl-4-2-ex3.svg){#fig-aasl42-ex3 width=100%}",
        "E07 演習3 の解答図")
in_text("**最初の点は $(0, 0)$ です。**", "E07 累積度数は 0 から始める")
in_text("**この読み取りは、階級の中で値が均等に分布しているとみなして"
        "います。**", "E07 均等分布の仮定")
in_text("[Draw the box and whisker diagram on a scale from $10$ to $50$.]",
        "E07 演習5 は箱ひげ図")
in_text("(img/aasl-4-2-ex5.svg){#fig-aasl42-ex5 width=100%}",
        "E07 演習5 の解答図")
in_text("**ひげの先と外れ値を、はっきり分けてかきます。**",
        "E07 ひげと外れ値の区別")
# 演習2 のヒストグラム
_e07f = [6, 14, 22, 12, 6]
chk(sum(_e07f) == 60, "E07 度数の合計は 60")
chk(_e07f.index(max(_e07f)) == 2, "E07 いちばん高い棒は 60 <= m < 70")
# 演習3 の累積度数
_e07c = [8, 20, 16, 6]
_e07cum = [0]
for _v in _e07c:
    _e07cum.append(_e07cum[-1] + _v)
chk(_e07cum == [0, 8, 28, 44, 50], "E07 累積度数は 0, 8, 28, 44, 50")
chk(sp.Rational(50, 2) == 25, "E07 median の位置は 25")
chk(5 + sp.Rational(25 - 8, 20) * 5 == sp.Rational(37, 4), "E07 median 9.25")
chk(5 < sp.Rational(37, 4) < 10, "E07 median は階級の中")
# 演習5 の箱ひげ図
_e07d = [12, 18, 20, 22, 25, 26, 27, 29, 30, 33, 48]
chk(len(_e07d) == 11 and _e07d[5] == 26, "E07 median は 26")
chk(_e07d[2] == 20 and _e07d[8] == 30, "E07 Q1 = 20, Q3 = 30")
chk(30 + sp.Rational(3, 2) * 10 == 45, "E07 上の境目は 45")
chk(20 - sp.Rational(3, 2) * 10 == 5, "E07 下の境目は 5")
chk(48 > 45 and 33 < 45, "E07 48 だけが外れ値")
chk(min(_e07d) == 12 and 12 > 5, "E07 下側に外れ値はない")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
