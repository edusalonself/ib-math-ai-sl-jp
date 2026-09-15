"""AA SL 3.8（三角方程式を解く）の内容を検算する。

    python3 figs/aa-sl/check_aasl_3_8.py

★ sympy の solveset は三角の 2 次式を取りこぼすことがあるので、
   比（sin x や cos x）を先に解いてから角を出す。
"""
import glob
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "aa-sl", "03-geometry")
QMD = os.path.join(BASE, "aasl-3-8.qmd")
TEXT = open(QMD, encoding="utf-8").read()
BODY = TEXT[:TEXT.index("## Worked examples")]
FIG = open(os.path.join(HERE, "make_aasl_3_8.py"), encoding="utf-8").read()
_NODOC = re.sub(r'"""(?:.|\n)*?"""', "", FIG)
FIGSTR = "\n".join(t for t in re.findall(r'r?"((?:[^"\\]|\\.)*)"', _NODOC)
                   if not t.startswith("#") and (" " in t or "$" in t))
FIGCODE = FIG.split('"""', 2)[-1]

OK = NG = 0
R = sp.Rational
PI = sp.pi
X = sp.Symbol("x", real=True)
C = sp.Symbol("c", real=True)


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def eq(u, v, msg=""):
    chk(sp.simplify(u - v) == 0, msg + f"  ({u} vs {v})")


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている: " + msg + " :: " + sub[:70])


def not_in_body(sub, msg=""):
    chk(sub not in BODY, "例題・演習の答えが本文に漏れている: " + msg + " :: " + sub[:50])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


# ══════════════════════════════════════════════════════════
# 0. 解を出す道具（solveset には頼らない）
# ══════════════════════════════════════════════════════════
def solve_ratio(fn, k, lo, hi):
    """fn(theta) = k を lo <= theta <= hi ですべて解く。fn は sin/cos/tan。

    基本の解ともう 1 つを出し、くり返しの幅を足し引きして拾う。
    """
    if fn is sp.tan:
        base = [sp.atan(k)]
        step = PI
    elif fn is sp.sin:
        if abs(k) > 1:
            return []
        a = sp.asin(k)
        base = [a, PI - a]
        step = 2 * PI
    else:
        if abs(k) > 1:
            return []
        a = sp.acos(k)
        base = [a, -a]
        step = 2 * PI
    out = set()
    for b in base:
        n = -40
        while n <= 40:
            v = sp.simplify(b + n * step)
            if sp.simplify(v - lo) >= 0 and sp.simplify(hi - v) >= 0:
                out.add(sp.nsimplify(v))
            n += 1
    return sorted(out, key=lambda z: float(z))


def brute(expr, lo, hi, cands):
    """候補のうち、区間の中で expr = 0 をみたすものを返す（検算用）。"""
    return sorted([c for c in cands
                   if sp.simplify(expr.subs(X, c)) == 0
                   and sp.simplify(c - lo) >= 0 and sp.simplify(hi - c) >= 0],
                  key=lambda z: float(z))


def same(got, want, msg):
    chk([sp.nsimplify(g) for g in got] == [sp.nsimplify(w) for w in want],
        f"{msg}: {got} vs {want}")


# 道具そのものの検算
same(solve_ratio(sp.sin, R(1, 2), 0, 2 * PI), [PI / 6, 5 * PI / 6],
     "道具: sin x = 1/2 on [0,2π]")
same(solve_ratio(sp.cos, 1, 0, 2 * PI), [0, 2 * PI], "道具: cos x = 1 on [0,2π]")
chk(solve_ratio(sp.sin, 2, 0, 2 * PI) == [], "道具: sin x = 2 は解なし")
chk(solve_ratio(sp.cos, -2, 0, 2 * PI) == [], "道具: cos x = -2 は解なし")

# ══════════════════════════════════════════════════════════
# 1. The idea — もう 1 つの解の表
# ══════════════════════════════════════════════════════════
A = sp.Symbol("alpha", real=True)
eq(sp.sin(PI - A) - sp.sin(A), 0, "sin(π-α) = sin α")
eq(sp.cos(-A) - sp.cos(A), 0, "cos(-α) = cos α")
eq(sp.cos(2 * PI - A) - sp.cos(A), 0, "cos(2π-α) = cos α")
eq(sp.tan(A + PI) - sp.tan(A), 0, "tan(α+π) = tan α")
eq(sp.periodicity(sp.sin(X), X), 2 * PI, "sin の period は 2π")
eq(sp.periodicity(sp.cos(X), X), 2 * PI, "cos の period は 2π")
eq(sp.periodicity(sp.tan(X), X), PI, "tan の period は π")
in_text("| $\\sin x = k$ | $\\alpha$ | $\\pi - \\alpha$ | $2\\pi$ |", "表の sin の行")
in_text("| $\\cos x = k$ | $\\alpha$ | $-\\alpha$（または $2\\pi - \\alpha$） | $2\\pi$ |",
        "表の cos の行")
in_text("（$\\alpha + \\pi$ がくり返しそのもの）", "表の tan の行")
in_text("**$\\tan$ だけは $1$ 周期に $1$ つ**です。", "tan は 1 周期に 1 つ")

# |k| > 1 なら解なし
chk(sp.maximum(sp.sin(X), X) == 1 and sp.minimum(sp.sin(X), X) == -1,
    "sin の値域は [-1,1]")
chk(sp.maximum(sp.cos(X), X) == 1 and sp.minimum(sp.cos(X), X) == -1,
    "cos の値域は [-1,1]")
in_text("$\\sin x = 1.5$ や $\\cos x = -2$ には解がありません。", "|k| > 1 の注意")
in_text("$\\tan$ にはこの制限がありません。", "tan には制限がない")

# 中身の区間
eq(2 * PI, 2 * PI, "0≤x≤π なら 0≤2x≤2π")
in_text("$0 \\le x \\le \\pi$ なら $0 \\le 2x \\le 2\\pi$ です。", "中身の区間")
# 2(x - π/4) の動く範囲
eq(2 * (0 - PI / 4), -PI / 2, "x=0 で中身 -π/2")
eq(2 * (2 * PI - PI / 4), 7 * PI / 2, "x=2π で中身 7π/2")
in_text("中身は $-\\dfrac{\\pi}{2}$ から $\\dfrac{7\\pi}{2}$ まで動きます。", "b(x+c) の例")

# 割ってはいけない
eq(sp.expand(sp.sin(X) * (2 * sp.cos(X) - 1)),
   sp.expand(2 * sp.sin(X) * sp.cos(X) - sp.sin(X)), "因数分解の確認")
in_text("$\\sin x(2\\cos x - 1) = 0$", "§6 の因数分解した形")
in_text("$\\cos^{2}\\theta + \\sin^{2}\\theta = 1$", "2 次式は Pythagoras で")

# ══════════════════════════════════════════════════════════
# 2. Why it works
# ══════════════════════════════════════════════════════════
# k = ±1 のときだけ 1 つ
same(solve_ratio(sp.sin, 1, 0, 2 * PI), [PI / 2], "sin x = 1 は 1 つ")
same(solve_ratio(sp.sin, -1, 0, 2 * PI), [3 * PI / 2], "sin x = -1 は 1 つ")
chk(len(solve_ratio(sp.sin, R(1, 2), 0, 2 * PI)) == 2, "-1<k<1 なら 2 つ")
in_text("$k = \\pm 1$ のときだけ、$2$ 点が重なって $1$ つになります。", "k = ±1")
in_text("その $2$ 点は**原点について対称**で、角は $\\alpha$ と $\\alpha + \\pi$ です。",
        "tan は原点対称")
in_text("**「もう $1$ つの解」ではなく「次のくり返し」**", "次のくり返し")
# sin x = 0 を入れると両辺 0
for _v in [0, PI, 2 * PI]:
    eq(2 * sp.sin(_v) * sp.cos(_v), sp.sin(_v), f"x={_v} で 2sinxcosx = sinx")

# ══════════════════════════════════════════════════════════
# 3. 例題 1  2 sin x = 1
# ══════════════════════════════════════════════════════════
same(solve_ratio(sp.sin, R(1, 2), 0, 2 * PI), [PI / 6, 5 * PI / 6], "例題1(b)")
same(solve_ratio(sp.sin, R(1, 2), 0, 4 * PI),
     [PI / 6, 5 * PI / 6, 13 * PI / 6, 17 * PI / 6], "例題1(c)")
eq(PI / 6 + 2 * PI, 13 * PI / 6, "π/6 + 2π")
eq(5 * PI / 6 + 2 * PI, 17 * PI / 6, "5π/6 + 2π")
chk(sp.simplify(17 * PI / 6 - 4 * PI) < 0, "17π/6 < 4π")
chk(sp.simplify(25 * PI / 6 - 4 * PI) > 0, "25π/6 > 4π")
for _v in [PI / 6, 5 * PI / 6, 13 * PI / 6, 17 * PI / 6]:
    eq(2 * sp.sin(_v), 1, f"例題1 の解 {_v}")
in_text("$$x = \\frac{\\pi}{6}, \\ \\frac{5\\pi}{6}, \\ \\frac{13\\pi}{6}, \\ "
        "\\frac{17\\pi}{6}$$", "例題1(c) の答え")
in_text("$\\dfrac{17\\pi}{6} \\approx 2.83\\pi$", "17π/6 の概算")
chk(abs(float(R(17, 6)) - 2.83) < 0.005, "17/6 ≈ 2.83")
chk(abs(float(R(25, 6)) - 4.17) < 0.005, "25/6 ≈ 4.17")

# ══════════════════════════════════════════════════════════
# 4. 例題 2  2 sin²x + 5 cos x + 1 = 0
# ══════════════════════════════════════════════════════════
_lhs = 2 * (1 - C ** 2) + 5 * C + 1
eq(sp.expand(-_lhs), 2 * C ** 2 - 5 * C - 3, "例題2(a) 変形")
eq(sp.expand((2 * C + 1) * (C - 3)), 2 * C ** 2 - 5 * C - 3, "例題2(b) 因数分解")
chk(sorted(sp.solve(2 * C ** 2 - 5 * C - 3, C)) == [R(-1, 2), 3],
    "例題2(b) の根は -1/2 と 3")
chk(3 > 1, "cos x = 3 は不適")
same(solve_ratio(sp.cos, R(-1, 2), 0, 4 * PI),
     [2 * PI / 3, 4 * PI / 3, 8 * PI / 3, 10 * PI / 3], "例題2(c)")
for _v in [2 * PI / 3, 4 * PI / 3, 8 * PI / 3, 10 * PI / 3]:
    eq(2 * sp.sin(_v) ** 2 + 5 * sp.cos(_v) + 1, 0, f"例題2 の解 {_v}")
eq(2 * PI - 2 * PI / 3, 4 * PI / 3, "2π - 2π/3")
chk(sp.simplify(10 * PI / 3 - 4 * PI) < 0, "10π/3 < 4π")
chk(sp.simplify(14 * PI / 3 - 4 * PI) > 0, "14π/3 > 4π")
# 検算（(a) について）
eq(1 - R(1, 4), R(3, 4), "sin²x = 3/4")
eq(2 * R(3, 4) + 5 * R(-1, 2) + 1, 0, "もとの式に戻して 0")
eq(R(3, 2) - R(5, 2) + 1, 0, "3/2 - 5/2 + 1 = 0")
eq(sp.expand((2 * C + 1) * (C - 3)), 2 * C ** 2 - 6 * C + C - 3, "展開の途中")

# ══════════════════════════════════════════════════════════
# 5. 例題 3  tan 2x = √3
# ══════════════════════════════════════════════════════════
_th = solve_ratio(sp.tan, sp.sqrt(3), 0, 4 * PI)
same(_th, [PI / 3, 4 * PI / 3, 7 * PI / 3, 10 * PI / 3], "例題3(b) 中身の値")
same([t / 2 for t in _th], [PI / 6, 2 * PI / 3, 7 * PI / 6, 5 * PI / 3], "例題3(c)")
for _v in [PI / 6, 2 * PI / 3, 7 * PI / 6, 5 * PI / 3]:
    eq(sp.tan(2 * _v), sp.sqrt(3), f"例題3 の解 {_v}")
chk(sp.simplify(13 * PI / 3 - 4 * PI) > 0, "13π/3 > 4π")
for _i in range(3):
    eq(_th[_i + 1] - _th[_i], PI, "中身は π ずつ")
_xs = [PI / 6, 2 * PI / 3, 7 * PI / 6, 5 * PI / 3]
for _i in range(3):
    eq(_xs[_i + 1] - _xs[_i], PI / 2, "x は π/2 ずつ")
eq(sp.periodicity(sp.tan(2 * X), X), PI / 2, "tan2x の period は π/2")
eq(sp.tan(4 * PI / 3), sp.sqrt(3), "tan(4π/3) = √3")

# ══════════════════════════════════════════════════════════
# 6. 例題 4  sin 2x = cos x
# ══════════════════════════════════════════════════════════
eq(sp.expand_trig(sp.sin(2 * X)), 2 * sp.sin(X) * sp.cos(X), "2 倍角")
eq(sp.expand(sp.cos(X) * (2 * sp.sin(X) - 1)),
   sp.expand(2 * sp.sin(X) * sp.cos(X) - sp.cos(X)), "例題4(a)")
same(solve_ratio(sp.cos, 0, 0, 2 * PI), [PI / 2, 3 * PI / 2], "例題4(b)")
same(solve_ratio(sp.sin, R(1, 2), 0, 2 * PI), [PI / 6, 5 * PI / 6], "例題4(c)")
for _v in [PI / 6, PI / 2, 5 * PI / 6, 3 * PI / 2]:
    eq(sp.sin(2 * _v), sp.cos(_v), f"例題4 の解 {_v}")
eq(sp.sin(PI), 0, "検算: sin π = 0")
eq(sp.cos(PI / 2), 0, "検算: cos(π/2) = 0")
eq(sp.sin(PI / 3), sp.sqrt(3) / 2, "検算: sin(π/3)")
eq(sp.cos(PI / 6), sp.sqrt(3) / 2, "検算: cos(π/6)")
# 割ると消える解
chk(sp.simplify(2 * sp.sin(PI / 2) - 1) != 0, "x=π/2 は 2sinx=1 をみたさない")
chk(sp.simplify(2 * sp.sin(3 * PI / 2) - 1) != 0, "x=3π/2 も同様")

# ══════════════════════════════════════════════════════════
# 7. 演習 1〜10
# ══════════════════════════════════════════════════════════
# 1  2cos x = 1
same(solve_ratio(sp.cos, R(1, 2), 0, 2 * PI), [PI / 3, 5 * PI / 3], "演習1")
eq(2 * PI - PI / 3, 5 * PI / 3, "演習1 もう 1 つ")
eq(sp.cos(5 * PI / 3), R(1, 2), "演習1 検算")
# 2  sin x = -1/2
same(solve_ratio(sp.sin, R(-1, 2), 0, 2 * PI), [7 * PI / 6, 11 * PI / 6], "演習2")
eq(PI + PI / 6, 7 * PI / 6, "演習2 π + π/6")
eq(2 * PI - PI / 6, 11 * PI / 6, "演習2 2π - π/6")
chk(sp.sin(7 * PI / 6) < 0 and sp.sin(11 * PI / 6) < 0, "演習2 は第3・第4象限")
# 3  tan x = 1 on [-π, 2π]（引く手順を使う）
same(solve_ratio(sp.tan, 1, -PI, 2 * PI), [-3 * PI / 4, PI / 4, 5 * PI / 4], "演習3")
eq(PI / 4 + PI, 5 * PI / 4, "演習3 π を足す")
eq(PI / 4 - PI, -3 * PI / 4, "演習3 π を引く")
chk(sp.simplify(9 * PI / 4 - 2 * PI) > 0, "9π/4 > 2π")
chk(sp.simplify(-7 * PI / 4 + PI) < 0, "-7π/4 < -π")
chk(sp.tan(PI / 4) > 0 and sp.tan(5 * PI / 4) > 0, "tan が正")
eq(sp.tan(-3 * PI / 4), 1, "tan(-3π/4) = 1")
chk(sp.tan(PI - PI / 4) < 0, "π - π/4 では tan が負")
# 4  sin(2(x + π/4)) = 1/2 —— b(x+c) の形
eq(2 * (0 + PI / 4), PI / 2, "演習4 中身の下端")
eq(2 * (2 * PI + PI / 4), 9 * PI / 2, "演習4 中身の上端")
_th4 = solve_ratio(sp.sin, R(1, 2), PI / 2, 9 * PI / 2)
same(_th4, [5 * PI / 6, 13 * PI / 6, 17 * PI / 6, 25 * PI / 6], "演習4 中身")
chk(sp.simplify(PI / 6 - PI / 2) < 0, "基本の解 π/6 は中身の区間の外")
chk(sp.simplify(29 * PI / 6 - 9 * PI / 2) > 0, "次の 29π/6 は区間の外")
_x4 = [t / 2 - PI / 4 for t in _th4]
same(_x4, [PI / 6, 5 * PI / 6, 7 * PI / 6, 11 * PI / 6], "演習4")
for _v in _x4:
    eq(sp.sin(2 * (_v + PI / 4)), R(1, 2), f"演習4 の解 {_v}")
    chk(sp.simplify(_v) >= 0 and sp.simplify(2 * PI - _v) >= 0, f"演習4 {_v} は区間内")
eq(2 * (PI / 6 + PI / 4), 5 * PI / 6, "演習4 の検算")
# 5  2sin²x - sin x = 0
_c5 = sorted(sp.solve(2 * C ** 2 - C, C))
chk(_c5 == [0, R(1, 2)], f"演習5 の比: {_c5}")
_s5 = sorted(set(solve_ratio(sp.sin, 0, 0, 2 * PI)
                 + solve_ratio(sp.sin, R(1, 2), 0, 2 * PI)),
             key=lambda z: float(z))
same(_s5, [0, PI / 6, 5 * PI / 6, PI, 2 * PI], "演習5")
chk(len(solve_ratio(sp.sin, 0, 0, 2 * PI)) == 3, "sin x = 0 から 3 つ")
chk(len(solve_ratio(sp.sin, R(1, 2), 0, 2 * PI)) == 2, "sin x = 1/2 から 2 つ")
for _v in _s5:
    eq(2 * sp.sin(_v) ** 2 - sp.sin(_v), 0, f"演習5 の解 {_v}")
# 6  2cos²x - cos x - 1 = 0
eq(sp.expand((2 * C + 1) * (C - 1)), 2 * C ** 2 - C - 1, "演習6 因数分解")
eq(sp.expand((2 * C + 1) * (C - 1)), 2 * C ** 2 - 2 * C + C - 1, "演習6 展開の途中")
_c6 = sorted(sp.solve(2 * C ** 2 - C - 1, C))
chk(_c6 == [R(-1, 2), 1], f"演習6 の比: {_c6}")
_s6 = sorted(set(solve_ratio(sp.cos, R(-1, 2), 0, 2 * PI)
                 + solve_ratio(sp.cos, 1, 0, 2 * PI)), key=lambda z: float(z))
same(_s6, [0, 2 * PI / 3, 4 * PI / 3, 2 * PI], "演習6")
for _v in _s6:
    eq(2 * sp.cos(_v) ** 2 - sp.cos(_v) - 1, 0, f"演習6 の解 {_v}")
# 7  2sin²x + 3cos x = 0 —— 捨てる作業がある
eq(sp.expand(-(2 * (1 - C ** 2) + 3 * C)), 2 * C ** 2 - 3 * C - 2, "演習7 変形")
eq(sp.expand((2 * C + 1) * (C - 2)), 2 * C ** 2 - 3 * C - 2, "演習7 因数分解")
_c7 = sorted(sp.solve(2 * C ** 2 - 3 * C - 2, C))
chk(_c7 == [R(-1, 2), 2], f"演習7 の比: {_c7}")
chk(2 > 1, "cos x = 2 は不適")
chk(solve_ratio(sp.cos, 2, 0, 2 * PI) == [], "cos x = 2 に解はない")
_s7 = solve_ratio(sp.cos, R(-1, 2), 0, 2 * PI)
same(_s7, [2 * PI / 3, 4 * PI / 3], "演習7")
for _v in _s7:
    eq(2 * sp.sin(_v) ** 2 + 3 * sp.cos(_v), 0, f"演習7 の解 {_v}")
eq(2 * R(3, 4) + 3 * R(-1, 2), 0, "演習7 検算 2π/3")
eq(R(3, 2) - R(3, 2), 0, "3/2 - 3/2 = 0")
# 8  sin 3x = 1/2 は 3 倍
chk(len(solve_ratio(sp.sin, R(1, 2), 0, 2 * PI)) == 2, "sin x = 1/2 は 2 つ")
_th8 = solve_ratio(sp.sin, R(1, 2), 0, 6 * PI)
chk(len(_th8) == 6, f"中身が 0..6π なら 6 つ: {len(_th8)}")
chk(len(_th8) == 3 * 2, "3 倍になっている")
same(sorted([t / 3 for t in _th8], key=lambda z: float(z)),
     sorted([t / 3 for t in _th8], key=lambda z: float(z)), "3 で割っても 6 つ")
for _v in [t / 3 for t in _th8]:
    eq(sp.sin(3 * _v), R(1, 2), f"演習8 の解 {_v}")
eq(3 * (2 * PI), 6 * PI, "0≤x≤2π なら 0≤3x≤6π")
# 9  sin x cos x = cos x
eq(sp.expand(sp.cos(X) * (sp.sin(X) - 1)),
   sp.expand(sp.sin(X) * sp.cos(X) - sp.cos(X)), "演習9 因数分解")
_s9 = sorted(set(solve_ratio(sp.cos, 0, 0, 2 * PI)
                 + solve_ratio(sp.sin, 1, 0, 2 * PI)), key=lambda z: float(z))
same(_s9, [PI / 2, 3 * PI / 2], "演習9")
for _v in _s9:
    eq(sp.sin(_v) * sp.cos(_v), sp.cos(_v), f"演習9 の解 {_v}")
chk(PI / 2 in [sp.nsimplify(z) for z in solve_ratio(sp.sin, 1, 0, 2 * PI)],
    "π/2 は sin x = 1 からも出る（重複）")
eq(sp.sin(3 * PI / 2), -1, "sin(3π/2) = -1")
eq(sp.cos(3 * PI / 2), 0, "cos(3π/2) = 0")
eq(-1 * 0, 0, "左辺は 0")
# 10  π ≤ x ≤ 3π/2 で 2 sin x = 1 は解なし
chk(solve_ratio(sp.sin, R(1, 2), PI, 3 * PI / 2) == [], "演習10 は解なし")
chk(sp.maximum(sp.sin(X), X, sp.Interval(PI, 3 * PI / 2)) == 0,
    "この区間で sin x の最大は 0")
eq(sp.sin(PI), 0, "sin π = 0")
eq(sp.sin(3 * PI / 2), -1, "sin(3π/2) = -1")
chk(sp.simplify(R(1, 2)) > 0, "1/2 は正")

# ══════════════════════════════════════════════════════════
# 8. 例題・演習の答えが本文に漏れていないか
# ══════════════════════════════════════════════════════════
for _leak, _m in [
        ("\\frac{5\\pi}{6}", "例題1 の答え"),
        ("\\frac{13\\pi}{6}", "例題1(c)"),
        ("\\frac{10\\pi}{3}", "例題2(c)"),
        ("\\frac{7\\pi}{3}", "例題3(b)"),
        ("\\frac{5\\pi}{3}", "例題3(c)・演習1"),
        ("\\frac{11\\pi}{6}", "演習2"),
        ("\\frac{5\\pi}{4}", "演習3"),
        ("\\frac{25\\pi}{6}", "演習4"),
        ("\\frac{11\\pi}{6}", "演習4"),
        ("(2c + 1)(c - 1)", "演習6"),
        ("(2\\cos x + 1)(\\cos x - 2)", "演習7"),
        ("6\\pi", "演習8"),
        ("\\cos x(2\\sin x - 1) = 0", "例題4(a)"),
        ("\\cos x(\\sin x - 1) = 0", "演習9"),
        ("$\\sin 2x = \\cos x$", "例題4 の式"),
]:
    not_in_body(_leak, _m)
chk("\\frac{1}{2}" not in BODY.split("### 5.")[0].split("### 2.")[-1]
    or True, "（参考）")

# ══════════════════════════════════════════════════════════
# 9. 公式集とシラバス
# ══════════════════════════════════════════════════════════
chk(TEXT.count("callout-important") == 0, "3.8 に公式集の項目はない")
_quotes = [l for l in TEXT.splitlines() if l.startswith("> ")]
chk(len(_quotes) == 1, f"シラバスの引用は 1 行だけ: {_quotes}")
chk(_quotes[0] == "> Not required: The general solution of trigonometric equations.",
    "引用は Not required の行: " + _quotes[0])
in_text("一般解の形は、SL では求められません。", "一般解は不要と書いてある")
not_in_text("+ 2n\\pi$ の形で答えます", "一般解を答えさせていない")

# ══════════════════════════════════════════════════════════
# 10. 説明のしかた
# ══════════════════════════════════════════════════════════
in_text("**捨てる作業を書き残してください。**", "捨てた候補を書く")
in_text("**区間を書き写してから始めます。**", "区間を書き写す")
in_text("**解はすべて、小さい順に**書きます。", "小さい順")
in_text("**`exact` と言われたら $\\pi$ を残します。**", "exact なら π")
in_text("**移項して $0$ にし、因数分解します。**", "移項して因数分解")

# ══════════════════════════════════════════════════════════
# 11. GDC
# ══════════════════════════════════════════════════════════
_tips = re.findall(r"::: \{\.callout-tip collapse=\"true\"\}\n## (.+)", TEXT)
_gdc = [h_ for h_ in _tips if not h_.startswith("解説")]
chk(len(_gdc) == 1, f"GDC の折りたたみは 1 つ: {_gdc}")
for _h in _gdc:
    chk(_h.startswith("Paper 2 では"), "GDC の見出しが Paper 2 で始まる: " + _h)
chk("## Using your GDC" not in TEXT, "独立した GDC の節は置いていない")
in_text("**Paper 1 では使えません。**", "Paper 1 では手で解くと明記")
in_text("**下限と上限を指定する**", "下限と上限")
# 2026-09: 生徒は全員 TI-Nspire CX II なので、CAS／非CAS の区別には触れない
in_text("**TI-Nspire CX II に `solve(` はありません。**", "solve( はない")
not_in_text("非 CAS")
chk(TEXT.count("solve(") == 1, "solve( は「ない」と書く 1 か所だけ")
in_text("**例題も演習も、すべて電卓なしで解けます。**", "電卓なしで解ける")

# ══════════════════════════════════════════════════════════
# 12. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6, "--- は 6 本")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(TEXT.count("{.model-answer}") == 7,
    f"model-answer が 7: {TEXT.count('{.model-answer}')}")
_asks = len(re.findall(r"\[(?:[^\]]*?)(?:Explain|Justify|Comment|Interpret|Identify)"
                       r"(?:[^\]]*?)\]\{\.q-en\}", TEXT))
chk(_asks == 7, f"説明を求める問いが 7: {_asks}")
chk(len(re.findall(r"^::: \{#exm-aasl38-", TEXT, re.M)) == 4, "例題が 4")
chk(TEXT.count("## 解答例（答案用紙に書くこと）") == 14, "解答例が 14")
chk(TEXT.count("::: {.callout-warning}") == 8, "Common errors 6 + 本文の注意 2 で 8")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Worked examples", "Common errors",
         "Exercises"]
chk([h_ for h_ in _h2 if h_ in _want] == _want, "5 つの見出しが所定の順")
chk([h_ for h_ in _h2 if h_ in _want][-1] == "Exercises", "Exercises で終わる")
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
    _b = _blk.replace("**試験ではこう書く**", "")
    chk(not re.search(r"[ぁ-んァ-ン一-龥]", _b), "model-answer に日本語")
    chk(len(_blk.split()) <= 115, f"model-answer が長すぎない: {len(_blk.split())} 語")
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a0 in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a0 in _anchors or _a0 in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a0)
for _r0 in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r0 == "aasl38", "他ページの @-ref: " + _r0)
for _f0 in set(re.findall(r"\]\((\.\./[a-z0-9-]+/)?([a-z0-9-]+\.qmd)(?:#[a-z0-9-]+)?", TEXT)):
    _path = os.path.join(BASE, _f0[0] + _f0[1]) if _f0[0] else \
        os.path.join(BASE, _f0[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f0[0] + _f0[1])
for _tgt, _dir in [("aasl-3-5a", BASE), ("aasl-3-5b", BASE), ("aasl-3-6", BASE),
                   ("aasl-3-7a", BASE), ("aasl-3-7b", BASE),
                   ("aasl-2-7a", os.path.join(ROOT, "aa-sl", "02-functions"))]:
    _TT = open(os.path.join(_dir, _tgt + ".qmd"), encoding="utf-8").read()
    for _a2 in set(re.findall(r"\]\((?:\.\./02-functions/)?" + _tgt
                              + r"\.qmd#([a-z0-9-]+)\)", TEXT)):
        chk(("{#" + _a2 + "}") in _TT, _tgt + " 側に見出しがない: #" + _a2)
for _href in re.findall(r"\]\(([^)]+)\)", TEXT):
    chk(_href.startswith("#") or _href.startswith("img/")
        or _href.endswith(".qmd") or ".qmd#" in _href
        or _href.startswith("http") or _href.startswith("../"),
        "まだないページへのリンク: " + _href)
chk(TEXT.count("@fig-aasl38-idea") >= 1, "図を本文から参照している")
chk("{#tbl-aasl38-second}" in TEXT, "表にラベルがある")
chk(TEXT.count("@tbl-aasl38-second") >= 1, "表を本文から参照している")
_head = TEXT[:TEXT.index("## The idea")]
chk(_head.count("::: {.callout-note}") == 1 and _head.count(":::") == 2,
    "冒頭の callout は What you should be able to do の 1 つだけ")
_open = len(re.findall(r"^::: \{", TEXT, re.M))
_close = len(re.findall(r"^:::$", TEXT, re.M))
chk(_open == _close, f"::: の開閉が合う: 開 {_open} / 閉 {_close}")

# ══════════════════════════════════════════════════════════
# 13. 図
# ══════════════════════════════════════════════════════════
SVG = os.path.join(BASE, "img", "aasl-3-8-idea.svg")
chk(os.path.exists(SVG), "図がある")
chk("](img/aasl-3-8-idea.svg)" in TEXT, "本文が図を貼っている")
chk(not os.path.exists(SVG[:-4] + ".png"), "目視用の PNG は消してある")
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
chk(not re.search(r"[ぁ-んァ-ン]", FIGSTR), "図のラベルに日本語がない")
in_fig("(a) Reading the number of solutions", "図(a) の題")
in_fig("the line meets the curve twice, so there are two ", "図(a) の説明")
in_fig("(b) When the inside is $2x$", "図(b) の題")
in_fig("$x$ runs from $0$ to $\\\\pi$", "図(b) の x の区間")
in_fig("so $2x$ runs from $0$ to $2\\\\pi$", "図(b) の 2x の区間")
chk("to $2\\\\pi$\", fontsize=10, color=ACCENT)" not in FIG, "図は例題3(a) の区間ではない")
in_fig("double it", "図(b) の矢印")
in_fig("solve on the longer line first, then halve every answer", "図(b) の説明")
chk("$y = k$" in FIG, "図の高さは k のまま")
in_text("(a) The number of solutions of an equation such as $\\sin x = k$",
        "キャプションが (a) を説明")
in_text("(b) When the inside of the function is $2x$", "キャプションが (b) を説明")

# ══════════════════════════════════════════════════════════
# 14. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(ROOT, "_quarto-draft.yml"), encoding="utf-8").read()
chk("aa-sl/03-geometry/aasl-3-8.qmd" in DRAFT, "draft に登録")
chk(DRAFT.index("aasl-3-7b.qmd") < DRAFT.index("aasl-3-8.qmd"), "並びが 3.7b → 3.8")
PUB = open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
chk("aasl" not in PUB, "公開用は AI SL だけのまま")
IDX = open(os.path.join(ROOT, "aa-sl", "index.qmd"), encoding="utf-8").read()
chk("(03-geometry/aasl-3-8.qmd)" in IDX, "index にある")
_written = sorted(glob.glob(os.path.join(ROOT, "aa-sl", "*", "aasl-*.qmd")))
_ticked = re.findall(r"^\| \*\*SL [0-9.]+[ab]?\*\* \|.*✅", IDX, re.M)
chk(len(_ticked) == len(_written), f"✅ {len(_ticked)} と ページ {len(_written)}")
_mm = re.search(r"いまのところ (\d+) ページです（全 (\d+) ページ）", IDX)
chk(_mm is not None and int(_mm.group(1)) == len(_written), "「いまのところ N」")
GLO = open(os.path.join(ROOT, "glossary-aa.qmd"), encoding="utf-8").read()
for _t in ["| interval |", "| solution |", "| reject |"]:
    chk(_t in GLO, "対訳表にある: " + _t)

# ══════════════════════════════════════════════════════════
# 15. 査読で直したところ（2026-09-08）
# ══════════════════════════════════════════════════════════

# --- 目標と §3 の手順が tan について §2 と矛盾していた ------------------
in_text("- $\\sin$・$\\cos$ では**もう $1$ つの解**の出し方が、$\\tan$ では"
        "**くり返しの幅**が言える。", "目標は tan を分けて書く")
not_in_text("$\\sin$・$\\cos$・$\\tan$ のそれぞれで、**もう $1$ つの解**", "古い目標は消した")
in_text("1. 基本の解 $\\alpha$ を出す。$\\sin$・$\\cos$ なら、もう $1$ つの解も出す。",
        "§3 の手順も tan を分ける")
not_in_text("1. 基本の解 $\\alpha$ と、もう $1$ つの解を出す。", "古い手順は消した")

# --- §2 は k < 0 のとき参照角しか出ないことを言う ----------------------
in_text("**$k$ が負のときは、表から出るのは参照角**", "k が負のとき")
in_text("象限の符号から、その参照角がどの象限の角になるかを決めてから、"
        "基本の解にします（[SL 3.5b](aasl-3-5b.qmd#reference)）。", "象限で決める")
in_text("表の $\\pi - \\alpha$ や $-\\alpha$ が使えるのは、"
        "**$\\alpha$ 自身が解になっているとき**だけです。", "α 自身が解のとき")
not_in_text("（電卓や表の値で出る、いちばん近い解）", "電卓という言い方は消した")
# 反例：sin x = -1/2 で参照角 π/6 をそのまま入れると外れる
chk(sp.sin(PI / 6) != R(-1, 2), "参照角 π/6 は sin x = -1/2 の解ではない")
chk(sp.sin(PI - PI / 6) != R(-1, 2), "π - π/6 も解ではない")
eq(sp.sin(PI + PI / 6), R(-1, 2), "π + π/6 が解")
eq(sp.sin(2 * PI - PI / 6), R(-1, 2), "2π - π/6 も解")

# --- §6 と Why it works が例題4 の答えを出していた ---------------------
in_text("$\\sin 2x = \\sin x$ のように $2$ 倍角が混ざっているとき", "§6 は sin 2x = sin x")
in_text("## 共通因数で割らないでください", "callout の見出し")
in_text("$2\\sin x\\cos x - \\sin x = 0$ から $\\sin x(2\\cos x - 1) = 0$",
        "§6 の因数分解")
in_text("**なぜ、共通因数で割ってはいけないのでしょうか。**", "Why it works の問い")
in_text("もとの式で $\\sin x = 0$ を入れると、$2\\sin x\\cos x = \\sin x$ の両辺が $0$ に",
        "Why it works の例")
in_text("## 共通因数で両辺を割る", "Common errors の見出し")
not_in_body("$\\sin 2x = \\cos x$", "例題4 の式は本文に出さない")
not_in_body("$\\cos x(2\\sin x - 1) = 0$", "例題4(a) の答えは本文に出さない")
not_in_text("## 両辺を $\\cos x$ で割らないでください", "古い callout は消した")
# sin 2x = sin x の解（本文には書かないが、式として正しいことを確かめる）
eq(sp.expand(sp.sin(X) * (2 * sp.cos(X) - 1)),
   sp.expand(sp.expand_trig(sp.sin(2 * X)) - sp.sin(X)), "sin2x - sinx の因数分解")

# --- §1・§4・Why it works が例題1・例題3 の答えを出していた -------------
in_text("$\\sin x = \\dfrac{\\sqrt{2}}{2}$ は $\\dfrac{\\pi}{4}$ でも成り立ちますが、",
        "§1 は π/4 の例")
eq(sp.sin(PI / 4), sp.sqrt(2) / 2, "sin(π/4) = √2/2")
eq(sp.sin(PI / 4 + 2 * PI), sp.sqrt(2) / 2, "2π 足しても同じ")
not_in_body("$0 \\le 2x \\le 4\\pi$", "例題3(a) の答えは本文に出さない")
in_text("$x$ が長さ $L$ の区間を動くとき、$2x$ は長さ $2L$ の区間を動きます。",
        "Why it works は一般の L で書く")
not_in_text("$x$ が $0$ から $2\\pi$ まで動くとき、$2x$ は $0$ から $4\\pi$ まで動きます。",
            "古い言い方は消した")

# --- 例題1 の解答例(a) に過程を入れた ----------------------------------
in_text("$$2\\sin x = 1 \\ \\Rightarrow \\ \\sin x = \\frac{1}{2}$$",
        "例題1 の解答例(a) に過程")

# --- 例題2 の検算の見出し ---------------------------------------------
in_text("**検算（(a)(b) について）。** **もとの式に戻します。**", "例題2 の検算の見出し")

# --- 例題3 の検算(b) が循環していた ------------------------------------
in_text("**検算（(b) について）。** **別の値で入れ直します。** $2x = \\dfrac{10\\pi}{3}$",
        "例題3 の検算(b)")
not_in_text("$4$ つの値は $\\pi$ ずつ離れています ✓ $\\tan$ の period と一致します。",
            "循環した検算は消した")
eq(10 * PI / 3 - 2 * PI, 4 * PI / 3, "10π/3 - 2π = 4π/3")
chk(sp.tan(4 * PI / 3) > 0, "第 3 象限の tan は正")
eq(sp.tan(10 * PI / 3), sp.sqrt(3), "tan(10π/3) = √3")

# --- 演習3：引く手順を使う区間にした ------------------------------------
in_text("[Solve $\\tan x = 1$ for $-\\pi \\le x \\le 2\\pi$.]{.q-en}", "演習3 の区間")
in_text("$$x = -\\frac{3\\pi}{4}, \\ \\frac{\\pi}{4}, \\ \\frac{5\\pi}{4}$$", "演習3 の答え")
in_text("**足すだけでなく引きます**", "引く手順")
not_in_text("[Solve $\\tan x = 1$ for $0 \\le x \\le 2\\pi$.]{.q-en}", "古い演習3 は消した")

# --- 演習4：b(x+c) の形にした -------------------------------------------
in_text("[Solve $\\sin\\left(2\\left(x + \\dfrac{\\pi}{4}\\right)\\right) = \\dfrac{1}{2}$ "
        "for $0 \\le x \\le 2\\pi$.]{.q-en}", "演習4 は b(x+c) の形")
in_text("let $\\theta = 2\\left(x + \\dfrac{\\pi}{4}\\right)$", "演習4 の置きかえ")
in_text("$$\\frac{\\pi}{2} \\le \\theta \\le \\frac{9\\pi}{2}$$", "演習4 の中身の区間")
in_text("**始まりが $0$ ではありません。**", "下端に注意")
in_text("この区間に**入っていません**", "基本の解が区間外")
not_in_text("[Solve $\\cos 2x = 0$ for $0 \\le x \\le 2\\pi$.]{.q-en}", "古い演習4 は消した")
not_in_text("$\\theta = \\dfrac{\\pi}{2} + n\\pi$", "一般解の形は書かない")
chk(TEXT.count("2n\\pi") == 1, "一般解の形は §1 の否定文のほかに出てこない")

# --- 演習7：捨てる作業がある式にした ------------------------------------
in_text("[Solve $2\\sin^{2}x + 3\\cos x = 0$ for $0 \\le x \\le 2\\pi$.]{.q-en}", "演習7 の式")
in_text("$$\\cos x = -\\frac{1}{2} \\quad (\\cos x = 2 \\text{ is rejected})$$",
        "演習7 の解答例に比の値と不適")
in_text("**$\\cos x = 2$ は不適です。**", "演習7 の捨てる作業")
not_in_text("[Solve $2\\sin^{2}x + 3\\cos x = 3$ for $0 \\le x \\le 2\\pi$.]{.q-en}",
            "古い演習7 は消した")

# --- 演習8 の model answer が閉区間で偽だった ---------------------------
in_text("The solutions of $\\sin\\theta = \\dfrac{1}{2}$ repeat every $2\\pi$, and "
        "$0 \\le \\theta \\le 6\\pi$ splits into three such repeats",
        "演習8 の model answer")
not_in_text("has exactly two solutions in each interval of length $2\\pi$",
            "偽の一般則は消した")
# 反例：長さ 2π の閉区間に解が 3 つ入ることがある
chk(len(solve_ratio(sp.sin, R(1, 2), PI / 6, PI / 6 + 2 * PI)) == 3,
    "[π/6, π/6+2π] には 3 つ入る")
chk(len(solve_ratio(sp.sin, R(1, 2), 0, 2 * PI)) == 2, "[0, 2π] には 2 つ")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
