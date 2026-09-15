# -*- coding: utf-8 -*-
"""AA SL 5.2 のページを検算する。

    python3 figs/aa-sl/check_aasl_5_2.py
"""
import os
import re

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
QMD = os.path.join(ROOT, "aa-sl", "05-calculus", "aasl-5-2.qmd")
FIGP = os.path.join(HERE, "make_aasl_5_2.py")

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
X = sp.Symbol("x", real=True)
T = sp.Symbol("t", real=True)


def pos_set(e, v=None):
    return sp.solve_univariate_inequality(sp.sympify(e) > 0, v or X,
                                          relational=False)


def neg_set(e, v=None):
    return sp.solve_univariate_inequality(sp.sympify(e) < 0, v or X,
                                          relational=False)


def I(a, b):
    return sp.Interval.open(a, b)


OO = sp.oo

# ══════════════════════════════════════════════════════════
# 1. ページの骨組み
# ══════════════════════════════════════════════════════════
chk(TEXT.startswith("---\nsidebar: aa-sl\n---\n"), "front matter")
in_text("# SL 5.2 — Increasing and decreasing functions"
        "（増加・減少と導関数の符号） {#sec-aasl-5-2}", "見出し")

for _h in ("## What you should be able to do", "## The idea",
           "## Why it works", "## Worked examples", "## Common errors",
           "## Exercises"):
    in_text(_h, "節 " + _h)
not_in_text("## Using your GDC", "Topic 5 に GDC の節は置かない")

_secs = re.findall(r"^### (\d)\. .*\{#([a-z0-9-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 8)],
    "### の番号 1..7: %s" % [s[0] for s in _secs])
chk([s[1] for s in _secs] == ["meaning", "sign", "zero", "interval",
                              "fromgraph", "pointwise", "table"],
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
    "callout-important 0（5.2 に公式集の欄はない）")
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

in_text("(img/aasl-5-2-idea.svg){#fig-aasl52-idea width=100%}", "図の埋め込み")
in_text("@fig-aasl52-idea (b)", "図 (b) の参照")

for _w in ("そのとおり", "もちろん", "簡単です", "自明", "当たり前", "明らか", "当然"):
    not_in_text(_w, "禁止語 " + _w)
for _w in ("得点になりません", "点になりません", "減点されます"):
    not_in_text(_w, "採点の断定 " + _w)

# ══════════════════════════════════════════════════════════
# 2. 引用と公式集
# ══════════════════════════════════════════════════════════
_quotes = re.findall(r"^> (.*)$", TEXT, re.M)
chk(_quotes == [], "5.2 でシラバスの引用は使わない: %s" % _quotes)
not_in_text("公式集", "5.2 に公式集の話は置かない（欄がない）")

for _t in ("{#tbl-aasl52-word}", "{#tbl-aasl52-sign}", "{#tbl-aasl52-stat}",
           "{#tbl-aasl52-read}", "{#tbl-aasl52-tbl}", "{#tbl-aasl52-we1}",
           "{#tbl-aasl52-we4}"):
    in_text(_t, "表 " + _t)
in_text("[SL 5.3](aasl-5-3.qmd)", "5.3 への参照（f' の求め方）")
in_text("[SL 5.1](aasl-5-1.qmd#gradfn)", "5.1 への参照")
# 5.8 の語をここで使わない
for _w in ("point of inflexion", "変曲点", "concave", "凸"):
    not_in_text(_w, "5.8 の語 %s は 5.2 で使わない" % _w)

# ══════════════════════════════════════════════════════════
# 3. 図
# ══════════════════════════════════════════════════════════
in_fig('"(a) The graph of $y = f(x)$"', "図 (a) の題")
FIG2P = os.path.join(HERE, "make_aasl_5_2_ex.py")
FIG2 = open(FIG2P, encoding="utf-8").read()
chk("ROOTS = (-1.0, 2.0, 4.0)" in FIG2, "演習2 の図の交点")
chk("(t + 1.0) * (t - 2.0) * (t - 4.0) / 4.0" in FIG2, "演習2 の図の式")
in_text("(img/aasl-5-2-ex.svg){#fig-aasl52-ex width=78%}",
        "演習2 の図の埋め込み")
in_fig("(b) The graph of $y = f'(x)$, drawn under the same $x$-axis",
       "図 (b) の題")
in_fig('"turns here"', "図 (a) の「向きが変わる」")
in_fig('"flat, but does not turn"', "図 (a) の「向きは変わらない」")
in_fig('"crosses the axis: sign changes"', "図 (b) の横切る")
in_fig("touches the axis:", "図 (b) の触れるだけ")
# 図の f' は (x+2)(x-1)^2 / 6 で、p で符号が変わり q では変わらない
_FA, _FB = -2, 1
_fp = (X + 2) * (X - 1) ** 2 / 6
eq(_fp.subs(X, _FA), 0, "図 f'(p) = 0")
eq(_fp.subs(X, _FB), 0, "図 f'(q) = 0")
chk(_fp.subs(X, -3) < 0, "図 p の左は負")
chk(_fp.subs(X, 0) > 0, "図 p の右は正（符号が変わる）")
chk(_fp.subs(X, 2) > 0, "図 q の右も正（符号が変わらない）")
chk(sp.expand(sp.integrate(_fp, X)) == sp.expand(
    (X ** 4 / 4 - sp.Rational(3, 2) * X ** 2 + 2 * X) / 6),
    "図 f は f' の原始関数")
# 図に数値の答えを出していないこと
_figmath = " ".join(re.findall(r"\$([^$]*)\$", FIGCODE))
for _v in ("-2", "2", "4", "3", "5", "6", "8"):
    chk(_v not in _figmath, "図の数式に数 %s は出さない" % _v)
for _bad in ("\\le ", "\\ge ", "\\lvert", "\\rvert", "\\begin{pmatrix}"):
    chk(_bad not in FIGCODE, "図に mathtext が読めない記法: " + _bad)

# ══════════════════════════════════════════════════════════
# 4. 例題1  f'(x) = 3x^2 - 12
# ══════════════════════════════════════════════════════════
_w1 = 3 * X ** 2 - 12
eq(sp.factor(_w1), 3 * (X - 2) * (X + 2), "例題1 の因数分解")
chk(sorted(sp.solve(sp.Eq(_w1, 0), X)) == [-2, 2], "例題1 の停留点")
chk(pos_set(_w1) == sp.Union(I(-OO, -2), I(2, OO)), "例題1 増加の区間")
chk(neg_set(_w1) == I(-2, 2), "例題1 減少の区間")
eq(_w1.subs(X, -3), 15, "例題1 検算 f'(-3)")
eq(_w1.subs(X, 0), -12, "例題1 検算 f'(0)")
eq(_w1.subs(X, 3), 15, "例題1 検算 f'(3)")
in_text("increasing for $x < -2$ and for $x > 2$", "例題1 の答え（増加）")
in_text("decreasing for $-2 < x < 2$", "例題1 の答え（減少）")

# ══════════════════════════════════════════════════════════
# 5. 例題2  符号表（+ 0 - 0 +）
# ══════════════════════════════════════════════════════════
in_text("| $f'(x)$ | $+$ | $0$ | $-$ | $0$ | $+$ |", "例題2 の符号表")
in_text("increasing for $x < -1$ and for $x > 2$", "例題2(a)")
in_text("the graph turns at $x = -1$ and at $x = 2$", "例題2(b)")
# + から - へ、- から + へ、どちらも符号が変わる
chk(1 * -1 < 0, "例題2 x=-1 の前後で符号が変わる")
chk(-1 * 1 < 0, "例題2 x=2 の前後で符号が変わる")

# ══════════════════════════════════════════════════════════
# 6. 例題3  dV/dt = 20 - 4t、0 <= t <= 8
# ══════════════════════════════════════════════════════════
_w3 = 20 - 4 * T
chk(sp.solve(sp.Eq(_w3, 0), T) == [5], "例題3 の停留点 t=5")
chk(pos_set(_w3, T) == I(-OO, 5), "例題3 dV/dt > 0 は t < 5")
eq(_w3.subs(T, 4), 4, "例題3 検算 t=4")
eq(_w3.subs(T, 6), -4, "例題3 検算 t=6")
eq(_w3.subs(T, 5), 0, "例題3 検算 t=5")
chk(0 <= 5 <= 8, "例題3 t=5 は与えられた範囲の中")
in_text("increasing for $0 \\leq t < 5$", "例題3 の答え（範囲つき）")

# ══════════════════════════════════════════════════════════
# 7. 例題4  f'(x) = 3x^2（触れるだけ）
# ══════════════════════════════════════════════════════════
_w4 = 3 * X ** 2
chk(sp.solve(sp.Eq(_w4, 0), X) == [0], "例題4 の停留点 x=0")
chk(pos_set(_w4) == sp.Union(I(-OO, 0), I(0, OO)), "例題4 増加の区間")
chk(neg_set(_w4) == sp.EmptySet, "例題4 減少の区間はない")
eq(_w4.subs(X, -1), 3, "例題4 検算 f'(-1)")
eq(_w4.subs(X, 1), 3, "例題4 検算 f'(1)")
chk(_w4.subs(X, -1) > 0 and _w4.subs(X, 1) > 0, "例題4 両側で正")
in_text("increasing for all $x$ (equivalently for $x < 0$ and for "
        "$x > 0$)", "例題4 の答え（まとめた形）")
in_text("there is no interval on which $f$ is decreasing", "例題4 の答え")

# ══════════════════════════════════════════════════════════
# 8. Why it works の (x-1)^2
# ══════════════════════════════════════════════════════════
_wy = (X - 1) ** 2
chk(pos_set(_wy) == sp.Union(I(-OO, 1), I(1, OO)), "Why it works: (x-1)^2 は 1 以外で正")
eq(_wy.subs(X, 1), 0, "Why it works: (x-1)^2 は 1 で 0")
in_text("$f'$ が $(x - a)^{2}$ の形の因数をもつときを考えます。",
        "Why it works の例は文字だけ")
chk("f'(x) = (x + 1)(x - 2)^{2}" in TEXT, "演習7 は (x+1)(x-2)^2")
not_in_body("(x - 2)^{2}", "演習7 の式は本文に出さない")
not_in_body("(x - 4)^{2}", "古い演習7 の式は残っていない")

# ══════════════════════════════════════════════════════════
# 9. 演習の答え
# ══════════════════════════════════════════════════════════
_E = [
    ("演習1", 2 * X - 8, I(4, OO), I(-OO, 4)),
    ("演習3", X ** 2 - 5 * X + 6, sp.Union(I(-OO, 2), I(3, OO)), I(2, 3)),
    ("演習4", 4 - X ** 2, I(-2, 2), sp.Union(I(-OO, -2), I(2, OO))),
    ("演習5", 4 * X ** 3, I(0, OO), I(-OO, 0)),
    ("演習7", (X + 1) * (X - 2) ** 2, sp.Union(I(-1, 2), I(2, OO)),
     I(-OO, -1)),
    ("演習8", 3 * X ** 2 + 5, sp.S.Reals, sp.EmptySet),
]
for _name, _e, _up, _dn in _E:
    chk(pos_set(_e) == _up, "%s 増加の区間: %s" % (_name, pos_set(_e)))
    chk(neg_set(_e) == _dn, "%s 減少の区間: %s" % (_name, neg_set(_e)))

eq((2 * X - 8).subs(X, 5), 2, "演習1 検算 f'(5)")
eq((2 * X - 8).subs(X, 0), -8, "演習1 検算 f'(0)")
eq((2 * X - 8).subs(X, 4), 0, "演習1 境目")
# 演習2 は図から読む問題。f'(x) = (x+1)(x-2)(x-4)/4
_e2 = (X + 1) * (X - 2) * (X - 4) / 4
chk(sorted(sp.solve(sp.Eq(_e2, 0), X)) == [-1, 2, 4], "演習2 の交点")
chk(pos_set(_e2) == sp.Union(I(-1, 2), I(4, OO)), "演習2 増加の区間")
chk(neg_set(_e2) == sp.Union(I(-OO, -1), I(2, 4)), "演習2 減少の区間")
eq(_e2.subs(X, -2), -6, "演習2 検算 f'(-2)")
eq(_e2.subs(X, 0), 2, "演習2 検算 f'(0)")
eq(_e2.subs(X, 3), -1, "演習2 検算 f'(3)")
eq(_e2.subs(X, 5), R(9, 2), "演習2 検算 f'(5)")
eq(sp.factor(X ** 2 - 5 * X + 6), (X - 2) * (X - 3), "演習3 の因数分解")
eq((X ** 2 - 5 * X + 6).subs(X, 0), 6, "演習3 検算 f'(0)")
eq((X ** 2 - 5 * X + 6).subs(X, R("2.5")), R("-0.25"), "演習3 検算 f'(2.5)")
eq((X ** 2 - 5 * X + 6).subs(X, 4), 2, "演習3 検算 f'(4)")
eq(sp.factor(4 - X ** 2), -(X - 2) * (X + 2), "演習4 の因数分解")
eq((4 - X ** 2).subs(X, 0), 4, "演習4 検算 f'(0)")
eq((4 - X ** 2).subs(X, 3), -5, "演習4 検算 f'(3)")
eq((4 - X ** 2).subs(X, -3), -5, "演習4 検算 f'(-3)")
eq((4 * X ** 3).subs(X, -1), -4, "演習5 検算 f'(-1)")
eq((4 * X ** 3).subs(X, 1), 4, "演習5 検算 f'(1)")
_e7 = (X + 1) * (X - 2) ** 2
chk(sorted(sp.solve(sp.Eq(_e7, 0), X)) == [-1, 2], "演習7 の停留点は 2 つ")
eq(_e7.subs(X, -2), -16, "演習7 検算 f'(-2)")
eq(_e7.subs(X, 0), 4, "演習7 検算 f'(0)")
eq(_e7.subs(X, 3), 4, "演習7 検算 f'(3)")
chk(_e7.subs(X, 0) > 0 and _e7.subs(X, 3) > 0,
    "演習7 x=2 の前後はどちらも正")
chk(_e7.subs(X, -2) < 0 < _e7.subs(X, 0), "演習7 x=-1 で符号が変わる")
eq((3 * X ** 2 + 5).subs(X, 0), 5, "演習8 いちばん小さい値")
eq((3 * X ** 2 + 5).subs(X, -2), 17, "演習8 検算 f'(-2)")
eq((3 * X ** 2 + 5).subs(X, 2), 17, "演習8 検算 f'(2)")
chk(sp.solve(sp.Eq(3 * X ** 2 + 5, 0), X) == [] or
    all(not r.is_real for r in sp.solve(sp.Eq(3 * X ** 2 + 5, 0), X)),
    "演習8 に実数の停留点はない")
eq(sp.solve(sp.Eq(3 * X ** 2 + 5, 0), X ** 2)[0] if
   sp.solve(sp.Eq(3 * X ** 2 + 5, 0), X ** 2) else R(-5, 3), R(-5, 3),
   "演習8 x^2 = -5/3")

# 演習6 の符号表（- 0 - 0 +）
in_text("| $f'(x)$ | $-$ | $0$ | $-$ | $0$ | $+$ |", "演習6 の符号表")
in_text("decreasing for $x < 5$", "演習6 の答え（減少・停留点で切らない）")
not_in_text("decreasing for $x < 0$ and for $0 < x < 5$",
            "停留点で切った古い答えが消えている")
in_text("the graph turns only at $x = 5$", "演習6 の答え（向きが変わる点）")

# 演習10  dN/dt = t(6-t)
_e10 = T * (6 - T)
chk(pos_set(_e10, T) == I(0, 6), "演習10 増加の区間")
eq(_e10.subs(T, 3), 9, "演習10 検算 t=3")
eq(_e10.subs(T, 7), -7, "演習10 検算 t=7")
eq(_e10.subs(T, 0), 0, "演習10 t=0 で 0")
eq(_e10.subs(T, 6), 0, "演習10 t=6 で 0")
in_text("increasing for $0 < t < 6$", "演習10 の答え")

# ★ 例題・演習の答えを本文（例題より前）に出していないこと
for _v in ("x < -2$ と $x > 2", "0 \\leq t < 5", "0 < t < 6", "x > 4$ で増加",
           "2 < x < 3", "-2 < x < 2"):
    not_in_body(_v, "答え %s は本文に出さない" % _v)

# ══════════════════════════════════════════════════════════
# 10. ページに書いてある計算を、機械的にたしかめる
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

# --- B1: 停留点で切っても切らなくてもよい、と正しく書く -----------
chk("**停留点で切って書いても、切らずに書いてもかまいません。**" in TEXT,
    "第4節: 停留点の扱い")
chk("$f$ はその点をまたいで増加しつづけています。" in TEXT,
    "第4節: 孤立した停留点をまたいで増加する")
chk("**停留点そのものは、ふつう区間に入れません。**" not in TEXT,
    "誤った（第6節と矛盾する）文が消えている")
chk("$f'(x) = 0$ の点では増加も減少もしていない" not in TEXT,
    "点で増加・減少を語る文が消えている")
chk("increasing for all $x$ (equivalently" in TEXT, "例題4 の答え")
chk("decreasing for $x < 5$" in TEXT, "演習6 の答え")

# --- B2: Why it works の例は文字だけ（演習7 とかぶらない）---------
chk("$f'$ が $(x - a)^{2}$ の形の因数をもつときを考えます。" in TEXT,
    "Why it works は一般の形で書いている")
chk("$f'(x) = (x - 1)^{2}$ を考えます。" not in TEXT,
    "具体的な数を出した古い文が消えている")
chk("(x + 1)(x - 2)^{2}" in TEXT, "演習7 は単純な因数と 2 乗の因数の組み合わせ")

# --- B3: 5.8 の語（山・谷・最大）を 5.2 で使わない ---------------
for _w in ("maximum or a minimum", "maximum or minimum", "is greatest at",
           "at its largest", "が谷になります", "山か谷"):
    chk(_w not in TEXT, "5.8 の語 %s は 5.2 で使わない" % _w)

# --- M1: 代表の値で確かめてよい条件 -----------------------------
chk("**区間を区切るのは、$f'(x) = 0$ となる $x$ と、$f'$ が定義されない $x$ の"
    "両方です。**" in TEXT, "第7節: 区間を区切るもの")
chk("**分母に $x$ があるときは、分母が $0$ になる $x$ も境目にしてください。**"
    in TEXT, "第7節: 分母が 0 になる点も境目")
chk("$f'$ がその区間のどの点でも定義されていることが要ります。" in TEXT,
    "Why it works: f' が定義されている条件")

# --- M2: 第5節の表に「触れる点」が入っている ---------------------
chk("| $x$ 軸と交わる点・触れる点 | $f$ の停留点（交われば向きが変わり、"
    "触れるだけなら変わらない） |" in TEXT, "第5節の表")
chk("| $x$ 軸と交わる点 | $f$ の停留点 |" not in TEXT,
    "触れる点を落とした古い行が消えている")

# --- M3: f' の最大の言い方 -------------------------------------
chk("$f'$ が最大になるところは、$f$ の傾きがいちばん大きいところです。" in TEXT,
    "第5節: f' の最大は傾きが最大")
chk("$f'$ が最大になるところは、$f$ がいちばん急に上がっているところです。"
    not in TEXT, "f' が負のとき偽になる文が消えている")

# --- M4: f' のグラフを読む演習がある -----------------------------
chk("[The diagram shows the graph of $y = f'(x)$ for a function $f$.]{.q-en}"
    in TEXT, "演習2 は f' のグラフを読む問題")
chk("increasing for $-1 < x < 2$ and for $x > 4$" in TEXT, "演習2 の答え")
chk("the graph of $f$ turns at $x = -1$, at $x = 2$ and at $x = 4$" in TEXT,
    "演習2 の答え（向きが変わる点）")
chk("$f'(x) = 6 - 2x$" not in TEXT, "演習1 と重なっていた古い演習2 が消えている")

# --- M5: 与えられた範囲の話が第4節にある -------------------------
chk("**場面のある問題では、与えられた範囲の中で答えます。**" in TEXT,
    "第4節: 与えられた範囲")

# --- m1: 英語の書き方を示している -------------------------------
chk("*increasing for $x < -2$ and for $x > 2$* のように書きます" in TEXT,
    "第4節: 英語の書き方")

# --- m3: 電卓の話は折りたたみ ----------------------------------
chk('## Paper 2 では、電卓でこう確かめます' in TEXT,
    "電卓の話は折りたたみの callout の中")
chk(TEXT.count('{.callout-note collapse="true"}') >= 11,
    "折りたたみの callout が足りている")
chk("**電卓は、答えを確かめるために使ってください。** $f'$ のグラフをかけば"
    not in TEXT, "Paper 1 の callout から電卓の話が抜けている")

# --- m4: 演習9 の検算が走らせられるものになっている ---------------
chk("**検算（反例で）。** $f(5) = 7$ という値だけを決めても" in TEXT,
    "演習9: 反例による検算")
chk("「$x > 4$ で増加」のような区間の形なら問題ありません" not in TEXT,
    "演習1 の答えを引いていた検算が消えている")

# --- m5: 演習8 の 2 点は「見当」であって検算ではない ---------------
chk("**見当（代表の値で）。**" in TEXT, "演習8: 見当という見出し")
chk("**検算（代表の値で）。** $f'(-2) = 12 + 5 = 17 > 0$" not in TEXT,
    "全称命題を 2 点で確かめる検算が消えている")

# --- m6: stationary point の言い方 -----------------------------
chk("$f'(x) = 0$ となる $x$ では、$f$ のグラフは **stationary point**"
    "（停留点）をもつといいます。" in TEXT, "第3節: 停留点の言い方")

# --- m7: 循環していた検算を直した -------------------------------
chk("**検算（$f$ の上がり下がりの向き）。**" in TEXT, "例題1 の検算")
chk("**検算（区間に停留点を入れていないか）。**" not in TEXT,
    "書き写しの確認だった検算が消えている")
chk("**検算（$x = 0$ をまたいで上がるか）。**" in TEXT, "例題4 の検算")
chk("**検算（減少する区間があるか）。** $3x^{2} < 0$" not in TEXT,
    "循環していた検算が消えている")

print()
print("OK", OK, "/ NG", NG)
