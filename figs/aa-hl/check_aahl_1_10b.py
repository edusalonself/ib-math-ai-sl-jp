"""AA HL 1.10b（二項定理の拡張）の内容を検算する。

    python3 figs/aa-hl/check_aahl_1_10b.py
"""
import glob
import os
import re
import sys

import sympy as sp
from sympy import Rational as R
from sympy import factorial as F

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-hl", "01-number-and-algebra")
QMD = os.path.join(BASE, "aahl-1-10b.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_aahl_1_10b.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
x = sp.Symbol("x")
u = sp.Symbol("u")


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def eq(a, b, msg=""):
    chk(sp.simplify(sp.expand(a) - sp.expand(b)) == 0, msg + "  (%s vs %s)" % (a, b))


def ne(a, b, msg=""):
    chk(sp.simplify(sp.expand(a) - sp.expand(b)) != 0, msg + "  (%s vs %s)" % (a, b))


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


def chain(n, r):
    """かけ算の鎖 n(n-1)...(n-r+1) / r!"""
    p = sp.Integer(1)
    for k in range(r):
        p *= (n - k)
    return sp.nsimplify(p / F(r))


def series_of(expr, k=5, var=x):
    return sp.expand(sp.series(expr, var, 0, k).removeO())


def coeffs(poly, k, var=x):
    e = sp.expand(poly)
    return [sp.nsimplify(e.coeff(var, i)) for i in range(k)]


# ══════════════════════════════════════════════════════════
# 0. 公式そのもの（記号のまま）
# ══════════════════════════════════════════════════════════
# かけ算の鎖が、sympy の級数展開と一致するか（分数・負・整数の n で）
for _n in [R(1, 2), R(1, 3), R(1, 4), R(-1, 2), R(2, 3), R(-3, 2),
           -1, -2, -3, -4, 2, 3, 5]:
    _s = series_of((1 + x) ** _n, 6)
    for _r in range(6):
        eq(sp.nsimplify(sp.expand(_s).coeff(x, _r)), chain(sp.nsimplify(_n), _r),
           "係数 = かけ算の鎖: n=%s r=%d" % (_n, _r))
# n が 0 以上の整数なら、nCr と一致し、r > n で 0 になる
for _n in range(0, 7):
    for _r in range(0, _n + 1):
        eq(chain(_n, _r), sp.binomial(_n, _r), "nCr と一致: n=%d r=%d" % (_n, _r))
    for _r in range(_n + 1, _n + 4):
        eq(chain(_n, _r), 0, "r>n で 0 になる: n=%d r=%d" % (_n, _r))
# n が分数・負なら、鎖に 0 が現れない（= 展開が終わらない）
for _n in [R(1, 2), R(1, 3), R(-1, 2), -1, -3, -4]:
    for _r in range(0, 30):
        chk(sp.nsimplify(_n) - _r != 0, "因数が 0 にならない: n=%s r=%d" % (_n, _r))
        ne(chain(sp.nsimplify(_n), _r), 0, "係数が 0 でない: n=%s r=%d" % (_n, _r))
# となり合う項の比は (n-r)/(r+1) x で、r→∞ で -x
_n, _r = sp.symbols("n r")
eq(sp.simplify(chain(_n, 3) / chain(_n, 2)), (_n - 2) / 3, "比 (n-r)/(r+1)")
chk(sp.limit((_n - _r) / (_r + 1), _r, sp.oo) == -1, "比の係数は -1 に近づく")

# ══════════════════════════════════════════════════════════
# 1. The idea の数値
# ══════════════════════════════════════════════════════════
eq((1 + x) ** 3, 1 + 3 * x + 3 * x ** 2 + x ** 3, "§1 (1+x)^3")
eq(chain(3, 4), 0, "§1 n=3 では 4 番目の因数で 0")
eq(chain(3, 3), 1, "§1 x^3 の係数は 1")
eq(chain(-3, 2), 6, "§2 例：n=-3 の x^2 の係数")
eq(chain(-3, 3), -10, "§2 例：n=-3 の x^3 の係数")
# 第 4 節（n = -1）
eq(series_of((1 + x) ** -1, 4), 1 - x + x ** 2 - x ** 3, "§4 (1+x)^-1")
eq(1 / (1 - (-x)), 1 / (1 + x), "§4 等比級数の和 = 1/(1+x)")
for _r in range(6):
    eq(chain(-1, _r), (-1) ** _r, "§4 n=-1 の係数は (-1)^r: r=%d" % _r)
# 第 5 節（n = 1/2）
eq(series_of((1 + x) ** R(1, 2), 4),
   1 + x / 2 - x ** 2 / 8 + x ** 3 / 16, "§5 sqrt(1+x)")
eq(chain(R(1, 2), 2), R(-1, 8), "§5 x^2 の係数は -1/8")
eq(chain(R(1, 2), 3), R(1, 16), "§5 x^3 の係数は 1/16")
chk([sp.sign(chain(R(1, 2), _r)) for _r in range(4)] == [1, 1, -1, 1],
    "§5 符号は +,+,-,+ で交互ではない")
# 第 6 節（くくり出し）
eq(series_of((2 + x) ** -1, 3), R(1, 2) - x / 4 + x ** 2 / 8, "§6 (2+x)^-1")
eq(sp.Integer(2) ** -1, R(1, 2), "§6 2^-1 = 1/2")
_a, _b, _n2 = sp.symbols("a b n", positive=True)
eq((_a * (1 + _b / _a)) ** _n2, (_a + _b) ** _n2, "§6 くくり出しの恒等式")
# 第 7 節（近似）
_ap = 1 + R(4, 100) / 2 - (R(4, 100)) ** 2 / 8
eq(_ap, R(10198, 10000), "§7 sqrt(1.04) の近似は 1.0198")
chk(abs(float(_ap) - float(sp.sqrt(R(104, 100)))) < 5e-6, "§7 真の値との差が小さい")
eq((R(4, 100)) ** 3 / 16, R(4, 1000000), "§7 次の項は 0.000004")

# ══════════════════════════════════════════════════════════
# 2. Why it works
# ══════════════════════════════════════════════════════════
for _m in range(1, 8):
    for _k in range(0, _m + 1):
        eq(sp.binomial(_m, _k),
           sp.prod([_m - _i for _i in range(_k)]) / F(_k),
           "nCr の約分した形: n=%d r=%d" % (_m, _k))

# ══════════════════════════════════════════════════════════
# 3. 例題 1（(1+x)^-3）
# ══════════════════════════════════════════════════════════
eq(series_of((1 + x) ** -3, 4),
   1 - 3 * x + 6 * x ** 2 - 10 * x ** 3, "例題1(a)")
eq(sp.Integer(-3) * -4 / F(2), 6, "(-3)(-4)/2! = 6")
eq(sp.Integer(-3) * -4 * -5 / F(3), -10, "(-3)(-4)(-5)/3! = -10")
eq(chain(-3, 4), 15, "次の項の係数は 15")
# 検算：(1+x)^-1 × (1+x)^-2
_p1 = series_of((1 + x) ** -1, 4)
_p2 = series_of((1 + x) ** -2, 4)
eq(_p2, 1 - 2 * x + 3 * x ** 2 - 4 * x ** 3, "(1+x)^-2 の展開")
_pr = sp.expand(_p1 * _p2)
eq(sp.nsimplify(_pr.coeff(x, 2)), 6, "積の x^2 の係数は 6")
eq(sp.nsimplify(_pr.coeff(x, 3)), -10, "積の x^3 の係数は -10")
eq(3 + 2 + 1, 6, "3+2+1 = 6")
eq(-4 - 3 - 2 - 1, -10, "-4-3-2-1 = -10")
# 検算（数で）
chk(abs(float(sp.Rational(11, 10) ** -3) - 0.75131) < 1e-5, "(1.1)^-3 = 0.75131...")
eq(1 - R(3, 10) + R(6, 100) - R(1, 100), R(3, 4), "部分和は 0.75")
chk(abs(float(sp.Rational(11, 10) ** -3) - 0.75) < 0.0015 + 1e-6,
    "差は次の項 15x^4 = 0.0015 の大きさ")
eq(15 * R(1, 10) ** 4, R(15, 10000), "15x^4 = 0.0015")

# ══════════════════════════════════════════════════════════
# 4. 例題 2（(1-2x)^(1/2)）
# ══════════════════════════════════════════════════════════
eq(series_of((1 - 2 * x) ** R(1, 2), 3), 1 - x - x ** 2 / 2, "例題2(a)")
eq((-2 * x) ** 2, 4 * x ** 2, "(-2x)^2 = 4x^2")
eq(R(4, 8), R(1, 2), "4/8 = 1/2")
# 範囲
chk(sp.solve(sp.Abs(-2 * x) < 1, x) == sp.And(-R(1, 2) < x, x < R(1, 2)),
    "|−2x|<1 は |x|<1/2")
# 検算：2 乗して 1-2x に戻る（x^2 まで）
_sq = sp.expand((1 - x - x ** 2 / 2) ** 2)
eq(sp.nsimplify(_sq.coeff(x, 0)), 1, "2 乗の定数項は 1")
eq(sp.nsimplify(_sq.coeff(x, 1)), -2, "2 乗の x の係数は -2")
eq(sp.nsimplify(_sq.coeff(x, 2)), 0, "2 乗の x^2 の係数は 0")
eq(_sq, 1 - 2 * x + x ** 3 + x ** 4 / 4, "2 乗の残りは x^3 と x^4")
# 検算（数で）
chk(abs(float(sp.sqrt(R(8, 10))) - 0.89442) < 1e-5, "sqrt(0.8) = 0.89442...")
eq(1 - R(1, 10) - R(5, 1000), R(895, 1000), "部分和は 0.895")

# ══════════════════════════════════════════════════════════
# 5. 例題 3（(4+x)^(-1/2)）
# ══════════════════════════════════════════════════════════
eq(sp.Integer(4) ** R(-1, 2), R(1, 2), "4^(-1/2) = 1/2")
eq(chain(R(-1, 2), 2), R(3, 8), "(1+u)^(-1/2) の u^2 の係数は 3/8")
eq(series_of((1 + u) ** R(-1, 2), 3, u), 1 - u / 2 + 3 * u ** 2 / 8,
   "(1+u)^(-1/2)")
eq(series_of((4 + x) ** R(-1, 2), 3),
   R(1, 2) - x / 16 + 3 * x ** 2 / 256, "例題3(b)")
eq(R(3, 8) * R(1, 16), R(3, 128), "3/8 × 1/16 = 3/128")
# 検算：2 乗して (4+x)^-1 に戻る
_sq3 = sp.expand((R(1, 2) - x / 16 + 3 * x ** 2 / 256) ** 2)
_t3 = series_of((4 + x) ** -1, 3)
eq(_t3, R(1, 4) - x / 16 + x ** 2 / 64, "(4+x)^-1 の展開")
for _k in range(3):
    eq(sp.nsimplify(_sq3.coeff(x, _k)), sp.nsimplify(sp.expand(_t3).coeff(x, _k)),
       "2 乗が (4+x)^-1 と一致: x^%d" % _k)
eq(R(3, 256) + R(1, 256), R(1, 64), "3/256 + 1/256 = 1/64")
# 検算（数で）
chk(abs(float((R(44, 10)) ** R(-1, 2)) - 0.47673) < 1e-5, "(4.4)^(-1/2)")
eq(R(5, 10) - R(25, 1000) + 3 * R(16, 100) / 256,
   R(476875, 1000000), "部分和は 0.476875")
# 誤答
ne(R(1, 4), R(1, 2), "4^(-1/2) は 1/4 ではない")
ne(-2, R(1, 2), "4^(-1/2) は -2 ではない")

# ══════════════════════════════════════════════════════════
# 6. 例題 4（(1+x)^(1/3) と近似）
# ══════════════════════════════════════════════════════════
eq(series_of((1 + x) ** R(1, 3), 3), 1 + x / 3 - x ** 2 / 9, "例題4(a)")
eq(chain(R(1, 3), 2), R(-1, 9), "x^2 の係数は -1/9")
eq(chain(R(1, 3), 3), R(5, 81), "x^3 の係数は 5/81")
_a4 = 1 + R(3, 100) / 3 - (R(3, 100)) ** 2 / 9
eq(_a4, R(10099, 10000), "例題4(b) 1.0099")
chk(abs(float(_a4) - float(R(103, 100) ** R(1, 3))) < 2e-6, "真の値との差は 0.000002 ほど")
chk(abs(float(_a4 ** 3) - 1.03) < 6e-6, "3 乗すると 1.03 に近い")
chk(abs(float(_a4 ** 3) - 1.029995) < 1e-6, "3 乗は 1.029995...")
eq(R(5, 81) * (R(3, 100)) ** 3, R(5 * 27, 81 * 1000000), "次の項の大きさ")
chk(abs(float(R(5, 81) * (R(3, 100)) ** 3) - 0.0000017) < 1e-7, "次の項は 0.0000017 ほど")
# 誤答：x^2 の係数を +1/9 にする
_w4 = 1 + R(3, 100) / 3 + (R(3, 100)) ** 2 / 9
eq(_w4, R(10101, 10000), "誤答は 1.0101")
chk(abs(float(_w4 ** 3) - 1.0306) < 1e-4, "その 3 乗は 1.0306 ほど")
ne(_w4, _a4, "誤答は合わない")
# (c) x = 3 は範囲外
chk(abs(3) >= 1, "x = 3 は |x| < 1 を満たさない")

# ══════════════════════════════════════════════════════════
# 7. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(series_of((1 + x) ** -4, 4),
   1 - 4 * x + 10 * x ** 2 - 20 * x ** 3, "演習1")
eq(sp.Integer(-4) * -5 / F(2), 10, "(-4)(-5)/2! = 10")
eq(sp.Integer(-4) * -5 * -6 / F(3), -20, "(-4)(-5)(-6)/3! = -20")
_sq1 = sp.expand(_p2 ** 2)
for _k, _v in [(1, -4), (2, 10), (3, -20)]:
    eq(sp.nsimplify(_sq1.coeff(x, _k)), _v, "((1+x)^-2)^2 の x^%d" % _k)
eq(2 * 3 + 4, 10, "6+4 = 10")
eq(-8 - 12, -20, "-8-12 = -20")
chk([sp.sign(chain(-4, _r)) for _r in range(4)] == [1, -1, 1, -1],
    "n が負の整数なら符号は交互")
chk([sp.sign(chain(R(1, 2), _r)) for _r in range(4)] != [1, -1, 1, -1],
    "n が分数なら交互ではない")

eq(series_of((1 + x) ** R(1, 4), 3), 1 + x / 4 - 3 * x ** 2 / 32, "演習2")
eq(chain(R(1, 4), 2), R(-3, 32), "1/4 の鎖から -3/32")
chk(abs(float(R(11, 10) ** R(1, 4)) - 1.024114) < 1e-6, "1.1^(1/4)")
eq(1 + R(25, 1000) - 3 * R(1, 100) / 32, R(10240625, 10000000), "部分和 1.0240625")
chk(abs(float(R(11, 10) ** R(1, 4)) - 1.0240625) < 1e-4, "近い")

eq(series_of((1 - 3 * x) ** -1, 3), 1 + 3 * x + 9 * x ** 2, "演習3")
eq((-3 * x) ** 2, 9 * x ** 2, "(-3x)^2 = 9x^2")
for _r in range(5):
    eq(sp.nsimplify(series_of((1 - 3 * x) ** -1, 5).coeff(x, _r)), 3 ** _r,
       "等比：公比 3x の項: r=%d" % _r)
chk(all(sp.nsimplify(series_of((1 - 3 * x) ** -1, 5).coeff(x, _r)) > 0
        for _r in range(5)), "演習3 の係数はすべて正")

eq(series_of((1 + 2 * x) ** -3, 3), 1 - 6 * x + 24 * x ** 2, "演習4")
eq(6 * (2 * x) ** 2, 24 * x ** 2, "6(2x)^2 = 24x^2")
eq(1 - 6 * R(5, 100) + 24 * (R(5, 100)) ** 2, R(76, 100), "部分和 0.76")
chk(abs(float(R(11, 10) ** -3) - 0.75131) < 1e-5, "(1.1)^-3")
eq(-10 * (2 * R(5, 100)) ** 3, R(-1, 100), "次の項は -0.01")
eq(1 - 6 * R(5, 100) + 12 * (R(5, 100)) ** 2, R(73, 100), "誤答は 0.73")
ne(R(73, 100), R(76, 100), "その誤答は合わない")

eq(sp.Integer(9) ** R(1, 2), 3, "9^(1/2) = 3")
eq(series_of((9 + x) ** R(1, 2), 3), 3 + x / 6 - x ** 2 / 216, "演習5")
eq(3 * R(1, 2) * R(1, 9), R(1, 6), "3 × 1/2 × 1/9 = 1/6")
eq(3 * R(-1, 8) * R(1, 81), R(-1, 216), "3 × (-1/8) × 1/81 = -1/216")
_sq5 = sp.expand((3 + x / 6 - x ** 2 / 216) ** 2)
eq(sp.nsimplify(_sq5.coeff(x, 0)), 9, "2 乗の定数項は 9")
eq(sp.nsimplify(_sq5.coeff(x, 1)), 1, "2 乗の x の係数は 1")
eq(sp.nsimplify(_sq5.coeff(x, 2)), 0, "2 乗の x^2 の係数は 0")
ne(R(9, 2), 3, "9^(1/2) は 9/2 ではない")

eq(sp.Integer(2) ** -2, R(1, 4), "2^-2 = 1/4")
eq(series_of((2 - x) ** -2, 3), R(1, 4) + x / 4 + 3 * x ** 2 / 16, "演習6")
eq(series_of((1 + u) ** -2, 3, u), 1 - 2 * u + 3 * u ** 2, "(1+u)^-2")
eq((-2) * (-x / 2), x, "-2u = x")
eq(3 * (-x / 2) ** 2, 3 * x ** 2 / 4, "3u^2 = 3x^2/4")
eq(R(1, 4) + R(5, 100) + 3 * R(4, 100) / 16, R(3075, 10000), "部分和 0.3075")
chk(abs(float((R(18, 10)) ** -2) - 0.308641) < 1e-6, "(1.8)^-2")
eq(R(1, 4) * 4 * (R(2, 10) / 2) ** 3, R(1, 1000), "次の項は 0.001")
ne(R(1, 2), R(1, 4), "2^-2 は 1/2 ではない")

_q7 = 1 + R(8, 100) / 2 - (R(8, 100)) ** 2 / 8
eq(_q7, R(10392, 10000), "演習7 1.0392")
chk(abs(float(_q7) - float(sp.sqrt(R(108, 100)))) < 4e-5, "真の値に近い")
chk(abs(float(_q7 ** 2) - 1.08) < 8e-5, "2 乗すると 1.08 に近い")
chk(abs(float(_q7 ** 2) - 1.07993) < 1e-5, "2 乗は 1.07993...")
eq((R(8, 100)) ** 3 / 16, R(32, 1000000), "次の項は 0.000032")
chk(round(float(_q7), 4) == 1.0392, "小数第 4 位まで 1.0392")
chk(round(float(sp.sqrt(R(108, 100))), 4) == 1.0392, "真の値も 1.0392")

eq(series_of((1 - x) ** -1, 5), 1 + x + x ** 2 + x ** 3 + x ** 4, "演習8")
for _r in range(5):
    eq(sp.nsimplify(series_of((1 - x) ** -1, 5).coeff(x, _r)), 1,
       "演習8 の係数はすべて 1: r=%d" % _r)
eq(1 / (1 - x), (1 - x) ** -1, "S∞ = u1/(1-r) がもとの式に戻る")
ne(1 / (1 + x), 1 / (1 - x), "r = -x としたら別の式")
chk(abs(float(1 / (1 - R(1, 2))) - 2) < 1e-9, "x=0.5 で 1/(1-x) = 2")
chk(abs(float(1 / (1 + R(1, 2))) - sp.Rational(2, 3)) < 1e-9, "x=0.5 で 1/(1+x) = 0.67")

eq(sp.Integer(9) ** R(-1, 2), R(1, 3), "9^(-1/2) = 1/3")
eq(series_of((9 - 2 * x) ** R(-1, 2), 3),
   R(1, 3) + x / 27 + x ** 2 / 162, "演習9")
eq(-(-2 * x / 9) / 2, x / 9, "-u/2 = x/9")
eq(R(3, 8) * (-2 * x / 9) ** 2, x ** 2 / 54, "3u^2/8 = x^2/54")
_sq9 = sp.expand((R(1, 3) + x / 27 + x ** 2 / 162) ** 2)
_t9 = series_of((9 - 2 * x) ** -1, 3)
eq(_t9, R(1, 9) + 2 * x / 81 + 4 * x ** 2 / 729, "(9-2x)^-1 の展開")
for _k in range(3):
    eq(sp.nsimplify(_sq9.coeff(x, _k)), sp.nsimplify(sp.expand(_t9).coeff(x, _k)),
       "演習9 の 2 乗が一致: x^%d" % _k)
eq(R(1, 243) + R(1, 729), R(4, 729), "1/243 + 1/729 = 4/729")
eq(2 * R(1, 3) * R(1, 162), R(1, 243), "2 × 1/3 × 1/162 = 1/243")
eq((R(1, 27)) ** 2, R(1, 729), "(1/27)^2 = 1/729")
ne(9, R(9, 2), "|x|<9 ではなく |x|<9/2")

eq(series_of((1 - x) ** -2, 4),
   1 + 2 * x + 3 * x ** 2 + 4 * x ** 3, "演習10 の展開は正しい")
chk(all(sp.nsimplify(series_of((1 - x) ** -2, 5).coeff(x, _r)) > 0
        for _r in range(5)), "演習10 の係数はすべて正")
chk(abs(float((R(9, 10)) ** -2) - 1.234568) < 1e-6, "(0.9)^-2 = 1.2345...")
eq(1 + R(2, 10) + R(3, 100) + R(4, 1000), R(1234, 1000), "部分和 1.234")
chk(abs(1) >= 1, "x = 1 は |x| < 1 を満たさない")

# ══════════════════════════════════════════════════════════
# 8. 公式集とシラバス（逐語）
# ══════════════════════════════════════════════════════════
in_text("公式集の **1.10** の欄に、次の形で印刷されています。", "公式集にある")
in_text("> Extension of binomial theorem, $n \\in \\mathbb{Q}$", "見出しを逐語で")
in_text("> $(a+b)^{n} = a^{n}\\left(1 + n\\left(\\dfrac{b}{a}\\right)"
        " + \\dfrac{n(n-1)}{2!}\\left(\\dfrac{b}{a}\\right)^{2} + \\ldots\\right)$",
        "公式集の式を逐語で")
in_text("> Not required: Proof of binomial theorem.", "Not required を逐語で")
in_text("> $(a + b)^{n} = \\left(a\\left(1 + \\dfrac{b}{a}\\right)\\right)^{n}"
        " = a^{n}\\left(1 + \\dfrac{b}{a}\\right)^{n}$, $n \\in \\mathbb{Q}$",
        "Guidance のくくり出しを逐語で")
in_text("## 範囲は、公式集にありません", "範囲は公式集にないと書く")
not_in_text("## 参考：この項目のシラバス（原文）", "末尾のシラバスは置かない")

# ══════════════════════════════════════════════════════════
# 9. GDC
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h for h in _tips
        if not h.startswith("解説") and h != "クリックすると開きます"]
chk(len(_gdc) == 1, "GDC の折りたたみは 1 つ: %s" % _gdc)
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")
in_text("**Paper 1 では使えません。**", "Paper 1 では手で解くと明記")
for _m in ["Casio", "fx-CG50", "TI-84", "OPTN", "PRB", "nDeriv", "taylor("]:
    not_in_text(_m, "TI-Nspire 以外の機種・確かめていない機能: " + _m)

# ══════════════════════════════════════════════════════════
# 10. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 4, "model-answer が 4")
chk(len(re.findall(r"^::: \{#exm-aahl110b-", TEXT, re.M)) == 4, "例題が 4")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例が 14")
chk("## 解答例（答案用紙にはこう書く）" not in TEXT, "解答例の見出しをそろえた")
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
    chk(_r0 == "aahl110b", "他ページの @-ref: " + _r0)
for _href in re.findall(r"\]\(([^)]+\.qmd[^)]*)\)", TEXT):
    _p = os.path.normpath(os.path.join(os.path.dirname(QMD),
                                       _href.split("#")[0]))
    chk(os.path.exists(_p), "リンク先のページがない: " + _href)
chk(len(re.findall(r"\]\(\.\./\.\./aa-sl/", TEXT)) >= 4,
    "AA SL へのリンクが 4 本以上ある")
chk(len(re.findall(r"\]\(aahl-1-10a\.qmd", TEXT)) >= 2,
    "HL 1.10a へのリンクがある")
chk(not re.search(r"SL [0-9.]+[ab]? の第 \d+ 節", TEXT.replace(
    "[SL 1.9 第 6 節]", "")), "SL を節番号で呼んでいない（1 か所の例外を除く）")
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

# ══════════════════════════════════════════════════════════
# 11. Why it works は折りたたむ
# ══════════════════════════════════════════════════════════
_i = TEXT.index(chr(10) + "## Why it works" + chr(10))
_j = TEXT.index(chr(10) + "## Worked examples", _i)
_wiw = TEXT[_i:_j]
chk('collapse="true"}' + chr(10) + "## クリックすると開きます" in _wiw,
    "Why it works は折りたたんである")
chk(_wiw.rstrip().endswith(":::"), "折りたたみが閉じてある")
chk(_wiw.count("クリックすると開きます") == 1, "折りたたみは 1 つだけ")

# ══════════════════════════════════════════════════════════
# 12. 節の見出し
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
in_text("### 1. Expansions that stop and expansions that do "
        "not（終わる展開と、終わらない展開） {#finite-or-not}", "見出し 1")
in_text("### 2. The extended binomial theorem（一般の $n$ での展開） "
        "{#formula}", "見出し 2")
in_text("### 3. Validity: where the expansion may be used（展開が使える範囲） "
        "{#validity}", "見出し 3")
in_text("### 4. Negative indices: the link with geometric "
        "series（負の指数：等比級数とのつながり） {#negative}", "見出し 4")
in_text("### 5. Fractional indices: expanding a square "
        "root（分数の指数：平方根を展開する） {#fractional}", "見出し 5")
in_text("### 6. $(a+b)^{n}$: taking out $a^{n}$（$a^{n}$ をくくり出す） "
        "{#factor}", "見出し 6")
in_text("### 7. Using the expansion to approximate（近似に使う） "
        "{#approximation}", "見出し 7")

# ══════════════════════════════════════════════════════════
# 13. 図
# ══════════════════════════════════════════════════════════
SVG_A = os.path.join(BASE, "img", "aahl-1-10b-idea-a.svg")
SVG_B = os.path.join(BASE, "img", "aahl-1-10b-idea-b.svg")
chk(os.path.exists(SVG_A), "図 (a) がある")
chk(os.path.exists(SVG_B), "図 (b) がある")
chk("](img/aahl-1-10b-idea-a.svg)" in TEXT, "本文が図 (a) を貼っている")
chk("](img/aahl-1-10b-idea-b.svg)" in TEXT, "本文が図 (b) を貼っている")
for _s in glob.glob(os.path.join(BASE, "img", "*.png")):
    chk(False, "PNG が残っている: " + os.path.basename(_s))
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("The chain of factors", "図(a) の題")
in_fig("a factor of $0$ arrives, so the expansion stops", "図(a) の要点")
in_fig("no factor is ever $0$, so the expansion never stops", "図(a) の要点")
in_fig("$(1+x)^{-1}$ and its partial sums", "図(b) の題")
in_fig("$|x| < 1$", "図(b) の帯")
in_text("上の鎖に $0$ が現れるかどうかで、展開が終わるかどうかが決まります。",
        "キャプションが (a) を説明")
in_text("色の付いた帯の中でだけ、部分和が曲線に近づきます。",
        "キャプションが (b) を説明")
# 図の値が本文と合っている
chk([3, 2, 1, 0] == [3 - _k for _k in range(4)], "図(a) の n=3 の鎖")
chk([R(1, 2) - _k for _k in range(4)] == [R(1, 2), R(-1, 2), R(-3, 2), R(-5, 2)],
    "図(a) の n=1/2 の鎖")
# 図が例題・演習の答えを載せていないか
for leak in ["10392", "1.0392", "1.0099", "1.00990", "0.476875", "0.895",
             "24x", "-20x", "3x^{2}/32", "162", "216", "256", "128"]:
    chk(leak not in FIGSTR, "図が例題・演習の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 14. 演習の答えが、本文・例題に出ていないか
# ══════════════════════════════════════════════════════════
_BODY = TEXT[:TEXT.index("## Exercises")]
for leak, where in [("1.0392", "演習7"), ("20x^{3}", "演習1"),
                    ("3x^{2}}{32}", "演習2"), ("24x^{2}", "演習4"),
                    ("x^{2}}{216}", "演習5"), ("3x^{2}}{16}", "演習6"),
                    ("x^{2}}{162}", "演習9")]:
    chk(leak not in _BODY, "%s の答えが本文・例題に出ている: %s" % (where, leak))

# ══════════════════════════════════════════════════════════
# 15. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-hl/01-number-and-algebra/aahl-1-10b.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aahl-1-10a.qmd") < DRAFT.index("aahl-1-10b.qmd"),
    "サイドバーの並びが 1.10a → 1.10b")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aahl" not in PUB, "公開用には入れない")
IDX = open(os.path.join(ROOT, "aa-hl", "index.qmd"), encoding="utf-8").read()
chk("(01-number-and-algebra/aahl-1-10b.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-hl", "*", "aahl-*.qmd")))
_ticked = re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written),
    "✅ %d と ページ %d" % (len(_ticked), len(_written)))
_rows = re.findall(r"^\| \*\*HL [0-9.]+[abc]?\*\* \|", IDX, re.M)
chk(len(_rows) == 35, "一覧は 35 行: %d" % len(_rows))
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
chk(_mm is not None and int(_mm.group(2)) == 35, "「全 35 ページ」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for t in ["| valid |", "| ascending powers |", "| approximation |",
          "| terminate |", "| partial sum |", "| convergent |",
          "| rational exponent |"]:
    chk(t in GLO, "対訳表にある: " + t)
PLAN = open(os.path.join(ROOT, "_AA-HL-PLAN.md"), encoding="utf-8").read()
# 進捗は、書き上がったページ数から動的に見る（ページを足すたびに
# 直さずにすむように）。
_pm = re.search(r"\*\*(\d+) / 35 ページ。\*\*", PLAN)
chk(_pm is not None and int(_pm.group(1)) == len(_written),
    "PLAN の進捗がページ数と合っている")

# ══════════════════════════════════════════════════════════
# 16. 見張り（設計判断が戻っていないか）
# ══════════════════════════════════════════════════════════
in_text("**$\\lvert x \\rvert = 1$ は、$n$ によって変わります。** この本では扱いません。",
        "|x|=1 を言い切っていない")
not_in_text("$\\lvert x \\rvert \\geq 1$ では使えません", "旧：言い切り")
in_text("**$n$ が分数や負の数なら、$n - r = 0$ になる $0$ 以上の整数 $r$ がありません。**",
        "終わらない理由")
in_text("$n!$ が消えたことが要です。", "Why it works の要点")
in_text("ただし**これは $n$ が負の整数のときの話**で、$n$ が分数のときは当てはまりません。",
        "符号が交互になる条件を限定")
in_text("**負の符号があるから交互になる、とはかぎりません。**", "演習3 の注意")
in_text("**$2$ 乗のほうは、$-\\frac{1}{2}$ 乗の計算をまったく使っていません。**",
        "検算が独立であることを書いている")
chk(TEXT.count("まったく使っていません") >= 3, "独立な道すじだと明示している")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
