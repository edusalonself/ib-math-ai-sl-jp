# -*- coding: utf-8 -*-
"""AA SL 4.8 のページを検算する。

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
QMD = os.path.join(ROOT, "aa-sl", "04-statistics-and-probability", "aasl-4-8.qmd")
FIGP = os.path.join(HERE, "make_aasl_4_8.py")

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
in_text("# SL 4.8 — The binomial distribution（二項分布） {#sec-aasl-4-8}", "見出し")

for _h in ("## What you should be able to do", "## The idea", "## Why it works",
           "## Worked examples", "## Common errors",
           "## Using your GDC (TI-Nspire CX II)", "## Exercises"):
    in_text(_h, "節 " + _h)

_secs = re.findall(r"^### (\d)\. .*\{#([a-z-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 8)] + ["1", "2", "3"],
    "### の番号 1..7 と GDC 1..3: %s" % [s[0] for s in _secs])
chk([s[1] for s in _secs] == ["when", "notation", "pmf", "range", "mean",
                              "model", "read",
                              "gdc-pdf", "gdc-cdf", "gdc-check"],
    "アンカー: %s" % [s[1] for s in _secs])
# GDC の節は Exercises の直前
chk(TEXT.index("## Using your GDC (TI-Nspire CX II)") > TEXT.index("## Common errors"),
    "GDC の節は Common errors の後")
chk(TEXT.index("## Using your GDC (TI-Nspire CX II)") < TEXT.index("## Exercises"),
    "GDC の節は Exercises の前")

chk(len(re.findall(r"^\[\d+\]\{\.ex-no\}", TEXT, re.M)) == 10, "演習 10 問")
chk(TEXT.count("::: {#exm-") == 4, "例題 4 つ")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep 9 個")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳 14")
chk(TEXT.count("</details>") == 14, "details 閉じ 14")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例 14")
chk(len(re.findall(r"^---$", TEXT, re.M)) == 6, "行頭 --- は 6 本")
chk(TEXT.count("{.callout-warning}") == 7, "callout-warning 7（誤り 6 + Paper 2 の注 1）")
chk(TEXT.count("{.callout-important}") == 2,
    "callout-important 2（B(n,p) と、平均・分散）")
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

in_text("(img/aasl-4-8-idea.svg){#fig-aasl48-idea width=100%}", "図の埋め込み")
in_text("@fig-aasl48-idea (a)", "図 (a) の参照")
in_text("@fig-aasl48-idea (b)", "図 (b) の参照")

# シラバスの引用は「Not required:」の 1 行だけ
_quotes = re.findall(r"^> (.+)$", TEXT, re.M)
chk(_quotes == ["Not required: Formal proof of mean and variance."],
    "引用は Not required の 1 行だけ: %s" % _quotes)
for _w in ("そのとおり", "もちろん", "簡単です", "自明", "当たり前", "明らか"):
    not_in_text(_w, "禁止語 " + _w)
for _w in ("得点になりません", "点になりません", "減点されます"):
    not_in_text(_w, "採点の断定 " + _w)

# ══════════════════════════════════════════════════════════
# 2. 式と公式集
# ══════════════════════════════════════════════════════════
in_text("X \\sim B(n, p)\n$$ {#eq-aasl48-not}", "B(n,p)")
in_text("P(X = x) = \\binom{n}{x} p^{x} (1 - p)^{n - x}\n$$ {#eq-aasl48-pmf}",
        "確率の式")
in_text("E(X) = np\n$$ {#eq-aasl48-mean}", "平均の式")
in_text("\\mathrm{Var}(X) = np(1 - p)\n$$ {#eq-aasl48-var}", "分散の式")
in_text("公式集の **4.8** の欄に *Binomial distribution* として載っています",
        "公式集 4.8 B(n,p)")
in_text("公式集の **4.8** の欄に *Mean* と *Variance* として載っています",
        "公式集 4.8 平均と分散")
in_text("**@eq-aasl48-pmf そのものは、公式集の 4.8 の欄にはありません。**",
        "確率の式は 4.8 にない")
in_text("$\\binom{n}{r}$ は Topic 1 の **1.9**（binomial theorem）の欄にあります。",
        "nCr は 1.9 の欄")
in_text("この式は公式集にありませんが", "σ の式は公式集にない")
in_text("{#tbl-aasl48-cond}", "4 条件の表")
in_text("{#tbl-aasl48-words}", "ことばと範囲の表")
in_text("{#tbl-aasl48-gdc}", "binomCdf の表")

# 確率の合計が 1 になること（記号のまま）
_p = sp.Symbol("p")
for _n in (1, 2, 5, 8):
    _tot = sum(sp.binomial(_n, _x) * _p ** _x * (1 - _p) ** (_n - _x)
               for _x in range(_n + 1))
    eq(sp.expand(_tot), 1, "n=%d のとき確率の合計は 1" % _n)
# 分散が p=1/2 で最大
eq(sp.expand(_p * (1 - _p) - (-(_p - sp.Rational(1, 2)) ** 2
                              + sp.Rational(1, 4))), 0, "平方完成が正しい")
for _pv in (sp.Rational(1, 10), sp.Rational(1, 4), sp.Rational(3, 4),
            sp.Rational(9, 10)):
    chk(_pv * (1 - _pv) < sp.Rational(1, 4), "p=%s では 1/4 未満" % _pv)
eq(sp.Rational(1, 2) * sp.Rational(1, 2), sp.Rational(1, 4), "p=1/2 で 1/4")

# ══════════════════════════════════════════════════════════
# 3. Why it works
# ══════════════════════════════════════════════════════════
in_text("$n = 4$、$x = 2$ なら、成功する回の選び方は $\\binom{4}{2} = 6$ 通り",
        "Why it works の例")
eq(sp.binomial(4, 2), 6, "4C2 = 6")
in_text("[SL 1.9 の binomial theorem](../01-number-and-algebra/aasl-1-9.qmd)",
        "1.9 への参照")
in_text("[SL 4.5 の期待される回数](aasl-4-5.qmd#expected)", "4.5 への参照")
in_text("[SL 4.6b](aasl-4-6b.qmd#without)", "4.6b への参照（もどさない）")
in_text("[SL 4.6b](aasl-4-6b.qmd#independent)", "4.6b への参照（独立）")
in_text("[SL 4.3](aasl-4-3.qmd#sd)", "4.3 への参照")
in_text("$1$ 回あたりの確率に回数をかける、という形が共通しています。",
        "4.5 とのつながり")
not_in_text("$X \\sim B(128,\\ 0.1)$", "欠席の例は本文に出さない（演習10 と矛盾）")

# ★ 例題・演習の答えを本文に出していないこと
for _v in ("0.311", "0.679", "0.321", "0.268", "0.678", "0.231", "0.398",
           "0.227", "0.324", "0.420", "0.193", "0.387", "0.736", "0.0781"):
    not_in_body(_v, "答え %s は本文に出さない" % _v)
not_in_body("2.88", "例題4 の分散は本文に出さない")
not_in_body("2.55", "演習2 の分散は本文に出さない")

# ══════════════════════════════════════════════════════════
# 4. 図
# ══════════════════════════════════════════════════════════
in_fig("N1, P1 = 7, 0.4", "図 (a) は B(7, 0.4)")
in_fig("N2, P2 = 6, 0.5", "図 (b) は B(6, 0.5)")
_fig_pairs = [(7, sp.Rational("0.4")), (6, sp.Rational("0.5"))]
_page_pairs = [(8, sp.Rational("0.25")), (10, sp.Rational("0.8")),
               (15, sp.Rational("0.8")), (12, sp.Rational("0.4")),
               (6, sp.Rational("0.3")), (20, sp.Rational("0.15")),
               (12, sp.Rational("0.5")), (25, sp.Rational("0.04")),
               (30, sp.Rational("0.6")), (10, sp.Rational("0.25")),
               (14, sp.Rational("0.2"))]
for _fp in _fig_pairs:
    chk(_fp not in _page_pairs, "図の %s は例題・演習と重ならない" % (_fp,))
eq(7 * sp.Rational("0.4"), sp.Rational("2.8"), "図 (a) の np は 2.8")
in_fig("$E(X) = np = 2.8$", "図 (a) のラベル")
for _n, _p2 in _fig_pairs:
    eq(sum(sp.binomial(_n, _x) * _p2 ** _x * (1 - _p2) ** (_n - _x)
           for _x in range(_n + 1)), 1, "図 B(%d, %s) の合計は 1" % (_n, _p2))
# 図に確率の値そのものは書かない
chk("0.29" not in FIGCODE and "0.31" not in FIGCODE, "図に確率の値は書かない")

# ══════════════════════════════════════════════════════════
# 5. 二項分布の値（例題）
# ══════════════════════════════════════════════════════════
def bp(n, p, x):
    return sp.binomial(n, x) * sp.Rational(p) ** x * (1 - sp.Rational(p)) ** (n - x)


def bc(n, p, a, b):
    return sum(bp(n, p, x) for x in range(a, b + 1))


def r3(v):
    return float(sp.N(v, 20))


# 例題1 B(8, 0.25)
chk(abs(r3(bp(8, "0.25", 2)) - 0.311) < 5e-4, "例題1(a) 0.311: %.5f" % r3(bp(8, "0.25", 2)))
chk(abs(r3(bc(8, "0.25", 0, 2)) - 0.679) < 5e-4, "例題1(b) 0.679")
chk(abs(r3(1 - bc(8, "0.25", 0, 2)) - 0.321) < 5e-4, "例題1(c) 0.321")
eq(8 * sp.Rational("0.25"), 2, "例題1(d) E(X)")
eq(8 * sp.Rational("0.25") * sp.Rational("0.75"), sp.Rational("1.5"),
   "例題1(d) Var(X)")
chk(bc(8, "0.25", 0, 2) > bp(8, "0.25", 2), "P(X≤2) > P(X=2)")
chk(sp.Rational("1.5") < 2, "Var < np")
chk(0 <= 2 <= 8, "E(X) は 0..n の間")

# 例題2 B(10, 0.8)
chk(abs(r3(bp(10, "0.8", 9)) - 0.268) < 5e-4, "例題2(a) 0.268")
chk(abs(r3(bc(10, "0.8", 8, 10)) - 0.678) < 5e-4, "例題2(b) 0.678")
chk(abs(r3(bc(10, "0.8", 0, 7)) - 0.3222) < 5e-4, "例題2 余事象 0.3222")
eq(bc(10, "0.8", 0, 7) + bc(10, "0.8", 8, 10), 1, "余事象の合計は 1")
eq(10 * sp.Rational("0.8"), 8, "例題2(c) E(X)")
chk(bc(10, "0.8", 8, 10) > bp(10, "0.8", 9), "P(X≥8) > P(X=9)")
chk(bp(10, "0.8", 8) < 1, "P(X=8) は 1 よりずっと小さい")

# 例題3 B(15, 0.8)
chk(abs(r3(bp(15, "0.8", 13)) - 0.231) < 5e-4, "例題3(b) 0.231")
chk(abs(r3(bc(15, "0.8", 13, 15)) - 0.398) < 5e-4, "例題3(c) 0.398")
chk(abs(r3(bc(15, "0.8", 0, 12)) - 0.6019) < 5e-4, "例題3 余事象 0.6019")
eq(15 * sp.Rational("0.8"), 12, "例題3(d) E(X)")
eq(15 * sp.Rational("0.8") * sp.Rational("0.2"), sp.Rational("2.4"),
   "例題3(d) Var(X)")
chk(abs(float(sp.sqrt(sp.Rational("2.4"))) - 1.549) < 5e-3, "√2.4 ≈ 1.55")
chk(12 - 2 * float(sp.sqrt(sp.Rational("2.4"))) < 13 <= 15, "13 は 2σ の中")
chk(bc(15, "0.8", 13, 15) > bp(15, "0.8", 13), "P(X≥13) > P(X=13)")

# 例題4 B(12, p), E=4.8
_pv = sp.Symbol("pv")
chk(sp.solve(sp.Eq(12 * _pv, sp.Rational("4.8")), _pv) == [sp.Rational("0.4")],
    "例題4(a) p = 0.4")
eq(12 * sp.Rational("0.4") * sp.Rational("0.6"), sp.Rational("2.88"),
   "例題4(b) Var(X)")
chk(abs(r3(bp(12, "0.4", 5)) - 0.227) < 5e-4, "例題4(c) 0.227")
chk(abs(float(sp.sqrt(sp.Rational("2.88"))) - 1.6971) < 1e-3, "√2.88 ≈ 1.70")
chk((12 - sp.Rational("4.8")) / float(sp.sqrt(sp.Rational("2.88"))) > 4,
    "12 は平均から 4σ より上")
chk(abs(r3(bp(12, "0.4", 12)) - 1.6777e-5) < 1e-8, "P(X=12) ≈ 1.7e-5")
chk(r3(bp(12, "0.4", 12)) < 1e-4, "P(X=12) はごく小さい")
chk(0 <= sp.Rational("0.4") <= 1, "p は 0..1 の間")
chk(sp.Rational("2.88") < sp.Rational("4.8"), "Var < np")

# ══════════════════════════════════════════════════════════
# 6. 演習の答え
# ══════════════════════════════════════════════════════════
chk(abs(r3(bp(6, "0.3", 2)) - 0.324) < 5e-4, "演習1 P(X=2)")
chk(abs(r3(bc(6, "0.3", 0, 1)) - 0.420) < 5e-4, "演習1 P(X≤1)")
chk(abs(r3(bp(6, "0.3", 0)) - 0.117649) < 1e-6, "演習1 P(X=0)")
chk(abs(r3(bp(6, "0.3", 1)) - 0.302526) < 1e-6, "演習1 P(X=1)")
eq(bp(6, "0.3", 0) + bp(6, "0.3", 1), bc(6, "0.3", 0, 1), "分けて足しても同じ")
eq(6 * sp.Rational("0.3"), sp.Rational("1.8"), "演習1 np = 1.8")

eq(20 * sp.Rational("0.15"), 3, "演習2 E(X)")
eq(20 * sp.Rational("0.15") * sp.Rational("0.85"), sp.Rational("2.55"),
   "演習2 Var(X)")
chk(abs(float(sp.sqrt(sp.Rational("2.55"))) - 1.5969) < 1e-3, "√2.55 ≈ 1.60")
chk(sp.Rational("2.55") < 3, "Var < np")
chk(0 <= 3 <= 20, "E(X) は 0..n の間")

chk(abs(r3(bp(12, "0.5", 7)) - 0.193) < 5e-4, "演習3 P(X=7)")
chk(abs(r3(bc(12, "0.5", 7, 12)) - 0.387) < 5e-4, "演習3 P(X≥7)")
eq(bc(12, "0.5", 7, 12), bc(12, "0.5", 0, 5), "p=0.5 の対称性")
chk(abs(r3(bp(12, "0.5", 6)) - 0.226) < 5e-4, "演習3 P(X=6)")
eq(bc(12, "0.5", 0, 5) + bp(12, "0.5", 6) + bc(12, "0.5", 7, 12), 1,
   "3 つに分けて足すと 1")
chk(bc(12, "0.5", 7, 12) < sp.Rational(1, 2), "P(X≥7) は 1/2 より小さい")

chk(abs(r3(bc(25, "0.04", 0, 1)) - 0.736) < 5e-4, "演習4 P(X≤1)")
chk(abs(r3(bp(25, "0.04", 0)) - 0.3604) < 5e-4, "演習4 P(X=0)")
chk(abs(r3(bp(25, "0.04", 1)) - 0.3754) < 5e-4, "演習4 P(X=1)")
eq(25 * sp.Rational("0.04"), 1, "演習4 np = 1")
chk(bc(25, "0.04", 0, 1) > sp.Rational(1, 2), "山を含むので 1/2 より大きい")

eq(F(13, 52), F(1, 4), "演習5 1 枚目のハート")
chk(F(12, 51) != F(1, 4), "演習5 2 枚目は 1/4 でない")
chk(abs(float(F(12999, 51999)) - 0.25) < 1e-4, "大きな山なら 1/4 に近い")

chk(sp.solve(sp.Eq(sp.Symbol("nn") * sp.Rational("0.6"), 18),
             sp.Symbol("nn")) == [30], "演習6 n = 30")
eq(30 * sp.Rational("0.6") * sp.Rational("0.4"), sp.Rational("7.2"),
   "演習6 Var(X)")
chk(sp.Rational("7.2") < 18, "Var < np")
chk(sp.Integer(30).is_integer, "n は整数")

chk(abs(r3(bc(10, "0.25", 5, 10)) - 0.0781) < 5e-5, "演習7 P(X≥5)")
chk(abs(r3(bc(10, "0.25", 0, 4)) - 0.9219) < 5e-5, "演習7 余事象")
eq(bc(10, "0.25", 0, 4) + bc(10, "0.25", 5, 10), 1, "演習7 の合計は 1")
eq(10 * sp.Rational("0.25"), sp.Rational("2.5"), "演習7 np = 2.5")
chk(abs(float(sp.sqrt(10 * sp.Rational("0.25") * sp.Rational("0.75"))) - 1.369)
    < 5e-3, "演習7 σ ≈ 1.37")
chk(abs((5 - 2.5) / 1.3693 - 1.83) < 0.02, "5 は平均から約 1.8σ")
chk(bc(10, "0.25", 5, 10) < sp.Rational(1, 2), "0.0781 は 0.5 より小さい")

chk(float(sp.Rational("0.8") ** 13) > 0.05, "n=13 では 0.05 をこえる")
chk(float(sp.Rational("0.8") ** 14) < 0.05, "n=14 で 0.05 を下回る")
chk(abs(float(sp.Rational("0.8") ** 13) - 0.0550) < 5e-5, "0.8^13 = 0.0550")
chk(abs(float(sp.Rational("0.8") ** 14) - 0.0440) < 5e-5, "0.8^14 = 0.0440")
chk(abs(1 - float(sp.Rational("0.8") ** 14) - 0.956) < 5e-4, "1 - 0.8^14 = 0.956")
for _k in range(1, 20):
    chk(sp.Rational("0.8") ** (_k + 1) < sp.Rational("0.8") ** _k,
        "0.8^n は単調に減る: k=%d" % _k)
eq(bp(14, "0.2", 0), sp.Rational("0.8") ** 14, "P(X=0) = 0.8^n")

chk(abs(r3(bp(12, "0.4", 5)) - 0.227) < 5e-4, "演習9 P(X=5)")
chk(abs(r3(bc(12, "0.4", 2, 8)) - 0.965) < 5e-4, "演習9 P(2≤X≤8)")
chk(sp.Rational("4.8") - 2 * float(sp.sqrt(sp.Rational("2.88"))) < 2,
   "4.8 - 2σ は 2 より小さい")
chk(sp.Rational("4.8") + 2 * float(sp.sqrt(sp.Rational("2.88"))) > 8,
   "4.8 + 2σ は 8 より大きい")
chk(bp(12, "0.4", 5) < sp.Rational(1, 2), "P(X=5) は 0.5 より小さい")
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
chk(_nstmt >= 15, "ページの計算を %d 本たしかめた" % _nstmt)

# 確率の値は、すべて 0 以上 1 以下
_nprob = 0
for _m in re.finditer(r"P\([^)]*\)\s*=\s*(%s)" % _ATOM, TEXT):
    _nprob += 1
    _v = _tonum(_m.group(1))
    chk(0 <= _v <= 1, "確率が 0..1 の外: %s" % _m.group(0)[:60])
chk(_nprob >= 3, "確率の値を %d 個たしかめた" % _nprob)

# ══════════════════════════════════════════════════════════
# 15. 査読で直したところ（2026-09-08）
# ══════════════════════════════════════════════════════════

# --- B1 有効数字 3 桁 ---------------------------------------------------
in_text("答えは**有効数字 $3$ 桁**（$3$ significant figures）で書きます。",
        "B1 有効数字")
not_in_text("答えは小数第 $3$ 位まで（$3$ significant figures）",
            "誤った言い方は消した")
# 0.0781 は有効数字 3 桁だが、小数第 3 位ではない
chk(len("0781".lstrip("0")) == 3, "0.0781 は有効数字 3 桁")
chk(round(0.0781, 3) != 0.0781, "小数第 3 位に丸めると 0.0781 ではなくなる")

# --- B2 GDC 節 3 の役に立たない検算 ------------------------------------
in_text("**`binomPdf` の $x$ を $1$ つずつ変えて、いちばん大きくなる $x$ を"
        "見ます。**", "B2 直した検算")
not_in_text("答えが $1$ になれば、$n$ と $p$ の入力は正しいはずです",
            "何も検出しない検算は消した")
# 0 から n まで足すと、どんな p でも 1（だから検算にならない）
for _pp in ("0.04", "0.4", "0.9"):
    eq(bc(8, _pp, 0, 8), 1, "p=%s でも 0..n の合計は 1" % _pp)

# --- B3 例題1(c) の循環した検算 ----------------------------------------
in_text("**検算（(c) について、別の入力で）。** `binomCdf(8, 0.25, 3, 8)` を"
        "直接使うと $0.3214\\ldots$ です", "B3 直した検算")
not_in_text("$0.6785 + 0.3215 = 1$ ✓", "循環した検算は消した")
chk(abs(r3(bc(8, "0.25", 3, 8)) - 0.32146) < 1e-4, "直接の binomCdf は 0.3215")
eq(bc(8, "0.25", 3, 8), 1 - bc(8, "0.25", 0, 2), "直接でも余事象でも同じ")

# --- M1・M2・M3 GDC の記述を検証ずみの範囲に ---------------------------
not_in_text("ctrl + doc → Add Calculator", "検証していない番号は書かない")
not_in_text("Binomial Pdf", "検証していないメニュー名は書かない")
not_in_text("Binomial Cdf", "検証していないメニュー名は書かない（2）")
in_text("計算画面で `menu → Statistics → Distributions` を開き、二項分布の Pdf を"
        "選びます。", "M1 道すじ")
not_in_text("**$x$ を空けると、$0$ から $n$ までの一覧が出ます。**",
            "検証していない使い方は消した")
in_text("$p$ を $0.04$ と $0.4$ のように桁ちがいで入れていないかを見ます。",
        "m10 直した診断")
# 検証ずみの関数名だけを使っていること
for _fn in ("binomPdf", "binomCdf"):
    chk(_fn in TEXT, "検証ずみの関数 %s を使う" % _fn)
for _bad in ("binompdf", "binomialPdf", "BinomPdf", "invBinom"):
    not_in_text(_bad, "検証していない関数名 %s は使わない" % _bad)

# --- M4 演習8 の検算 ----------------------------------------------------
in_text("**検算（GDC で別の道から）。** `binomCdf(13, 0.2, 0, 0)` は $0.0550$",
        "M4 別の道")
in_text("**検算（$0.2$ と $0.8$ の取りちがい）。**", "M4 取りちがい")
eq(bc(13, "0.2", 0, 0), sp.Rational("0.8") ** 13, "binomCdf(13,0.2,0,0) = 0.8^13")
eq(bc(14, "0.2", 0, 0), sp.Rational("0.8") ** 14, "binomCdf(14,0.2,0,0) = 0.8^14")
chk(abs(float(sp.Rational("0.2") ** 13) - 8.192e-10) < 1e-13,
    "0.2^13 は約 8.2e-10")
chk(float(sp.Rational("0.2") ** 13) < 1e-8, "取りちがえると極端に小さい")

# --- M5・M6 第 6 節の例 ------------------------------------------------
in_text("- **回どうしが影響しあう。** 同じ家に住む人、同じ日に同じ場所で測った"
        "測定値、など。", "M5 直した例")
not_in_text("同じクラスの生徒、同じ機械で連続して作った製品",
            "演習10・演習4 と重なる例は消した")

# --- M7 Why it works の欠席の例 ----------------------------------------
in_text("**$E(X) = np$ そのものには、独立性は要りません。**",
        "M08 np に独立性は不要")
in_text("**独立性が要るのは、ここで $X$ を二項分布として扱うためです。**",
        "M08 独立性が要る理由")
not_in_text("ただし、$np$ が使えるかどうかは @tbl-aasl48-cond の $4$ 条件が"
            "成り立つかどうかで決まります。", "M08 旧記述が消えている")
# 赤2・白2 から、もどさずに 2 個。赤の個数の期待値は 2 x 1/2 = 1
_pr = [F(1, 6), F(4, 6), F(1, 6)]   # 赤 0 個・1 個・2 個
chk(sum(_pr) == 1, "M08 非復元の分布の和は 1")
chk(sum(_k * _p for _k, _p in enumerate(_pr)) == 1,
    "M08 非復元でも E(X) = np = 1")
# 同じ n, p の二項分布とは分散がちがう（独立でないから）
chk(sum(_k * _k * _p for _k, _p in enumerate(_pr)) - 1
    != 2 * F(1, 2) * F(1, 2), "M08 分散は二項とちがう")
# C10: 単元全体を Paper 1 の対象外にしていない
in_text("**単元全体が Paper 1 の対象外というわけではありません。**",
        "C10 4.8 単元全体ではない")
not_in_text("## この項目は Paper 2 です", "C10 4.8 断定が消えている")

# --- M8 「もどさない → 確率が毎回変わる」 ------------------------------
in_text("前に何が出たかで次の確率が変わるので、独立の条件が崩れます", "M8 第 1 節")
in_text("- **もどさずに取り出す。** $1$ 回目の結果が分かると、$2$ 回目の確率が"
        "変わります。", "M8 第 6 節")
in_text("回数は $5$ で決まっていて、結果も $2$ 通りですが、各回が独立では"
        "ありません。", "M8 演習5 の解説")
not_in_text("the success probability is not constant", "誤った言い方は消した")
not_in_text("もどさずに取り出す**場面では確率が毎回変わるので", "誤った言い方は消した（2）")
# 反例：1 枚目を見なければ 2 枚目がハートである確率は 1/4 のまま
_hearts = 13
_deck = 52
_p2 = (F(_hearts, _deck) * F(_hearts - 1, _deck - 1)
       + F(_deck - _hearts, _deck) * F(_hearts, _deck - 1))
eq(_p2, F(1, 4), "1 枚目を見なければ 2 枚目のハートも 1/4")
chk(F(12, 51) != F(1, 4), "1 枚目がハートと分かれば変わる")

# --- M9 演習8 に (a) を足した ------------------------------------------
in_text("**(a)** [Write down an expression for $P(X = 0)$ in terms of $n$. "
        "Explain why the binomial coefficient equals $1$ in this case.]{.q-en}",
        "M9 演習8(a)")
in_text("P(X = 0) = \\binom{n}{0}(0.2)^{0}(0.8)^{n} = 0.8^{n}", "M9 演習8(a) の式")
in_text("The coefficient $\\binom{n}{0}$ counts the ways of choosing which "
        "trials are successes", "M9 演習8(a) の model answer")
eq(sp.binomial(9, 0), 1, "nC0 = 1")
eq(sp.Rational("0.2") ** 0, 1, "0.2^0 = 1")
chk(TEXT.count("{.model-answer}") == 9, "model answer は 9 個")

# --- M10 演習10 の検算 -------------------------------------------------
in_text("**検算（$4$ 条件のどれを名指ししたか）。**", "M10")
in_text("という**向き**まで書けているかを見ます。", "M10 向き")
not_in_text("もし独立なら、$1$ 人休んだことが他の人の確率を変えないはずです",
            "定義の言いかえは消した")

# --- m1 演習4 のリンク -------------------------------------------------
in_text("$p$ は $0$ と $1$ の間の数です（[第 2 節](#notation)）。", "m1")
not_in_text("[第 3 節の誤り](#read)", "節番号のずれは直した")

# --- m2 例題3 の検算の見出し -------------------------------------------
in_text("**検算（(b) について、標準偏差で）。** $\\sqrt{2.4} \\approx 1.55$", "m2 (b)")
in_text("**検算（(d) について、大小で）。** $\\mathrm{Var}(X) = 2.4$ は $np = 12$",
        "m2 (d)")

# --- m3 例題3(a) の検算 ------------------------------------------------
in_text("**検算（(a) について、$4$ つ全部に触れたか）。**", "m3")
in_text("**補足（袋の大きさ）。**", "m3 補足に格下げ")

# --- m4 図 (b) のタイトル ----------------------------------------------
in_fig("(b) $X \\\\sim B(6,\\\\ 0.5)$: $P(X \\\\leq 2)$ adds the bars up ",
       "m4 図 (b) のタイトル")

# --- m5 キャプション ---------------------------------------------------
in_text("this panel uses a success probability below one half, so the bars are "
        "not symmetric", "m5 キャプション (a)")
in_text("(b) The same kind of diagram for a success probability of one half is "
        "symmetric", "m5 キャプション (b)")

# --- m6 演習9 を B(20, 0.35) にした ------------------------------------
in_text("[9]{.ex-no} [For $X \\sim B(20,\\ 0.35)$ we have $E(X) = 7$.", "m6 演習9")
not_in_text("[9]{.ex-no} [For $X \\sim B(12,\\ 0.4)$", "例題4 と同じ分布は消した")
eq(20 * sp.Rational("0.35"), 7, "演習9 E(X) = 7")
eq(20 * sp.Rational("0.35") * sp.Rational("0.65"), sp.Rational("4.55"),
   "演習9 Var(X) = 4.55")
chk(abs(float(sp.sqrt(sp.Rational("4.55"))) - 2.133) < 5e-3, "√4.55 ≈ 2.13")
chk(abs(r3(bp(20, "0.35", 7)) - 0.184) < 5e-4, "演習9 P(X=7) = 0.184")
chk(abs(r3(bc(20, "0.35", 3, 11)) - 0.968) < 5e-4, "演習9 P(3≤X≤11) = 0.968")
chk(7 - 2 * float(sp.sqrt(sp.Rational("4.55"))) < 3, "7 - 2σ は 3 より小さい")
chk(7 + 2 * float(sp.sqrt(sp.Rational("4.55"))) > 11, "7 + 2σ は 11 より大きい")

# --- m7 演習4 を fewer than にした -------------------------------------
in_text("Find the probability that the box contains fewer than two faulty "
        "components.", "m7 演習4")
in_text("`fewer than two` は $X \\le 1$ です（@tbl-aasl48-words）。$2$ は"
        "含みません。", "m7 演習4 の解説")
# fewer than / more than を使う問いが、実際にあること
chk("fewer than" in TEXT and "at most" in TEXT and "at least" in TEXT,
    "境目のことばが 3 種類そろっている")

# --- m8 演習3 の解答例 -------------------------------------------------
in_text("*binomPdf*$(12, 0.5, 7)$", "m8 演習3 の GDC 入力")
in_text("*binomCdf*$(12, 0.5, 7, 12)$", "m8 演習3 の GDC 入力（2）")

# --- m9 Var の最大に n を固定 ------------------------------------------
in_text("**$n$ を決めておくと、$\\mathrm{Var}(X)$ は $p = 0.5$ のとき最大に"
        "なります。**", "m9")
# n を動かせば、いくらでも大きくなる
chk(100 * sp.Rational("0.1") * sp.Rational("0.9")
    > 10 * sp.Rational("0.5") * sp.Rational("0.5"),
    "n を動かすと p=0.5 でなくても大きくなる")

# --- m11 例題2(d) の model answer --------------------------------------
in_text("the number scored varies from set to set.*", "m11")
not_in_text("$P(X = 8)$ is well below $1$", "情報量のない一文は消した")

# --- m12 例題4 の検算の順 ----------------------------------------------
chk(TEXT.index("**検算（(b) について、大小で）。**")
    < TEXT.index("**検算（(c) について、$np$ との位置で）。**"),
    "m12 例題4 の検算は (b) → (c) の順")

# --- m13・m14 演習7 ----------------------------------------------------
in_text("*about $7.8\\%$ of guessers reach $5$ correct", "m13")
not_in_text("*about $8\\%$ of guessers", "8% は 7.8% に直した")
in_text("$0.0781$ は $\\dfrac{1}{2}$ よりずっと小さく、$0.001$ ほど小さくもない",
        "m14")
not_in_text("$0.0781$ という値と合っています。", "言い切りは直した")
chk(sp.Rational("0.0781") < sp.Rational(1, 2), "0.0781 < 1/2")
chk(sp.Rational("0.0781") > sp.Rational("0.001"), "0.0781 > 0.001")

# ══════════════════════════════════════════════════════════
# E10  演習2 — 非復元と、二項モデルによる近似
# ══════════════════════════════════════════════════════════
in_text("The batch is large compared with the sample, so the components "
        "may be treated as independent. Using a binomial model, find "
        "$E(X)$", "E10 演習2 の英語")
in_text("バッチは標本にくらべて十分大きいので、各部品は独立とみなしてよい"
        "ものとします。", "E10 演習2 の訳")
in_text("**取り出しは、ほんとうは非復元です。**", "E10 非復元だと断る")
in_text("独立とみなして**二項モデルで近似**します", "E10 近似だと書く")
in_text("**$E(X) = np = 3$ は、非復元でも成り立ちます**",
        "E10 平均は非復元でも成立")
in_text("**$\\mathrm{Var}(X) = 2.55$ は、独立とみなしたモデルでの値**",
        "E10 分散はモデルの値")
not_in_text("超幾何", "E10 超幾何分布は持ち出さない")
chk(20 * 0.15 == 3, "E10 E(X) = 3")
chk(abs(20 * 0.15 * 0.85 - 2.55) < 1e-12, "E10 Var(X) = 2.55")

print()
print("OK", OK, "/ NG", NG)
