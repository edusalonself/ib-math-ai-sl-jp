# -*- coding: utf-8 -*-
"""AA SL 5.4 のページを検算する。

    python3 figs/aa-sl/check_aasl_5_4.py
"""
import os
import re

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
QMD = os.path.join(ROOT, "aa-sl", "05-calculus", "aasl-5-4.qmd")
FIGP = os.path.join(HERE, "make_aasl_5_4.py")

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


R = sp.Rational
X = sp.Symbol("x")
A = sp.Symbol("a")


def tangent(f, at):
    """(点の y 座標, 接線の傾き, 接線の式, 法線の式) を返す。"""
    fp = sp.diff(f, X)
    y0 = sp.nsimplify(f.subs(X, at))
    m = sp.nsimplify(fp.subs(X, at))
    tan = sp.expand(m * (X - at) + y0)
    nrm = None if m == 0 else sp.expand(-1 / m * (X - at) + y0)
    return y0, m, tan, nrm


# ══════════════════════════════════════════════════════════
# 1. ページの骨組み
# ══════════════════════════════════════════════════════════
chk(TEXT.startswith("---\nsidebar: aa-sl\n---\n"), "front matter")
in_text("# SL 5.4 — Tangents and normals（接線と法線） {#sec-aasl-5-4}", "見出し")

for _h in ("## What you should be able to do", "## The idea",
           "## Why it works", "## Worked examples", "## Common errors",
           "## Exercises"):
    in_text(_h, "節 " + _h)
not_in_text("## Using your GDC", "Topic 5 に GDC の節は置かない")

_secs = re.findall(r"^### (\d)\. .*\{#([a-z0-9-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 8)],
    "### の番号 1..7: %s" % [s[0] for s in _secs])
chk([s[1] for s in _secs] == ["gradient", "tangent", "normalidea",
                              "normalgrad", "normaleq", "steps", "special"],
    "アンカー: %s" % [s[1] for s in _secs])

chk(len(re.findall(r"^\[\d+\]\{\.ex-no\}", TEXT, re.M)) == 10, "演習 10 問")
chk(TEXT.count("::: {#exm-") == 4, "例題 4 つ")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep 9 個")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳 14")
chk(TEXT.count("</details>") == 14, "details 閉じ 14")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例 14")
chk(len(re.findall(r"^---$", TEXT, re.M)) == 6, "行頭 --- は 6 本")
chk(TEXT.count("{.callout-warning}") == 7, "callout-warning 7（誤り 6 + Paper 1）")
chk(TEXT.count("{.callout-important}") == 0,
    "callout-important 0（5.4 に Topic 5 の公式集の欄はない）")
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
chk(len(_qs) == 4, "Explain 系の問いは 4: %d" % len(_qs))

for _i, _m in enumerate(re.findall(r"\{\.model-answer\}(.*?):::", TEXT, re.S), 1):
    _b = _m.replace("**試験ではこう書く**", "")
    chk(len(_b.split()) <= 115, "model answer %d は 115 語以内" % _i)
    chk(not [c for c in _b if "぀" <= c <= "ヿ" or "一" <= c <= "鿿"],
        "model answer %d に日本語がない" % _i)

in_text("(img/aasl-5-4-idea.svg){#fig-aasl54-idea width=100%}", "図の埋め込み")
in_text("@fig-aasl54-idea (a)", "図 (a) の参照")
in_text("@fig-aasl54-idea (b)", "図 (b) の参照")

for _w in ("そのとおり", "もちろん", "簡単です", "自明", "当たり前", "明らか", "当然"):
    not_in_text(_w, "禁止語 " + _w)
for _w in ("得点になりません", "点になりません", "減点されます"):
    not_in_text(_w, "採点の断定 " + _w)

# ══════════════════════════════════════════════════════════
# 2. 引用と公式集
# ══════════════════════════════════════════════════════════
_quotes = re.findall(r"^> (.*)$", TEXT, re.M)
chk(_quotes == [], "5.4 でシラバスの引用は使わない: %s" % _quotes)
in_text("**@eq-aasl54-line は、公式集の 2.1 の欄にあります。**", "直線の式は 2.1")
in_text("**Topic 5 の欄には、接線・法線の式はありません。**", "5.4 に欄はない")
in_text("**@eq-aasl54-perp は公式集にありません。**", "垂直の関係は公式集にない")

in_text("m = f'(a)\n$$ {#eq-aasl54-m}", "接線の傾きの式")
in_text("y - y_{1} = m(x - x_{1})\n$$ {#eq-aasl54-line}", "直線の式")
in_text("$$ {#eq-aasl54-perp}", "垂直の式")
for _t in ("{#tbl-aasl54-cmp}", "{#tbl-aasl54-steps}", "{#tbl-aasl54-zero}"):
    in_text(_t, "表 " + _t)
in_text("[SL 5.1](aasl-5-1.qmd#gradfn)", "5.1 への参照")
in_text("[SL 5.3](aasl-5-3.qmd#negative)", "5.3 への参照（負の指数）")
in_text("[SL 5.3](aasl-5-3.qmd#constant)", "5.3 への参照（定数倍）")
# 5.8 の語をここで使わない
for _w in ("maximum", "minimum", "極大", "極小", "変曲点", "optimi"):
    not_in_text(_w, "5.8 の語 %s は 5.4 で使わない" % _w)

# ══════════════════════════════════════════════════════════
# 3. 図
# ══════════════════════════════════════════════════════════
in_fig('"(a) The tangent and the normal at $P$"', "図 (a) の題")
in_fig('"(b) Three steps, and one special case"', "図 (b) の題")
in_fig('"tangent"', "図 (a) の接線ラベル")
in_fig('"normal"', "図 (a) の法線ラベル")
in_fig("special case:  $m = 0$", "図 (b) の特別な場合")
in_fig("a vertical line has no gradient", "図 (b) の縦の直線")
# 図の接線と法線が本当に垂直か
_FM = 2 * 0.30 * 2.6
eq(_FM * (-1 / _FM), -1, "図 傾きの積は -1")
_figmath = " ".join(re.findall(r"\$([^$]*)\$", FIGCODE))
for _v in ("2x - 8", "11x", "9x - 27", "6x - 9", "8x - 16", "16", "-4"):
    chk(_v not in _figmath, "図の数式に答え %s は出さない" % _v)
for _bad in ("\\le ", "\\ge ", "\\lvert", "\\rvert", "\\begin{pmatrix}"):
    chk(_bad not in FIGCODE, "図に mathtext が読めない記法: " + _bad)

# ══════════════════════════════════════════════════════════
# 4. 例題
# ══════════════════════════════════════════════════════════
# 例題1  y = x^2 - 4x + 1、x = 3 の接線
_y0, _m, _tan, _nrm = tangent(X ** 2 - 4 * X + 1, 3)
eq(_y0, -2, "例題1 点の y 座標")
eq(_m, 2, "例題1 傾き")
eq(_tan, 2 * X - 8, "例題1 接線")
eq(_tan.subs(X, 3), _y0, "例題1 接線は点を通る")
in_text("y = 2x - 8", "例題1 の答え")

# 例題2  y = x^2 + 1、x = 2 の法線
_y0, _m, _tan, _nrm = tangent(X ** 2 + 1, 2)
eq(_y0, 5, "例題2 点の y 座標")
eq(_m, 4, "例題2 接線の傾き")
eq(-1 / _m, R(-1, 4), "例題2 法線の傾き")
eq(_nrm, -X / 4 + R(11, 2), "例題2 法線")
eq(_nrm.subs(X, 2), _y0, "例題2 法線は点を通る")
eq(_m * (-1 / _m), -1, "例題2 傾きの積")
eq(R(-1, 4) * (-2), R(1, 2), "例題2 かっこをはずす")
in_text("y = -\\frac{1}{4}x + \\frac{11}{2}", "例題2 の答え")

# 例題3  y = x^2 - 6x + 5、x = 3（傾き 0）
_y0, _m, _tan, _nrm = tangent(X ** 2 - 6 * X + 5, 3)
eq(_y0, -4, "例題3 点の y 座標")
eq(_m, 0, "例題3 傾きは 0")
chk(_nrm is None, "例題3 法線は縦の直線")
eq(sp.factor(X ** 2 - 6 * X + 5), (X - 1) * (X - 5), "例題3 因数分解")
eq(((X - 1) * (X - 5)).subs(X, 3), -4, "例題3 因数分解から y 座標")
eq(-(-6) / 2, 3, "例題3 軸の x 座標")
in_text("*the tangent is* $y = -4$", "例題3 接線")
in_text("**(b)** $x = 3$", "例題3 法線")

# 例題4  y = x^3 - 3x^2、傾き 9
_f4 = X ** 3 - 3 * X ** 2
chk(sorted(sp.solve(sp.Eq(sp.diff(_f4, X), 9), X)) == [-1, 3], "例題4 の解")
eq(sp.diff(_f4, X).subs(X, 3), 9, "例題4 x=3 で傾き 9")
eq(sp.diff(_f4, X).subs(X, -1), 9, "例題4 x=-1 でも傾き 9")
eq(_f4.subs(X, 3), 0, "例題4 x=3 の y 座標")
_y0, _m, _tan, _nrm = tangent(_f4, 3)
eq(_tan, 9 * X - 27, "例題4 接線")
eq(sp.expand((X - 3) * (X + 1)), X ** 2 - 2 * X - 3, "例題4 因数分解")
in_text("y = 9x - 27", "例題4 の答え")

# ══════════════════════════════════════════════════════════
# 5. 演習の答え
# ══════════════════════════════════════════════════════════
_E = [("演習1", X ** 2, 1, 1, 2, 2 * X - 1, None),
      ("演習2", 3 * X ** 2 - X, 2, 10, 11, 11 * X - 12, None),
      ("演習3", X ** 3, 1, 1, 3, None, -X / 3 + R(4, 3)),
      ("演習4", 2 / X, 2, 1, R(-1, 2), -X / 2 + 2, None),
      ("演習10", X ** 2 - 4 * X, 1, -3, -2, None, X / 2 + R(-7, 2)),
      ("演習7", X ** 2, 3, 9, 6, 6 * X - 9, None),
      ("演習9", X ** 3 - 4 * X, 2, 0, 8, 8 * X - 16, -X / 8 + R(1, 4))]
for _name, _f, _at, _wy, _wm, _wt, _wn in _E:
    _y0, _m, _tan, _nrm = tangent(_f, _at)
    eq(_y0, _wy, "%s 点の y 座標" % _name)
    eq(_m, _wm, "%s 接線の傾き" % _name)
    if _wt is not None:
        eq(_tan, _wt, "%s 接線" % _name)
        eq(_tan.subs(X, _at), _y0, "%s 接線は点を通る" % _name)
    if _wn is not None:
        eq(_nrm, _wn, "%s 法線" % _name)
        eq(_nrm.subs(X, _at), _y0, "%s 法線は点を通る" % _name)
        eq(_m * (-1 / _m), -1, "%s 傾きの積" % _name)

# 演習5  y = x^2 - 8x、接線が水平
chk(sp.solve(sp.Eq(sp.diff(X ** 2 - 8 * X, X), 0), X) == [4], "演習5 の x")
eq((X ** 2 - 8 * X).subs(X, 4), -16, "演習5 の y")
eq(sp.factor(X ** 2 - 8 * X), X * (X - 8), "演習5 の因数分解")
eq((0 + 8) / 2, 4, "演習5 交点の真ん中")
in_text("*the point is* $(4,\\ -16)$", "演習5 の答え")

# 演習7  生徒のまちがい
eq(sp.expand(2 * X * (X - 3) + 9), 2 * X ** 2 - 6 * X + 9, "演習7 生徒の式の展開")
chk(sp.degree(sp.Poly(2 * X ** 2 - 6 * X + 9, X)) == 2, "演習7 生徒の式は 2 次")
eq((6 * X - 9).subs(X, 3), 9, "演習7 正しい式は点を通る")
in_text("y = 6x - 9", "演習7 の正しい答え")

# 演習8  y = x^3 + ax、f'(1) = 7
_e8 = sp.diff(X ** 3 + A * X, X)
chk(sp.solve(sp.Eq(_e8.subs(X, 1), 7), A) == [4], "演習8 a = 4")
eq(_e8.subs({X: 1, A: 4}), 7, "演習8 もどすと 7")

# 演習10  傾きの積
for _mm in (3, -2, R(2, 3), -4):
    eq(_mm * (-1 / _mm), -1, "演習10 傾きの積 m=%s" % _mm)
in_text("m \\times \\left(-\\frac{1}{m}\\right) = -1", "演習10 の式")

# ★ 例題・演習の答えを本文（例題より前）に出していないこと
for _v in ("2x - 8", "11x - 12", "9x - 27", "6x - 9", "8x - 16",
           "(4,\\ -16)", "\\frac{11}{2}", "\\frac{4}{3}"):
    not_in_body(_v, "答え %s は本文に出さない" % _v)

# ══════════════════════════════════════════════════════════
# 6. ページに書いてある計算を、機械的にたしかめる
# ══════════════════════════════════════════════════════════
_ATOM = r"(?:\\[dt]?frac\{-?\d+\}\{-?\d+\}|-?\d+(?:\.\d+)?)"
_TERM = r"%s(?:\s*\\times\s*%s)*" % (_ATOM, _ATOM)
_EXPR = r"%s(?:\s*[+-]\s*%s)*" % (_TERM, _TERM)
_STMT = re.compile(
    r"(?<![\d\w}])(%s(?:\s*=\s*%s)+)(?!\s*(?:[+-]|[\d.(]|\\(?!ldots|approx)))"
    % (_EXPR, _EXPR))


def _tonum(t):
    t = t.strip()
    m = re.fullmatch(r"\\[dt]?frac\{(-?\d+)\}\{(-?\d+)\}", t)
    if m:
        return sp.Rational(int(m.group(1)), int(m.group(2)))
    return sp.Rational(t)


def _value(expr):
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
    _before = TEXT[:_m.start()].rstrip()
    if _before and _before[-1] in "+-=)*/(":
        continue
    if _before.endswith("\\times"):
        continue
    _vals = [_value(x) for x in _m.group(1).split("=")]
    _nstmt += 1
    chk(len(set(_vals)) == 1,
        "式が合わない: %s  →  %s" % (_m.group(1)[:80], _vals))
chk(_nstmt >= 2, "ページの計算を %d 本たしかめた" % _nstmt)
print("  （計算 %d 本）" % _nstmt)

# ══════════════════════════════════════════════════════════
# 見直し（2026-09）で直したところ。もどってしまわないように。
# ══════════════════════════════════════════════════════════

# --- B1: 図は縦横の目もりをそろえてある（直角が直角に見える）------
chk('ax1.set_aspect("equal", adjustable="box")' in FIG,
    "図(a): 縦横の目もりをそろえている")
chk("直角を直角に見せるため" in FIG, "図(a): その理由が書いてある")

# --- B2: 垂直と傾きの積の同値に条件がついている -------------------
chk("**どちらの直線にも傾きがあるとき**、$2$ つの直線が垂直であることと、"
    "傾きの積が $-1$ であることは同じです。" in TEXT, "第4節: 同値の条件")
chk("片方が縦の直線のときは、傾きがないのでこの言い方はできません。" in TEXT,
    "第4節: 縦の直線を除いている")
chk(TEXT.count("$2$ つの直線が垂直であることと、傾きの積が $-1$ であることは"
                "同じです。") == 1, "条件なしの言い方は残っていない")

# --- B3: 演習10 は計算させてから説明させる ------------------------
chk("Find the gradient of the normal to $C$ at the point where $x = 1$, and "
    "verify that the product" in TEXT, "演習10: 計算してから確かめる")
chk("Explain what is different at the point where $x = 2$." in TEXT,
    "演習10: m = 0 の場合を聞いている")
chk("At a point $P$ on a curve, the tangent has gradient $m$. Explain why"
    not in TEXT, "本文の丸写しだった古い演習10 が消えている")
chk("Rotating a direction of gradient $m$ through a right angle" not in TEXT,
    "Why it works の丸写しが答えから消えている")

# --- B4: 循環していた検算を差しかえた ----------------------------
chk("**検算（別の道で $y_{1}$ を）。** 平方完成すると" in TEXT,
    "例題1: 別の道での検算")
chk("**検算（点が曲線上にあるか）。** $3^{2} - 4 \\times 3 + 1 = -2$"
    not in TEXT, "例題1: 同じ計算をくり返す検算が消えている")
chk("**検算（点が曲線上にあるか）。** $\\dfrac{2}{2} = 1$" not in TEXT,
    "演習4: 同じ計算をくり返す検算が消えている")
chk("**検算（もう $1$ 点で）。** 接線に $x = 4$ を入れると" in TEXT,
    "演習4: 別の点での検算")
chk(TEXT.count("**検算（点が曲線上にあるか）。**") == 1,
    "「曲線上にあるか」の検算は、点が与えられた演習9 だけ")
chk("**検算（取りちがえたらどうなるか）。**" in TEXT,
    "取りちがえたときに何が起こるかを見る検算")
chk("別の数なので、入れかえるとすぐ分かります。" not in TEXT,
    "何も確かめていなかった文が消えている")

# --- M1: Paper 1 の書き方 ---------------------------------------
chk("接線と法線は、電卓が使えない Paper 1 でも出ます。" in TEXT,
    "Paper 1 の注意（技術も使う項目であることと矛盾しない）")
chk("接線と法線は、電卓なしで出します。" not in TEXT,
    "Paper 2 に出ないと読める文が消えている")

# --- M2: 電卓では直角を確かめられない -----------------------------
chk("**法線が直角に見えるかどうかで確かめないでください。**" in TEXT,
    "電卓の節: 直角では確かめない")
chk("（または垂直に交わっている）ようすが見えます。" not in TEXT,
    "画面では確かめられないことを約束した文が消えている")

# --- M3: 回転の議論が負の m でも正しい ----------------------------
chk("**$x$ が $m$ 増えて $y$ が $1$ 減る向き**になります（$m$ が負なら、"
    "$x$ の側は左向きです）。" in TEXT, "Why it works: 負の m の但し書き")
chk("右に $m$ 進んで $1$ 下がる向き、つまり右に $1$ 進んで" not in TEXT,
    "負の m で読めなくなる文が消えている")

# --- m1: Common errors の参照先 ---------------------------------
chk("（[第 6 節](#steps) の $3$ 歩目）。$-\\dfrac{1}{2}$ ではありません。"
    in TEXT, "かっこの符号の誤りは第6節を指す")

# --- m3: 図の式が @eq-aasl54-line と同じ文字 ----------------------
chk("$y - y_{1} = m(x - x_{1})$" in FIG, "図(b): 式の文字が本文と同じ")
chk("with  $x_{1} = a$" in FIG, "図(b): x1 = a と書いてある")

# --- m4: 演習2 は ax + by + d = 0 の形 ---------------------------
chk("giving your answer in the form $ax + by + d = 0$." in TEXT,
    "演習2: 指定された形")
chk("$$11x - y - 12 = 0$$" in TEXT, "演習2 の答え")
chk("**検算（形）。**" in TEXT, "演習2: 形の検算")

# --- m5: 与えられた直線に平行な接線の演習がある --------------------
chk("Find the coordinates of the points on $C$ at which the tangent is "
    "parallel to the line $y = 15x - 4$." in TEXT, "演習6: 平行な接線")
chk("*the points are* $(3,\\ -9)$ *and* $(-3,\\ 9)$" in TEXT, "演習6 の答え")
chk("Find the equation of the normal to $C$ at the point where $x = 1$.]"
    "{.q-en}" in TEXT, "演習3 の法線の問題は残っている")

# --- m6: 点と傾きの形の導出に x != x1 の但し書き -------------------
chk("（$x \\ne x_{1}$ のときの話です）" in TEXT, "Why it works: x != x1")
chk("**かけ算の形にすると、点そのもの（$x = x_{1}$）もふくめて書けます。**"
    in TEXT, "Why it works: かけ算の形なら点もふくむ")

print()
print("OK", OK, "/ NG", NG)
