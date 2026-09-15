# -*- coding: utf-8 -*-
"""AA SL 5.3 のページを検算する。

    python3 figs/aa-sl/check_aasl_5_3.py
"""
import os
import re

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
QMD = os.path.join(ROOT, "aa-sl", "05-calculus", "aasl-5-3.qmd")
FIGP = os.path.join(HERE, "make_aasl_5_3.py")

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
K = sp.Symbol("k")


def d(e):
    return sp.simplify(sp.diff(sp.expand(sp.together(e)), X))


# ══════════════════════════════════════════════════════════
# 1. ページの骨組み
# ══════════════════════════════════════════════════════════
chk(TEXT.startswith("---\nsidebar: aa-sl\n---\n"), "front matter")
in_text("# SL 5.3 — Differentiating $ax^{n}$（べき乗の微分） {#sec-aasl-5-3}",
        "見出し")

for _h in ("## What you should be able to do", "## The idea",
           "## Why it works", "## Worked examples", "## Common errors",
           "## Exercises"):
    in_text(_h, "節 " + _h)
not_in_text("## Using your GDC", "Topic 5 に GDC の節は置かない")

_secs = re.findall(r"^### (\d)\. .*\{#([a-z0-9-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 8)],
    "### の番号 1..7: %s" % [s[0] for s in _secs])
chk([s[1] for s in _secs] == ["power", "constant", "sum", "zeroderiv",
                              "negative", "rewrite", "evaluate"],
    "アンカー: %s" % [s[1] for s in _secs])

chk(len(re.findall(r"^\[\d+\]\{\.ex-no\}", TEXT, re.M)) == 10, "演習 10 問")
chk(TEXT.count("::: {#exm-") == 4, "例題 4 つ")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep 9 個")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳 14")
chk(TEXT.count("</details>") == 14, "details 閉じ 14")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例 14")
chk(len(re.findall(r"^---$", TEXT, re.M)) == 6, "行頭 --- は 6 本")
chk(TEXT.count("{.callout-warning}") == 7, "callout-warning 7（誤り 6 + Paper 1）")
chk(TEXT.count("{.callout-important}") == 1,
    "callout-important 1（公式集 5.3 の x^n）")
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
chk(len(_qs) == 6, "Explain 系の問いは 6: %d" % len(_qs))

for _i, _m in enumerate(re.findall(r"\{\.model-answer\}(.*?):::", TEXT, re.S), 1):
    _b = _m.replace("**試験ではこう書く**", "")
    chk(len(_b.split()) <= 115, "model answer %d は 115 語以内" % _i)
    chk(not [c for c in _b if "぀" <= c <= "ヿ" or "一" <= c <= "鿿"],
        "model answer %d に日本語がない" % _i)

in_text("(img/aasl-5-3-idea.svg){#fig-aasl53-idea width=100%}", "図の埋め込み")
in_text("@fig-aasl53-idea (a)", "図 (a) の参照")
in_text("@fig-aasl53-idea (b)", "図 (b) の参照")

for _w in ("そのとおり", "もちろん", "簡単です", "自明", "当たり前", "明らか", "当然"):
    not_in_text(_w, "禁止語 " + _w)
for _w in ("得点になりません", "点になりません", "減点されます"):
    not_in_text(_w, "採点の断定 " + _w)

# ══════════════════════════════════════════════════════════
# 2. 引用と公式集
# ══════════════════════════════════════════════════════════
_quotes = re.findall(r"^> (.*)$", TEXT, re.M)
chk(_quotes == [], "5.3 でシラバスの引用は使わない: %s" % _quotes)
in_text("公式集の **5.3** の欄に、*Derivative of $x^{n}$* として", "公式集 5.3")
in_text("**@eq-aasl53-const は公式集にありません。**", "定数倍は公式集にない")
in_text("**この規則も公式集にありません。**", "和と差は公式集にない")

in_text("f(x) = x^{n} \\quad \\Longrightarrow \\quad f'(x) = nx^{n-1}\n"
        "$$ {#eq-aasl53-power}", "べき乗の微分の式")
in_text("$$ {#eq-aasl53-const}", "定数倍の式")
in_text("$$ {#eq-aasl53-sum}", "和と差の式")
in_text("$$ {#eq-aasl53-zero}", "定数の微分の式")
in_text("$$ {#eq-aasl53-neg}", "負の指数の式")
in_text("{#tbl-aasl53-neg}", "負の指数の表")
in_text("{#tbl-aasl53-rewrite}", "直し方の表")
in_text("{#tbl-aasl53-we1}", "例題1 の表")
in_text("[SL 5.6a](aasl-5-6a.qmd)", "5.6a への参照（有理数の指数）")
in_text("[SL 5.6b](aasl-5-6b.qmd)", "5.6b への参照（積と商）")
in_text("[SL 5.1](aasl-5-1.qmd#gradfn)", "5.1 への参照")
in_text("[SL 5.2](aasl-5-2.qmd#sign)", "5.2 への参照")
chk(os.path.exists(os.path.join(ROOT, "aa-sl", "01-number-and-algebra",
                                "aasl-1-9.qmd")), "1.9 のファイルがある")

# ══════════════════════════════════════════════════════════
# 3. 図
# ══════════════════════════════════════════════════════════
in_fig('"(a) Two things happen to the power"', "図 (a) の題")
in_fig('"(b) Get it into a sum of powers first"', "図 (b) の題")
in_fig('"1. the old power comes down and multiplies"', "図 (a) の動き 1")
in_fig('"2. the power drops by one"', "図 (a) の動き 2")
in_fig('"a product of brackets", "expand it"', "図 (b) の行 1")
in_fig('"there is no rule yet for a product or a quotient"', "図 (b) の注意")
_figmath = " ".join(re.findall(r"\$([^$]*)\$", FIGCODE))
for _v in ("12", "239", "4x - 5", "2x", "7x^{6}", "15"):
    chk(_v not in _figmath, "図の数式に答え %s は出さない" % _v)
for _bad in ("\\le ", "\\ge ", "\\lvert", "\\rvert", "\\begin{pmatrix}"):
    chk(_bad not in FIGCODE, "図に mathtext が読めない記法: " + _bad)

# ══════════════════════════════════════════════════════════
# 4. 例題
# ══════════════════════════════════════════════════════════
# 例題1  f(x) = 4x^3 - 5x^2 + 7x - 2
_w1 = 4 * X ** 3 - 5 * X ** 2 + 7 * X - 2
eq(d(_w1), 12 * X ** 2 - 10 * X + 7, "例題1 の導関数")
eq(4 * 3, 12, "例題1 の係数 1")
eq(-5 * 2, -10, "例題1 の係数 2")
eq(7 * 1, 7, "例題1 の係数 3")
chk(sp.degree(sp.Poly(_w1, X)) == 3 and
    sp.degree(sp.Poly(d(_w1), X)) == 2, "例題1 次数が 1 下がる")
in_text("f'(x) = 12x^{2} - 10x + 7", "例題1 の答え")

# 例題2  y = 3x^5 - x
_w2 = 3 * X ** 5 - X
eq(d(_w2), 15 * X ** 4 - 1, "例題2 の導関数")
eq(d(_w2).subs(X, 2), 239, "例題2(b) の値")
eq(2 ** 4, 16, "例題2 検算 2^4")
eq(15 * 16, 240, "例題2 検算 15x16")
eq(240 - 1, 239, "例題2 検算 240-1")
chk(d(_w2).subs(X, 2) > 0, "例題2 傾きは正")
in_text("15x^{4} - 1", "例題2 の導関数")
in_text("240 - 1 = 239", "例題2 の値")

# 例題3  f(x) = 2/x^3
_w3 = 2 * X ** -3
eq(d(_w3), -6 * X ** -4, "例題3 の導関数")
eq(d(_w3).subs(X, 1), -6, "例題3(b) の値")
eq(2 * -3, -6, "例題3 の係数")
eq(-3 - 1, -4, "例題3 の指数")
for _v in (-2, -1, R(1, 2), 1, 2, 3):
    chk(sp.Integer(_v) ** 4 > 0 if _v == int(_v) else _v ** 4 > 0,
        "4 乗は正: %s" % _v)
    chk(d(_w3).subs(X, _v) < 0, "例題3 f'(%s) < 0" % _v)
eq((-2) ** 4, 16, "例題3 検算 (-2)^4")
in_text("f'(x) = -6x^{-4} = -\\frac{6}{x^{4}}", "例題3 の導関数")

# 例題4  f(x) = (2x+1)(x-3)
_w4 = (2 * X + 1) * (X - 3)
eq(sp.expand(_w4), 2 * X ** 2 - 5 * X - 3, "例題4 の展開")
eq(d(_w4), 4 * X - 5, "例題4 の導関数")
eq(_w4.subs(X, 0), -3, "例題4 検算 f(0)")
eq((2 * X ** 2 - 5 * X - 3).subs(X, 0), -3, "例題4 検算 展開後の f(0)")
eq(d(_w4).subs(X, 0), -5, "例題4 検算 f'(0)")
chk(d(_w4).subs(X, 0) != 2, "例題4 生徒の答え 2 とはちがう")
chk(sp.degree(sp.Poly(d(_w4), X)) == 1, "例題4 導関数は 1 次式")
in_text("f'(x) = 4x - 5", "例題4 の答え")

# ══════════════════════════════════════════════════════════
# 5. 演習の答え
# ══════════════════════════════════════════════════════════
_E = [("演習1", X ** 7, 7 * X ** 6),
      ("演習2", 5 * X ** 3 - 2 * X ** 2 + 9, 15 * X ** 2 - 4 * X),
      ("演習3", 6 * X - 4, sp.Integer(6)),
      ("演習4", 3 * X ** -2, -6 * X ** -3),
      ("演習5", X ** 3 - 12 * X, 3 * X ** 2 - 12),
      ("演習6", (X + 4) * (X - 1), 2 * X + 3),
      ("演習7", (X ** 3 + 2 * X) / X, 2 * X),
      ("演習8", 4 * X ** -1 + 3 * X ** 2, -4 * X ** -2 + 6 * X),
      ("演習10", X ** 5, 5 * X ** 4)]
for _name, _f, _want in _E:
    eq(d(_f), _want, "%s の導関数" % _name)

eq((7 * X ** 6).subs(X, 1), 7, "演習1 検算 f'(1)")
eq(5 * 3, 15, "演習2 係数 1")
eq(-2 * 2, -4, "演習2 係数 2")
eq(sp.expand((X + 4) * (X - 1)), X ** 2 + 3 * X - 4, "演習6 の展開")
eq(((X + 4) * (X - 1)).subs(X, 1), 0, "演習6 検算 f(1)")
eq((X ** 2 + 3 * X - 4).subs(X, 1), 0, "演習6 検算 展開後")
eq(sp.simplify((X ** 3 + 2 * X) / X), X ** 2 + 2, "演習7 の簡単化")
eq(((X ** 3 + 2 * X) / X).subs(X, 2), 6, "演習7 検算 x=2 もとの式")
eq((X ** 2 + 2).subs(X, 2), 6, "演習7 検算 x=2 直した式")
eq((-4 * X ** -2 + 6 * X).subs(X, 1), 2, "演習8 検算 x=1")
eq(4 * -1, -4, "演習8 係数 1")
eq(3 * 2, 6, "演習8 係数 2")
eq((3 * X ** 2 - 12).subs(X, 2), 0, "演習5 f'(2)")
eq((3 * X ** 2 - 12).subs(X, 1), -9, "演習5 検算 f'(1)")
eq((3 * X ** 2 - 12).subs(X, 3), 15, "演習5 検算 f'(3)")
chk(sorted(sp.solve(sp.Eq(3 * X ** 2 - 12, 0), X)) == [-2, 2],
    "演習5 停留点は 2 つ")
# 演習9  f(x) = 2x^3 + kx、f'(1) = 12
_e9 = sp.diff(2 * X ** 3 + K * X, X)
eq(_e9, 6 * X ** 2 + K, "演習9 の導関数")
chk(sp.solve(sp.Eq(_e9.subs(X, 1), 12), K) == [6], "演習9 k = 6")
eq(_e9.subs({X: 1, K: 6}), 12, "演習9 もどすと 12")
# 演習10 の生徒のまちがい
chk(sp.expand(5 * X ** 5) != sp.expand(5 * X ** 4), "演習10 生徒の答えは誤り")
eq((5 * X ** 4).subs(X, 2), 80, "演習10 検算 x=2 正しい答え")
eq((5 * X ** 5).subs(X, 2), 160, "演習10 検算 x=2 生徒の答え")
eq((5 * X ** 4).subs(X, 1), 5, "演習10 x=1 では一致する")
eq((5 * X ** 5).subs(X, 1), 5, "演習10 x=1 では一致する（生徒）")

# ★ 例題・演習の答えを本文（例題より前）に出していないこと
for _v in ("12x^{2} - 10x + 7", "15x^{4}", "239", "4x - 5", "7x^{6}",
           "-6x^{-4}", "-6x^{-3}", "2x + 3", "5x^{4}"):
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

# --- B1: x != 0 の条件を書いている ------------------------------
chk("**$n$ が $0$ 以下の整数のときは、$x \\ne 0$ のところだけです。**" in TEXT,
    "第1節: n <= 0 のときの範囲")
chk("$x^{n}$ も $nx^{n-1}$ も、$x = 0$ では値がありません。" in TEXT,
    "第1節: x=0 では値がない")
chk("\\frac{1}{x^{k}} = x^{-k} \\qquad (x \\ne 0)" in TEXT,
    "第5節: 負の指数の式に条件がついている")
chk("**この等式は $x \\ne 0$ のときのものです。**" in TEXT,
    "第5節: 条件の言いかえ")
chk("**符号を調べるときは、$x > 0$ と $x < 0$ を分けて見てください。**" in TEXT,
    "第5節: 符号は分けて調べる")

# --- B2: 定数の導関数を説明させる問いがある ----------------------
chk("Explain why the constant term does not appear in your answer." in TEXT,
    "演習3: 定数項が消える理由を説明させる")
chk("a constant does not change as $x$ changes, so it contributes nothing to "
    "the rate of change" in TEXT, "演習3 の答え")
chk("**検算（定数を変えてみる）。**" in TEXT, "演習3: 定数を変えた検算")
chk("**検算（定数項）。** $-4$ は消えました" not in TEXT,
    "循環していた検算が消えている")

# --- M1: Why it works の適用範囲 --------------------------------
chk("**ここでの $n$ は正の整数です。**" in TEXT, "Why it works: n は正の整数")
chk("$n$ が負の整数のときに同じ式が成り立つことは、この計算では出せません。"
    in TEXT, "Why it works: 負の指数はこの計算では出ない")

# --- M2: 例題2 の符号の検算 -------------------------------------
chk("$x^{4} > \\dfrac{1}{15}$ のときです。$x = 2$ では $x^{4} = 16$ なので"
    in TEXT, "例題2: 符号の検算が正しい")
chk("$15x^{4} \\geq 0$ なので、$x^{4} > \\dfrac{1}{15}$ ならつねに正です。"
    not in TEXT, "誤った推論の文が消えている")
chk("$x$ が $0$ に近いところでは負になります。" in TEXT,
    "例題2: 0 の近くでは負だと書いている")

# --- M3: 直してよい理由を第6節に書いた ---------------------------
chk("**直してよいのは、直した式ともとの式が同じ関数だからです。**" in TEXT,
    "第6節: 直してよい理由")
chk("$x = 0$ はもとの式にもとから入っていないので、困りません。" in TEXT,
    "第6節: 定義域の話")
chk("for $x \\ne 0$ the two expressions take the same value, so they are the "
    "same function and have the same derivative" in TEXT, "演習7 の答え")
chk("$$f'(x) = 2x, \\qquad x \\ne 0$$" in TEXT, "演習7 の答えに定義域がある")

# --- m1: x^0 = 1 の但し書きと、ax の導関数 ----------------------
chk("$3 \\times 1 \\times x^{0} = 3$ になります（$x^{0} = 1$）。" in TEXT,
    "第2節: x^0 = 1 の但し書き")
chk("**$ax$ の導関数は、$x = 0$ をふくめてどの $x$ でも $a$ です。**" in TEXT,
    "第2節: ax の導関数はどこでも a")

# --- m2: 第6節の参照は eq-aasl53-sum ----------------------------
chk("@eq-aasl53-sum が使えるのは、$ax^{n}$ の**和の形**のときだけです。"
    in TEXT, "第6節の参照")
chk("@eq-aasl53-power が使えるのは、$ax^{n}$ の**和の形**" not in TEXT,
    "まちがった参照が消えている")

# --- m3: ax の話は第2節にあり、リンクもそこを指す -----------------
chk("$ax = ax^{1}$ なので、導関数は $a$ です（[第 2 節](#constant)）。" in TEXT,
    "Common errors のリンクは第2節")
chk("$kx$ の導関数は $k$ です（[第 2 節](#constant)）。" in TEXT,
    "演習9 のリンクは第2節")
chk("**$3x$ の微分は $3$ です。**" in TEXT and
    TEXT.index("**$3x$ の微分は $3$ です。**") < TEXT.index("### 3. 和と差"),
    "3x の話は第2節にある")

# --- m4: 指数の検算のつじつま ------------------------------------
chk("$3$、$2$、$1$ が、$2$、$1$、$0$ に下がっています" in TEXT,
    "例題1: 指数の検算")
chk("（消える）に下がっています" not in TEXT, "つじつまの合わない古い文が消えている")

# --- m5: 中身のない検算を差しかえた ------------------------------
chk("**検算（$x = 2$ で数を入れる）。**" in TEXT, "例題3: 数を入れた検算")
chk("**検算（負の指数にもどす）。**" not in TEXT, "書きかえだけの検算が消えている")
chk("**検算（$y$ の値と混同していないか）。**" in TEXT, "例題2: y と傾きの区別")
chk("**検算（順番）。** 先に $\\dfrac{dy}{dx}$ を求めてから" not in TEXT,
    "手順の言いかえだった検算が消えている")
chk("**検算（もう $1$ つの値で）。** $x = -1$ で" in TEXT, "演習7: 負の x での検算")
chk("**検算（割線の傾きで）。** $x = 2$ から $x = 2.01$ まで" in TEXT,
    "演習10: 割線の傾きで見分ける検算")
chk("**検算（もっと簡単な例で）。** $x^{2}$ の導関数は $2x$" not in TEXT,
    "べき乗の規則でべき乗の規則を確かめる検算が消えている")

# --- m6: 例題4 の検算は x = 1 -----------------------------------
chk("**検算（$1$ つの値で）。** $x = 1$ で $f(1) = (3)(-2) = -6$" in TEXT,
    "例題4: x=1 での検算")
chk("$x = 0$ で $f(0) = (1)(-3) = -3$" not in TEXT,
    "定数項しか見ない検算が消えている")

# --- m7: stationary point の訳を出している ----------------------
chk("$f'(a) = 0$ のとき、その点を **stationary point**（停留点）といいます"
    in TEXT, "第7節: 停留点の訳")
chk(TEXT.index("**stationary point**（停留点）")
    < TEXT.index("## Worked examples"), "訳は The idea の中にある")

# --- m8: 電卓の書き方が検証ずみの範囲 ----------------------------
chk("グラフ画面に $y = f(x)$ をかくと、$x = a$ のあたりで上がっているか"
    in TEXT, "電卓の節: 検証ずみの言い方")
chk("接線の傾きを見れば、求めた $f'(a)$ の見当が付きます。" not in TEXT,
    "検証していない操作の記述が消えている")

print()
print("OK", OK, "/ NG", NG)
