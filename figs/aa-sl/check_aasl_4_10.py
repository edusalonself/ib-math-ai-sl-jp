# -*- coding: utf-8 -*-
"""AA SL 4.10 のページを検算する。

    python3 figs/aa-sl/check_aasl_4_6a.py
"""
import glob
import os
import re
import sys
from fractions import Fraction as F

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
QMD = os.path.join(ROOT, "aa-sl", "04-statistics-and-probability", "aasl-4-10.qmd")
FIGP = os.path.join(HERE, "make_aasl_4_10.py")

TEXT = open(QMD, encoding="utf-8").read()
FIG = open(FIGP, encoding="utf-8").read()
FIGCODE = FIG.split('"""', 2)[-1]

OK = 0
NG = 0


def chk(cond, msg=""):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def eq(a, b, msg=""):
    chk(sp.simplify(sp.nsimplify(a) - sp.nsimplify(b)) == 0,
        "%s :: %s != %s" % (msg, a, b))


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: %s :: %s" % (msg, sub[:60]))


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: %s :: %s" % (msg, sub[:60]))


def in_fig(sub, msg=""):
    chk(sub in FIG, "図に見つからない: %s :: %s" % (msg, sub[:60]))


BODY = TEXT.split("## Worked examples")[0]


def not_in_body(sub, msg=""):
    chk(sub not in BODY, "本文（例題より前）に残っている: %s :: %s" % (msg, sub[:60]))


DICE = [(a, b) for a in range(1, 7) for b in range(1, 7)]


def prob(space, pred):
    return F(sum(1 for s in space if pred(s)), len(space))


import numpy as np


def fitlines(x, y):
    """(y on x の a, b), (x on y の c, d), r, 平均点 をもどす。"""
    X = np.array(x, dtype=float)
    Y = np.array(y, dtype=float)
    _r = float(np.corrcoef(X, Y)[0, 1])
    _a, _b = np.polyfit(X, Y, 1)
    _c, _d = np.polyfit(Y, X, 1)
    return (float(_a), float(_b)), (float(_c), float(_d)), _r, X.mean(), Y.mean()


def near(v, target, tol=5e-4):
    return abs(v - target) < tol


# ══════════════════════════════════════════════════════════
# 1. ページの骨組み
# ══════════════════════════════════════════════════════════
chk(TEXT.startswith("---\nsidebar: aa-sl\n---\n"), "front matter")
in_text("# SL 4.10 — The regression line of $x$ on $y$"
        "（$x$ を $y$ で表す回帰直線） {#sec-aasl-4-10}", "見出し")

for _h in ("## What you should be able to do", "## The idea", "## Why it works",
           "## Worked examples", "## Common errors", "## Exercises"):
    in_text(_h, "節 " + _h)
not_in_text("## Using your GDC", "4.10 に GDC の節は置かない（4.4 を参照する）")

_secs = re.findall(r"^### (\d)\. .*\{#([a-z-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 8)],
    "### の番号 1..7: %s" % [s[0] for s in _secs])
chk([s[1] for s in _secs] == ["why", "which", "equation", "gdc", "predict",
                              "danger", "compare"],
    "アンカー: %s" % [s[1] for s in _secs])

chk(len(re.findall(r"^\[\d+\]\{\.ex-no\}", TEXT, re.M)) == 10, "演習 10 問")
chk(TEXT.count("::: {#exm-") == 4, "例題 4 つ")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep 9 個")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳 14")
chk(TEXT.count("</details>") == 14, "details 閉じ 14")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例 14")
chk(len(re.findall(r"^---$", TEXT, re.M)) == 6, "行頭 --- は 6 本")
chk(TEXT.count("{.callout-warning}") == 7, "callout-warning 7（誤り 6 + Paper 2 の注 1）")
chk(TEXT.count("{.callout-important}") == 0,
    "callout-important 0（4.10 は公式集に欄がない）")
chk(TEXT.count("**検算") >= 12, "検算 12 以上: %d" % TEXT.count("**検算"))

_d = 0
for _l in TEXT.split("\n"):
    _t = _l.strip()
    if _t.startswith(":::"):
        _d += -1 if _t[3:].strip() == "" else 1
chk(_d == 0, "::: の開閉が合う: %d" % _d)

_verbs = re.compile(r"Explain|Justify|Comment|Interpret|Identify|Describe|Suggest")
_qs = [q for q in re.findall(r"\[([^\[\]]*?)\]\{\.q-en\}", TEXT, re.S)
       if _verbs.search(q)]
chk(TEXT.count("{.model-answer}") == len(_qs),
    "model-answer %d = 問い %d" % (TEXT.count("{.model-answer}"), len(_qs)))
chk(len(_qs) == 9, "Explain 系の問いは 9: %d" % len(_qs))

for _i, _m in enumerate(re.findall(r"\{\.model-answer\}(.*?):::", TEXT, re.S), 1):
    _b = _m.replace("**試験ではこう書く**", "")
    chk(len(_b.split()) <= 115, "model answer %d は 115 語以内" % _i)
    chk(not [c for c in _b if "぀" <= c <= "ヿ" or "一" <= c <= "鿿"],
        "model answer %d に日本語がない" % _i)

in_text("(img/aasl-4-10-idea.svg){#fig-aasl410-idea width=100%}", "図の埋め込み")
in_text("@fig-aasl410-idea (a)", "図 (a) の参照")
in_text("@fig-aasl410-idea (b)", "図 (b) の参照")

chk(not re.search(r"^> ", TEXT, re.M), "引用ブロックは使わない（4.10 に引用可の行はない）")
not_in_text("シラバスにあります", "公式集にない式に callout-important を付けない")
for _w in ("そのとおり", "もちろん", "簡単です", "自明", "当たり前", "明らか"):
    not_in_text(_w, "禁止語 " + _w)
for _w in ("得点になりません", "点になりません", "減点されます"):
    not_in_text(_w, "採点の断定 " + _w)

# ══════════════════════════════════════════════════════════
# 2. 式と参照
# ══════════════════════════════════════════════════════════
in_text("x = cy + d\n$$ {#eq-aasl410-line}", "x on y の式")
not_in_text("a \\times c = r^{2}", "M13 傾きの積の式は削除した")
not_in_text("{#eq-aasl410-product}", "式番号は外した（公式集にない関係だから）")
in_text("{#tbl-aasl410-which}", "直線の選び方の表")
in_text("**この式は公式集にありません。**", "公式集にないことを書く")
in_text("[SL 4.4](aasl-4-4.qmd#regression)", "4.4 の回帰への参照")
in_text("[SL 4.4](aasl-4-4.qmd#prediction)", "4.4 の予測への参照")
in_text("[SL 4.4 の GDC の節](aasl-4-4.qmd#gdc-reg)", "4.4 の GDC への参照")
in_text("**$y$ の列を先、$x$ の列をあとに**指定する", "列の入れかえ")
not_in_text("X List", "検証していない語は使わない")
not_in_text("Y List", "検証していない語は使わない（2）")

# 傾きは σ と r で書ける（本文が使っている形）
_r, _sx, _sy = sp.symbols("r sigma_x sigma_y", positive=True)
_a_sym, _c_sym = _r * _sy / _sx, _r * _sx / _sy
chk(sp.sign(_a_sym.subs(_r, 1)) == sp.sign(_c_sym.subs(_r, 1)),
    "M13 a と c は同符号")
eq(sp.limit(_a_sym, _r, 0), 0, "M13 r→0 で y on x の傾きは 0（水平）")
eq(sp.limit(_c_sym, _r, 0), 0, "M13 r→0 で x on y の傾きは 0（垂直）")
# 式変形した 1/a は、c とはふつう一致しない
chk(sp.simplify(1 / _a_sym - _c_sym) != 0, "M13 1/a と c はちがう")
chk(sp.simplify((1 / _a_sym - _c_sym).subs(_r, 1)) == 0,
    "M13 r = 1 のときだけ一致する")

# ══════════════════════════════════════════════════════════
# 3. 図
# ══════════════════════════════════════════════════════════
in_fig("XS = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=float)", "図の x")
in_fig("YS = np.array([3, 6, 4, 5, 9, 7, 11, 8], dtype=float)", "図の y")
_FA, _FB, _FR, _FMX, _FMY = fitlines([1, 2, 3, 4, 5, 6, 7, 8],
                                     [3, 6, 4, 5, 9, 7, 11, 8])
chk(near(_FMX, 4.5) and near(_FMY, 6.625), "図の平均点 (4.5, 6.625)")
chk(near(_FA[0] * _FMX + _FA[1], _FMY, 1e-9), "図の y on x は平均点を通る")
chk(near(_FB[0] * _FMY + _FB[1], _FMX, 1e-9), "図の x on y は平均点を通る")
chk(_FA[0] * _FR > 0 and _FB[0] * _FR > 0, "図の a・c は r と同符号")
chk(not near(_FA[0], 1 / _FB[0], 1e-3), "図の 2 本は別の直線")
# 図のデータが例題・演習と重ならないこと
chk([3, 6, 4, 5, 9, 7, 11, 8] != [9, 15, 11, 19, 14, 20],
    "図のデータは例題1 とちがう")
# 図に直線の式の数値は書かない
for _v in ("0.86905", "0.73183", "0.79749"):
    chk(_v not in FIGCODE, "図に係数 %s は書かない" % _v)

# ★ 例題・演習の答えを本文に出していないこと
for _v in ("0.799", "0.536", "6.71", "0.568", "20.8", "0.879", "0.781",
           "6.21", "0.935", "13.2", "0.894"):
    not_in_body(_v, "答え %s は本文に出さない" % _v)

# ══════════════════════════════════════════════════════════
# 4. 例題1
# ══════════════════════════════════════════════════════════
E1A, E1B, E1R, E1MX, E1MY = fitlines([2, 4, 5, 7, 8, 10],
                                     [9, 15, 11, 19, 14, 20])
chk(near(E1R, 0.79860), "例題1(a) r = 0.799: %.5f" % E1R)
chk(near(E1B[0], 0.53571), "例題1(b) c = 0.536")
chk(near(E1B[1], -1.85714), "例題1(b) d = -1.86")
chk(near(E1B[0] * 16 + E1B[1], 6.71429), "例題1(c) x = 6.71")
chk(near((16 - E1A[1]) / E1A[0], 7.12, 5e-3), "式変形すると 7.12")
chk(near(E1MX, 6.0) and near(E1MY, 14.6667, 1e-3), "例題1 の平均点")
chk(near(E1B[0] * E1MY + E1B[1], E1MX, 1e-9), "平均点を通る")
chk(E1B[0] > 0 and E1R > 0, "r > 0 なら c > 0")
chk(E1A[0] > 0 and E1B[0] > 0 and E1R > 0, "例題1 は 3 つとも正")
chk(near(1 / E1A[0], 0.84, 5e-3), "例題1 式変形した傾きは 0.84")
chk(not near(1 / E1A[0], E1B[0], 1e-3), "例題1 の 2 本は別の直線")
chk(9 <= 16 <= 20, "y=16 はデータの範囲の中")
chk(2 <= 6.71 <= 10, "x=6.71 はデータの範囲の中")
in_text("x = 0.536y - 1.86", "例題1(b)")
in_text("x = 0.53571(16) - 1.85714 = 6.71", "例題1(c)")

# ══════════════════════════════════════════════════════════
# 5. 例題2
# ══════════════════════════════════════════════════════════
_xv = sp.Symbol("xv")
_sol = sp.solve(sp.Eq(_xv, sp.Rational("0.6") * (sp.Rational("1.5") * _xv
                                                 + 4) - sp.Rational("2.2")),
                _xv)
chk(_sol == [2], "例題2(a) x̄ = 2: %s" % _sol)
eq(sp.Rational("1.5") * 2 + 4, 7, "例題2(a) ȳ = 7")
eq(sp.Rational("0.6") * 7 - sp.Rational("2.2"), 2, "もう一方の式でも 2")
eq(sp.Rational("0.6") * sp.Rational("1.5") * _xv
   - sp.Rational("0.9") * _xv, 0, "0.6×1.5 = 0.9")
eq(sp.Rational("0.6") * 4 - sp.Rational("2.2"), sp.Rational("0.2"),
   "0.6×4 - 2.2 = 0.2")
eq(sp.Rational("0.6") * 10 - sp.Rational("2.2"), sp.Rational("3.8"),
   "例題2(b) x = 3.8")
eq(sp.Rational("1.5") * 5 + 4, sp.Rational("11.5"), "例題2(c) y = 11.5")
chk(sp.Rational("1.5") > 0 and sp.Rational("0.6") > 0,
    "例題2 の 2 本の傾きは同符号")
eq(sp.Rational("1.5") * 2 + 4, 7, "例題2 平均点 (2, 7) は y on x の上")
eq(sp.Rational("0.6") * 7 - sp.Rational("2.2"), 2,
   "例題2 平均点 (2, 7) は x on y の上")
eq((10 - 4) / sp.Rational("1.5"), 4, "まちがった直線だと 4")
chk(sp.Rational("3.8") != 4, "答えが変わる")

# ══════════════════════════════════════════════════════════
# 6. 例題3
# ══════════════════════════════════════════════════════════
E3A, E3B, E3R, E3MX, E3MY = fitlines([10, 14, 16, 20, 22, 26],
                                     [38, 50, 44, 58, 49, 61])
chk(near(E3R, 0.83882), "例題3 r = 0.839")
chk(near(E3B[0], 0.56831), "例題3(a) c = 0.568")
chk(near(E3B[1], -10.41530, 5e-3), "例題3(a) d = -10.4")
chk(near(E3B[0] * 55 + E3B[1], 20.84153, 5e-3), "例題3(b) x = 20.8")
chk(near((55 - E3A[1]) / E3A[0], 22.03846, 5e-3), "式変形すると 22.0")
chk(near(E3MX, 18.0) and near(E3MY, 50.0), "例題3 の平均点 (18, 50)")
chk(near(E3B[0] * E3MY + E3B[1], E3MX, 1e-9), "平均点を通る")
chk(near(E3A[0], 1.23810, 5e-5), "例題3 の y on x の傾き")
chk(near(1 / E3A[0], 0.80769, 5e-5), "例題3 式変形した傾きは 0.80769")
chk(not near(1 / E3A[0], E3B[0], 1e-3), "例題3 の 2 本は別の直線")
chk(E3B[0] * 55 + E3B[1] > E3MX, "y > ȳ なら x > x̄")
in_text("x = 0.568y - 10.4", "例題3(a)")

# ══════════════════════════════════════════════════════════
# 7. 例題4
# ══════════════════════════════════════════════════════════
eq(sp.Rational("0.041") * 400 + sp.Rational("12.6"), sp.Rational("29.0"),
   "例題4(b) 29.0")
eq(sp.Rational("0.041") * 900 + sp.Rational("12.6"), sp.Rational("49.5"),
   "例題4(c) 49.5")
eq(sp.Rational("0.041") * 500, sp.Rational("20.5"), "500 増えると 20.5 増える")
eq(sp.Rational("49.5") - sp.Rational("29.0"), sp.Rational("20.5"),
   "差は 20.5")
chk(200 <= 400 <= 600, "y=400 は範囲の中")
chk(not (200 <= 900 <= 600), "y=900 は範囲の外")
eq(sp.Rational("0.041") * 400, sp.Rational("16.4"), "0.041×400 = 16.4")
eq(sp.Rational("0.041") * 900, sp.Rational("36.9"), "0.041×900 = 36.9")

# ══════════════════════════════════════════════════════════
# 8. 演習の答え
# ══════════════════════════════════════════════════════════
X1A, X1B, X1R, X1MX, X1MY = fitlines([1, 3, 4, 6, 8, 9],
                                     [14, 9, 12, 10, 5, 6])
chk(near(X1R, -0.87895), "演習1 r = -0.879")
chk(near(X1B[0], -0.78090), "演習1 c = -0.781")
chk(near(X1B[1], 12.45506, 5e-3), "演習1 d = 12.5")
chk(near(X1B[0] * 8 + X1B[1], 6.20787, 5e-3), "演習1 x = 6.21")
chk(X1R < 0 and X1B[0] < 0, "r < 0 なら c < 0")
chk(near(X1MX, 31 / 6, 1e-6) and near(X1MY, 56 / 6, 1e-6), "演習1 の平均点")
chk(near(X1B[0] * X1MY + X1B[1], X1MX, 1e-9), "平均点を通る")
chk(X1B[0] * 8 + X1B[1] > X1MX, "y < ȳ で c < 0 なら x > x̄")

_sol2 = sp.solve(sp.Eq(_xv, sp.Rational("0.4") * (2 * _xv + 3)
                       - sp.Rational("0.7")), _xv)
chk(_sol2 == [sp.Rational("2.5")], "演習2 x̄ = 2.5: %s" % _sol2)
eq(2 * sp.Rational("2.5") + 3, 8, "演習2 ȳ = 8")
eq(sp.Rational("0.4") * 8 - sp.Rational("0.7"), sp.Rational("2.5"),
   "もう一方の式でも 2.5")
eq(sp.Rational(1, 2) * 8 - sp.Rational("1.5"), sp.Rational("2.5"),
   "演習2 式変形した式でも x = 2.5")
chk(sp.Rational(1, 2) != sp.Rational("0.4"),
   "演習2 式変形した傾き 0.5 と x on y の傾き 0.4 はちがう")

X3A, X3B, X3R, X3MX, X3MY = fitlines([5, 8, 10, 12, 15, 18],
                                     [22, 26, 25, 31, 29, 35])
chk(near(X3B[0], 0.93519), "演習3 c = 0.935")
chk(near(X3B[1], -14.85185, 5e-3), "演習3 d = -14.9")
chk(near(X3B[0] * 30 + X3B[1], 13.20370, 5e-3), "演習3 x = 13.2")
chk(near(X3A[0], 0.90719, 5e-5), "演習3 の y on x の傾き")
chk(near(X3A[1], 17.71856, 5e-3), "演習3 の y on x の切片")
chk(near((30 - X3A[1]) / X3A[0], 13.53795, 5e-3), "式変形すると 13.5")
chk(near(X3MX, 68 / 6, 1e-6) and near(X3MY, 28.0), "演習3 の平均点")
chk(22 <= 30 <= 35, "y=30 は範囲の中")

eq(1 / sp.Rational("2"), sp.Rational("0.5"), "1/a = 0.5 のとき c=0.4 とちがう")
chk(sp.Rational("0.4") != sp.Rational("0.5"), "c ≠ 1/a")

eq(sp.Rational("0.7") * 20 - 4, 10, "演習5 x = 10")
eq(sp.Rational("0.7") * 20, 14, "0.7×20 = 14")

_dd = sp.Symbol("dd")
chk(sp.solve(sp.Eq(14, sp.Rational("0.8") * 45 + _dd), _dd) == [-22],
    "演習6 d = -22")
eq(sp.Rational("0.8") * 45, 36, "0.8×45 = 36")
eq(36 - 22, 14, "36 - 22 = 14")

eq(sp.Rational("1.6") * sp.Rational("0.5"), sp.Rational("0.8"), "演習7 r² = 0.8")
chk(abs(float(sp.sqrt(sp.Rational("0.8"))) - 0.894) < 5e-4, "演習7 r = 0.894")
chk(-1 <= float(sp.sqrt(sp.Rational("0.8"))) <= 1, "r は -1..1")
chk(abs(float(1 / sp.Rational("1.6")) - 0.625) < 1e-9, "1/1.6 = 0.625")
chk(sp.Rational("0.5") < sp.Rational("0.625"), "c < 1/a")

eq(sp.Rational("1.4") * 150 - 12, 198, "演習9 x = 198")
eq(sp.Rational("1.4") * 150, 210, "1.4×150 = 210")
eq(210 - 12, 198, "210 - 12 = 198")
chk(not (30 <= 150 <= 70), "y=150 は範囲の外")
eq(sp.Rational("1.4") * 50 - 12, 58, "範囲の中なら 58")
chk(30 <= 50 <= 70, "y=50 は範囲の中")

eq(sp.Rational("0.12") ** 2, sp.Rational("0.0144"), "演習10 r² = 0.0144")
chk(sp.Rational("0.0144") < sp.Rational("0.1"), "r² はとても小さい")
# ══════════════════════════════════════════════════════════
# 10. ページに書いてある計算を、機械的に全部たしかめる
# ══════════════════════════════════════════════════════════
_ATOM = r"(?:\\[dt]?frac\{-?\d+\}\{-?\d+\}|-?\d+(?:\.\d+)?)"
_TERM = r"%s(?:\s*\\times\s*%s)*" % (_ATOM, _ATOM)
_EXPR = r"%s(?:\s*[+-]\s*%s)*" % (_TERM, _TERM)
_STMT = re.compile(r"(?<![\d\w}])(%s(?:\s*=\s*%s)+)(?!\s*(?:[+-]|\\times|[\d.(]))"
                   % (_EXPR, _EXPR))


def _tonum(t):
    t = t.strip()
    m = re.fullmatch(r"\\[dt]?frac\{(-?\d+)\}\{(-?\d+)\}", t)
    if m:
        return sp.Rational(int(m.group(1)), int(m.group(2)))
    return sp.Rational(t)


def _value(expr):
    """+ - かけ算だけの式を、かけ算を先に計算して評価する。"""
    total = sp.Integer(0)
    sign = 1
    for _tk in re.finditer(r"([+-])|(%s)" % _TERM, expr):
        if _tk.group(1):
            sign = 1 if _tk.group(1) == "+" else -1
        else:
            prod = sp.Integer(1)
            for _f in re.finditer(_ATOM, _tk.group(2)):
                prod *= _tonum(_f.group(0))
            total += sign * prod
    return total


_nstmt = 0
for _m in _STMT.finditer(TEXT):
    # 長い式の途中を切り取っていないかを見る（直前が演算子や括弧なら飛ばす）
    _before = TEXT[:_m.start()].rstrip()
    if _before and _before[-1] in "+-=)*/(":
        continue
    if _before.endswith("\\times"):
        continue
    _vals = [_value(x) for x in _m.group(1).split("=")]
    _nstmt += 1
    chk(len(set(_vals)) == 1,
        "式が合わない: %s  →  %s" % (_m.group(1)[:80], _vals))
chk(_nstmt >= 8, "ページの計算を %d 本たしかめた" % _nstmt)

# ══════════════════════════════════════════════════════════
# 15. 査読で直したところ（2026-09-08）
# ══════════════════════════════════════════════════════════

# --- B1 c ≤ 1/a は負の傾きで偽 ----------------------------------------
not_in_text("$\\dfrac{1}{|a|}$", "M13 1/|a| の比較は削除した")
not_in_text("**$|c|$ は $\\dfrac{1}{|a|}$ 以下**です。", "M13 §7 の比較")
in_text("**$a$ と $c$ は、どちらも $r$ と同じ符号です。**", "M13 符号")
not_in_text("**$c$ は $\\dfrac{1}{a}$ 以下**です", "誤りは消した")
# 演習1 が反例（傾きが負のとき c > 1/a）
chk(X1A[0] < 0 and X1B[0] < 0, "演習1 は傾きが負")
chk(X1B[0] > 1 / X1A[0], "負のときは c > 1/a（反例）")
chk(abs(X1B[0]) <= abs(1 / X1A[0]) + 1e-12, "絶対値なら成り立つ")
# 正のときも絶対値で成り立つ
chk(abs(E1B[0]) <= abs(1 / E1A[0]) + 1e-12, "例題1 でも |c| ≤ 1/|a|")

# --- B2 禁止語 ---------------------------------------------------------
not_in_text("当然", "禁止語 当然")
in_text("式変形で移り合わないのは、このためです。", "B2 言いかえ")

# --- B3・M1 演習7 を差し替えた -----------------------------------------
in_text("[7]{.ex-no} [For a set of data, the regression line of $x$ on $y$ is "
        "$x = 0.45y + 3.2$", "B3 演習7")
not_in_text("has gradient $1.6$ and the regression line of $x$ on $y$ has "
            "gradient $0.5$", "傾きから r を出す問いは消した")
eq((12 - sp.Rational("3.2")) / sp.Rational("0.45"),
   sp.Rational("8.8") / sp.Rational("0.45"), "式変形の途中")
chk(abs(float((12 - sp.Rational("3.2")) / sp.Rational("0.45")) - 19.6) < 0.05,
    "式変形すると 3 桁で 19.6")
chk(sp.Rational("0.86") != 1 and sp.Rational("0.86") != -1, "r は ±1 でない")
# 目標「x on y で y を予測しない」を問う設問があること
chk("Explain why this does not give the regression estimate of $y$" in TEXT,
    "M1 y を予測しない向きの問いがある")

# --- M2 a×c = r² と σ の式の扱い ---------------------------------------
not_in_text("**この関係は、公式集にもシラバスにもありません。**",
            "M13 傾きの積の補足は削除した")
not_in_text("**ここは参考です。SL の答案では使いません。**",
            "M13 σ の式の参考枠は削除した")
in_text("**なぜ、式変形では、もう一方の直線にならないのでしょうか。**",
        "M13 式変形で説明する")
in_text("$|r| \\le 1$ になっているか", "M2 Paper 2 callout")
not_in_text("傾きの積が $1$ 以下か ——この $3$ つ", "手計算チェックから外した")
not_in_text("@eq-aasl410-product", "式番号の参照は消した")

# --- M3 循環した検算を直した -------------------------------------------
in_text("**検算（もし逆に使ったら）。** この式に $x = 10$ を入れて $y$ を"
        "出そうとすると", "M3 演習5")
not_in_text("**検算（左辺で）。** 式の左辺が $x$ なので", "答えの反復は消した")
not_in_text("**検算（左辺で）。** 予測したい変数が式の左辺に来ます。",
            "答えの反復は消した（演習8）")
in_text("**検算（入れちがえていないか）。** $x$ と $y$ を逆に入れると "
        "$45 = 0.8(14) + d$", "M3 演習6")
not_in_text("**検算（符号で）。** $c = 0.8 > 0$ なので $r > 0$ です。",
            "d を確かめない検算は消した")
# 入れちがえると大きくちがうこと
_dwrong = 45 - sp.Rational("0.8") * 14
eq(_dwrong, sp.Rational("33.8"), "入れちがえると d = 33.8")
eq(sp.Rational("0.8") * 45 + sp.Rational("33.8"), sp.Rational("69.8"),
   "そのとき x = 69.8")
chk(abs(float(sp.Rational("69.8")) - 14) > 50, "x̄ = 14 と大きくちがう")
eq((10 + 4) / sp.Rational("0.7"), 20, "演習5 の逆算はもとの y にもどる")

# --- M4 検算でないものを地の文にした -----------------------------------
in_text("**なぜそうなるか（傾きで見ます）。**", "M4 演習4")
in_text("**参考（与えられた $2$ 本に矛盾がないか）。**", "M4 例題2")
not_in_text("**検算（(d) について、傾きの積で）。**",
            "M13 傾きの積の検算は差しかえた")
not_in_text("**検算（傾きの積で）。**", "M13 演習の検算も差しかえた")
in_text("**検算（(d) について、符号で）。**", "M13 符号での検算")
in_text("**検算（式変形とくらべて）。**", "M13 式変形での検算")
in_text("**なぜそうなるか（まちがった直線を使ったら）。**", "M4 例題2(b)")
not_in_text("**検算（(a) について、傾きの積で）。**", "対象のない検算は直した")
not_in_text("**検算（(b) について、まちがった直線を使ったら）。**",
            "説明を検算と呼ばない")
in_text("**なぜそうなるか（$r$ の大きさ）。**", "M4 演習10")

# --- M5 例題3 の文脈 ---------------------------------------------------
in_text("[A coach records the age, $x$ years, and the time taken to complete a "
        "task, $y$ seconds, of six young athletes.]{.q-en}", "M5 例題3")
not_in_text("of six adults", "adult なのに 10 歳、は消した")
not_in_text("reaction time", "ありえない反応時間は消した")

# --- M6 演習2 の r の検算を消した --------------------------------------
in_text("**検算（$\\bar{y}$ をもう一度）。**", "M6 演習2")
not_in_text("**検算（$r$ の値）。** $r^{2} = 0.8$ なので $r = \\sqrt{0.8} = 0.894$",
            "演習7 の答えの先出しは消した")

# --- M7 X List / Y List をやめた ---------------------------------------
in_text("**$y$ の列を先、$x$ の列をあとに**指定する", "M7 §4")
chk(TEXT.count("$y$ の列を先、$x$ の列をあとに") >= 4,
    "M7 全体で言い方をそろえた: %d" % TEXT.count("$y$ の列を先、$x$ の列をあとに"))

# --- M8 例題1(a) の GDC ------------------------------------------------
in_text("GDC の Linear Regression で出します", "M8")
in_text("`r` の欄がそれです。", "M8 r の欄")
not_in_text("Two-Variable Statistics か Linear Regression",
            "検証していない主張は消した")

# --- m1 演習10 を Comment にした ---------------------------------------
in_text("Comment on the reliability of an estimate made from this line.",
        "m1 演習10")
not_in_text("Suggest what the student should do instead", "Suggest はやめた")
not_in_text("could use $\\\\bar{x}$ as the best available estimate",
            "本文で教えていない代案は消した")

# --- m2 #idea アンカー -------------------------------------------------
in_text("## The idea {#idea}", "m2 #idea")

# --- m3 c の意味 -------------------------------------------------------
in_text("**$c$ の意味は「$y$ が $1$ 増えるごとの $x$ の増え方」です。**", "m3")
not_in_text("**$c$ の単位は", "単位ではなく意味")

# --- m6・m7 model answer ----------------------------------------------
in_text("It estimates that, on average, the temperature is about $0.041$ °C "
        "higher for each extra ice cream sold.", "m6 例題4(a)")
not_in_text("each extra unit of ice-cream sales", "硬い言い方は消した")
in_text("*The two lines minimise gaps in different directions:", "m7 例題1(d)")
not_in_text("minimising different things", "口語は消した")

# --- m8 Common errors --------------------------------------------------
in_text("**逆に、$x = cy + d$ を解いて $y$ を出すのも同じ誤りです。**", "m8")

# --- m9 Why it works ---------------------------------------------------
in_text("ずれの $2$ 乗の和を最小にした結果として、**ずれの和が $0$ になる**"
        "ことが知られているからです。", "m9")
not_in_text("「ずれの和が $0$ になる」ようにつくられているからです",
            "誤解を招く言い方は消した")

# --- m10 水平・垂直 ----------------------------------------------------
in_text("$r \\to 0$ では水平な直線 $y = \\bar{y}$ に近づきます。",
        "M13 r→0 で水平")
in_text("こちらは垂直な直線 $x = \\bar{x}$ に近づきます。",
        "M13 r→0 で垂直")
not_in_text("$2$ 本の傾きの差が大きくなります", "M13 傾きの差は削除した")
not_in_text("$2$ 本のなす角", "M13 目盛りによる言い方は使わない")

# --- m4・m5 図 ---------------------------------------------------------
in_fig('ax2.set_ylabel("$y$", fontsize=10, color=GREY)', "m4 図 (b) の y 軸")
in_fig('"horizontal gaps: $x$ on $y$"', "m5 図のラベル")
chk('"dashed horizontal gaps' not in FIGCODE, "dashed の語は外した")

print()
print("OK", OK, "/ NG", NG)
