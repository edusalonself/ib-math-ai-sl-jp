# -*- coding: utf-8 -*-
"""AA SL 5.10a のページを検算する。

    python3 figs/aa-sl/check_aasl_5_10a.py
"""
import os
import re

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
QMD = os.path.join(ROOT, "aa-sl", "05-calculus", "aasl-5-10a.qmd")
FIGP = os.path.join(HERE, "make_aasl_5_10a.py")

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
X = sp.Symbol("x", positive=True)
XR = sp.Symbol("xr", real=True)


def same(a, b):
    return sp.simplify(sp.nsimplify(a) - sp.nsimplify(b)) == 0


def anti(f, F):
    """F を微分すると f にもどるか。"""
    return sp.simplify(sp.diff(F, X) - f) == 0


# ══════════════════════════════════════════════════════════
# 1. ページの骨組み
# ══════════════════════════════════════════════════════════
chk(TEXT.startswith("---\nsidebar: aa-sl\n---\n"), "front matter")
in_text("# SL 5.10a — Standard integrals（標準的な不定積分と $ax+b$ との合成）"
        " {#sec-aasl-5-10a}", "見出し")

for _h in ("## What you should be able to do", "## The idea",
           "## Why it works", "## Worked examples", "## Common errors",
           "## Exercises"):
    in_text(_h, "節 " + _h)
not_in_text("## Using your GDC", "Topic 5 に GDC の節は置かない")

_secs = re.findall(r"^### (\d)\. .*\{#([a-z0-9-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 8)],
    "### の番号 1..7: %s" % [s[0] for s in _secs])
chk([s[1] for s in _secs] == ["standard", "rational", "lnabs", "signs",
                              "linear", "steps", "notlinear"],
    "アンカー: %s" % [s[1] for s in _secs])

chk(len(re.findall(r"^\[\d+\]\{\.ex-no\}", TEXT, re.M)) == 10, "演習 10 問")
chk(TEXT.count("::: {#exm-") == 4, "例題 4 つ")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep 9 個")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳 14")
chk(TEXT.count("</details>") == 14, "details 閉じ 14")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例 14")
chk(len(re.findall(r"^---$", TEXT, re.M)) == 6, "行頭 --- は 6 本")
chk(TEXT.count("{.callout-warning}") == 7, "callout-warning 7（誤り 6 + Paper）")
chk(TEXT.count("{.callout-important}") == 2,
    "callout-important 2（公式集 5.10 と 5.5）")
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

in_text("(img/aasl-5-10a-idea.svg){#fig-aasl510a-idea width=100%}", "図の埋め込み")
in_text("@fig-aasl510a-idea (a)", "図 (a) の参照")
in_text("@fig-aasl510a-idea (b)", "図 (b) の参照")

for _w in ("そのとおり", "もちろん", "簡単です", "自明", "当たり前", "明らか", "当然"):
    not_in_text(_w, "禁止語 " + _w)
for _w in ("得点になりません", "点になりません", "減点されます"):
    not_in_text(_w, "採点の断定 " + _w)

# ══════════════════════════════════════════════════════════
# 2. 引用と公式集
# ══════════════════════════════════════════════════════════
_quotes = re.findall(r"^> (.*)$", TEXT, re.M)
chk(_quotes == [], "SL 5.10 に引用してよいシラバス文はない: %s" % _quotes)

in_text("公式集の **5.10** の欄に、@eq-aasl510a-ln、@eq-aasl510a-trig の "
        "$2$ 本、@eq-aasl510a-exp が印刷されています。", "公式集 5.10 の 4 本")
in_text("@eq-aasl510a-power は公式集の **5.5** の欄に、*Integral of $x^{n}$* "
        "として印刷されています", "公式集 5.5 の x^n")
in_text("**5.10 の欄ではありません。**", "x^n は 5.10 の欄ではない")
in_text("**@eq-aasl510a-linear は公式集にありません。**", "合成は公式集にない")
in_fig("not printed in the formula booklet", "図: 公式集にない")

# 公式集にない式を「公式集にある」と書いていないか
chk("*Integral of $x^{n}$*" in TEXT, "公式集の項目名（5.5）")
chk(TEXT.count("## この式は公式集にあります") == 2, "公式集の見出し 2 つ")

# ══════════════════════════════════════════════════════════
# 3. 式そのもの
# ══════════════════════════════════════════════════════════
in_text("\\int x^{n}\\,dx = \\frac{x^{n+1}}{n+1} + C, \\qquad n \\ne -1\n"
        "$$ {#eq-aasl510a-power}", "x^n の式")
in_text("\\int \\frac{1}{x}\\,dx = \\ln|x| + C\n$$ {#eq-aasl510a-ln}",
        "1/x の式")
in_text("\\int \\sin x\\,dx = -\\cos x + C, \\qquad "
        "\\int \\cos x\\,dx = \\sin x + C\n$$ {#eq-aasl510a-trig}",
        "sin と cos の式")
in_text("\\int e^{x}\\,dx = e^{x} + C\n$$ {#eq-aasl510a-exp}", "e^x の式")
in_text("\\int \\frac{k}{x}\\,dx = k\\ln|x| + C\n$$ {#eq-aasl510a-kln}",
        "k/x の式")
in_text("\\int f'(ax + b)\\,dx = \\frac{1}{a}f(ax + b) + C, \\qquad a \\ne 0\n"
        "$$ {#eq-aasl510a-linear}", "合成の式")

for _r in ("{#tbl-aasl510a-rational}", "{#tbl-aasl510a-signs}",
           "{#tbl-aasl510a-linear}", "{#tbl-aasl510a-steps}"):
    in_text(_r, "参照 " + _r)
for _a in ("aasl-5-3.qmd#rewrite", "aasl-5-5.qmd#power", "aasl-5-5.qmd#plusc",
           "aasl-5-5.qmd#boundary", "aasl-5-5.qmd#expression",
           "aasl-5-6a.qmd#standard", "aasl-5-6a.qmd#radian",
           "aasl-5-6a.qmd#chain", "aasl-5-6b.qmd#product",
           "aasl-5-10b.qmd"):
    in_text(_a, "参照 " + _a)

# 標準形が正しい（微分してもどるか）
chk(anti(1 / X, sp.log(X)), "1/x の原始関数")
chk(anti(sp.sin(X), -sp.cos(X)), "sin の原始関数")
chk(anti(sp.cos(X), sp.sin(X)), "cos の原始関数")
chk(anti(sp.exp(X), sp.exp(X)), "e^x の原始関数")
chk(sp.simplify(sp.diff(sp.log(-XR), XR) - 1 / XR) == 0,
    "x < 0 で ln(-x) の導関数は 1/x")

# 表の分数の指数
for _n, _F in ((R(1, 2), R(2, 3) * X ** R(3, 2)),
               (R(-1, 2), 2 * X ** R(1, 2)),
               (R(1, 3), R(3, 4) * X ** R(4, 3))):
    chk(anti(X ** _n, _F), "分数の指数 n = %s" % _n)

# 合成の表
_a, _b, _n = sp.symbols("a b n", positive=True)
chk(sp.simplify(sp.diff((_a * X + _b) ** (_n + 1) / (_a * (_n + 1)), X)
                - (_a * X + _b) ** _n) == 0, "表: (ax+b)^n")
chk(sp.simplify(sp.diff(sp.log(_a * X + _b) / _a, X)
                - 1 / (_a * X + _b)) == 0, "表: 1/(ax+b)")
chk(sp.simplify(sp.diff(-sp.cos(_a * X + _b) / _a, X)
                - sp.sin(_a * X + _b)) == 0, "表: sin(ax+b)")
chk(sp.simplify(sp.diff(sp.sin(_a * X + _b) / _a, X)
                - sp.cos(_a * X + _b)) == 0, "表: cos(ax+b)")
chk(sp.simplify(sp.diff(sp.exp(_a * X + _b) / _a, X)
                - sp.exp(_a * X + _b)) == 0, "表: e^(ax+b)")

# ══════════════════════════════════════════════════════════
# 4. 図
# ══════════════════════════════════════════════════════════
in_fig('"(a) Why the integral of $1/x$ needs $|x|$"', "図 (a) の題")
in_fig('"(b) Integrating $f\'(ax + b)$"', "図 (b) の題")
in_fig("gradient $= 1/x > 0$", "図 (a) の右の傾き")
in_fig("gradient $= 1/x < 0$", "図 (a) の左の傾き")
in_fig("the inside must be linear: $ax + b$, nothing else", "図 (b) の注意")
in_fig("differentiate: the chain rule", "図 (b) の微分")
_figmath = " ".join(re.findall(r"\$([^$]*)\$", FIGCODE))
for _v in ("3x - 1", "5x - 1", "2x - 1", "\\frac{8}{3}", "15"):
    chk(_v not in _figmath, "図の数式に具体的な数・式 %s は出さない" % _v)
for _bad in ("\\le ", "\\ge ", "\\lvert", "\\rvert", "\\begin{pmatrix}",
             "\\bigl", "\\bigr", "\\Box"):
    chk(_bad not in FIGCODE, "図に mathtext が読めない記法: " + _bad)

# ══════════════════════════════════════════════════════════
# 5. 例題
# ══════════════════════════════════════════════════════════
# 例題1
_f1 = 4 * sp.sqrt(X) + 6 / X ** 2
_F1 = R(8, 3) * X ** R(3, 2) - 6 / X
chk(anti(_f1, _F1), "例題1 の原始関数")
chk(same(4 * sp.sqrt(X), 4 * X ** R(1, 2)), "例題1 の書きかえ 1")
chk(same(6 / X ** 2, 6 * X ** -2), "例題1 の書きかえ 2")
eq(4 * R(2, 3), R(8, 3), "例題1 の係数")
eq(R(1, 2) + 1, R(3, 2), "例題1 の指数 1")
eq(-2 + 1, -1, "例題1 の指数 2")
in_text("\\frac{8}{3}x^{\\frac{3}{2}} - \\frac{6}{x} + C", "例題1 の答え")

# 例題2
_f2 = 3 / X + 2 * sp.exp(X) - sp.sin(X)
_F2 = 3 * sp.log(X) + 2 * sp.exp(X) + sp.cos(X)
chk(anti(_f2, _F2), "例題2 の原始関数")
in_text("3\\ln|x| + 2e^{x} + \\cos x + C", "例題2 の答え")

# 例題3
chk(anti(sp.cos(3 * X - 1), sp.sin(3 * X - 1) / 3), "例題3(a)")
chk(anti(sp.exp(5 * X - 1), sp.exp(5 * X - 1) / 5), "例題3(b)")
in_text("\\frac{1}{3}\\sin(3x - 1) + C", "例題3(a) の答え")
in_text("\\frac{1}{5}e^{5x - 1} + C", "例題3(b) の答え")

# 例題4
_f4 = 4 / (2 * X - 1)
_F4 = 2 * sp.log(2 * X - 1)
chk(sp.simplify(sp.diff(_F4, X) - _f4) == 0, "例題4 の原始関数")
eq(4 * R(1, 2), 2, "例題4 の係数")
eq(sp.log(1), 0, "例題4 ln 1 = 0")
eq(_F4.subs(X, 1) + 5, 5, "例題4 は (1, 5) を通る")
in_text("y = 2\\ln(2x - 1) + 5", "例題4 の答え")
in_text("2\\ln 1 + C = 5", "例題4 の代入")
chk(sp.Rational(1, 2) * 2 - 1 == 0, "例題4 の端 x = 1/2 で中身が 0")

# ══════════════════════════════════════════════════════════
# 6. 演習
# ══════════════════════════════════════════════════════════
chk(anti(2 / sp.sqrt(X) - X ** 3, 4 * sp.sqrt(X) - X ** 4 / 4), "演習1")
eq(R(-1, 2) + 1, R(1, 2), "演習1 の新しい指数")
eq(2 / R(1, 2), 4, "演習1 の係数")
in_text("4\\sqrt{x} - \\frac{x^{4}}{4} + C", "演習1 の答え")
in_text("2x^{-\\frac{1}{2}} - x^{3}", "演習1 の書きかえ")

chk(anti(5 / X - 3 * sp.cos(X) + 2 * sp.exp(X),
         5 * sp.log(X) - 3 * sp.sin(X) + 2 * sp.exp(X)), "演習2")
in_text("5\\ln|x| - 3\\sin x + 2e^{x} + C", "演習2 の答え")

chk(anti(sp.sqrt(4 * X + 1), (4 * X + 1) ** R(3, 2) / 6), "演習3")
eq(4 * R(3, 2), 6, "演習3 の割る数")
in_text("\\frac{(4x + 1)^{\\frac{3}{2}}}{6} + C", "演習3 の答え")
in_text("(4x + 1)^{\\frac{1}{2}}", "演習3 の書きかえ")

chk(anti(sp.sin(4 * X + 1), -sp.cos(4 * X + 1) / 4), "演習4")
in_text("-\\frac{1}{4}\\cos(4x + 1) + C", "演習4 の答え")

chk(sp.simplify(sp.diff(sp.log(5 * X - 2) / 5, X) - 1 / (5 * X - 2)) == 0,
    "演習5")
in_text("\\frac{1}{5}\\ln\\lvert 5x - 2\\rvert + C", "演習5 の答え")

chk(anti(sp.exp(-2 * X), -sp.exp(-2 * X) / 2), "演習6")
in_text("-\\frac{1}{2}e^{-2x} + C", "演習6 の答え")

chk(anti((3 * X + 2) ** 4, (3 * X + 2) ** 5 / 15), "演習7")
eq(3 * 5, 15, "演習7 の分母")
in_text("\\frac{(3x + 2)^{5}}{15} + C", "演習7 の答え")

_F8 = 2 * sp.log(X) + sp.exp(X) + 4 - sp.E
chk(anti(2 / X + sp.exp(X), _F8), "演習8 の原始関数")
eq(_F8.subs(X, 1), 4, "演習8 は (1, 4) を通る")
chk(abs(float(4 - sp.E) - 1.28) < 0.005, "演習8 の C は約 1.28")
in_text("y = 2\\ln x + e^{x} + 4 - e", "演習8 の答え")

# 演習9: 生徒の答えは 4 倍になる
chk(sp.simplify(sp.diff(2 * sp.sin(2 * X), X) - 4 * sp.cos(2 * X)) == 0,
    "演習9 生徒の答えを微分すると 4cos(2x)")
chk(anti(sp.cos(2 * X), sp.sin(2 * X) / 2), "演習9 の正しい答え")
in_text("\\frac{1}{2}\\sin(2x) + C", "演習9 の答え")

# 演習10: 中身が 1 次式かどうかで判断する
chk(anti(sp.cos(3 * X + 4), sp.sin(3 * X + 4) / 3), "演習10 の 1 つめ")
chk(sp.simplify(sp.diff(sp.sin(3 * X ** 2 + 4), X)
                - 6 * X * sp.cos(3 * X ** 2 + 4)) == 0,
    "演習10 の 2 つめは 6x が付く")
chk(sp.diff(3 * X ** 2 + 4, X).has(X), "演習10 中身の導関数は定数ではない")
in_text("differentiating multiplies by $6x$, which is not a constant",
        "演習10 の答え")

# ══════════════════════════════════════════════════════════
# 7. 答えを本文に出していないか
# ══════════════════════════════════════════════════════════
for _v in ("\\frac{8}{3}x^{\\frac{3}{2}}", "3\\ln|x| + 2e^{x} + \\cos x",
           "\\frac{1}{3}\\sin(3x - 1)", "\\frac{1}{5}e^{5x - 1}",
           "2\\ln(2x - 1) + 5", "4\\sqrt{x} - \\frac{x^{4}}{4}",
           "-\\frac{1}{4}\\cos(4x + 1)", "\\frac{(4x + 1)^{\\frac{3}{2}}}{6}",
           "\\frac{(3x + 2)^{5}}{15}", "4 - e"):
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

# --- B1: 演習9 の検算が、規則を逆に言っていた --------------------------
chk("**検算（ずれの大きさ）。** $\\dfrac{1}{2}$ をかけるべきところを $2$ に"
    "したので、生徒の答えは正しい値の $4$ 倍になっています ✓" in TEXT,
    "演習9: ずれの大きさ")
chk("$2$ をかけるべきところを $\\dfrac{1}{2}$ にすると" not in TEXT,
    "逆に言っていた検算が消えている")
eq(2 / R(1, 2), 4, "演習9 のずれは 4 倍")

# --- B2: Why it works の sin の符号 -----------------------------------
chk("原始関数の候補を $\\cos x$ にしてみます。" in TEXT, "Why: 候補を cos に")
chk("$\\cos x$ を積分すると $\\sin x$ ではなく $-\\sin x$" not in TEXT,
    "微分と積分が入れかわっていた文が消えている")
chk(sp.simplify(sp.diff(sp.cos(X), X) + sp.sin(X)) == 0, "cos の導関数")

# --- B3: b で割らない ---------------------------------------------------
chk("**割るのは $a$ だけで、$b$ では割りません。**" in TEXT, "第5節: b では割らない")
chk("**$b$ は答えに影響しません。**" not in TEXT, "偽の主張が消えている")

# --- B4: 表の条件 -------------------------------------------------------
chk("**この表は、$a$、$b$ が定数で $a \\ne 0$ のときの形です。**" in TEXT,
    "第5節: 表の条件")
chk("$ax + b \\ne 0$ のところで" in TEXT, "第5節: 1/(ax+b) の条件")
chk("$n$ が整数でないとき" in TEXT, "第5節: (ax+b)^n の条件")
chk("**このページでは、$n$ が整数でない $x^{n}$ は $x > 0$ の範囲で考えます。**"
    in TEXT, "第2節: 定義域")

# --- M1: 演習7 で微分して確かめさせる -----------------------------------
chk("Verify your answer by differentiating it." in TEXT, "演習7: Verify")
chk("\\frac{5(3x + 2)^{4} \\times 3}{15} = (3x + 2)^{4} \\ \\checkmark" in TEXT,
    "演習7: 確かめの行")

# --- M2 + M3: 演習10 -----------------------------------------------------
chk("Explain why $\\displaystyle\\int \\cos(3x + 4)\\,dx$ can be found using "
    "the rule for a linear inside" in TEXT, "演習10 の英語")
chk("Explain why $\\displaystyle\\int \\frac{1}{x}\\,dx$ cannot be found"
    not in TEXT, "本文の言いかえだった演習10 が消えている")

# --- M4: 目標を練習に合わせた -------------------------------------------
chk("- $\\ln\\lvert x\\rvert$ と $\\ln x$ の**どちらを書くか**を、定義域から"
    "判断できる。" in TEXT, "目標: ln|x| か ln x か")

# --- M5 + M6: 演習1・2・3 ------------------------------------------------
chk("Find $\\displaystyle\\int \\left(\\frac{2}{\\sqrt{x}} - x^{3}\\right)dx$"
    in TEXT, "演習1 の英語")
chk("Find $\\displaystyle\\int \\sqrt{4x + 1}\\,dx$" in TEXT, "演習3 の英語")
chk("Find $\\displaystyle\\int \\left(6\\sqrt{x}" not in TEXT,
    "例題1 と同型だった演習1 が消えている")
chk("Find $\\displaystyle\\int \\left(2e^{x} + 4\\sin x\\right)dx$" not in TEXT,
    "分かれていた演習3 が消えている")
chk("**検算（規則を $2$ つ使う）。**" in TEXT, "演習3: 規則を 2 つ")

# --- M7: 循環していた検算 -------------------------------------------------
chk("**検算（$x < 0$ でも）。**" in TEXT, "例題2: x<0 の検算")
chk("**検算（絶対値）。** 定義域が指定されていないので" not in TEXT,
    "言いかえだった検算が消えている（例題2）")
chk("**検算（定数を足しても）。**" in TEXT, "例題2: 定数を足しても")
chk("**検算（$+C$）。** 不定積分なので $+C$ が要ります" not in TEXT,
    "言いかえだった検算が消えている（+C）")
chk("**検算（中身を落としたら）。**" in TEXT, "例題3: 中身を落としたら")
chk("**検算（中身は写すだけ）。**" not in TEXT, "言いかえだった検算が消えている（例題3）")
chk("**検算（展開して最高次だけ見て）。**" in TEXT, "演習7: 最高次で確かめる")
chk("**検算（展開しなくてよい）。**" not in TEXT, "検算でなかった注意が消えている")
chk("**検算（符号を取りちがえたら）。**" in TEXT, "演習6: 符号")
chk("**検算（符号）。** $a$ が負なので、答えの符号も負です" not in TEXT,
    "無条件に偽だった検算が消えている")
eq(R(243, 15), R(81, 5), "演習7 の最高次の係数")
chk(sp.expand((3 * X + 2) ** 5).coeff(X, 5) == 243, "演習7 の 243")
chk(sp.expand((3 * X + 2) ** 4).coeff(X, 4) == 81, "演習7 の 81")

# --- M8: 「だけは」の含み --------------------------------------------------
chk("**$\\dfrac{1}{x}$ は $x^{-1}$ と書けますが、@eq-aasl510a-power は"
    "使えません。**" in TEXT, "第3節: x^{-1} と書ける")
chk("**@eq-aasl510a-ln だけは、@eq-aasl510a-power から出せません。**"
    not in TEXT, "誤解を招く「だけは」が消えている")

# --- M9: 分数の指数の定義域 -------------------------------------------------
chk("$\\dfrac{1}{\\sqrt{x}}$ が使えるのは $x > 0$ のところだけです。" in TEXT,
    "第2節: 1/sqrt(x) の定義域")

# --- M10: Paper の注記 -------------------------------------------------------
chk("## この項目は電卓なしで解きます" in TEXT, "Paper の見出し")
chk("## この項目は Paper 1 でも Paper 2 でも出ます" not in TEXT,
    "brief にない断定が消えている")
chk("Paper 2 でも、まず式を書いてから値を出す問題が出ます" not in TEXT,
    "brief にない断定が消えている（2）")

# --- M11: 見出しと callout の矛盾 ----------------------------------------------
chk("### 1. 標準的な $5$ つの形 {#standard}" in TEXT, "第1節の見出し")
chk("覚えておく $5$ つの形" not in TEXT, "矛盾していた見出しが消えている")

# --- M12: 手順表 ---------------------------------------------------------------
chk("| $5$ | 最後に $+C$ を書く |" in TEXT, "手順表は 5 行")
chk("| $4$ | 合成なら $\\dfrac{1}{a}$ をかけ、最後に $+C$ を書く |" not in TEXT,
    "1/a を二重にかけさせる読み方が消えている")

# --- m1 から m9 ------------------------------------------------------------------
chk("radian（ラジアン）で測った角です" in TEXT, "m1: radian の訳")
chk("**ここで $k$ は定数です。**" in TEXT, "m2: k は定数")
chk("**もとの被積分関数のグラフと、自分の答えを微分したもののグラフ**" in TEXT,
    "m3: 電卓の callout")
chk("**この積分は、SL のどのやり方でも原始関数を書けません。**" in TEXT,
    "m4: cos(x^2) は SL では書けない")
chk("*The student multiplied by $a$ instead of dividing by $a$. Here $a = 2$,"
    in TEXT, "m5: Identify の答案例")
chk("**$x < 0$ と $x > 0$ は、つながっていない $2$ つの区間です。**" in TEXT,
    "m6: 2 つの区間")
chk("微分してもとの式にもどり、**$+C$ が書いてあれば**" in TEXT, "m7: +C の条件")
chk('Headed "Why the integral of 1/x needs |x|"' in TEXT, "m8: 図 (a) の見出し")
chk('Headed "Integrating f dash of a x plus b"' in TEXT, "m8: 図 (b) の見出し")
chk("y = \\int \\frac{4}{2x - 1}\\,dx = 4 \\times \\frac{1}{2}"
    "\\ln\\lvert 2x - 1\\rvert + C" in TEXT, "m9: 例題4 の解答例")

print()
print("OK", OK, "/ NG", NG)
