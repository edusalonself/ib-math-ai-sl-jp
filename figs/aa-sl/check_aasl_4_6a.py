# -*- coding: utf-8 -*-
"""AA SL 4.6a のページを検算する。

    python3 figs/aa-sl/check_aasl_4_6a.py
"""
import glob
import os
import re
import sys
from fractions import Fraction as F

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
QMD = os.path.join(ROOT, "aa-sl", "04-statistics-and-probability", "aasl-4-6a.qmd")
FIGP = os.path.join(HERE, "make_aasl_4_6a.py")

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


DICE = [(a, b) for a in range(1, 7) for b in range(1, 7)]


def prob(space, pred):
    return F(sum(1 for s in space if pred(s)), len(space))


# ══════════════════════════════════════════════════════════
# 1. ページの骨組み
# ══════════════════════════════════════════════════════════
chk(TEXT.startswith("---\nsidebar: aa-sl\n---\n"), "front matter")
in_text("# SL 4.6a — Combined events: Venn diagrams, tree diagrams and tables"
        "（事象の組み合わせ） {#sec-aasl-4-6a}", "見出し")

for _h in ("## What you should be able to do", "## The idea", "## Why it works",
           "## Worked examples", "## Common errors", "## Exercises"):
    in_text(_h, "節 " + _h)

_secs = re.findall(r"^### (\d)\. .*\{#([a-z-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 8)],
    "### の番号 1..7: %s" % [s[0] for s in _secs])
chk([s[1] for s in _secs] == ["and-or", "venn", "addition", "exclusive",
                              "table", "tree", "which"],
    "アンカー: %s" % [s[1] for s in _secs])

chk(len(re.findall(r"^\[\d+\]\{\.ex-no\}", TEXT, re.M)) == 10, "演習 10 問")
chk(TEXT.count("::: {#exm-") == 4, "例題 4 つ")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep 9 個")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳 14")
chk(TEXT.count("</details>") == 14, "details 閉じ 14")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例 14")
chk(len(re.findall(r"^---$", TEXT, re.M)) == 6, "行頭 --- は 6 本")
chk(TEXT.count("{.callout-warning}") == 7, "callout-warning 7（誤り 6 + 電卓 1）")
chk(TEXT.count("{.callout-important}") == 2, "callout-important 2（公式集 4.6 の 2 式）")
chk(TEXT.count("**検算") >= 12, "検算 12 以上: %d" % TEXT.count("**検算"))

# ::: の開閉
_d = 0
for _l in TEXT.split("\n"):
    _t = _l.strip()
    if _t.startswith(":::"):
        _d += -1 if _t[3:].strip() == "" else 1
chk(_d == 0, "::: の開閉が合う: %d" % _d)

# model answer は Explain/Justify/… の問いの数と同じ
_verbs = re.compile(r"Explain|Justify|Comment|Interpret|Identify|Describe|Suggest")
_qs = [q for q in re.findall(r"\[([^\[\]]*?)\]\{\.q-en\}", TEXT, re.S)
       if _verbs.search(q)]
chk(TEXT.count("{.model-answer}") == len(_qs),
    "model-answer %d = 問い %d" % (TEXT.count("{.model-answer}"), len(_qs)))
chk(len(_qs) == 8, "Explain 系の問いは 8: %d" % len(_qs))

# model answer は英語だけ、115 語以内
for _i, _m in enumerate(re.findall(r"\{\.model-answer\}(.*?):::", TEXT, re.S), 1):
    _b = _m.replace("**試験ではこう書く**", "")
    chk(len(_b.split()) <= 115, "model answer %d は 115 語以内" % _i)
    chk(not [c for c in _b if "぀" <= c <= "ヿ" or "一" <= c <= "鿿"],
        "model answer %d に日本語がない" % _i)

# 図の参照
in_text("(img/aasl-4-6a-idea.svg){#fig-aasl46a-idea width=100%}", "図の埋め込み")
in_text("@fig-aasl46a-idea (a)", "図 (a) の参照")
in_text("@fig-aasl46a-idea (b)", "図 (b) の参照")

# シラバスの引用はしない
chk("> " not in TEXT, "引用ブロックは使わない（4.6 に Not required はない）")
not_in_text("シラバス", "シラバスへの言及はしない")

# 禁止語
for _w in ("そのとおり", "もちろん", "簡単です", "自明"):
    not_in_text(_w, "禁止語 " + _w)

# ══════════════════════════════════════════════════════════
# 2. The idea —— ことばと記号
# ══════════════════════════════════════════════════════════
in_text("| $A \\cap B$ | $A$ **and** $B$（intersection） | 積事象 |", "cap の行")
in_text("| $A \\cup B$ | $A$ **or** $B$（union） | 和事象 |", "cup の行")
in_text("| $A'$ | **not** $A$（complement） | 余事象 |", "余事象の行")
in_text("**確率の \"or\" は「両方でもよい」を含みます。**", "or の非排他性")
in_text("**「少なくとも一方」と読みかえると、まちがえません。**", "少なくとも一方")
in_text("{#tbl-aasl46a-words}", "ことばの表")
in_text("{#tbl-aasl46a-regions}", "領域の表")
in_text("{#tbl-aasl46a-which}", "図の選び方の表")

# ══════════════════════════════════════════════════════════
# 3. combined events の式
# ══════════════════════════════════════════════════════════
in_text("P(A \\cup B) = P(A) + P(B) - P(A \\cap B)\n$$ {#eq-aasl46a-add}", "加法の式")
in_text("P(A \\cap B) = 0\n$$ {#eq-aasl46a-zero}", "排反の式")
in_text("P(A \\cup B) = P(A) + P(B)\n$$ {#eq-aasl46a-me}", "排反のときの和")
in_text("公式集の **4.6** の欄に *Combined events* として載っています", "公式集 4.6 combined")
in_text("公式集の **4.6** の欄に *Mutually exclusive events* として載っています",
        "公式集 4.6 mutually exclusive")
in_text("**ただし、使ってよいのは $A \\cap B$ が空のときだけです。**", "使う条件")

# 記号のままで加法定理を確かめる
_a, _b, _ab, _u = sp.symbols("a b ab u", positive=True)
eq((_a + _ab) / _u + (_b + _ab) / _u - _ab / _u, (_a + _b + _ab) / _u,
   "P(A)+P(B)-P(A∩B) = P(A∪B)（記号のまま）")

# ══════════════════════════════════════════════════════════
# 4. Why it works —— 樹形図でかける理由
# ══════════════════════════════════════════════════════════
in_text("赤玉 $3$ 個と青玉 $1$ 個の袋を考えます。", "Why it works の袋")
in_text("4 \\times 4 = 16", "16 とおり")
in_text("$3 \\times 3 = 9$ とおりなので、確率は $\\dfrac{9}{16}$", "9/16")
eq(4 * 4, 16, "4×4 = 16")
eq(F(3, 4) * F(3, 4), F(9, 16), "3/4 × 3/4 = 9/16")
eq(F(3 * 3, 4 * 4), F(9, 16), "数えても 9/16")
# ★ Why it works の数値が例題4・演習9 と重ならないこと
not_in_body("\\dfrac{4}{25}", "例題4(b) の答えは本文に出さない")
not_in_body("\\dfrac{16}{25}", "例題4(d) の答えは本文に出さない")
not_in_body("\\dfrac{17}{32}", "演習9 の答えは本文に出さない")
# ★ 図の数値も例題・演習と重ならないこと
import re as _re
_figlabels = sorted(_re.findall(r'"\$(\d+)\$"', FIGCODE))
chk(_figlabels == ["10", "12", "13", "15"],
    "図の Venn ラベルは 10/12/13/15 だけ: %s" % _figlabels)
for _n in ("$30$", "$18$", "$14$", "$40$", "$60$", "$20$"):
    chk(_n not in FIGCODE, "図に例題・演習の数 %s は出さない" % _n)
eq(15 + 10 + 12 + 13, 50, "図の Venn の合計は 50")
eq(F(1, 9) + F(2, 9) + F(2, 9) + F(4, 9), 1, "図の樹形図の枝先の合計は 1")

# ══════════════════════════════════════════════════════════
# 5. 例題1 —— Venn 図
# ══════════════════════════════════════════════════════════
_N, _F, _T, _B = 30, 18, 14, 6
eq(_F - _B, 12, "例題1 サッカーだけ")
eq(_T - _B, 8, "例題1 テニスだけ")
eq(_N - (_F + _T - _B), 4, "例題1 どちらでもない")
eq(_F + _T - _B, 26, "例題1 少なくとも一方")
eq(F(26, 30), F(13, 15), "例題1(b)")
eq(F(4, 30), F(2, 15), "例題1(c)")
eq(12 + 6 + 8 + 4, 30, "例題1 の 4 つの合計")
eq(F(13, 15) + F(2, 15), 1, "例題1 余事象")
chk(_F + _T > _N, "18+14 は 30 をこえる（だから足すだけでは誤り）")
in_text("30 - (12 + 6 + 8) = 30 - 26 = 4", "例題1(a) の引き算")
in_text("P(F \\cup T) = \\frac{12 + 6 + 8}{30} = \\frac{26}{30} = \\frac{13}{15}",
        "例題1(b)")
in_text("P((F \\cup T)') = \\frac{4}{30} = \\frac{2}{15}", "例題1(c)")

# ══════════════════════════════════════════════════════════
# 6. 例題2 —— カード 1..20
# ══════════════════════════════════════════════════════════
CARDS = list(range(1, 21))
_A2 = [x for x in CARDS if x % 3 == 0]
_B2 = [x for x in CARDS if x % 4 == 0]
_AB2 = [x for x in CARDS if x % 12 == 0]
chk(_A2 == [3, 6, 9, 12, 15, 18], "3 の倍数: %s" % _A2)
chk(_B2 == [4, 8, 12, 16, 20], "4 の倍数: %s" % _B2)
chk(_AB2 == [12], "12 の倍数: %s" % _AB2)
eq(F(len(_A2), 20), F(3, 10), "例題2(a) P(A)")
eq(F(len(_B2), 20), F(1, 4), "例題2(a) P(B)")
eq(F(len(_AB2), 20), F(1, 20), "例題2(b)")
eq(F(6 + 5 - 1, 20), F(1, 2), "例題2(c)")
_U2 = sorted(set(_A2) | set(_B2))
chk(_U2 == [3, 4, 6, 8, 9, 12, 15, 16, 18, 20], "例題2 の書き出し: %s" % _U2)
eq(len(_U2), 10, "書き出しは 10 個")
chk(F(6, 20) + F(5, 20) != F(10, 20), "引かないと合わない")
eq(F(11, 20) - F(10, 20), F(1, 20), "引き忘れると 1 個多い")
chk(24 > 20, "次の 12 の倍数 24 は 20 をこえる")
in_text("P(A) = \\frac{6}{20} = \\frac{3}{10}, \\qquad P(B) = \\frac{5}{20} "
        "= \\frac{1}{4}", "例題2(a)")
in_text("P(A \\cup B) = \\frac{6}{20} + \\frac{5}{20} - \\frac{1}{20} "
        "= \\frac{10}{20} = \\frac{1}{2}", "例題2(c)")
in_text("$3, 4, 6, 8, 9, 12, 15, 16, 18, 20$ の $10$ 個です", "例題2 の検算")

# ══════════════════════════════════════════════════════════
# 7. 例題3 —— さいころ 2 個の表
# ══════════════════════════════════════════════════════════
_A3 = lambda s: sum(s) >= 10
_B3 = lambda s: 6 in s
eq(sum(1 for s in DICE if _A3(s)), 6, "例題3 A のマス")
eq(sum(1 for s in DICE if _B3(s)), 11, "例題3 B のマス")
eq(sum(1 for s in DICE if _A3(s) and _B3(s)), 5, "例題3 A∩B のマス")
eq(sum(1 for s in DICE if _A3(s) or _B3(s)), 12, "例題3 A∪B のマス")
eq(prob(DICE, lambda s: _A3(s)), F(1, 6), "例題3(a)")
eq(prob(DICE, lambda s: _B3(s)), F(11, 36), "例題3(b)")
eq(prob(DICE, lambda s: _A3(s) or _B3(s)), F(1, 3), "例題3(c)")
eq(F(6, 36) + F(11, 36) - F(5, 36), F(12, 36), "例題3 加法定理")
eq(36 - 5 * 5, 11, "6 を含むマスは 36 - 25")
eq(6 + 6 - 1, 11, "行と列で数えても 11")
chk(sorted(s for s in DICE if _A3(s) and _B3(s))
    == [(4, 6), (5, 6), (6, 4), (6, 5), (6, 6)], "例題3 の重なりのマス")
chk(sum(1 for s in DICE if sum(s) == 10) == 3, "合計 10 は 3 通り")
chk(sum(1 for s in DICE if sum(s) == 11) == 2, "合計 11 は 2 通り")
chk(sum(1 for s in DICE if sum(s) == 12) == 1, "合計 12 は 1 通り")
# 検算に並べた 12 マスが本当に A∪B と一致すること
_listed = [(4, 6), (5, 5), (6, 4), (5, 6), (6, 5), (6, 6),
           (1, 6), (2, 6), (3, 6), (6, 1), (6, 2), (6, 3)]
chk(len(set(_listed)) == 12, "並べたマスは 12 個で重複なし")
chk(set(_listed) == set(s for s in DICE if _A3(s) or _B3(s)),
    "並べたマスは A∪B と一致する")
in_text("P(A \\cup B) = \\frac{6}{36} + \\frac{11}{36} - \\frac{5}{36} "
        "= \\frac{12}{36} = \\frac{1}{3}", "例題3(c)")
in_text("$6$ が $1$ つも出ないマスは $5 \\times 5 = 25$ 個", "例題3(b) の数え方")

# ══════════════════════════════════════════════════════════
# 8. 例題4 —— 樹形図（もどす）
# ══════════════════════════════════════════════════════════
_g, _y = F(4, 10), F(6, 10)
eq(_g, F(2, 5), "4/10 = 2/5")
eq(_y, F(3, 5), "6/10 = 3/5")
eq(_g * _g, F(4, 25), "例題4(b)")
eq(_g * _y + _y * _g, F(12, 25), "例題4(c)")
eq(1 - _y * _y, F(16, 25), "例題4(d)")
eq(_g * _g + _g * _y + _y * _g + _y * _y, 1, "例題4 枝先の合計")
eq(F(4, 25) + F(6, 25) + F(6, 25), F(16, 25), "例題4(d) を直接足す")
eq(F(4 * 6 + 6 * 4, 100), F(12, 25), "例題4(c) を数えても 12/25")
eq(10 * 10, 100, "もどすので 10×10 = 100")
in_text("P(GG) = \\frac{2}{5} \\times \\frac{2}{5} = \\frac{4}{25}", "例題4(b)")
in_text("P(\\text{at least one green}) = 1 - \\frac{9}{25} = \\frac{16}{25}",
        "例題4(d)")
in_text("**駒に名前を付けて数えます。** もどすので順序を区別した組は "
        "$10 \\times 10 = 100$ とおりです。", "例題4(c) の検算")

# ══════════════════════════════════════════════════════════
# 9. 演習の答え
# ══════════════════════════════════════════════════════════
# 演習1
eq(25 + 18 - 9, 34, "演習1 少なくとも一方")
eq(F(34, 40), F(17, 20), "演習1 の答え")
eq(F(40 - 34, 40), F(3, 20), "演習1 どちらでもない")
eq(16 + 9 + 9 + 6, 40, "演習1 の 4 つの合計")
chk(25 + 18 > 40, "引かないと 43 で 40 をこえる")

# 演習2
_C2 = list(range(1, 13))
_E = [x for x in _C2 if x % 2 == 0]
_M = [x for x in _C2 if x % 3 == 0]
eq(len(_E), 6, "1..12 の偶数は 6 個")
eq(len(_M), 4, "1..12 の 3 の倍数は 4 個")
chk(sorted(set(_E) & set(_M)) == [6, 12], "両方は 6 と 12")
eq(F(6 + 4 - 2, 12), F(2, 3), "演習2 の答え")
chk(sorted(set(_E) | set(_M)) == [2, 3, 4, 6, 8, 9, 10, 12], "演習2 の書き出し")
chk(sorted(set(_C2) - set(_E) - set(_M)) == [1, 5, 7, 11], "演習2 のあてはまらない側")
eq(8 + 4, 12, "8 + 4 = 12")

# 演習3
_A4 = [2, 4, 6]
_B4 = [5, 6]
chk(sorted(set(_A4) & set(_B4)) == [6], "演習3 の重なりは 6 だけ")
chk(sorted(set(_A4) | set(_B4)) == [2, 4, 5, 6], "演習3 の和事象")
eq(F(3, 6) + F(2, 6) - F(1, 6), F(2, 3), "演習3 の答え")
eq(prob(range(1, 7), lambda x: x % 2 == 0 or x > 4), F(2, 3), "演習3 を直接数える")
chk(F(3, 6) + F(2, 6) != F(4, 6), "排反として足すと合わない")

# 演習4
eq(sum(1 for s in DICE if s[0] % 2 and s[1] % 2), 9, "両方奇数は 9 マス")
eq(36 - 9, 27, "積が偶数は 27 マス")
eq(F(27, 36), F(3, 4), "演習4 の答え")
eq(F(18, 36) + F(18, 36) - F(9, 36), F(27, 36), "加法定理でも 27/36")
eq(sum(1 for s in DICE if (s[0] * s[1]) % 2 == 0), 27, "直接数えても 27")
chk(min(a * b for a, b in DICE) == 1, "積の最小は 1（0 にならない）")

# 演習5
_p5 = sp.Rational("0.3")
eq(_p5 * _p5, sp.Rational("0.09"), "演習5 両方当たり")
eq(_p5 * (1 - _p5) * 2, sp.Rational("0.42"), "演習5 ちょうど 1 回")
eq(1 - (1 - _p5) ** 2, sp.Rational("0.51"), "演習5 少なくとも 1 回")
eq(sp.Rational("0.09") + sp.Rational("0.21") + sp.Rational("0.21")
   + sp.Rational("0.49"), 1, "演習5 枝先の合計")
eq(sp.Rational("0.09") + sp.Rational("0.21") + sp.Rational("0.21"),
   sp.Rational("0.51"), "演習5 直接足しても 0.51")
chk(_p5 + _p5 != sp.Rational("0.51"), "0.3+0.3 は答えではない")

# 演習6
eq(sp.Rational("0.5") + sp.Rational("0.4") - sp.Rational("0.2"),
   sp.Rational("0.7"), "演習6 P(A∪B)")
eq(1 - sp.Rational("0.7"), sp.Rational("0.3"), "演習6 どちらでもない")
eq(sp.Rational("0.5") - sp.Rational("0.2"), sp.Rational("0.3"), "演習6 A だけ")
eq(sp.Rational("0.4") - sp.Rational("0.2"), sp.Rational("0.2"), "演習6 B だけ")
eq(sp.Rational("0.3") + sp.Rational("0.2") + sp.Rational("0.2")
   + sp.Rational("0.3"), 1, "演習6 の 4 つの合計")

# 演習7
eq(sp.Rational("0.45") + sp.Rational("0.35") - sp.Rational("0.6"),
   sp.Rational("0.2"), "演習7 P(A∩B)")
eq(sp.Rational("0.45") + sp.Rational("0.35") - sp.Rational("0.2"),
   sp.Rational("0.6"), "演習7 もどして確かめる")
for _v in (sp.Rational("0.25"), sp.Rational("0.2"), sp.Rational("0.15"),
           sp.Rational("0.4")):
    chk(_v >= 0, "演習7 の 4 つの部分は 0 以上")
eq(sp.Rational("0.25") + sp.Rational("0.2") + sp.Rational("0.15")
   + sp.Rational("0.4"), 1, "演習7 の 4 つの合計")
chk(sp.Rational("0.2") != 0, "演習7 は排反でない")

# 演習8
eq(35 + 28 - 12, 51, "演習8 の答え")
eq(60 - 51, 9, "演習8 どちらでもない")
eq(23 + 12 + 16 + 9, 60, "演習8 の 4 つの合計")
chk(35 + 28 > 60, "63 は 60 をこえる")
eq(35 - 12, 23, "スープだけ")
eq(28 - 12, 16, "サラダだけ")

# 演習9
_r9, _w9 = F(3, 8), F(5, 8)
eq(_r9 * _r9 + _w9 * _w9, F(34, 64), "演習9 同じ色")
eq(F(34, 64), F(17, 32), "34/64 = 17/32")
eq(1 - F(17, 32), F(15, 32), "演習9 ちがう色")
eq(_r9 * _w9 * 2, F(30, 64), "演習9 ちがう色を直接")
eq(F(30, 64), F(15, 32), "30/64 = 15/32")
eq(F(9, 64) + F(15, 64) + F(15, 64) + F(25, 64), 1, "演習9 枝先の合計")
eq(8 * 8, 64, "8×8 = 64")
eq(3 * 3 + 5 * 5, 34, "同じ色は 34 とおり")

# 演習10
_s8 = [s for s in DICE if sum(s) == 8]
_same = [s for s in DICE if s[0] == s[1]]
eq(len(_s8), 5, "合計 8 は 5 マス")
eq(len(_same), 6, "ぞろ目は 6 マス")
chk(sorted(set(_s8) & set(_same)) == [(4, 4)], "重なりは (4,4) だけ")
eq(F(5 + 6 - 1, 36), F(5, 18), "演習10 の答え")
_l10 = [(2, 6), (3, 5), (4, 4), (5, 3), (6, 2), (1, 1), (2, 2), (3, 3),
        (5, 5), (6, 6)]
chk(len(set(_l10)) == 10, "演習10 の書き出しは 10 マス")
chk(set(_l10) == set(_s8) | set(_same), "演習10 の書き出しは A∪B と一致")
chk(F(5, 36) + F(6, 36) != F(10, 36), "引かないと合わない")




# ══════════════════════════════════════════════════════════
# 10. ページに書いてある計算を、機械的に全部たしかめる
# ══════════════════════════════════════════════════════════
_ATOM = r"(?:\\[dt]?frac\{-?\d+\}\{-?\d+\}|-?\d+(?:\.\d+)?)"
_TERM = r"%s(?:\s*\\times\s*%s)*" % (_ATOM, _ATOM)
_EXPR = r"%s(?:\s*[+-]\s*%s)*" % (_TERM, _TERM)
_STMT = re.compile(r"(?<![\d\w}])(%s(?:\s*=\s*%s)+)(?!\s*(?:[+-]|\\times|[\d.]))"
                   % (_EXPR, _EXPR))


def _tonum(t):
    t = t.strip()
    m = re.fullmatch(r"\\[dt]?frac\{(-?\d+)\}\{(-?\d+)\}", t)
    if m:
        return sp.Rational(int(m.group(1)), int(m.group(2)))
    return sp.Rational(t)


def _value(expr):
    """+ - かけ算だけの式を、かけ算を先に計算して評価する。"""
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
    _vals = [_value(x) for x in _m.group(1).split("=")]
    _nstmt += 1
    chk(len(set(_vals)) == 1,
        "式が合わない: %s  →  %s" % (_m.group(1)[:80], _vals))
chk(_nstmt >= 55, "ページの計算を %d 本たしかめた" % _nstmt)

# 確率の値は、すべて 0 以上 1 以下
_nprob = 0
for _m in re.finditer(r"P\([^)]*\)\s*=\s*(%s)" % _ATOM, TEXT):
    _nprob += 1
    _v = _tonum(_m.group(1))
    chk(0 <= _v <= 1, "確率が 0..1 の外: %s" % _m.group(0)[:60])
chk(_nprob >= 12, "確率の値を %d 個たしかめた" % _nprob)

# ══════════════════════════════════════════════════════════
# 15. 査読で直したところ（2026-09-08）
# ══════════════════════════════════════════════════════════

# --- B1 電卓 callout が例題3 の答えを先に出していた ----------------------
in_text("$\\dfrac{15}{36}$ は $\\dfrac{5}{12}$ まで約分します。", "B1 直した例")
not_in_body("$\\dfrac{12}{36}$ は $\\dfrac{1}{3}$", "例題3(c) の答えは本文に出さない")
eq(F(15, 36), F(5, 12), "15/36 = 5/12")
# 5/12 と 15/36 は、このページのどの答えとも重ならない
_answers = [F(13, 15), F(2, 15), F(3, 10), F(1, 4), F(1, 20), F(1, 2), F(1, 6),
            F(11, 36), F(1, 3), F(4, 25), F(12, 25), F(16, 25), F(17, 20),
            F(3, 20), F(2, 3), F(3, 4), F(17, 32), F(15, 32), F(5, 18), F(1, 1)]
chk(F(5, 12) not in _answers, "5/12 は答えに使っていない")

# --- M1 互いに排反な組を、演習3(b) で実際に使わせる ---------------------
in_text("**(b)** Explain whether $A$ and $C$ are mutually exclusive, and find "
        "$P(A \\cup C)$.", "演習3(b)")
in_text("P(A \\cup C) = \\frac{3}{6} + \\frac{3}{6} = 1", "演習3(b) の答え")
in_text("**(b)** 偶数でも奇数でもある数はないので、$A$ と $C$ は互いに排反です。",
        "演習3(b) の解説")
in_text("引くものがないので、@eq-aasl46a-me がそのまま使えます。",
        "排反の式を実際に使う")
_A6, _C6 = {2, 4, 6}, {1, 3, 5}
chk(_A6 & _C6 == set(), "A と C は共通の目がない")
chk(_A6 | _C6 == {1, 2, 3, 4, 5, 6}, "A ∪ C は U そのもの")
eq(F(3, 6) + F(3, 6), 1, "3/6 + 3/6 = 1")
eq(F(len(_A6 | _C6), 6), 1, "数えても 1")
# 排反の式が、ページのどこかで実際に使われていること
chk(TEXT.count("@eq-aasl46a-me") >= 2, "排反の式が本文と演習で使われる")

# --- M2 表が使える条件の言いすぎを直した ---------------------------------
in_text("**マスを数えて確率を出せるのは、マスがすべて同様に確からしいときだけです。**",
        "M2 数えられる条件")
in_text("そうでないときは、マスに確率を書いて足します。", "M2 そうでないとき")
not_in_text("**表が使えるのは、マスがすべて同様に確からしいときです。**",
            "言いすぎは消した")

# --- M3 循環していた検算を、もとの数にもどす検算にした -------------------
in_text("**もとの人数にもどるか見ます。** サッカーは $12 + 6 = 18$ ✓", "例題1(a) の検算")
in_text("$30 - 18 - 8 = 4$ ✓ (a) の $4$ 人と一致します。", "例題1(c) の検算")
in_text("コーヒーは $16 + 9 = 25$ ✓、紅茶は $9 + 9 = 18$ ✓", "演習1 の検算")
in_text("$40 - 25 - 9 = 6$ ✓", "演習1 の別の道すじ")
in_text("**積が偶数のマスを直接数えます。**", "演習4 の検算")
in_text("$P(A) = 0.3 + 0.2 = 0.5$ ✓、$P(B) = 0.2 + 0.2 = 0.4$ ✓", "演習6 の検算")
in_text("スープは $23 + 12 = 35$ ✓、サラダは $16 + 12 = 28$ ✓", "演習8 の検算")
not_in_text("**$4$ つを足します。** $12 + 6 + 8 + 4 = 30$ ✓ $n(U)$ と一致します。",
            "循環した検算は消した（例題1）")
not_in_text("**$4$ つを足します。** $0.3 + 0.2 + 0.2 + 0.3 = 1$ ✓",
            "循環した検算は消した（演習6）")
not_in_text("**足して $36$ になるか見ます。** $9 + 27 = 36$ ✓",
            "循環した検算は消した（演習4）")
# もどす検算が、実際に誤りを捕まえられること
chk(12 + 6 == 18 and 8 + 6 == 14, "例題1 のもどし")
chk(6 + 6 != 18, "重なりを引き忘れて 6 と書いたら、もどして合わない")
eq(30 - 18 - 8, 4, "別の道すじでも 4")
eq(3 * 6 + 3 * 3, 27, "積が偶数を直接数えると 27")
chk(16 + 9 == 25 and 9 + 9 == 18, "演習1 のもどし")
chk(23 + 12 == 35 and 16 + 12 == 28, "演習8 のもどし")

# --- M4 個数で与えられていない確率でも、かけ算を正当化した ---------------
in_text("**確率が個数で与えられていないときも、同じことが言えます。**", "M4 の段落")
in_text("円を $10$ 等分して $3$ つを当たりにしたルーレット", "M4 の言いかえ")
in_text("$2$ 回とも当たる組は $3 \\times 3 = 9$ とおりなので $\\dfrac{9}{100}$",
        "M4 の数え上げ")
eq(F(9, 100), sp.Rational("0.3") * sp.Rational("0.3"), "9/100 = 0.3 × 0.3")
eq(10 * 10, 100, "10×10 = 100")
not_in_body("0.51", "演習5 の答えは本文に出さない")
not_in_body("0.42", "演習5 の答えは本文に出さない（2）")

# --- m1 4 つに分かれるのは重なっているとき ------------------------------
in_text("円が $2$ つ**重なっているとき**、$U$ は $4$ つの部分に分かれます", "m1")
in_text("**Venn 図では、ふつう円を離してかきます。**", "m1 排反の図")
not_in_text("**Venn 図では、円が離れている形になります。**", "古い言い方は消した")

# --- m2 演習6 で Venn 図をかかせる ---------------------------------------
in_text("By drawing a Venn diagram and writing the probability in each of the "
        "four regions", "m2 演習6")
in_text("ベン図をかいて $4$ つの部分それぞれに確率を書き", "m2 演習6 の訳")
chk("Draw a Venn diagram and write the number of students" in TEXT
    and "By drawing a Venn diagram and writing the probability" in TEXT,
    "人数を書く問いと確率を書く問いの両方がある")

# --- m3 A ∩ B' を導入した -----------------------------------------------
in_text("$A$ だけ。$A \\cap B'$ と書きます", "m3 A∩B'")
in_text("$B$ だけ。$A' \\cap B$ と書きます", "m3 A'∩B")

# --- m4 「1 をこえたら引き忘れ」の一方向性 -------------------------------
in_text("**$1$ 以下でも、まちがっていることがあります。**", "m4")
not_in_text("$1$ をこえたら、引き忘れです。", "断定は消した")
# 引き忘れても 1 をこえない例
chk(sp.Rational("0.3") + sp.Rational("0.2") <= 1,
    "0.3 + 0.2 は 1 をこえない（だから一方向の検査）")

# --- m5 例題3 の検算の日本語 --------------------------------------------
in_text("$1$ 個目が $6$ のマスが $6$ 個、$2$ 個目が $6$ のマスが $6$ 個", "m5")
not_in_text("$1$ 行目が $6$ のマスが $6$ 個", "読めない言い方は消した")
chk(sum(1 for s in DICE if s[0] == 6) == 6, "1 個目が 6 のマスは 6 個")
chk(sum(1 for s in DICE if s[1] == 6) == 6, "2 個目が 6 のマスは 6 個")

# --- m6 用語 -------------------------------------------------------------
in_text("sample space（標本空間）$U$ を長方形で表し", "m6 sample space")
in_text("**with replacement**（復元、玉をもどす）場合", "m6 with replacement")
in_text("$1$ 本の道すじ（始点から端まで）", "m6 始点")
chk(TEXT.count("（標本空間の表）") == 0, "table of outcomes の訳をそろえた")

# --- m8 演習4 の注意 -----------------------------------------------------
in_text("**「積が偶数」を「両方とも偶数」と読みまちがえないでください。**", "m8")
not_in_text("**$0$ は出てきません。**", "空振りの注意は消した")
chk(sum(1 for s in DICE if s[0] % 2 == 0 and s[1] % 2 == 0) == 9, "両方偶数は 9 マス")
chk(sum(1 for s in DICE if (s[0] * s[1]) % 2 == 0) == 27, "積が偶数は 27 マス")
chk(9 != 27, "両方偶数と積が偶数はちがう")

# --- m9 演習5 の注意 -----------------------------------------------------
in_text("この $2$ つは同時に起こりえます。", "m9")
in_text("$0.6 - 0.09 = 0.51$ ✓", "m9 の計算")
not_in_text("これは枝ではなく段をまたいで足しています。", "説明になっていない文は消した")
eq(sp.Rational("0.6") - sp.Rational("0.09"), sp.Rational("0.51"), "0.6 - 0.09 = 0.51")
eq(sp.Rational("0.3") + sp.Rational("0.3") - sp.Rational("0.09"),
   sp.Rational("0.51"), "加法定理でも 0.51")

# --- m10 演習2 の解答例 --------------------------------------------------
in_text("*even:* $6$ *outcomes; multiples of $3$:* $4$ *outcomes; both:* $6$ "
        "*and* $12$", "m10")

# --- m11 model answer ----------------------------------------------------
in_text("The second counter is again taken at random from the same $10$ counters",
        "m11 例題4(e)")
in_text("more than the $60$ customers who were asked.", "m11 演習8")

# --- m12 4.5 への参照先 --------------------------------------------------
in_text("[SL 4.5 の Why it works](aasl-4-5.qmd#why-it-works)", "m12")
not_in_text("重ならない部分の確率は足せるので（[SL 4.5 第 3 節]", "誤った参照は消した")

# --- m7 図 ---------------------------------------------------------------
in_fig('"$W$"', "図の 1 段目は W")
in_fig("the first result does not change the probabilities", "図に条件を書いた")
in_fig("at least one $W$", "図の注記も W")
chk('"$A$"' not in FIG.split("# (b) tree diagram")[-1],
    "樹形図に A は使わない（(a) の A と紛らわしい）")
in_text("(b) A tree diagram shows a two-stage experiment in which the first "
        "result does not change the probabilities for the second", "m7 キャプション")


# ══════════════════════════════════════════════════════════
# E09  作図問題の解答に完成図を入れる
# ══════════════════════════════════════════════════════════
in_text("(img/aasl-4-6a-ex6.svg){#fig-aasl46a-ex6 width=100%}",
        "E09 演習6 の Venn 図")
in_text("(img/aasl-4-6a-tree.svg){#fig-aasl46a-tree width=100%}",
        "E09 例題4 の樹形図")
# Venn の 4 領域と、樹形図の枝先
chk(sp.Rational(3, 10) + sp.Rational(2, 10) + sp.Rational(2, 10)
    + sp.Rational(3, 10) == 1, "E09 Venn の 4 領域の和は 1")
_e09p = [sp.Rational(2, 5) ** 2, sp.Rational(2, 5) * sp.Rational(3, 5),
         sp.Rational(3, 5) * sp.Rational(2, 5), sp.Rational(3, 5) ** 2]
chk(sum(_e09p) == 1, "E09 樹形図の枝先の和は 1")
chk(_e09p == [sp.Rational(4, 25), sp.Rational(6, 25), sp.Rational(6, 25),
              sp.Rational(9, 25)], "E09 樹形図の枝先の値")

print()
print("OK", OK, "/ NG", NG)
