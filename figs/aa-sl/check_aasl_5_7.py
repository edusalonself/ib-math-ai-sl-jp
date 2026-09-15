# -*- coding: utf-8 -*-
"""AA SL 5.7 のページを検算する。

    python3 figs/aa-sl/check_aasl_5_7.py
"""
import os
import re

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
QMD = os.path.join(ROOT, "aa-sl", "05-calculus", "aasl-5-7.qmd")
FIGP = os.path.join(HERE, "make_aasl_5_7.py")
FIGP2 = os.path.join(HERE, "make_aasl_5_7_ex.py")

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
X = sp.Symbol("x", positive=True)
Z = sp.Symbol("z", real=True)


def d2(f):
    return sp.simplify(sp.diff(f, X, 2))


def d1(f):
    return sp.simplify(sp.diff(f, X))


def same(a, b):
    return sp.simplify(sp.nsimplify(a) - sp.nsimplify(b)) == 0


# ══════════════════════════════════════════════════════════
# 1. ページの骨組み
# ══════════════════════════════════════════════════════════
chk(TEXT.startswith("---\nsidebar: aa-sl\n---\n"), "front matter")
in_text("# SL 5.7 — The second derivative（第 2 次導関数） {#sec-aasl-5-7}",
        "見出し")

for _h in ("## What you should be able to do", "## The idea",
           "## Why it works", "## Worked examples", "## Common errors",
           "## Exercises"):
    in_text(_h, "節 " + _h)
not_in_text("## Using your GDC", "Topic 5 に GDC の節は置かない")

_secs = re.findall(r"^### (\d)\. .*\{#([a-z0-9-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 8)],
    "### の番号 1..7: %s" % [s[0] for s in _secs])
chk([s[1] for s in _secs] == ["again", "notation", "meaning", "sign",
                             "shape", "identify", "zero"],
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
    "callout-important 0（SL 5.7 は公式集にない）")
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

in_text("(img/aasl-5-7-idea.svg){#fig-aasl57-idea width=100%}", "図1 の埋め込み")
in_text("(img/aasl-5-7-ex.svg){#fig-aasl57-ex width=100%}", "図2 の埋め込み")
in_text("@fig-aasl57-idea (a)", "図1 (a) の参照")
in_text("@fig-aasl57-idea (b)", "図1 (b) の参照")

for _w in ("そのとおり", "もちろん", "簡単です", "自明", "当たり前", "明らか", "当然"):
    not_in_text(_w, "禁止語 " + _w)
for _w in ("得点になりません", "点になりません", "減点されます"):
    not_in_text(_w, "採点の断定 " + _w)

# ══════════════════════════════════════════════════════════
# 2. 引用・公式集・となりのページとの境目
# ══════════════════════════════════════════════════════════
_quotes = re.findall(r"^> (.*)$", TEXT, re.M)
chk(_quotes == [], "SL 5.7 にシラバスの引用はない: %s" % _quotes)

# 5.8a の語彙が漏れていないこと（判定はこのページでしない）
chk(TEXT.count("concave") == 0, "concave は 5.8a の語")
chk(TEXT.count("inflexion") == 0, "inflexion は 5.8a の語")
chk(TEXT.count("変曲点") == 0, "変曲点は 5.8a の語: %d" % TEXT.count("変曲点"))
chk(TEXT.count("極大") == 0, "極大は 5.8a の語: %d" % TEXT.count("極大"))
chk(TEXT.count("極小") == 0, "極小は 5.8a の語: %d" % TEXT.count("極小"))
chk(TEXT.count("aasl-5-8a.qmd") >= 4, "5.8a への送り: %d"
    % TEXT.count("aasl-5-8a.qmd"))

for _r in ("{#eq-aasl57-chainarrow}", "{#eq-aasl57-notation}",
           "{#tbl-aasl57-notation}", "{#tbl-aasl57-what}",
           "{#tbl-aasl57-sign}", "{#tbl-aasl57-match}"):
    in_text(_r, "参照 " + _r)
for _a in ("aasl-5-2.qmd#sign", "aasl-5-3.qmd#power", "aasl-5-3.qmd#sum",
           "aasl-5-3.qmd#negative", "aasl-5-3.qmd#zeroderiv",
           "aasl-5-6a.qmd#standard", "aasl-5-6a.qmd#chain",
           "aasl-5-6a.qmd#rational", "aasl-5-6b.qmd#product",
           "aasl-5-6b.qmd#withchain", "aasl-5-1.qmd#rate", "aasl-5-9.qmd"):
    in_text(_a, "参照 " + _a)

# ══════════════════════════════════════════════════════════
# 3. 図
# ══════════════════════════════════════════════════════════
in_fig('"(a) The same $x$ on all three graphs"', "図1 (a) の題")
in_fig('"(b) What the sign of $f\'\'$ tells you"', "図1 (b) の題")
in_fig('"$f\'$ is increasing there"', "図1 (b) 増加")
in_fig('"$f\'$ is decreasing there"', "図1 (b) 減少")
in_fig("F = X ** 3 - 3 * X ** 2", "図1 の関数")
in_fig2("X ** 3 / 3 - X", "図2 の関数（C）")
in_fig2("X ** 2 - 1", "図2 の関数（A）")
in_fig2("2 * X", "図2 の関数（B）")
# 図1 の 3 本は、ほんとうに微分の関係にある
_t = sp.Symbol("t")
chk(sp.simplify(sp.diff(_t ** 3 - 3 * _t ** 2, _t) - (3 * _t ** 2 - 6 * _t))
    == 0, "図1 f' が合っている")
chk(sp.simplify(sp.diff(3 * _t ** 2 - 6 * _t, _t) - (6 * _t - 6)) == 0,
    "図1 f'' が合っている")
chk(sp.solve(sp.Eq(3 * _t ** 2 - 6 * _t, 0), _t) == [0, 2], "図1 f' の零点")
chk(sp.solve(sp.Eq(6 * _t - 6, 0), _t) == [1], "図1 f'' の零点")
# 図2 の 3 本
chk(sp.simplify(sp.diff(_t ** 3 / 3 - _t, _t) - (_t ** 2 - 1)) == 0,
    "図2 A は C の導関数")
chk(sp.simplify(sp.diff(_t ** 2 - 1, _t) - 2 * _t) == 0, "図2 B は A の導関数")
chk(sorted(sp.solve(sp.Eq(_t ** 2 - 1, 0), _t)) == [-1, 1], "図2 A の零点")
chk(sp.solve(sp.Eq(2 * _t, 0), _t) == [0], "図2 B の零点")
for _bad in ("\\le ", "\\ge ", "\\lvert", "\\rvert", "\\begin{pmatrix}",
             "\\bigl", "\\bigr", "\\Box"):
    chk(_bad not in FIGCODE, "図に mathtext が読めない記法: " + _bad)

# ══════════════════════════════════════════════════════════
# 4. 例題
# ══════════════════════════════════════════════════════════
# 例題1
_f1 = X ** 5 - 4 * X ** 3 + 7 * X
chk(same(d1(_f1), 5 * X ** 4 - 12 * X ** 2 + 7), "例題1 の f'")
chk(same(d2(_f1), 20 * X ** 3 - 24 * X), "例題1 の f''")
eq(5 * 4, 20, "例題1 の係数 1")
eq(12 * 2, 24, "例題1 の係数 2")
eq(d2(_f1).subs(X, 1), -4, "例題1 f''(1)")
eq(d1(_f1).subs(X, 0), 7, "例題1 f'(0)")
eq(d1(_f1).subs(X, 1), 0, "例題1 f'(1)")
chk(d1(_f1).subs(X, 1) < d1(_f1).subs(X, 0), "例題1 f' は 0 から 1 で減る")
in_text("f''(x) = 20x^{3} - 24x", "例題1 の答え")

# 例題2
_f2 = X * sp.exp(X)
chk(same(d1(_f2), X * sp.exp(X) + sp.exp(X)), "例題2 の dy/dx")
chk(same(d2(_f2), X * sp.exp(X) + 2 * sp.exp(X)), "例題2 の d2y/dx2")
chk(same(d2(_f2), sp.exp(X) * (X + 2)), "例題2 のくくった形")
eq(d2(_f2).subs(X, 0), 2, "例題2 x=0 での値")
eq(d1(_f2).subs(X, 0), 1, "例題2 dy/dx(0)")
eq(d1(_f2).subs(X, 1), 2 * sp.E, "例題2 dy/dx(1)")
chk(abs(float(2 * sp.E) - 5.4) < 0.05, "例題2 2e ≈ 5.4")
in_text("e^{x}(x + 2)", "例題2 の答え")

# 例題3
_f3 = X ** 3 - 6 * X ** 2 + 5
chk(same(d1(_f3), 3 * X ** 2 - 12 * X), "例題3 の f'")
chk(same(d2(_f3), 6 * X - 12), "例題3 の f''")
chk(sp.solve(sp.Eq(6 * Z - 12, 0), Z) == [2], "例題3 f''=0 は x=2")
eq(6 * 2 - 12, 0, "例題3 代入")
eq((6 * X - 12).subs(X, 1), -6, "例題3 f''(1)")
eq((6 * X - 12).subs(X, 3), 6, "例題3 f''(3)")
in_text("f''(x) = 6x - 12", "例題3 の答え")

# 例題4（図2 の見分け）
in_text("*$R = f$, $P = f'$, $Q = f''$*", "例題4 の答え")

# ══════════════════════════════════════════════════════════
# 5. 演習の答え
# ══════════════════════════════════════════════════════════
_E = [("演習1", X ** 4 - 2 * X ** 2 + 3, 4 * X ** 3 - 4 * X, 12 * X ** 2 - 4),
      ("演習2", 2 * X ** 3 - 5 * X, 6 * X ** 2 - 5, 12 * X),
      ("演習3", sp.sqrt(X) + sp.log(X),
       R(1, 2) * X ** R(-1, 2) + 1 / X,
       R(-1, 4) * X ** R(-3, 2) - 1 / X ** 2),
      ("演習4", sp.sin(3 * X), 3 * sp.cos(3 * X), -9 * sp.sin(3 * X)),
      ("演習6", X ** 4 - 6 * X ** 2, 4 * X ** 3 - 12 * X, 12 * X ** 2 - 12),
      ("演習8", sp.exp(-X), -sp.exp(-X), sp.exp(-X)),
      ("演習9", sp.sin(X), sp.cos(X), -sp.sin(X)),
      ("演習10", X ** 2 + 5 * X, 2 * X + 5, sp.Integer(2))]
for _name, _f, _fp, _fpp in _E:
    chk(same(d1(_f), _fp), "%s の 1 回目" % _name)
    chk(same(d2(_f), _fpp), "%s の 2 回目" % _name)

eq((12 * X ** 2 - 4).subs(X, 0), -4, "演習1 f''(0)")
eq((4 * X ** 3 - 4 * X).subs(X, R(-1, 2)), R(3, 2), "演習1 f'(-0.5)")
eq((4 * X ** 3 - 4 * X).subs(X, R(1, 2)), R(-3, 2), "演習1 f'(0.5)")
eq(2 * 3, 6, "演習2 の係数 1")
eq(6 * 2, 12, "演習2 の係数 2")
eq((6 * X ** 2 - 5).subs(X, -2), 19, "演習2 dy/dx(-2)")
eq((6 * X ** 2 - 5).subs(X, -1), 1, "演習2 dy/dx(-1)")
eq(R(-1, 2) - 1, R(-3, 2), "演習3 の指数")
eq(R(1, 2) * R(-1, 2), R(-1, 4), "演習3 の係数")
chk(same(R(1, 2) * X ** R(-1, 2), 1 / (2 * sp.sqrt(X))), "演習3 f' の形")
eq(3 * 3, 9, "演習4 の係数")
eq((-9 * sp.sin(3 * X)).subs(X, 0), 0, "演習4 x=0")
eq((3 * sp.cos(3 * X)).subs(X, 0), 3, "演習4 dy/dx(0) は最大")
chk(float(3 * sp.cos(sp.Rational(1, 10))) < 3, "演習4 x=0 で最大")
chk(sorted(sp.solve(sp.Eq(12 * Z ** 2 - 12, 0), Z)) == [-1, 1],
    "演習6 f''=0 は x=±1")
eq(12 * 1 - 12, 0, "演習6 代入")
eq(sp.diff(sp.Integer(4), X), 0, "演習7 定数の導関数")
chk(same(d1(4 * X + Z), 4), "演習7 f=4x+c なら f'=4")
chk(same(d2(4 * X + Z), 0), "演習7 f''=0")
eq((-1) * (-1), 1, "演習8 マイナス 2 つ")
eq(sp.exp(-X).subs(X, 0), 1, "演習8 f''(0)")
eq((-sp.exp(-X)).subs(X, 0), -1, "演習8 f'(0)")
chk(abs(float(-sp.exp(-1)) + 0.37) < 0.005, "演習8 f'(1) ≈ -0.37")
chk(float(-sp.exp(-1)) > float(-1), "演習8 f' は増えている")
_pi2 = sp.pi / 2
eq((-sp.sin(X)).subs(X, _pi2), -1, "演習9 正しい答えの π/2 での値")
eq(sp.sin(_pi2), 1, "演習9 生徒の答えの π/2 での値")
chk(same(sp.diff(sp.sin(X), X, 4), sp.sin(X)), "演習9 4 回でもどる")
chk(not same(sp.diff(sp.sin(X), X, 2), sp.sin(X)), "演習9 2 回ではもどらない")
eq((2 * X + 5).subs(X, 0), 5, "演習10 f'(0)")
eq((2 * X + 5).subs(X, 1), 7, "演習10 f'(1)")
eq(7 - 5, 2, "演習10 増え方")

# ★ 例題・演習の答えを本文（例題より前）に出していないこと
for _v in ("20x^{3} - 24x", "e^{x}(x + 2)", "6x - 12", "12x^{2} - 4",
           "= 12x$$", "-\\frac{1}{4}x^{-\\frac{3}{2}}", "-9\\sin(3x)",
           "-\\frac{1}{x^{2}}", "12x^{2} - 12", "e^{-x}$$", "-\\sin x$$"):
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

# --- B1: 例題4 の問題文の前提 --------------------------------------
chk("The diagram shows the graphs of a function $f$, its derivative $f'$ and "
    "its second derivative $f''$, labelled P, Q and R in some order." in TEXT,
    "例題4: 前提が正しい問題文")
chk("Each one is the derivative of one of the others." not in TEXT,
    "偽の前提が消えている")
chk("labelled A, B and C" not in TEXT, "古いラベルが消えている")
# 並べ方は 1 通りしか合わない
_P, _Q, _R = Z ** 2 - 1, 2 * Z, Z ** 3 / 3 - Z
_names = {"P": _P, "Q": _Q, "R": _R}
_ok = []
for _f in _names:
    for _g in _names:
        for _h in _names:
            if len({_f, _g, _h}) < 3:
                continue
            if (sp.simplify(sp.diff(_names[_f], Z) - _names[_g]) == 0
                    and sp.simplify(sp.diff(_names[_g], Z) - _names[_h]) == 0):
                _ok.append((_f, _g, _h))
chk(_ok == [("R", "P", "Q")], "例題4: 並べ方は R,P,Q だけ: %s" % _ok)

# --- B2: f'' > 0 から「上がりはじめる」は言えない --------------------
chk("**$f'' > 0$ だからといって、$f$ が上がりはじめるとはかぎりません。**"
    in TEXT, "第5節: 上がりはじめるとはかぎらない")
chk("$f(x) = e^{x}$ のように、$f'' > 0$ でずっと上がりつづける関数もあります。"
    in TEXT, "第5節: e^x の例")
chk("やがて上がりはじめ、その上がり方が急になっていきます。" not in TEXT,
    "無条件に偽の文が消えている")
chk(sp.simplify(sp.diff(sp.exp(X), X, 2) - sp.exp(X)) == 0, "e^x の f''")
chk(sp.diff(sp.exp(X), X, 2).subs(X, 0) > 0, "e^x は f'' > 0")
chk(sp.diff(sp.exp(X), X).subs(X, 0) > 0, "e^x は f' > 0（下がらない）")

# --- B3: 「いちばん急」の行が向きと範囲で限定されている ----------------
chk("| そのあたりでのぼり方がいちばん急なところ | 山（そのあたりでいちばん高い） |"
    in TEXT, "第6節: のぼり方の行")
chk("| そのあたりでくだり方がいちばん急なところ | 谷（そのあたりでいちばん低い） |"
    in TEXT, "第6節: くだり方の行")
chk("| いちばん急なところ | 山または谷 |" not in TEXT,
    "向きを言わない古い行が消えている")
chk("**急なところの読み方が使えるのは、グラフの途中にある場所だけです。**"
    in TEXT, "第6節: 端の但し書き")

# --- B4: 「x 軸と交わる」→「出会う」 --------------------------------
chk("| 水平なところ | $x$ 軸と出会う（横切るか、触れる） |" in TEXT,
    "第6節: 出会う")
chk("| 水平なところ | $x$ 軸と交わる |" not in TEXT, "交わるだけの行が消えている")
chk("[SL 5.2](aasl-5-2.qmd#zero)" in TEXT, "5.2 の触れるだけの節への参照")
chk(sp.solve(sp.Eq(3 * Z ** 2, 0), Z) == [0], "f'=3x^2 の零点は 1 つ")
chk((3 * Z ** 2).subs(Z, -1) > 0 and (3 * Z ** 2).subs(Z, 1) > 0,
    "f'=3x^2 は符号が変わらない")

# --- M1: 増減は区間で言う ------------------------------------------
chk("| ある範囲でずっと $f''(x) > 0$ | 増加している |" in TEXT,
    "第4節: 区間で言う表")
chk("**増加・減少は、区間で言います**（[SL 5.2](aasl-5-2.qmd#interval)）。"
    in TEXT, "第4節: 区間の但し書き")
chk("| $f''(x) > 0$ | 増えている |" not in TEXT, "点で言う古い行が消えている")

# --- M2: f'' の符号から f' の増減を答えさせる演習がある ---------------
chk("Find the values of $x$ for which $\\dfrac{dy}{dx}$ is increasing."
    in TEXT, "演習2(b): f' の増減")
chk("*$\\dfrac{dy}{dx}$ is increasing for $x > 0$*" in TEXT, "演習2(b) の答え")
chk(sp.solve(sp.Eq(12 * Z, 0), Z) == [0], "演習2 12x = 0 は x = 0")
chk((12 * Z).subs(Z, 1) > 0 and (12 * Z).subs(Z, -1) < 0, "演習2 符号")
eq((6 * X ** 2 - 5).subs(X, 1), 1, "演習2 dy/dx(1)")
eq((6 * X ** 2 - 5).subs(X, 2), 19, "演習2 dy/dx(2)")

# --- M3: グラフから読む演習がある -----------------------------------
chk("For a function $f$, the graph of $f'$ is a parabola which meets the "
    "$x$-axis at $x = 1$ and at $x = 3$, and which has its lowest point at "
    "$x = 2$." in TEXT, "演習5: グラフから読む")
chk("**(b)** *negative*" in TEXT, "演習5(b) の答え")
eq(sp.Rational(1 + 3, 2), 2, "演習5 対称の中点")
# 1 と 3 を零点、頂点 2 の放物線で、f''(1) < 0、f''(3) > 0
_par = (Z - 1) * (Z - 3)
chk(sp.diff(_par, Z).subs(Z, 1) < 0, "演習5 f''(1) < 0")
chk(sp.diff(_par, Z).subs(Z, 3) > 0, "演習5 f''(3) > 0")
chk(sp.solve(sp.Eq(sp.diff(_par, Z), 0), Z) == [2], "演習5 f''=0 は x=2")

# --- M4: 例題3 の検算が 5.8a の判定になっていない ---------------------
chk("**検算（$1$ 次式として）。**" in TEXT, "例題3: 1 次式としての検算")
chk("この符号から $f$ のグラフについて何が言えるかは、"
    "[SL 5.8a](aasl-5-8a.qmd) で扱います。" in TEXT, "例題3: 5.8a へ送る")
chk("**検算（符号の変わり方）。**" not in TEXT, "変曲点判定だった検算が消えている")

# --- M5: 単位の説明 -------------------------------------------------
chk("**単位は、微分するたびに横軸の単位で割られます。**" in TEXT, "第3節: 単位")
chk("**単位も $1$ 段ずれます。**" not in TEXT, "理由のない言い方が消えている")

# --- M6: 例題4 が Q を落としている -----------------------------------
chk("**Q は $x = 0$ でしか $0$ になりません。** だから Q は R の導関数では"
    "ありえません。残るのは P です。" in TEXT, "例題4: Q を落としている")
chk("graph Q is zero only at $x = 0$, so Q cannot be the derivative of R "
    "and P must be." in TEXT, "例題4 の model answer に Q の排除")
chk(sp.solve(sp.Eq(2 * Z, 0), Z) == [0], "Q の零点は 1 つ")

# --- M7: 循環的な検算を差しかえた --------------------------------------
chk("**検算（$x = -2$ で）。**" in TEXT, "例題2: x=-2 の検算")
chk("**検算（$2$ 回目でも規則が要る）。**" not in TEXT, "手順の再確認が消えている")
chk("**検算（もし $f''$ が $0$ でなかったら）。**" in TEXT, "演習7: 対偶の検算")
chk("**検算（$2$ 回でもどる理由）。**" in TEXT, "演習8: 理由つきの検算")
chk("**検算（$1$ 次式の微分）。**" in TEXT, "演習10: 1 次式の検算")
chk("**検算（$f'$ のグラフ）。** $f'(x) = 2x + 5$ は傾き $2$ の直線です"
    not in TEXT, "答えの言いかえだった検算が消えている")
# 例題2 の x = -2 の検算の中身
chk(sp.simplify(sp.diff(X * sp.exp(X), X) - sp.exp(X) * (X + 1)) == 0,
    "例題2 dy/dx = e^x(x+1)")
chk(float(2 * sp.exp(-3)) < float(sp.exp(-2)), "例題2 2e^{-3} < e^{-2}")
chk(float(sp.E) > 2, "例題2 e > 2")
eq((sp.exp(X) * (X + 1)).subs(X, -1), 0, "例題2 dy/dx(-1) = 0")
chk(float((sp.exp(X) * (X + 1)).subs(X, -3))
    > float((sp.exp(X) * (X + 1)).subs(X, -2)), "例題2 x=-2 が谷（左）")
chk(float((sp.exp(X) * (X + 1)).subs(X, -1))
    > float((sp.exp(X) * (X + 1)).subs(X, -2)), "例題2 x=-2 が谷（右）")

# --- m2: 次数の但し書き ----------------------------------------------
chk("$1$ 次以上のあいだは、微分するたびに次数が $1$ 下がります"
    "（定数を微分すると $0$ です）。" in TEXT, "第6節: 次数の但し書き")

# --- m4: 演習6 の参照先 -----------------------------------------------
chk("答えが $2$ つになることがあります（[第 6 節](#identify)）。" in TEXT,
    "演習6 の参照先")

# --- m5 + m6: 演習9 -----------------------------------------------------
chk("Explain what the student has done wrong, and write down the correct "
    "second derivative." in TEXT, "演習9: Explain")
chk("Identify the error and write down the correct second derivative."
    not in TEXT, "Identify の古い問題文が消えている")
chk("$f'(x) = \\cos x$ の値は $x = 0$ で $1$、$x = \\pi$ で $-1$ と減っている"
    in TEXT, "演習9: cos の値の引き合い")
eq(sp.cos(0), 1, "cos 0")
eq(sp.cos(sp.pi), -1, "cos π")

# --- m9: SL 2.3 への参照 ------------------------------------------------
chk("[SL 2.3](../02-functions/aasl-2-3.qmd)" in TEXT, "第6節: SL 2.3 へ")

# --- m12: 第 1 節の例が演習1 と重ならない ---------------------------------
chk("$f(x) = x^{6}$ なら $f'(x) = 6x^{5}$、もう $1$ 回微分して "
    "$f''(x) = 30x^{4}$ です。" in TEXT, "第1節の例")
chk(sp.simplify(sp.diff(X ** 6, X, 2) - 30 * X ** 4) == 0, "x^6 の f''")
chk("$f''(x) = 12x^{2}$ です。" not in TEXT, "演習1 と重なる例が消えている")

# --- m14: 図2 のラベルが P・Q・R ------------------------------------------
chk('("P", X ** 2 - 1' in FIG2, "図2 のラベル P")
chk('("Q", 2 * X' in FIG2, "図2 のラベル Q")
chk('("R", X ** 3 / 3 - X' in FIG2, "図2 のラベル R")
chk("labelled P, Q and R" in TEXT, "図2 の alt のラベル")

# --- 演習3 に ln x が入っている --------------------------------------------
chk("f(x) = \\sqrt{x} + \\ln x$, for $x > 0$" in TEXT, "演習3: √x + ln x")
chk("f''(x) = -\\frac{1}{4}x^{-\\frac{3}{2}} - \\frac{1}{x^{2}}" in TEXT, "演習3 の答え")
eq((R(1, 2) * X ** R(-1, 2) + 1 / X).subs(X, 1), R(3, 2), "演習3 f'(1)")
eq((R(1, 2) * X ** R(-1, 2) + 1 / X).subs(X, 4), R(1, 2), "演習3 f'(4)")

print()
print("OK", OK, "/ NG", NG)
