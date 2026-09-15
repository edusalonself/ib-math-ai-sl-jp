# -*- coding: utf-8 -*-
"""AA SL 5.8a のページを検算する。

    python3 figs/aa-sl/check_aasl_5_8a.py
"""
import os
import re

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
QMD = os.path.join(ROOT, "aa-sl", "05-calculus", "aasl-5-8a.qmd")
FIGP = os.path.join(HERE, "make_aasl_5_8a.py")
FIGP2 = os.path.join(HERE, "make_aasl_5_8a_ex.py")

TEXT = open(QMD, encoding="utf-8").read()
FIG = open(FIGP, encoding="utf-8").read()
FIG2 = open(FIGP2, encoding="utf-8").read()
FIGCODE = FIG.split('"""', 2)[-1] + FIG2.split('"""', 2)[-1]

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
    chk(sub in FIG, "図1 に見つからない: %s :: %s" % (msg, sub[:60]))


def in_fig2(sub, msg=""):
    chk(sub in FIG2, "図2 に見つからない: %s :: %s" % (msg, sub[:60]))


BODY = TEXT.split("## Worked examples")[0]


def not_in_body(sub, msg=""):
    chk(sub not in BODY, "本文（例題より前）に残っている: %s :: %s" % (msg, sub[:60]))


R = sp.Rational
X = sp.Symbol("x", real=True)


def d1(f):
    return sp.simplify(sp.diff(f, X))


def d2(f):
    return sp.simplify(sp.diff(f, X, 2))


def same(a, b):
    return sp.simplify(sp.nsimplify(a) - sp.nsimplify(b)) == 0


def stat(f):
    return sorted(sp.solve(sp.Eq(d1(f), 0), X))


def infl(f):
    """f'' = 0 の解のうち、符号が変わるもの。"""
    out = []
    for r in sorted(sp.solve(sp.Eq(d2(f), 0), X)):
        L = d2(f).subs(X, r - R(1, 10))
        Rt = d2(f).subs(X, r + R(1, 10))
        if sp.sign(L) * sp.sign(Rt) == -1:
            out.append(r)
    return out


# ══════════════════════════════════════════════════════════
# 1. ページの骨組み
# ══════════════════════════════════════════════════════════
chk(TEXT.startswith("---\nsidebar: aa-sl\n---\n"), "front matter")
in_text("# SL 5.8a — Maximum and minimum points, concavity and inflexion"
        "（極大・極小・凹凸・変曲点） {#sec-aasl-5-8a}", "見出し")

for _h in ("## What you should be able to do", "## The idea",
           "## Why it works", "## Worked examples", "## Common errors",
           "## Exercises"):
    in_text(_h, "節 " + _h)
not_in_text("## Using your GDC", "Topic 5 に GDC の節は置かない")

_secs = re.findall(r"^### (\d)\. .*\{#([a-z0-9-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 8)],
    "### の番号 1..7: %s" % [s[0] for s in _secs])
chk([s[1] for s in _secs] == ["stationary", "firsttest", "secondtest",
                             "concavity", "inflexion", "notenough",
                             "nonzero"],
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
    "callout-important 0（SL 5.8 は公式集にない）")
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

in_text("(img/aasl-5-8a-idea.svg){#fig-aasl58a-idea width=100%}", "図1 の埋め込み")
in_text("(img/aasl-5-8a-ex.svg){#fig-aasl58a-ex width=100%}", "図2 の埋め込み")
in_text("@fig-aasl58a-idea (a)", "図1 (a) の参照")
in_text("@fig-aasl58a-idea (b)", "図1 (b) の参照")
in_text("@fig-aasl58a-ex", "図2 の参照")

for _w in ("そのとおり", "もちろん", "簡単です", "自明", "当たり前", "明らか", "当然"):
    not_in_text(_w, "禁止語 " + _w)
for _w in ("得点になりません", "点になりません", "減点されます"):
    not_in_text(_w, "採点の断定 " + _w)

# ══════════════════════════════════════════════════════════
# 2. 引用・公式集・となりのページとの境目
# ══════════════════════════════════════════════════════════
_quotes = re.findall(r"^> (.*)$", TEXT, re.M)
chk(_quotes == [], "SL 5.8 にシラバスの引用はない: %s" % _quotes)

# シラバスが指定した用語
for _w in ("concave-up", "concave-down", "point of inflexion",
           "local maximum", "local minimum", "stationary point"):
    in_text(_w, "用語 " + _w)
# 5.8b（最適化）の語は漏らさない
for _w in ("optimization", "optimisation", "最適化"):
    not_in_text(_w, "5.8b の語 " + _w)
in_text("[SL 5.8b](aasl-5-8b.qmd)", "5.8b への送り")
in_text("文章題（面積・体積・利益などを最大にする問題）は "
        "[SL 5.8b](aasl-5-8b.qmd) です。", "5.8b へ送る 1 文")
chk(TEXT.count("利益") == 1, "利益は 5.8b へ送るときだけ: %d" % TEXT.count("利益"))

for _r in ("{#eq-aasl58a-inflexion}", "{#tbl-aasl58a-kinds}",
           "{#tbl-aasl58a-first}", "{#tbl-aasl58a-second}",
           "{#tbl-aasl58a-two}"):
    in_text(_r, "参照 " + _r)
for _a in ("aasl-5-2.qmd#zero", "aasl-5-2.qmd#interval", "aasl-5-7.qmd#shape",
           "aasl-5-7.qmd#sign", "aasl-5-6a.qmd#chain"):
    in_text(_a, "参照 " + _a)

# ══════════════════════════════════════════════════════════
# 3. 図
# ══════════════════════════════════════════════════════════
in_fig('"(a) Maximum, minimum and point of inflexion"', "図1 (a) の題")
in_fig('"(b) How to decide"', "図1 (b) の題")
in_fig('"concave-down"', "図1 concave-down")
in_fig('"concave-up"', "図1 concave-up")
in_fig('"$f\'(a) = 0$ and $f\'\'(a) < 0$", "local maximum at $x = a$"',
       "図1 極大の行")
in_fig('"$f\'(a) = 0$ and $f\'\'(a) = 0$", "no conclusion yet"',
       "図1 決まらない行")
in_fig("F = X ** 3 / 3 - 2 * X ** 2 + 3 * X", "図1 の関数")
in_fig2("X ** 4", "図2 の x^4")
in_fig2("X ** 3", "図2 の x^3")
in_fig2('"$f\'\'$ does not change sign"', "図2 x^4 の注記")
in_fig2('"$f\'\'$ changes sign"', "図2 x^3 の注記")

# 図1 の関数の停留点・変曲点が、注記と合っている
_fig = X ** 3 / 3 - 2 * X ** 2 + 3 * X
chk(stat(_fig) == [1, 3], "図1 の停留点は 1 と 3: %s" % stat(_fig))
chk(infl(_fig) == [2], "図1 の変曲点は 2: %s" % infl(_fig))
chk(d2(_fig).subs(X, 1) < 0, "図1 x=1 は極大")
chk(d2(_fig).subs(X, 3) > 0, "図1 x=3 は極小")
# 図2
chk(infl(X ** 4) == [], "図2 x^4 に変曲点はない")
chk(infl(X ** 3) == [0], "図2 x^3 の変曲点は 0")
eq(d2(X ** 4).subs(X, 0), 0, "図2 x^4 の f''(0)")
eq(d2(X ** 3).subs(X, 0), 0, "図2 x^3 の f''(0)")
for _bad in ("\\le ", "\\ge ", "\\lvert", "\\rvert", "\\begin{pmatrix}",
             "\\bigl", "\\bigr", "\\Box"):
    chk(_bad not in FIGCODE, "図に mathtext が読めない記法: " + _bad)

# ══════════════════════════════════════════════════════════
# 4. 例題
# ══════════════════════════════════════════════════════════
# 例題1
_f1 = 2 * X ** 3 + 3 * X ** 2 - 12 * X + 1
chk(same(d1(_f1), 6 * X ** 2 + 6 * X - 12), "例題1 の f'")
chk(same(6 * (X + 2) * (X - 1), 6 * X ** 2 + 6 * X - 12), "例題1 の因数分解")
chk(stat(_f1) == [-2, 1], "例題1 の停留点: %s" % stat(_f1))
chk(same(d2(_f1), 12 * X + 6), "例題1 の f''")
eq(d2(_f1).subs(X, -2), -18, "例題1 f''(-2)")
eq(d2(_f1).subs(X, 1), 18, "例題1 f''(1)")
eq(_f1.subs(X, -2), 21, "例題1 f(-2)")
eq(_f1.subs(X, 1), -6, "例題1 f(1)")
eq(d1(_f1).subs(X, 0), -12, "例題1 f'(0)")
in_text("(-2,\\ 21) \\quad \\text{and} \\quad (1,\\ -6)", "例題1 の答え")

# 例題2
_f2 = X ** 4 - 4 * X ** 3
chk(same(d1(_f2), 4 * X ** 3 - 12 * X ** 2), "例題2 の f'")
chk(same(d2(_f2), 12 * X ** 2 - 24 * X), "例題2 の f''")
chk(same(12 * X * (X - 2), 12 * X ** 2 - 24 * X), "例題2 の因数分解")
chk(infl(_f2) == [0, 2], "例題2 の変曲点: %s" % infl(_f2))
eq(d2(_f2).subs(X, -1), 36, "例題2 f''(-1)")
eq(d2(_f2).subs(X, 1), -12, "例題2 f''(1)")
eq(d2(_f2).subs(X, 3), 36, "例題2 f''(3)")
eq(_f2.subs(X, 0), 0, "例題2 f(0)")
eq(_f2.subs(X, 2), -16, "例題2 f(2)")
eq(d1(_f2).subs(X, 0), 0, "例題2 f'(0) = 0（停留点）")
eq(d1(_f2).subs(X, 2), -16, "例題2 f'(2) ≠ 0")
chk(d1(_f2).subs(X, 2) != 0, "例題2 (2,-16) は停留点でない")
in_text("(0,\\ 0) \\quad \\text{and} \\quad (2,\\ -16)", "例題2 の答え")

# 例題3
_f3 = X ** 6
chk(same(d1(_f3), 6 * X ** 5), "例題3 の f'")
chk(same(d2(_f3), 30 * X ** 4), "例題3 の f''")
eq(d1(_f3).subs(X, 0), 0, "例題3 f'(0)")
eq(d2(_f3).subs(X, 0), 0, "例題3 f''(0)")
chk(infl(_f3) == [], "例題3 変曲点なし")
chk(d2(_f3).subs(X, -1) > 0 and d2(_f3).subs(X, 1) > 0, "例題3 f'' は両側で正")
eq(d1(_f3).subs(X, -1), -6, "例題3 f'(-1)")
eq(d1(_f3).subs(X, 1), 6, "例題3 f'(1)")
eq(d2(_f3).subs(X, 1), 30, "例題3 f''(1)")
chk(same(d2(X ** 3), 6 * X), "例題3 くらべる x^3 の f''")

# 例題4
_f4 = sp.exp(X) - X ** 2
chk(same(d1(_f4), sp.exp(X) - 2 * X), "例題4 の f'")
chk(same(d2(_f4), sp.exp(X) - 2), "例題4 の f''")
chk(sp.solve(sp.Eq(sp.exp(X) - 2, 0), X) == [sp.log(2)], "例題4 x = ln 2")
eq(d2(_f4).subs(X, 0), -1, "例題4 f''(0)")
chk(float(d2(_f4).subs(X, 1)) > 0, "例題4 f''(1) > 0")
chk(float(sp.E) > 2, "例題4 e > 2")
chk(0 < float(sp.log(2)) < 1, "例題4 0 < ln 2 < 1")
in_text("x = \\ln 2", "例題4 の答え")

# ══════════════════════════════════════════════════════════
# 5. 演習
# ══════════════════════════════════════════════════════════
_E1 = X ** 3 - 12 * X + 1
chk(stat(_E1) == [-2, 2], "演習1 の停留点")
eq(d2(_E1).subs(X, -2), -12, "演習1 f''(-2)")
eq(d2(_E1).subs(X, 2), 12, "演習1 f''(2)")
eq(_E1.subs(X, -2), 17, "演習1 f(-2)")
eq(_E1.subs(X, 2), -15, "演習1 f(2)")

_E2 = X ** 2 - 6 * X + 4
chk(stat(_E2) == [3], "演習2 の停留点")
eq(d2(_E2), 2, "演習2 の f''")
eq(_E2.subs(X, 3), -5, "演習2 f(3)")
chk(infl(_E2) == [], "演習2 に変曲点はない")

_E3 = X ** 3 - 3 * X ** 2 + 4
chk(same(d2(_E3), 6 * X - 6), "演習3 の f''")
chk(infl(_E3) == [1], "演習3 の変曲点")
eq(d2(_E3).subs(X, 0), -6, "演習3 f''(0)")
eq(d2(_E3).subs(X, 2), 6, "演習3 f''(2)")
eq(_E3.subs(X, 1), 2, "演習3 f(1)")
eq(d1(_E3).subs(X, 1), -3, "演習3 f'(1) ≠ 0")

_E4 = X ** 4 - 2 * X ** 3
chk(same(d1(_E4), 4 * X ** 3 - 6 * X ** 2), "演習4 の f'")
chk(same(d2(_E4), 12 * X ** 2 - 12 * X), "演習4 の f''")
chk(same(12 * X * (X - 1), 12 * X ** 2 - 12 * X), "演習4 の因数分解")
chk(sorted(sp.solve(sp.Eq(d2(_E4), 0), X)) == [0, 1], "演習4 f''=0")
eq(d2(_E4).subs(X, R(1, 2)), -3, "演習4 f''(1/2)")
eq(d2(_E4).subs(X, -1), 24, "演習4 f''(-1)")
eq(d2(_E4).subs(X, 2), 24, "演習4 f''(2)")
eq(d2(_E4).subs(X, 0), 0, "演習4 f''(0)")
eq(d2(_E4).subs(X, 1), 0, "演習4 f''(1)")

_E5 = X + 4 / X
chk(same(d1(_E5), 1 - 4 * X ** -2), "演習5 の f'")
chk(same(d2(_E5), 8 * X ** -3), "演習5 の f''")
chk(stat(_E5) == [-2, 2], "演習5 の停留点: %s" % stat(_E5))
eq(d2(_E5).subs(X, -2), -1, "演習5 f''(-2)")
eq(d2(_E5).subs(X, 2), 1, "演習5 f''(2)")
eq(_E5.subs(X, -2), -4, "演習5 f(-2)")
eq(_E5.subs(X, 2), 4, "演習5 f(2)")
chk(_E5.subs(X, -2) < _E5.subs(X, 2), "演習5 極大の値 < 極小の値")

_E6 = X ** 5
eq(d2(_E6).subs(X, 0), 0, "演習6 f''(0)")
chk(infl(_E6) == [0], "演習6 の変曲点")
eq(d2(_E6).subs(X, -1), -20, "演習6 f''(-1)")
eq(d2(_E6).subs(X, 1), 20, "演習6 f''(1)")
eq(d1(_E6).subs(X, 0), 0, "演習6 f'(0) = 0")

# 演習8 の反例
_E8 = (X - 2) ** 4
eq(d2(_E8).subs(X, 2), 0, "演習8 反例の f''(2)")
chk(same(d2(_E8), 12 * (X - 2) ** 2), "演習8 反例の f''")
chk(infl(_E8) == [], "演習8 反例に変曲点はない")

_E9 = X ** 3 - 3 * X ** 2 + 3 * X
chk(same(d1(_E9), 3 * (X - 1) ** 2), "演習9 の f'")
eq(d1(_E9).subs(X, 1), 0, "演習9 f'(1)")
eq(d2(_E9).subs(X, 1), 0, "演習9 f''(1)")
eq(d1(_E9).subs(X, 0), 3, "演習9 f'(0)")
eq(d1(_E9).subs(X, 2), 3, "演習9 f'(2)")
eq(_E9.subs(X, 1), 1, "演習9 f(1)")
chk(infl(_E9) == [1], "演習9 は変曲点")

_E10 = sp.exp(X) + sp.exp(-X)
chk(same(d1(_E10), sp.exp(X) - sp.exp(-X)), "演習10 の f'")
chk(same(d2(_E10), _E10), "演習10 の f'' はもとにもどる")
chk(float(d2(_E10).subs(X, 0)) == 2, "演習10 f''(0)")
eq(d1(_E10).subs(X, 0), 0, "演習10 f'(0)")
chk(all(float(d2(_E10).subs(X, _v)) > 0 for _v in (-3, -1, 0, 1, 3)),
    "演習10 f'' はどこでも正")

# ★ 例題・演習の答えを本文（例題より前）に出していないこと
for _v in ("(-2,\\ 21)", "(1,\\ -6)", "(2,\\ -16)", "(-2,\\ 17)",
           "(2,\\ -15)", "(3,\\ -5)", "(1,\\ 2)", "(-2,\\ -4)",
           "(2,\\ 4)", "\\ln 2", "0 < x < 1", "20x^{3}", "6x^{5}"):
    not_in_body(_v, "答え %s は本文に出さない" % _v)

# ══════════════════════════════════════════════════════════
# 6. ページに書いてある計算を、機械的にたしかめる
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

# --- B1: 第 2 節の表に f'(a) = 0 の条件がある ------------------------
chk("**$f'(a) = 0$ のとき、$a$ の左右で $f'$ の符号を調べます。**" in TEXT,
    "第2節: f'(a) = 0 の前提")
chk("| $f' > 0$ | $f' > 0$ | 極大でも極小でもない |" in TEXT,
    "第2節: 符号が変わらない行（正）")
chk("| $f' < 0$ | $f' < 0$ | 極大でも極小でもない |" in TEXT,
    "第2節: 符号が変わらない行（負）")
chk("| 符号が変わらない | 同じ | 変曲点（傾き $0$） |" not in TEXT,
    "変曲点だと言い切っていた行が消えている")
chk("**下の $2$ 行のときは、そこで止めてください。**" in TEXT,
    "第2節: そこで止める")
chk("$f'$ の符号を左右で調べれば、必ず決まります。" not in TEXT,
    "「必ず決まる」が消えている")
# x^3 の x=1 は f' の符号が変わらないが、変曲点ではない
chk(d1(X ** 3).subs(X, 1) != 0, "x^3 の x=1 は停留点ではない")
chk(infl(X ** 3) == [0], "x^3 の変曲点は 0 だけ")

# --- B2: 図 (b) の 4 行目に f''(a) = 0 が入っている --------------------
_q2 = chr(39) * 2
chk('("$f' + _q2 + '(a) = 0$ and $f' + _q2 + '$ changes sign", '
    '"point of inflexion at $x = a$"))' in FIG, "図1 (b) 4 行目の条件")
chk('("$f' + _q2 + '$ changes sign at $a$", '
    '"point of inflexion at $x = a$"))' not in FIG,
    "条件が 1 つだけの行が消えている")
chk("the second derivative is zero and changes sign is a point of inflexion"
    in TEXT, "図1 の alt の 4 行目")
# 1/x は f'' が符号を変えるが、x=0 に変曲点はない（定義されていない）
chk(sp.simplify(sp.diff(1 / X, X, 2) - 2 / X ** 3) == 0, "1/x の f''")

# --- B3: 例題3 は x^6（x^4 は第 6 節と図 2 が扱う） ---------------------
chk("[The function $f$ is given by $f(x) = x^{6}$.]{.q-en}" in TEXT,
    "例題3: x^6")
chk("[The function $f$ is given by $f(x) = x^{4}$.]{.q-en}" not in TEXT,
    "第6節と重なっていた x^4 の例題が消えている")
chk("f''(x) = 30x^{4} > 0" in TEXT, "例題3 の model answer")
chk("偶数乗と奇数乗でちがいます。" in TEXT, "例題3 の検算")

# --- B4: Why it works の f''(a) < 0 の一歩 ---------------------------
chk("$f''(a) < 0$ は、**$f'$ の変化率が $x = a$ で負**だということです。" in TEXT,
    "Why it works: 1 点での変化率として使っている")
chk("**「$a$ のまわりの区間で $f'$ が減少している」とまでは、$f''(a) < 0$ だけからは"
    "言えません。**" in TEXT, "Why it works: 区間では言えないと断っている")
chk("$f''(a) < 0$ なら、$a$ のまわりで $f'$ は減少しています" not in TEXT,
    "1 点から近傍の単調性を出していた文が消えている")
chk("**これは @tbl-aasl58a-first の $1$ 行目そのものです。**" in TEXT,
    "Why it works: 表への参照")

# --- M1: 第 1 節の表 --------------------------------------------------
chk("SL で扱う関数では、停留点は次の $3$ 種類のどれかになります" in TEXT,
    "第1節: SL の範囲での話だと断っている")
chk("| 傾き $0$ の変曲点 | point of inflexion with zero gradient |" in TEXT,
    "第1節: zero gradient を明記")

# --- M3 + M4: 循環していた検算を差しかえた -----------------------------
chk("**検算（両側の値で）。**" in TEXT, "両側の値による検算")
chk(TEXT.count("**検算（両側の値で）。**") == 2, "両側の値の検算は 2 か所: %d"
    % TEXT.count("**検算（両側の値で）。**"))
chk("**検算（符号の向き）。** 極大のほうが $f'' < 0$ です" not in TEXT,
    "循環していた検算が消えている")
chk("**検算（大小）。**" not in TEXT, "成り立たない一般則の検算が消えている")
_w1 = 2 * X ** 3 + 3 * X ** 2 - 12 * X + 1
eq(_w1.subs(X, -3), 10, "例題1 f(-3)")
eq(_w1.subs(X, -1), 14, "例題1 f(-1)")
chk(_w1.subs(X, -3) < 21 and _w1.subs(X, -1) < 21, "例題1 両側とも 21 より小さい")
_e1 = X ** 3 - 12 * X + 1
eq(_e1.subs(X, -3), 10, "演習1 f(-3)")
eq(_e1.subs(X, -1), 12, "演習1 f(-1)")
chk(_e1.subs(X, -3) < 17 and _e1.subs(X, -1) < 17, "演習1 両側とも 17 より小さい")

# --- M5(2): 演習1 が f' の符号で判定させる形になっている ------------------
chk("using the sign of $f'$ to show which is which." in TEXT,
    "演習1: f' の符号で判定")
chk("*$f'$ changes from positive to negative at $x = -2$, so $(-2,\\ 17)$ is "
    "a local maximum point*" in TEXT, "演習1 の答え（極大）")
eq(d1(_e1).subs(X, -3), 15, "演習1 f'(-3)")
eq(d1(_e1).subs(X, 0), -12, "演習1 f'(0)")
eq(d1(_e1).subs(X, 3), 15, "演習1 f'(3)")
chk(same(3 * (X - 2) * (X + 2), 3 * X ** 2 - 12), "演習1 の因数分解")

# --- M5(1) + M2: 演習5 で「local」の意味が出てくる ----------------------
chk("The function $f$ is given by $f(x) = x + \\dfrac{4}{x}$, for $x \\ne 0$."
    in TEXT, "演習5: x + 4/x")
chk("**極大のほうが小さい**です ✓" in TEXT, "演習5: local の意味の検算")
chk("f(x) = 2x^{3} - 9x^{2} + 12x$. Find the coordinates of the stationary"
    not in TEXT, "例題1 と同型だった演習5 が消えている")

# --- M6: 「いつでも使えます」 -------------------------------------------
chk("**この方法は、$f''$ が使えないときにも使えます。**" in TEXT,
    "第2節: いつでもではない")
chk("**この方法は、いつでも使えます。**" not in TEXT, "言い切りが消えている")

# --- minor 1: concave-up の訳 -------------------------------------------
chk("- **concave-up**（下に凸）と **concave-down**（上に凸）の範囲を、" in TEXT,
    "目標: concave の訳")

# --- minor 2: 変曲点を点で書く -------------------------------------------
chk("$(a,\\ f(a))$ が変曲点であるための条件は、次の $2$ つです。" in TEXT,
    "第5節: 点として書く")

# --- minor 3: 演習8 の逆向き ---------------------------------------------
chk("$f''(a)$ が計算できる変曲点では、$f''(a) = 0$ です" in TEXT,
    "演習8: f'' が計算できるとき")

# --- minor 6 + 7: 演習7・9 の英語 -----------------------------------------
chk("changing from negative to positive." in TEXT, "演習7 の英語")
chk("that $(1,1)$ is neither a local maximum point nor a local minimum point."
    in TEXT, "演習9 の英語")

# --- minor 12: 演習4 が 5.7 の演習6 と重ならない ---------------------------
chk("f(x) = x^{4} - 2x^{3}$. Find the interval" in TEXT, "演習4: x^4 - 2x^3")
chk("f(x) = x^{4} - 6x^{2}$. Find the interval" not in TEXT,
    "5.7 と重なっていた演習4 が消えている")
chk("$$0 < x < 1$$" in TEXT, "演習4 の答え")

# --- minor 14 + 15: 検算の言い方 -------------------------------------------
chk("**検算（符号の並び）。**" in TEXT, "例題2: 符号の並びの検算")
chk("**検算（何が聞かれているか）。**" in TEXT, "演習7: 何が聞かれているか")

print()
print("OK", OK, "/ NG", NG)
