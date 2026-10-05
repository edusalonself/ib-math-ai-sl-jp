"""AA HL 1.11（部分分数分解）の内容を検算する。

    python3 figs/aa-hl/check_aahl_1_11.py
"""
import glob
import os
import re
import sys

import sympy as sp
from sympy import Rational as R

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "01-number-and-algebra")
QMD = os.path.join(BASE, "aahl-1-11.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_1_11.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
x = sp.Symbol("x")
A, B = sp.symbols("A B")


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def eq(a, b, msg=""):
    chk(sp.simplify(sp.together(a) - sp.together(b)) == 0,
        msg + "  (%s vs %s)" % (a, b))


def ne(a, b, msg=""):
    chk(sp.simplify(sp.together(a) - sp.together(b)) != 0,
        msg + "  (%s vs %s)" % (a, b))


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


def split_ok(num, p, q, a, b, tag):
    """num/((x-p)(x-q)) = a/(x-p) + b/(x-q) を、第一原理から確かめる。"""
    lhs = num / ((x - p) * (x - q))
    rhs = a / (x - p) + b / (x - q)
    eq(lhs, rhs, tag + " の分解")
    # 恒等式なので、使っていない値でも一致する
    for _v in [0, 1, 7, -5, R(1, 3)]:
        if (_v - p) != 0 and (_v - q) != 0:
            chk(sp.simplify(lhs.subs(x, _v) - rhs.subs(x, _v)) == 0,
                "%s：x=%s でも一致" % (tag, _v))
    # 代入で出した A, B が、sympy の apart と合う
    _ap = sp.apart(sp.together(lhs), x)
    eq(_ap, rhs, tag + " の apart と一致")


# ══════════════════════════════════════════════════════════
# 0. 一般論（記号のまま）
# ══════════════════════════════════════════════════════════
_p, _q, _m, _c = sp.symbols("p q m c")
# A(x-q) + B(x-p) = mx + c の連立方程式の解（p ≠ q のとき）
_sol = sp.solve([sp.Eq(A + B, _m), sp.Eq(-_q * A - _p * B, _c)], [A, B],
                dict=True)
chk(len(_sol) == 1, "p ≠ q なら解はただ 1 組")
_AA, _BB = _sol[0][A], _sol[0][B]
eq(sp.simplify(_AA * (x - _q) + _BB * (x - _p)), _m * x + _c,
   "解を戻すと mx + c に戻る")
chk(sp.denom(sp.simplify(_AA)).has(_p - _q) or sp.denom(sp.simplify(_AA)).has(_q - _p),
    "解の分母に p - q が現れる（p = q だと決まらない）")
# 右辺をまとめた分子は、いつも 1 次以下
_comb = sp.together(A / (x - _p) + B / (x - _q))
_num = sp.expand(sp.numer(_comb))
chk(sp.degree(_num, x) <= 1, "まとめた分子はいつも 1 次以下")
# 2 次の分子は作れない
chk(sp.solve([sp.Eq(A + B, 0), sp.Eq(-_q * A - _p * B, 0)], [A, B],
             dict=True) is not None, "連立方程式が立つ")
chk(sp.expand(_num).coeff(x, 2) == 0, "x^2 の項は作れない")

# ══════════════════════════════════════════════════════════
# 1. The idea の数値
# ══════════════════════════════════════════════════════════
eq(2 / (x - 3) + 1 / (x + 1), (3 * x - 1) / (x ** 2 - 2 * x - 3), "§1 の足し算")
eq(sp.expand(2 * (x + 1) + (x - 3)), 3 * x - 1, "§1 の分子")
eq(sp.expand((x - 3) * (x + 1)), x ** 2 - 2 * x - 3, "§1 の分母")
eq(sp.factor(x ** 2 - x - 6), (x - 3) * (x + 2), "§3 手順1 の因数分解")
split_ok(7 * x - 1, 3, -2, 4, 3, "§3〜§6")
eq(7 * 3 - 1, 20, "§4 x=3 で 20")
eq(sp.Integer(20) / 5, 4, "§4 A = 4")
eq(7 * (-2) - 1, -15, "§4 x=-2 で -15")
eq(sp.Integer(-15) / -5, 3, "§4 B = 3")
# 係数の比較
eq(sp.expand(A * (x + 2) + B * (x - 3)), (A + B) * x + (2 * A - 3 * B),
   "§5 展開した形")
_s5 = sp.solve([sp.Eq(A + B, 7), sp.Eq(2 * A - 3 * B, -1)], [A, B], dict=True)[0]
chk(_s5[A] == 4 and _s5[B] == 3, "§5 連立方程式の解は A=4, B=3")
eq(2 * (7 - B) - 3 * B, 14 - 5 * B, "§5 代入して 14 - 5B")
eq(sp.solve(sp.Eq(14 - 5 * B, -1), B)[0], 3, "§5 B = 3")
# §6 の検算（x = 0）
eq(R(-1, -6), R(1, 6), "§6 左辺は 1/6")
eq(R(4, -3) + R(3, 2), R(1, 6), "§6 右辺も 1/6")
# §7 積分
eq(sp.diff(4 * sp.log(x - 3) + 3 * sp.log(x + 2), x),
   4 / (x - 3) + 3 / (x + 2), "§7 微分すると分解した式に戻る")
# §7 二項展開
eq(5 / ((1 - x) * (1 + 4 * x)), 1 / (1 - x) + 4 / (1 + 4 * x), "§7 の分解")
eq(sp.expand(sp.series(5 / ((1 - x) * (1 + 4 * x)), x, 0, 3).removeO()),
   5 - 15 * x + 65 * x ** 2, "§7 の展開")
eq(1 + 4, 5, "§7 定数項 1 + 4 = 5")
eq(1 - 16, -15, "§7 x の係数 1 - 16 = -15")
eq(1 + 64, 65, "§7 x^2 の係数 1 + 64 = 65")
chk(min(1, R(1, 4)) == R(1, 4), "§7 きびしいほうは |x| < 1/4")

# ══════════════════════════════════════════════════════════
# 2. 例題 1〜4
# ══════════════════════════════════════════════════════════
split_ok(5 * x + 7, -1, -3, 1, 4, "例題1")
eq(sp.expand((x + 3) + 4 * (x + 1)), 5 * x + 7, "例題1 の足し戻し")
eq(R(7, 3), 1 + R(4, 3), "例題1 x=0 の検算")
eq(5 * (-1) + 7, 2, "例題1 x=-1 で 2")
eq(5 * (-3) + 7, -8, "例題1 x=-3 で -8")

eq(sp.factor(x ** 2 - 3 * x - 4), (x - 4) * (x + 1), "例題2 の因数分解")
split_ok(x + 6, 4, -1, 2, -1, "例題2")
eq(sp.expand(2 * (x + 1) - (x - 4)), x + 6, "例題2 の足し戻し")
eq(R(6, -4), R(-3, 2), "例題2 x=0 の左辺")
eq(R(2, -4) - 1, R(-3, 2), "例題2 x=0 の右辺")
eq(R(2, -4) + 1, R(1, 2), "例題2 の誤答（B の符号）")
ne(R(1, 2), R(-3, 2), "その誤答は合わない")
chk(sp.discriminant(x ** 2 - 3 * x + 4, x) == -7, "例題2(b) の判別式は -7")
chk(sp.discriminant(x ** 2 - 3 * x + 4, x) < 0, "実数解を持たない")
chk(len([r for r in sp.solve(sp.Eq(x ** 2 - 3 * x + 4, 0), x) if r.is_real]) == 0,
    "実数の 1 次式の積に書けない")

eq(sp.factor(x ** 2 + 3 * x - 4), (x - 1) * (x + 4), "例題3 の因数分解")
split_ok(2 * x + 23, 1, -4, 5, -3, "例題3")
eq(sp.expand(A * (x + 4) + B * (x - 1)), (A + B) * x + (4 * A - B),
   "例題3 の展開")
_s3 = sp.solve([sp.Eq(A + B, 2), sp.Eq(4 * A - B, 23)], [A, B], dict=True)[0]
chk(_s3[A] == 5 and _s3[B] == -3, "例題3 の連立方程式の解")
eq(2 + 23, 25, "例題3 2 本を足すと 25")
eq(R(25, 5), 5, "例題3 A = 5")
eq(2 * 1 + 23, 25, "例題3 代入 x=1 で 25")
eq(2 * (-4) + 23, 15, "例題3 代入 x=-4 で 15")
eq(R(15, -5), -3, "例題3 B = -3")
eq(R(23, -4), R(-23, 4), "例題3 x=0 の左辺")
eq(R(5, -1) - R(3, 4), R(-23, 4), "例題3 x=0 の右辺")
eq(sp.expand(5 * (x + 4) - 3 * (x - 1)), 2 * x + 23, "例題3 の足し戻し")

split_ok(10, 2, -3, 2, -2, "例題4")
eq(sp.integrate(10 / ((x - 2) * (x + 3)), x).rewrite(sp.log).diff(x),
   10 / ((x - 2) * (x + 3)), "例題4(b) 微分すると戻る")
eq(sp.diff(2 * sp.log(x - 2) - 2 * sp.log(x + 3), x),
   2 / (x - 2) - 2 / (x + 3), "例題4(b) の微分")
_I = sp.integrate(10 / ((x - 2) * (x + 3)), (x, 3, 4))
eq(sp.simplify(_I), 2 * sp.log(R(12, 7)), "例題4(c) = 2 ln(12/7)")
eq(2 * sp.log(2) - 2 * sp.log(7) + 2 * sp.log(6), 2 * sp.log(R(12, 7)),
   "2ln2 - 2ln7 + 2ln6 = 2ln(12/7)")
eq(sp.log(1), 0, "ln 1 = 0")
chk(abs(float(2 * sp.log(R(12, 7))) - 1.078) < 1e-3, "値は 1.078 ほど")
chk(abs(float(R(10, 6)) - 1.67) < 0.01, "x=3 での被積分関数は 1.67")
chk(abs(float(R(10, 14)) - 0.71) < 0.01, "x=4 での被積分関数は 0.71")
chk(float(R(10, 14)) < float(2 * sp.log(R(12, 7))) < float(R(10, 6)),
    "面積は 0.71 と 1.67 のあいだ")
ne(sp.log(R(14, 6)), sp.log(R(12, 7)), "12/7 と 14/6 はちがう")
eq(R(10, (-2) * 3), R(-5, 3), "例題4 x=0 の左辺")
eq(R(2, -2) - R(2, 3), R(-5, 3), "例題4 x=0 の右辺")

# ══════════════════════════════════════════════════════════
# 3. 演習 1〜10
# ══════════════════════════════════════════════════════════
split_ok(5 * x + 16, -2, -5, 2, 3, "演習1")
eq(5 * (-2) + 16, 6, "演習1 x=-2 で 6")
eq(5 * (-5) + 16, -9, "演習1 x=-5 で -9")
eq(R(16, 10), R(8, 5), "演習1 x=0 の左辺")
eq(1 + R(3, 5), R(8, 5), "演習1 x=0 の右辺")
eq(sp.expand(2 * (x + 5) + 3 * (x + 2)), 5 * x + 16, "演習1 の足し戻し")

eq(sp.factor(x ** 2 - x - 2), (x - 2) * (x + 1), "演習2 の因数分解")
split_ok(x - 8, -1, 2, 3, -2, "演習2")
eq(-1 - 8, -9, "演習2 x=-1 で -9")
eq(2 - 8, -6, "演習2 x=2 で -6")
eq(R(-8, -2), 4, "演習2 x=0 の左辺")
eq(3 - R(2, -2), 4, "演習2 x=0 の右辺")
eq(3 - 1, 2, "演習2 の誤答（B=+2）は 2")
ne(2, 4, "その誤答は合わない")

eq(sp.factor(x ** 2 - 3 * x - 10), (x - 5) * (x + 2), "演習3 の因数分解")
split_ok(9 * x - 17, 5, -2, 4, 5, "演習3")
eq(9 * 5 - 17, 28, "演習3 x=5 で 28")
eq(9 * (-2) - 17, -35, "演習3 x=-2 で -35")
eq(sp.expand(4 * (x + 2) + 5 * (x - 5)), 9 * x - 17, "演習3 の足し戻し")
eq(4 + 5, 9, "演習3 A+B = x の係数")
eq(4 * 2 + 5 * (-5), -17, "演習3 定数項も合う")

eq(sp.factor(2 * x ** 2 + 5 * x + 2), (x + 2) * (2 * x + 1), "演習4 の因数分解")
eq((8 * x + 7) / (2 * x ** 2 + 5 * x + 2), 2 / (2 * x + 1) + 3 / (x + 2),
   "演習4 の分解")
eq(8 * (-2) + 7, -9, "演習4 x=-2 で -9")
eq(8 * R(-1, 2) + 7, 3, "演習4 x=-1/2 で 3")
eq(sp.expand(2 * (x + 2) + 3 * (2 * x + 1)), 8 * x + 7, "演習4 の足し戻し")
eq(R(7, 2), 2 + R(3, 2), "演習4 x=0 の検算")

split_ok(5 * x + 11, 1, -3, 4, 1, "演習5")
eq(5 * 1 + 11, 16, "演習5 x=1 で 16")
eq(5 * (-3) + 11, -4, "演習5 x=-3 で -4")
eq(R(11, -3), -4 + R(1, 3), "演習5 x=0 の検算")
eq(sp.expand(4 * (x + 3) + (x - 1)), 5 * x + 11, "演習5 の足し戻し")

eq(sp.factor(x ** 2 - 9), (x - 3) * (x + 3), "演習6 の因数分解")
split_ok(x - 9, 3, -3, -1, 2, "演習6")
eq(sp.expand(A * (x + 3) + B * (x - 3)), (A + B) * x + (3 * A - 3 * B),
   "演習6 の展開")
_s6 = sp.solve([sp.Eq(A + B, 1), sp.Eq(3 * A - 3 * B, -9)], [A, B], dict=True)[0]
chk(_s6[A] == -1 and _s6[B] == 2, "演習6 の連立方程式の解")
eq(3 - 9, -6, "演習6 x=3 で -6")
eq(-3 - 9, -12, "演習6 x=-3 で -12")
eq(R(-6, 6), -1, "演習6 A = -1")
eq(R(-12, -6), 2, "演習6 B = 2")

eq(6 / ((1 - x) * (1 + 2 * x)), 2 / (1 - x) + 4 / (1 + 2 * x), "演習7(a)")
eq(6, sp.expand(2 * (1 + 2 * x) + 4 * (1 - x)), "演習7 の足し戻し")
eq(sp.expand(sp.series(6 / ((1 - x) * (1 + 2 * x)), x, 0, 3).removeO()),
   6 - 6 * x + 18 * x ** 2, "演習7(b)")
eq(2 + 4, 6, "演習7 定数項")
eq(2 - 8, -6, "演習7 x の係数")
eq(2 + 16, 18, "演習7 x^2 の係数")
chk(min(1, R(1, 2)) == R(1, 2), "演習7(c) きびしいほうは |x| < 1/2")
eq(sp.expand((1 - x) * (1 + 2 * x)), 1 + x - 2 * x ** 2, "演習7 分母の展開")
eq(sp.expand(sp.series(6 * (1 + (x - 2 * x ** 2)) ** -1, x, 0, 3).removeO()),
   6 - 6 * x + 18 * x ** 2, "演習7 分けずに出しても同じ")
eq(6 / ((1 - 0) * (1 + 0)), 6, "演習7 f(0) = 6")

_lhs8 = (x ** 2 + 1) / ((x - 1) * (x + 2))
_num8 = sp.expand(A * (x + 2) + B * (x - 1))
chk(sp.expand(_num8).coeff(x, 2) == 0, "演習8：まとめた分子に x^2 はない")
chk(sp.solve([sp.Eq(A + B, 0), sp.Eq(2 * A - B, 0), sp.Eq(0, 1)],
             [A, B], dict=True) == [], "演習8：解が存在しない")
eq(sp.expand(_num8), (A + B) * x + (2 * A - B), "演習8 の分子")

eq(sp.factor(x ** 2 + 2 * x - 8), (x - 2) * (x + 4), "演習9 の因数分解")
split_ok(9 * x + 12, -4, 2, 4, 5, "演習9")
eq(9 * (-4) + 12, -24, "演習9 x=-4 で -24")
eq(9 * 2 + 12, 30, "演習9 x=2 で 30")
eq(sp.expand(4 * (x - 2) + 5 * (x + 4)), 9 * x + 12, "演習9 の足し戻し")
eq(sp.diff(4 * sp.log(x + 4) + 5 * sp.log(x - 2), x),
   4 / (x + 4) + 5 / (x - 2), "演習9(b) 微分すると戻る")

split_ok(7 * x + 1, -1, 2, 2, 5, "演習10")
eq(7 * (-1) + 1, -6, "演習10 x=-1 で -6")
eq(7 * 2 + 1, 15, "演習10 x=2 で 15")
eq(sp.expand(2 * (x - 2) + 5 * (x + 1)), 7 * x + 1, "演習10 の足し戻し")
eq(R(1, (1) * (-2)), R(-1, 2), "演習10 x=0 の左辺")
eq(2 - R(5, 2), R(-1, 2), "演習10 x=0 の右辺")
# 生徒の式は x=-1 で成り立たない
chk(sp.simplify((7 * x + 1).subs(x, -1)
                - (A * (x + 1) + B * (x - 2)).subs(x, -1)) == -6 + 3 * B,
    "生徒の式は x=-1 で -6 = -3B となり A が出ない")
chk((7 * (-1) + 1) != 0, "生徒の式では左辺が 0 でない")

# ══════════════════════════════════════════════════════════
# 4. シラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("> Maximum of two distinct linear terms in the denominator,"
        " with degree of numerator less than the degree of the denominator.",
        "範囲の Guidance を逐語で")
in_text("> Example: $\\dfrac{2x+1}{x^{2}+x-2} \\equiv \\dfrac{1}{(x-1)}"
        " + \\dfrac{1}{(x+2)}$", "シラバスの例を逐語で")
in_text("`Link to: use of partial fractions to rearrange the integrand`",
        "積分への Link を引用")
in_text("## この項目に、公式集の欄はありません", "公式集にないと書く")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")
# シラバスの例は、例題・演習で使い回していない
chk(TEXT.count("x^{2}+x-2") == 1, "シラバスの分母は引用の 1 か所だけ")
eq((2 * x + 1) / (x ** 2 + x - 2), 1 / (x - 1) + 1 / (x + 2),
   "シラバスの例は正しい")

# ══════════════════════════════════════════════════════════
# 5. GDC
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h for h in _tips
        if not h.startswith("解説") and h != "クリックすると開きます"]
chk(len(_gdc) == 1, "GDC の折りたたみは 1 つ: %s" % _gdc)
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")
in_text("**Paper 1 では使えません。**", "Paper 1 では手で解くと明記")
in_text("**Simultaneous Equation Solver**", "検証済みの機能だけを書く")
for _m in ["Casio", "fx-CG50", "TI-84", "OPTN", "PRB", "expand(", "propFrac"]:
    not_in_text(_m, "他機種・確かめていない機能: " + _m)

# ══════════════════════════════════════════════════════════
# 6. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 4, "model-answer が 4")
chk(len(re.findall(r"^::: \{#exm-aahl111-", TEXT, re.M)) == 4, "例題が 4")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例が 14")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Worked examples", "Common errors",
         "Exercises"]
chk([h for h in _h2 if h in _want] == _want, "5 つの見出しが所定の順")
_idea = [int(_v) for _v in re.findall(r"^### (\d+)\. ", TEXT, re.M)]
chk(_idea == list(range(1, 8)), "The idea が 1..7 で連番: %s" % _idea)
chk(TEXT.count("**検算") >= 12, "検算が十分ある: %d" % TEXT.count("**検算"))
chk("**確かめ。**" not in TEXT and "**確かめます。**" not in TEXT, "「確かめ。」なし")
for word in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん",
             "当たり前", "そのとおり"]:
    not_in_text(word, "禁止語")
_ce = TEXT[TEXT.index("\n## Common errors"):TEXT.index("\n## Exercises")]
chk(_ce.count("::: {.callout-warning}") == 6, "Common errors が 6 つ")
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
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a0 in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a0 in _anchors or _a0 in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aahl111", "他ページの @-ref: " + _r0)
for _href in re.findall(r"\]\(([^)]+\.qmd[^)]*)\)", TEXT):
    _p0 = os.path.normpath(os.path.join(os.path.dirname(QMD),
                                        _href.split("#")[0]))
    chk(os.path.exists(_p0), "リンク先のページがない: " + _href)
chk(len(re.findall(r"\]\(aahl-1-10b\.qmd", TEXT)) >= 2,
    "HL 1.10b へのリンクがある")
chk(len(re.findall(r"\]\(\.\./\.\./aa-sl/", TEXT)) >= 2,
    "AA SL へのリンクがある")
_head = TEXT[:TEXT.index("## The idea")]
chk("::: {.callout-important}" not in _head,
    "冒頭に公式集の callout を置いていない")
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は What you should be able to do の 1 つだけ")
not_in_text("**この節ですること：", "節の頭の 1 文は置かない")
not_in_text("\\vec{", "ベクトルの記号は太字")
chk(len(re.findall(r"^::: ", TEXT, re.M)) == len(re.findall(r"^:::$", TEXT, re.M)),
    "::: の開閉が一致")
for _h in re.findall(r"^#{1,4} .+$", TEXT, re.M):
    chk(not re.search(r"\$\s*—", _h), "見出しで数式の直後に —: " + _h)
# 表のセルの中に裸の | がない
for _line in TEXT.splitlines():
    if _line.startswith("|") and _line.endswith("|"):
        if re.fullmatch(r"[|:\- ]+", _line):
            continue          # 表の区切り行（|:--|:--|）は対象外
        _cells = _line[1:-1].split(" | ")
        for _cell in _cells:
            chk("|" not in _cell or "\\lvert" in _cell or "\\rvert" in _cell,
                "表のセルの中の裸の | :: " + _line[:60])

# ══════════════════════════════════════════════════════════
# 7. Why it works は折りたたむ
# ══════════════════════════════════════════════════════════
_i = TEXT.index(chr(10) + "## Why it works" + chr(10))
_j = TEXT.index(chr(10) + "## Worked examples", _i)
_wiw = TEXT[_i:_j]
chk('collapse="true"}' + chr(10) + "## クリックすると開きます" in _wiw,
    "Why it works は折りたたんである")
chk(_wiw.rstrip().endswith(":::"), "折りたたみが閉じてある")
chk(_wiw.count("クリックすると開きます") == 1, "折りたたみは 1 つだけ")

# ══════════════════════════════════════════════════════════
# 8. 節の見出し
# ══════════════════════════════════════════════════════════
# ★ The idea の見出しは「英語（日本語）」の形（_AA-HL-PLAN.md の「決まったこと」5）
for _hh in re.findall(r"^### \d+\. (.+?) \{#", TEXT, re.M):
    chk(_hh.endswith("）") and "（" in _hh,
        "見出しが 英語（日本語） の形でない: " + _hh)
    chk(re.match(r"[A-Za-z$]", _hh) is not None,
        "見出しが英語で始まっていない: " + _hh)
    _en = _hh[:_hh.rindex("（")]
    chk(not re.search(r"[ぁ-んァ-ヶ一-龥]", _en),
        "見出しの英語の側に日本語がある: " + _hh)
in_text("### 1. Undoing an addition of fractions（足し算を、逆向きにたどる） "
        "{#idea}", "見出し 1")
in_text("### 2. How far the syllabus goes（どこまでが範囲か） {#scope}", "見出し 2")
in_text("### 3. The method（手順） {#method}", "見出し 3")
in_text("### 4. Finding $A$ and $B$ by substitution（$A$ と $B$ "
        "の出し方：代入する） {#substitution}", "見出し 4")
in_text("### 5. Equating coefficients（係数をくらべる） {#coefficients}", "見出し 5")
in_text("### 6. Identities and equations（恒等式と方程式のちがい） {#identity}", "見出し 6")
in_text("### 7. What partial fractions are for（何に使うのか） {#uses}", "見出し 7")
for _st in ["#### 手順 1：分母を因数分解する {#step1}",
            "#### 手順 2：分けた形を書く {#step2}",
            "#### 手順 3：分母をはらう {#step3}",
            "#### 手順 4：$A$ と $B$ を決める {#step4}"]:
    in_text(_st, "手順の見出し")

# ══════════════════════════════════════════════════════════
# 9. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aahl-1-11-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aahl-1-11-idea.svg)" in TEXT, "本文が図を貼っている")
for _s in glob.glob(os.path.join(BASE, "img", "*.png")):
    chk(False, "PNG が残っている: " + os.path.basename(_s))
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("A single fraction, seen as a sum of two simple ones", "図の題")
in_fig("their sum", "図の凡例")
in_fig("POLES = (-1.0, 3.0)", "図の漸近線は x=-1, x=3")
in_text("$2$ つの点線を足すと、実線になります。点線は $x = -1$ と $x = 3$ で切れています。",
        "キャプションが図を説明")
# 図の関数が本文と合っている
eq(2 / (x - 3) + 1 / (x + 1), (3 * x - 1) / ((x - 3) * (x + 1)), "図の和")
in_fig("$y = \\\\dfrac{2}{x-3}$", "図の 1 本目")
in_fig("$y = \\\\dfrac{1}{x+1}$", "図の 2 本目")
# 図が例題・演習の答えを載せていないか
for leak in ["5x+7", "x+6", "2x+23", "5x+16", "x-8", "9x-17", "8x+7",
             "5x+11", "x-9", "9x+12", "7x+1"]:
    chk(leak not in FIGSTR, "図が例題・演習の式を載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 10. 演習の答えが、本文・例題に出ていないか
# ══════════════════════════════════════════════════════════
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("5x+16", "演習1"), ("x-8}{x^{2}-x-2", "演習2"),
                    ("9x-17", "演習3"), ("8x+7", "演習4"),
                    ("5x+11", "演習5"), ("x-9}{x^{2}-9", "演習6"),
                    ("9x+12", "演習9"), ("7x+1", "演習10")]:
    chk(leak not in _BODY, "%s の式が本文・例題に出ている: %s" % (where, leak))
chk("6 - 6x + 18x^{2}" not in _BODY and "6 - 6x + 18x^{2}" not in _BODY,
    "演習7 の展開が本文に出ていない")

# ══════════════════════════════════════════════════════════
# 11. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-hl/01-number-and-algebra/aahl-1-11.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aahl-1-10b.qmd") < DRAFT.index("aahl-1-11.qmd"),
    "サイドバーの並びが 1.10b → 1.11")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(01-number-and-algebra/aahl-1-11.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
_ticked = re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written),
    "✅ %d と ページ %d" % (len(_ticked), len(_written)))
chk(len(re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|", IDX, re.M)) == 35,
    "一覧は 35 行")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
chk(_mm is not None and int(_mm.group(2)) == 35, "「全 35 ページ」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| partial fractions |", "| equating coefficients |",
          "| difference of two squares |", "| identity |", "| discriminant |"]:
    chk(t in GLO, "対訳表にある: " + t)
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written),
    "PLAN の進捗がページ数と合っている")

# ══════════════════════════════════════════════════════════
# 12. 見張り
# ══════════════════════════════════════════════════════════
in_text("**ですから $p \\neq q$、つまり $2$ つの因数が別のものであることが要ります。**",
        "distinct の理由")
in_text("**これが `degree of numerator less than the degree of the denominator`"
        " の意味です。**", "分子の次数の理由")
in_text("**$x = 3$ と $x = -2$ は、$A$ と $B$ を決めるのに使った値なので、"
        "検算になりません。**", "検算に使ってはいけない値")
in_text("**きびしいほうに合わせます。**", "二項展開の範囲")
chk(TEXT.count("足し算に戻します") + TEXT.count("足し算に戻す") >= 4,
    "足し戻しの検算を何度も使っている")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
