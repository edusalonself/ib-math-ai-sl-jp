# -*- coding: utf-8 -*-
"""AA SL 4.6b のページを検算する。

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
QMD = os.path.join(ROOT, "aa-sl", "04-statistics-and-probability", "aasl-4-6b.qmd")
FIGP = os.path.join(HERE, "make_aasl_4_6b.py")

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
in_text("# SL 4.6b — Conditional probability and independence"
        "（条件付き確率と独立） {#sec-aasl-4-6b}", "見出し")

for _h in ("## What you should be able to do", "## The idea", "## Why it works",
           "## Worked examples", "## Common errors", "## Exercises"):
    in_text(_h, "節 " + _h)

_secs = re.findall(r"^### (\d)\. .*\{#([a-z-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 8)],
    "### の番号 1..7: %s" % [s[0] for s in _secs])
chk([s[1] for s in _secs] == ["restrict", "formula", "twoway", "multiply",
                              "without", "independent", "compare"],
    "アンカー: %s" % [s[1] for s in _secs])

chk(len(re.findall(r"^\[\d+\]\{\.ex-no\}", TEXT, re.M)) == 10, "演習 10 問")
chk(TEXT.count("::: {#exm-") == 4, "例題 4 つ")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep 9 個")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳 14")
chk(TEXT.count("</details>") == 14, "details 閉じ 14")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例 14")
chk(len(re.findall(r"^---$", TEXT, re.M)) == 6, "行頭 --- は 6 本")
chk(TEXT.count("{.callout-warning}") == 7, "callout-warning 7（誤り 6 + 電卓 1）")
chk(TEXT.count("{.callout-important}") == 2,
    "callout-important 2（公式集 4.6 の条件付き確率と独立）")
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
chk(len(_qs) == 8, "Explain 系の問いは 8: %d" % len(_qs))

for _i, _m in enumerate(re.findall(r"\{\.model-answer\}(.*?):::", TEXT, re.S), 1):
    _b = _m.replace("**試験ではこう書く**", "")
    chk(len(_b.split()) <= 115, "model answer %d は 115 語以内" % _i)
    chk(not [c for c in _b if "぀" <= c <= "ヿ" or "一" <= c <= "鿿"],
        "model answer %d に日本語がない" % _i)

in_text("(img/aasl-4-6b-idea.svg){#fig-aasl46b-idea width=100%}", "図の埋め込み")
in_text("@fig-aasl46b-idea (a)", "図 (a) の参照")
in_text("@fig-aasl46b-idea (b)", "図 (b) の参照")

chk(not re.search(r"^> ", TEXT, re.M),
    "引用ブロックは使わない（4.6 に Not required はない）")
not_in_text("シラバス", "シラバスへの言及はしない")
for _w in ("そのとおり", "もちろん", "簡単です", "自明"):
    not_in_text(_w, "禁止語 " + _w)

# ══════════════════════════════════════════════════════════
# 2. 式と公式集
# ══════════════════════════════════════════════════════════
in_text("P(A \\mid B) = \\frac{P(A \\cap B)}{P(B)}\n$$ {#eq-aasl46b-cond}",
        "条件付き確率の式")
in_text("P(A \\cap B) = P(B)\\,P(A \\mid B)\n$$ {#eq-aasl46b-mult}", "かけ算の形")
in_text("P(A \\cap B) = P(A)P(B)\n$$ {#eq-aasl46b-indep}", "独立の式")
in_text("公式集の **4.6** の欄に *Conditional probability* として載っています",
        "公式集 4.6 conditional")
in_text("公式集の **4.6** の欄に *Independent events* として載っています",
        "公式集 4.6 independent")
in_text("**@eq-aasl46b-mult は、公式集にはこの形では載っていません。**",
        "かけ算の形は公式集にない")
in_text("縦棒の**右**にあるほうが分母です。", "分母は右")
in_text("**$P(B) = 0$ のときは使えません。**", "P(B)=0 は使えない")
in_text("{#tbl-aasl46b-twoway}", "二元表の表")
in_text("{#tbl-aasl46b-compare}", "排反と独立の表")

# 記号のままで、条件付き確率と独立の関係をたしかめる
_pa, _pb, _pab = sp.symbols("p_A p_B p_AB", positive=True)
eq(sp.simplify((_pab / _pb) * _pb), _pab, "P(A|B)·P(B) = P(A∩B)")
eq(sp.simplify((_pa * _pb) / _pb), _pa, "独立なら P(A|B) = P(A)")
# 排反かつ独立なら、どちらかが 0
_s = sp.solve(sp.Eq(_pa * _pb, 0), _pb)
chk(_s == [] or all(v == 0 for v in _s), "排反かつ独立は P(A)P(B)=0 のときだけ")
chk(sp.Rational(3, 10) * sp.Rational(1, 2) != 0, "0.3×0.5 は 0 でない")

# ══════════════════════════════════════════════════════════
# 3. Why it works —— もどさない場合の数え上げ
# ══════════════════════════════════════════════════════════
in_text("図 (b) と同じ袋で考えます。白玉 $2$ 個と黒玉 $3$ 個に", "Why it works の袋")
in_text("5 \\times 4 = 20", "5×4 = 20")
in_text("$\\dfrac{2}{5} \\times \\dfrac{1}{4} = \\dfrac{2}{20}$", "枝でかける")
eq(5 * 4, 20, "もどさないと 5×4")
eq(F(2, 5) * F(1, 4), F(2, 20), "2/5 × 1/4 = 2/20")
eq(5 * 5, 25, "もどせば 5×5")
eq(F(2 * 2, 5 * 5), F(4, 25), "もどせば 4/25")
eq(2 * 25, 50, "たすき掛け 2×25")
eq(4 * 20, 80, "たすき掛け 4×20")
chk(F(2, 20) < F(4, 25), "もどしたほうが大きい")
# 実際に数え上げてたしかめる
import itertools as _it
_BALLS5 = ["W1", "W2", "B1", "B2", "B3"]
_wo = list(_it.permutations(_BALLS5, 2))
_wi = list(_it.product(_BALLS5, repeat=2))
chk(len(_wo) == 20, "もどさない組は 20")
chk(len(_wi) == 25, "もどす組は 25")
chk(sum(1 for p in _wo if p[0][0] == "W" and p[1][0] == "W") == 2, "もどさず白白は 2")
chk(sum(1 for p in _wi if p[0][0] == "W" and p[1][0] == "W") == 4, "もどして白白は 4")
# 本文の値が、図に印刷されている値と一致すること
in_fig(r"\frac{2}{5}\times\frac{1}{4}=\frac{2}{20}", "図にも 2/20")
# ★ Why it works と図の数値が例題・演習と重ならないこと
not_in_body("\\dfrac{5}{14}", "例題3(b) の答えは本文に出さない")
not_in_body("\\dfrac{15}{28}", "例題3(c) の答えは本文に出さない")
not_in_body("\\dfrac{2}{15}", "演習3 の答えは本文に出さない")
not_in_body("\\dfrac{19}{33}", "演習6 の答えは本文に出さない")
not_in_body("\\dfrac{3}{7}", "例題4(c) の答えは本文に出さない")
_figlabels = sorted(re.findall(r'"\$(\d+)\$"', FIGCODE))
chk(_figlabels == ["100", "21", "30", "34", "36", "45", "55", "70", "9"],
    "図の二元表のラベル: %s" % _figlabels)
eq(21 + 9 + 34 + 36, 100, "図の表の合計は 100")
eq(F(21, 30), F(7, 10), "図の P(A|B) = 7/10")
eq(F(55, 100), F(11, 20), "図の P(A) = 11/20")
chk(F(7, 10) != F(11, 20), "図では条件付き確率が変わる")
eq(F(2, 20) + F(6, 20) + F(6, 20) + F(6, 20), 1, "図の樹形図の枝先の合計は 1")
eq(F(2, 5) * F(1, 4), F(2, 20), "図の 2/5 × 1/4")
eq(F(3, 5) * F(2, 4), F(6, 20), "図の 3/5 × 2/4")

# ══════════════════════════════════════════════════════════
# 4. 例題1 —— 二元表
# ══════════════════════════════════════════════════════════
T1 = {("Y12", "G"): 14, ("Y12", "N"): 26, ("Y13", "G"): 10, ("Y13", "N"): 30}
eq(sum(T1.values()), 80, "例題1 の合計")
eq(T1[("Y12", "G")] + T1[("Y12", "N")], 40, "Year 12 の行の合計")
eq(T1[("Y13", "G")] + T1[("Y13", "N")], 40, "Year 13 の行の合計")
eq(T1[("Y12", "G")] + T1[("Y13", "G")], 24, "めがねの列の合計")
eq(T1[("Y12", "N")] + T1[("Y13", "N")], 56, "めがねでない列の合計")
eq(F(24, 80), F(3, 10), "例題1(a)")
eq(F(14, 40), F(7, 20), "例題1(b)")
eq(F(14, 24), F(7, 12), "例題1(c)")
eq(F(14, 80), F(7, 40), "P(Y∩G)")
eq(F(40, 80) * F(24, 80), F(3, 20), "P(Y)P(G)")
eq(F(3, 20), F(6, 40), "3/20 = 6/40")
chk(F(7, 40) != F(6, 40), "例題1(d) 独立ではない")
chk(F(14, 40) > F(14, 24) or F(14, 40) < F(14, 24), "(b) と (c) はちがう")
chk(F(14, 40) < F(14, 24), "分母が小さいほうが大きい")
chk(F(7, 20) > F(3, 10), "Year 12 と分かると確率が上がる")
in_text("P(G) = \\frac{24}{80} = \\frac{3}{10}", "例題1(a)")
in_text("P(G \\mid Y) = \\frac{14}{40} = \\frac{7}{20}", "例題1(b)")
in_text("P(Y \\mid G) = \\frac{14}{24} = \\frac{7}{12}", "例題1(c)")

# ══════════════════════════════════════════════════════════
# 5. 例題2 —— 与えられた確率
# ══════════════════════════════════════════════════════════
_A, _B, _AB = sp.Rational("0.6"), sp.Rational("0.5"), sp.Rational("0.3")
eq(_AB / _B, sp.Rational("0.6"), "例題2(a)")
eq(_AB / _A, sp.Rational("0.5"), "例題2(b)")
eq(_A * _B, _AB, "例題2(c) 独立")
eq(_AB / _B, _A, "P(A|B) = P(A)")
eq(_AB / _A, _B, "P(B|A) = P(B)")
eq(_A + _B - _AB, sp.Rational("0.8"), "例題2 の和")
chk(_A + _B - _AB <= 1, "和が 1 以下（矛盾がない）")
in_text("P(A \\mid B) = \\frac{0.3}{0.5} = 0.6", "例題2(a)")
in_text("P(A)P(B) = 0.6 \\times 0.5 = 0.3 = P(A \\cap B)", "例題2(c)")

# ══════════════════════════════════════════════════════════
# 6. 例題3 —— もどさない
# ══════════════════════════════════════════════════════════
eq(F(5, 8) * F(4, 7), F(20, 56), "例題3(b)")
eq(F(20, 56), F(5, 14), "20/56 = 5/14")
eq(F(5, 8) * F(3, 7) + F(3, 8) * F(5, 7), F(30, 56), "例題3(c)")
eq(F(30, 56), F(15, 28), "30/56 = 15/28")
eq(F(3, 8) * F(2, 7), F(6, 56), "青青")
eq(F(20, 56) + F(15, 56) + F(15, 56) + F(6, 56), 1, "例題3 枝先の合計")
eq(8 * 7, 56, "8×7 = 56")
eq(5 * 4, 20, "5×4 = 20")
eq(F(5, 8) * F(5, 8), F(25, 64), "もどせば 25/64")
chk(F(5, 14) < F(25, 64), "もどさないほうが小さい")
eq(F(5, 14), F(160, 448), "5/14 = 160/448")
eq(F(25, 64), F(175, 448), "25/64 = 175/448")
in_text("P(RR) = \\frac{5}{8} \\times \\frac{4}{7} = \\frac{20}{56} "
        "= \\frac{5}{14}", "例題3(b)")

# ══════════════════════════════════════════════════════════
# 7. 例題4 —— 樹形図と、さかのぼる条件付き確率
# ══════════════════════════════════════════════════════════
_M, _N = sp.Rational("0.6"), sp.Rational("0.4")
_FM, _FN = sp.Rational("0.05"), sp.Rational("0.10")
eq(_M + _N, 1, "M と N で 1")
eq(_M * _FM, sp.Rational("0.03"), "例題4(a)")
eq(_N * _FN, sp.Rational("0.04"), "N の不良")
eq(_M * _FM + _N * _FN, sp.Rational("0.07"), "例題4(b)")
eq((_M * _FM) / (_M * _FM + _N * _FN), F(3, 7), "例題4(c)")
eq((_N * _FN) / (_M * _FM + _N * _FN), F(4, 7), "N の側")
eq(F(3, 7) + F(4, 7), 1, "3/7 + 4/7 = 1")
chk(F(3, 7) < sp.Rational("0.6"), "3/7 は 0.6 より小さい")
chk(_FN == 2 * _FM, "N の不良率は M の 2 倍")
# 個数でたしかめる
eq(10000 * _M, 6000, "M は 6000 個")
eq(6000 * _FM, 300, "M の不良は 300 個")
eq(4000 * _FN, 400, "N の不良は 400 個")
eq(F(300, 700), F(3, 7), "300/700 = 3/7")
in_text("P(M \\mid F) = \\frac{0.03}{0.07} = \\frac{3}{7}", "例題4(c)")

# ══════════════════════════════════════════════════════════
# 8. 演習の答え
# ══════════════════════════════════════════════════════════
# 演習1
eq(27 + 3, 30, "practised の行")
eq(10 + 10, 20, "did not practise の行")
eq(27 + 10, 37, "passed の列")
eq(3 + 10, 13, "failed の列")
eq(30 + 20, 50, "演習1 の合計")
eq(F(27, 30), F(9, 10), "演習1 の 1 つ目")
chk(sp.isprime(37), "37 は素数（約分できない）")
chk(F(27, 30) > F(27, 37), "分母が小さいほうが大きい")

# 演習2
_a2, _b2, _ab2 = sp.Rational("0.5"), sp.Rational("0.3"), sp.Rational("0.2")
eq(_ab2 / _b2, F(2, 3), "演習2 P(A|B)")
eq(_ab2 / _a2, F(2, 5), "演習2 P(B|A)")
eq(_a2 * _b2, sp.Rational("0.15"), "演習2 P(A)P(B)")
chk(sp.Rational("0.15") != _ab2, "演習2 は独立でない")
chk(F(2, 3) > _a2, "P(A|B) は P(A) より大きい")
chk(abs(float(F(2, 3)) - 0.667) < 5e-4, "2/3 は約 0.667")

# 演習3
eq(F(4, 10) * F(3, 9), F(12, 90), "演習3 両方緑")
eq(F(12, 90), F(2, 15), "12/90 = 2/15")
eq(F(6, 10) * F(5, 9), F(30, 90), "2 本とも赤")
eq(1 - F(30, 90), F(2, 3), "演習3 少なくとも 1 本")
eq(F(4, 10) * F(6, 9) + F(6, 10) * F(4, 9), F(48, 90), "ちょうど 1 本")
eq(F(12, 90) + F(48, 90), F(60, 90), "12/90 + 48/90")
eq(F(60, 90), F(2, 3), "60/90 = 2/3")
eq(10 * 9, 90, "10×9 = 90")
eq(4 * 3, 12, "4×3 = 12")
eq(F(4, 10) * F(4, 10), F(16, 100), "もどせば 16/100")
chk(F(2, 15) < F(16, 100), "もどさないほうが小さい")

# 演習4
eq(sp.Rational("0.4") * sp.Rational("0.25"), sp.Rational("0.1"), "演習4 P(A∩B)")
eq(sp.Rational("0.1") / sp.Rational("0.5"), sp.Rational("0.2"), "演習4 P(B|A)")
eq(sp.Rational("0.1") / sp.Rational("0.4"), sp.Rational("0.25"), "演習4 もどす")
chk(sp.Rational("0.1") < sp.Rational("0.5"), "P(A∩B) < P(A)")
chk(sp.Rational("0.1") < sp.Rational("0.4"), "P(A∩B) < P(B)")
chk(sp.Rational("0.5") * sp.Rational("0.4") != sp.Rational("0.1"),
    "演習4 は独立でない")

# 演習5
T5 = {("Y", "X"): 12, ("Y", "Xp"): 8, ("Yp", "X"): 18, ("Yp", "Xp"): 12}
eq(sum(T5.values()), 50, "演習5 の合計")
eq(12 + 8, 20, "Y の行")
eq(18 + 12, 30, "Y' の行")
eq(12 + 18, 30, "X の列")
eq(8 + 12, 20, "X' の列")
eq(F(12, 50), F(6, 25), "演習5 P(X∩Y)")
eq(F(30, 50) * F(20, 50), F(6, 25), "演習5 P(X)P(Y)")
eq(F(12, 20), F(3, 5), "P(X|Y)")
eq(F(30, 50), F(3, 5), "P(X)")
eq(F(18, 30), F(3, 5), "P(X|Y')")
chk(F(12, 50) == F(30, 50) * F(20, 50), "演習5 は独立")

# 演習6
eq(12 - 4, 8, "良品は 8 個")
eq(F(8, 12) * F(7, 11), F(56, 132), "演習6 2 個とも良品")
eq(F(56, 132), F(14, 33), "56/132 = 14/33")
eq(1 - F(14, 33), F(19, 33), "演習6 の答え")
eq(F(8, 12) * F(4, 11) + F(4, 12) * F(8, 11), F(64, 132), "ちょうど 1 個")
eq(F(4, 12) * F(3, 11), F(12, 132), "2 個とも不良")
eq(F(64, 132) + F(12, 132), F(76, 132), "64/132 + 12/132")
eq(F(76, 132), F(19, 33), "76/132 = 19/33")
eq(F(56, 132) + F(64, 132) + F(12, 132), 1, "演習6 枝先の合計")
eq(12 * 11, 132, "12×11 = 132")
eq(8 * 7, 56, "8×7 = 56")

# 演習7
eq(F(1, 6) * F(1, 6), F(1, 36), "1/6 × 1/6 = 1/36")
chk(prob(range(1, 7), lambda x: x == 1 and x == 2) == 0, "1 と 2 は同時に出ない")
chk(F(1, 36) != 0, "だから排反な 2 つは独立でない")
chk(prob(DICE, lambda s: s[0] == 1 and s[1] == 2) == F(1, 36), "独立な例")
chk(prob(DICE, lambda s: s[0] == 1) * prob(DICE, lambda s: s[1] == 2)
    == F(1, 36), "独立な例の積")
chk(sum(1 for s in DICE if s[0] == 1 and s[1] == 2) > 0, "独立な例は排反でない")

# 演習8
eq(sp.Rational("0.55") + sp.Rational("0.4") - sp.Rational("0.75"),
   sp.Rational("0.2"), "演習8 P(A∩B)")
eq(sp.Rational("0.2") / sp.Rational("0.4"), F(1, 2), "演習8 P(A|B)")
eq(sp.Rational("0.2") / sp.Rational("0.55"), F(4, 11), "演習8 P(B|A)")
eq(sp.Rational("0.55") + sp.Rational("0.4") - sp.Rational("0.2"),
   sp.Rational("0.75"), "演習8 もどす")
eq(sp.Rational("0.35") + sp.Rational("0.2") + sp.Rational("0.2")
   + sp.Rational("0.25"), 1, "演習8 の 4 つの合計")
eq(sp.Rational("0.55") * sp.Rational("0.4"), sp.Rational("0.22"), "P(A)P(B)")
chk(sp.Rational("0.22") != sp.Rational("0.2"), "演習8 は独立でない")

# 演習9
eq(F(1, 2) * F(3, 5), F(3, 10), "演習9 箱 1 で赤")
eq(F(1, 2) * F(1, 5), F(1, 10), "演習9 箱 2 で赤")
eq(F(3, 10) + F(1, 10), F(2, 5), "演習9 P(R)")
eq(F(3, 10) / F(2, 5), F(3, 4), "演習9 P(箱1|R)")
eq(F(1, 10) / F(2, 5), F(1, 4), "演習9 P(箱2|R)")
eq(F(3, 4) + F(1, 4), 1, "3/4 + 1/4 = 1")
eq(5 * F(3, 5), 3, "10 回のうち箱 1 の赤は 3 回")
eq(5 * F(1, 5), 1, "10 回のうち箱 2 の赤は 1 回")
eq(F(3, 4), F(3, 4), "3/4")
chk(F(3, 4) > F(1, 2), "赤が出たら箱 1 の可能性が高い")

# 演習10
eq(sp.Rational("0.3") * sp.Rational("0.5"), sp.Rational("0.15"), "演習10 P(A)P(B)")
chk(sp.Rational("0.15") != 0, "演習10 は独立でない")
eq(sp.Integer(0) / sp.Rational("0.5"), 0, "P(A|B) = 0")
chk(0 != sp.Rational("0.3"), "P(A|B) は P(A) とちがう")
chk(sp.Rational("0.3") != 0 and sp.Rational("0.5") != 0,
    "どちらの確率も 0 でない")
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

# --- B-1 「もどす場合は独立」の言いすぎ --------------------------------
in_text("**もどす場合、$1$ 回目の結果は $2$ 回目の枝の確率を変えません。**",
        "B-1 言いかえた")
in_text("その試行に関する**どの $2$ つの事象も**独立になるわけでは", "B-1 反例への注意")
not_in_text("**もどす場合は独立、もどさない場合は独立ではありません。**",
            "言いすぎは消した")
# 復元試行でも独立でない 2 事象がある（反例）
_p, _q = F(3, 5), F(2, 5)
_pA = _p                       # 1 回目が赤
_pB = _p * _p + _q * _q        # 2 回とも同じ色
_pAB = _p * _p                 # 1 回目が赤で、2 回とも同じ色
chk(_pAB != _pA * _pB, "復元でも独立でない 2 事象がある: %s != %s"
    % (_pAB, _pA * _pB))
# 中身が 1 種類なら、もどさなくても独立
chk(F(1, 1) * F(1, 1) == F(1, 1), "1 色だけなら、もどさなくても確率が変わらない")

# --- M-1 P(A|B) と P(B|A) の断定 --------------------------------------
in_text("**$P(A \\mid B)$ と $P(B \\mid A)$ は、ふつう別のものです。**", "M-1")
in_text("**$P(A) = P(B)$ なら一致します。**", "M07 一致する場合 1")
in_text("また $A$ と $B$ が排反で $P(A \\cap B) = 0$ なら、$P(A)$ と "
        "$P(B)$ がちがっていても両方 $0$ になって一致します。",
        "M07 排反なら両方 0")
in_text("$2$ つを比べるので $P(A) > 0$、$P(B) > 0$ とします",
        "M07 比べる前提")
not_in_text("$P(A) = P(B)$ のときだけ、たまたま一致します",
            "M07 「ときだけ」が消えている")
# 排反な例: P(A)=0.2, P(B)=0.3, P(A∩B)=0 なら両方の条件付き確率が 0
chk(F(0, 1) / F(3, 10) == 0 and F(0, 1) / F(2, 10) == 0,
    "M07 排反なら P(A|B) = P(B|A) = 0")
not_in_text("**$P(A \\mid B)$ と $P(B \\mid A)$ はちがいます。**", "断定は消した")
# P(A) = P(B) なら一致する
chk(F(12, 50) / F(30, 50) == F(12, 50) / F(30, 50), "分母が同じなら一致")

# --- M-2 例題1 の (b)(c) 検算 ------------------------------------------
in_text("P(G' \\mid Y) = \\dfrac{14}{40} + \\dfrac{26}{40} = 1$ ✓", "M-2 (b) の検算")
in_text("P(Y' \\mid G) = \\dfrac{14}{24} + \\dfrac{10}{24} = 1$ ✓", "M-2 (c) の検算")
not_in_text("$\\dfrac{14}{40} < \\dfrac{14}{24}$ ✓ 分母が小さいほうが",
            "循環した検算は消した")
eq(F(14, 40) + F(26, 40), 1, "Year 12 の行で 1")
eq(F(14, 24) + F(10, 24), 1, "めがねの列で 1")
chk(F(14, 24) + F(26, 24) > 1, "取りちがえると 1 をこえる")

# --- M-3 演習1 の検算 --------------------------------------------------
in_text("practised の行なら $\\dfrac{27}{30} + \\dfrac{3}{30} = 1$ ✓", "M-3")
not_in_text("$\\dfrac{27}{30} > \\dfrac{27}{37}$ です ✓ 分子が", "循環した検算は消した")
eq(F(27, 30) + F(3, 30), 1, "practised の行で 1")
eq(F(27, 37) + F(10, 37), 1, "passed の列で 1")
chk(F(27, 37) + F(3, 37) != 1, "取りちがえると 1 にならない")

# --- M-4 例題4(b) の検算 ----------------------------------------------
in_text("**$P(F)$ は $2$ つの不良率の間に入るはずです。**", "M-4")
not_in_text("$0.07 \\le 1$ ✓ 不良品はまれ", "何も検出しない検算は消した")
chk(sp.Rational("0.05") <= sp.Rational("0.07") <= sp.Rational("0.10"),
    "0.07 は 0.05 と 0.10 の間")
chk(sp.Rational("0.15") > sp.Rational("0.10"), "足すと上をこえる")
# 加重平均は、必ず 2 つの値の間に入る
for _w in (F(0, 10), F(3, 10), F(6, 10), F(1, 1)):
    _m = _w * sp.Rational("0.05") + (1 - _w) * sp.Rational("0.10")
    chk(sp.Rational("0.05") <= _m <= sp.Rational("0.10"),
        "加重平均は 0.05..0.10 の間: %s" % _m)

# --- M-5 演習4 の検算 --------------------------------------------------
in_text("**$P(A \\cap B)$ を $2$ とおりに書いて比べます。**", "M-5")
not_in_text("**もどして確かめます。** $\\dfrac{0.1}{0.4} = 0.25$ ✓",
            "逆演算だけの検算は消した")
eq(sp.Rational("0.4") * sp.Rational("0.25"), sp.Rational("0.1"), "P(B)P(A|B)")
eq(sp.Rational("0.5") * sp.Rational("0.2"), sp.Rational("0.1"), "P(A)P(B|A)")
# かける相手を取りちがえると、2 つが合わない
chk(sp.Rational("0.5") * sp.Rational("0.25") != sp.Rational("0.1"),
    "P(A) にかけると 0.125 で合わない")
eq(sp.Rational("0.5") * sp.Rational("0.25"), sp.Rational("0.125"), "0.125")

# --- M-6 演習8 を Venn 図の問いにした ----------------------------------
in_text("By drawing a Venn diagram and writing the probability in each of the "
        "four regions", "M-6 演習8")
in_text("*Venn diagram: $A$ only $0.35$, both $0.2$, $B$ only $0.2$, "
        "neither $0.25$*", "M-6 演習8 の解答例")
eq(sp.Rational("0.55") - sp.Rational("0.2"), sp.Rational("0.35"), "A だけ")
eq(sp.Rational("0.4") - sp.Rational("0.2"), sp.Rational("0.2"), "B だけ")
eq(1 - sp.Rational("0.75"), sp.Rational("0.25"), "外")

# --- M-7 4.11 との切り分け --------------------------------------------
in_text("[SL 4.11](aasl-4-11.qmd) で扱います。", "M-7 4.11 へのリンク")
in_text("$P(A \\mid B) = P(A) = P(A \\mid B')$ という書き方を使った判定",
        "M-7 4.11 の内容")
in_text("（この見方を式にしたものが [SL 4.11](aasl-4-11.qmd) です）", "M-7 演習5")
chk(TEXT.count("aasl-4-11.qmd") >= 2, "4.11 へのリンクが 2 か所以上")

# --- M-8 演習7 を「例を作る」問いにした --------------------------------
in_text("[7]{.ex-no} [Give an example of two events that are mutually "
        "exclusive but not independent", "M-8 演習7")
in_text("*mutually exclusive but not independent: one die, $A$: the number is "
        "$1$, $B$: the number is $2$*", "M-8 演習7 の解答例 1")
in_text("*independent but not mutually exclusive: two dice, $C$: the first "
        "shows $1$, $D$: the second shows $2$*", "M-8 演習7 の解答例 2")
not_in_text("[7]{.ex-no} [Explain the difference between two events being "
            "mutually exclusive", "思い出すだけの問いは消した")
# 2 つの例が、実際に条件を満たすこと
chk(prob(range(1, 7), lambda x: x == 1) == F(1, 6), "P(1 が出る) = 1/6")
chk(len([x for x in range(1, 7) if x == 1 and x == 2]) == 0, "1 と 2 は同時に出ない")
chk(F(1, 6) * F(1, 6) == F(1, 36) and F(1, 36) != 0, "積は 0 でない → 独立でない")
chk(prob(DICE, lambda s: s[0] == 1 and s[1] == 2) == F(1, 36), "2 個なら 1/36")
chk(prob(DICE, lambda s: s[0] == 1) * prob(DICE, lambda s: s[1] == 2)
    == F(1, 36), "積も 1/36 → 独立")
chk(sum(1 for s in DICE if s[0] == 1 and s[1] == 2) == 1, "同時に起こる → 排反でない")

# --- m-1 例題2(c) の検算 -----------------------------------------------
in_text("**検算（(c) について、条件付き確率で）。**", "m-1")
in_text("**検算（与えられた $3$ つの値が矛盾していないか）。**", "m-1 見出しを直した")
not_in_text("**検算（(c) について、和で）。**", "見出しは直した")

# --- m-2 「1 以上になります」 ------------------------------------------
in_text("分子と分母を逆にしていたら、$1$ 以上になります。", "m-2")
not_in_text("分子と分母を逆にしていたら、$1$ をこえます。", "言いすぎは消した")
# B ⊆ A なら、逆にするとちょうど 1
chk(F(3, 10) / F(3, 10) == 1, "P(A∩B) = P(B) なら逆にしてちょうど 1")

# --- m-3 演習10 の model answer ----------------------------------------
in_text("changes the probability of $A$ from $0.3$ to $0$.*", "m-3")
not_in_text("changes the probability of $A$ as much as it can", "言いすぎは消した")

# --- m-4 例題4 の model answer -----------------------------------------
in_text("although it makes fewer items, its faulty rate is twice as high",
        "m-4")
not_in_text("produces a larger share of those because its faulty rate is twice "
            "as high", "不完全な理由は消した")
chk(sp.Rational("0.4") < sp.Rational("0.6"), "N のほうが生産量は少ない")
chk(sp.Rational("0.04") > sp.Rational("0.03"), "それでも不良品は N のほうが多い")

# --- m-5 同様に確からしい条件 ------------------------------------------
in_text("**結果がどれも同様に確からしいとき**、次のように数えられます。", "m-5")

# --- m-6 表の P(B) ≠ 0 -------------------------------------------------
in_text("$A$ は起こらない（$P(B) \\ne 0$ なら $P(A \\mid B) = 0$）", "m-6")

# --- m-8 Common errors の見出し ----------------------------------------
in_text("## 樹形図で、$1$ つの分かれ目から出る枝の合計が $1$ になっていない",
        "m-8")
not_in_text("## 樹形図の $2$ 段目の枝を、$1$ 本ずつ足して $1$ にしない",
            "読めない見出しは消した")

# --- m-9 図の説明 ------------------------------------------------------
in_fig("演習9 の箱 1 は 3 と 2 で構成が同じだが", "m-9 図の説明")


# ══════════════════════════════════════════════════════════
# E09  もどさない場合の樹形図を、解答に入れる
# ══════════════════════════════════════════════════════════
in_text("(img/aasl-4-6b-tree.svg){#fig-aasl46b-tree width=100%}",
        "E09 例題 の樹形図")
_e09q = [sp.Rational(5, 8) * sp.Rational(4, 7),
         sp.Rational(5, 8) * sp.Rational(3, 7),
         sp.Rational(3, 8) * sp.Rational(5, 7),
         sp.Rational(3, 8) * sp.Rational(2, 7)]
chk(sum(_e09q) == 1, "E09 枝先の和は 1")
chk(_e09q[0] == sp.Rational(20, 56), "E09 RR は 20/56")
chk(_e09q[3] == sp.Rational(6, 56), "E09 BB は 6/56")
chk(_e09q[0] < sp.Rational(5, 8) ** 2, "E09 もどさないほうが小さい")

print()
print("OK", OK, "/ NG", NG)
