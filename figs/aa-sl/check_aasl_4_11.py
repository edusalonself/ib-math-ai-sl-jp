# -*- coding: utf-8 -*-
"""AA SL 4.11 のページを検算する。

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
QMD = os.path.join(ROOT, "aa-sl", "04-statistics-and-probability", "aasl-4-11.qmd")
FIGP = os.path.join(HERE, "make_aasl_4_11.py")

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


R = sp.Rational

# ══════════════════════════════════════════════════════════
# 1. ページの骨組み
# ══════════════════════════════════════════════════════════
chk(TEXT.startswith("---\nsidebar: aa-sl\n---\n"), "front matter")
in_text("# SL 4.11 — Formal conditional probability and independence"
        "（条件付き確率の定義と独立性の判定） {#sec-aasl-4-11}", "見出し")

for _h in ("## What you should be able to do", "## The idea {#idea}",
           "## Why it works", "## Worked examples", "## Common errors",
           "## Exercises"):
    in_text(_h, "節 " + _h)
not_in_text("## Using your GDC", "4.11 に GDC の節は置かない")

_secs = re.findall(r"^### (\d)\. .*\{#([a-z-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 8)],
    "### の番号 1..7: %s" % [s[0] for s in _secs])
chk([s[1] for s in _secs] == ["formal", "multiply", "three", "test", "solve",
                              "total", "choose"],
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

in_text("(img/aasl-4-11-idea.svg){#fig-aasl411-idea width=100%}", "図の埋め込み")
in_text("@fig-aasl411-idea (a)", "図 (a) の参照")
in_text("@fig-aasl411-idea (b)", "図 (b) の参照")

chk(not re.search(r"^> ", TEXT, re.M), "引用ブロックは使わない")
for _w in ("そのとおり", "もちろん", "簡単です", "自明", "当たり前", "明らか", "当然"):
    not_in_text(_w, "禁止語 " + _w)
for _w in ("得点になりません", "点になりません", "減点されます"):
    not_in_text(_w, "採点の断定 " + _w)

# ══════════════════════════════════════════════════════════
# 2. 式と公式集
# ══════════════════════════════════════════════════════════
in_text("P(A \\mid B) = \\frac{P(A \\cap B)}{P(B)}, \\qquad P(B) \\ne 0\n"
        "$$ {#eq-aasl411-cond}", "条件付き確率の式")
in_text("P(A \\cap B) = P(B)\\,P(A \\mid B)\n$$ {#eq-aasl411-mult}", "かけ算の形")
in_text("P(A \\cap B) = P(A)P(B)\n$$ {#eq-aasl411-indep}", "独立の式")
in_text("$$ {#eq-aasl411-three}", "3 つの言い方の式")
in_text("$$ {#eq-aasl411-total}", "P(A) の組み立て")
in_text("公式集の **4.6** の欄に *Conditional probability* として載っています",
        "公式集 4.6 conditional")
in_text("公式集の **4.6** の欄に *Independent events* として載っています",
        "公式集 4.6 independent")
in_text("シラバスの **4.11** に出てきます。公式集にはありません。",
        "3 つの言い方は公式集にない")
in_text("{#tbl-aasl411-formulae}", "式の使い分けの表")
in_text("{#tbl-aasl411-choose}", "式の選び方の表")
in_text("[SL 4.6b](aasl-4-6b.qmd#restrict)", "4.6b への参照（狭まる）")
in_text("[SL 4.6b](aasl-4-6b.qmd#formula)", "4.6b への参照（式）")
in_text("[SL 4.6b](aasl-4-6b.qmd#multiply)", "4.6b への参照（かけ算）")
in_text("[SL 4.6b](aasl-4-6b.qmd#compare)", "4.6b への参照（排反と独立）")
in_text("[SL 4.6a の加法定理](aasl-4-6a.qmd#addition)", "4.6a への参照")

# 3 つの言い方が同値であること（記号のまま）
_pa, _pb = sp.symbols("p_A p_B", positive=True)
eq(sp.simplify((_pa * _pb) / _pb), _pa, "P(A∩B)=P(A)P(B) → P(A|B)=P(A)")
eq(sp.simplify((_pa - _pa * _pb) / (1 - _pb)), _pa,
   "→ P(A|B')=P(A)")
eq(sp.expand(_pa - _pa * _pb), sp.expand(_pa * (1 - _pb)), "因数分解")
# P(B)=0 でもかけ算の形は成り立つ
eq(sp.Integer(0), _pa * 0, "P(B)=0 のときもかけ算の形は成り立つ")
# 重みつき平均は 2 つの間に入る
for _w in (R(0), R(1, 4), R(1, 2), R(3, 4), R(1)):
    _m = _w * R(1, 5) + (1 - _w) * R(1, 2)
    chk(R(1, 5) <= _m <= R(1, 2), "重みつき平均は 1/5..1/2 の間: %s" % _m)

# ══════════════════════════════════════════════════════════
# 3. 図
# ══════════════════════════════════════════════════════════
in_fig('r"$P(A \\cap B) = P(A)\\,P(B)$"', "図 (a) のかけ算の形")
in_fig('r"$P(A \\mid B) = P(A)$"', "図 (a) の条件付きの形")
in_fig('r"$P(A \\mid B\') = P(A)$"', "図 (a) の余事象の形")
in_fig('["$B$", "$18$", "$12$", "$30$"]', "図 (b) の表の 1 行目")
eq(18 + 12 + 42 + 28, 100, "図の表の合計は 100")
eq(R(18, 30), R(3, 5), "図 18/30 = 0.6")
eq(R(42, 70), R(3, 5), "図 42/70 = 0.6")
eq(R(60, 100), R(3, 5), "図 60/100 = 0.6")
eq(R(18, 100), R(60, 100) * R(30, 100), "図の表は独立")
# 図の数値が例題・演習と重ならないこと
chk(100 != 200, "図の合計 100 は演習4 の 200 とちがう")
for _v in ("0.29", "15/29", "$0.24$", "3/7", "$0.45$", "0.28"):
    chk(_v not in FIGCODE, "図に答え %s は出さない" % _v)

# ★ 例題・演習の答えを本文に出していないこと
for _v in ("\\dfrac{15}{29}", "\\dfrac{2}{3}", "\\dfrac{4}{9}", "\\dfrac{3}{7}",
           "0.29", "0.24", "0.28"):
    not_in_body(_v, "答え %s は本文に出さない" % _v)

# ══════════════════════════════════════════════════════════
# 4. 例題1  P(A)=0.4, P(B)=0.5, P(A∩B)=0.2
# ══════════════════════════════════════════════════════════
_A, _B, _AB = R("0.4"), R("0.5"), R("0.2")
eq(_AB / _B, R("0.4"), "例題1(a) P(A|B)")
eq(_A - _AB, R("0.2"), "例題1(b) P(A∩B')")
eq(1 - _B, R("0.5"), "例題1(b) P(B')")
eq((_A - _AB) / (1 - _B), R("0.4"), "例題1(b) P(A|B')")
eq(_A * _B, _AB, "例題1(c) 独立")
eq(_AB / _B, _A, "P(A|B) = P(A)")
eq(_AB + (_A - _AB) + (_B - _AB) + (1 - _A - _B + _AB), 1, "4 つの部分の合計")
eq(_B * (_AB / _B) + (1 - _B) * ((_A - _AB) / (1 - _B)), _A, "重みつき平均")
chk(0 <= _AB / _B <= 1, "0..1 の間")
in_text("P(A \\mid B) = \\frac{0.2}{0.5} = 0.4", "例題1(a)")
in_text("P(A)P(B) = 0.4 \\times 0.5 = 0.2 = P(A \\cap B)", "例題1(c)")

# ══════════════════════════════════════════════════════════
# 5. 例題2  P(A)=0.6, P(B)=0.4, P(A∪B)=0.8
# ══════════════════════════════════════════════════════════
_A2, _B2, _U2 = R("0.6"), R("0.4"), R("0.8")
_AB2 = _A2 + _B2 - _U2
eq(_AB2, R("0.2"), "例題2(a)")
eq(_AB2 / _B2, R("0.5"), "例題2(b) P(A|B)")
eq(_A2 - _AB2, R("0.4"), "P(A∩B')")
eq(1 - _B2, R("0.6"), "P(B')")
eq((_A2 - _AB2) / (1 - _B2), R(2, 3), "例題2(b) P(A|B')")
eq(_A2 * _B2, R("0.24"), "例題2(c) P(A)P(B)")
chk(R("0.24") != _AB2, "例題2 は独立でない")
eq(_A2 + _B2 - _AB2, _U2, "もどすと 0.8")
eq(_B2 * R("0.5") + (1 - _B2) * R(2, 3), _A2, "重みつき平均は P(A)")
chk(R("0.5") <= _A2 <= R(2, 3), "P(A) は 2 つの条件付き確率の間")
eq(_AB2 + (_A2 - _AB2) + (_B2 - _AB2) + (1 - _U2), 1, "4 つの部分の合計")

# ══════════════════════════════════════════════════════════
# 6. 例題3  P(B)=0.3, P(A|B)=0.5, P(A|B')=0.2
# ══════════════════════════════════════════════════════════
_B3, _AgB, _AgBp = R("0.3"), R("0.5"), R("0.2")
eq(_B3 * _AgB, R("0.15"), "例題3(a)")
eq((1 - _B3) * _AgBp, R("0.14"), "P(A∩B')")
eq(_B3 * _AgB + (1 - _B3) * _AgBp, R("0.29"), "例題3(b) P(A)")
eq((_B3 * _AgB) / R("0.29"), R(15, 29), "例題3(c) P(B|A)")
eq(R("0.14") / R("0.29"), R(14, 29), "P(B'|A)")
eq(R(15, 29) + R(14, 29), 1, "足すと 1")
chk(_AgBp <= R("0.29") <= _AgB, "P(A) は 0.2 と 0.5 の間")
chk(abs(float(R("0.29") - _AgBp)) < abs(float(_AgB - R("0.29"))),
    "重みが大きい 0.2 に近い")
chk(R(15, 29) > _B3, "P(B|A) > P(B)")
chk(abs(float(R(15, 29)) - 0.517) < 5e-4, "15/29 ≈ 0.517")

# ══════════════════════════════════════════════════════════
# 7. 例題4  独立、P(A)=0.5, P(A∩B)=0.2
# ══════════════════════════════════════════════════════════
_k = sp.Symbol("k")
chk(sp.solve(sp.Eq(R("0.5") * _k, R("0.2")), _k) == [R("0.4")],
    "例題4(a) P(B) = 0.4")
eq(R("0.5") + R("0.4") - R("0.2"), R("0.7"), "例題4(b)")
eq((R("0.5") - R("0.2")) / (1 - R("0.4")), R("0.5"), "例題4(c) 直接計算でも 0.5")
eq(R("0.5") * R("0.4"), R("0.2"), "もどすと 0.2")
chk(R("0.2") != 0, "排反ではない")
chk(R("0.5") != 0 and R("0.4") != 0, "どちらの確率も 0 でない")
eq(R("0.2") + R("0.3") + R("0.2") + R("0.3"), 1, "4 つの部分の合計")

# ══════════════════════════════════════════════════════════
# 8. 演習の答え
# ══════════════════════════════════════════════════════════
eq(R("0.7") * R("0.4"), R("0.28"), "演習1 独立")
eq(R("0.28") / R("0.4"), R("0.7"), "演習1 P(A|B)")
eq((R("0.7") - R("0.28")) / (1 - R("0.4")), R("0.7"), "演習1 P(A|B')")
eq(R("0.28") + R("0.42") + R("0.12") + R("0.18"), 1, "演習1 の 4 つの合計")

eq(R("0.2") / R("0.6"), R(1, 3), "演習2 P(A|B)")
eq(R("0.2") / R("0.45"), R(4, 9), "演習2 P(B|A)")
eq(R("0.45") * R("0.6"), R("0.27"), "演習2 P(A)P(B)")
chk(R("0.27") != R("0.2"), "演習2 は独立でない")
eq(R("0.6") * R(1, 3), R("0.2"), "かけ算の形でもどる")
chk(abs(float(R(1, 3)) - 0.333) < 5e-4, "1/3 ≈ 0.333")
chk(abs(float(R(4, 9)) - 0.444) < 5e-4, "4/9 ≈ 0.444")

eq(R("0.25") * R("0.8"), R("0.2"), "演習3")
eq(R("0.2") / R("0.25"), R("0.8"), "もどすと 0.8")
chk(R("0.2") < R("0.25"), "共通部分は P(B) より小さい")
eq(R("0.2") + (1 - R("0.25")) * 1, R("0.95"), "P(A|B')=1 なら P(A)=0.95")
eq(R("0.2") + (1 - R("0.25")) * 0, R("0.2"), "P(A|B')=0 なら P(A)=0.2")
eq(1 - R("0.25"), R("0.75"), "P(B') = 0.75")

_T4 = {("Y", "X"): 30, ("Y", "Xp"): 70, ("Yp", "X"): 50, ("Yp", "Xp"): 50}
eq(sum(_T4.values()), 200, "演習4 の合計")
eq(30 + 70, 100, "Y の行")
eq(50 + 50, 100, "Y' の行")
eq(30 + 50, 80, "X の列")
eq(70 + 50, 120, "X' の列")
eq(R(30, 200), R("0.15"), "演習4 P(X∩Y)")
eq(R(80, 200) * R(100, 200), R("0.2"), "演習4 P(X)P(Y)")
chk(R(30, 200) != R(80, 200) * R(100, 200), "演習4 は独立でない")
eq(R(30, 100), R("0.3"), "演習4 P(X|Y)")
eq(R(50, 100), R("0.5"), "演習4 P(X|Y')")
eq(R(80, 200), R("0.4"), "演習4 P(X)")
chk(R("0.3") < R("0.4") < R("0.5"), "演習4 P(X) は 2 つの行の割合の間")
eq(R(100, 200) * R(30, 100) + R(100, 200) * R(50, 100), R(80, 200),
   "演習4 重みつき平均は P(X)")

eq(R("0.36") * R("0.5"), R("0.18"), "演習5")
eq(R("0.5") * R("0.36"), R("0.18"), "独立なので同じ")
eq(R("0.18") / R("0.36"), R("0.5"), "もどすと 0.5")
chk(R("0.18") < R("0.36") and R("0.18") < R("0.5"), "共通部分は小さい")

eq(R("0.4") * R("0.5"), R("0.2"), "演習6 P(A∩B)")
eq(R("0.4") + R("0.5") - R("0.2"), R("0.7"), "演習6 P(A∪B)")
eq(R("0.6") * R("0.5"), R("0.3"), "演習6 余事象の積")
eq(1 - R("0.3"), R("0.7"), "余事象からも 0.7")
eq(R("0.2") + R("0.2") + R("0.3") + R("0.3"), 1, "演習6 の 4 つの合計")

# 演習7: P(A)=0.5, P(B)=0.2 のとき P(A|B) は 0 から 1 まで何でもありうる
eq(R("0.2") * 0 / R("0.2"), 0, "演習7 P(A∩B)=0 なら P(A|B)=0")
eq(R("0.2") / R("0.2"), 1, "演習7 P(A∩B)=0.2 なら P(A|B)=1")
chk(R("0.2") <= R("0.5"), "演習7 P(A∩B) の上限は min(P(A),P(B)) = 0.2")
eq(R("0.5") * R("0.2"), R("0.1"), "演習7 独立なら P(A∩B)=0.1")
eq(R("0.1") / R("0.2"), R("0.5"), "演習7 そのとき P(A|B)=P(A)=0.5")

eq(R("0.6") * R("0.25"), R("0.15"), "演習8 P(A∩B)")
eq(R("0.4") * R("0.5"), R("0.2"), "演習8 P(A∩B')")
eq(R("0.15") + R("0.2"), R("0.35"), "演習8 P(A)")
eq(R("0.15") / R("0.35"), R(3, 7), "演習8 P(B|A)")
eq(R("0.2") / R("0.35"), R(4, 7), "演習8 P(B'|A)")
eq(R(3, 7) + R(4, 7), 1, "足すと 1")
chk(R("0.25") <= R("0.35") <= R("0.5"), "P(A) は 0.25 と 0.5 の間")
chk(R(3, 7) < R("0.6"), "P(B|A) < P(B)")
chk(abs(float(R(3, 7)) - 0.429) < 5e-4, "3/7 ≈ 0.429")

# 演習9: 独立、P(A)=0.3、P(A∪B)=0.65 から P(B) を出す
chk(sp.solve(sp.Eq(R("0.3") + (1 - R("0.3")) * _k, R("0.65")), _k)
    == [R("0.5")], "演習9 P(B) = 0.5")
eq(R("0.3") * R("0.5"), R("0.15"), "演習9 P(A∩B)")
eq(R("0.3") + R("0.5") - R("0.15"), R("0.65"), "演習9 もどすと 0.65")
eq(R("0.15") / R("0.5"), R("0.3"), "演習9 P(A|B) = P(A)")
chk(R("0.65") > R("0.5") and R("0.65") <= 1, "演習9 範囲の検算")

eq(R("0.6") * R("0.5"), R("0.3"), "演習10 の例 P(A∩B)")
chk(R("0.3") != 0, "演習10 排反ではない")
eq(sp.Integer(0) / R("0.5"), 0, "排反なら P(A|B)=0")
chk(0 != R("0.6"), "0.6 ではない")
# ══════════════════════════════════════════════════════════
# 10. ページに書いてある計算を、機械的に全部たしかめる
# ══════════════════════════════════════════════════════════
_ATOM = r"(?:\\[dt]?frac\{-?\d+\}\{-?\d+\}|-?\d+(?:\.\d+)?)"
_TERM = r"%s(?:\s*\\times\s*%s)*" % (_ATOM, _ATOM)
_EXPR = r"%s(?:\s*[+-]\s*%s)*" % (_TERM, _TERM)
_STMT = re.compile(r"(?<![\d\w}])(%s(?:\s*=\s*%s)+)(?!\s*(?:[+-]|\\times|[\d.(]))"
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
    # 長い式の途中を切り取っていないかを見る（直前が演算子や括弧なら飛ばす）
    _before = TEXT[:_m.start()].rstrip()
    if _before and _before[-1] in "+-=)*/(":
        continue
    if _before.endswith("\\times"):
        continue
    _vals = [_value(x) for x in _m.group(1).split("=")]
    _nstmt += 1
    chk(len(set(_vals)) == 1,
        "式が合わない: %s  →  %s" % (_m.group(1)[:80], _vals))
chk(_nstmt >= 8, "ページの計算を %d 本たしかめた" % _nstmt)

# ══════════════════════════════════════════════════════════
# 見直し（2026-09）で直したところ。もどってしまわないように。
# ══════════════════════════════════════════════════════════

# --- B2: 3 つの言いかえは 0 < P(B) < 1 のときだけ同値 -----------
chk("$0 < P(B) < 1$ のとき、次の $3$ つのどれで書いても同じです" in TEXT,
    "第3節: 同値の条件 0 < P(B) < 1 を書いている")
chk("**$0 < P(B) < 1$ なら、$1$ つ示せば十分です。**" in TEXT,
    "第3節: 「1 つ示せば十分」に条件がついている")
chk("だから、独立の定義に選ぶのはかけ算の形です。" in TEXT,
    "第3節: かけ算の形を定義に選ぶ理由を書いている")
chk("$P(B) = 1$ だと $P(A \\mid B')$ が定義されません" in TEXT,
    "第3節: P(B)=1 のとき P(A|B') が定義されないと書いている")
chk("$3$ つは同じことなので" in TEXT, "第3節: 言いかえの説明が残っている")
# 「割り算がないから P(B)=0 でも使える」だけで終わっていないこと
chk("$P(B) = 0$ でも $P(B) = 1$ でも意味を持ちます" in TEXT,
    "第3節: かけ算の形は両端でも意味を持つ")

# --- B2 図: 同値の条件と、かけ算の形の但し書き ------------------
chk("when $0 < P(B) < 1$, each one implies the others" in FIGCODE,
    "図(a): 同値に条件がついている")
chk("only the first still makes sense when $P(B) = 0$ or " in FIGCODE,
    "図(a): かけ算の形だけが両端でも意味を持つ")
chk("the first needs no division, so it works even when" not in FIGCODE,
    "図(a): 古い（条件なしの）文が消えている")

# --- M2: Why it works に逆向き（B' から積の形）が入っている ------
chk("&= P(A)\\bigl(1 - P(B)\\bigr) = P(A)P(B')" in TEXT,
    "Why it works: P(A∩B') の式が 2 行に分かれている")
chk("割るときに $P(B') \\ne 0$ が要ります" in TEXT,
    "Why it works: P(B') != 0 の条件を書いている")
chk("$B$ について独立なら、$B'$ についても独立" in TEXT,
    "Why it works: B' 側の独立を述べている")
chk("$3$ つのどれか $1$ つから残りの $2$ つが出ます。" in TEXT,
    "Why it works: 3 つが循環することを述べている")
chk("$P(B)$ が $0$ か $1$ だと条件付き確率の側が定義されない" in TEXT,
    "Why it works: 両端で言いかえができないと書いている")

# --- M3: 全確率の式は公式集にない ------------------------------
chk("**@eq-aasl411-total は公式集にありません。**" in TEXT,
    "全確率の式が公式集にないと明記している")
chk(TEXT.count("callout-important") == 2,
    "callout-important は 2 つ（どちらも 4.6 の欄）")
chk(TEXT.count("公式集の **4.6** の欄") == 2,
    "公式集の参照はどちらも 4.6 の欄")

# --- M4: 演習 9 は和の公式と独立を組み合わせる ------------------
chk("$P(A \\cup B) = 0.65$. Find $P(B)$." in TEXT,
    "演習9: P(A∪B) から P(B) を求める問題になっている")
chk("$0.8 \\times P(B) = 0.24$" not in TEXT, "演習9: 古い問題が消えている")

# --- M5: 演習 4 の表は独立でない ------------------------------
chk("| $Y$ | $30$ | $70$ | $100$ |" in TEXT,
    "演習4: 表の Y の行が 30 / 70 / 100")
chk("| $Y'$ | $50$ | $50$ | $100$ |" in TEXT,
    "演習4: 表の Y' の行が 50 / 50 / 100")
chk("| total | $80$ | $120$ | $200$ |" in TEXT,
    "演習4: 表の合計が 80 / 120 / 200")
chk("These are not equal, so $X$ and $Y$ are not independent." in TEXT,
    "演習4: 独立でないと結論している")
chk("$P(X \\mid Y) = \\dfrac{30}{100} = 0.3$" in TEXT,
    "演習4: 行の割合による検算がある")

# --- B1: 演習 7 は答えが本文にない問題 -------------------------
chk("A student says that $P(A \\mid B)$ must be smaller than $P(A)$" in TEXT,
    "演習7: 生徒の主張を評価する問題になっている")
chk("Comment on the student's reasoning." in TEXT,
    "演習7: Comment の指示がある")

# --- 重みつき平均の言いかたに条件がついている -------------------
for _sent in ["$0 < P(B) < 1$ なので、重みつき平均は必ず $2$ つの間に入ります。",
              "$0 < P(B) < 1$ なので、重みつき平均は必ず間に入ります。"]:
    chk(_sent in TEXT, "重みつき平均の検算に条件がついている: %s" % _sent[:24])

# --- 図の表は両方の行に色がついている（B と B' を並べて見る）----
chk('facecolor=SHADE if _i == 0 else "white"' not in FIGCODE,
    "図(b): B と B' の両方の行に同じ色がついている")

# --- 答えのもれ: 演習の答えが The idea / Why it works にない ----
_head = TEXT[:TEXT.index("## Worked examples")]
for _leak in ["$0.5$ です", "何でもありえます", "$0$ から $1$ まで"]:
    chk(_leak not in _head, "前半に演習の答えがもれていない: %s" % _leak)

print()
print("OK", OK, "/ NG", NG)
