# -*- coding: utf-8 -*-
"""AA SL 5.6a のページを検算する。

    python3 figs/aa-sl/check_aasl_5_6a.py
"""
import os
import re

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
QMD = os.path.join(ROOT, "aa-sl", "05-calculus", "aasl-5-6a.qmd")
FIGP = os.path.join(HERE, "make_aasl_5_6a.py")

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
Z = sp.Symbol("z", real=True)


def d(f, v=None):
    return sp.simplify(sp.diff(f, v if v is not None else X))


def same(a, b):
    return sp.simplify(sp.nsimplify(a) - sp.nsimplify(b)) == 0


# ══════════════════════════════════════════════════════════
# 1. ページの骨組み
# ══════════════════════════════════════════════════════════
chk(TEXT.startswith("---\nsidebar: aa-sl\n---\n"), "front matter")
in_text("# SL 5.6a — Standard derivatives and the chain rule"
        "（標準的な導関数と連鎖律） {#sec-aasl-5-6a}", "見出し")

for _h in ("## What you should be able to do", "## The idea",
           "## Why it works", "## Worked examples", "## Common errors",
           "## Exercises"):
    in_text(_h, "節 " + _h)
not_in_text("## Using your GDC", "Topic 5 に GDC の節は置かない")

_secs = re.findall(r"^### (\d)\. .*\{#([a-z0-9-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 8)],
    "### の番号 1..7: %s" % [s[0] for s in _secs])
chk([s[1] for s in _secs] == ["rational", "standard", "radian", "sum",
                             "composite", "chain", "order"],
    "アンカー: %s" % [s[1] for s in _secs])

chk(len(re.findall(r"^\[\d+\]\{\.ex-no\}", TEXT, re.M)) == 10, "演習 10 問")
chk(TEXT.count("::: {#exm-") == 4, "例題 4 つ")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep 9 個")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳 14")
chk(TEXT.count("</details>") == 14, "details 閉じ 14")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例 14")
chk(len(re.findall(r"^---$", TEXT, re.M)) == 6, "行頭 --- は 6 本")
chk(TEXT.count("{.callout-warning}") == 7, "callout-warning 7（誤り 6 + Paper）")
chk(TEXT.count("{.callout-important}") == 3,
    "callout-important 3（公式集 5.3 の 1 つ + 5.6 の 2 つ）")
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
chk(len(_qs) == 5, "Explain 系の問いは 5: %d" % len(_qs))

for _i, _m in enumerate(re.findall(r"\{\.model-answer\}(.*?):::", TEXT, re.S), 1):
    _b = _m.replace("**試験ではこう書く**", "")
    chk(len(_b.split()) <= 115, "model answer %d は 115 語以内" % _i)
    chk(not [c for c in _b if "぀" <= c <= "ヿ" or "一" <= c <= "鿿"],
        "model answer %d に日本語がない" % _i)

in_text("(img/aasl-5-6a-idea.svg){#fig-aasl56a-idea width=100%}", "図の埋め込み")
in_text("@fig-aasl56a-idea (a)", "図 (a) の参照")
in_text("@fig-aasl56a-idea (b)", "図 (b) の参照")

for _w in ("そのとおり", "もちろん", "簡単です", "自明", "当たり前", "明らか", "当然"):
    not_in_text(_w, "禁止語 " + _w)
for _w in ("得点になりません", "点になりません", "減点されます"):
    not_in_text(_w, "採点の断定 " + _w)

# ══════════════════════════════════════════════════════════
# 2. 引用と公式集
# ══════════════════════════════════════════════════════════
_quotes = re.findall(r"^> (.*)$", TEXT, re.M)
chk(_quotes == [], "SL 5.6 にシラバスの引用はない: %s" % _quotes)
in_text("公式集の **5.6** の欄に、*Derivative of $\\sin x$*", "公式集 5.6 標準")
in_text("公式集の **5.6** の欄に、*Chain rule* として", "公式集 5.6 連鎖律")
in_text("公式集の **5.3** の欄に、*Derivative of $x^{n}$* として "
        "@eq-aasl56a-power が印刷されています。", "べき乗は 5.3 の欄")
in_text("**この規則は公式集にありません。**", "和と定数倍は公式集にない")
in_text("**@eq-aasl56a-chain2 は公式集にありません。**", "書きかえは公式集にない")

for _r in ("{#eq-aasl56a-power}", "{#eq-aasl56a-sum}", "{#eq-aasl56a-chain}",
           "{#eq-aasl56a-chain2}", "{#tbl-aasl56a-root}", "{#tbl-aasl56a-std}",
           "{#tbl-aasl56a-io}", "{#tbl-aasl56a-steps}", "{#tbl-aasl56a-we2}"):
    in_text(_r, "参照 " + _r)
for _a in ("aasl-5-6b.qmd", "aasl-5-3.qmd#power", "aasl-5-3.qmd#sum"):
    in_text(_a, "参照 " + _a)

# ══════════════════════════════════════════════════════════
# 3. 図
# ══════════════════════════════════════════════════════════
in_fig('"(a) A composite function is two steps"', "図 (a) の題")
in_fig('"(b) Which part is the inside?"', "図 (b) の題")
in_fig('"the two rates multiply:"', "図 (a) の説明")
in_fig('"$u$ is the inside"', "図 (b) の説明")
in_fig("the inside is whatever $u$ stands for", "図 (b) の結び")
_figmath = " ".join(re.findall(r"\$([^$]*)\$", FIGCODE))
for _v in ("30x", "3x^{2} + 1", "4x - 3", "2x + 7", "x^{2} + 4", "0.0175"):
    chk(_v not in _figmath, "図の数式に答え %s は出さない" % _v)
for _bad in ("\\le ", "\\ge ", "\\lvert", "\\rvert", "\\begin{pmatrix}",
             "\\bigl", "\\bigr", "\\Box"):
    chk(_bad not in FIGCODE, "図に mathtext が読めない記法: " + _bad)

# ══════════════════════════════════════════════════════════
# 4. 標準的な導関数と根号
# ══════════════════════════════════════════════════════════
eq(sp.sqrt(X) - X ** R(1, 2), 0, "√x = x^{\\frac{1}{2}}")
eq(1 / sp.sqrt(X) - X ** R(-1, 2), 0, "1/√x = x^{-\\frac{1}{2}}")
eq(sp.root(X, 3) - X ** R(1, 3), 0, "3√x = x^{\\frac{1}{3}}")
chk(same(d(sp.sin(X)), sp.cos(X)), "sin の導関数")
chk(same(d(sp.cos(X)), -sp.sin(X)), "cos の導関数")
chk(same(d(sp.exp(X)), sp.exp(X)), "e^x の導関数")
chk(same(d(sp.log(X)), 1 / X), "ln x の導関数")

# 度で測ったときの傾き
_deg = sp.sin(sp.pi * Z / 180)
eq(sp.diff(_deg, Z).subs(Z, 0), sp.pi / 180, "度のときの x=0 での傾き")
chk(abs(float(sp.pi / 180) - 0.0175) < 5e-5, "π/180 ≈ 0.0175")
eq(1 / (sp.pi / 180), 180 / sp.pi, "180/π は π/180 の逆数")

# ══════════════════════════════════════════════════════════
# 5. 例題
# ══════════════════════════════════════════════════════════
# 例題1  3√x
_f1 = 3 * sp.sqrt(X)
chk(same(d(_f1), 3 / (2 * sp.sqrt(X))), "例題1 の導関数")
chk(same(d(_f1), R(3, 2) * X ** R(-1, 2)), "例題1 の指数の形")
eq(R(1, 2) - 1, R(-1, 2), "例題1 の指数")
eq(d(_f1).subs(X, 4), R(3, 4), "例題1 f'(4)")
chk(d(_f1).subs(X, 1) > d(_f1).subs(X, 4), "例題1 f' は減っていく")
in_text("f'(x) = \\frac{3}{2\\sqrt{x}}", "例題1 の答え")

# 例題2  2sin x - 3cos x + e^x
_f2 = 2 * sp.sin(X) - 3 * sp.cos(X) + sp.exp(X)
_g2 = 2 * sp.cos(X) + 3 * sp.sin(X) + sp.exp(X)
chk(same(d(_f2), _g2), "例題2 の導関数")
eq(_g2.subs(X, 0), 3, "例題2 f'(0) = 3")
chk(same(d(_g2), -2 * sp.sin(X) + 3 * sp.cos(X) + sp.exp(X)),
    "例題2 もう 1 回微分")
eq(sp.sin(0), 0, "sin 0")
eq(sp.cos(0), 1, "cos 0")
eq(sp.exp(0), 1, "e^0")
in_text("f'(x) = 2\\cos x + 3\\sin x + e^{x}", "例題2 の答え")

# 例題3  (3x^2+1)^5
_f3 = (3 * X ** 2 + 1) ** 5
chk(same(d(_f3), 30 * X * (3 * X ** 2 + 1) ** 4), "例題3 の導関数")
eq(d(_f3).subs(X, 0), 0, "例題3 x=0 で傾き 0")
chk(_f3.subs(X, 0) < _f3.subs(X, 1), "例題3 x=0 で最小")
chk(_f3.subs(X, 0) < _f3.subs(X, R(1, 2)), "例題3 x=0 で最小（近く）")
eq(d(3 * X ** 2 + 1), 6 * X, "例題3 内側の導関数")
in_text("30x(3x^{2} + 1)^{4}", "例題3 の答え")

# 例題4
_a4 = sp.exp(X ** 2 + 5)
chk(same(d(_a4), 2 * X * sp.exp(X ** 2 + 5)), "例題4(a) の導関数")
_b4 = sp.sin(4 * X - 3)
chk(same(d(_b4), 4 * sp.cos(4 * X - 3)), "例題4(b) の導関数")
_c4 = sp.log(2 * X)
chk(same(d(_c4), 1 / X), "例題4(c) の導関数")
chk(same(_c4, sp.log(2) + sp.log(X)), "例題4(c) 対数法則")
chk(same(d(sp.log(2) + sp.log(X)), 1 / X), "例題4(c) 対数法則から微分")
eq(R(1, 2) * 2, 1, "例題4(c) 2 が打ち消し合う")
eq(d(4 * X - 3), 4, "例題4(b) 内側の導関数")
in_text("f'(x) = 2x\\,e^{x^{2} + 5}", "例題4(a) の答え")
in_text("g'(x) = 4\\cos(4x - 3)", "例題4(b) の答え")

# ══════════════════════════════════════════════════════════
# 6. 演習の答え
# ══════════════════════════════════════════════════════════
_E = [("演習1", X ** R(1, 3), R(1, 3) * X ** R(-2, 3)),
      ("演習2", 1 / sp.sqrt(X), -1 / (2 * X * sp.sqrt(X))),
      ("演習3", 5 * sp.sin(X), 5 * sp.cos(X)),
      ("演習4", sp.exp(X) - sp.log(X), sp.exp(X) - 1 / X),
      ("演習5", (2 * X + 7) ** 4, 8 * (2 * X + 7) ** 3),
      ("演習6", sp.cos(5 * X), -5 * sp.sin(5 * X)),
      ("演習7", sp.exp(2 * X) + sp.sin(3 * X),
       2 * sp.exp(2 * X) + 3 * sp.cos(3 * X)),
      ("演習8", sp.log(X ** 2 + 1), 2 * X / (X ** 2 + 1)),
      ("演習9", sp.sin(4 * X), 4 * sp.cos(4 * X)),
      ("演習10", sp.sqrt(X ** 2 + 4), X / sp.sqrt(X ** 2 + 4))]
for _name, _f, _fp in _E:
    chk(same(d(_f), _fp), "%s の導関数" % _name)

eq(R(1, 3) - 1, R(-2, 3), "演習1 の指数")
eq((R(1, 3) * X ** R(-2, 3)).subs(X, 1), R(1, 3), "演習1 f'(1)")
eq(R(-1, 2) - 1, R(-3, 2), "演習2 の指数")
eq(sp.diff(1 / sp.sqrt(X), X).subs(X, 4), R(-1, 16), "演習2 f'(4)")
chk(sp.diff(1 / sp.sqrt(X), X).subs(X, 1) < 0, "演習2 f' は負")
chk(sp.simplify(-1 / (2 * X * sp.sqrt(X)) - R(-1, 2) * X ** R(-3, 2)) == 0, "演習2 負の指数を消した形")
eq((5 * sp.cos(X)).subs(X, 0), 5, "演習3 x=0")
chk(abs(float(sp.E - 1) - 1.718) < 1e-3, "演習4 f'(1) = e-1 ≈ 1.72")
chk(sp.E - 1 > 0, "演習4 f'(1) > 0")
eq(4 * 2, 8, "演習5 の係数")
_x5 = R(-7, 2)
eq(2 * _x5 + 7, 0, "演習5 x=-3.5 で内側が 0")
eq((8 * (2 * X + 7) ** 3).subs(X, _x5), 0, "演習5 x=-3.5 で傾き 0")
chk(((2 * X + 7) ** 4).subs(X, _x5) < ((2 * X + 7) ** 4).subs(X, 0),
    "演習5 x=-3.5 で最小")
eq((-5 * sp.sin(5 * X)).subs(X, 0), 0, "演習6 x=0 で傾き 0")
chk(sp.cos(0) >= sp.cos(5 * R(1, 10)), "演習6 x=0 で最大")
eq((2 * sp.exp(2 * X) + 3 * sp.cos(3 * X)).subs(X, 0), 5, "演習7 x=0 の値")
chk(sp.diff(sp.exp(2 * X), X).subs(X, 0) > 0, "演習7 e^{2x} の項は増える")
chk(sp.diff(sp.sin(3 * X), X).subs(X, 0) > 0, "演習7 sin(3x) の項は増える")
eq((2 * X / (X ** 2 + 1)).subs(X, 1), 1, "演習8 x=1")
chk((2 * Z / (Z ** 2 + 1)).subs(Z, -1) < 0, "演習8 x<0 では負")
chk(sp.Integer(1) ** 2 + 1 >= 1, "演習8 分母は 1 以上")
eq(sp.Integer(9) + 4, 13, "演習10 先に中を計算する")
eq((X / sp.sqrt(X ** 2 + 4)).subs(X, 0), 0, "演習10 x=0 で傾き 0")
eq(R(1, 2) * 2, 1, "演習10 1/2 × 2x = x の係数")
chk(same(sp.sqrt(X ** 2 + 4), (X ** 2 + 4) ** R(1, 2)), "演習10 指数の形")

# ★ 例題・演習の答えを本文（例題より前）に出していないこと
for _v in ("\\frac{3}{2\\sqrt{x}}", "30x(3x^{2} + 1)^{4}",
           "2x\\,e^{x^{2} + 5}", "4\\cos(4x - 3)", "8(2x + 7)^{3}",
           "-5\\sin(5x)", "2e^{2x} + 3\\cos(3x)",
           "\\frac{2x}{x^{2} + 1}", "\\frac{1}{2x\\sqrt{x}}",
           "\\frac{1}{3}x^{-\\frac{2}{3}}", "5\\cos x",
           "2\\cos x + 3\\sin x", "\\frac{x}{\\sqrt{x^{2} + 4}}",
           "4\\cos(4x)"):
    not_in_body(_v, "答え %s は本文に出さない" % _v)

# ══════════════════════════════════════════════════════════
# 7. ページに書いてある計算を、機械的にたしかめる
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
    if _before.endswith("\\times"):
        continue
    if re.search(r"(\\(?:sin|cos|tan|ln|log|exp|sqrt)|[{^_])$", _before):
        continue
    _vals = [_value(x) for x in _m.group(1).split("=")]
    _nstmt += 1
    chk(len(set(_vals)) == 1,
        "式が合わない: %s  →  %s" % (_m.group(1)[:80], _vals))
chk(_nstmt >= 3, "ページの計算を %d 本たしかめた" % _nstmt)
print("  （計算 %d 本）" % _nstmt)

# ══════════════════════════════════════════════════════════
# 見直し（2026-09）で直したところ。もどってしまわないように。
# ══════════════════════════════════════════════════════════

# --- B1: (3x+1)^4 の導関数に、内側の 3 をかけている ---------------
chk("$3$ 歩目で内側の導関数 $3$ をかけて、"
    "$\\dfrac{d}{dx}(3x+1)^{4} = 12(3x+1)^{3}$ になります。" in TEXT,
    "第7節: 3 をかけた形まで書いている")
chk("$(3x+1)^{4}$ を微分すると $4(3x+1)^{3}$ で" not in TEXT,
    "かけ忘れた式を「微分すると」と書いた文が消えている")
chk(same(d((3 * X + 1) ** 4), 12 * (3 * X + 1) ** 3), "(3x+1)^4 の導関数")

# --- B2: 例題1 の検算が f の増え方になっている ---------------------
chk("✓ $x = 4$ の近くで $f(x) = 3\\sqrt{x}$ は、$x$ が $1$ 増えるあいだに"
    in TEXT, "例題1: 検算は f の増え方")
chk("✓ $x = 4$ の近くで $\\sqrt{x}$ は、$x$ が $1$ 増えるあいだに" not in TEXT,
    "√x の増え方と取りちがえた文が消えている")
chk(abs(float(3 * sp.sqrt(5) - 3 * sp.sqrt(4)) - 0.75) < 0.05,
    "例題1: f(5) - f(4) は 3/4 くらい")
chk(abs(float(sp.sqrt(5) - sp.sqrt(4)) - 0.75) > 0.4,
    "例題1: √x なら 3/4 にはならない")

# --- M1: 演習3 で「なぜラジアンか」を書かせている -------------------
chk("Explain why the answer would be different if $x$ were measured in "
    "degrees." in TEXT, "演習3: 度との違いを説明させている")
chk("**検算（度で測ったら）。**" in TEXT, "演習3: 度のときの検算")
chk("**検算（合成かどうか）。** 内側は $x$ そのものなので、かける数は $1$ です"
    not in TEXT, "演習9 と重なっていた検算が消えている")
_degsin = sp.sin(sp.pi * Z / 180)
chk(sp.simplify(sp.diff(5 * _degsin, Z)
                - sp.pi / 180 * 5 * sp.cos(sp.pi * Z / 180)) == 0,
    "演習3: 度で測ったときの導関数")

# --- M2: 例題2 の検算が、独立に確かめるものになっている --------------
chk("**検算（$-3\\cos x$ の項をグラフで）。**" in TEXT, "例題2: グラフでの検算")
chk("**検算（もう $1$ 回微分してみる）。**" not in TEXT,
    "5.7 に入りこむ検算が消えている")
chk(sp.cos(0) > sp.cos(R(1, 2)), "例題2: cos は x=0 で最も大きい")
chk((3 * sp.sin(X)).subs(X, 0) == 0, "例題2: 3 sin 0 = 0")

# --- M3: 有理数の指数を、実際にたしかめている ----------------------
chk("[SL 5.1](aasl-5-1.qmd#limit) の考え方でたしかめられます。" in TEXT,
    "Why it works: 5.1 の考え方でたしかめる")
chk("分子を有理化して書きなおします。" in TEXT, "Why it works: 有理化")
chk("**ほかの有理数の $n$ については、SL ではたしかめません。**" in TEXT,
    "Why it works: 残りは認めて使うと断っている")
chk("結果としてそうなるからです。" not in TEXT, "理由になっていない一文が消えている")
chk("両辺を微分する方法は AHL の内容なので" not in TEXT,
    "問いを言いかえただけの説明が消えている")
_h = sp.Symbol("h", positive=True)
chk(sp.simplify((sp.sqrt(X + _h) - sp.sqrt(X)) / _h
                - 1 / (sp.sqrt(X + _h) + sp.sqrt(X))) == 0,
    "Why it works: 有理化した式が等しい")
chk(sp.simplify(sp.limit((sp.sqrt(X + _h) - sp.sqrt(X)) / _h, _h, 0)
                - 1 / (2 * sp.sqrt(X))) == 0, "Why it works: 極限は 1/(2√x)")
chk(sp.simplify(1 / (2 * sp.sqrt(X)) - R(1, 2) * X ** R(-1, 2)) == 0,
    "Why it works: 1/(2√x) は (1/2)x^{-\\frac{1}{2}}")

# --- M4: 演習2 が 1/√x になっている -------------------------------
chk("f(x) = \\dfrac{1}{\\sqrt{x}}$, for $x > 0$" in TEXT, "演習2: 1/√x")
chk("f(x) = 4\\sqrt{x}$, for $x > 0$" not in TEXT,
    "例題1 と同じだった演習2 が消えている")
chk("-\\frac{1}{2x\\sqrt{x}}" in TEXT, "演習2 の答え")

# --- M5: 内側の見分け方が本文にある --------------------------------
chk("**迷ったら、数を入れてみてください。**" in TEXT, "第5節: 数を入れて決める")
chk("**先に計算するほうが内側**です。" in TEXT, "第5節: 先に計算するほうが内側")

# --- M6: 演習7 が和と連鎖律の組み合わせ ----------------------------
chk("y = e^{2x} + \\sin(3x)$, where $x$ is in radians" in TEXT,
    "演習7: 和と連鎖律")
chk("y = e^{3x^{2}}$. Find" not in TEXT, "例題4(a) と同型だった演習7 が消えている")
chk("2e^{2x} + 3\\cos(3x)" in TEXT, "演習7 の答え")

# --- m1: 定数倍の参照先 -------------------------------------------
chk("**定数倍はそのまま残ります**（[SL 5.3](aasl-5-3.qmd#constant)）。" in TEXT,
    "第4節: 定数倍は #constant")
chk("定数倍はそのまま残ります（[SL 5.3](aasl-5-3.qmd#sum)）。" not in TEXT,
    "誤った参照先が消えている")

# --- m3: Δx を定義している ----------------------------------------
chk("それぞれの変わり方を $\\Delta x$（$= h$）、$\\Delta u$、$\\Delta y$ と書くと"
    in TEXT, "Why it works: Δx の定義")
chk("その結果 $y$ も少し増えます。" not in TEXT, "増えるとは限らない文が消えている")

# --- m4: 例題4 の検算の順 ------------------------------------------
chk(TEXT.index("**検算（(b) の内側）。**") < TEXT.index("**検算（(c) を対数法則で）。**"),
    "例題4: 検算の順が (a)(b)(b)(c)")

# --- m5: 例題4 の柱書き -------------------------------------------
chk("Differentiate each of the following. Where an angle appears, $x$ is in "
    "radians." in TEXT, "例題4 の柱書き")

# --- m7: 第3節の結び -----------------------------------------------
chk("**導関数に角を入れるときも、ラジアンの値を入れます**" in TEXT,
    "第3節: 導関数に入れる角もラジアン")
chk("**答えの角も、ラジアンで書きます**" not in TEXT,
    "このページに出てこない話が消えている")

# --- m8: SL 2.5 への参照 -------------------------------------------
chk("[SL 2.5](../02-functions/aasl-2-5.qmd#order)" in TEXT, "第5節: SL 2.5 へ")

# --- m9: 折りたたみの見出し ----------------------------------------
chk("## 電卓が使えるときは、こう確かめます" in TEXT, "電卓の節の見出し")
chk("## Paper 2 では、電卓でこう確かめます" not in TEXT,
    "Paper 2 に出ると読める見出しが消えている")

print()
print("OK", OK, "/ NG", NG)
