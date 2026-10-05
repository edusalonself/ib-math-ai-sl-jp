# -*- coding: utf-8 -*-
"""AA SL 5.8 のページを検算する。

    python3 figs/aa-sl/check_aasl_5_8.py

このページは、2026-09-29 に SL 5.8a と SL 5.8b をまとめて作ったものです。
"""
import os
import re

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
QMD = os.path.join(ROOT, "aa-sl", "05-calculus", "aasl-5-8.qmd")
FIGP = os.path.join(HERE, "make_aasl_5_8.py")

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


X = sp.Symbol("x", real=True)
P = sp.Symbol("p", real=True)


def d1(e, v=X):
    return sp.simplify(sp.diff(e, v))


def d2(e, v=X):
    return sp.simplify(sp.diff(e, v, 2))


# ══════════════════════════════════════════════════════════
# 1. ページの骨組み
# ══════════════════════════════════════════════════════════
in_text("# SL 5.8 — Maximum and minimum points, concavity and optimization"
        "（極大・極小・凹凸・変曲点と最適化） {#sec-aasl-5-8}", "ページの題")
for _h in ("## What you should be able to do", "## The idea",
           "## Why it works", "## Worked examples", "## Common errors",
           "## Exercises"):
    in_text(_h, "節 " + _h)
not_in_text("## Using your GDC", "Topic 5 に GDC の節は置かない")

_secs = re.findall(r"^### (\d)\. (.*) \{#([a-z0-9-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 7)],
    "### の番号 1..6: %s" % [s[0] for s in _secs])
chk([s[2] for s in _secs] == ["stationary", "firsttest", "concavity",
                              "secondtest", "inflexion", "what"],
    "アンカー: %s" % [s[2] for s in _secs])

chk(len(re.findall(r"^\[\d+\]\{\.ex-no\}", TEXT, re.M)) == 10, "演習 10 問")
chk([int(x) for x in re.findall(r"^\[(\d+)\]\{\.ex-no\}", TEXT, re.M)]
    == list(range(1, 11)), "演習の番号が 1..10")
chk(TEXT.count("::: {#exm-") == 4, "例題 4 つ")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep 9 個")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳 14 個")
chk(TEXT.count("## 解答例") == 14, "解答例 14 個")
chk(len(re.findall(r"^---$", TEXT, re.M)) == 6, "行頭の --- は 6 本")
chk(TEXT.count("**検算") >= 12, "検算は 12 本以上: %d" % TEXT.count("**検算"))
chk(TEXT.count(":::") % 2 == 0, "::: の数が偶数: %d" % TEXT.count(":::"))
chk("\n\n\n" not in TEXT, "空行が 2 つ続いていない")

for _w in ("そのとおり", "もちろん", "簡単です", "自明", "当たり前", "明らか", "当然"):
    not_in_text(_w, "禁止語 " + _w)
for _w in ("得点になりません", "点になりません", "減点されます"):
    not_in_text(_w, "採点の断定 " + _w)
chk(re.findall(r"^> (.*)$", TEXT, re.M) == [], "5.8 でシラバスの引用は使わない")

for _i, _m in enumerate(re.findall(r"\{\.model-answer\}(.*?):::", TEXT, re.S), 1):
    _b = _m.replace("**試験ではこう書く**", "")
    chk(len(_b.split()) <= 115, "model answer %d は 115 語以内" % _i)
    chk(not [c for c in _b if "぀" <= c <= "ヿ" or "一" <= c <= "鿿"],
        "model answer %d に日本語がない" % _i)

# ══════════════════════════════════════════════════════════
# 2. 式・表・図・参照
# ══════════════════════════════════════════════════════════
in_text("{#eq-aasl58-inflexion}", "変曲点の条件の式")
for _t in ("{#tbl-aasl58-kinds}", "{#tbl-aasl58-second}"):
    in_text(_t, "表 " + _t)
for _f, _i in (("aasl-5-8-idea-a.svg", "fig-aasl58-idea-a"),
               ("aasl-5-8-concavity.svg", "fig-aasl58-concavity"),
               ("aasl-5-8-box.svg", "fig-aasl58-box")):
    in_text("(img/%s){#%s width=100%%}" % (_f, _i), "図 " + _f)
    in_text("@" + _i, "図の参照 @" + _i)
    chk(os.path.exists(os.path.join(os.path.dirname(QMD), "img", _f)),
        "SVG がある: " + _f)
for _bad in ("\\le ", "\\ge ", "\\lvert", "\\rvert", "\\begin{pmatrix}"):
    chk(_bad not in FIGCODE, "図に mathtext が読めない記法: " + _bad)
in_fig('"Maximum, minimum and point of inflexion"', "図 (a) の題")
in_fig('"concave-up:  $f\'\' > 0$"', "図 concavity の左の題")
in_fig('"concave-down:  $f\'\' < 0$"', "図 concavity の右の題")
in_fig('"aasl-5-8-box.svg"', "図 box を書き出している")

for _a in ("aasl-5-2.qmd#zero", "aasl-5-7.qmd#shape", "aasl-5-3.qmd#negative"):
    in_text(_a, "参照 " + _a)
chk(not re.search(r"aasl-5-8[ab]", TEXT), "5.8a / 5.8b へのリンクは残っていない")
for _a in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(("{#" + _a + "}") in TEXT or ("{#" + _a + " ") in TEXT
        or _a == "why-it-works", "ページ内リンクの行き先がある: #" + _a)

# 図のキャプションは 1 行に収める（方針 第 23 節）
for _cm in re.finditer(r"^!\[(.*?)\]\(img/", TEXT, re.M):
    chk(0 < len(_cm.group(1)) <= 75,
        "図のキャプションは 75 字以内（%d 字）: %s"
        % (len(_cm.group(1)), _cm.group(1)[:50]))

# ══════════════════════════════════════════════════════════
# 3. 2026-09-29：5.8a + 5.8b をまとめたときの決めごと
# ══════════════════════════════════════════════════════════
# 5.8b は第 1 節だけ残した
in_text("### 6. optimization（最適化）とは {#what}", "第 6 節の見出し")
in_text("**optimization（最適化）は、ある量をいちばん大きく（小さく）する場面を"
        "求めることです。**", "第 6 節の書き出し")
in_text("**やることは第 1〜5 節と同じで、極大・極小を求めるだけです。**",
        "第 1〜5 節と同じだと言う")
in_text("**式の作り方と進め方は、例題で具体的に見てください。** "
        "例題 $3$ と例題 $4$ が、この形の問題です。", "例題で見せる")
for _s in ("{#steps}", "{#onevariable}", "{#domain}", "{#justify}",
           "{#context}", "{#common}", "### 7."):
    not_in_text(_s, "5.8b の第 2〜7 節は消した: " + _s)
not_in_text("**次の $6$ 歩で進めます**", "手順の 6 歩は消した")
not_in_text("{#tbl-aasl58-steps}", "手順の表は消した")
chk(not os.path.exists(os.path.join(os.path.dirname(QMD), "img",
                                    "aasl-5-8b-idea-a.svg")),
    "6 歩の図は消した")
for _p in ("aasl-5-8a.qmd", "aasl-5-8b.qmd"):
    chk(not os.path.exists(os.path.join(os.path.dirname(QMD), _p)),
        "もとのページは消した: " + _p)
# 箱の図は、例題 4 で使うので残した
_i6 = TEXT.index("### 6. optimization（最適化）とは {#what}")
_iw = TEXT.index(chr(10) + "## Why it works")
_s6 = TEXT[_i6:_iw]
chk("(img/aasl-5-8-box.svg)" in _s6, "箱の図は第 6 節に")
chk("## この項目は Paper 1 でも Paper 2 でも出ます" in _s6,
    "Paper の callout は第 6 節に")
chk(_s6.count("### ") == 1, "第 6 節が The idea の最後")
chk(_s6.count(":::") % 2 == 0, "第 6 節の ::: が閉じている")
in_text("Paper 2 では、文章題の最大・最小を電卓で出してもかまいませんが、"
        "**式を作るところと定義域は自分で書きます。**", "Paper 2 の書き方")
in_text("**文章題では、定義域の外を見ていないかもいっしょに確かめて"
        "ください。**", "電卓では定義域の外に注意")
not_in_text("文章題（面積・体積・利益などを最大にする問題）は",
            "自分のページへ送る文は消した")

# 第 1〜5 節（5.8a 側）の決めごと
in_text("**$f'(a) = 0$ のとき、$a$ の左右で $f'$ の符号を調べる方法です。** "
        "$f'$ が $+$ から $-$ に変われば **local maximum**（極大）、"
        "$-$ から $+$ に変われば **local minimum**（極小）です。",
        "第 2 節: 極大・極小の判定")
in_text("**符号の並びと停留点の種類の対応は、[SL 5.2](aasl-5-2.qmd#zero) に"
        "まとめてあります。** sign diagram のかき方も、そちらを見て"
        "ください。", "第 2 節は 5.2 への参照")
in_text("**$f''$ の符号は、そこでの concavity を表していました**"
        "（[第 3 節](#concavity)）。停留点ではグラフが水平になっているので、"
        "そのまわりが concave-down なら山の形、concave-up なら谷の形です。"
        "**だから、$f''(a)$ の符号が分かれば極大か極小かが決まります。**",
        "第 4 節の書き出しは concavity からの流れ")
in_text("**接線をならべると、傾きの変わり方が見えます**", "第 4 節：図への参照")
in_text("**$f''$ の sign diagram（符号表）をかくのがいちばん確かです**",
        "第 5 節: sign diagram")
in_text("**$f''(a) = 0$ だけでは足りません。**", "x^4 の注意")
in_text("**変曲点は、停留点とはかぎりません。**", "傾きのある変曲点の注意")
not_in_text("{#tbl-aasl58-first}", "5.8a 第 2 節の表は消した")
not_in_text("{#tbl-aasl58-two}", "2 種類の変曲点の表は消した")

# ══════════════════════════════════════════════════════════
# 4. 例題
# ══════════════════════════════════════════════════════════
# 例題1  f(x) = 2x^3 + 3x^2 - 12x + 1
_w1 = 2 * X ** 3 + 3 * X ** 2 - 12 * X + 1
eq(d1(_w1), 6 * X ** 2 + 6 * X - 12, "例題1 の f'")
eq(6 * X ** 2 + 6 * X - 12, 6 * (X + 2) * (X - 1), "例題1 の因数分解")
chk(sorted(sp.solve(sp.Eq(d1(_w1), 0), X)) == [-2, 1], "例題1 の停留点")
eq(d2(_w1), 12 * X + 6, "例題1 の f''")
eq(d2(_w1).subs(X, -2), -18, "例題1 f''(-2)")
eq(d2(_w1).subs(X, 1), 18, "例題1 f''(1)")
eq(_w1.subs(X, -2), 21, "例題1 の極大の y")
eq(_w1.subs(X, 1), -6, "例題1 の極小の y")
in_text("$$(-2,\\ 21) \\quad \\text{and} \\quad (1,\\ -6)$$", "例題1 の答え")

# 例題2  f(x) = x^4 - 4x^3
_w2 = X ** 4 - 4 * X ** 3
eq(d1(_w2), 4 * X ** 3 - 12 * X ** 2, "例題2 の f'")
eq(d2(_w2), 12 * X ** 2 - 24 * X, "例題2 の f''")
eq(12 * X ** 2 - 24 * X, 12 * X * (X - 2), "例題2 の因数分解")
chk(sorted(sp.solve(sp.Eq(d2(_w2), 0), X)) == [0, 2], "例題2 の候補")
for _v, _sg in ((-1, 1), (1, -1), (3, 1)):
    chk(sp.sign(d2(_w2).subs(X, _v)) == _sg, "例題2 f''(%d) の符号" % _v)
eq(_w2.subs(X, 0), 0, "例題2 (0,0)")
eq(_w2.subs(X, 2), -16, "例題2 (2,-16)")
chk(d1(_w2).subs(X, 0) == 0 and d1(_w2).subs(X, 2) != 0,
    "例題2: x=0 は停留点、x=2 はちがう")

# 例題3  長方形、周 40
_A3 = X * (20 - X)
eq(_A3, 20 * X - X ** 2, "例題3 の A")
eq(d1(_A3), 20 - 2 * X, "例題3 の dA/dx")
chk(sp.solve(sp.Eq(d1(_A3), 0), X) == [10], "例題3 の x")
eq(d2(_A3), -2, "例題3 の d2A/dx2")
eq(_A3.subs(X, 10), 100, "例題3 の答え 100")

# 例題4  ふたのない箱、板 24 cm
_V4 = X * (24 - 2 * X) ** 2
eq(sp.factor(d1(_V4)), sp.factor((24 - 2 * X) * (24 - 6 * X)),
   "例題4 の dV/dx")
chk(sorted(sp.solve(sp.Eq(d1(_V4), 0), X)) == [4, 12], "例題4 の候補")
chk(d1(_V4).subs(X, 3) > 0 and d1(_V4).subs(X, 5) < 0, "例題4 x=4 で最大")
eq(_V4.subs(X, 4), 1024, "例題4 の体積 1024")
in_text("*$x = 12$ is outside the domain, so it is rejected*", "例題4 の定義域")

# ══════════════════════════════════════════════════════════
# 5. 演習
# ══════════════════════════════════════════════════════════
_e1 = X ** 3 - 12 * X + 1
eq(d1(_e1), 3 * X ** 2 - 12, "演習1 の f'")
chk(sorted(sp.solve(sp.Eq(d1(_e1), 0), X)) == [-2, 2], "演習1 の停留点")
for _v, _sg in ((-3, 1), (0, -1), (3, 1)):
    chk(sp.sign(d1(_e1).subs(X, _v)) == _sg, "演習1 f'(%d) の符号" % _v)
eq(_e1.subs(X, -2), 17, "演習1 の極大の y")
eq(_e1.subs(X, 2), -15, "演習1 の極小の y")

_e2 = X ** 3 - 3 * X ** 2 + 4
eq(d2(_e2), 6 * X - 6, "演習2 の f''")
chk(sp.solve(sp.Eq(d2(_e2), 0), X) == [1], "演習2 の変曲点の x")
chk(d2(_e2).subs(X, 0) < 0 and d2(_e2).subs(X, 2) > 0, "演習2 で符号が変わる")
eq(_e2.subs(X, 1), 2, "演習2 の y")

_e3 = X ** 4 - 2 * X ** 3
eq(d2(_e3), 12 * X ** 2 - 12 * X, "演習3 の f''")
chk(sp.solve_univariate_inequality(d2(_e3) < 0, X, relational=False)
    == sp.Interval.open(0, 1), "演習3 concave-down は 0 < x < 1")

_e4 = X + 4 / X
eq(d1(_e4), 1 - 4 / X ** 2, "演習4 の f'")
chk(sorted(sp.solve(sp.Eq(d1(_e4), 0), X)) == [-2, 2], "演習4 の停留点")
eq(d2(_e4), 8 / X ** 3, "演習4 の f''")
eq(d2(_e4).subs(X, -2), -1, "演習4 f''(-2)")
eq(d2(_e4).subs(X, 2), 1, "演習4 f''(2)")
eq(_e4.subs(X, -2), -4, "演習4 の極大の y")
eq(_e4.subs(X, 2), 4, "演習4 の極小の y")
chk(-4 < 4, "演習4: 極大の y のほうが小さい")

in_text("*$f''(2) = 0$ does not say that $f''$ changes sign at $2$*",
        "演習5 の答え")

_Y6 = 36 / X
_P6 = 2 * X + 2 * _Y6
eq(_P6, 2 * X + 72 / X, "演習6 の P")
eq(d1(_P6), 2 - 72 / X ** 2, "演習6 の dP/dx")
chk(6 in sp.solve(sp.Eq(d1(_P6), 0), X), "演習6 の x = 6")
eq(d2(_P6).subs(X, 6), sp.Rational(144, 216), "演習6 の d2P/dx2")
chk(d2(_P6).subs(X, 6) > 0, "演習6 は最小")
eq(_P6.subs(X, 6), 24, "演習6 の答え 24")

_A7 = X * (200 - 2 * X)
eq(d1(_A7), 200 - 4 * X, "演習7 の dA/dx")
chk(sp.solve(sp.Eq(d1(_A7), 0), X) == [50], "演習7 の x = 50")
eq(d2(_A7), -4, "演習7 の d2A/dx2")
eq(_A7.subs(X, 50), 5000, "演習7 の答え 5000")

_P8 = P * (60 - 2 * P) - 100
eq(_P8, 60 * P - 2 * P ** 2 - 100, "演習8 の P")
eq(d1(_P8, P), 60 - 4 * P, "演習8 の dP/dp")
chk(sp.solve(sp.Eq(d1(_P8, P), 0), P) == [15], "演習8 の p = 15")
eq(d2(_P8, P), -4, "演習8 の d2P/dp2")
eq(_P8.subs(P, 15), 350, "演習8 の利益 350")

_C9 = 3 * X + 1200 / X
eq(d1(_C9), 3 - 1200 / X ** 2, "演習9 の C'")
chk(20 in sp.solve(sp.Eq(d1(_C9), 0), X), "演習9 の x = 20")
eq(d2(_C9), 2400 / X ** 3, "演習9 の C''")
chk(d2(_C9).subs(X, 20) > 0, "演習9 は最小")

_A10 = X * (24 - X)
eq(d1(_A10), 24 - 2 * X, "演習10 の dA/dx")
chk(sp.solve(sp.Eq(d1(_A10), 0), X) == [12], "演習10 の x = 12")
eq(d2(_A10), -2, "演習10 の d2A/dx2")
eq(_A10.subs(X, 12), 144, "演習10 の面積 144")
in_text("*state the domain $0 < x < 24$*", "演習10: 定義域")

# ══════════════════════════════════════════════════════════
# 6. 本文の数
# ══════════════════════════════════════════════════════════
_Z = sp.Symbol("z", real=True)
eq(sp.diff(_Z ** 4, _Z, 2), 12 * _Z ** 2, "x^4 の f''")
eq(sp.diff(_Z ** 3, _Z, 2), 6 * _Z, "x^3 の f''")
chk((12 * _Z ** 2).subs(_Z, -1) > 0 and (12 * _Z ** 2).subs(_Z, 1) > 0,
    "12z^2 は符号が変わらない")
chk((6 * _Z).subs(_Z, -1) < 0 and (6 * _Z).subs(_Z, 1) > 0,
    "6z は符号が変わる")
# 図 concavity：接線の傾きの向き
_xs = [-1.1, 0.0, 1.1]
chk([2 * 0.42 * _x for _x in _xs] == sorted([2 * 0.42 * _x for _x in _xs]),
    "concave-up では接線の傾きが増える")
chk([2 * -0.42 * _x for _x in _xs]
    == sorted([2 * -0.42 * _x for _x in _xs], reverse=True),
    "concave-down では接線の傾きが減る")



# ══════════════════════════════════════════════════════════
# 2026-09-29（その 2）：表 2 の列を英語に／第 3・4 節を入れかえ
# ══════════════════════════════════════════════════════════
in_text("### 3. concave-up と concave-down {#concavity}", "第 3 節は concavity")
in_text("### 4. second derivative test（第 2 次導関数による判定） {#secondtest}",
        "第 4 節は second derivative test")
chk(TEXT.index("### 3. concave-up と concave-down")
    < TEXT.index("### 4. second derivative test"),
    "concavity が second derivative test より前")
# 表 2 の判定は英語
for _r in ("| $f''(a) < 0$ | *a local maximum* |",
           "| $f''(a) > 0$ | *a local minimum* |",
           "| $f''(a) = 0$ | *not decided by this test* |"):
    in_text(_r, "表 2 の行: " + _r[:26])
for _r in ("| $f''(a) < 0$ | 極大 |", "| $f''(a) > 0$ | 極小 |",
           "| $f''(a) = 0$ | この方法では決まらない |"):
    not_in_text(_r, "日本語の判定は消した: " + _r[:26])
# 取りちがえの注意は concavity（第 3 節）を指す
in_text("**$f'' < 0$ は concave-down、つまり上にふくらんだ形**だと思えば、"
        "取りちがえにくくなります（[第 3 節](#concavity)）。", "取りちがえの注意")
not_in_text("[第 4 節](#concavity)", "#concavity は第 3 節")
not_in_text("[第 3 節](#secondtest)", "#secondtest は第 4 節")
chk(TEXT.count("[第 4 節](#secondtest)") >= 4,
    "#secondtest への参照: %d 件" % TEXT.count("[第 4 節](#secondtest)"))
chk(TEXT.count("[第 3 節](#concavity)") >= 3,
    "#concavity への参照: %d 件" % TEXT.count("[第 3 節](#concavity)"))


# ══════════════════════════════════════════════════════════
# 2026-10-05：表 1 から「図」の列を外した
# ══════════════════════════════════════════════════════════
_ls58 = TEXT.split(chr(10))
_ci58 = [i for i, l in enumerate(_ls58)
         if l.startswith(": ") and "{#tbl-aasl58-kinds}" in l]
chk(len(_ci58) == 1, "tbl-aasl58-kinds がある")
_e58 = _ci58[0]
while not _ls58[_e58].startswith("|"):
    _e58 -= 1
_s58 = _e58
while _s58 > 0 and _ls58[_s58 - 1].startswith("|"):
    _s58 -= 1
chk(_ls58[_s58].rstrip().endswith("そのまわりでのようす |"),
    "最後の列はそのまわりでのようす")
chk(not _ls58[_s58].rstrip().endswith("図 |"), "図の列はない")
_rows58 = _ls58[_s58 + 2:_e58 + 1]
chk(len(_rows58) == 3, "3 行ある")
for _r58 in _rows58:
    chk(_r58.count("|") == 4, "1 行は 3 列: " + _r58[:20])
    chk("@fig-" not in _r58, "行に図の参照はない: " + _r58[:20])
# 図そのものは、表の前の文から参照している
in_text("停留点は次の $3$ 種類のどれかになります（@fig-aasl58-idea-a）。",
        "図は表の前の文で参照")

print()
print("OK", OK, "/ NG", NG)
