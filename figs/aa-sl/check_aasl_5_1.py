# -*- coding: utf-8 -*-
"""AA SL 5.1 のページを検算する。

    python3 figs/aa-sl/check_aasl_5_1.py
"""
import os
import re

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
QMD = os.path.join(ROOT, "aa-sl", "05-calculus", "aasl-5-1.qmd")
FIGP = os.path.join(HERE, "make_aasl_5_1.py")

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


def close(a, b, tol, msg=""):
    chk(abs(float(a) - float(b)) < tol, "%s :: %s vs %s" % (msg, a, b))


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
X, H = sp.symbols("x h")


def chord(f, a, h):
    """f の a から a+h までの割線の傾き（正確に）。"""
    a = sp.nsimplify(a)
    h = sp.nsimplify(h)
    return sp.nsimplify(sp.simplify((f(a + h) - f(a)) / h), rational=True)


def d3(v):
    """小数第 3 位まで（四捨五入）。"""
    return sp.Rational(round(float(v) * 1000), 1000)


# ══════════════════════════════════════════════════════════
# 1. ページの骨組み
# ══════════════════════════════════════════════════════════
chk(TEXT.startswith("---\nsidebar: aa-sl\n---\n"), "front matter")
in_text("# SL 5.1 — Limits and the derivative（極限と導関数の考え方） "
        "{#sec-aasl-5-1}", "見出し")

for _h in ("## What you should be able to do", "## The idea",
           "## Why it works", "## Worked examples", "## Common errors",
           "## Exercises"):
    in_text(_h, "節 " + _h)
not_in_text("## Using your GDC", "Topic 5 に GDC の節は置かない")

_secs = re.findall(r"^### (\d)\. .*\{#([a-z0-9-]+)\}$", TEXT, re.M)
chk([s[0] for s in _secs] == [str(i) for i in range(1, 8)],
    "### の番号 1..7: %s" % [s[0] for s in _secs])
chk([s[1] for s in _secs] == ["average", "limit", "estimate", "tangent",
                              "notation", "gradfn", "rate"],
    "アンカー: %s" % [s[1] for s in _secs])

chk(len(re.findall(r"^\[\d+\]\{\.ex-no\}", TEXT, re.M)) == 10, "演習 10 問")
chk(TEXT.count("::: {#exm-") == 4, "例題 4 つ")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep 9 個")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳 14")
chk(TEXT.count("</details>") == 14, "details 閉じ 14")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例 14")
chk(len(re.findall(r"^---$", TEXT, re.M)) == 6, "行頭 --- は 6 本")
chk(TEXT.count("{.callout-warning}") == 7, "callout-warning 7（誤り 6 + Paper 1）")
chk("## 電卓が使えるときは、こう確かめます" in TEXT,
    "電卓の話は、たたむ callout に分ける（Topic 5 の他ページと同じ形）")
chk("**電卓は、考えを確かめるために使ってください。**" not in TEXT,
    "たためない callout に入っていた電卓の段落が消えている")
chk(TEXT.count("{.callout-important}") == 0,
    "callout-important 0（5.1 に公式集の欄はない）")
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
chk(len(_qs) == 7, "Explain 系の問いは 7: %d" % len(_qs))

for _i, _m in enumerate(re.findall(r"\{\.model-answer\}(.*?):::", TEXT, re.S), 1):
    _b = _m.replace("**試験ではこう書く**", "")
    chk(len(_b.split()) <= 115, "model answer %d は 115 語以内" % _i)
    chk(not [c for c in _b if "぀" <= c <= "ヿ" or "一" <= c <= "鿿"],
        "model answer %d に日本語がない" % _i)

in_text("(img/aasl-5-1-idea.svg){#fig-aasl51-idea width=100%}", "図の埋め込み")
in_text("@fig-aasl51-idea (a)", "図 (a) の参照")
in_text("@fig-aasl51-idea (b)", "図 (b) の参照")

for _w in ("そのとおり", "もちろん", "簡単です", "自明", "当たり前", "明らか", "当然"):
    not_in_text(_w, "禁止語 " + _w)
for _w in ("得点になりません", "点になりません", "減点されます"):
    not_in_text(_w, "採点の断定 " + _w)

# ══════════════════════════════════════════════════════════
# 2. 引用と公式集
# ══════════════════════════════════════════════════════════
_quotes = re.findall(r"^> (.*)$", TEXT, re.M)
chk(_quotes == ["Not required: Formal analytic methods of calculating limits."],
    "シラバスの引用は Not required の 1 本だけ: %s" % _quotes)
in_text("**@eq-aasl51-chord は公式集にありません。**", "割線の式は公式集にない")
not_in_text("公式集にあります", "5.1 に「公式集にあります」は置かない")

in_text("\\text{平均変化率} = \\frac{f(b) - f(a)}{b - a}\n$$ {#eq-aasl51-avg}",
        "平均変化率の式")
in_text("\\lim_{x \\to a} f(x) = L\n$$ {#eq-aasl51-lim}", "極限の式")
in_text("\\frac{f(x + h) - f(x)}{h}\n$$ {#eq-aasl51-chord}", "割線の傾きの式")
in_text("{#tbl-aasl51-est}", "極限を見積もる表")
in_text("{#tbl-aasl51-not}", "記号の表")
in_text("{#tbl-aasl51-we1}", "例題1 の表")
in_text("{#tbl-aasl51-we2}", "例題2 の表")
in_text("{#tbl-aasl51-we4}", "例題4 の表")
in_text("[SL 5.2](aasl-5-2.qmd)", "5.2 への参照")

# 記号は 4 つとも出ている（シラバスの Forms of notation）
for _n in ("f'(x)", "\\dfrac{dy}{dx}", "\\dfrac{dV}{dr}", "\\dfrac{ds}{dt}"):
    in_text(_n, "記号 " + _n)

# ══════════════════════════════════════════════════════════
# 3. 図
# ══════════════════════════════════════════════════════════
in_fig('"(a) The chord turns into the tangent"', "図 (a) の題")
in_fig('"(b) A limit is where the outputs are heading"', "図 (b) の題")
in_fig('"$Q_1$"', "図 (a) の Q1")
in_fig('"tangent at $P$"', "図 (a) の接線")
in_fig('"the open circle says $f(a)$ itself need not exist"', "図 (b) の但し書き")
# 図に数値の答えを出していないこと
_figmath = " ".join(re.findall(r"\$([^$]*)\$", FIGCODE))
for _v in ("4", "2.001", "13", "-1", "0.25", "5", "6", "7"):
    chk(_v not in _figmath, "図の数式に答え %s は出さない" % _v)
for _bad in ("\\le ", "\\ge ", "\\lvert", "\\rvert", "\\begin{pmatrix}"):
    chk(_bad not in FIGCODE, "図に mathtext が読めない記法: " + _bad)

# ══════════════════════════════════════════════════════════
# 4. 例題1  f(x) = x^2、x = 2 の割線
# ══════════════════════════════════════════════════════════
_sq = lambda t: sp.nsimplify(t) ** 2
for _h, _want in ((R(1), 5), (R(1, 2), R("4.5")), (R(1, 10), R("4.1")),
                  (R(1, 100), R("4.01"))):
    eq(chord(_sq, 2, _h), _want, "例題1 h=%s の割線" % _h)
    eq(_want - 4, _h, "例題1 h=%s: 4 との差は h" % _h)
eq(_sq(R("2.5")), R("6.25"), "例題1 f(2.5)")
eq(_sq(R("2.1")), R("4.41"), "例題1 f(2.1)")
eq(_sq(R("2.01")), R("4.0401"), "例題1 f(2.01)")
eq(_sq(R("2.05")), R("4.2025"), "検算 f(2.05)")
eq(chord(_sq, 2, R("0.05")), R("4.05"), "検算 h=0.05 の割線")
chk(R("4.01") < R("4.05") < R("4.1"), "検算 4.05 は 4.01 と 4.1 の間")
for _h in (R(1), R(1, 2), R(1, 10), R(1, 100)):
    chk(chord(_sq, 2, _h) > 4, "例題1 h>0 の割線は 4 より大きい")
in_text("| $1$ | $3$ | $9$ | $\\dfrac{9 - 4}{1} = 5$ |", "例題1 表の 1 行目")
in_text("**(b)** 傾きは $4$ に近づいています。", "例題1(b)")

# ══════════════════════════════════════════════════════════
# 5. 例題2  (x^2-9)/(x-3)
# ══════════════════════════════════════════════════════════
_g = lambda t: (sp.nsimplify(t) ** 2 - 9) / (sp.nsimplify(t) - 3)
for _x, _want in ((R("2.9"), R("5.9")), (R("2.99"), R("5.99")),
                  (R("3.01"), R("6.01")), (R("3.1"), R("6.1"))):
    eq(_g(_x), _want, "例題2 x=%s" % _x)
eq(_g(R("2.999")), R("5.999"), "検算 x=2.999")
eq(3 ** 2 - 9, 0, "例題2 分子は 0")
eq(3 - 3, 0, "例題2 分母は 0")
chk(sp.limit((X ** 2 - 9) / (X - 3), X, 3) == 6, "例題2 の極限は 6")
in_text("| $g(x)$ | $5.9$ | $5.99$ | $6.01$ | $6.1$ |", "例題2 の表")
in_text("\\lim_{x \\to 3} g(x) = 6", "例題2 の答え")

# ══════════════════════════════════════════════════════════
# 6. 例題3  植物の高さ
# ══════════════════════════════════════════════════════════
_PLANT = {0: 0, 2: 3, 4: 8, 6: 15, 8: 20}
eq(R(_PLANT[6] - _PLANT[2], 6 - 2), 3, "例題3(a) 平均変化率")
eq(R(_PLANT[4] - _PLANT[2], 4 - 2), R("2.5"), "例題3 検算 2->4")
eq(R(_PLANT[6] - _PLANT[4], 6 - 4), R("3.5"), "例題3 検算 4->6")
chk(R("2.5") < 3 < R("3.5"), "例題3 3 は 2.5 と 3.5 の間")
eq((R("2.5") + R("3.5")) / 2, 3, "例題3 幅が同じなので真ん中")
in_text("| $y$ (cm) | $0$ | $3$ | $8$ | $15$ | $20$ |", "例題3 の表")

# ══════════════════════════════════════════════════════════
# 7. 例題4  f(x) = 1/x、x = 1 の割線
# ══════════════════════════════════════════════════════════
_inv = lambda t: sp.Integer(1) / sp.nsimplify(t)
_W4 = ((R(1, 10), R(-10, 11)), (R(1, 100), R(-100, 101)),
       (R(-1, 10), R(-10, 9)), (R(-1, 100), R(-100, 99)))
for _h, _exact in _W4:
    eq(chord(_inv, 1, _h), _exact, "例題4 h=%s の割線" % _h)
    chk(_exact < 0, "例題4 h=%s の割線は負" % _h)
chk(R(-10, 11) > -1 and R(-100, 101) > -1, "例題4 右からは -1 より大きい")
chk(R(-10, 9) < -1 and R(-100, 99) < -1, "例題4 左からは -1 より小さい")
eq(abs(R(-100, 101) + 1), R(1, 101), "例題4 -100/101 の -1 からのずれ")
eq(abs(R(-100, 99) + 1), R(1, 99), "例題4 -100/99 の -1 からのずれ")
eq(_inv(R("1.1")), R(10, 11), "例題4 f(1.1)")
eq(_inv(R("1.01")), R(100, 101), "例題4 f(1.01)")
eq(_inv(R("0.9")), R(10, 9), "例題4 f(0.9)")
eq(_inv(R("0.99")), R(100, 99), "例題4 f(0.99)")
chk(sp.limit((1 / (1 + H) - 1) / H, H, 0) == -1, "例題4 の極限は -1")

# ══════════════════════════════════════════════════════════
# 8. 演習の答え
# ══════════════════════════════════════════════════════════
# 演習1  x^2、x = 1
for _h, _want, _f1h in ((R(1, 10), R("2.1"), R("1.21")),
                        (R(1, 100), R("2.01"), R("1.0201")),
                        (R(1, 1000), R("2.001"), R("1.002001"))):
    eq(chord(_sq, 1, _h), _want, "演習1 h=%s" % _h)
    eq(_sq(1 + _h), _f1h, "演習1 f(1+h) h=%s" % _h)
    eq(_want - 2, _h, "演習1 2 との差は h")
chk(sp.limit(((1 + H) ** 2 - 1) / H, H, 0) == 2, "演習1 の極限は 2")

# 演習2  (x^2-4)/(x-2)
_g2 = lambda t: (sp.nsimplify(t) ** 2 - 4) / (sp.nsimplify(t) - 2)
for _x, _want in ((R("1.9"), R("3.9")), (R("1.99"), R("3.99")),
                  (R("2.01"), R("4.01")), (R("2.1"), R("4.1"))):
    eq(_g2(_x), _want, "演習2 x=%s" % _x)
chk(sp.limit((X ** 2 - 4) / (X - 2), X, 2) == 4, "演習2 の極限は 4")
eq(_sq(R("2.1")) - 4, R("0.41"), "演習2 検算の分子")

# 演習3  x^3、1 から 3
_cu = lambda t: sp.nsimplify(t) ** 3
eq(chord(_cu, 1, 2), 13, "演習3 平均変化率")
eq(_cu(3), 27, "演習3 f(3)")
eq(chord(_cu, 1, 1), 7, "演習3 1->2")
eq(chord(_cu, 2, 1), 19, "演習3 2->3")
eq((7 + 19) / R(2), 13, "演習3 2 区間の平均")
eq(_cu(2), 8, "演習3 f(2)")

# 演習4  温度
_TEMP = {0: 20, 1: 34, 2: 44, 3: 51, 4: 55, 5: 57}
eq(R(_TEMP[4] - _TEMP[1], 4 - 1), 7, "演習4 平均変化率")
_steps = [_TEMP[i + 1] - _TEMP[i] for i in range(5)]
chk(_steps == [14, 10, 7, 4, 2], "演習4 1 分ごとの増え方: %s" % _steps)
eq(R(sum(_steps[1:4]), 3), 7, "演習4 区間 1..4 の平均")
chk(len(set(_steps[1:4])) > 1, "演習4 1 分ごとの増え方はちがう")
for _v in _steps:
    chk(_v > 0, "演習4 温度は上がりつづける")

# 演習7  区分関数（左右で行き先がちがう）
_L7 = lambda t: 2 * sp.nsimplify(t) + 1
_R7 = lambda t: 5 - sp.nsimplify(t)
for _x, _want in ((R("0.9"), R("2.8")), (R("0.99"), R("2.98"))):
    eq(_L7(_x), _want, "演習7 左の式 x=%s" % _x)
for _x, _want in ((R("1.01"), R("3.99")), (R("1.1"), R("3.9"))):
    eq(_R7(_x), _want, "演習7 右の式 x=%s" % _x)
eq(_L7(1), 3, "演習7 左からの行き先は 3")
eq(_R7(1), 4, "演習7 右からの行き先は 4")
chk(_L7(1) != _R7(1), "演習7 左右で行き先がちがう → 極限なし")
eq(_R7(1), 4, "演習7 f(1) は右の式なので 4")
chk(R("0.9") < 1 and R("0.99") < 1, "演習7 左の 2 点は 1 未満")
chk(R("1.01") > 1 and R("1.1") > 1, "演習7 右の 2 点は 1 より大きい")
chk(sp.limit(2 * X + 1, X, 1) == 3, "演習7 左の式の x->1 は 3")
chk(sp.limit(5 - X, X, 1) == 4, "演習7 右の式の x->1 は 4")

# 演習8  1/x、x = 2
_E8 = ((R(1, 10), R(-5, 21)), (R(-1, 10), R(-5, 19)))
for _h, _exact in _E8:
    eq(chord(_inv, 2, _h), _exact, "演習8 h=%s" % _h)
    chk(_exact < 0, "演習8 h=%s は負" % _h)
chk(R(-5, 19) < R(-1, 4) < R(-5, 21), "演習8 -1/4 をはさむ")
chk(R(5, 21) < R(5, 20) < R(5, 19), "演習8 5/20 をはさむ（検算の形）")
eq(R(5, 20), R(1, 4), "演習8 5/20 = 1/4")
eq(_inv(2), R(1, 2), "演習8 f(2)")
eq(_inv(R("2.1")), R(10, 21), "演習8 f(2.1)")
eq(_inv(R("1.9")), R(10, 19), "演習8 f(1.9)")
chk(sp.limit((1 / (2 + H) - R(1, 2)) / H, H, 0) == R(-1, 4),
    "演習8 の極限は -1/4")
chk(abs(float(R(-1, 4))) < abs(-1), "演習8 x=2 の傾きは x=1 より絶対値が小さい")

# Why it works の (1+h)^2 の展開
chk(sp.expand(((1 + H) ** 2 - 1) / H) == 2 + H, "Why it works: (1+h)^2 の展開")
in_text("= 2 + h", "Why it works: 2 + h")
# |x|/x の左右のちがい
chk(sp.limit(sp.Abs(X) / X, X, 0, "+") == 1, "|x|/x は右から 1")
chk(sp.limit(sp.Abs(X) / X, X, 0, "-") == -1, "|x|/x は左から -1")

# ★ 例題・演習の答えを本文（例題より前）に出していないこと
for _v in ("4.01", "5.99", "6.01", "2.001", "1.002001", "0.909", "1.111",
           "0.238", "0.263", "4.999", "5.01", "13", "$7$"):
    not_in_body(_v, "答え %s は本文に出さない" % _v)

# ══════════════════════════════════════════════════════════
# 9. ページに書いてある計算を、機械的に全部たしかめる
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
    _before = TEXT[:_m.start()].rstrip()
    if _before and _before[-1] in "+-=)*/(":
        continue
    if _before.endswith("\\times"):
        continue
    _vals = [_value(x) for x in _m.group(1).split("=")]
    _nstmt += 1
    chk(len(set(_vals)) == 1,
        "式が合わない: %s  →  %s" % (_m.group(1)[:80], _vals))
chk(_nstmt >= 5, "ページの計算を %d 本たしかめた" % _nstmt)
print("  （計算 %d 本）" % _nstmt)

# ══════════════════════════════════════════════════════════
# 見直し（2026-09）で直したところ。もどってしまわないように。
# ══════════════════════════════════════════════════════════

# --- B1: Why it works の例は x = 5（演習1 の x = 1 と重ねない）----
chk("$f(x) = x^{2}$ で $x = 5$ のところを見てみます。" in TEXT,
    "Why it works の例は x = 5")
chk("= 10 + h" in TEXT, "Why it works: 10 + h")
chk("\\frac{2h + h^{2}}{h} = 2 + h" not in TEXT,
    "演習1 の答えを導く closed form が本文にない")
chk("割線の傾きはちょうど $2 + h$ です" not in TEXT, "同上（言いかえ）")
not_in_body("$2 + h$", "2 + h は本文に出さない")
chk("割線の傾きが $2 + h$ の形になり" not in TEXT, "演習9 の検算からも消えている")

# --- B2: 演習7 は左右で行き先がちがう問題 ------------------------
chk("$f(x) = 2x + 1$ for $x < 1$" in TEXT, "演習7 は区分関数")
chk("does not exist, even though $f(1)$ does" in TEXT,
    "演習7: 極限がないのに f(1) はある")
chk("| $f(x)$ | $2.8$ | $2.98$ | $3.99$ | $3.9$ |" in TEXT, "演習7 の表")
chk("\\dfrac{x^{2} - x - 6}{x - 3}" not in TEXT,
    "演習7: 演習2 と同じ関数（x+2）の古い問題が消えている")
chk("**検算（片側だけ見るとどうなるか）。**" in TEXT,
    "演習7: 片側だけ見た場合の検算がある")

# --- B3: 表に a を入れない理由を正しく書く -----------------------
chk("**表には $a$ そのものを入れません。**" in TEXT, "第3節の言いかえ")
chk("入れても値がないか、極限とは別の値になります。" not in TEXT,
    "誤った（連続なら偽の）文が消えている")
chk("存在していても、極限をそこから決めるわけではありません。" in TEXT,
    "第3節: 極限は f(a) から決めるものではない")

# --- B4: 演習5 は 5.1 の目標の中の問題に差しかわった --------------
chk("Describe the difference in meaning between" in TEXT,
    "演習5: 平均変化率と f'(5) のちがい")
chk("A function $f$ satisfies $f'(x) < 0$ for every value of $x$" not in TEXT,
    "演習5: SL 5.2 の内容だった古い問題が消えている")
chk("turning point" not in TEXT, "5.1 に turning point は出さない（5.8a の語）")
chk("many different curves pass through both given points" in TEXT,
    "演習5: f'(5) が決まらない理由")

# --- M1: 例題3 の検算は「はさまれる」と言わない -------------------
chk("**検算（区間をせまくする）。**" in TEXT, "例題3 の検算の見出し")
chk("この $2$ つの間にあると考えられます。" not in TEXT,
    "導けない（平均値の定理では出ない）主張が消えている")
chk("表の $5$ 点だけからは、その値そのものは決まりません。" in TEXT,
    "例題3: 5 点だけでは決まらないと書いている")

# --- M2: 演習2 は表を完成させる問題 ------------------------------
chk("[Copy and complete the table below, and use it to estimate" in TEXT,
    "演習2: 表を完成させる指示")
chk("| $\\dfrac{x^{2} - 4}{x - 2}$ | | | | |" in TEXT, "演習2 の空の行")
chk("| value | $3.9$" not in TEXT, "演習2: 問題文にない value という見出しが消えた")

# --- M3: 出題のされ方を断定しない ---------------------------------
chk("**このページの例題と演習は、計算が手でできる数にしてあります。**" in TEXT,
    "Paper 1 の注意は、このページについての約束になっている")
chk("割り算が手でできる数で出されます。" not in TEXT,
    "IB の出題を断定した文が消えている")

# --- M4: 3 桁の丸めではなく分数で答えさせる ------------------------
chk("Give each answer as a fraction." in TEXT, "例題4: 分数で答える")
chk("giving each answer as a fraction" in TEXT, "演習8: 分数で答える")
chk("correct to $3$ decimal places" not in TEXT,
    "長い割り算が要る 3 桁指定が消えている")
for _bad in ("-0.909", "-0.990", "-1.111", "-1.010", "-0.238", "-0.263",
             "-0.2505"):
    chk(_bad not in TEXT, "丸めた値 %s が残っていない" % _bad)
chk("$\\dfrac{5}{21} < \\dfrac{5}{20} < \\dfrac{5}{19}$" in TEXT,
    "演習8: 分数のままのはさみうち")

# --- M5: 「落ち着く」に条件がついている ---------------------------
chk("**なめらかな曲線では、割線 $PQ$ の傾きは $1$ つの値に落ち着いていきます。**"
    in TEXT, "第4節: なめらかな曲線では、という条件")
chk("**とがった点があるときは、落ち着かないこともあります。**" in TEXT,
    "Why it works: 落ち着かない場合にふれている")

# --- m1: Leibniz notation の名前を出している ----------------------
chk("**Leibniz notation**（ライプニッツの記法）" in TEXT,
    "第5節で Leibniz notation を定義している")
chk(TEXT.index("Leibniz notation**（ライプニッツの記法）")
    < TEXT.index("in Leibniz notation"), "定義は使う前にある")

# --- m4: ds/dt は「変位」（SL 5.9 と合わせる）---------------------
chk("| $\\dfrac{ds}{dt}$ | 変位 $s$ が時刻 $t$ で決まるとき |" in TEXT,
    "記号の表: ds/dt は変位")

# --- m5: 例題3 の高さは y（h は割線の増分に使っている）-------------
chk("The height of a plant, $y$ cm" in TEXT, "例題3: 高さは y")
chk("$\\dfrac{dy}{dt}$ at $t = 4$" in TEXT, "例題3: dy/dt")
chk("The height of a plant, $h$ cm" not in TEXT, "例題3: 古い h が消えている")

# --- m6: 演習8 の参照先を演習1 と合わせる -------------------------
chk("$f(1.9) = \\dfrac{10}{19}$ です（[第 1 節](#average)）。" in TEXT,
    "演習8 の参照は第 1 節")

print()
print("OK", OK, "/ NG", NG)
