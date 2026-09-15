"""AA SL 4.3（代表値と散らばり）の内容を検算する。

    python3 figs/aa-sl/check_aasl_4_3.py
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
QMD = os.path.join(BASE, "aasl-4-3.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_4_3.py"), encoding="utf-8").read()
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


def mean_ft(x, f):
    n = sum(f)
    return F(sum(F(a) * b for a, b in zip(x, f)), n)


def mids(edges):
    return [F(edges[i] + edges[i + 1], 2) for i in range(len(edges) - 1)]


def sd(d):
    m = F(sum(F(v) for v in d), len(d))
    return sp.sqrt(sum((F(v) - m) ** 2 for v in d) / len(d))


chk(mean_ft([1, 2], [1, 1]) == F(3, 2), "道具: 度数つきの平均")
chk(mids([0, 10, 20]) == [5, 15], "道具: 階級値")
chk(sd([1, 1, 1]) == 0, "道具: 全部同じなら sd = 0")

# ══════════════════════════════════════════════════════════
# 1. The idea
# ══════════════════════════════════════════════════════════
in_text("{#eq-aasl43-mean}", "平均の式のラベル")
in_text("{#eq-aasl43-mid}", "階級値の式のラベル")
in_text("{#eq-aasl43-var}", "分散の式のラベル")
in_text("{#tbl-aasl43-which}", "代表値の選び方の表")
in_text("{#tbl-aasl43-change}", "定数の表")
chk(TEXT.count("@eq-aasl43-mean") >= 2, "平均の式を参照している")
chk(TEXT.count("@eq-aasl43-mid") >= 2, "階級値の式を参照している")
chk(TEXT.count("@eq-aasl43-var") >= 2, "分散の式を参照している")
chk(TEXT.count("@tbl-aasl43-change") >= 2, "定数の表を参照している")
in_text("\\bar{x} = \\frac{\\sum_{i=1}^{k} f_i x_i}{n}", "公式集の形")
in_text("n = \\sum_{i=1}^{k} f_i", "n の定義")
in_text("\\text{mid-interval value} = \\frac{(\\text{下端}) + (\\text{上端})}{2}",
        "階級値の式")
in_text("\\text{variance} = \\sigma^{2}", "分散の式")
# 階級値の例
eq(F(50 + 70, 2), 60, "50-70 の階級値は 60")
in_text("$\\dfrac{50 + 70}{2} = 60$", "本文の階級値の例")
# 下端を使うと 10 ずつ小さい
eq(60 - 50, 10, "階級値と下端の差は 10")
# 定数の表
_a, _c, _mu, _sg = sp.symbols("a c mu sigma", real=True)
in_text("| すべてに $c$ を足す | $\\bar{x} + c$ | 変わらない |", "足す行")
in_text("| すべてに $a$ をかける | $a\\bar{x}$ | $\\lvert a \\rvert \\sigma$ |",
        "かける行")
in_text("| $ax + c$ にする | $a\\bar{x} + c$ | $\\lvert a \\rvert \\sigma$ |",
        "ax+c の行")
# 実データで確かめる
_D = [1, 3, 5, 11]
_m0 = F(sum(_D), len(_D))
_s0 = sd(_D)
for _cc in (6, -4):
    chk(F(sum(v + _cc for v in _D), len(_D)) == _m0 + _cc, f"足すと平均は +{_cc}")
    chk(sp.simplify(sd([v + _cc for v in _D]) - _s0) == 0, f"足しても sd は同じ ({_cc})")
for _aa in (3, -2, F(1, 2)):
    chk(F(sum(F(v) * _aa for v in _D), len(_D)) == _aa * _m0, f"かけると平均は {_aa} 倍")
    chk(sp.simplify(sd([F(v) * _aa for v in _D]) - abs(_aa) * _s0) == 0,
        f"sd は |a| 倍 ({_aa})")
# sigma >= 0、sigma = 0 は全部等しいとき
chk(sd([7, 7, 7, 7]) == 0, "全部 7 でも sd = 0")
chk(sd([0, 0, 0]) == 0, "全部 0 でも sd = 0")
chk(sd([1, 2]) > 0, "ちがえば sd > 0")
in_text("**$\\sigma = 0$ になるのは、すべての値が等しいとき**だけです。", "sd = 0 の意味")
in_text("**$0$ 以上**です。負にはなりません。", "sd は 0 以上")
in_text("**$\\sigma$ の式は公式集にありません。**", "sd の式は公式集にない")

# ══════════════════════════════════════════════════════════
# 2. Why it works
# ══════════════════════════════════════════════════════════
_x, _xb = sp.symbols("x xbar", real=True)
eq((_x + _c) - (_xb + _c), _x - _xb, "足しても偏差は同じ")
eq(_a * _x - _a * _xb, _a * (_x - _xb), "かけると偏差は a 倍")
in_text("(x_i + c) - (\\bar{x} + c) = x_i - \\bar{x}", "偏差が変わらない式")
in_text("a x_i - a\\bar{x} = a(x_i - \\bar{x})", "偏差が a 倍になる式")
in_text("**$a$ が負のときも散らばりは正**なので、絶対値が付きます。", "絶対値の理由")
in_text("**どちらにも寄せない**のが公平です。", "まん中を使う理由")
in_text("median は順番しか見ません。", "median は順番だけ")
# median は最大値を変えても動かない
_E = [1, 2, 3, 4, 5]
chk(med(_E) == med([1, 2, 3, 4, 50]), "最大値を変えても median は同じ")
chk(F(sum(_E), 5) != F(sum([1, 2, 3, 4, 50]), 5), "mean は変わる")

# ══════════════════════════════════════════════════════════
# 3. 例題 1  図書館
# ══════════════════════════════════════════════════════════
X1, F1 = [0, 1, 2, 3, 4], [4, 8, 10, 6, 2]
chk(sum(F1) == 30, "例題1 の n は 30")
eq(sum(a * b for a, b in zip(X1, F1)), 54, "例題1 の Σfx")
eq(mean_ft(X1, F1), F(9, 5), "例題1 の mean は 1.8")
eq(F(54, 30), sp.Rational("1.8"), "54/30 = 1.8")
chk([sum(F1[:i + 1]) for i in range(5)] == [4, 12, 22, 28, 30], "例題1 の累積度数")
D1 = expand(X1, F1)
_q1, _m1, _q3 = quartiles(D1)
eq(_m1, 2, "例題1 の median")
eq(_q1, 1, "例題1 の Q1")
eq(_q3, 3, "例題1 の Q3")
eq(_q3 - _q1, 2, "例題1 の IQR")
chk(X1[F1.index(max(F1))] == 2, "例題1 の mode は 2")
chk(sorted(D1)[14] == 2 and sorted(D1)[15] == 2, "15 番目と 16 番目はどちらも 2")
chk(sorted(D1)[7] == 1, "8 番目は 1")
chk(sorted(D1)[22] == 3, "23 番目は 3")
chk(0 <= float(mean_ft(X1, F1)) <= 4, "mean はデータの範囲の中")
# x をそのまま足した誤りの側
eq(F(0 + 1 + 2 + 3 + 4, 5), 2, "x を平均すると 2")
chk(F(0 + 1 + 2 + 3 + 4, 5) != mean_ft(X1, F1), "正しい mean とちがう")
in_text("$0+1+2+3+4 = 10$ を $5$ で割ると $2$ です。正しい $1.8$ とちがいます",
        "誤りの側との対比")
in_text("\\bar{x} = \\frac{54}{30} = 1.8", "例題1(a) の答え")

# ══════════════════════════════════════════════════════════
# 4. 例題 2  グループ化された通勤時間
# ══════════════════════════════════════════════════════════
E2 = [0, 10, 20, 30, 40, 50]
F2 = [4, 10, 14, 8, 4]
M2 = mids(E2)
chk(M2 == [5, 15, 25, 35, 45], f"例題2 の階級値: {M2}")
chk(sum(F2) == 40, "例題2 の n は 40")
eq(sum(a * b for a, b in zip(M2, F2)), 980, "例題2 の Σfx")
eq(mean_ft(M2, F2), F(49, 2), "例題2 の mean は 24.5")
eq(F(980, 40), sp.Rational("24.5"), "980/40 = 24.5")
chk(max(F2) == 14 and F2.index(14) == 2, "modal class は 3 番目の階級")
# 下端を使った誤りの側
_low = [0, 10, 20, 30, 40]
eq(sum(a * b for a, b in zip(_low, F2)), 780, "下端だと Σfx = 780")
eq(mean_ft(_low, F2), F(39, 2), "下端だと mean は 19.5")
eq(F(49, 2) - F(39, 2), 5, "差はちょうど 5")
in_text("$\\sum f x = 0 + 100 + 280 + 240 + 160 = 780$ で、mean は $19.5$ です",
        "下端の誤りの側")
not_in_body("$\\dfrac{20 + 30}{2} = 25$", "例題2(a) の答えは本文に出さない")
not_in_body("$20 \\le t < 30$", "例題2(c) の答えは本文に出さない")
# 階級値をただ平均した誤りの側
eq(F(sum(M2), 5), 25, "階級値の平均は 25")
chk(F(sum(M2), 5) != mean_ft(M2, F2), "度数を使うとちがう")
in_text("$\\dfrac{5+15+25+35+45}{5} = 25$", "階級値の単純平均")
in_text("\\bar{x} = \\frac{980}{40} = 24.5 \\ \\text{minutes}", "例題2(b) の答え")

# ══════════════════════════════════════════════════════════
# 5. 例題 3  定数を足す・かける
# ══════════════════════════════════════════════════════════
MU3, SD3 = 50, 8
eq(MU3 + 6, 56, "例題3(a) の mean")
eq(3 * MU3, 150, "例題3(b) の mean")
eq(3 * SD3, 24, "例題3(b) の sd")
eq(2 * MU3 - 5, 95, "例題3(c) の mean")
eq(2 * SD3, 16, "例題3(c) の sd")
# 2(x-5) との対比
eq(2 * (MU3 - 5), 90, "2(x-5) なら mean は 90")
chk(2 * (MU3 - 5) != 2 * MU3 - 5, "順番で mean が変わる")
in_text("$2(x - 5) = 2x - 10$ なので、mean は $2(50) - 10 = 90$", "順番の検算")
# 小さなデータでの検算
_S = [1, 3, 5]
chk(F(sum(_S), 3) == 3, "1,3,5 の mean は 3")
chk([v - 3 for v in _S] == [-2, 0, 2], "ずれは -2,0,2")
chk([v + 6 for v in _S] == [7, 9, 11], "6 を足すと 7,9,11")
chk(F(sum(v + 6 for v in _S), 3) == 9, "その mean は 9")
chk([(v + 6) - 9 for v in _S] == [-2, 0, 2], "ずれは同じ")
chk([v * 3 for v in _S] == [3, 9, 15], "3 倍すると 3,9,15")
chk(F(sum(v * 3 for v in _S), 3) == 9, "その mean は 9")
chk([(v * 3) - 9 for v in _S] == [-6, 0, 6], "ずれは 3 倍")
in_text("$1, 3, 5$ の mean は $3$、ずれは $-2, 0, 2$ です。", "小さなデータの検算")

# ══════════════════════════════════════════════════════════
# 6. 例題 4  分散
# ══════════════════════════════════════════════════════════
eq(sp.Rational("1.5") ** 2, sp.Rational("2.25"), "A の分散")
eq(4 ** 2, 16, "B の分散")
eq(sp.sqrt(sp.Rational("6.25")), sp.Rational("2.5"), "C の標準偏差")
chk(sp.Rational("1.5") < sp.Rational("2.5") < 4, "1.5 < 2.5 < 4")
chk(sp.Rational("2.25") < sp.Rational("6.25") < 16, "分散も同じ順")
eq(sp.Rational("2.5") ** 2, sp.Rational("6.25"), "2.5 を 2 乗すると 6.25")
in_text("\\sigma = \\sqrt{6.25} = 2.5 \\ \\text{g}", "例題4(c) の答え")
in_text("$1.5 < 2.5 < 4$", "例題4 の大きさの検算")

# ══════════════════════════════════════════════════════════
# 7. 演習 1〜10
# ══════════════════════════════════════════════════════════
# 1
XE1, FE1 = [1, 2, 3, 4, 5], [3, 7, 9, 4, 2]
chk(sum(FE1) == 25, "演習1 の n は 25")
eq(sum(a * b for a, b in zip(XE1, FE1)), 70, "演習1 の Σfx")
eq(mean_ft(XE1, FE1), F(14, 5), "演習1 の mean は 2.8")
eq(F(70, 25), sp.Rational("2.8"), "70/25 = 2.8")
chk([sum(FE1[:i + 1]) for i in range(5)] == [3, 10, 19, 23, 25], "演習1 の累積度数")
DE1 = expand(XE1, FE1)
chk(quartiles(DE1)[1] == 3, "演習1 の median は 3")
chk(sorted(DE1)[12] == 3, "13 番目は 3")
chk(XE1[FE1.index(max(FE1))] == 3, "演習1 の mode は 3")
chk(mean_ft(XE1, FE1) < 3, "mean は median より小さい")
in_text("$$\\sum f x = 3 + 14 + 27 + 16 + 10 = 70, \\qquad n = 25$$", "演習1 の Σfx")
in_text("$3+7+9+4+2 = 25$", "演習1 の検算")
# 2
EE2 = [0, 10, 20, 30, 40]
FE2 = [6, 12, 14, 8]
ME2 = mids(EE2)
chk(ME2 == [5, 15, 25, 35], f"演習2 の階級値: {ME2}")
chk(sum(FE2) == 40, "演習2 の n は 40")
eq(sum(a * b for a, b in zip(ME2, FE2)), 840, "演習2 の Σfx")
eq(mean_ft(ME2, FE2), 21, "演習2 の mean は 21")
eq(F(sum(ME2), 4), 20, "階級値の単純平均は 20")
chk(mean_ft(ME2, FE2) > F(sum(ME2), 4), "度数を使うと右に寄る")
in_text("$$\\sum f x = 30 + 180 + 350 + 280 = 840, \\qquad n = 40$$", "演習2 の Σfx")
in_text("$\\dfrac{5+15+25+35}{4} = 20$", "演習2 の検算")
# 3
EE3 = [0, 20, 40, 60, 80]
FE3 = [5, 15, 20, 10]
ME3 = mids(EE3)
chk(ME3 == [10, 30, 50, 70], f"演習3 の階級値: {ME3}")
chk(sum(FE3) == 50, "演習3 の n は 50")
eq(sum(a * b for a, b in zip(ME3, FE3)), 2200, "演習3 の Σfx")
eq(mean_ft(ME3, FE3), 44, "演習3 の mean は 44")
chk(max(FE3) == 20 and FE3.index(20) == 2, "modal class は 40-60")
chk(40 <= 44 < 60, "mean は modal class の中")
chk(len(set(EE3[i + 1] - EE3[i] for i in range(4))) == 1, "階級の幅はすべて同じ")
in_text("$$\\text{modal class}: \\ 40 \\le L < 60$$", "演習3 の modal class")
in_text("$$\\sum f x = 50 + 450 + 1000 + 700 = 2200, \\qquad n = 50$$", "演習3 の Σfx")
# 4
MU4, SD4 = 12, 3
eq(MU4 + 5, 17, "演習4(i) の mean")
eq(4 * MU4, 48, "演習4(ii) の mean")
eq(4 * SD4, 12, "演習4(ii) の sd")
eq(sp.Rational("0.5") * MU4 - 3, 3, "演習4(iii) の mean")
eq(sp.Rational("0.5") * SD4, sp.Rational("1.5"), "演習4(iii) の sd")
eq(sp.Rational("0.5") * (MU4 - 3), sp.Rational("4.5"), "0.5(x-3) なら 4.5")
chk(sp.Rational("0.5") * (MU4 - 3) != sp.Rational("0.5") * MU4 - 3, "順番で変わる")
chk(sp.Rational("1.5") < SD4, "0.5 倍で sd は小さくなる")
in_text("$0.5(x - 3)$ なら mean は $0.5(12-3) = 4.5$", "演習4 の順番の検算")
# 5
eq(sp.sqrt(sp.Rational("20.25")), sp.Rational("4.5"), "演習5 の sd")
eq(sp.Rational("0.6") ** 2, sp.Rational("0.36"), "演習5 の variance")
chk(sp.Rational("0.36") < sp.Rational("0.6"), "1 より小さいと 2 乗で小さくなる")
eq(sp.Rational("4.5") ** 2, sp.Rational("20.25"), "4.5 を 2 乗すると 20.25")
in_text("$0.6 < 1$ なので、$2$ 乗すると**小さく**なります。", "1 より小さいとき")
# 6
DE6 = [32, 34, 35, 36, 38, 40, 420]
chk(len(DE6) == 7, "演習6 は 7 個")
eq(sum(DE6), 635, "演習6 の合計")
_m6 = F(635, 7)
chk(abs(float(_m6) - 90.7) < 0.05, f"演習6 の mean は約 90.7: {float(_m6)}")
chk(quartiles(DE6)[1] == 36, "演習6 の median は 36")
chk(len([v for v in DE6 if v < _m6]) == 6, "mean より小さい値が 6 個")
chk(len([v for v in DE6 if v > _m6]) == 1, "mean より大きい値が 1 個")
_a6, _m6b, _c6 = quartiles(DE6)
eq(_a6, 34, "演習6 の Q1")
eq(_c6, 40, "演習6 の Q3")
eq(_c6 - _a6, 6, "演習6 の IQR")
eq(_c6 + F(3, 2) * 6, 49, "演習6 の上の境目は 49")
chk(420 > 49, "420 は外れ値")
in_text("$\\bar{x} = \\frac{635}{7} \\approx 90.7", "演習6 の mean")
in_text("$Q_1 = 34$、$Q_3 = 40$、$\\mathrm{IQR} = 6$ で、上の境目は $40 + 9 = 49$",
        "演習6 の外れ値の検算")
# 7  極端な例
eq(25 * 3, 75, "階級値では 75")
eq(21 * 3, 63, "本当は 63")
chk(75 != 63, "ずれが出る")
in_text("$25 \\times 3 = 75$ ですが、本当は $63$ です", "演習7 の極端な例")
# 8  度数が同じなら一致する
_eqf = [4, 4, 4, 4, 4]
_mm = [5, 15, 25, 35, 45]
chk(mean_ft(_mm, _eqf) == F(sum(_mm), 5), "度数が同じなら 2 つの答えは一致")
chk(mean_ft(M2, F2) != F(sum(M2), 5), "度数がちがえば一致しない")
# 9  反例
chk(sd([7, 7, 7, 7]) == 0 and 7 != 0, "7,7,7,7 は sd = 0 だが値は 0 でない")
in_text("$7, 7, 7, 7$ は mean が $7$、ずれはすべて $0$ なので $\\sigma = 0$ です",
        "演習9 の反例")
# 10
chk(15 / 4 > 3, "15 は 4 の 3 倍より大きい")
chk(abs(15 / 4 - 4) < 0.3, "およそ 4 倍")
in_text("Class A の $\\sigma$ は $4$、Class B は $15$ で、およそ $4$ 倍です",
        "演習10 の検算")

# ══════════════════════════════════════════════════════════
# 8. 例題・演習の答えが本文に漏れていないか
# ══════════════════════════════════════════════════════════
for _leak, _m in [
        ("1.8", "例題1(a)"),
        ("24.5", "例題2(b)"),
        ("980", "例題2(b)"),
        ("= 56", "例題3(a)"),
        ("2.25", "例題4(a)"),
        ("90.7", "演習6"),
        ("2.8", "演習1"),
        ("2200", "演習3"),
]:
    not_in_body(_leak, _m)

# ══════════════════════════════════════════════════════════
# 9. 公式集とシラバス
# ══════════════════════════════════════════════════════════
chk(TEXT.count("callout-important") == 1, "公式集の callout は 1 つ（平均）")
in_text("公式集の **4.3** の欄にあります", "平均は公式集の 4.3")
in_text("**$n$ が「度数の合計」であることが大事です。**", "n の意味")
_quotes = [l for l in TEXT.splitlines() if l.startswith("> ")]
chk(len(_quotes) == 1, f"シラバスの引用は 1 行: {_quotes}")
chk(_quotes[0] == "> Students should use mid-interval values to estimate the mean "
    "of grouped data.", "引用は階級値の指定")
not_in_text("Calculation of standard deviation and variance of the sample using only",
            "Guidance は逐語で貼らない")
not_in_text("Variance is the square of the standard deviation", "Guidance は貼らない")
not_in_text("`using only technology`", "Guidance の逐語は貼らない")
in_text("標準偏差と分散は電卓で求めるものと決めています", "technology の指定")

# ══════════════════════════════════════════════════════════
# 10. 説明のしかた
# ══════════════════════════════════════════════════════════
in_text("**理由をつけて選びます。**", "理由をつける")
in_text("**答えるのは階級です。** 度数ではありません。", "modal class は階級")
in_text("「$50 \\le v < 70$」のように階級を書きます", "階級で答える例")
in_text("**階級の幅がすべて同じときだけ**使えます。", "幅が同じときだけ")
in_text("**四分位数の求め方は、$1$ つではありません。**", "四分位数の方法")

# ══════════════════════════════════════════════════════════
# 11. GDC
# ══════════════════════════════════════════════════════════
chk("## Using your GDC (TI-Nspire CX II)" in TEXT, "GDC の節がある")
_gdc = TEXT[TEXT.index("## Using your GDC"):TEXT.index("## Exercises")]
chk("**この節は Paper 2 のためのものです。**" in _gdc, "節の冒頭に Paper 2")
_gnum = [int(v) for v in re.findall(r"^### (\d+)\. ", _gdc, re.M)]
chk(_gnum == list(range(1, len(_gnum) + 1)) and len(_gnum) == 3,
    f"GDC の ### が 1..3 の連番: {_gnum}")
for _op in ["ctrl + doc → Add Lists & Spreadsheet",
            "menu → Statistics → Stat Calculations → One-Variable Statistics",
            "`Frequency List` に度数の列を指定します"]:
    chk(_op in _gdc, "確認ずみの操作: " + _op)
for _bad in ["Num of Lists", "X1 List", "グレーの行", "Plot Type", "`OK` です"]:
    chk(_bad not in _gdc, "確認していない操作は書かない: " + _bad)
for _row in ["| $\\sigma_x$ | population standard deviation | **これを書く** |",
             "| $s_x$ | sample standard deviation | ふつう使わない |",
             "| MedianX | median | 使う |",
             "| Q1X / Q3X | $Q_1$ / $Q_3$ | 使う |"]:
    chk(_row in _gdc, "結果の読み方: " + _row[:24])
chk("**variance の欄はありません。**" in _gdc, "variance の欄はない")
chk("**$n$ を見る習慣**" in _gdc, "n を見る習慣")
not_in_text("solve(", "CAS 前提の solve( は書いていない")
not_in_text("Plot Type", "確認していない操作は書かない")
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_tip = [h_ for h_ in _tips if not h_.startswith("解説")]
chk(len(_tip) == 1, f"本文中の GDC の折りたたみは 1 つ: {_tip}")
for _h in _tip:
    chk(_h.startswith("Paper 2 では"), "折りたたみの見出しが Paper 2 で始まる: " + _h)

# ══════════════════════════════════════════════════════════
# 12. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 9,
    f"model-answer が 9: {TEXT.count('{.model-answer}')}")
_asks = len(re.findall(r"\[(?:[^\]]*?)(?:Explain|Justify|Comment|Interpret|Identify"
                       r"|Describe|Suggest)(?:[^\]]*?)\]\{\.q-en\}", TEXT))
chk(_asks == 9, f"説明を求める問いが 9: {_asks}")
chk(len(re.findall(r"^::: \{#exm-aasl43-", TEXT, re.M)) == 4, "例題が 4")
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
    chk(_r0 == "aasl43", "他ページの @-ref: " + _r0)
_T41 = open(os.path.join(BASE, "aasl-4-1.qmd"), encoding="utf-8").read()
for _a2 in set(re.findall(r"\]\(aasl-4-1\.qmd#([a-z0-9-]+)\)", TEXT)):
    chk(("{#" + _a2 + "}") in _T41, "4.1 側に見出しがない: #" + _a2)
# 4.1 と 4.2 からこのページへのリンク先が、ここにあること
for _src in ("aasl-4-1.qmd", "aasl-4-2.qmd"):
    _TS = open(os.path.join(BASE, _src), encoding="utf-8").read()
    for _a3 in set(re.findall(r"\]\(aasl-4-3\.qmd#([a-z0-9-]+)\)", _TS)):
        chk(("{#" + _a3 + "}") in TEXT, _src + " が指す見出しがない: #" + _a3)
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or ".qmd#" in _href
        or _href.startswith("http") or _href.startswith("../"),
        "まだないページへのリンク: " + _href)
chk(TEXT.count("@fig-aasl43-idea") >= 2, "図を本文から 2 か所以上参照している")
_head = TEXT[:TEXT.index("## The idea")]
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は What you should be able to do の 1 つだけ")
_open = len(re.findall(r"^::: \{", TEXT, re.M))
_close = len(re.findall(r"^:::$", TEXT, re.M))
chk(_open == _close, f"::: の開閉が合う: 開 {_open} / 閉 {_close}")

# ══════════════════════════════════════════════════════════
# 13. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-4-3-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-4-3-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) The mid-interval value stands for the whole class", "図(a) の題")
in_fig("the actual values in a class are not known", "図(a) の説明 1")
in_fig("each one is replaced by the middle of its class", "図(a) の説明 2")
in_fig("so the mean found from a grouped table is an estimate", "図(a) の結論")
in_fig("(b) Adding and multiplying by a constant", "図(b) の題")
in_fig("the gaps are unchanged, so $\\\\sigma$ is unchanged", "図(b) の足す")
in_fig("the gaps are scaled, so $\\\\sigma$ is multiplied by $|a|$", "図(b) のかける")
in_fig("the mean moves both times; the spread moves only when ", "図(b) の結論")
# 図の (b) が、本当に足しても間隔が変わらないように描かれていること
chk("BASE + 3.2" in FIGCODE, "足す行は BASE + 定数")
chk("BASE * 2.2" in FIGCODE, "かける行は BASE × 定数")
in_text("(a) When data are grouped, every value in a class is replaced by the "
        "mid-interval value", "キャプションが (a) を説明")
in_text("(b) Adding a constant slides every value along without changing the gaps",
        "キャプションが (b) を説明")

# ══════════════════════════════════════════════════════════
# 14. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/04-statistics-and-probability/aasl-4-3.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-4-2.qmd") < DRAFT.index("aasl-4-3.qmd"), "並びが 4.2 → 4.3")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(04-statistics-and-probability/aasl-4-3.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| mean |", "| median |", "| mode |", "| standard deviation |",
           "| variance |", "| mid-interval value |", "| modal class |"]:
    chk(_t in GLO, "対訳表にある: " + _t)

# ══════════════════════════════════════════════════════════
# 15. 査読で直したところ（2026-09-08）
# ══════════════════════════════════════════════════════════

# --- 1 つの値が mean を動かす量が誤っていた ----------------------------
in_text("$1$ つの値が $d$ だけ大きくなると、mean は $\\dfrac{d}{n}$ だけ動きます。",
        "d/n だけ動く")
not_in_text("$n$ で割っても、$\\dfrac{(\\text{その値})}{n}$ だけ mean が動きます",
            "誤った言い方は消した")
# 演習6 で反例になっていたことを、数で確かめる
_rest = [32, 34, 35, 36, 38, 40]
_m_rest = F(sum(_rest), 6)
_m_all = F(sum(_rest) + 420, 7)
chk(abs(float(_m_all - _m_rest) - 54.88) < 0.02,
    f"420 を足すと mean は約 54.9 動く: {float(_m_all - _m_rest)}")
chk(abs(float(_m_all - _m_rest) - 420 / 7) > 1,
    "420/7 = 60 ではない（古い主張は偽）")

# --- The idea が例題2 の答えを出していた -------------------------------
in_text("$50 \\le v < 70$ なら $\\dfrac{50 + 70}{2} = 60$ です。", "§4 の階級値の例")
in_text("$50 \\le v < 70$ に $50$ を使うと、その階級の値をすべて $10$ ずつ",
        "callout の例も差しかえた")
not_in_text("$20 \\le t < 30$ なら $\\dfrac{20 + 30}{2} = 25$ です。", "古い例は消した")
not_in_body("$20 \\le t < 30$", "例題2(c) の答えは本文に出さない")
eq(F(50 + 70, 2), 60, "50-70 の階級値は 60")
eq(60 - 50, 10, "下端との差は 10")
# 差しかえた階級が、例題・演習のどこにも出てこないこと
chk(TEXT.count("50 \\le v < 70") >= 2 and "50 \\le v < 70" not in
    TEXT[TEXT.index("## Worked examples"):], "50<=v<70 は本文だけに出る")

# --- Why it works が σ を「ずれの平均」と書いていた ---------------------
in_text("$\\sigma$ はずれの大きさから作られる数なので、どのずれも "
        "$\\lvert a \\rvert$ 倍になれば、$\\sigma$ も $\\lvert a \\rvert$ 倍になります。",
        "σ の言い方")
not_in_text("$\\sigma$ はずれの大きさを平均したものなので", "誤った定義は消した")
# 平均絶対偏差と標準偏差はちがう（だから「平均」と書けない）
_dd = [1, 3, 5, 11]
_mm = F(sum(_dd), 4)
_mad = F(sum(abs(F(v) - _mm) for v in _dd), 4)
chk(sp.simplify(_mad - sd(_dd)) != 0, f"平均絶対偏差 {_mad} と σ はちがう")

# --- 幅がちがうときの理由が断定になっていた ----------------------------
in_text("幅の広い階級ほど度数が大きくなりやすいので", "なりやすい、と書く")
not_in_text("幅の広い階級ほど度数が大きくなるので、比べられません", "断定は消した")

# --- 四分位数の方法についての言い方 ------------------------------------
in_text("**どちらの方法を使ったかが分かるように書きます。**", "方法を書く")
not_in_text("**どちらでも答えになります。**", "古い言い方は消した")

# --- σx と sx を、折りたたみの外にも書いた ------------------------------
in_text("**電卓は標準偏差を $2$ つ出します。** $\\sigma_x$（population standard "
        "deviation）と $s_x$（sample standard deviation）です。", "§6 の本文に σx と sx")
in_text("**どちらの欄を読むかを決めておく**ようにしてください。", "欄で決める")
not_in_text("$s_x$ は少し大きな値になるので、取りちがえるとすぐ分かります。",
            "「すぐ分かる」は消した")
# s/σ = sqrt(n/(n-1)) は n = 40 でほとんど 1
chk(abs(float(sp.sqrt(sp.Rational(40, 39))) - 1.0127) < 1e-3,
    "n=40 では s/σ は約 1.013")
chk(abs(float(sp.Rational("6.40") * sp.sqrt(sp.Rational(40, 39))) - 6.48) < 0.005,
    "σx=6.40, n=40 なら sx は 6.48")

# --- 「σ は与えられている」が偽だった -----------------------------------
in_text("$\\sigma$ か variance のどちらかが与えられていて、計算するのは平方根と "
        "$2$ 乗だけです。", "与えられているものの言い直し")
not_in_text("このページの例題と演習も、$\\sigma$ の値は与えられています。",
            "古い言い方は消した")

# --- サイズは順序があるので例から外した --------------------------------
in_text("| 数でないもの（色・血液型） | mode |", "血液型に差しかえた")
not_in_text("（色・サイズ）", "サイズは消した")

# --- median が動かない、の但し書き --------------------------------------
in_text("（データが $3$ 個以上のとき）", "3 個以上のとき")
# n = 2 なら動く
chk(med([2, 4]) != med([2, 8]), "n=2 なら最大値を変えると median が動く")
chk(med([1, 2, 3]) == med([1, 2, 30]), "n=3 なら動かない")

# --- 位置の規則の参照先を SL 4.2 に直した --------------------------------
in_text("$\\dfrac{n}{2}$ の位置を読むのではなく、小さい順に数えます"
        "（[SL 4.2](aasl-4-2.qmd#cfgraph)）", "例題1(c) の参照先")
in_text("median は $13$ 番目です（[SL 4.2](aasl-4-2.qmd#cfgraph)）", "演習1 の参照先")
chk(TEXT.count("aasl-4-2.qmd#cfgraph") >= 2, "SL 4.2 を 2 か所で参照")

# --- 例題1 の検算 -------------------------------------------------------
in_text("**検算（(b) について）。** **答えが $x$ の値になっているか見ます。**",
        "例題1(b) の検算")
in_text("**検算（(c) について）。** **反対から数えます。**", "例題1(c) の検算")
not_in_text("たまたま一致しています。", "空の検算は消した")
# 大きいほうから 15・16 番目も 2 であること
_rev = sorted(D1, reverse=True)
chk(_rev[14] == 2 and _rev[15] == 2, "大きいほうから数えても 2")
in_text("$Q_1$ と $Q_3$ は、どちらも表にある $x$ の値です。", "(d) の検算")
not_in_text("mean $1.8$ も、この範囲に入っています。", "条件でない文は消した")

# --- 例題1(d) の解答例に方法を入れた ------------------------------------
in_text("**(d)** lower half $1$–$15$: $Q_1$ is the $8$th value; "
        "upper half $16$–$30$: $Q_3$ is the $23$rd value", "解答例に位置")

# --- 例題2 の検算（(c)） -------------------------------------------------
in_text("**検算（(c) について）。** **度数を合計します。** $4+10+14+8+4 = 40$",
        "例題2(c) の検算")
eq(4 + 10 + 14 + 8 + 4, 40, "度数の合計は 40")
not_in_text("**度数を答えていないか見ます。**", "言い直しの検算は消した")

# --- 例題4 の検算（(c) の大きさ） ----------------------------------------
in_text("variance $6.25$ は $2^{2} = 4$ より大きく $3^{2} = 9$ より小さいので",
        "2 乗ではさむ検算")
chk(4 < sp.Rational("6.25") < 9, "4 < 6.25 < 9")
chk(2 < sp.Rational("2.5") < 3, "2 < 2.5 < 3")
# 2 で割る誤りは、この検算で落ちる
chk(not (2 < sp.Rational("6.25") / 2 < 3), "3.125 は 2 と 3 のあいだにない")
not_in_text("**A と B のあいだか見ます。**", "偶然に頼った検算は消した")

# --- 例題4(d)・演習10 の言いすぎを直した ---------------------------------
in_text("Machine A's masses are therefore the ones lying closest to $200$ g on average",
        "例題4(d) は on average")
not_in_text("closest to $200$ g most often", "most often は消した")
in_text("Class B's scores are therefore typically much further from $62$, on both "
        "sides of it", "演習10 は typically")
not_in_text("contains both lower and higher scores than Class A", "断定は消した")
not_in_text("much weaker and much stronger students", "断定は消した（解答例）")

# --- 演習4 の指示語 -----------------------------------------------------
in_text("and when (ii) every value is multiplied by $4$. Find the new mean and the "
        "new standard deviation when (iii)", "演習4 は Write down と Find を分ける")

# --- 演習5 に σx / sx を選ばせる問いを足した -----------------------------
in_text("Justify which of the two values $6.40$ and $6.48$ should be written as the "
        "standard deviation.", "演習5(b)")
in_text("**(b)** *$\\sigma_x = 6.40$, because at SL the data set is treated as the "
        "population unless the question says otherwise*", "演習5(b) の解答例")
in_text("**検算（(b) について）。** **どちらが大きいか見ます。**", "演習5(b) の検算")
in_text("差は $0.08$ しかないので、**見た目では決められません**", "差は小さい")
eq(sp.Rational("6.48") - sp.Rational("6.40"), sp.Rational("0.08"), "差は 0.08")
chk(sp.Rational("6.48") > sp.Rational("6.40"), "sx > σx")

# --- GDC の節 —— 確認していない操作と、逐語の引用 -------------------------
in_text("標準偏差と分散は電卓で求めるものと決めています", "日本語で書く")
not_in_text("`using only technology`", "Guidance の逐語は貼らない")
in_text("列の先頭にその列の名前（`mass` など）を付け", "列の名前")
in_text("を選び、**データを入れた列を指定します**。", "列を指定する")
in_text("度数の合計より小さければ、度数の列がうまく使われていません。", "n の確かめ方")
not_in_text("これは統計でいちばん多い操作ミスです", "根拠のない断定は消した")

# --- 図 (a) の点を、まん中について対称に置いた --------------------------
in_fig("-0.40, -0.20, 0.0, 0.20, 0.40", "対称なオフセット")
chk("rng.uniform(0, 1, 5)" not in FIGCODE, "片寄る置き方は消した")
in_fig("まん中について対称に置く", "理由をスクリプトに残す")


# ══════════════════════════════════════════════════════════
# 変更指示（2026-09）で直したところ
# ══════════════════════════════════════════════════════════

# --- M09: 例題4(c) の機械 C にも平均を与える -----------------------------
in_text("A third machine, C, produces packets with mean mass $200$ g and "
        "variance $6.25 \\ \\text{g}^{2}$", "M09 機械 C の平均（英語）")
in_text("$3$ 台目の機械 C が作る袋の質量は平均 $200$ g、分散は "
        "$6.25 \\ \\text{g}^{2}$ です。", "M09 機械 C の平均（訳）")
not_in_text("A third machine, C, produces packets with variance",
            "M09 平均のない問題文が消えている")
# (d) が 3 台の平均を同じだとしてよい
in_text("all three have mean $200$ g", "M09 (d) は 3 台とも平均 200 g")

# --- M10: 階級値の平均が真の平均と一致する条件 ---------------------------
in_text("there is no guarantee that the result equals the true mean, "
        "although the two can happen to agree", "M10 解答例")
not_in_text("the true mean would differ unless the values happen to average "
            "to the mid-interval value in every class", "M10 旧解答例が消えた")
in_text("**検算（たまたま合う例）。**", "M10 たまたま合う例")
in_text("**一致する保証がない**、というのが答えです。", "M10 まとめ")
# 反例: [0,10) に 1、[10,20) に 19。階級値の平均も真の平均も 10
_lo, _hi = 1, 19
_mid = (5 + 15) / 2
_true = (_lo + _hi) / 2
chk(_mid == _true == 10, "M10 階級値の平均と真の平均が一致する例")
chk(_lo != 5 and _hi != 15, "M10 どの階級でも階級値と一致していない")
# ずれが出る例: 20≤t<30 に 21 が 3 個
chk(25 * 3 == 75 and 21 * 3 == 63, "M10 ずれが出る例")


# ══════════════════════════════════════════════════════════
# E08  演習2 — 度数表から GDC で平均・σx・分散
# ══════════════════════════════════════════════════════════
in_text("[Use your calculator to find the mean and the standard deviation "
        "$\\sigma_{x}$ of these estimated masses, giving $\\sigma_{x}$ "
        "correct to three significant figures, and hence write down the "
        "variance.", "E08 演習2(b) は GDC")
in_text("どのリストを度数として入れるか、また $40$ 個ぶん入力できているかを"
        "どう確かめるかも書きなさい。", "E08 演習2(b) の訳")
in_text("**度数はもう $1$ つのリストに入れ、`Frequency List` としてその"
        "リストを指定します。**", "E08 度数リストの指定")
in_text("画面の **$n$ が $40$ になっているか**を、必ず見てください。",
        "E08 入力件数の確認")
in_text("**丸めた $9.70$ を $2$ 乗しないでください。**", "E08 丸めてから 2 乗しない")
# 階級値 5,15,25,35 と度数 6,12,14,8
_mid = [5, 15, 25, 35]
_frq = [6, 12, 14, 8]
_nn = sum(_frq)
_mean = sp.Rational(sum(_m * _f for _m, _f in zip(_mid, _frq)), _nn)
_var = sp.Rational(sum(_m ** 2 * _f for _m, _f in zip(_mid, _frq)),
                   _nn) - _mean ** 2
chk(_nn == 40, "E08 度数の合計は 40")
chk(_mean == 21, "E08 平均は 21")
chk(_var == 94, "E08 分散は 94")
chk(float("%.3g" % float(sp.sqrt(_var))) == 9.7, "E08 σx は 3 有効数字で 9.70")
chk(sp.Rational(sum(_mid), 4) == 20, "E08 度数を使わないと 20 になる")
chk(_mean != sp.Rational(sum(_mid), 4), "E08 重みをつけると値が変わる")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
