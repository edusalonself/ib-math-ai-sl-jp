# -*- coding: utf-8 -*-
"""AA SL 5.11 のページを検算する。

    python3 figs/aa-sl/check_aasl_5_11.py

このページは、2026-10-01 に SL 5.11a と SL 5.11b をまとめて作ったものです。
"""
import os
import re

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
QMD = os.path.join(ROOT, "aa-sl", "05-calculus", "aasl-5-11.qmd")
FIGP = os.path.join(HERE, "make_aasl_5_11.py")

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


def in_fig(sub, msg=""):
    chk(sub in FIG, "図に見つからない: %s :: %s" % (msg, sub[:60]))


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: %s :: %s" % (msg, sub[:60]))


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: %s :: %s" % (msg, sub[:60]))


X = sp.Symbol("x", positive=True)
XR = sp.Symbol("x", real=True)


def val(expr, lo, hi, want, msg):
    """定積分の値を確かめる。"""
    chk(sp.simplify(sp.integrate(expr, (XR, lo, hi)) - want) == 0,
        "%s :: int = %s, 答え = %s"
        % (msg, sp.integrate(expr, (XR, lo, hi)), want))


# ══════════════════════════════════════════════════════════
# 1. ページの骨組み
# ══════════════════════════════════════════════════════════
in_text("# SL 5.11 — Definite integrals and areas（定積分と面積） "
        "{#sec-aasl-5-11}", "ページの題")
for _h in ("## What you should be able to do", "## The idea",
           "## Why it works", "## Worked examples", "## Common errors",
           "## Exercises"):
    in_text(_h, "節 " + _h)
not_in_text("## Using your GDC", "Topic 5 に GDC の節は置かない")
not_in_text("5-11a", "5.11a へのリンクは残っていない")
not_in_text("5-11b", "5.11b へのリンクは残っていない")
not_in_text("aasl511a", "古い識別子 aasl511a は残っていない")
not_in_text("aasl511b", "古い識別子 aasl511b は残っていない")

_secs = re.findall(r"^### (\d+)\. (.*) \{#([a-z0-9-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 8)],
    "### の番号 1..7: %s" % [s[0] for s in _secs])
chk([s[2] for s in _secs] == ["what", "props", "positive", "negative",
                              "booklet", "between", "sub"],
    "アンカー: %s" % [s[2] for s in _secs])
for _n, _t, _ in _secs:
    chk(re.match(r"^[a-z]", _t), "見出し %s は英語で始まる: %s" % (_n, _t))
    chk("（" in _t and "）" in _t, "見出し %s は 英語（日本語）: %s" % (_n, _t))

chk(len(re.findall(r"^\[\d+\]\{\.ex-no\}", TEXT, re.M)) == 10, "演習 10 問")
chk([int(x) for x in re.findall(r"^\[(\d+)\]\{\.ex-no\}", TEXT, re.M)]
    == list(range(1, 11)), "演習の番号が 1..10")
chk(TEXT.count("::: {#exm-") == 4, "例題 4 つ")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep 9 個")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳 14 個")
chk(TEXT.count("## 解答例") == 14, "解答例 14 個")
chk(len(re.findall(r"^---$", TEXT, re.M)) == 6, "行頭の --- は 6 本")
chk(TEXT.count("**検算") >= 12, "検算は 12 本以上: %d" % TEXT.count("**検算"))
chk(TEXT.count(":::") % 2 == 0, "::: の数が偶数")
chk("\n\n\n" not in TEXT, "空行が 2 つ続いていない")
for _w in ("そのとおり", "もちろん", "簡単です", "自明", "当たり前", "明らか", "当然"):
    not_in_text(_w, "禁止語 " + _w)
for _w in ("得点になりません", "点になりません", "減点されます"):
    not_in_text(_w, "採点の断定 " + _w)
for _i, _m in enumerate(re.findall(r"\{\.model-answer\}(.*?):::", TEXT, re.S), 1):
    _b = _m.replace("**試験ではこう書く**", "")
    chk(len(_b.split()) <= 115, "model answer %d は 115 語以内" % _i)
    chk(not [c for c in _b if "぀" <= c <= "ヿ" or "一" <= c <= "鿿"],
        "model answer %d に日本語がない" % _i)

# ══════════════════════════════════════════════════════════
# 2. 式・図・参照
# ══════════════════════════════════════════════════════════
for _e in ("{#eq-aasl511-bracket}", "{#eq-aasl511-swap}",
           "{#eq-aasl511-split}", "{#eq-aasl511-zero}",
           "{#eq-aasl511-pos}", "{#eq-aasl511-neg}",
           "{#eq-aasl511-abs}", "{#eq-aasl511-between}"):
    in_text(_e, "式 " + _e)
for _f, _i in (("aasl-5-11-area.svg", "fig-aasl511-area"),
               ("aasl-5-11-below.svg", "fig-aasl511-below"),
               ("aasl-5-11-cross.svg", "fig-aasl511-cross"),
               ("aasl-5-11-between.svg", "fig-aasl511-between")):
    in_text("(img/%s){#%s width=100%%}" % (_f, _i), "図 " + _f)
    chk(os.path.exists(os.path.join(os.path.dirname(QMD), "img", _f)),
        "SVG がある: " + _f)
    chk(("@" + _i) in TEXT, "図を本文から参照している: " + _i)
chk(TEXT.count("](img/") == 4, "図は 4 枚: %d" % TEXT.count("](img/"))
chk([m for m in re.findall(r"\]\(img/aasl-5-11-([a-z]+)\.svg\)", TEXT)]
    == ["area", "below", "cross", "between"], "図の並び")
for _bad in ("\\le ", "\\ge ", "\\lvert", "\\rvert", "\\begin{pmatrix}",
             "\\dfrac", "\\bigl", "\\bigr"):
    chk(_bad not in FIGCODE, "図に mathtext が読めない記法: " + _bad)
_FIGNC = "\n".join(l for l in FIGCODE.split("\n")
                   if not l.lstrip().startswith("#"))
chk(not [c for c in _FIGNC if "぀" <= c <= "ヿ" or "一" <= c <= "鿿"],
    "図のラベルに日本語がない")
# 図の文字が枠の中にあるか
for _ax in ("ax0", "ax1", "ax2", "ax3"):
    _m = re.search(_ax + r"\.set_ylim\(([-\d.]+), ([-\d.]+)\)", FIGCODE)
    chk(_m is not None, _ax + " に set_ylim がある")
    if _m:
        _lo, _hi = float(_m.group(1)), float(_m.group(2))
        for _t in re.finditer(_ax + r"\.text\(\s*[-\d.]+\s*,\s*([-\d.]+)",
                              FIGCODE):
            _y = float(_t.group(1))
            chk(_lo <= _y <= _hi,
                "%s.text の y=%s は %s〜%s の中" % (_ax, _y, _lo, _hi))
# ページ内リンクの行き先
for _a in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(("{#" + _a + "}") in TEXT or ("{#" + _a + " ") in TEXT
        or _a == "why-it-works", "ページ内リンクの行き先がある: #" + _a)
# 節番号とアンカーが合っている
_NUM = {a: int(n) for n, _, a in _secs}
for _m in re.finditer(r"\[第 (\d+) 節\]\(#([a-z0-9-]+)\)", TEXT):
    chk(_NUM.get(_m.group(2)) == int(_m.group(1)),
        "「第 %s 節」(#%s) の番号" % (_m.group(1), _m.group(2)))

# ══════════════════════════════════════════════════════════
# 3. The idea の本文
# ══════════════════════════════════════════════════════════
in_text("**definite integral（定積分）とは、関数を $a \\leq x \\leq b$ の範囲で"
        "積分して、$1$ つの数を出すものです。**", "第 1 節の書き出し")
in_text("**その数は、antiderivative（原始関数）$F$ の両端での差です。**",
        "原始関数は英語も添える")
in_text("$$\n\\int_{a}^{b} f(x)\\,dx = \\bigl[F(x)\\bigr]_{a}^{b} "
        "= F(b) - F(a)\n$$ {#eq-aasl511-bracket}", "定義の式は F と f")
not_in_text("g(b) - g(a)", "定義を g' と g で書いていない")
in_text("**$a$ を lower limit（下端）、$b$ を upper limit（上端）といいます。**",
        "上端・下端の英語")
in_text("**引く順番は「上端 $-$ 下端」です。**", "引く順番")
in_text("**$+C$ は書きません。**", "+C を書かない")
# 2026-10-01：第 1 節の後半 4 段落は削除した
for _s in ("**$F(a)$ が負のときは、かっこを付けてください。**",
           "**$x$ は答えに残りません。**",
           "**@eq-aasl511-bracket は公式集にありません。**",
           "**@eq-aasl511-bracket が使えるのは"):
    not_in_text(_s, "第 1 節の後半は削除した")
_i1a = TEXT.index("### 1. definite integral")
chk(len(TEXT[_i1a:TEXT.index("### 2. limits")].split("\n\n")) <= 8,
    "第 1 節は短くなった")
not_in_text("tbl-aasl511", "表は置いていない")
not_in_text("| 手順 |", "手順の表は置いていない")
# 第 2 節は式を文の中に入れない
_i2 = TEXT.index("### 2. limits of integration")
_i3 = TEXT.index("### 3. area under a curve")
_s2 = TEXT[_i2:_i3]
chk(len(re.findall(r"^\$\$", _s2, re.M)) == 10,
    "第 2 節の display は 5 本: %d" % (len(re.findall(r"^\$\$", _s2, re.M)) / 2))
not_in_text("**どれも @eq-aasl511-bracket から出ます。**", "ここは削除した")
not_in_text("**どの性質も、$a$ と $b$（と $c$）をふくむ", "ここも削除した")
in_text("$$\n\\int_{a}^{b} kf(x)\\,dx = k\\int_{a}^{b} f(x)\\,dx\n$$",
        "定数倍は別の行")
for _s in ("**$1$ つ目。上下を入れかえると、符号が変わります。**",
           "**$2$ つ目。途中の点 $c$ で、区間を分けられます。**",
           "**$3$ つ目。上端と下端が同じなら、値は $0$ です。**"):
    chk(_s in _s2, "第 2 節: " + _s[:24])
chk("\\int_{b}^{a} f(x)\\,dx = -\\int_{a}^{b} f(x)\\,dx$" not in _s2,
    "入れかえの式を文の中に埋めていない")
# 第 3 節（新しい図）
in_text("![The region between $y = f(x)$ and the $x$-axis, from $a$ to $b$]"
        "(img/aasl-5-11-area.svg)", "第 3 節の図")
in_text("**ここでいう面積は、曲線 $y = f(x)$、$x$ 軸、そして $2$ 本の"
        "たての直線 $x = a$、$x = b$ で囲まれた部分の面積です。**",
        "何の面積かを書いてある")
in_text("`the region enclosed by the curve and the x-axis` とだけ",
        "領域の言い方は英語")
# 第 4 節
in_text("その範囲の面積を求めたい場合は、面積は正の数なので、符号を"
        "変えます。", "面積を求めたい場合は")
in_text("**定積分の値は、負の値になることもあります。** それをそのまま"
        "面積にはしないでください。", "負の値の言い方")
for _s in ("**「面積が負になった」ということは起こりません。**",
           "**定積分の値が負になること自体は、まちがいではありません。**",
           "**マイナスを前に書くか、上下を入れかえるかは同じことです**"):
    not_in_text(_s, "第 4 節から削除した")
# 第 5 節（絶対値＋符号の変わる点）
in_text("### 5. the formula booklet form（絶対値でまとめ、符号の変わる点で"
        "分ける） {#booklet}", "第 5 節の見出し")
not_in_text("{#split}", "符号の節は第 5 節に合流した")
not_in_text("splitting at a sign change", "その見出しは消した")
not_in_text("eq-aasl511-areasplit", "一般の式は消した")
not_in_text("**つまり、電卓なしで求められる形が出ます。**", "ここは削除した")
in_text("**電卓で求める場合は、絶対値の記号をそのまま入力してください。**",
        "電卓のときは絶対値をそのまま")
in_text("**$y = 2x - x^{2}$ と $x$ 軸が、$0 \\leq x \\leq 3$ で囲む部分で"
        "やってみます**", "具体例で示す")
in_text("$$\nA = \\int_{0}^{2} \\bigl(2x - x^{2}\\bigr)dx "
        "- \\int_{2}^{3} \\bigl(2x - x^{2}\\bigr)dx\n$$", "具体例の式")
in_text("$$\n= \\frac{4}{3} - \\left(-\\frac{4}{3}\\right) = \\frac{8}{3}\n$$",
        "具体例の値")
_F5 = 2 * XR - XR ** 2
chk(sorted(sp.solve(_F5, XR)) == [0, 2], "2x - x^2 の零点は 0, 2")
chk(_F5.subs(XR, 1) == 1 and _F5.subs(XR, sp.Rational(5, 2)) == sp.Rational(-5, 4),
    "x=1 で正、x=2.5 で負")
chk(sp.integrate(_F5, (XR, 0, 2)) == sp.Rational(4, 3), "0〜2 は 4/3")
chk(sp.integrate(_F5, (XR, 2, 3)) == sp.Rational(-4, 3), "2〜3 は -4/3")
chk(sp.integrate(_F5, (XR, 0, 2)) - sp.integrate(_F5, (XR, 2, 3))
    == sp.Rational(8, 3), "面積は 8/3")
chk(sp.integrate(_F5, (XR, 0, 3)) == 0, "分けずに積分すると 0")
# 第 7 節（置換）を具体例で
in_text("$\\displaystyle\\int_{0}^{2} 2x\\bigl(x^{2}+1\\bigr)^{3}dx$ で"
        "やってみます。", "置換の具体例")
in_text("**中身が $x^{2}+1$ なので、$u$ はこう置きます。**", "u の置き方")
in_text("$$\nu = x^{2}+1, \\qquad du = 2x\\,dx\n$$", "u と du は別の行")
in_text("$$\nx = 0 \\ \\Rightarrow\\ u = 1, \\qquad x = 2 \\ \\Rightarrow\\ u = 5\n$$",
        "上端・下端の直し方は別の行")
not_in_text("**$x$ にもどしてから代入してもかまいません。**",
            "最後の段落は削除した")
in_text("= \\left[\\frac{u^{4}}{4}\\right]_{1}^{5} = \\frac{625}{4} "
        "- \\frac{1}{4} = 156", "置換の値")
val(2 * XR * (XR ** 2 + 1) ** 3, 0, 2, 156, "置換の具体例")
_U2 = sp.Symbol("u")
chk(sp.integrate(_U2 ** 3, (_U2, 1, 5)) == 156, "u は 1 から 5")
chk(TEXT.index("img/aasl-5-11-area.svg")
    < TEXT.index("img/aasl-5-11-below.svg")
    < TEXT.index("img/aasl-5-11-cross.svg")
    < TEXT.index("img/aasl-5-11-between.svg"), "図の順")
# 置換の節はいちばん最後
chk(_secs[-1][2] == "sub", "置換は The idea の最後の節")
_isub = TEXT.index("### 7. substitution")
chk(TEXT.index("### 6. area between two curves") < _isub,
    "置換は面積の説明のあと")
chk("## この項目は電卓なしで解きます" in TEXT[_isub:TEXT.index("## Why it works")],
    "Paper の callout は第 7 節に")
# 交点の話は第 7 節の注意書きに入った
not_in_text("{#which}", "交点の節は消した")
in_text("**上端・下端は、$2$ つのグラフの交点なので、$f(x) = g(x)$ を解いて"
        "求めます。**", "交点の注意書き")
not_in_text("どちらが上かは、$a$ と $b$ の間の値を", "そのあとは削除した")

# ══════════════════════════════════════════════════════════
# 4. 例題の値
# ══════════════════════════════════════════════════════════
in_text("{#exm-aasl511-poly}", "例題 1")
in_text("{#exm-aasl511-props}", "例題 2")
in_text("{#exm-aasl511-split}", "例題 3")
in_text("{#exm-aasl511-between}", "例題 4")
val(3 * XR ** 2 - 4 * XR + 1, 1, 3, 12, "例題 1")
# 例題 2（性質だけで出る）
chk(7 - 3 == 4, "例題 2 (a) 4")
chk(-7 == -(7), "例題 2 (b) -7")
chk(3 * 7 == 21, "例題 2 (c) 21")
# 例題 3（符号の変わる点で分ける）
_f3 = XR ** 2 - XR
chk(sp.solve(_f3, XR) == [0, 1], "例題 3 の零点 0, 1")
chk(sp.simplify(-sp.integrate(_f3, (XR, 0, 1))
                + sp.integrate(_f3, (XR, 1, 2)) - 1) == 0, "例題 3 の面積 1")
chk(sp.integrate(_f3, (XR, 0, 2)) == sp.Rational(2, 3),
    "例題 3：分けずに積分すると 2/3（面積ではない）")
# 例題 4（2 曲線）
_up, _lo = XR + 2, XR ** 2
chk(sorted(sp.solve(sp.Eq(_up, _lo), XR)) == [-1, 2], "例題 4 の交点 -1, 2")
chk(sp.integrate(_up - _lo, (XR, -1, 2)) == sp.Rational(9, 2), "例題 4 の面積 9/2")
chk((_up - _lo).subs(XR, 0) > 0, "例題 4 は x + 2 が上")

# ══════════════════════════════════════════════════════════
# 5. 演習の値
# ══════════════════════════════════════════════════════════
val(XR ** 2 + 1, 0, 2, sp.Rational(14, 3), "演習 1")
val(sp.sin(XR), sp.pi, 3 * sp.pi / 2, -1, "演習 2")
val((XR ** 2 + 1) / sp.sqrt(XR), 1, 4, sp.Rational(72, 5), "演習 3")
# 演習 4：y = x^2 - 3x と x 軸
_f4 = XR ** 2 - 3 * XR
chk(sorted(sp.solve(_f4, XR)) == [0, 3], "演習 4 の零点 0, 3")
chk(-sp.integrate(_f4, (XR, 0, 3)) == sp.Rational(9, 2), "演習 4 の面積 9/2")
# 演習 5：cos x, 0..pi
chk(sp.integrate(sp.cos(XR), (XR, 0, sp.pi / 2))
    - sp.integrate(sp.cos(XR), (XR, sp.pi / 2, sp.pi)) == 2, "演習 5 の面積 2")
chk(sp.integrate(sp.cos(XR), (XR, 0, sp.pi)) == 0,
    "演習 5：分けずに積分すると 0")
# 演習 6：置換（上端・下端も変える）
val(3 * XR ** 2 * (XR ** 3 + 1) ** 2, 0, 1, sp.Rational(7, 3), "演習 6")
_U = sp.Symbol("u")
chk(sp.integrate(_U ** 2, (_U, 1, 2)) == sp.Rational(7, 3),
    "演習 6：u は 1 から 2")
# 演習 7：y = x^2 - 4 と y = -x^2 + 2x
_a7, _b7 = XR ** 2 - 4, -XR ** 2 + 2 * XR
chk(sorted(sp.solve(sp.Eq(_a7, _b7), XR)) == [-1, 2], "演習 7 の交点 -1, 2")
chk(sp.integrate(_b7 - _a7, (XR, -1, 2)) == 9, "演習 7 の面積 9")
# 演習 8：y = x^3 と y = 4x
chk(sorted(sp.solve(sp.Eq(XR ** 3, 4 * XR), XR)) == [-2, 0, 2],
    "演習 8 の交点 -2, 0, 2")
chk(sp.integrate(4 * XR - XR ** 3, (XR, 0, 2))
    + sp.integrate(XR ** 3 - 4 * XR, (XR, -2, 0)) == 8, "演習 8 の面積 8")
chk(sp.integrate(4 * XR - XR ** 3, (XR, -2, 2)) == 0,
    "演習 8：分けずに積分すると 0")
# 演習 9：x^2 + C と書いてしまう
val(2 * XR, 1, 3, 8, "演習 9")
# 演習 10：sin x, 0..2pi
chk(sp.integrate(sp.sin(XR), (XR, 0, 2 * sp.pi)) == 0, "演習 10：積分は 0")
chk(sp.integrate(sp.sin(XR), (XR, 0, sp.pi))
    - sp.integrate(sp.sin(XR), (XR, sp.pi, 2 * sp.pi)) == 4, "演習 10 の面積 4")

# ══════════════════════════════════════════════════════════
# 6. 第 1 節の注意（区間の中に定義されない点）
# ══════════════════════════════════════════════════════════
in_text("$\\displaystyle\\int_{-1}^{1}\\frac{1}{x^{2}}\\,dx$ のように",
        "定義されない点の注意は Common errors に残っている")
chk((-1 / 1) - (-1 / -1) == -2, "角かっこを当てると -2")

# ══════════════════════════════════════════════════════════
# 7. 計画・索引・サイドバー
# ══════════════════════════════════════════════════════════
for _p, _s, _m in (
    (os.path.join(ROOT, "_quarto.yml"),
     'text: "SL 5.11 — Definite integrals and areas"', "サイドバー"),
    (os.path.join(ROOT, "aa-sl", "index.qmd"),
     "[SL 5.11 — Definite integrals and areas](05-calculus/aasl-5-11.qmd)",
     "索引"),
    (os.path.join(ROOT, "_AA-SL-PLAN.md"), "`aasl-5-11.qmd`", "計画"),
):
    chk(_s in open(_p, encoding="utf-8").read(), _m + " に SL 5.11 がある")
for _p in (os.path.join(ROOT, "aa-sl", "05-calculus", "aasl-5-11a.qmd"),
           os.path.join(ROOT, "aa-sl", "05-calculus", "aasl-5-11b.qmd")):
    chk(not os.path.exists(_p), "古いページは消した: " + os.path.basename(_p))



# --- 図 2 は具体的な y = 2x - x^2 ----------------------------------------
in_text("![$y = 2x - x^{2}$: $A_{1}$ is above the axis, $A_{2}$ is below]"
        "(img/aasl-5-11-cross.svg){#fig-aasl511-cross width=100%}",
        "図 2 のキャプション")
in_fig('ax1.set_title("$y = 2x - x^2$"', "図 2 の題")
in_fig("YS = 2 * XS - XS ** 2", "図 2 は y = 2x - x^2")
in_fig('ax1.set_xticklabels(["$0$", "$2$", "$3$"]', "図 2 の目盛は 0, 2, 3")
chk("A curve that crosses the axis" not in FIG, "前の題は消した")
for _c in re.findall(r"^!\[(.*?)\]\(img/", TEXT, re.M):
    chk(0 < len(_c) <= 75, "図のキャプションは 75 字以内（%d 字）: %s"
        % (len(_c), _c[:50]))



# ══════════════════════════════════════════════════════════
# 2026-10-01（その 3）
# ══════════════════════════════════════════════════════════
not_in_text("$\displaystyle\int_{a}^{b} f(x)\,dx$ と書き、不定積分とちがって",
            "第 1 節の 2 文目は削除した")
in_text("**定積分には、計算が短くなる性質が $3$ つあります。**",
        "第 2 節の書き出し")
not_in_text("**上端と下端には、計算が短くなる", "前の書き出しは消した")

# --- 第 4 節：ずっと x 軸の下にある曲線 ----------------------------------
in_text("![$y = x^{2} - 4$ between $x = -2$ and $x = 2$, below the axis]"
        "(img/aasl-5-11-below.svg){#fig-aasl511-below width=100%}", "図 2")
in_fig("YB = XB ** 2 - 4", "図 2 は y = x^2 - 4")
in_fig('ax3.set_title("$y = x^2 - 4$"', "図 2 の題")
_i4d = TEXT.index("### 4. area below the axis")
_i5d = TEXT.index("### 5. the formula booklet form")
_s4d = TEXT[_i4d:_i5d]
chk("img/aasl-5-11-below.svg" in _s4d, "図 2 は第 4 節の中")
chk("img/aasl-5-11-cross.svg" not in _s4d, "交わる図は第 4 節から外した")
in_text("**$y = x^{2} - 4$ と $x$ 軸が囲む部分でやってみます**", "第 4 節の具体例")
in_text("$$\n\\int_{-2}^{2} \\bigl(x^{2} - 4\\bigr)dx "
        "= \\left[\\frac{x^{3}}{3} - 4x\\right]_{-2}^{2} "
        "= -\\frac{16}{3} - \\frac{16}{3} = -\\frac{32}{3}\n$$", "第 4 節の計算")
in_text("$$\nA = -\\left(-\\frac{32}{3}\\right) = \\frac{32}{3}\n$$", "第 4 節の面積")
_FB = XR ** 2 - 4
chk(sorted(sp.solve(_FB, XR)) == [-2, 2], "x^2 - 4 の零点は -2, 2")
chk(sp.maximum(_FB, XR, sp.Interval(-2, 2)) == 0, "-2〜2 で x^2 - 4 は 0 以下")
chk(sp.integrate(_FB, (XR, -2, 2)) == sp.Rational(-32, 3), "積分は -32/3")
chk(-sp.integrate(_FB, (XR, -2, 2)) == sp.Rational(32, 3), "面積は 32/3")

# --- 第 5 節 -------------------------------------------------------------
in_text("$x$ 軸の上なのか下なのかにかかわらず、曲線と $x$ 軸ではさまれた部分の"
        "面積を求める公式は、次のとおりです。", "第 5 節の書き出し")
in_text("**そこで、$x$ 軸の上と下の場合で分けます。**", "x 軸の上と下で分ける")
in_text("**まず、グラフの $x$ 切片（`x-intercept`、`zero`、`root`）を"
        "見つけます**（[SL 5.2](aasl-5-2.qmd#zero)）。", "x 切片")
not_in_text("解が見つかったら、その前後で $1$ 点ずつ", "ここは削除した")
chk("img/aasl-5-11-cross.svg" in TEXT[_i5d:TEXT.index("### 6. area between")],
    "交わる図は第 5 節の中")
chk(TEXT.index("**まず、グラフの $x$ 切片")
    < TEXT.index("img/aasl-5-11-cross.svg")
    < TEXT.index("**$y = 2x - x^{2}$ と $x$ 軸が"), "図は x 切片の話と例の間")

print()
print("OK", OK, "/ NG", NG)
