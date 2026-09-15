# -*- coding: utf-8 -*-
"""AA SL 5.11a のページを検算する。

    python3 figs/aa-sl/check_aasl_5_11a.py
"""
import os
import re

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
QMD = os.path.join(ROOT, "aa-sl", "05-calculus", "aasl-5-11a.qmd")
FIGP = os.path.join(HERE, "make_aasl_5_11a.py")

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
U = sp.Symbol("u")


def dint(f, a, b, v=X):
    return sp.simplify(sp.integrate(f, (v, a, b)))


def anti(f, F, v=X):
    return sp.simplify(sp.diff(F, v) - f) == 0


# ══════════════════════════════════════════════════════════
# 1. ページの骨組み
# ══════════════════════════════════════════════════════════
chk(TEXT.startswith("---\nsidebar: aa-sl\n---\n"), "front matter")
in_text("# SL 5.11a — Definite integrals（定積分） {#sec-aasl-5-11a}", "見出し")

for _h in ("## What you should be able to do", "## The idea",
           "## Why it works", "## Worked examples", "## Common errors",
           "## Exercises"):
    in_text(_h, "節 " + _h)
not_in_text("## Using your GDC", "Topic 5 に GDC の節は置かない")

_secs = re.findall(r"^### (\d)\. .*\{#([a-z0-9-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 8)],
    "### の番号 1..7: %s" % [s[0] for s in _secs])
chk([s[1] for s in _secs] == ["what", "ftc", "bracket", "steps", "props",
                              "sub", "value"],
    "アンカー: %s" % [s[1] for s in _secs])

chk(len(re.findall(r"^\[\d+\]\{\.ex-no\}", TEXT, re.M)) == 10, "演習 10 問")
chk(TEXT.count("::: {#exm-") == 4, "例題 4 つ")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep 9 個")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳 14")
chk(TEXT.count("</details>") == 14, "details 閉じ 14")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例 14")
chk(len(re.findall(r"^---$", TEXT, re.M)) == 6, "行頭 --- は 6 本")
chk(TEXT.count("{.callout-warning}") == 7, "callout-warning 7（誤り 6 + Paper）")
chk(TEXT.count("{.callout-important}") == 0,
    "5.11 の欄にあるのは面積の式だけなので、このページに公式集の callout は"
    "置かない: %d" % TEXT.count("{.callout-important}"))
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

in_text("(img/aasl-5-11a-idea.svg){#fig-aasl511a-idea width=100%}", "図の埋め込み")
in_text("@fig-aasl511a-idea (a)", "図 (a) の参照")
in_text("@fig-aasl511a-idea (b)", "図 (b) の参照")

for _w in ("そのとおり", "もちろん", "簡単です", "自明", "当たり前", "明らか", "当然"):
    not_in_text(_w, "禁止語 " + _w)
for _w in ("得点になりません", "点になりません", "減点されます"):
    not_in_text(_w, "採点の断定 " + _w)

# ページをまたぐ相互参照は使わない（Quarto が解決できない）
chk(not re.search(r"@(eq|tbl|fig)-aasl(?!511a)", TEXT),
    "他ページの @ 参照: %s" % re.findall(r"@(?:eq|tbl|fig)-aasl\w+", TEXT))

# ══════════════════════════════════════════════════════════
# 2. 引用と公式集
# ══════════════════════════════════════════════════════════
_quotes = re.findall(r"^> (.*)$", TEXT, re.M)
chk(_quotes == [], "5.11a に引用してよいシラバス文はない: %s" % _quotes)
in_text("**@eq-aasl511a-ftc は公式集にありません。**", "公式集にない")
in_text("公式集の **5.11** の欄にあるのは面積の式だけで、それは "
        "[SL 5.11b](aasl-5-11b.qmd) で使います。", "5.11 の欄は面積")
not_in_text("この式は公式集にあります", "公式集の callout は置かない")

# ══════════════════════════════════════════════════════════
# 3. 式そのもの
# ══════════════════════════════════════════════════════════
in_text("\\int_{a}^{b} g'(x)\\,dx = g(b) - g(a)\n$$ {#eq-aasl511a-ftc}",
        "基本の式")
in_text("\\int_{a}^{b} f(x)\\,dx = \\bigl[F(x)\\bigr]_{a}^{b} = F(b) - F(a)\n"
        "$$ {#eq-aasl511a-bracket}", "角かっこの式")
in_text("\\int_{b}^{a} f(x)\\,dx = -\\int_{a}^{b} f(x)\\,dx\n"
        "$$ {#eq-aasl511a-swap}", "入れかえの式")
in_text("\\int_{a}^{b} f(x)\\,dx = \\int_{a}^{c} f(x)\\,dx + "
        "\\int_{c}^{b} f(x)\\,dx\n$$ {#eq-aasl511a-split}", "分ける式")
in_text("\\int_{a}^{b} k\\,g'(x)\\,f(g(x))\\,dx = k\\int_{g(a)}^{g(b)} "
        "f(u)\\,du\n$$ {#eq-aasl511a-sub}", "置換の式")
for _r in ("{#tbl-aasl511a-two}", "{#tbl-aasl511a-steps}",
           "{#tbl-aasl511a-props}"):
    in_text(_r, "参照 " + _r)
for _a in ("aasl-5-5.qmd#sum", "aasl-5-5.qmd#power", "aasl-5-5.qmd#expression",
           "aasl-5-6a.qmd#radian", "aasl-5-10a.qmd#standard",
           "aasl-5-10a.qmd#lnabs", "aasl-5-10a.qmd#linear",
           "aasl-5-10a.qmd#rational", "aasl-5-10a.qmd#signs",
           "aasl-5-10b.qmd#spot", "aasl-5-10b.qmd#substitution",
           "aasl-5-11b.qmd"):
    in_text(_a, "参照 " + _a)

# 性質そのもの
_a, _b, _c = sp.symbols("a b c")
_f = sp.Function("f")
_F = sp.Function("F")
chk(sp.simplify((_F(_a) - _F(_b)) + (_F(_b) - _F(_a))) == 0, "入れかえは -1 倍")
chk(sp.simplify((_F(_c) - _F(_a)) + (_F(_b) - _F(_c))
                - (_F(_b) - _F(_a))) == 0, "分けると F(c) が消える")
_CC = sp.Symbol("C")
chk(sp.simplify((_F(_b) + _CC) - (_F(_a) + _CC) - (_F(_b) - _F(_a))) == 0,
    "+C は消える")

# ══════════════════════════════════════════════════════════
# 4. 図
# ══════════════════════════════════════════════════════════
in_fig('"(a) Why $+C$ cancels"', "図 (a) の題")
in_fig('"(b) Three properties of the limits"', "図 (b) の題")
in_fig("both vertical gaps are $F(b) - F(a)$", "図 (a) の注意")
in_fig("shifting the curve up by $C$", "図 (a) の説明")
in_fig("the value of a definite integral can be negative", "図 (b) の注意")
in_fig("swapping:", "図 (b) の入れかえ")
in_fig("equal limits:", "図 (b) の同じ上下")
_figmath = " ".join(re.findall(r"\$([^$]*)\$", FIGCODE))
for _v in ("156", "\\frac{14}{3}", "625", "3x^{2}", "e^{2}"):
    chk(_v not in _figmath, "図の数式に具体的な数・式 %s は出さない" % _v)
for _bad in ("\\le ", "\\ge ", "\\lvert", "\\rvert", "\\begin{pmatrix}",
             "\\bigl", "\\bigr", "\\Box"):
    chk(_bad not in FIGCODE, "図に mathtext が読めない記法: " + _bad)

# ══════════════════════════════════════════════════════════
# 5. 例題
# ══════════════════════════════════════════════════════════
# 例題1
_F1 = X ** 3 - 2 * X ** 2 + X
chk(anti(3 * X ** 2 - 4 * X + 1, _F1), "例題1 の原始関数")
eq(_F1.subs(X, 3), 12, "例題1 F(3)")
eq(_F1.subs(X, 1), 0, "例題1 F(1)")
eq(dint(3 * X ** 2 - 4 * X + 1, 1, 3), 12, "例題1 の値")
eq(27 - 18 + 3, 12, "例題1 の代入 1")
eq(1 - 2 + 1, 0, "例題1 の代入 2")
in_text("\\Bigl[x^{3} - 2x^{2} + x\\Bigr]_{1}^{3}", "例題1 の角かっこ")

# 例題2
eq(dint(sp.cos(X), 0, sp.pi / 2), 1, "例題2(a) の値")
eq(dint(1 / X, 1, sp.E), 1, "例題2(b) の値")
eq(sp.sin(sp.pi / 2), 1, "例題2(a) sin(pi/2)")
eq(sp.log(sp.E), 1, "例題2(b) ln e")
eq(sp.log(1), 0, "例題2(b) ln 1")
in_text("\\Bigl[\\sin x\\Bigr]_{0}^{\\frac{\\pi}{2}} = 1 - 0 = 1", "例題2(a) の答え")
in_text("\\Bigl[\\ln x\\Bigr]_{1}^{e} = 1 - 0 = 1", "例題2(b) の答え")

# 例題3
eq(dint(2 * X * (X ** 2 + 1) ** 3, 0, 2), 156, "例題3 の値")
eq(dint(U ** 3, 1, 5, U), 156, "例題3 の u の積分")
eq(dint(U ** 3, 0, 2, U), 4, "例題3 でまちがえると 4")
eq(5 ** 4, 625, "例題3 の 5^4")
eq(R(625, 4) - R(1, 4), 156, "例題3 の引き算")
eq(((X ** 2 + 1) ** 4 / 4).subs(X, 2) - ((X ** 2 + 1) ** 4 / 4).subs(X, 0),
   156, "例題3 を x にもどしても同じ")
in_text("\\int_{1}^{5} u^{3}\\,du = \\left[\\frac{u^{4}}{4}\\right]_{1}^{5}",
        "例題3 の u の式")

# 例題4
eq(7 - 3, 4, "例題4(a)")
eq(3 + 4, 7, "例題4(a) の検算")
eq(3 * 7, 21, "例題4(c)")
in_text("\\int_{2}^{4} f(x)\\,dx = 4", "例題4(a) の答え")
in_text("\\int_{4}^{1} f(x)\\,dx = -7", "例題4(b) の答え")
in_text("\\int_{1}^{4} 3f(x)\\,dx = 3 \\times 7 = 21", "例題4(c) の答え")

# ══════════════════════════════════════════════════════════
# 6. 演習
# ══════════════════════════════════════════════════════════
eq(dint(X ** 2 + 1, 0, 2), R(14, 3), "演習1")
eq(R(8, 3) + 2, R(14, 3), "演習1 の足し算")
chk(abs(float(R(14, 3)) - 4.67) < 0.005, "演習1 は約 4.67")
in_text("\\frac{14}{3}", "演習1 の答え")

eq(dint(4 / X ** 2, 1, 2), 2, "演習2")
eq(-2 - (-4), 2, "演習2 の引き算")
in_text("\\left[-\\frac{4}{x}\\right]_{1}^{2}", "演習2 の角かっこ")

eq(dint(sp.sin(X), sp.pi, 3 * sp.pi / 2), -1, "演習3")
eq(sp.cos(3 * sp.pi / 2), 0, "演習3 cos(3pi/2)")
eq(sp.cos(sp.pi), -1, "演習3 cos(pi)")
eq(0 - 1, -1, "演習3 の引き算")
chk(all(sp.sin(_t) <= 0 for _t in (sp.pi, 5 * sp.pi / 4, 3 * sp.pi / 2)),
    "演習3 の区間で sin は 0 以下")
chk(abs(float(sp.pi / 2) - 1.57) < 0.005, "演習3 の区間の幅は約 1.57")
in_text("\\Bigl[-\\cos x\\Bigr]_{\\pi}^{\\frac{3\\pi}{2}}", "演習3 の角かっこ")

eq(dint(sp.exp(2 * X), 0, 1), (sp.E ** 2 - 1) / 2, "演習4")
chk(abs(float((sp.E ** 2 - 1) / 2) - 3.19) < 0.005, "演習4 は約 3.19")
chk(abs(float(sp.E ** 2) - 7.39) < 0.005, "e^2 は約 7.39")
in_text("\\frac{e^{2} - 1}{2}", "演習4 の答え")

_f5 = (X ** 2 + 1) / sp.sqrt(X)
_F5 = R(2, 5) * X ** R(5, 2) + 2 * X ** R(1, 2)
chk(anti(_f5, _F5), "演習5 の原始関数")
eq(dint(_f5, 1, 4), R(72, 5), "演習5 の値")
eq(sp.Integer(4) ** R(5, 2), 32, "演習5 の 4^(5/2)")
eq(R(2, 5) * 32, R(64, 5), "演習5 の上端")
eq(R(64, 5) + 4 - (R(2, 5) + 2), R(72, 5), "演習5 の引き算")
in_text("\\left[\\frac{2}{5}x^{\\frac{5}{2}} + 2x^{\\frac{1}{2}}\\right]_{1}^{4}",
        "演習5 の角かっこ")
in_text("x^{\\frac{3}{2}} + x^{-\\frac{1}{2}}", "演習5 の書き直し")

eq(dint(3 * X ** 2 * (X ** 3 + 1) ** 2, 0, 1), R(7, 3), "演習6")
eq(dint(U ** 2, 1, 2, U), R(7, 3), "演習6 の u の積分")
eq(R(8, 3) - R(1, 3), R(7, 3), "演習6 の引き算")
in_text("\\int_{1}^{2} u^{2}\\,du", "演習6 の u の式")

eq(12 - 5, 7, "演習7 の 1 つめ")
eq(5 + 7, 12, "演習7 の検算")
in_text("\\int_{3}^{5} f(x)\\,dx = 7", "演習7 の答え")
in_text("\\int_{5}^{0} f(x)\\,dx = -12", "演習7 の 2 つめ")

_F8 = X ** 3 - X ** 2
chk(anti(3 * X ** 2 - 2 * X, _F8), "演習8 の原始関数")
eq(dint(3 * X ** 2 - 2 * X, -1, 2), 6, "演習8 の値")
eq(_F8.subs(X, 2), 4, "演習8 F(2)")
eq(_F8.subs(X, -1), -2, "演習8 F(-1)")
eq(4 - (-2), 6, "演習8 の引き算")
in_text("\\Bigl[x^{3} - x^{2}\\Bigr]_{-1}^{2}", "演習8 の角かっこ")

# 演習9
eq(dint(2 * X * (X ** 2 - 1) ** 2, 1, 2), 9, "演習9 の正しい値")
eq(dint(U ** 2, 0, 3, U), 9, "演習9 の u の積分")
eq(dint(U ** 2, 1, 2, U), R(7, 3), "演習9 の生徒の値")
eq(R(2 ** 3, 3) - R(1, 3), R(7, 3), "演習9 の生徒の計算")
chk((2 * X * (X ** 2 - 1) ** 2).subs(X, 2) == 36, "演習9 の最大は 36")
eq(((X ** 2 - 1) ** 3 / 3).subs(X, 2) - ((X ** 2 - 1) ** 3 / 3).subs(X, 1),
   9, "演習9 を x にもどしても同じ")
in_text("the limits $1$ and $2$ are values of $x$, not of $u$", "演習9 の答え")

# 演習10
eq(dint(2 * X, 1, 3), 8, "演習10 の値")
eq(9 - 1, 8, "演習10 の引き算")
in_text("*a definite integral is a number, so the answer must not contain "
        "$x$ or $C$*", "演習10 の答え")

# ══════════════════════════════════════════════════════════
# 7. 答えを本文に出していないか
# ══════════════════════════════════════════════════════════
for _v in ("= 12", "156", "\\frac{14}{3}", "\\frac{7}{3}",
           "\\frac{e^{2} - 1}{2}", "= 21", "= -7"):
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

# --- B1: 区間全体で定義されていることが要る ------------------------------
chk("**この式が使えるのは、$a \\leq x \\leq b$ の全体で被積分関数が定義され、"
    "値が途切れていないときだけです。**" in TEXT, "第2節: 定義域の条件")
chk("$\\left[-\\dfrac{1}{x}\\right]_{-1}^{1} = -1 - 1 = -2$" in TEXT,
    "第2節: 反例")
chk("**どの性質も、$a$ と $b$（と $c$）をふくむ区間全体で被積分関数が定義されて"
    "いるときの話です**" in TEXT, "第5節: 定義域の条件")
chk("## 区間の中に、定義されない点があるまま角かっこを当てる" in TEXT,
    "Common errors: 定義されない点")
chk("## 三角関数の角を度で計算する" not in TEXT, "5.6a の再掲が消えている")
# 1/x^2 は正なのに、角かっこをそのまま当てると負になる
chk((1 / X ** 2).subs(X, R(1, 2)) > 0 and (1 / X ** 2).subs(X, -R(1, 2)) > 0,
    "1/x^2 は正")
eq((-1 / X).subs(X, 1) - (-1 / X).subs(X, -1), -2, "反例の -2")

# --- B2: 「積分すると g にもどる」は偽だった -------------------------------
chk("その $g'$ を $a$ から $b$ まで積分しても、$g$ そのものが出てくるわけでは"
    "ありません" in TEXT, "第2節: g にはもどらない")
chk("それをまた積分すると $g$ にもどります" not in TEXT, "偽の主張が消えている")

# --- B3: 例題1 の見積もりが偽だった -----------------------------------------
chk("だから値は $0 \\times 2 = 0$ 以上 $16 \\times 2 = 32$ 以下になります ✓"
    in TEXT, "例題1: 幅をかけた見積もり")
chk("答えの $12$ は、その範囲におさまっています。" not in TEXT,
    "偽の見積もりが消えている")
eq(16 * 2, 32, "例題1 の上限")
chk(0 <= 12 <= 32, "例題1 の 12 は 0 と 32 の間")

# --- M1: 演習9 が例題3 と同じ積分だった ---------------------------------------
chk("A student calculates $\\displaystyle\\int_{1}^{2} 2x\\left(x^{2} - 1"
    "\\right)^{2}dx$" in TEXT, "演習9 の英語")
chk("A student calculates $\\displaystyle\\int_{0}^{2} 2x\\left(x^{2} + 1"
    "\\right)^{3}dx$" not in TEXT, "例題3 と同じだった演習9 が消えている")

# --- M2 + M4: 演習10 が Why it works の写しだった ------------------------------
chk("A student writes $\\displaystyle\\int_{1}^{3} 2x\\,dx = x^{2} + C$."
    in TEXT, "演習10 の英語")
chk("Explain why the constant of integration is not needed" not in TEXT,
    "Why it works の写しだった演習10 が消えている")
chk("生徒が書いたのは不定積分の答えです" in TEXT, "演習10: 不定積分と定積分のちがい")
chk("**(d)** 分ける性質は、$F(c)$ が打ち消し合うことから出るものです。" in TEXT,
    "例題4(d): その場で理由を書く")
chk("（[Why it works](#why-it-works)）" not in TEXT,
    "答えを取りに行かせるリンクが消えている")

# --- M3: 値が負になる演習を入れた -----------------------------------------------
chk("Find the value of $\\displaystyle\\int_{\\pi}^{\\frac{3\\pi}{2}} \\sin x\\,dx$."
    in TEXT, "演習3 の英語")
chk("**検算（符号）。** $\\pi \\leq x \\leq \\dfrac{3\\pi}{2}$ で $\\sin x \\leq 0$ "
    "なので、値が負になるのは正しいことです ✓" in TEXT, "演習3: 負の値")

# --- M5: 上下が同じなら 0 を使わせる ---------------------------------------------
chk("$\\displaystyle\\int_{3}^{3} f(x)\\,dx$ を求めなさい。" in TEXT,
    "演習7: 上下が同じ")
chk("$$\\int_{3}^{3} f(x)\\,dx = 0$$" in TEXT, "演習7 の答え")
chk("**検算（上下が同じ）。**" in TEXT, "演習7 の検算")

# --- M6: 循環していた検算 ----------------------------------------------------------
chk("**検算（当てはまる $f$ を $1$ つ作って）。**" in TEXT, "例題4: 具体的な f")
chk("**検算（(b) の符号）。** $-7$ と $7$ で、大きさが同じです" not in TEXT,
    "言いかえだった検算が消えている（例題4）")
chk("**検算（(c) の大きさ）。** $3$ 倍しているので" not in TEXT,
    "言いかえだった検算が消えている（例題4 c）")
chk("**検算（分けても同じ）。**" in TEXT, "例題1: 分けても同じ")
chk("**検算（引く順番）。** 上端の $12$ から" not in TEXT,
    "言いかえだった検算が消えている（例題1）")
chk("**検算（別の道で）。**" in TEXT, "演習7: 別の道で")
chk("**検算（$f$ を知らなくてよい）。**" not in TEXT,
    "言いかえだった検算が消えている（演習7）")
chk("**検算（下端の値）。**" in TEXT, "演習1 の検算")
# 例題4 の検算に使う f は、与えられた 2 つの値を満たす
_ff = -R(2, 3) * X + 4
eq(dint(_ff, 1, 4), 7, "例題4 の f は 7")
eq(dint(_ff, 1, 2), 3, "例題4 の f は 3")
eq(dint(_ff, 2, 4), 4, "例題4 の f で (a)")
eq(dint(_ff, 4, 1), -7, "例題4 の f で (b)")
eq(dint(3 * _ff, 1, 4), 21, "例題4 の f で (c)")
# 例題1 を x = 2 で分けた検算
_FF1 = X ** 3 - 2 * X ** 2 + X
eq(_FF1.subs(X, 2), 2, "例題1 F(2)")
eq((_FF1.subs(X, 2) - _FF1.subs(X, 1))
   + (_FF1.subs(X, 3) - _FF1.subs(X, 2)), 12, "例題1 を分けても 12")
# 演習7 の別の道
eq(-7 + (-5), -12, "演習7 の別の道")

# --- M7: 演習5 が例題2(b) の言いかえだった ------------------------------------------
chk("Find the value of $\\displaystyle\\int_{1}^{4} \\frac{x^{2} + 1}"
    "{\\sqrt{x}}\\,dx$." in TEXT, "演習5 の英語")
chk("Find the value of $\\displaystyle\\int_{1}^{e^{2}} \\frac{1}{x}\\,dx$."
    not in TEXT, "例題2(b) の言いかえだった演習5 が消えている")

# --- m1 から m11 ----------------------------------------------------------------------
chk("**$a$ を lower limit（下端）、$b$ を upper limit（上端）といいます。**"
    in TEXT, "m1: 用語の順")
chk("radian（ラジアン）" in TEXT, "m2: radian の訳")
chk("\\int_{a}^{b}\\bigl(f(x) + g(x)\\bigr)dx = \\int_{a}^{b} f(x)\\,dx + "
    "\\int_{a}^{b} g(x)\\,dx" in TEXT, "m3: 和の式")
chk("| 区間を分けられる | $\\displaystyle\\int_{a}^{b} f(x)\\,dx = "
    "\\int_{a}^{c} f(x)\\,dx + \\int_{c}^{b} f(x)\\,dx$ |" in TEXT,
    "m4: 表の略記をやめた")
chk("$\\int_{1}^{4} f = \\int_{1}^{2} f + \\int_{2}^{4} f$" not in TEXT,
    "略記が消えている")
chk("= \\sin\\frac{\\pi}{2} - \\sin 0 = 1 - 0 = 1" in TEXT, "m5: 例題2(a) の代入")
chk("= \\ln e - \\ln 1 = 1 - 0 = 1" in TEXT, "m5: 例題2(b) の代入")
chk("\\int_{1}^{2} \\frac{4}{x^{2}}\\,dx = \\int_{1}^{2} 4x^{-2}\\,dx" in TEXT,
    "m6: 演習2 は与えられた式から")
chk("$x = 0$ をふくむ区間だと $-\\dfrac{4}{x}$ が定義されない点が" in TEXT,
    "m7: 演習2 の検算")
chk("Two double-headed arrows drawn to the right of the curves" in TEXT,
    "m8: 図の alt の矢印の位置")
chk("（@fig-aasl511a-idea (b) の下の注記）" in TEXT, "m9: 図 (b) の注記への参照")
chk("$F(b)$ が $F(a)$ より小さければ、$F(b) - F(a)$ は負です" in TEXT,
    "m11: 第7節の書き方")
chk("$f(x) < 0$ の範囲があると、その分が引かれるからです。" not in TEXT,
    "面積に寄っていた文が消えている")

print()
print("OK", OK, "/ NG", NG)
