"""AA SL 2.4（グラフの重要な特徴）の内容を検算する。

    python3 figs/aa-sl/check_aasl_2_4.py
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "02-functions")
QMD = os.path.join(BASE, "aasl-2-4.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_2_4.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
# 色コード・ファイル名・キーワードはラベルではないので外す
# （ラベルは必ず空白か $ を含む）
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational
x = sp.Symbol("x")
REALS = sp.S.Reals


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def eq(u, v, msg=""):
    chk(sp.simplify(sp.expand(u) - sp.expand(v)) == 0, msg + f"  ({u} vs {v})")


def ne(u, v, msg=""):
    chk(sp.simplify(sp.expand(u) - sp.expand(v)) != 0, msg + f"  ({u} vs {v})")


def roots(expr, want, msg=""):
    chk(sp.solveset(sp.Eq(expr, 0), x, REALS) == want, "零点: " + msg)


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def not_in_body(sub, msg=""):
    chk(sub not in BODY, "演習の答えが本文に漏れている: " + msg + " :: " + sub[:50])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


# ══════════════════════════════════════════════════════════
# 0. The idea
# ══════════════════════════════════════════════════════════
# zeros と roots は同じ数
roots(x ** 2 - 9, {3, -3}, "x^2-9 の zeros")
chk(sp.solveset(sp.Eq(x ** 2 - 9, 0), x, REALS)
    == sp.solveset(sp.Eq(x ** 2, 9), x, REALS), "zeros と roots は同じ")
# y 切片は 1 つだけ
chk(len(sp.solveset(sp.Eq(x, 0), x, REALS)) == 1, "x = 0 はただ 1 つ")
# 対称性
chk(sp.simplify(((-x) ** 4 - 5 * (-x) ** 2 + 4) - (x ** 4 - 5 * x ** 2 + 4)) == 0,
    "x^4-5x^2+4 は偶関数")
ne(sp.expand((-x) ** 2 + (-x)), sp.expand(x ** 2 + x), "x^2+x は偶関数でない")
# 漸近線（本文の例は p(x) = 1/(x-1) + 2）
_p = 1 / (x - 1) + 2
chk(sp.limit(_p, x, sp.oo) == 2, "本文 水平漸近線 y = 2")
chk(sp.limit(_p, x, -sp.oo) == 2, "左でも 2")
chk(sp.limit(_p, x, 1, "+") is sp.oo, "x → 1+ で +∞")
chk(sp.limit(_p, x, 1, "-") is -sp.oo, "x → 1- で -∞")
eq((1 / (x - 1)).subs(x, sp.Rational("1.01")), 100, "x=1.01 で 100")
eq((1 / (x - 1)).subs(x, sp.Rational("0.99")), -100, "x=0.99 で -100")
eq((1 / (x - 1)).subs(x, 1001), sp.Rational(1, 1000), "x=1001 で 0.001")
eq(sp.Rational(1, sp.Rational("0.5")), 2, "0.5 で割っても 2 倍にしかならない")
# 例題 2 の関数
_g = 1 / (x - 2) + 3
chk(sp.limit(_g, x, sp.oo) == 3, "例題2 水平漸近線 y = 3")
chk(sp.limit(_g, x, 2, "+") is sp.oo, "x → 2+ で +∞")
chk(sp.solveset(sp.Eq(_g, 3), x, REALS) == sp.S.EmptySet, "y = 3 にはならない")
# 本文が例題 2 を先に解いていないか
chk("\\dfrac{1}{x-2} + 3" not in BODY, "例題2 の関数は本文に出てこない")
chk("垂直漸近線は $x = 2$" not in BODY, "例題2(a) の答えは本文にない")
eq(R(1, sp.Rational(1, 100)), 100, "1/0.01 = 100")
eq(R(1, sp.Rational(1, 10000)), 10000, "1/0.0001 = 10000")
eq(R(1, 1000), sp.Rational("0.001"), "1/1000 = 0.001")
# 分子も 0 なら漸近線にならない
chk(sp.simplify((x - 2) / (x - 2)) == 1, "(x-2)/(x-2) は 1")
chk(sp.limit((x - 2) / (x - 2), x, 2) == 1, "x → 2 でも 1")
# 対称の軸は 2 つの零点のまん中
for _p, _q in [(1, 5), (-4, 2), (-3, 7)]:
    eq(R(_p + _q, 2) - _p, _q - R(_p + _q, 2), f"まん中から等距離: {_p},{_q}")

# ══════════════════════════════════════════════════════════
# 1. 例題 1  f(x) = x^2 - 6x + 5
# ══════════════════════════════════════════════════════════
_f1 = x ** 2 - 6 * x + 5
chk(sp.factor(_f1) == (x - 1) * (x - 5), "例題1 因数分解")
roots(_f1, {1, 5}, "例題1(a)")
eq(_f1.subs(x, 1), 0, "検算 f(1) = 0")
eq(_f1.subs(x, 5), 0, "検算 f(5) = 0")
eq(_f1.subs(x, 0), 5, "例題1(b) y 切片 5")
eq(R(1 + 5, 2), 3, "例題1(c) 軸は x = 3")
eq(_f1.subs(x, 3), -4, "頂点の y は -4")
chk(sp.minimum(_f1, x, REALS) == -4, "例題1(d) 最小は -4")
eq(_f1.subs(x, 2), -3, "検算 f(2) = -3")
eq(_f1.subs(x, 4), -3, "検算 f(4) = -3（左右対称）")
chk(_f1.subs(x, 2) == _f1.subs(x, 4), "等しい")
chk(_f1.subs(x, 2) > -4, "頂点より大きい")
chk(sp.solveset(sp.Eq(_f1, -5), x, REALS) == sp.S.EmptySet, "-5 は出ない")
eq(sp.expand((x - 3) ** 2 + 1), x ** 2 - 6 * x + 10, "f(x) = -5 は (x-3)^2+1 = 0")

# ══════════════════════════════════════════════════════════
# 2. 例題 2  g(x) = 1/(x-2) + 3
# ══════════════════════════════════════════════════════════
chk(sp.solveset(sp.Eq(x - 2, 0), x, REALS) == {2}, "例題2(a) VA は x = 2")
eq(sp.simplify(_g.subs(x, 0)), R(5, 2), "例題2(b) y 切片 5/2")
chk(sp.solveset(sp.Eq(_g, 0), x, REALS) == {R(5, 3)}, "例題2(c) x 切片 5/3")
eq(sp.simplify(_g.subs(x, R(5, 3))), 0, "検算 g(5/3) = 0")
eq(sp.simplify(sp.together(_g)), (3 * x - 5) / (x - 2), "通分した形")
eq(sp.simplify(((3 * x - 5) / (x - 2)).subs(x, 0)), R(5, 2), "通分した形でも 5/2")
chk(R(5, 3) < 2, "x 切片は VA の左")
chk(R(5, 2) < 3, "y 切片は HA の下")

# ══════════════════════════════════════════════════════════
# 3. 例題 3  f = x^2-3, g = 2x
# ══════════════════════════════════════════════════════════
_f3, _g3 = x ** 2 - 3, 2 * x
chk(sp.solveset(sp.Eq(_f3, _g3), x, REALS) == {3, -1}, "例題3(a)")
chk(sp.factor(x ** 2 - 2 * x - 3) == (x - 3) * (x + 1), "因数分解")
eq(_g3.subs(x, 3), 6, "例題3(b) g(3) = 6")
eq(_g3.subs(x, -1), -2, "g(-1) = -2")
eq(_f3.subs(x, 3), 6, "検算 f(3) = 6")
eq(_f3.subs(x, -1), -2, "検算 f(-1) = -2")
chk(len(sp.solveset(sp.Eq(_f3, _g3), x, REALS)) == 2, "解は 2 個まで")
chk(sp.degree(sp.expand(_f3 - _g3), x) == 2, "2 次方程式")
eq(_f3.subs(x, 0), -3, "頂点は (0,-3)")
chk(_f3.subs(x, 0) < _g3.subs(x, 0), "頂点は直線より下")

# ══════════════════════════════════════════════════════════
# 4. 例題 4  f(x) = x^4 - 5x^2 + 4
# ══════════════════════════════════════════════════════════
_f4 = x ** 4 - 5 * x ** 2 + 4
chk(sp.factor(_f4) == (x - 1) * (x + 1) * (x - 2) * (x + 2), "例題4 因数分解")
eq(sp.expand((x ** 2 - 1) * (x ** 2 - 4)), _f4, "(x^2-1)(x^2-4)")
roots(_f4, {1, -1, 2, -2}, "例題4(b)")
eq(_f4.subs(x, 0), 4, "例題4(c) y 切片 4")
chk(sp.simplify(_f4.subs(x, -x) - _f4) == 0, "例題4(a) 偶関数")
eq(_f4.subs(x, 2), 0, "検算 f(2) = 0")
eq(_f4.subs(x, -2), 0, "検算 f(-2) = 0")
eq(_f4.subs(x, 1), 0, "検算 f(1) = 0")
eq(_f4.subs(x, 3), 40, "例題4(d) f(3) = 40")
chk(40 > 4, "4 より大きい")
chk(sp.maximum(_f4, x, sp.Interval(-1, 1)) == 4, "x=0 の近くでは 4 が最大")
chk(sp.limit(_f4, x, sp.oo) is sp.oo, "いくらでも大きくなる")
chk(sp.degree(_f4, x) == 4, "4 次なので零点は 4 個まで")

# ══════════════════════════════════════════════════════════
# 5. 演習 1〜10
# ══════════════════════════════════════════════════════════
_x1 = x ** 2 - 4 * x + 3
chk(sp.factor(_x1) == (x - 1) * (x - 3), "演習1 因数分解")
roots(_x1, {1, 3}, "演習1")
eq(_x1.subs(x, 0), 3, "演習1 y 切片")
eq((-1) * (-3), 3, "定数項は (-1)(-3)")
eq(-1 - 3, -4, "x の係数は -4")

_x2 = x ** 2 + 2 * x - 8
chk(sp.factor(_x2) == (x + 4) * (x - 2), "演習2 因数分解")
roots(_x2, {-4, 2}, "演習2 零点")
eq(R(-4 + 2, 2), -1, "演習2 軸")
eq(_x2.subs(x, -1), -9, "演習2 頂点の y")
chk(sp.minimum(_x2, x, REALS) == -9, "実際に最小は -9")
eq(_x2.subs(x, -2), -8, "検算 f(-2) = -8")
eq(_x2.subs(x, 0), -8, "検算 f(0) = -8（左右対称）")
eq(_x2.subs(x, 3), 7, "符号を落とした誤答の位置では 7")
chk(7 > -9, "頂点ではない")

_x3 = 1 / (x + 1)
chk(sp.solveset(sp.Eq(x + 1, 0), x, REALS) == {-1}, "演習3 VA は x = -1")
chk(sp.limit(_x3, x, sp.oo) == 0, "演習3 HA は y = 0")
eq(_x3.subs(x, sp.Rational("-0.9")), 10, "x=-0.9 で 10")
eq(_x3.subs(x, sp.Rational("-0.99")), 100, "x=-0.99 で 100")
eq(_x3.subs(x, 99), R(1, 100), "x=99 で 0.01")
eq(_x3.subs(x, 1), R(1, 2), "x=1 ではふつうの値")

_x4 = 2 / (x - 3) - 1
chk(sp.solveset(sp.Eq(x - 3, 0), x, REALS) == {3}, "演習4 VA は x = 3")
chk(sp.limit(_x4, x, sp.oo) == -1, "演習4 HA は y = -1")
eq(sp.simplify(_x4.subs(x, 0)), -R(5, 3), "演習4 y 切片 -5/3")
eq(sp.simplify(sp.together(_x4)), (5 - x) / (x - 3), "通分した形")
eq(sp.simplify(((5 - x) / (x - 3)).subs(x, 0)), -R(5, 3), "通分した形でも -5/3")
chk(-R(5, 3) < -1, "y 切片は HA の下")
chk(0 < 3, "x=0 は VA の左")

chk(sp.solveset(sp.Eq(x ** 2, x + 2), x, REALS) == {2, -1}, "演習5")
chk(sp.factor(x ** 2 - x - 2) == (x - 2) * (x + 1), "演習5 因数分解")
eq(sp.Integer(2) ** 2, 4, "演習5 (2,4)")
eq(sp.Integer(-1) ** 2, 1, "演習5 (-1,1)")
eq(2 + 2, 4, "もう一方の式でも 4")
eq(-1 + 2, 1, "もう一方の式でも 1")

eq(R(-3 + 7, 2), 2, "演習6 軸は x = 2")
eq(2 - (-3), 5, "左まで 5")
eq(7 - 2, 5, "右まで 5")
eq(R(10, 2), 5, "足し算をまちがえると 5")
ne(5 - (-3), 7 - 5, "その位置では距離が合わない")

chk(sp.simplify(((-x) ** 4 + 3 * (-x) ** 2) - (x ** 4 + 3 * x ** 2)) == 0,
    "演習7 偶関数")
eq((x ** 4 + 3 * x ** 2).subs(x, 2), 28, "演習7 f(2) = 28")
eq((x ** 4 + 3 * x ** 2).subs(x, -2), 28, "f(-2) = 28")
ne(sp.expand((-x) ** 3), sp.expand(x ** 3), "x^3 は偶関数でない")

_x8 = x ** 3 - 4 * x
chk(sp.factor(_x8) == x * (x - 2) * (x + 2), "演習8 因数分解")
roots(_x8, {0, 2, -2}, "演習8")
eq(_x8.subs(x, 0), 0, "検算 f(0) = 0")
eq(_x8.subs(x, 2), 0, "検算 f(2) = 0")
eq(_x8.subs(x, -2), 0, "検算 f(-2) = 0")
chk(sp.degree(_x8, x) == 3, "3 次なので零点は 3 個まで")

chk(sp.solveset(sp.Eq(1 / (x - 4), 0), x, REALS) == sp.S.EmptySet,
    "演習9 x 切片なし")
eq((1 / (x - 4)).subs(x, 104), R(1, 100), "x=104 で 0.01")
eq((1 / (x - 4)).subs(x, 1004), R(1, 1000), "x=1004 で 0.001")
chk(R(1, 1000) != 0, "0 にはならない")

chk(sp.solveset(sp.Eq(x + 2, 0), x, REALS) == {-2}, "演習10 正しくは x = -2")
eq((3 / (x + 2)).subs(x, 2), R(3, 4), "x=2 ではふつうの値 3/4")
ne(R(3, 4), sp.oo, "だから漸近線ではない")
eq((3 / (x + 2)).subs(x, sp.Rational("-1.99")), 300, "x=-1.99 で 300")

# ══════════════════════════════════════════════════════════
# 6. 演習の答えが本文に漏れていないか
# ══════════════════════════════════════════════════════════
for _lk, _m in [("x^{2} - 4x + 3", "演習1"), ("x^{2} + 2x - 8", "演習2"),
                ("(-1, \\ -9)", "演習2"), ("\\dfrac{1}{x+1}", "演習3"),
                ("\\dfrac{2}{x-3}", "演習4"), ("(2, \\ 4)", "演習5"),
                ("x^{4} + 3x^{2}", "演習7"), ("x^{3} - 4x", "演習8"),
                ("\\dfrac{1}{x-4}", "演習9"), ("\\dfrac{3}{x+2}", "演習10")]:
    not_in_body(_lk, _m)

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバス
# ══════════════════════════════════════════════════════════
in_text("## この式は、公式集にありません", "2.4 は公式集にない")
chk(TEXT.index("{#eq-aasl24-axis}") < TEXT.index("## この式は、公式集にありません"),
    "公式集の callout は式の直後に置く")
in_text("> Maximum and minimum values; intercepts; symmetry; vertex; zeros of "
        "functions or roots of equations; vertical and horizontal asymptotes "
        "using graphing technology.", "Guidance を逐語で（末尾まで）")
chk(TEXT.count("\n> ") == 1, f"引用は 1 つだけ: {TEXT.count(chr(10) + '> ')}")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

# ══════════════════════════════════════════════════════════
# 8. 説明のしかた（条件と断定）
# ══════════════════════════════════════════════════════════
in_text("**分数の形をした関数**では、**vertical asymptote（垂直漸近線）** は、", "適用範囲")
in_text("ただし、そこで**分子が $0$ でないこと**が要ります。", "VA の条件")
in_text("## 「極大」は「いちばん大きい」ではありません", "極大と最大を分ける")
in_text("**domain の端の値も、候補に入れてください。**", "端も候補")
in_text("**どんな関数でもグラフが水平漸近線を横切らない、というわけではありません。**",
        "無条件の断定を避けた")
in_text("**$0$ に近い数で割ると、答えの絶対値は大きくなります。**", "言い方を正した")
not_in_text("**小さい数で割ると、答えは大きくなります。**", "誤った言い方は残っていない")
in_text("左から近づけると、$x = 0.99$ で $\\dfrac{1}{-0.01} = -100$", "左からも見た")
in_text("## 対称かどうかは、見た目で決めないでください", "式で確かめる")
in_text("$\\dfrac{x-2}{x-2}$ は、$x \\neq 2$ ではいつも $1$ です。", "分子も 0 の場合")
in_text("**戻すのは、どちらの式でもかまいません。**", "交点の性質")

# ══════════════════════════════════════════════════════════
# 9. GDC
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h for h in _tips if not h.startswith("解説")]
chk(len(_gdc) == 1, f"GDC の折りたたみは 1 つ: {_gdc}")
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")
in_text("**Paper 1 では使えません。**", "Paper 1 では手で解くと明記")

# ══════════════════════════════════════════════════════════
# 10. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 5, "model-answer が 5")
chk(len(re.findall(r"^::: \{#exm-aasl24-", TEXT, re.M)) == 4, "例題が 4")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例が 14")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Worked examples", "Common errors",
         "Exercises"]
chk([h for h in _h2 if h in _want] == _want, "5 つの見出しが所定の順")
chk([h for h in _h2 if h in _want][-1] == "Exercises", "Exercises で終わる")
_idea = [int(_v) for _v in re.findall(r"^### (\d+)\. ", TEXT, re.M)]
chk(_idea == list(range(1, 8)), f"The idea が 1..7 で連番: {_idea}")
chk(TEXT.count("**検算") >= 12, f"検算が十分ある: {TEXT.count('**検算')}")
chk("**確かめ。**" not in TEXT and "**確かめます。**" not in TEXT, "「確かめ。」なし")
for word in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん",
             "当たり前", "そのとおり"]:
    not_in_text(word, "禁止語")
for word in ["得点になりません", "点になりません", "点を落とします",
             "認められません", "減点されます"]:
    not_in_text(word, "採点の断定は避ける")
_MASKED = TEXT.replace("\\$", "")
for _blk in re.findall(r"\$\$(.*?)\$\$", _MASKED, re.S):
    chk("✓" not in _blk and "✗" not in _blk, "表示数式に ✓/✗: " + _blk[:40])
for _blk in re.findall(r"(?<!\$)\$([^$\n]+)\$(?!\$)", _MASKED):
    chk("✓" not in _blk and "✗" not in _blk, "インライン数式に ✓/✗: " + _blk[:40])
_parts = TEXT.split("$$")
chk(all("@eq-" not in _parts[i] for i in range(1, len(_parts), 2)),
    "表示数式の中に @-ref がない")
for _blk in re.findall(r"::: \{\.model-answer\}(.*?):::", TEXT, re.S):
    _body = _blk.replace("**試験ではこう書く**", "")
    chk(not re.search(r"[ぁ-んァ-ン一-龥]", _body), "model-answer に日本語")
    chk(len(_blk.split()) <= 115, f"model-answer が長すぎない: {len(_blk.split())} 語")
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a0 in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a0 in _anchors or _a0 in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aasl24", "他ページの @-ref: " + _r0)
for _f0 in set(re.findall(r"\]\((\.\./)?([a-z0-9/-]+\.qmd)(?:#[a-z0-9-]+)?", TEXT)):
    _path = os.path.join(BASE, _f0[0] + _f0[1]) if _f0[0] else \
        os.path.join(BASE, _f0[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f0[1])
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or ".qmd#" in _href
        or _href.startswith("http"),
        "まだないページへのリンク: " + _href)
for _lab in ["tbl-aasl24-list", "tbl-aasl24-zeros", "tbl-aasl24-how",
             "fig-aasl24-idea", "eq-aasl24-axis", "eq-aasl24-even",
             "eq-aasl24-meet"]:
    chk(TEXT.count("@" + _lab) >= 1, "本文から参照していない: " + _lab)
_head = TEXT[:TEXT.index("## The idea")]
chk("::: {.callout-important}" not in _head,
    "冒頭に公式集の callout を置いていない")
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は What you should be able to do の 1 つだけ")

# ══════════════════════════════════════════════════════════
# 11. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-2-4-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-2-4-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) Key features of a graph", "図(a) の題")
in_fig("local maximum", "図(a) の極大")
in_fig("local minimum", "図(a) の極小")
in_fig("zeros of $f$", "図(a) の零点")
in_fig("(b) Vertical and horizontal asymptotes", "図(b) の題")
in_fig("vertical asymptote", "図(b) の垂直漸近線")
in_fig("horizontal asymptote", "図(b) の水平漸近線")
in_text("(a) Some key features of a curve", "キャプションが (a) を説明")
in_text("(b) A curve with a vertical asymptote and a horizontal asymptote",
        "キャプションが (b) を説明")
# 図は「必ず届かない」と断定していない
chk("but never" not in FIGSTR, "図が無条件の断定をしていない")
# 図に数値の座標を書いていない
chk(not re.search(r"\(\s*-?\d", FIGSTR), "図に数値の座標を書いていない")
for leak in ["= -9", "= -2", "(2, 4)", "x = 3", "y = -1", "= -5/3"]:
    chk(leak not in FIGSTR, "図が演習の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 12. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/02-functions/aasl-2-4.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-2-3.qmd") < DRAFT.index("aasl-2-4.qmd"), "並びが 2.3 → 2.4")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(02-functions/aasl-2-4.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| zero |", "| root |", "| asymptote |", "| vertex |",
           "| local maximum |", "| symmetry |"]:
    chk(_t in GLO, "対訳表にある: " + _t)


# ══════════════════════════════════════════════════════════
# 13. 査読で直したところ（2026-09-07）
# ══════════════════════════════════════════════════════════
# 所見 1 — 例題 4 の検算に零点を使わない
in_text("**数を $1$ つ入れて確かめます。ただし零点は使えません。**", "零点では検算にならない")
eq(_f4.subs(x, 3), _f4.subs(x, -3), "f(3) = f(-3)")
eq(_f4.subs(x, 3), 40, "しかも 0 ではない")
# 零点を使う検算は、偶関数でない関数も通してしまう
_odd = x ** 3 - 4 * x
eq(_odd.subs(x, 2), _odd.subs(x, -2), "x^3-4x でも f(2) = f(-2) = 0")
ne(sp.expand(_odd.subs(x, -x)), sp.expand(_odd), "しかし偶関数ではない")
# 所見 2 — 例題 1(d) の検算を値域そのものに
in_text("**頂点からのずれを $t$ とおいて、値域そのものを出します。**", "すべての x で示した")
_t = sp.Symbol("t")
eq(sp.expand(_f1.subs(x, 3 + _t)), _t ** 2 - 4, "f(3+t) = t^2 - 4")
not_in_text("$(x-3)^{2} + 1 = 0$", "平方完成（SL 2.6）を先取りしない")
# 所見 3 — 演習 1 の y 切片の検算
in_text("$y$ 切片は、**因数分解した形から出し直します。**", "別の道すじ")
eq((0 - 1) * (0 - 3), 3, "(0-1)(0-3) = 3")
# 所見 7 — maximum と local maximum
in_text("- **maximum value**（最大値）が、極大の値とは別ものであることが分かる。",
        "冒頭で区別した")
not_in_text("- **maximum**（極大）と **minimum**（極小）を、座標で書ける。",
            "古い書き方は残っていない")
# 所見 10 — 断定を弱めた
in_text("試験で減点されるとは限りませんが、**聞かれた形に合わせて書く**のがいちばん安全です。",
        "断定を弱めた")
in_text("## `zero` と `intercept` を書き分けない", "Common error の見出し")
# 所見 11 — 例題 1(d) に定義域
in_text("**(d)** 定義域は実数全体です。下に凸の放物線なので、", "定義域を書いた")
# 所見 12 — 谷の底といえる条件
chk(TEXT.count("**下に凸の放物線では、軸の上の点がいちばん低い点**") == 2,
    "例題 1 と演習 2 の 2 か所")
# 所見 13 — 演習 10 の検算
in_text("**「$x = -2$ で分母が $0$」を確かめても、$-2$ を出した手順をなぞるだけ**",
        "循環だと明記")
eq((3 / (x + 2)).subs(x, sp.Rational("-2.01")), -300, "x=-2.01 で -300")
# 所見 16 — 表記をそろえた
in_text("因数分解、または解の公式（SL 2.7）で解けるなら", "項目番号をそろえた")
# 図のラベル
chk("($x$-intercepts)" not in FIGSTR, "図は zeros と intercepts を同一視していない")
in_text("(a) Some key features of a curve: the zeros of $f$", "キャプションも直した")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
