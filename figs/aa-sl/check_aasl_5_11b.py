# -*- coding: utf-8 -*-
"""AA SL 5.11b のページを検算する。

    python3 figs/aa-sl/check_aasl_5_11b.py
"""
import os
import re

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
QMD = os.path.join(ROOT, "aa-sl", "05-calculus", "aasl-5-11b.qmd")
FIGP = os.path.join(HERE, "make_aasl_5_11b.py")

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


def dint(f, a, b):
    return sp.simplify(sp.integrate(f, (X, a, b)))


def anti(f, F):
    return sp.simplify(sp.diff(F, X) - f) == 0


# ══════════════════════════════════════════════════════════
# 1. ページの骨組み
# ══════════════════════════════════════════════════════════
chk(TEXT.startswith("---\nsidebar: aa-sl\n---\n"), "front matter")
in_text("# SL 5.11b — Areas（符号のある面積と、$2$ 曲線ではさまれた面積）"
        " {#sec-aasl-5-11b}", "見出し")

for _h in ("## What you should be able to do", "## The idea",
           "## Why it works", "## Worked examples", "## Common errors",
           "## Exercises"):
    in_text(_h, "節 " + _h)
not_in_text("## Using your GDC", "Topic 5 に GDC の節は置かない")

_secs = re.findall(r"^### (\d)\. .*\{#([a-z0-9-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 8)],
    "### の番号 1..7: %s" % [s[0] for s in _secs])
chk([s[1] for s in _secs] == ["positive", "negative", "booklet", "split",
                              "steps", "between", "which"],
    "アンカー: %s" % [s[1] for s in _secs])

chk(len(re.findall(r"^\[\d+\]\{\.ex-no\}", TEXT, re.M)) == 10, "演習 10 問")
chk(TEXT.count("::: {#exm-") == 4, "例題 4 つ")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep 9 個")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳 14")
chk(TEXT.count("</details>") == 14, "details 閉じ 14")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例 14")
chk(len(re.findall(r"^---$", TEXT, re.M)) == 6, "行頭 --- は 6 本")
chk(TEXT.count("{.callout-warning}") == 7, "callout-warning 7（誤り 6 + Paper）")
chk(TEXT.count("{.callout-important}") == 1,
    "callout-important 1（公式集 5.11 の面積の式）")
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
chk(len(_qs) == 3, "Explain 系の問いは 3: %d" % len(_qs))

for _i, _m in enumerate(re.findall(r"\{\.model-answer\}(.*?):::", TEXT, re.S), 1):
    _b = _m.replace("**試験ではこう書く**", "")
    chk(len(_b.split()) <= 115, "model answer %d は 115 語以内" % _i)
    chk(not [c for c in _b if "぀" <= c <= "ヿ" or "一" <= c <= "鿿"],
        "model answer %d に日本語がない" % _i)

in_text("(img/aasl-5-11b-idea.svg){#fig-aasl511b-idea width=100%}", "図の埋め込み")
in_text("@fig-aasl511b-idea (a)", "図 (a) の参照")
in_text("@fig-aasl511b-idea (b)", "図 (b) の参照")

for _w in ("そのとおり", "もちろん", "簡単です", "自明", "当たり前", "明らか", "当然"):
    not_in_text(_w, "禁止語 " + _w)
for _w in ("得点になりません", "点になりません", "減点されます"):
    not_in_text(_w, "採点の断定 " + _w)

chk(not re.search(r"@(eq|tbl|fig)-aasl(?!511b)", TEXT),
    "他ページの @ 参照: %s" % re.findall(r"@(?:eq|tbl|fig)-aasl\w+", TEXT))

# ══════════════════════════════════════════════════════════
# 2. 引用と公式集
# ══════════════════════════════════════════════════════════
_quotes = re.findall(r"^> (.*)$", TEXT, re.M)
chk(_quotes == [
    "Areas of a region enclosed by a curve y = f (x) and the x-axis, where "
    "f (x) can be positive or negative, without the use of technology.",
    "Students are expected to first write a correct expression before "
    "calculating the area."],
    "シラバスの引用は 2 本: %s" % _quotes)
in_text("公式集の **5.11** の欄に、*Area of region enclosed by a curve and "
        "$x$-axis* として @eq-aasl511b-abs が印刷されています。",
        "公式集 5.11 の面積")
in_text("**@eq-aasl511b-between は公式集にありません。**", "2 曲線は公式集にない")
chk(TEXT.count("## この式は公式集にあります") == 1, "公式集の見出し 1 つ")

# ══════════════════════════════════════════════════════════
# 3. 式そのもの
# ══════════════════════════════════════════════════════════
in_text("A = \\int_{a}^{b} f(x)\\,dx, \\qquad f(x) \\geq 0 \\text{ on } "
        "a \\leq x \\leq b\n$$ {#eq-aasl511b-pos}", "f>0 の式")
in_text("A = -\\int_{a}^{b} f(x)\\,dx, \\qquad f(x) \\leq 0 \\text{ on } "
        "a \\leq x \\leq b\n$$ {#eq-aasl511b-neg}", "f<0 の式")
in_text("A = \\int_{a}^{b} \\lvert y\\rvert\\,dx\n$$ {#eq-aasl511b-abs}",
        "絶対値の式")
in_text("A = \\int_{a}^{c} f(x)\\,dx - \\int_{c}^{b} f(x)\\,dx\n"
        "$$ {#eq-aasl511b-split}", "分ける式")
in_text("A = \\int_{a}^{b} \\bigl(f(x) - g(x)\\bigr)dx, \\qquad "
        "f(x) \\geq g(x) \\text{ on } a \\leq x \\leq b\n"
        "$$ {#eq-aasl511b-between}", "2 曲線の式")
in_text("{#tbl-aasl511b-steps}", "参照 手順表")
for _a in ("aasl-5-2.qmd#zero", "aasl-5-5.qmd#area", "aasl-5-5.qmd#expression",
           "aasl-5-10a.qmd#rational", "aasl-5-11a.qmd#props",
           "aasl-5-11a.qmd#value", "aasl-5-11a.qmd#steps"):
    in_text(_a, "参照 " + _a)

# 2 曲線の差は、上下にずらしても変わらない
_f, _g = sp.Function("f"), sp.Function("g")
chk(sp.simplify((_f(X) - 3) - (_g(X) - 3) - (_f(X) - _g(X))) == 0,
    "ずらしても差は同じ")

# ══════════════════════════════════════════════════════════
# 4. 図
# ══════════════════════════════════════════════════════════
in_fig('"(a) A curve that crosses the axis"', "図 (a) の題")
in_fig('"(b) Between two curves"', "図 (b) の題")
in_fig("the integral from $a$ to $b$ gives $A_{1} - A_{2}$", "図 (a) の積分")
in_fig("the area is $A_{1} + A_{2}$, and both of these are positive",
       "図 (a) の面積")
in_fig("$f(x) > 0$ from $a$ to $c$, and $f(x) < 0$ from $c$ to $b$",
       "図 (a) の符号")
in_fig("$f$ is the upper curve, $g$ is the lower curve on $a$ to $b$",
       "図 (b) の上下")
in_fig("$a$ and $b$ come from solving $f(x) = g(x)$", "図 (b) の交点")
_figmath = " ".join(re.findall(r"\$([^$]*)\$", FIGCODE))
for _v in ("x^{2} - 4", "\\frac{16}{3}", "\\frac{9}{2}", "125", "\\sqrt{x}"):
    chk(_v not in _figmath, "図の数式に具体的な数・式 %s は出さない" % _v)
for _bad in ("\\le ", "\\ge ", "\\lvert", "\\rvert", "\\begin{pmatrix}",
             "\\bigl", "\\bigr", "\\Box"):
    chk(_bad not in FIGCODE, "図に mathtext が読めない記法: " + _bad)

# ══════════════════════════════════════════════════════════
# 5. 例題
# ══════════════════════════════════════════════════════════
# 例題1
chk(anti(X ** 2 - 4, X ** 3 / 3 - 4 * X), "例題1 の原始関数")
eq(dint(X ** 2 - 4, 0, 2), -R(16, 3), "例題1 の積分の値")
eq(-dint(X ** 2 - 4, 0, 2), R(16, 3), "例題1 の面積")
chk(all((X ** 2 - 4).subs(X, _t) <= 0 for _t in (0, 1, R(3, 2), 2)),
    "例題1 は区間で f <= 0")
chk(abs(float(R(16, 3)) - 5.33) < 0.005, "例題1 は約 5.33")
eq(R(8, 3) - 8, -R(16, 3), "例題1 の代入")
in_text("A = \\frac{16}{3}", "例題1 の答え")

# 例題2
chk(anti(X ** 2 - X, X ** 3 / 3 - X ** 2 / 2), "例題2 の原始関数")
eq(dint(X ** 2 - X, 0, 1), -R(1, 6), "例題2 の前半")
eq(dint(X ** 2 - X, 1, 2), R(5, 6), "例題2 の後半")
eq(R(1, 6) + R(5, 6), 1, "例題2 の面積")
eq(dint(X ** 2 - X, 0, 2), R(2, 3), "例題2 で分けないと 2/3")
eq((X ** 2 - X).subs(X, R(1, 2)), -R(1, 4), "例題2 の符号 x=1/2")
eq((X ** 2 - X).subs(X, R(3, 2)), R(3, 4), "例題2 の符号 x=3/2")
chk(sp.solve(sp.Eq(X ** 2 - X, 0), X) == [0, 1], "例題2 の零点")
in_text("A = \\frac{1}{6} + \\frac{5}{6} = 1", "例題2 の答え")

# 例題3
chk(sp.solve(sp.Eq(X ** 2, X + 2), X) == [-1, 2], "例題3 の交点")
chk(sp.expand((X + 1) * (X - 2)) == X ** 2 - X - 2, "例題3 の因数分解")
eq(dint(X + 2 - X ** 2, -1, 2), R(9, 2), "例題3 の面積")
chk(anti(X + 2 - X ** 2, X ** 2 / 2 + 2 * X - X ** 3 / 3), "例題3 の原始関数")
eq((X + 2 - X ** 2).subs(X, R(1, 2)), R(9, 4), "例題3 の最大の高さ")
chk(R(9, 2) < 3 * R(9, 4), "例題3 の面積は 幅 x 高さ より小さい")
eq(2 + 4 - R(8, 3), R(10, 3), "例題3 の上端の代入")
eq(R(1, 2) - 2 + R(1, 3), -R(7, 6), "例題3 の下端の代入")
eq(R(10, 3) + R(7, 6), R(9, 2), "例題3 の引き算")
in_text("= \\frac{10}{3} + \\frac{7}{6} = \\frac{9}{2}", "例題3 の答え")

# 例題4
eq(dint(sp.sqrt(X) - X, 0, 1), R(1, 6), "例題4 の面積")
eq(dint(X - sp.sqrt(X), 0, 1), -R(1, 6), "例題4 で逆に引くと負")
chk(anti(sp.sqrt(X) - X, R(2, 3) * X ** R(3, 2) - X ** 2 / 2),
    "例題4 の原始関数")
eq(sp.sqrt(R(1, 4)), R(1, 2), "例題4 の x=1/4 で sqrt")
chk(R(1, 2) > R(1, 4), "例題4 で曲線が上")
eq(R(2, 3) - R(1, 2), R(1, 6), "例題4 の引き算")
chk(R(1, 6) < R(1, 4), "例題4 の面積は 1/4 より小さい")
in_text("A = \\int_{0}^{1} \\bigl(\\sqrt{x} - x\\bigr)dx", "例題4 の式")

# ══════════════════════════════════════════════════════════
# 6. 演習
# ══════════════════════════════════════════════════════════
chk(sp.solve(sp.Eq(X ** 2 - 3 * X, 0), X) == [0, 3], "演習1 の交点")
eq(dint(X ** 2 - 3 * X, 0, 3), -R(9, 2), "演習1 の積分")
eq(-dint(X ** 2 - 3 * X, 0, 3), R(9, 2), "演習1 の面積")
eq(dint(3 * X - X ** 2, 0, 3), R(9, 2), "演習1 を -f で積分しても同じ")
eq(9 - R(27, 2), -R(9, 2), "演習1 の代入")
eq((X ** 2 - 3 * X).subs(X, 1), -2, "演習1 の符号 x=1")
eq(abs((X ** 2 - 3 * X).subs(X, R(3, 2))), R(9, 4), "演習1 の最大の高さ")
chk(R(9, 2) < 3 * R(9, 4), "演習1 の面積は 幅 x 高さ より小さい")
in_text("= -\\left(9 - \\frac{27}{2}\\right) = \\frac{9}{2}", "演習1 の答え")

chk(sp.solve(sp.Eq(4 - X ** 2, 0), X) == [-2, 2], "演習2 の交点")
eq(dint(4 - X ** 2, -2, 2), R(32, 3), "演習2 の面積")
eq(16 - R(16, 3), R(32, 3), "演習2 の引き算")
chk(abs(float(R(32, 3)) - 10.7) < 0.05, "演習2 は約 10.7")
chk(R(32, 3) < 16, "演習2 の面積は 16 より小さい")
in_text("= \\frac{32}{3}", "演習2 の答え")

eq(dint(X ** 3, -1, 0), -R(1, 4), "演習3 の前半")
eq(dint(X ** 3, 0, 1), R(1, 4), "演習3 の後半")
eq(dint(X ** 3, -1, 1), 0, "演習3 で分けないと 0")
eq(R(1, 4) + R(1, 4), R(1, 2), "演習3 の面積")
in_text("= -\\left(0 - \\frac{1}{4}\\right) + \\left(\\frac{1}{4} - 0\\right) = \\frac{1}{2}", "演習3 の答え")

eq(dint(sp.cos(X), 0, sp.pi / 2), 1, "演習4 の前半")
eq(dint(sp.cos(X), sp.pi / 2, sp.pi), -1, "演習4 の後半")
eq(dint(sp.cos(X), 0, sp.pi), 0, "演習4 で分けないと 0")
chk(sp.cos(sp.pi / 4) > 0 and sp.cos(3 * sp.pi / 4) < 0, "演習4 の符号")
in_text("= 1 + 1 = 2", "演習4 の答え")

chk(sp.solve(sp.Eq(X ** 2 - 4, -X ** 2 + 2 * X), X) == [-1, 2],
    "演習5 の交点")
chk(sp.expand(2 * (X + 1) * (X - 2)) == 2 * X ** 2 - 2 * X - 4,
    "演習5 の因数分解")
chk(sp.expand(-X ** 2 + 2 * X - (X ** 2 - 4)) == -2 * X ** 2 + 2 * X + 4,
    "演習5 の被積分関数")
eq(dint(-2 * X ** 2 + 2 * X + 4, -1, 2), 9, "演習5 の面積")
_F5 = -R(2, 3) * X ** 3 + X ** 2 + 4 * X
chk(anti(-2 * X ** 2 + 2 * X + 4, _F5), "演習5 の原始関数")
eq(_F5.subs(X, 2), R(20, 3), "演習5 の上端")
eq(_F5.subs(X, -1), -R(7, 3), "演習5 の下端")
eq(R(20, 3) + R(7, 3), 9, "演習5 の引き算")
chk((X ** 2 - 4).subs(X, 0) < 0 and (-X ** 2 + 2 * X).subs(X, 0) == 0,
    "演習5 は x 軸をまたぐ")
eq((-2 * X ** 2 + 2 * X + 4).subs(X, -1), 0, "演習5 の交点で高さ 0")
eq((-2 * X ** 2 + 2 * X + 4).subs(X, 2), 0, "演習5 の交点で高さ 0（右）")
in_text("= \\frac{20}{3} + \\frac{7}{3} = 9", "演習5 の答え")

chk(sp.solve(sp.Eq(X ** 3, 4 * X), X) == [-2, 0, 2], "演習6 の交点は 3 つ")
eq(dint(X ** 3 - 4 * X, -2, 0), 4, "演習6 の左の領域")
eq(dint(4 * X - X ** 3, 0, 2), 4, "演習6 の右の領域")
eq(4 + 4, 8, "演習6 の面積")
eq(dint(4 * X - X ** 3, -2, 2), 0, "演習6 で分けないと 0")
chk((X ** 3).subs(X, -1) > (4 * X).subs(X, -1), "演習6 左は曲線が上")
chk((4 * X).subs(X, 1) > (X ** 3).subs(X, 1), "演習6 右は直線が上")
in_text("= 4 + 4 = 8", "演習6 の答え")

chk(sp.solve(sp.Eq(6 * X - X ** 2, 0), X) == [0, 6], "演習7 の交点")
eq(dint(6 * X - X ** 2, 0, 6), 36, "演習7 の面積")
eq(108 - 72, 36, "演習7 の代入")
eq((6 * X - X ** 2).subs(X, 3), 9, "演習7 の最大の高さ")
chk(36 < 6 * 9, "演習7 の面積は 54 より小さい")
in_text("= 36", "演習7 の答え")

chk(sp.solve(sp.Eq(X ** 2 - 2 * X, 0), X) == [0, 2], "演習8 の零点")
eq(dint(X ** 2 - 2 * X, 0, 2), -R(4, 3), "演習8 の前半")
eq(dint(X ** 2 - 2 * X, 2, 3), R(4, 3), "演習8 の後半")
eq(R(4, 3) + R(4, 3), R(8, 3), "演習8 の面積")
eq(dint(X ** 2 - 2 * X, 0, 3), 0, "演習8 で分けないと 0")
eq((X ** 2 - 2 * X).subs(X, R(5, 2)), R(5, 4), "演習8 の符号 x=5/2")
in_text("= \\frac{4}{3} + \\frac{4}{3} = \\frac{8}{3}", "演習8 の答え")

eq(dint(X ** 2 - 1, -1, 1), -R(4, 3), "演習9 の積分")
eq(-dint(X ** 2 - 1, -1, 1), R(4, 3), "演習9 の面積")
chk(all((X ** 2 - 1).subs(X, _t) <= 0 for _t in (-1, -R(1, 2), 0, 1)),
    "演習9 は区間で f <= 0")
chk(abs(float(R(4, 3)) - 1.33) < 0.005, "演習9 は約 1.33")
in_text("A = -\\int_{-1}^{1} \\left(x^{2} - 1\\right)dx = \\frac{4}{3}",
        "演習9 の答え")

eq(dint(sp.sin(X), 0, 2 * sp.pi), 0, "演習10 の積分は 0")
eq(dint(sp.sin(X), 0, sp.pi), 2, "演習10 の前半")
eq(dint(sp.sin(X), sp.pi, 2 * sp.pi), -2, "演習10 の後半")
eq(2 + 2, 4, "演習10 の面積")
chk(abs(float(2 * sp.pi) - 6.28) < 0.005, "演習10 の幅は約 6.28")
chk(4 < float(2 * sp.pi), "演習10 の面積は 2pi より小さい")
in_text("= 2 + 2 = 4", "演習10 の答え")

# ══════════════════════════════════════════════════════════
# 7. 答えを本文に出していないか
# ══════════════════════════════════════════════════════════
for _v in ("\\frac{16}{3}", "\\frac{9}{2}", "\\frac{125}{6}", "\\frac{1}{12}",
           "\\frac{32}{3}", "\\frac{8}{3}", "= 36", "= 18"):
    not_in_body(_v, "答え %s は本文に出さない" % _v)

# ══════════════════════════════════════════════════════════
# 8. ページに書いてある計算を、機械的にたしかめる
# ══════════════════════════════════════════════════════════
_ATOM = r"(?:\\[dt]?frac\{-?\d+\}\{-?\d+\}|-?\d+(?:\.\d+)?)"
_TERM = r"%s(?:\s*\\times\s*%s)*" % (_ATOM, _ATOM)
_EXPR = r"%s(?:\s*[+-]\s*%s)*" % (_TERM, _TERM)
_STMT = re.compile(
    r"(?<![\d\w}])(%s(?:\s*=\s*%s)+)(?!\s*(?:[+-]|[\d.(^]|\\(?!ldots|approx)))"
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
    if _before.endswith("\\times") or _before.endswith("\\div"):
        continue
    if re.search(r"(\\(?:sin|cos|tan|ln|log|exp|sqrt)|[{^_])$", _before):
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

# --- B1: 交点が 2 つとはかぎらない ---------------------------------------
chk("**解が $3$ つ以上あるときは、となり合う解の間ごとに $1$ つの領域が"
    "できます。**" in TEXT, "第7節: 交点が 3 つ以上")
chk("「はさまれた」と書いてあれば、$2$ つの交点が上端と下端です。" not in TEXT,
    "無条件に偽の主張が消えている")
chk("**解が $3$ つ以上あるときは、となり合う解の間で上下が入れかわります。**"
    in TEXT, "第7節: 上下が入れかわる条件")
chk("解が $3$ つ以上あるときは、どの $2$ 解ではさまれた領域かを決めてから"
    "積分します。" in TEXT, "Common errors: 交点")
chk("The two graphs meet only where $\\sqrt{x} = x$, that is at $x = 0$ and "
    "$x = 1$, so their difference cannot change sign between these values."
    in TEXT, "例題4 の model answer")

# --- B2: 「2 つとも負でも差は正」は偽だった --------------------------------
chk("$a \\leq x \\leq b$ で $f(x) \\geq g(x)$ なら、$f$ と $g$ の値が両方とも"
    "負であっても、この差は $0$ 以上になります。" in TEXT, "第6節: 差の符号")
chk("$2$ つとも負でも差は正です。" not in TEXT, "偽の主張が消えている")

# --- B3: シラバスが言っていないことを言わない -------------------------------
chk("**この項目の面積は、電卓を使わずに求めます。**" in TEXT, "Paper の callout")
chk("**面積は、電卓を使わずに求める項目です。**" not in TEXT,
    "広すぎる断定が消えている")
chk("$f(x) > 0$ の面積を電卓で求めるのは" in TEXT, "5.5 との切り分け")

# --- B4: 区間を書かずに解を 1 つだけ書いていた -------------------------------
chk("$$\\cos x = 0, \\quad 0 \\leq x \\leq \\pi \\quad \\Rightarrow \\quad "
    "x = \\frac{\\pi}{2}$$" in TEXT, "演習4: 区間つきで解く")
chk("$$\\cos x = 0 \\quad \\Rightarrow \\quad x = \\frac{\\pi}{2}$$" not in TEXT,
    "区間のない解が消えている")

# --- B5: 「符号の変わる点」→「符号が変わりうる点」 ---------------------------
chk("**まず $f(x) = 0$ を解いて、符号が変わりうる点を見つけます**" in TEXT,
    "第4節: 変わりうる点")
chk("$f(x) = x^{2}$ の $x = 0$ のように、解であっても符号が変わらないことが"
    "あります。" in TEXT, "第4節: 反例")
chk("| $2$ | 見つけた点の前後の $1$ 点で値を調べ、符号が変わっているかを"
    "確かめる |" in TEXT, "手順表: 符号を確かめる行")
chk("| $6$ | 足して、正の数になっていることを確かめる |" in TEXT, "手順表は 6 行")
# x^2 は x = 0 が解だが符号は変わらない
chk((X ** 2).subs(X, -1) > 0 and (X ** 2).subs(X, 1) > 0, "x^2 は符号が変わらない")

# --- M1 + M6: 演習が例題の双子だった -----------------------------------------
chk("Find the area of the region enclosed by the curve $y = x^{2} - 3x$ and "
    "the $x$-axis." in TEXT, "演習1 の英語")
chk("Find the area of the region enclosed by the curves $y = x^{2} - 4$ and "
    "$y = -x^{2} + 2x$." in TEXT, "演習5 の英語")
chk("Find the total area of the regions enclosed by the curve $y = x^{3}$ "
    "and the line $y = 4x$." in TEXT, "演習6 の英語")
chk("$y = x^{2} - 9$" not in TEXT, "例題1 の双子だった演習1 が消えている")
chk("the line $y = x + 6$" not in TEXT, "例題3 の双子だった演習5 が消えている")

# --- M2: 解答例に角かっこの行を入れた -----------------------------------------
chk("$$= -\\left[\\frac{x^{3}}{3} - \\frac{x^{2}}{2}\\right]_{0}^{1} "
    "+ \\left[\\frac{x^{3}}{3} - \\frac{x^{2}}{2}\\right]_{1}^{2}$$" in TEXT,
    "例題2 の角かっこ")
chk("-\\left[\\frac{x^{4}}{4}\\right]_{-1}^{0}" in TEXT, "演習3 の角かっこ")
chk("\\Bigl[\\sin x\\Bigr]_{0}^{\\frac{\\pi}{2}} - \\Bigl[\\sin x\\Bigr]_{\\frac{\\pi}{2}}^{\\pi}"
    in TEXT, "演習4 の角かっこ")
chk("$$A = -\\left[\\frac{x^{3}}{3} - x^{2}\\right]_{0}^{2} "
    "+ \\left[\\frac{x^{3}}{3} - x^{2}\\right]_{2}^{3}$$" in TEXT,
    "演習8 の角かっこ")
chk("\\Bigl[-\\cos x\\Bigr]_{0}^{\\pi} - \\Bigl[-\\cos x\\Bigr]_{\\pi}^{2\\pi}"
    in TEXT, "演習10 の角かっこ")

# --- M3: 循環していた検算 -------------------------------------------------------
chk("**検算（別の道で）。** $\\displaystyle\\int_{0}^{2}\\left(4 - x^{2}\\right)"
    in TEXT, "例題1: 別の道で")
chk("**検算（符号）。** 積分の値が $-\\dfrac{16}{3}$" not in TEXT,
    "言いかえだった検算が消えている（例題1）")
chk("**検算（区間の中で入れかわらないこと）。**" in TEXT, "例題3: 入れかわらない")
chk("**検算（正になっている）。** $\\dfrac{9}{2} > 0$" not in TEXT,
    "偽の推論だった検算が消えている（例題3）")
chk("**検算（逆に引くと）。**" not in TEXT, "恒等式だった検算が消えている（例題4）")
chk("**検算（別の道で）。** $\\displaystyle\\int_{0}^{1} \\sqrt{x}\\,dx"
    in TEXT, "例題4: 別々に積分")
eq(dint(sp.sqrt(X), 0, 1), R(2, 3), "例題4 の sqrt の積分")
eq(dint(X, 0, 1), R(1, 2), "例題4 の x の積分")
eq(R(2, 3) - R(1, 2), R(1, 6), "例題4 の差")

# --- M4: 教えたのに練習させていなかったこと -------------------------------------
chk("この式は、公式集の **5.11** の欄の @eq-aasl511b-abs で $y \\geq 0$ の場合に"
    "あたります" in TEXT, "演習2: 公式集の欄")
chk("$2$ つとも負になる $x$ でも、上のほうを前に書きます。" in TEXT,
    "演習5: x 軸より下でも同じ")
chk("交点が $3$ つあるので、領域は $2$ つです" in TEXT, "演習6: 3 交点")

# --- M5: 区間が与えられないときのやり方 -------------------------------------------
chk("**上端・下端が問題文にないこともあります。**" in TEXT, "第1節: 区間がないとき")
chk("区間が与えられていないので、まず $x$ 軸との交点を求めて、上端・下端に"
    "します（[第 1 節](#positive)）。" in TEXT, "演習7 の送り先")
chk("まず交点を求めて、上端・下端にします（[第 7 節](#which)）。" not in TEXT,
    "まちがった送り先が消えている")

# --- m2 から m13 ---------------------------------------------------------------------
chk("**求められているのは、値の前に式を書くことです。**" in TEXT, "m2: 言い方")
chk("The correct area is $-\\int_{-1}^{1} \\left(x^{2} - 1\\right)dx"
    in TEXT, "m3: マイナスの置き場所")
chk("[Find an expression for the area of this region.]{.q-en}" in TEXT,
    "m4: 例題4(a) の command term")
chk("[Find an expression for the total area of the regions they enclose.]"
    "{.q-en}" in TEXT, "m4: 演習8(a) の command term")
chk("$f(x) = 0$ になる点があるのはかまいません。" in TEXT, "m5: 等号を認める")
chk("XS = np.linspace(1.15, 3.9, 500)" in FIG, "m6: 図 (a) の右端")
chk("いつもの規則で原始関数を書けません" in TEXT, "m8: 言いすぎを直した")
chk("@tbl-aasl511b-steps" in TEXT, "m9: 手順表を参照している")
chk("Find the total area of the regions enclosed by the curve $y = x^{3}$ "
    "and the $x$-axis" in TEXT, "m10: 演習3 は複数形")
chk("Find the total area of the regions enclosed by the curve $y = \\cos x$"
    in TEXT, "m10: 演習4 は複数形")
chk("Explain why the regions enclosed by the curve $y = \\sin x$" in TEXT,
    "m10: 演習10 は複数形")
chk("[SL 5.11a](aasl-5-11a.qmd#value)）。" in TEXT, "m11: リンクにアンカー")
chk("であることが分かっています。" in TEXT, "m12: It is given that の訳")
chk("**検算（大きさ）。** 幅は $\\pi$、およそ $3.14$ で、高さは最大 $1$ です。"
    in TEXT, "m13: 演習4 の検算を替えた")
chk(TEXT.count("**検算（分けないと）。**") <= 3,
    "m13: 同じ検算のくり返しが減っている: %d"
    % TEXT.count("**検算（分けないと）。**"))

print()
print("OK", OK, "/ NG", NG)
