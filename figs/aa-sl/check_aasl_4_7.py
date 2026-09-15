# -*- coding: utf-8 -*-
"""AA SL 4.7 のページを検算する。

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
QMD = os.path.join(ROOT, "aa-sl", "04-statistics-and-probability", "aasl-4-7.qmd")
FIGP = os.path.join(HERE, "make_aasl_4_7.py")

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
in_text("# SL 4.7 — Discrete random variables and expected value"
        "（離散確率変数と期待値） {#sec-aasl-4-7}", "見出し")

for _h in ("## What you should be able to do", "## The idea", "## Why it works",
           "## Worked examples", "## Common errors", "## Exercises"):
    in_text(_h, "節 " + _h)

_secs = re.findall(r"^### (\d)\. .*\{#([a-z-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 8)],
    "### の番号 1..7: %s" % [s[0] for s in _secs])
chk([s[1] for s in _secs] == ["rv", "dist", "sumone", "formula", "expected",
                              "meaning", "game"],
    "アンカー: %s" % [s[1] for s in _secs])

chk(len(re.findall(r"^\[\d+\]\{\.ex-no\}", TEXT, re.M)) == 10, "演習 10 問")
chk(TEXT.count("::: {#exm-") == 4, "例題 4 つ")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep 9 個")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳 14")
chk(TEXT.count("</details>") == 14, "details 閉じ 14")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例 14")
chk(len(re.findall(r"^---$", TEXT, re.M)) == 6, "行頭 --- は 6 本")
chk(TEXT.count("{.callout-warning}") == 7, "callout-warning 7（誤り 6 + 電卓 1）")
chk(TEXT.count("{.callout-important}") == 1, "callout-important 1（公式集 4.7 の E(X)）")
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
chk(len(_qs) == 9, "Explain 系の問いは 9: %d" % len(_qs))

for _i, _m in enumerate(re.findall(r"\{\.model-answer\}(.*?):::", TEXT, re.S), 1):
    _b = _m.replace("**試験ではこう書く**", "")
    chk(len(_b.split()) <= 115, "model answer %d は 115 語以内" % _i)
    chk(not [c for c in _b if "぀" <= c <= "ヿ" or "一" <= c <= "鿿"],
        "model answer %d に日本語がない" % _i)

in_text("(img/aasl-4-7-idea.svg){#fig-aasl47-idea width=100%}", "図の埋め込み")
in_text("@fig-aasl47-idea (a)", "図 (a) の参照")
in_text("@fig-aasl47-idea (b)", "図 (b) の参照")

chk(not re.search(r"^> ", TEXT, re.M), "引用ブロックは使わない（4.7 に Not required はない）")
not_in_text("シラバス", "シラバスへの言及はしない")
for _w in ("そのとおり", "もちろん", "簡単です", "自明"):
    not_in_text(_w, "禁止語 " + _w)

# ══════════════════════════════════════════════════════════
# 2. 式と公式集
# ══════════════════════════════════════════════════════════
in_text("\\sum_{i=1}^{k} P(X = x_i) = 1\n$$ {#eq-aasl47-sum}", "合計 1 の式")
in_text("E(X) = \\sum_{i=1}^{k} x_i P(X = x_i)\n$$ {#eq-aasl47-ev}", "期待値の式")
in_text("公式集の **4.7** の欄に *Expected value of a discrete random variable "
        "$X$* として載っています", "公式集 4.7")
in_text("{#tbl-aasl47-dist}", "分布の表")
in_text("**$E(X)$ は「つり合う点」です**", "つり合う点")
in_text("$E(X) = 0$ のゲームを fair（公平）といいます", "fair game")

# 記号のままで、期待値が最小と最大の間に入ることをたしかめる
_x1, _x2, _p1 = sp.symbols("x1 x2 p1")
_ev = _x1 * _p1 + _x2 * (1 - _p1)
for _pv in (sp.Rational(0), sp.Rational(1, 4), sp.Rational(1, 2),
            sp.Rational(3, 4), sp.Rational(1)):
    _v = _ev.subs({_x1: 1, _x2: 5, _p1: _pv})
    chk(1 <= _v <= 5, "期待値は 1..5 の間: p=%s → %s" % (_pv, _v))

# ══════════════════════════════════════════════════════════
# 3. The idea の例（答えを先に出していないこと）
# ══════════════════════════════════════════════════════════
in_text("P(X = x) = k(5 - x), \\qquad x \\in \\{1, 2, 3\\}", "§4 の例")
in_text("上の例なら $4k$、$3k$、$2k$ の合計を $1$ とおきます。", "§4 の説明")
eq(4 + 3 + 2, 9, "§4 の例の係数の和")
not_in_body("k(x + 1)", "例題2 の式は本文に出さない")
not_in_body("k(2x + 1)", "演習2 の式は本文に出さない")
not_in_body("\\dfrac{20}{7}", "例題2 の答えは本文に出さない")
not_in_body("2.7", "例題1 の答えは本文に出さない")
not_in_body("1.7", "演習1 の答えは本文に出さない")
not_in_body("\\dfrac{35}{12}", "演習2 の答えは本文に出さない")
in_text("$X$ が整数しかとらなくても、$E(X)$ は $2.4$ のような小数に", "§6 の例")
not_in_text("さいころの目の期待値は $3.5$", "演習3 の答えは本文に出さない")
chk("$\\dfrac{7}{2}$" not in BODY, "演習3 は 7/2 の形では本文に出さない")
in_text("$\\dfrac{45}{20}$ は $\\dfrac{9}{4}$ まで約分します。", "電卓 callout の約分")
eq(F(45, 20), F(9, 4), "45/20 = 9/4")

# ══════════════════════════════════════════════════════════
# 4. Why it works
# ══════════════════════════════════════════════════════════
in_text("$N$ で割ると、$N$ が約分されて", "N で割る")
in_text("[SL 4.3 の平均](aasl-4-3.qmd#mean)と同じ形です。", "4.3 への参照")
in_text("[SL 4.5 の期待される回数](aasl-4-5.qmd#expected)", "4.5 への参照")
in_text("\\sum x_i P(X = x_i) \\ge \\sum x_{\\min} P(X = x_i) = x_{\\min}",
        "下からの評価")
in_text("$E(X) = -0.2$ なら、$100$ 回で約 $-20$、$1000$ 回で約 $-200$",
        "Why it works の例")
eq(100 * sp.Rational("-0.2"), -20, "100 回で -20")
eq(1000 * sp.Rational("-0.2"), -200, "1000 回で -200")
chk(sp.Rational("-0.2") not in (sp.Rational("-0.5"), sp.Rational("-0.4")),
    "-0.2 は例題3・演習5 の答えとちがう")

# ══════════════════════════════════════════════════════════
# 5. 図
# ══════════════════════════════════════════════════════════
in_fig("XS = [0, 1, 2, 3]", "図 (a) の値")
in_fig("PS = [0.1, 0.3, 0.5, 0.1]", "図 (a) の確率")
eq(sum([sp.Rational("0.1"), sp.Rational("0.3"), sp.Rational("0.5"),
        sp.Rational("0.1")]), 1, "図 (a) の確率の合計は 1")
eq(0 * sp.Rational("0.1") + 1 * sp.Rational("0.3") + 2 * sp.Rational("0.5")
   + 3 * sp.Rational("0.1"), sp.Rational("1.6"), "図 (a) の E(X) は 1.6")
in_fig("$E(X) = 1.6$", "図 (a) のラベル")
eq(3 * F(1, 3) + (-2) * F(2, 3), F(-1, 3), "図 (b) game A の E(X)")
eq(4 * F(1, 3) + (-2) * F(2, 3), 0, "図 (b) game B の E(X)")
chk(sp.Rational("1.6") not in (sp.Rational("2.7"), sp.Rational("1.7"),
                               sp.Rational("0.75")),
    "図 (a) の E(X) は例題・演習とちがう")
chk(sorted([sp.Rational("0.1"), sp.Rational("0.3"), sp.Rational("0.5"),
            sp.Rational("0.1")])
    != sorted([sp.Rational("0.1"), sp.Rational("0.3"), sp.Rational("0.4"),
               sp.Rational("0.2")]),
    "図 (a) の確率の集まりは例題1 とちがう")

# ══════════════════════════════════════════════════════════
# 6. 例題1
# ══════════════════════════════════════════════════════════
_P1 = [sp.Rational("0.1"), sp.Rational("0.3"), sp.Rational("0.4"),
       sp.Rational("0.2")]
eq(1 - (sp.Rational("0.1") + sp.Rational("0.3") + sp.Rational("0.2")),
   sp.Rational("0.4"), "例題1(a) k")
eq(sum(_P1), 1, "例題1 の合計")
eq(sp.Rational("0.4") + sp.Rational("0.2"), sp.Rational("0.6"), "例題1(b)")
eq(1 - (sp.Rational("0.1") + sp.Rational("0.3")), sp.Rational("0.6"),
   "例題1(b) を余事象で")
eq(sum(x * p for x, p in zip([1, 2, 3, 4], _P1)), sp.Rational("2.7"),
   "例題1(c)")
chk(1 <= sp.Rational("2.7") <= 4, "例題1 の E(X) は 1..4 の間")
chk(sp.Rational("2.7") not in (1, 2, 3, 4), "例題1 の E(X) はとりうる値でない")
chk(max(range(4), key=lambda i: _P1[i]) == 2, "いちばん確率が大きいのは x = 3")
chk(abs(float(sp.Rational("2.7")) - 3) < 1, "2.7 は 3 の近く")
chk(1 + 2 + 3 + 4 == 10 and not (1 <= 10 <= 4), "確率をかけ忘れると範囲の外")

# ══════════════════════════════════════════════════════════
# 7. 例題2
# ══════════════════════════════════════════════════════════
_k = sp.Symbol("k")
chk(sp.solve(sp.Eq(sum(_k * (x + 1) for x in range(1, 5)), 1), _k)
    == [sp.Rational(1, 14)], "例題2(a) k = 1/14")
eq(2 + 3 + 4 + 5, 14, "係数の和は 14")
eq(sum(F(x + 1, 14) for x in range(1, 5)), 1, "例題2 の合計")
eq(sum(x * F(x + 1, 14) for x in range(1, 5)), F(20, 7), "例題2(c)")
eq(1 * 2 + 2 * 3 + 3 * 4 + 4 * 5, 40, "分子の和は 40")
eq(F(40, 14), F(20, 7), "40/14 = 20/7")
chk(1 <= F(20, 7) <= 4, "例題2 の E(X) は 1..4 の間")
chk(F(20, 7) > F(5, 2), "確率が右上がりなので、真ん中より大きい")
chk(abs(float(F(20, 7)) - 2.86) < 0.01, "20/7 は約 2.86")
for _x in range(1, 5):
    chk(0 < F(_x + 1, 14) < 1, "例題2 の確率は 0 と 1 の間: x=%d" % _x)

# ══════════════════════════════════════════════════════════
# 8. 例題3・例題4
# ══════════════════════════════════════════════════════════
eq(F(1, 6) + F(1, 3) + F(1, 2), 1, "例題3(a)")
eq(7 * F(1, 6) + 1 * F(1, 3) + (-4) * F(1, 2), F(-1, 2), "例題3(b)")
eq(F(7, 6) + F(2, 6) - F(12, 6), F(-3, 6), "例題3(b) の途中")
eq(F(-3, 6), F(-1, 2), "-3/6 = -1/2")
eq(30 * F(-1, 2), -15, "例題3(c)")
eq(F(-15, 30), F(-1, 2), "割りもどすと -1/2")
chk(-4 <= F(-1, 2) <= 7, "例題3 の E(X) は範囲の中")
chk(F(-1, 2) < 0, "例題3 は公平でない")

_p = sp.Symbol("p")
_evp = (_p - 2) * F(1, 4) + (-2) * F(3, 4)
eq(sp.simplify(_evp), sp.Rational(1, 4) * _p - 2, "例題4(b)")
eq(sp.simplify(_evp - (_p - 8) / 4), 0, "例題4(b) は (p-8)/4")
chk(sp.solve(sp.Eq(_evp, 0), _p) == [8], "例題4(c) p = 8")
eq(6 * F(1, 4) + (-2) * F(3, 4), 0, "例題4 の検算（p=8 で E=0）")
eq(8 - 2, 6, "当たりの利得は 6")
eq(4 * 2, 8, "参加料の 4 倍が 8")
# 参加料を引き忘れた場合
eq(sp.simplify(_p * F(1, 4) + 0 * F(3, 4)), _p / 4, "引き忘れると p/4")
chk(sp.solve(sp.Eq(_p / 4, 0), _p) == [0], "引き忘れると p = 0 になる")

# ══════════════════════════════════════════════════════════
# 9. 演習の答え
# ══════════════════════════════════════════════════════════
_Pe1 = [sp.Rational("0.15"), sp.Rational("0.25"), sp.Rational("0.35"),
        sp.Rational("0.25")]
eq(1 - (sp.Rational("0.15") + sp.Rational("0.25") + sp.Rational("0.25")),
   sp.Rational("0.35"), "演習1 a")
eq(sum(_Pe1), 1, "演習1 の合計")
eq(sum(x * p for x, p in zip([0, 1, 2, 3], _Pe1)), sp.Rational("1.7"), "演習1 E(X)")
chk(0 <= sp.Rational("1.7") <= 3, "演習1 の範囲")
eq(sp.Rational("0.35") + sp.Rational("0.25"), sp.Rational("0.6"), "x が 2,3 の確率")
eq(sp.Rational("0.15") + sp.Rational("0.25"), sp.Rational("0.4"), "x が 0,1 の確率")
chk(sp.Rational("1.7") > sp.Rational("1.5"), "演習1 は真ん中より大きい")

chk(sp.solve(sp.Eq(sum(_k * (2 * x + 1) for x in range(1, 5)), 1), _k)
    == [sp.Rational(1, 24)], "演習2 k = 1/24")
eq(3 + 5 + 7 + 9, 24, "演習2 の係数の和")
eq(sum(x * F(2 * x + 1, 24) for x in range(1, 5)), F(35, 12), "演習2 E(X)")
eq(1 * 3 + 2 * 5 + 3 * 7 + 4 * 9, 70, "演習2 の分子")
eq(F(70, 24), F(35, 12), "70/24 = 35/12")
chk(abs(float(F(35, 12)) - 2.92) < 0.01, "35/12 は約 2.92")
chk(F(35, 12) > F(5, 2), "演習2 は真ん中より大きい")

eq(sum(x * F(1, 6) for x in range(1, 7)), F(7, 2), "演習3 E(X)")
eq(1 + 2 + 3 + 4 + 5 + 6, 21, "目の合計は 21")
eq(F(21, 6), F(7, 2), "21/6 = 7/2")
eq(F(1 + 6, 2), F(7, 2), "対称性でも 7/2")
chk(F(7, 2) not in [F(i, 1) for i in range(1, 7)], "7/2 という目はない")

_a, _b = sp.symbols("a b")
_sol = sp.solve([sp.Eq(sp.Rational("0.2") + _a + _b, 1),
                 sp.Eq(1 * sp.Rational("0.2") + 2 * _a + 3 * _b,
                       sp.Rational("2.1"))], [_a, _b])
chk(_sol == {_a: sp.Rational("0.5"), _b: sp.Rational("0.3")},
    "演習4 a=0.5, b=0.3: %s" % _sol)
eq(sp.Rational("0.2") + sp.Rational("0.5") + sp.Rational("0.3"), 1, "演習4 の合計")
eq(sp.Rational("0.2") + 2 * sp.Rational("0.5") + 3 * sp.Rational("0.3"),
   sp.Rational("2.1"), "演習4 の E(X)")
eq(sp.Rational("0.8") - sp.Rational("0.3"), sp.Rational("0.5"), "a = 0.8 - b")

eq(5 * F(1, 10) + (-1) * F(9, 10), F(-2, 5), "演習5 E(X)")
eq(6 - 1, 5, "当たりの利得は 5")
eq(F(5, 10) - F(9, 10), F(-4, 10), "5/10 - 9/10")
eq(F(-4, 10), F(-2, 5), "-4/10 = -2/5")
chk(-1 <= F(-2, 5) <= 5, "演習5 の範囲")
eq(6 * F(1, 10), F(3, 5), "参加料を引き忘れると 3/5")
chk(F(3, 5) > 0, "引き忘れると正になってしまう")
chk(F(-2, 5) != F(-1, 2), "演習5 と例題3 の答えはちがう")

_Pe6 = [sp.Rational("0.5"), sp.Rational("0.3"), sp.Rational("0.15"),
        sp.Rational("0.05")]
eq(sum(_Pe6), 1, "演習6 の合計")
eq(sum(x * p for x, p in zip([0, 1, 2, 3], _Pe6)), sp.Rational("0.75"),
   "演習6 E(X)")
eq(40 * sp.Rational("0.75"), 30, "演習6 の 40 箱")
eq(F(30, 40), sp.Rational("0.75"), "割りもどすと 0.75")
chk(0 <= sp.Rational("0.75") <= 3, "演習6 の範囲")

_c = sp.Symbol("c")
_evc = (_c - 4) * F(1, 5) + (-4) * F(4, 5)
chk(sp.solve(sp.Eq(_evc, 0), _c) == [20], "演習7 c = 20")
eq(sp.simplify(_evc - (_c - 20) / 5), 0, "演習7 の式は (c-20)/5")
eq(20 - 4, 16, "当たりの利得は 16")
eq(16 * F(1, 5) + (-4) * F(4, 5), 0, "演習7 の検算")
eq(5 * 4, 20, "参加料の 5 倍が 20")
chk(sp.solve(sp.Eq(_c * F(1, 5), 0), _c) == [0], "引き忘れると c = 0")

eq(0 * F(1, 2) + 1 * F(1, 2), F(1, 2), "演習8 E(X)")
chk(F(1, 2) != 0 and F(1, 2) != 1, "演習8 は 0 でも 1 でもない")
eq(F(0 + 1, 2), F(1, 2), "対称性でも 1/2")

for _x in (2, 3, 4):
    chk(0 < F(_x - 1, 6) < 1, "演習9 の確率は 0 と 1 の間: x=%d" % _x)
eq(sum(F(x - 1, 6) for x in (2, 3, 4)), 1, "演習9 の合計")
eq(sum(x * F(x - 1, 6) for x in (2, 3, 4)), F(10, 3), "演習9 E(X)")
eq(2 * 1 + 3 * 2 + 4 * 3, 20, "演習9 の分子")
eq(F(20, 6), F(10, 3), "20/6 = 10/3")
chk(abs(float(F(10, 3)) - 3.33) < 0.01, "10/3 は約 3.33")
chk(F(10, 3) > 3, "演習9 は真ん中より大きい")

eq(3 * F(1, 2) + (-3) * F(1, 2), 0, "演習10 ゲーム A")
eq(10 * F(1, 5) + (-2) * F(4, 5), F(2, 5), "演習10 ゲーム B")
eq(F(10, 5) - F(8, 5), F(2, 5), "10/5 - 8/5")
chk(F(2, 5) > 0, "ゲーム B は正")
eq(100 * F(2, 5), 40, "100 回で 40 ドル")
eq(100 * 0, 0, "ゲーム A は 100 回でも 0")
eq(F(2, 5), sp.Rational("0.4"), "2/5 = 0.4")
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
chk(_nstmt >= 30, "ページの計算を %d 本たしかめた" % _nstmt)

# 確率の値は、すべて 0 以上 1 以下
_nprob = 0
for _m in re.finditer(r"P\([^)]*\)\s*=\s*(%s)" % _ATOM, TEXT):
    _nprob += 1
    _v = _tonum(_m.group(1))
    chk(0 <= _v <= 1, "確率が 0..1 の外: %s" % _m.group(0)[:60])
chk(_nprob >= 4, "確率の値を %d 個たしかめた" % _nprob)

# ══════════════════════════════════════════════════════════
# 15. 査読で直したところ（2026-09-08）
# ══════════════════════════════════════════════════════════

# --- B1 演習3 の答えの先出し -------------------------------------------
not_in_body("3.5", "演習3 の答え 3.5 は本文に出さない")
in_text("$E(X)$ は $2.4$ のような小数になりえます。", "B1 の言いかえ")
chk(sp.Rational("2.4") not in (F(7, 2), sp.Rational("2.7"), sp.Rational("1.7"),
                               sp.Rational("0.75"), F(20, 7), F(35, 12),
                               F(10, 3), F(1, 2)),
    "2.4 はどの答えとも重ならない")

# --- B2 「合計が 0 のまわりにとどまる」は誤り --------------------------
in_text("$N$ 回のあとの **$1$ 回あたりの平均**はおよそ $E(X)$ です。", "B2 平均で述べる")
in_text("合計そのものは $0$ から離れることもありますが、$N$ に比例して増えて"
        "いくことはありません。", "B2 合計についての正しい言い方")
not_in_text("この合計は $N$ が大きくなっても $0$ のまわりにとどまります",
            "誤った言い方は消した")
in_text("It means that the average gain per turn gets close to $\\$0$",
        "B2 例題4 の model answer")
not_in_text("over many turns the total gain stays near", "誤った答案例は消した")
# 反例：E(X)=0 でも、合計の散らばりは N とともに大きくなる
for _N in (100, 10000):
    _sd = sp.sqrt(_N * (3 ** 2))      # ±3 が半々のときの合計の標準偏差
    chk(float(_sd) > 0, "N=%d の合計の散らばり" % _N)
chk(float(sp.sqrt(10000 * 9)) > float(sp.sqrt(100 * 9)),
    "N が大きいほど合計の散らばりは大きい")
chk(float(sp.sqrt(10000 * 9)) / 10000 < float(sp.sqrt(100 * 9)) / 100,
    "それでも 1 回あたりの平均の散らばりは小さくなる")

# --- M1 Why it works の「およそ」 --------------------------------------
in_text("が**およその値として**出てきます。", "M1 近似のまま")
in_text("**$N$ を大きくするほど、この近似はよくなります。**", "M1 近似がよくなる")
in_text("（これは定義の動機づけであって、証明ではありません。）", "M1 動機づけ")
in_text("（最後の等号で $\\sum P(X = x_i) = 1$ を使いました）", "M1 合計 1 を使った")

# --- M2・M3 「かたよりで」を「中心からのずれで」に直した ---------------
in_text("**検算（(c) について、中心からのずれで）。**", "M2 例題1")
in_text("(-1.5)(0.1) + (-0.5)(0.3) + (0.5)(0.4) + (1.5)(0.2) = -0.15 - 0.15 "
        "+ 0.2 + 0.3 = 0.2", "M2 例題1 の計算")
not_in_text("いちばん確率が大きいのは $x = 3$ です。$2.7$ は $3$ の近くに",
            "最頻値の近く、という誤った検算は消した")
in_text("**検算（$E(X)$ について、中心からのずれで）。**", "M3 演習1")
not_in_text("$x = 0$ と $x = 1$ の合計 $0.4$ より大きいので", "誤った根拠は消した")
# 中心からのずれの計算が正しいこと
_P1c = [sp.Rational("0.1"), sp.Rational("0.3"), sp.Rational("0.4"),
        sp.Rational("0.2")]
eq(sum((x - sp.Rational("2.5")) * p for x, p in zip([1, 2, 3, 4], _P1c)),
   sp.Rational("0.2"), "例題1 の中心からのずれ")
eq(sp.Rational("2.5") + sp.Rational("0.2"), sp.Rational("2.7"), "2.5 + 0.2 = 2.7")
_P1e = [sp.Rational("0.15"), sp.Rational("0.25"), sp.Rational("0.35"),
        sp.Rational("0.25")]
eq(sum((x - sp.Rational("1.5")) * p for x, p in zip([0, 1, 2, 3], _P1e)),
   sp.Rational("0.2"), "演習1 の中心からのずれ")
eq(sp.Rational("1.5") + sp.Rational("0.2"), sp.Rational("1.7"), "1.5 + 0.2 = 1.7")
# 最頻値の近く、という主張が一般には偽であること（反例）
_bad = [sp.Rational("0.45"), sp.Rational("0.05"), sp.Rational("0.5"),
        sp.Rational("0")]
eq(sum(_bad), 1, "反例の確率の合計は 1")
eq(sum(x * p for x, p in zip([1, 2, 3, 4], _bad)), sp.Rational("2.05"),
   "反例では最頻値 3 に対して E(X)=2.05")
chk(abs(float(sp.Rational("2.05")) - 3) > 0.9, "最頻値からかなり離れる")
# 上下の確率の合計だけでは中点との大小が決まらないこと（反例）
_bad2 = [sp.Rational("0.4"), sp.Rational("0"), sp.Rational("0.6"),
         sp.Rational("0")]
eq(sum(x * p for x, p in zip([0, 1, 2, 3], _bad2)), sp.Rational("1.2"),
   "反例では上半分が 0.6 でも E(X)=1.2")
chk(sp.Rational("1.2") < sp.Rational("1.5"), "中点より小さい")

# --- N5 例題3 の表を昇順にした -----------------------------------------
in_text("| $x$ | $-4$ | $1$ | $7$ |", "N5 昇順の表")
in_text("E(X) = (-4)\\left(\\frac{1}{2}\\right) + 1\\left(\\frac{1}{3}\\right) "
        "+ 7\\left(\\frac{1}{6}\\right)", "N5 昇順の計算")
not_in_text("| $x$ | $7$ | $1$ | $-4$ |", "降順の表は消した")

# --- M4 例題3(b) の検算 -----------------------------------------------
in_text("**検算（(b) について、$4$ だけずらして）。**", "M4")
not_in_text("負の額 $-4$ が正の額より大きめです", "事実誤認は消した")
eq(5 * F(1, 3) + 11 * F(1, 6), F(21, 6), "ずらした平均は 21/6")
eq(F(21, 6) - F(24, 6), F(-3, 6), "4 を引きもどすと -3/6")
eq(F(-3, 6), F(-1, 2), "-3/6 = -1/2")
# 符号を落とすと、範囲の検算は通ってしまう
eq(7 * F(1, 6) + 1 * F(1, 3) + 4 * F(1, 2), F(21, 6), "符号を落とすと 21/6 = 3.5")
chk(-4 <= F(21, 6) <= 7, "符号を落としても範囲の検算は通ってしまう")
chk(F(21, 6) != F(-1, 2), "だからずらす検算が必要")

# --- M5 割りもどす検算を、回数からの検算にした -------------------------
in_text("**検算（(c) について、回数から）。**", "M5 例題3")
in_text("15(-4) + 10(1) + 5(7) = -60 + 10 + 35 = -15", "M5 例題3 の計算")
not_in_text("$\\dfrac{-15}{30} = -\\dfrac{1}{2}$ ✓", "循環した検算は消した")
in_text("**検算（回数から）。** $40$ 箱のうち、割れが $0$ 個の箱がおよそ "
        "$20$ 箱", "M5 演習6")
not_in_text("$\\dfrac{30}{40} = 0.75$ ✓", "循環した検算は消した（演習6）")
in_text("**検算（回数から）。** ゲーム B を $100$ 回すると、", "M5 演習10")
eq(30 * F(1, 2), 15, "30 回のうち -4 は 15 回")
eq(30 * F(1, 3), 10, "30 回のうち 1 は 10 回")
eq(30 * F(1, 6), 5, "30 回のうち 7 は 5 回")
eq(15 * (-4) + 10 * 1 + 5 * 7, -15, "回数からの合計は -15")
eq(40 * sp.Rational("0.5"), 20, "40 箱のうち 0 個は 20 箱")
eq(40 * sp.Rational("0.3"), 12, "1 個は 12 箱")
eq(40 * sp.Rational("0.15"), 6, "2 個は 6 箱")
eq(40 * sp.Rational("0.05"), 2, "3 個は 2 箱")
eq(0 * 20 + 1 * 12 + 2 * 6 + 3 * 2, 30, "回数からの合計は 30")
eq(100 * F(1, 5), 20, "100 回のうち +10 は 20 回")
eq(100 * F(4, 5), 80, "-2 は 80 回")
eq(20 * 10 + 80 * (-2), 40, "回数からの合計は 40")

# --- M6・M7 範囲の検算 -------------------------------------------------
in_text("$0 \\le 0.75 \\le 3$ ✓ 確率をかけ忘れて $0 + 1 + 2 + 3 = 6$ と",
        "M6 演習6 の範囲")
not_in_text("割れていない箱が半分あるので、$1$ より小さくなるのは自然です",
            "成り立たない理由は消した")
eq(0 + 1 + 2 + 3, 6, "かけ忘れると 6")
chk(not (0 <= 6 <= 3), "6 は範囲の外")
# 反例：P(0)=0.5 でも E(X) は 1 をこえられる
eq(0 * sp.Rational("0.5") + 3 * sp.Rational("0.5"), sp.Rational("1.5"),
   "反例では E(X)=1.5")
chk(sp.Rational("1.5") > 1, "P(0)=0.5 でも 1 をこえる")
in_text("ただし確率どうしを足しても $\\dfrac{1}{2} + \\dfrac{1}{2} = 1$ で範囲の"
        "中に入ってしまう", "M7 演習8 の範囲の限界")
chk(0 <= 1 <= 1, "確率を足した 1 も演習8 の範囲の中")

# --- M8 目標と、演習6 の (a) ------------------------------------------
in_text("$X$ が何を表すかを述べ、とりうる値をすべて書き出せる。", "M8 目標 1")
in_text("- $P(X \\ge 3)$ のような確率を、表から選んで足して求められる。",
        "M8 目標 P(X≥3)")
in_text("**(a)** [Describe what the value $X = 0$ means for a box", "M8 演習6(a)")
in_text("*$X$ is the number of broken eggs in one box, so $X = 0$ means",
        "M8 演習6(a) の model answer")
chk(TEXT.count("{.model-answer}") == 9, "model answer は 9 個")

# --- N6 p > 2、c > 4 --------------------------------------------------
in_text("a prize of $\\$p$, where $p > 2$, with probability", "N6 例題4")
in_text("a prize of $\\$c$, where $c > 4$, with probability", "N6 演習7")
chk(8 > 2, "例題4 の答え 8 は p > 2 を満たす")
chk(20 > 4, "演習7 の答え 20 は c > 4 を満たす")

# --- N7 折りたたみの説明 ----------------------------------------------
in_text("**解説**（なぜそうなるか。日本語です。英語の答案例が付くものも"
        "あります）。", "N7")

# --- N8 model answer の条件をそろえた ---------------------------------
in_text("A function that assigns positive numbers adding to $1$", "N8 例題2")
in_text("Since the formula assigns positive numbers adding to $1$", "N8 演習9")
not_in_text("assigns non-negative numbers adding to", "ずれた言い方は消した")

# --- N9 「もどして足します」の目的 ------------------------------------
chk(TEXT.count("これは**引き算をやり直すための検算**です。") == 2,
    "N9 目的を 2 か所に書いた")

# --- N1・N2・N3・N4 図 -------------------------------------------------
in_fig('"a losing game: gain $+3$', "N2 図の 1 つ目のゲーム")
in_fig('"a fair game: gain $+4$', "N2 図の 2 つ目のゲーム")
chk('"game A' not in FIGCODE and '"game B' not in FIGCODE,
    "図では game A / game B と呼ばない（演習10 と紛らわしい）")
in_fig('marker="v"', "N4 三角は線の上に置く")
in_text("(b) Two games are shown on a number line of gains, where the dots are "
        "the possible gains and their sizes show the probabilities while the "
        "triangle marks the expected value", "N3 キャプション")

print()
print("OK", OK, "/ NG", NG)
