# -*- coding: utf-8 -*-
"""AA SL 5.8b のページを検算する。

    python3 figs/aa-sl/check_aasl_5_8b.py
"""
import os
import re

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
QMD = os.path.join(ROOT, "aa-sl", "05-calculus", "aasl-5-8b.qmd")
FIGP = os.path.join(HERE, "make_aasl_5_8b.py")

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


def d1(f):
    return sp.simplify(sp.diff(f, X))


def d2(f):
    return sp.simplify(sp.diff(f, X, 2))


def same(a, b):
    return sp.simplify(sp.nsimplify(a) - sp.nsimplify(b)) == 0


def stat(f):
    return sorted(sp.solve(sp.Eq(d1(f), 0), X))


# ══════════════════════════════════════════════════════════
# 1. ページの骨組み
# ══════════════════════════════════════════════════════════
chk(TEXT.startswith("---\nsidebar: aa-sl\n---\n"), "front matter")
in_text("# SL 5.8b — Optimization（最適化） {#sec-aasl-5-8b}", "見出し")

for _h in ("## What you should be able to do", "## The idea",
           "## Why it works", "## Worked examples", "## Common errors",
           "## Exercises"):
    in_text(_h, "節 " + _h)
not_in_text("## Using your GDC", "Topic 5 に GDC の節は置かない")

_secs = re.findall(r"^### (\d)\. .*\{#([a-z0-9-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 8)],
    "### の番号 1..7: %s" % [s[0] for s in _secs])
chk([s[1] for s in _secs] == ["what", "steps", "onevariable", "domain",
                             "justify", "context", "common"],
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

in_text("(img/aasl-5-8b-idea.svg){#fig-aasl58b-idea width=100%}", "図の埋め込み")
in_text("@fig-aasl58b-idea (a)", "図 (a) の参照")
in_text("@fig-aasl58b-idea (b)", "図 (b) の参照")

for _w in ("そのとおり", "もちろん", "簡単です", "自明", "当たり前", "明らか", "当然"):
    not_in_text(_w, "禁止語 " + _w)
for _w in ("得点になりません", "点になりません", "減点されます"):
    not_in_text(_w, "採点の断定 " + _w)

# ══════════════════════════════════════════════════════════
# 2. 引用・公式集・となりのページとの境目
# ══════════════════════════════════════════════════════════
_quotes = re.findall(r"^> (.*)$", TEXT, re.M)
chk(_quotes == [], "SL 5.8 にシラバスの引用はない: %s" % _quotes)

# シラバスが挙げた題材（profit, area, volume）がそろっている
for _w in ("利益", "面積", "体積"):
    in_text(_w, "題材 " + _w)
# 5.9 / 5.10 / 5.11 の語は漏らさない
for _w in ("速度", "加速度", "変位", "道のり", "積分", "不定積分", "定積分"):
    not_in_text(_w, "先のページの語 " + _w)
in_text("[SL 5.8a](aasl-5-8a.qmd#secondtest)", "5.8a の判定への参照")
in_text("[SL 5.8a](aasl-5-8a.qmd#stationary)", "5.8a の停留点への参照")

for _r in ("{#tbl-aasl58b-steps}", "{#tbl-aasl58b-two}",
           "{#tbl-aasl58b-justify}", "{#tbl-aasl58b-kinds}"):
    in_text(_r, "参照 " + _r)
for _a in ("aasl-5-3.qmd#negative", "aasl-5-6b.qmd#withchain", "aasl-5-6a.qmd"):
    in_text(_a, "参照 " + _a)

# ══════════════════════════════════════════════════════════
# 3. 図
# ══════════════════════════════════════════════════════════
in_fig('"(a) The six steps"', "図 (a) の題")
in_fig('"(b) An open box made from a square sheet"', "図 (b) の題")
in_fig('"state the domain"', "図 (a) の 4 歩目")
in_fig('"solve $f\'(x) = 0$, then justify max or min"', "図 (a) の 5 歩目")
in_fig('"$a - 2x$"', "図 (b) の寸法")
in_fig("the base disappears when $2x$ reaches $a$", "図 (b) の観察")
chk("0 < x < \\frac{a}{2}" not in FIG, "図に演習6 の答えを出さない")
in_fig('ax2.set_aspect("equal", adjustable="box")', "図 (b) は縦横比を保つ")
_figmath = " ".join(re.findall(r"\$([^$]*)\$", FIGCODE))
for _v in ("24", "12", "1024", "500", "2000"):
    chk(_v not in _figmath, "図の数式に具体的な数 %s は出さない" % _v)
for _bad in ("\\le ", "\\ge ", "\\lvert", "\\rvert", "\\begin{pmatrix}",
             "\\bigl", "\\bigr", "\\Box"):
    chk(_bad not in FIGCODE, "図に mathtext が読めない記法: " + _bad)

# ══════════════════════════════════════════════════════════
# 4. 例題
# ══════════════════════════════════════════════════════════
# 例題1  まわり 40、面積最大
_A1 = X * (20 - X)
chk(same(_A1, 20 * X - X ** 2), "例題1 の式")
chk(stat(_A1) == [10], "例題1 の停留点")
eq(d2(_A1), -2, "例題1 の f''")
eq(_A1.subs(X, 10), 100, "例題1 の最大値")
eq(_A1.subs(X, 9), 99, "例題1 A(9)")
eq(_A1.subs(X, 11), 99, "例題1 A(11)")
eq(2 * 10 + 2 * 10, 40, "例題1 まわりの長さ")
in_text("A = 100 \\text{ m}^{2}", "例題1 の答え")

# 例題2  24 cm の板
_V2 = X * (24 - 2 * X) ** 2
chk(same(d1(_V2), (24 - 2 * X) * (24 - 6 * X)), "例題2 の導関数の因数分解")
chk(sorted(sp.solve(sp.Eq(d1(_V2), 0), X)) == [4, 12], "例題2 の停留点")
eq(_V2.subs(X, 4), 1024, "例題2 の最大値")
eq(_V2.subs(X, 3), 972, "例題2 V(3)")
eq(_V2.subs(X, 5), 980, "例題2 V(5)")
eq(d1(_V2).subs(X, 3), 108, "例題2 V'(3)")
eq(d1(_V2).subs(X, 5), -84, "例題2 V'(5)")
eq(24 - 2 * 12, 0, "例題2 x=12 では底面が 0")
chk(same(sp.expand((24 - 2 * X) * (24 - 6 * X)),
         12 * X ** 2 - 192 * X + 576), "例題2 の展開")
in_text("V = 1024 \\text{ cm}^{3}", "例題2 の答え")

# 例題3  利益
_P3 = 60 * X - X ** 2 - 500
chk(stat(_P3) == [30], "例題3 の停留点")
eq(d2(_P3), -2, "例題3 の f''")
eq(_P3.subs(X, 30), 400, "例題3 の最大利益")
eq(_P3.subs(X, 29), 399, "例題3 P(29)")
eq(_P3.subs(X, 31), 399, "例題3 P(31)")
eq((60 * sp.Symbol("t") - sp.Symbol("t") ** 2 - 500).subs(sp.Symbol("t"), 0),
   -500, "例題3 P(0)")

# 例題4  ふたのない箱、体積 500
_S4 = X ** 2 + 2000 / X
chk(same(X ** 2 + 4 * X * (500 / X ** 2), _S4), "例題4 の表面積の式")
chk(stat(_S4) == [10], "例題4 の停留点")
chk(same(d2(_S4), 2 + 4000 / X ** 3), "例題4 の f''")
chk(d2(_S4).subs(X, 10) > 0, "例題4 f'' > 0")
eq(_S4.subs(X, 10), 300, "例題4 S(10)")
eq(_S4.subs(X, 8), 314, "例題4 S(8)")
eq(_S4.subs(X, 20), 500, "例題4 S(20)")
eq(sp.Integer(500) / 100, 5, "例題4 高さ")
eq(100 * 5, 500, "例題4 体積にもどる")
in_text("S = x^{2} + \\dfrac{2000}{x}", "例題4 の式")

# ══════════════════════════════════════════════════════════
# 5. 演習
# ══════════════════════════════════════════════════════════
_E1 = X * (30 - X)
chk(stat(_E1) == [15], "演習1 の停留点")
eq(d2(_E1), -2, "演習1 の f''")
eq(_E1.subs(X, 15), 225, "演習1 の最大面積")
eq(_E1.subs(X, 14), 224, "演習1 A(14)")
eq(_E1.subs(X, 16), 224, "演習1 A(16)")

_E2 = 2 * X + 72 / X
chk(same(_E2, 2 * X + 2 * (36 / X)), "演習2 の式")
chk(stat(_E2) == [6], "演習2 の停留点")
chk(same(d2(_E2), 144 / X ** 3), "演習2 の f''")
eq(_E2.subs(X, 6), 24, "演習2 の最小まわり")
eq(_E2.subs(X, 4), 26, "演習2 P(4)")
eq(_E2.subs(X, 9), 26, "演習2 P(9)")
eq(sp.Integer(36) / 6, 6, "演習2 もう片方の辺")

_h3 = (150 - 2 * X ** 2) / (4 * X)
_E3 = (75 * X - X ** 3) / 2
chk(same(X ** 2 * _h3, _E3), "演習3 の体積の式")
chk(same(2 * X ** 2 + 4 * X * _h3, 150), "演習3 の表面積は 150")
chk(same(d1(_E3), (75 - 3 * X ** 2) / 2), "演習3 の導関数")
chk(stat(_E3) == [5], "演習3 の停留点")
chk(same(d2(_E3), -3 * X), "演習3 の f''")
chk(d2(_E3).subs(X, 5) < 0, "演習3 f''(5) < 0")
eq(_E3.subs(X, 5), 125, "演習3 の最大体積")
eq(_E3.subs(X, 4), 118, "演習3 V(4)")
eq(_E3.subs(X, 6), 117, "演習3 V(6)")
eq(_h3.subs(X, 5), 5, "演習3 の高さ")
eq(6 * 25, 150, "演習3 立方体の表面積")

_p = sp.Symbol("p", positive=True)
_E4 = _p * (60 - 2 * _p) - 100
chk(same(sp.expand(_E4), 60 * _p - 2 * _p ** 2 - 100), "演習4 の利益の式")
chk(sorted(sp.solve(sp.Eq(sp.diff(_E4, _p), 0), _p)) == [15], "演習4 の停留点")
eq(sp.diff(_E4, _p, 2), -4, "演習4 の f''")
eq(_E4.subs(_p, 15), 350, "演習4 の最大利益")
eq(_E4.subs(_p, 14), 348, "演習4 P(14)")
eq(_E4.subs(_p, 16), 348, "演習4 P(16)")
eq((60 - 2 * _p).subs(_p, 15), 30, "演習4 p=15 で売れる個数")
eq(15 * 30 - 100, 350, "演習4 売上から運営費を引く")
chk(sp.solve(sp.Eq(60 - 2 * _p, 0), _p) == [30], "演習4 の定義域の端")

_E5 = X * (200 - 2 * X)
chk(stat(_E5) == [50], "演習5 の停留点")
eq(d2(_E5), -4, "演習5 の f''")
eq(_E5.subs(X, 50), 5000, "演習5 の最大面積")
eq(_E5.subs(X, 49), 4998, "演習5 A(49)")
eq(_E5.subs(X, 51), 4998, "演習5 A(51)")
eq(2 * 50 + 100, 200, "演習5 柵の長さ")
eq(200 - 2 * 50, 100, "演習5 もう片方の辺")

# 演習6  定義域
_V6 = X * (10 - 2 * X) ** 2
eq(_V6.subs(X, 6), 24, "演習6 定義域の外でも数は出る")
eq(10 - 2 * 5, 0, "演習6 x=5 では底面が 0")

_E8 = 3 * X + 1200 / X
chk(stat(_E8) == [20], "演習8 の停留点")
chk(same(d2(_E8), 2400 / X ** 3), "演習8 の f''")
eq(_E8.subs(X, 20), 120, "演習8 の最小費用")
eq(_E8.subs(X, 10), 150, "演習8 C(10)")
eq(_E8.subs(X, 40), 150, "演習8 C(40)")

_E9 = 2 * X * (12 - X ** 2)
chk(same(_E9, 24 * X - 2 * X ** 3), "演習9 の式")
chk(stat(_E9) == [2], "演習9 の停留点")
chk(same(d2(_E9), -12 * X), "演習9 の f''")
eq(_E9.subs(X, 2), 32, "演習9 の最大面積")
eq(_E9.subs(X, 1), 22, "演習9 A(1)")
eq(_E9.subs(X, 3), 18, "演習9 A(3)")
chk(same(sp.sqrt(12), 2 * sp.sqrt(3)), "演習9 の定義域の端")

_r = sp.Symbol("r", positive=True)
_E10 = sp.pi * _r ** 2 * (12 - _r)
chk(same(sp.expand(_E10), 12 * sp.pi * _r ** 2 - sp.pi * _r ** 3),
    "演習10 の式")
chk(same(sp.diff(_E10, _r), 3 * sp.pi * _r * (8 - _r)), "演習10 の導関数")
chk(sorted(sp.solve(sp.Eq(sp.diff(_E10, _r), 0), _r)) == [8],
    "演習10 の停留点（r > 0）")
chk(same(sp.diff(_E10, _r, 2), 24 * sp.pi - 6 * sp.pi * _r), "演習10 の f''")
eq(sp.diff(_E10, _r, 2).subs(_r, 8), -24 * sp.pi, "演習10 f''(8)")
eq(_E10.subs(_r, 8), 256 * sp.pi, "演習10 の最大体積")
eq(_E10.subs(_r, 7), 245 * sp.pi, "演習10 V(7)")
eq(_E10.subs(_r, 9), 243 * sp.pi, "演習10 V(9)")
eq(12 - 8, 4, "演習10 の高さ")

# ★ 例題・演習の答えを本文（例題より前）に出していないこと
for _v in ("100 \\text{ m}", "1024", "400", "300", "225", "24 \\text{ cm}",
           "125", "350", "5000", "120", "32", "256\\pi"):
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
chk(_nstmt >= 2, "ページの計算を %d 本たしかめた" % _nstmt)
print("  （計算 %d 本）" % _nstmt)

# ══════════════════════════════════════════════════════════
# 見直し（2026-09）で直したところ。もどってしまわないように。
# ══════════════════════════════════════════════════════════

# --- B-1: k/x の理由が、実際にその形を導いている ---------------------
chk("固定された量から求めた文字を、面積の式でもう一度かけ算するからです。" in TEXT,
    "Why it works: k/x の理由")
chk("**$r^{2}$ が $1$ つ約分されるので、分母が $r^{2}$ ではなく $r$ に"
    "なります。**" in TEXT, "Why it works: 約分で分母が r になる")
chk("片方の文字がもう片方の逆数に比例するからです。" not in TEXT,
    "誤りだった理由づけが消えている")
_r0 = sp.Symbol("r", positive=True)
_V0 = sp.Symbol("V", positive=True)
chk(sp.simplify(2 * sp.pi * _r0 * (_V0 / (sp.pi * _r0 ** 2)) - 2 * _V0 / _r0)
    == 0, "円柱の側面積は 2V/r")

# --- B-2: 演習9 の問題文が成り立つ ------------------------------------
chk("The rectangle is symmetrical about the $y$-axis, so its upper vertices "
    "are $(-x,\\ 12 - x^{2})$ and $(x,\\ 12 - x^{2})$, where $x > 0$." in TEXT,
    "演習9: 対称と頂点を問題文で与えている")
chk("on the curve $y = 12 - x^{2}$, with $x > 0$. Find" not in TEXT,
    "成り立たない問題文が消えている")
chk("**検算（座標で）。**" in TEXT, "演習9: 座標での検算")
chk("**検算（幅を $2$ 倍にしたか）。**" not in TEXT, "循環していた検算が消えている")

# --- M-1(a)(b): 本文の例が例題と重ならない ------------------------------
chk("「$x = 9$ は $0 < x < 7$ に入らないので、この場面には合いません」" in TEXT,
    "第4節: 例題2 と重ならない例")
chk("$A = x(14 - x)$ は $x = 20$ でも計算できますが" in TEXT,
    "Why it works: 例題1 と重ならない例")
chk("「$x = 12$ は $0 < x < 12$ に入らない" not in TEXT, "例題2 の答えが消えている")
chk("$A = x(20 - x)$ は $x = 30$ でも計算できますが" not in TEXT,
    "例題1 の式が消えている")

# --- M-2 + M-3: 第 5 節の但し書き ---------------------------------------
chk("**$f''(a) = 0$ になったときは、$f'$ の符号のほうを使います。**" in TEXT,
    "第5節: f''=0 のとき")
chk("**関数の値を左右で $1$ つずつ調べるのは、検算であって判定ではありません。**"
    in TEXT, "第5節: 検算と判定のちがい")

# --- M-4: 例題2 が 3 歩目を飛ばしていない --------------------------------
chk("**$1$ 歩目から $3$ 歩目まで。**" in TEXT, "例題2: 3 歩目に名前がある")
chk("**この時点で、変数は $x$ だけになっています。**" in TEXT,
    "例題2: 変数が 1 つになったと書いている")

# --- M-5 + M-7: 個数を連続量として扱う断りと、解答例の定義域 ---------------
chk("**個数はほんとうは整数ですが、微分するために、いったん $x$ を連続な量として"
    "扱います。**" in TEXT, "例題3: 連続量として扱う断り")
chk("$$P(x) = 60x - x^{2} - 500, \\qquad x \\geq 0$$" in TEXT,
    "例題3 の解答例に定義域")

# --- M-6: 演習3 が「ふたのある箱」になった --------------------------------
chk("A closed box has a square base of side $x$ cm and a total surface area "
    "of $150$ cm$^{2}$." in TEXT, "演習3: ふたのある箱")
chk("V = \\dfrac{75x - x^{3}}{2}" in TEXT, "演習3 の体積の式")
chk("An open box is made from a square sheet of card of side $12$ cm"
    not in TEXT, "例題2 と同型だった演習3 が消えている")

# --- M-8: 演習10 の解答例が r = 0 を捨てている ------------------------------
chk("r = 0 \\text{ or } r = 8" in TEXT, "演習10: 2 つの解を書いている")
chk("*$r = 0$ is outside the domain, so it is rejected*" in TEXT,
    "演習10: r=0 を捨てる")

# --- M-9: 演習6・7 で x と条件が定義されている -------------------------------
chk("by cutting a square of side $x$ cm from each corner and folding up the "
    "sides. Its volume, in cm$^{3}$, is $V = x(10 - 2x)^{2}$." in TEXT,
    "演習6: x の定義")
chk("A rectangle has a perimeter of $48$ cm." in TEXT, "演習7: まわりの長さ")
chk("where $x$ cm is one side" in TEXT, "演習7: x の定義")
chk("*answer the question asked: the area, $A = 144$ cm$^{2}$, not the value "
    "of $x$*" in TEXT, "演習7 の答えに単位")
eq(sp.Integer(12) * 12, 144, "演習7 の面積")
eq(2 * 24, 48, "演習7 のまわりの長さ")

# --- M-11: 需要の式から利益を作る演習がある -----------------------------------
chk("At this price it sells $60 - 2p$ toys each day." in TEXT,
    "演習4: 需要の式")
chk("Show that the daily profit, in dollars, is $P = 60p - 2p^{2} - 100$."
    in TEXT, "演習4: Show that")
chk("A shop sells $x$ items each day." not in TEXT,
    "式が与えられていた古い演習4 が消えている")

# --- m-3: 地の文の記号 ---------------------------------------------------
chk("$\\dfrac{d^{2}A}{dx^{2}}$ が負なので、$x = 10$ で極大です。" in TEXT,
    "例題1: 記号が A")
chk("$P''$ が負なので、$x = 30$ で極大です。" in TEXT, "例題3: 記号が P")

# --- m-4: 因数分解の検算にくらべる相手がある ---------------------------------
chk("**検算（別の道で）。**" in TEXT, "例題2: 別の道での検算")
chk(sp.expand(X * (24 - 2 * X) ** 2) == 4 * X ** 3 - 96 * X ** 2 + 576 * X,
    "例題2 の展開")

# --- m-6: 第 7 節の表に「面積が制約条件」の行がある ----------------------------
chk("| 長方形の囲い | 面積 | まわりの長さ |" in TEXT, "第7節: 面積が制約条件の行")

# --- m-7: 演習10 の体積の検算 -------------------------------------------------
chk("**検算（体積）。** $V(8) = \\pi \\times 64 \\times 4 = 256\\pi$ ✓" in TEXT,
    "演習10: 体積の検算")

# --- m-8: 第 2 節の表が図と重ならない ------------------------------------------
chk("| 歩 | すること | 抜けやすいところ |" in TEXT, "第2節: 抜けやすいところの列")

# --- m-12: 誤答例に「寸法を取りちがえる」がある --------------------------------
chk("## 図から式を作るときに、寸法を取りちがえる" in TEXT, "誤答例: 寸法")
chk("## 聞かれた量を、単位をつけて答えない" in TEXT, "誤答例: 量と単位")

# --- m-13: 演習10 が (a) (b) に分かれている -------------------------------------
chk("**(a)** [Show that its volume, in cm$^{3}$, is $V = \\pi r^{2}(12 - r)$.]"
    in TEXT, "演習10 (a)")
chk("**(b)** [Find the value of $r$ that gives the largest volume.]{.q-en}"
    in TEXT, "演習10 (b)")

print()
print("OK", OK, "/ NG", NG)
