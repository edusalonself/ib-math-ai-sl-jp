# -*- coding: utf-8 -*-
"""AA SL 5.6b のページを検算する。

    python3 figs/aa-sl/check_aasl_5_6b.py
"""
import os
import re

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
QMD = os.path.join(ROOT, "aa-sl", "05-calculus", "aasl-5-6b.qmd")
FIGP = os.path.join(HERE, "make_aasl_5_6b.py")

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


def d(f):
    return sp.simplify(sp.diff(f, X))


def same(a, b):
    return sp.simplify(sp.nsimplify(a) - sp.nsimplify(b)) == 0


# ══════════════════════════════════════════════════════════
# 1. ページの骨組み
# ══════════════════════════════════════════════════════════
chk(TEXT.startswith("---\nsidebar: aa-sl\n---\n"), "front matter")
in_text("# SL 5.6b — The product and quotient rules"
        "（積の微分法と商の微分法） {#sec-aasl-5-6b}", "見出し")

for _h in ("## What you should be able to do", "## The idea",
           "## Why it works", "## Worked examples", "## Common errors",
           "## Exercises"):
    in_text(_h, "節 " + _h)
not_in_text("## Using your GDC", "Topic 5 に GDC の節は置かない")

_secs = re.findall(r"^### (\d)\. .*\{#([a-z0-9-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 8)],
    "### の番号 1..7: %s" % [s[0] for s in _secs])
chk([s[1] for s in _secs] == ["spot", "product", "choose", "quotient",
                             "order", "withchain", "simplify"],
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
    "callout-important 2（公式集 5.6 の積と商）")
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

in_text("(img/aasl-5-6b-idea.svg){#fig-aasl56b-idea width=100%}", "図の埋め込み")
in_text("@fig-aasl56b-idea (a)", "図 (a) の参照")
in_text("@fig-aasl56b-idea (b)", "図 (b) の参照")

for _w in ("そのとおり", "もちろん", "簡単です", "自明", "当たり前", "明らか", "当然"):
    not_in_text(_w, "禁止語 " + _w)
for _w in ("得点になりません", "点になりません", "減点されます"):
    not_in_text(_w, "採点の断定 " + _w)

# ══════════════════════════════════════════════════════════
# 2. 引用と公式集
# ══════════════════════════════════════════════════════════
_quotes = re.findall(r"^> (.*)$", TEXT, re.M)
chk(_quotes == [], "SL 5.6 にシラバスの引用はない: %s" % _quotes)
in_text("公式集の **5.6** の欄に、*Product rule* として @eq-aasl56b-product が"
        "印刷されています。", "公式集 5.6 積")
in_text("公式集の **5.6** の欄に、*Quotient rule* として @eq-aasl56b-quotient が"
        "印刷されています。", "公式集 5.6 商")
in_text("**@eq-aasl56b-wrong の左辺が、書きまちがえたときの形です。**",
        "逆順は書きまちがえの形")

for _r in ("{#eq-aasl56b-product}", "{#eq-aasl56b-quotient}",
           "{#eq-aasl56b-wrong}", "{#tbl-aasl56b-which}", "{#tbl-aasl56b-io}",
           "{#tbl-aasl56b-steps}"):
    in_text(_r, "参照 " + _r)
for _a in ("aasl-5-6a.qmd#chain", "aasl-5-6a.qmd#sum", "aasl-5-6a.qmd#standard",
           "aasl-5-6a.qmd#radian", "aasl-5-3.qmd#rewrite"):
    in_text(_a, "参照 " + _a)

# 公式集の形（逐語）
in_text("\\frac{dy}{dx} = u\\frac{dv}{dx} + v\\frac{du}{dx}\n"
        "$$ {#eq-aasl56b-product}", "積の微分法の式")
in_text("\\frac{dy}{dx} = \\frac{v\\dfrac{du}{dx} - u\\dfrac{dv}{dx}}{v^{2}}\n"
        "$$ {#eq-aasl56b-quotient}", "商の微分法の式")

# ══════════════════════════════════════════════════════════
# 3. 図
# ══════════════════════════════════════════════════════════
in_fig('"(a) The product rule: one factor at a time"', "図 (a) の題")
in_fig('"(b) The quotient rule: the order does matter"', "図 (b) の題")
in_fig('"keep $u$, differentiate $v$"', "図 (a) の説明 1")
in_fig('"keep $v$, differentiate $u$"', "図 (a) の説明 2")
in_fig('"this term comes first"', "図 (b) の説明 1")
in_fig('"minus, not plus"', "図 (b) の説明 2")
in_fig('"the bottom, squared"', "図 (b) の説明 3")
_figmath = " ".join(re.findall(r"\$([^$]*)\$", FIGCODE))
for _v in ("x^{3}", "e^{3x}", "\\sin", "\\cos", "\\ln", "1 - x^{2}"):
    chk(_v not in _figmath, "図の数式に具体例 %s は出さない" % _v)
for _bad in ("\\le ", "\\ge ", "\\lvert", "\\rvert", "\\begin{pmatrix}",
             "\\bigl", "\\bigr", "\\Box"):
    chk(_bad not in FIGCODE, "図に mathtext が読めない記法: " + _bad)

# ══════════════════════════════════════════════════════════
# 4. 規則そのもの
# ══════════════════════════════════════════════════════════
_u = sp.Function("u")(X)
_v = sp.Function("v")(X)
chk(sp.simplify(sp.diff(_u * _v, X)
                - (_u * sp.diff(_v, X) + _v * sp.diff(_u, X))) == 0,
    "積の微分法（記号のまま）")
chk(sp.simplify(sp.diff(_u / _v, X)
                - (_v * sp.diff(_u, X) - _u * sp.diff(_v, X)) / _v ** 2) == 0,
    "商の微分法（記号のまま）")
# 逆順にすると符号が変わる
chk(sp.simplify((_u * sp.diff(_v, X) - _v * sp.diff(_u, X)) / _v ** 2
                + sp.diff(_u / _v, X)) == 0, "分子を逆にすると符号が変わる")
# u v^{-1} からの導出
chk(sp.simplify(sp.diff(_u * _v ** -1, X)
                - (_v * sp.diff(_u, X) - _u * sp.diff(_v, X)) / _v ** 2) == 0,
    "Why it works: u v^{-1} から商の微分法")
# それぞれ微分してかけると合わない
chk(sp.simplify(d(X * X) - 2 * X) == 0, "x·x の導関数は 2x")
chk(sp.simplify(d(X) * d(X) - 2 * X) != 0, "1×1 は 2x ではない")
eq(d(X) * d(X), 1, "それぞれ微分してかけると 1")

# ══════════════════════════════════════════════════════════
# 5. 例題
# ══════════════════════════════════════════════════════════
# 例題1  x^3 e^x
_f1 = X ** 3 * sp.exp(X)
chk(same(d(_f1), X ** 3 * sp.exp(X) + 3 * X ** 2 * sp.exp(X)), "例題1 の導関数")
chk(same(d(_f1), X ** 2 * sp.exp(X) * (X + 3)), "例題1 のくくった形")
eq(d(_f1).subs(X, 0), 0, "例題1 x=0 で傾き 0")
eq(d(_f1).subs(X, -3), 0, "例題1 x=-3 で傾き 0")
chk(sp.exp(-3) * 9 != 0, "例題1 x^2 e^x は x=-3 で 0 でない")
in_text("x^{2}e^{x}(x + 3)", "例題1 の答え")

# 例題2  cos x / x
_f2 = sp.cos(X) / X
chk(same(d(_f2), (-X * sp.sin(X) - sp.cos(X)) / X ** 2), "例題2 の導関数")
chk(same(d(sp.cos(X)), -sp.sin(X)), "例題2 cos の導関数")
eq(-sp.pi * sp.sin(sp.pi) - sp.cos(sp.pi), 1, "例題2 x=π での分子")
eq(d(_f2).subs(X, sp.pi), 1 / sp.pi ** 2, "例題2 x=π での傾き")
chk(float(d(_f2).subs(X, sp.pi)) > 0, "例題2 x=π では増えている")
chk(float(sp.cos(3.5) / 3.5) > float(sp.cos(sp.pi) / sp.pi),
    "例題2 π の少し先では y が大きい")
chk(float(sp.cos(3.5)) > -1, "例題2 cos x > -1")
in_text("\\frac{-x\\sin x - \\cos x}{x^{2}}", "例題2 の答え")

# 例題3  x^2 e^{3x}
_f3 = X ** 2 * sp.exp(3 * X)
chk(same(d(_f3), 3 * X ** 2 * sp.exp(3 * X) + 2 * X * sp.exp(3 * X)),
    "例題3 の導関数")
chk(same(d(_f3), X * sp.exp(3 * X) * (3 * X + 2)), "例題3 のくくった形")
chk(same(d(sp.exp(3 * X)), 3 * sp.exp(3 * X)), "例題3 e^{3x} の導関数")
eq(d(_f3).subs(X, 0), 0, "例題3 x=0 で傾き 0")
in_text("xe^{3x}(3x + 2)", "例題3 の答え")

# 例題4  (x^3+2x)/x
_f4 = (X ** 3 + 2 * X) / X
chk(same(sp.simplify(_f4), X ** 2 + 2), "例題4 の整理")
chk(same(d(_f4), 2 * X), "例題4 の導関数")
eq(X * sp.diff(X ** 3 + 2 * X, X) - (X ** 3 + 2 * X), 2 * X ** 3,
   "例題4 商の微分法の分子")
chk(same((X * sp.diff(X ** 3 + 2 * X, X) - (X ** 3 + 2 * X)) / X ** 2, 2 * X),
    "例題4 商の微分法でも同じ")
eq(_f4.subs(X, 1), 3, "例題4 x=1 もとの式")
eq((X ** 2 + 2).subs(X, 1), 3, "例題4 x=1 直した式")
in_text("f'(x) = 2x", "例題4 の答え")

# ══════════════════════════════════════════════════════════
# 6. 演習の答え
# ══════════════════════════════════════════════════════════
_E = [("演習1", X ** 3 * sp.cos(X), -X ** 3 * sp.sin(X) + 3 * X ** 2 * sp.cos(X)),
      ("演習2(a)", 5 * sp.cos(X), -5 * sp.sin(X)),
      ("演習2(b)", X * sp.sin(X), X * sp.cos(X) + sp.sin(X)),
      ("演習2(c)", (X ** 4 + X) / X ** 2, 2 * X - X ** -2),
      ("演習3", X ** 2 * sp.log(X), X + 2 * X * sp.log(X)),
      ("演習4", (X + 1) / (X - 2), -3 / (X - 2) ** 2),
      ("演習5", X ** 2 / sp.exp(X), (2 * X - X ** 2) / sp.exp(X)),
      ("演習6", sp.exp(2 * X) / (X + 1),
       sp.exp(2 * X) * (2 * X + 1) / (X + 1) ** 2),
      ("演習7", X * sp.sin(2 * X), 2 * X * sp.cos(2 * X) + sp.sin(2 * X)),
      ("演習8", X ** 2 / (X + 3), (X ** 2 + 6 * X) / (X + 3) ** 2),
      ("演習9", (2 * X + 1) * (X - 4), 4 * X - 7),
      ("演習10", sp.sin(X) / (X ** 2 + 1),
       ((X ** 2 + 1) * sp.cos(X) - 2 * X * sp.sin(X)) / (X ** 2 + 1) ** 2)]
for _name, _f, _fp in _E:
    chk(same(d(_f), _fp), "%s の導関数" % _name)

eq((-X ** 3 * sp.sin(X) + 3 * X ** 2 * sp.cos(X)).subs(X, 0), 0, "演習1 x=0")
chk(same((X ** 4 + X) / X ** 2, X ** 2 + X ** -1), "演習2(c) の書きかえ")
eq(((X ** 4 + X) / X ** 2).subs(X, 1), 2, "演習2(c) x=1 もとの式")
eq((X ** 2 + X ** -1).subs(X, 1), 2, "演習2(c) x=1 直した式")
eq(R(1, 3) - R(1, 3), 0, "演習2 のならし")
eq(sp.log(1), 0, "演習3 ln 1 = 0")
eq((X + 2 * X * sp.log(X)).subs(X, 1), 1, "演習3 f'(1)")
eq((X - 2) - (X + 1), -3, "演習4 の分子")
chk((-3 / (X - 2) ** 2).subs(X, 3) < 0, "演習4 f' は負")
eq(((X + 1) / (X - 2)).subs(X, 3), 4, "演習4 y(3)")
eq(((X + 1) / (X - 2)).subs(X, 4), R(5, 2), "演習4 y(4)")
eq(((2 * X - X ** 2) / sp.exp(X)).subs(X, 0), 0, "演習5 x=0 で傾き 0")
eq(((2 * X - X ** 2) / sp.exp(X)).subs(X, 2), 0, "演習5 x=2 で傾き 0")
chk(same(sp.exp(X) / sp.exp(2 * X), 1 / sp.exp(X)), "演習5 の約分")
chk(float(sp.E) < 4, "演習5 e < 4")
chk(float(4 * sp.E) > 9, "演習5 4e > 9")
chk(float(4 / sp.exp(2)) > float(1 / sp.E), "演習5 y(2) > y(1)")
chk(float(4 / sp.exp(2)) > float(9 / sp.exp(3)), "演習5 y(2) > y(3)")
eq((X + 1) * 2 * sp.exp(2 * X) - sp.exp(2 * X),
   sp.exp(2 * X) * (2 * X + 1), "演習6 の分子")
eq((sp.exp(2 * X) * (2 * X + 1)).subs(X, R(-1, 2)), 0,
   "演習6 x=-1/2 で分子 0")
chk(same(d(sp.exp(2 * X)), 2 * sp.exp(2 * X)), "演習6 内側の導関数")
chk(same(d(sp.sin(2 * X)), 2 * sp.cos(2 * X)), "演習7 内側の導関数")
eq((2 * X * sp.cos(2 * X) + sp.sin(2 * X)).subs(X, 0), 0, "演習7 x=0")
_wrong8 = (X ** 2 - (X + 3) * 2 * X) / (X + 3) ** 2
_right8 = (X ** 2 + 6 * X) / (X + 3) ** 2
chk(same(_wrong8, -_right8), "演習8 生徒の答えは正しい答えの -1 倍")
eq(_right8.subs(X, 1), R(7, 16), "演習8 正しい答えの x=1 での値")
eq(_wrong8.subs(X, 1), R(-7, 16), "演習8 生徒の答えの x=1 での値")
eq((X ** 2 / (X + 3)).subs(X, 1), R(1, 4), "演習8 y(1)")
eq((X ** 2 / (X + 3)).subs(X, 2), R(4, 5), "演習8 y(2)")
chk((X ** 2 / (X + 3)).subs(X, 2) > (X ** 2 / (X + 3)).subs(X, 1),
    "演習8 x=1 から 2 で増えている")
eq((X + 3) * 2 * X - X ** 2, X ** 2 + 6 * X, "演習8 の分子")
eq(sp.expand((2 * X + 1) * (X - 4)), 2 * X ** 2 - 7 * X - 4, "演習9 の展開")
eq(2 * (X - 4) + (2 * X + 1), 4 * X - 7, "演習9 積の微分法でも同じ")
eq((4 * X - 7).subs(X, 0), -7, "演習9 f'(0)")
_f10p = ((X ** 2 + 1) * sp.cos(X) - 2 * X * sp.sin(X)) / (X ** 2 + 1) ** 2
eq(_f10p.subs(X, 0), 1, "演習10 f'(0) = 1")
eq(sp.sin(0), 0, "sin 0")
eq(sp.cos(0), 1, "cos 0")
chk((Z ** 2 + 1).subs(Z, -5) > 0, "x^2+1 は 0 にならない")

# ★ 例題・演習の答えを本文（例題より前）に出していないこと
for _v in ("x^{2}e^{x}(x + 3)", "\\frac{-x\\sin x - \\cos x}{x^{2}}",
           "xe^{3x}(3x + 2)", "-5\\sin x", "x\\cos x + \\sin x",
           "x + 2x\\ln x", "\\frac{-3}{(x - 2)^{2}}",
           "\\frac{2x - x^{2}}{e^{x}}",
           "\\frac{e^{2x}(2x + 1)}{(x + 1)^{2}}",
           "\\frac{x^{2} + 6x}{(x + 3)^{2}}", "2x\\cos(2x) + \\sin(2x)",
           "4x - 7", "-x^{3}\\sin x + 3x^{2}\\cos x", "f'(x) = 2x"):
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

# --- B1: u と v を入れかえると分母まで変わる ----------------------
chk("出てくるのは $\\dfrac{v}{u}$ の導関数です。" in TEXT,
    "第3節: 入れかえると v/u の導関数になる")
chk("**符号が変わるだけではなく、分母も別の式になります。**" in TEXT,
    "第3節: 分母も変わる")
chk("あとからマイナスを付けても、もとにはもどりません。" in TEXT,
    "第3節: マイナスでは直せない")
chk("ここを入れかえると、答えの符号が変わってしまいます。" not in TEXT,
    "符号だけの問題だと読める文が消えている")
chk("入れかえると、分母までちがう式になります。" in TEXT,
    "Common errors: 分母も変わる")
_T, _B = sp.Function("T")(X), sp.Function("B")(X)
_right = (_B * sp.diff(_T, X) - _T * sp.diff(_B, X)) / _B ** 2
_swapped = (_T * sp.diff(_B, X) - _B * sp.diff(_T, X)) / _T ** 2
chk(sp.simplify(_swapped + _right) != 0, "入れかえた式は -1 倍ではない")
chk(sp.simplify(_swapped - sp.diff(_B / _T, X)) == 0,
    "入れかえた式は B/T の導関数")

# --- M1: 商と連鎖律を組み合わせる演習がある ------------------------
chk("y = \\dfrac{e^{2x}}{x + 1}$, for $x \\ne -1$" in TEXT, "演習6: 商と連鎖律")
chk("商の微分法を使い、$u$ の微分で連鎖律を使います" in TEXT, "演習6 の解説")
chk("y = \\dfrac{x^{2}}{x + 3}$, for $x \\ne -3$. Find" not in TEXT,
    "演習4 と同型だった演習6 が消えている")

# --- M2: どの規則が要るかを判断させる演習がある ---------------------
chk("For each of the following, state which rule is needed, if any, and find "
    "the derivative." in TEXT, "演習2: 規則の判断")
chk("*a constant multiple, so no product rule is needed*" in TEXT,
    "演習2(a) の答え")
chk("*no rule is needed: divide first*" in TEXT, "演習2(c) の答え")
chk("y = xe^{x}$. Find $\\dfrac{dy}{dx}$, giving your answer in a factorised "
    "form." not in TEXT, "例題1 と同型だった演習2 が消えている")

# --- M3: Δ の筋道で、極限を取る場所がそろっている -------------------
chk("です。両辺を $\\Delta x$ で割ると" in TEXT, "Why it works: 割ってから書く")
chk("**$\\Delta x$ を $0$ に近づけると、はじめの $2$ 項が @eq-aasl56b-product の "
    "$2$ 項に向かいます。**" in TEXT, "Why it works: 極限で向かう")
chk("です。$\\Delta x$ で割ると、はじめの $2$ 項が @eq-aasl56b-product の $2$ 項に"
    "なります。" not in TEXT, "極限を飛ばした断定が消えている")

# --- M4: くくり方の検算だと明記している ----------------------------
chk("**検算（くくり方）。**" in TEXT, "例題3: くくり方の検算")
chk("これはくくり方の検算で、導関数そのものの検算ではありません。" in TEXT,
    "例題3: 何を確かめているかを書いている")
chk("**検算（くくる前ともどす）。**" not in TEXT, "循環的な検算が消えている")
chk("ここでも傾きが $0$ になります。" not in TEXT, "同語反復の検算が消えている")

# --- M5: 演習10 の Explain が説明を要する問いになっている -------------
chk("Find $f'(x)$ and show that $f'(0) = 1$. Explain why $f'(x)$ is defined "
    "for every real value of $x$." in TEXT, "演習10: 定義域を説明させている")
chk("Find $f'(x)$. Explain why $f'(0) = 1$." not in TEXT,
    "代入だけで済む Explain が消えている")
chk(all(((_t ** 2 + 1) ** 2 >= 1) for _t in (-3, 0, 2)), "演習10 分母は 1 以上")

# --- M6: 整理しないことは誤りではない ------------------------------
chk("## 整理できる式に、そのまま規則を使ってしまう" in TEXT,
    "Common errors: 見出し")
chk("答えは同じですが、計算が長くなり、途中で符号や $2$ 乗を落としやすく"
    "なります。" in TEXT, "Common errors: 答えは同じだと書いている")

# --- m2: 定義域の但し書き ------------------------------------------
chk("**もとの式が定義される範囲では**結果は変わりません。" in TEXT,
    "第7節: 定義域の但し書き")

# --- m3: 電卓の要る数を使っていない ---------------------------------
chk("\\approx 3.69" not in TEXT, "電卓の要る近似値が消えている")
chk("$e < 4$ なので" in TEXT, "演習5: 電卓なしで比べる")

# --- m5: 解答例に du/dx と dv/dx がそろっている ----------------------
chk(TEXT.count("\\frac{du}{dx} = ") >= 10, "解答例に du/dx がそろっている: %d"
    % TEXT.count("\\frac{du}{dx} = "))

# --- m7: 演習9 の英語 -----------------------------------------------
chk("Describe an alternative method for finding $f'(x)$, which does not use "
    "the product rule." in TEXT, "演習9 の英語")

# --- m8: 商の callout に余分な空行がない ------------------------------
chk("**$v \\ne 0$ になる範囲でだけ使えます。**" + chr(10) + ":::" in TEXT,
    "商の callout の閉じ方")

# --- 演習の答え（新しくなったもの） -----------------------------------
in_text("\\frac{2x - x^{2}}{e^{x}}", "演習5 の答え")
in_text("\\frac{e^{2x}(2x + 1)}{(x + 1)^{2}}", "演習6 の答え")
in_text("\\frac{x^{2} + 6x}{(x + 3)^{2}}", "演習8 の答え")
in_text("\\frac{dy}{dx} = x\\cos x + \\sin x", "演習2(b) の答え")
in_text("\\frac{dy}{dx} = 2x - x^{-2}", "演習2(c) の答え")

print()
print("OK", OK, "/ NG", NG)
