"""AHL 3.12a（等速度の運動）の内容を検算する。

    python3 figs/ai-hl/check_ahl_3_12a.py
"""
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "..", "..", "ai-hl", "03-geometry-and-trigonometry")
QMD = os.path.join(BASE, "ahl-3-12a.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_ahl_3_12a.py"), encoding="utf-8").read()

OK = NG = 0
t, lam, mu = sp.symbols("t lam mu")


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def vec(*a):
    return sp.Matrix(list(a))


def mag(u):
    return sp.sqrt(sum(x**2 for x in u))


def same(u, v, msg=""):
    chk(sp.simplify(u - v) == sp.zeros(*u.shape), msg + f"  ({list(u)} vs {list(v)})")


def eq(a, b, msg=""):
    chk(sp.simplify(a - b) == 0, msg + f"  ({a} vs {b})")


def near(a, b, tol=5e-4, msg=""):
    chk(abs(float(a) - float(b)) < tol, msg + f"  ({float(a)} vs {float(b)})")


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている（直したはず）: " + msg + " :: " + sub[:70])


def r(r0, v, T):
    return vec(*r0) + T * vec(*v)


def zeros_of(expr):
    """成分が恒等的に 0 なら None、そうでなければ解のリスト。"""
    e = sp.expand(expr)
    if e == 0:
        return None
    return sp.solve(sp.Eq(e, 0), t)


def collide(rA0, vA, rB0, vB):
    """衝突する t（t>=0）があれば返す。無ければ None。"""
    AB = sp.expand(r(rB0, vB, t) - r(rA0, vA, t))
    times = set()
    for c in AB:
        z = zeros_of(c)
        if z is None:
            continue
        if not z:
            return None
        times.add(z[0])
    if len(times) == 1:
        T = times.pop()
        return T if T >= 0 else None
    return None


# ══════════════════════════════════════════════════════════
# 1. r = r0 + vt そのもの
# ══════════════════════════════════════════════════════════
R0, VV = (1, 2), (2, 1)
for T, pt in [(0, (1, 2)), (1, (3, 3)), (2, (5, 4)), (3, (7, 5)), (4, (9, 6))]:
    same(r(R0, VV, T), vec(*pt), f"図1(a) t={T}")
same(r(R0, VV, 1) - r(R0, VV, 0), vec(*VV), "1 単位時間で v だけ進む")
# 図1(b): 速さ 2 倍だと、同じ道すじで別の場所
same(r(R0, (4, 2), 1), vec(5, 4), "図1(b) Q は t=1 で (5,4)")
same(r(R0, VV, 1), vec(3, 3), "図1(b) P は t=1 で (3,3)")
chk(sp.simplify(r(R0, (4, 2), 1) - r(R0, VV, 1)) != sp.zeros(2, 1),
    "同じ t で別の場所にいる")
in_text("$t = 1$ のとき $P$ は $(3,\\ 3)$、$Q$ は $(5,\\ 4)$ で、**別の場所にいます。**",
        "その数値を本文に書いている")
# 道すじ（経路）は同じ
chk(sp.simplify(vec(4, 2) - 2 * vec(*VV)) == sp.zeros(2, 1), "Q の v は P の 2 倍")

# ══════════════════════════════════════════════════════════
# 2. 例題の数値
# ══════════════════════════════════════════════════════════
# 例題 1
P0, PV = (-3, 7), (4, -2)
same(r(P0, PV, 5), vec(17, -3), "例題1(b)")
eq(mag(vec(*PV)), 2 * sp.sqrt(5), "例題1(c) 速さ")
near(mag(vec(*PV)), 4.47214, msg="例題1(c) の小数")
chk(sp.solve(sp.Eq(7 - 2 * t, 0), t) == [sp.Rational(7, 2)], "例題1(d) t=3.5")
same(r(P0, PV, sp.Rational(7, 2)), vec(11, 0), "例題1(d) の位置")
same(r(P0, PV, 5) - vec(*P0), 5 * vec(*PV), "例題1 の検算（変位 = 5v）")
eq(mag(r(P0, PV, 5) - vec(*P0)), 5 * mag(vec(*PV)), "道のり = 5|v|")
eq(mag(r(P0, PV, 5) - vec(*P0)), 10 * sp.sqrt(5), "10√5")
# 誤答 (17,3) は検算で落ちる
chk(sp.simplify((vec(17, 3) - vec(*P0)) - 5 * vec(*PV)) != sp.zeros(2, 1),
    "例題1 の検算は y の符号ミスを捕まえる")

# 例題 2（経路は交わるが衝突しない）
A0, AV = (1, 2), (2, 3)
B0, BV = (13, 0), (-2, 1)
sol = sp.solve([A0[0] + lam * AV[0] - (B0[0] + mu * BV[0]),
                A0[1] + lam * AV[1] - (B0[1] + mu * BV[1])], [lam, mu])
chk(sol[lam] == 1 and sol[mu] == 5, "例題2 λ=1, μ=5")
same(r(A0, AV, 1), vec(3, 5), "例題2 の交点（A から）")
same(r(B0, BV, 5), vec(3, 5), "例題2 の交点（B から）")
AB2 = sp.expand(r(B0, BV, t) - r(A0, AV, t))
same(AB2, vec(12 - 4 * t, -2 - 2 * t), "例題2 の AB(t)")
chk(sp.solve(sp.Eq(AB2[0], 0), t) == [3] and sp.solve(sp.Eq(AB2[1], 0), t) == [-1],
    "例題2 の成分ごとの t は 3 と -1")
chk(collide(A0, AV, B0, BV) is None, "例題2 は衝突しない")
same(AB2.subs(t, 1), vec(8, -4), "例題2 の t=1 での AB")
in_text("$B$ は $x$ 方向に $8$ m、$y$ 方向に $-4$ m ずれたところにいます", "方角を使っていない")
not_in_text("$B$ は $8$ m 東、$4$ m 南にいます", "設定していない方角を使った古い書き方")

# 例題 3（衝突する）
C0, CV = (5, 4), (-2, 1)
AB3 = sp.expand(r(C0, CV, t) - r(A0, AV, t))
same(AB3, vec(4 - 4 * t, 2 - 2 * t), "例題3 の AB(t)")
chk(collide(A0, AV, C0, CV) == 1, "例題3 は t=1 で衝突")
same(r(A0, AV, 1), vec(3, 5), "例題3 の衝突位置（A）")
same(r(C0, CV, 1), vec(3, 5), "例題3 の衝突位置（B）")
same(AB3.subs(t, 0), vec(4, 2), "例題3 の t=0 の AB")

# 例題 4（最接近）
S0, SV = (0, 0), (3, 0)
T0, TV = (25, 0), (0, 4)
AB4 = sp.expand(r(T0, TV, t) - r(S0, SV, t))
same(AB4, vec(25 - 3 * t, 4 * t), "例題4 の AB(t)")
d2 = sp.expand(AB4.dot(AB4))
eq(d2, 25 * t**2 - 150 * t + 625, "例題4 の d²")
eq(sp.expand(25 * ((t - 3)**2 + 16)), d2, "平方完成が合っている")
chk(sp.solve(sp.diff(d2, t), t) == [3], "最小は t=3")
eq(sp.sqrt(d2.subs(t, 3)), 20, "最小距離 20")
eq(sp.sqrt(d2.subs(t, 0)), 25, "t=0 では 25")
near(sp.sqrt(d2.subs(t, 1)), 22.3607, msg="t=1 では 22.4")
same(r(S0, SV, 3), vec(9, 0), "t=3 の A")
same(r(T0, TV, 3), vec(25, 12), "t=3 の B")
same(AB4.subs(t, 3), vec(16, 12), "t=3 の AB")
eq(mag(AB4.subs(t, 3)), 20, "その長さは 20")
# 検算が「-150t を落とした誤り」を捕まえるか
d2w = sp.expand(25 * (t**2 + 25))
eq(sp.sqrt(d2w.subs(t, 0)), 25, "誤答でも t=0 では 25（ここでは捕まらない）")
near(sp.sqrt(d2w.subs(t, 1)), 25.4951, msg="誤答は t=1 で 25.5")
chk(abs(float(sp.sqrt(d2w.subs(t, 1))) - float(sp.sqrt(d2.subs(t, 1)))) > 1,
    "t=1 なら誤答と正答が食い違う")
in_text("$t = 0$ では両方 $25$ で合ってしまいますが、$t = 1$ では $5\\sqrt{26} \\approx 25.5$ となり、"
        "ここで食い違います。", "その説明を本文に書いている")
not_in_text("**平方完成を間違えていたら、ここで合いません。**", "言いすぎの古い書き方")
not_in_text("**平方完成の計算ミスは、これで必ず見つかります。**", "言いすぎの古い書き方")

# ══════════════════════════════════════════════════════════
# 3. 演習の数値
# ══════════════════════════════════════════════════════════
same(r((2, -5), (-1, 3), 4), vec(-2, 7), "演習1 の位置")
eq(mag(vec(-1, 3)), sp.sqrt(10), "演習1 の速さ")
near(sp.sqrt(10), 3.16228, msg="演習1 の小数")
same(r((2, -5), (-1, 3), 4) - vec(2, -5), 4 * vec(-1, 3), "演習1 の検算")
chk(sp.simplify((vec(-2, -17) - vec(2, -5)) - 4 * vec(-1, 3)) != sp.zeros(2, 1),
    "演習1 の検算は -17 の誤りを捕まえる")

chk(sp.solve(sp.Eq(6 - 2 * t, 0), t) == [3], "演習2 t=3")
same(r((6, 1), (-2, 4), 3), vec(0, 13), "演習2 の位置")

same(r((1, 0, -2), (2, -3, 1), 6), vec(13, -18, 4), "演習3")
same(r((1, 0, -2), (2, -3, 1), 6) - vec(1, 0, -2), 6 * vec(2, -3, 1), "演習3 の検算")

E4A, E4AV = (0, 4), (3, -1)
E4B, E4BV = (10, -6), (-2, 4)
AB4e = sp.expand(r(E4B, E4BV, t) - r(E4A, E4AV, t))
same(AB4e, vec(10 - 5 * t, -10 + 5 * t), "演習4 の AB")
chk(collide(E4A, E4AV, E4B, E4BV) == 2, "演習4 は t=2 で衝突")
same(r(E4A, E4AV, 2), vec(6, 2), "演習4 の位置（A）")
same(r(E4B, E4BV, 2), vec(6, 2), "演習4 の位置（B）")

E5A, E5AV = (1, 1), (2, 2)
E5B, E5BV = (9, 1), (-1, 3)
s5 = sp.solve([E5A[0] + lam * E5AV[0] - (E5B[0] + mu * E5BV[0]),
               E5A[1] + lam * E5AV[1] - (E5B[1] + mu * E5BV[1])], [lam, mu])
chk(s5[lam] == 3 and s5[mu] == 2, "演習5 λ=3, μ=2")
same(r(E5A, E5AV, 3), vec(7, 7), "演習5 の交点（A）")
same(r(E5B, E5BV, 2), vec(7, 7), "演習5 の交点（B）")
AB5 = sp.expand(r(E5B, E5BV, t) - r(E5A, E5AV, t))
same(AB5, vec(8 - 3 * t, t), "演習5 の AB")
chk(collide(E5A, E5AV, E5B, E5BV) is None, "演習5 は衝突しない")
chk(sp.solve(sp.Eq(AB5[0], 0), t) == [sp.Rational(8, 3)], "1 つ目は t=8/3")
chk(sp.solve(sp.Eq(AB5[1], 0), t) == [0], "2 つ目は t=0")
same(AB5.subs(t, 0), vec(8, 0), "t=0 では x 成分が 8")

AB6 = sp.expand(r((0, 5), (1, 0), t) - r((0, 0), (1, 0), t))
same(AB6, vec(0, 5), "演習6 の AB は定数")
eq(mag(AB6), 5, "演習6 の距離は 5")
chk(sp.simplify(vec(1, 0) - vec(1, 0)) == sp.zeros(2, 1), "相対速度が 0")
for T in (0, 1, 10):
    same(r((0, 5), (1, 0), T) - r((0, 0), (1, 0), T), vec(0, 5), f"演習6 t={T}")

E7A, E7AV = (10, 30), (2, 1)
E7B, E7BV = (10, 5), (5, 5)
AB7 = sp.expand(r(E7B, E7BV, t) - r(E7A, E7AV, t))
same(AB7, vec(3 * t, 4 * t - 25), "演習7 の AB")
d7 = sp.expand(AB7.dot(AB7))
eq(d7, 25 * t**2 - 200 * t + 625, "演習7 の d²")
eq(sp.expand(25 * ((t - 4)**2 + 9)), d7, "演習7 の平方完成")
chk(sp.solve(sp.diff(d7, t), t) == [4], "演習7 の最小は t=4")
eq(sp.sqrt(d7.subs(t, 4)), 15, "演習7 の最小距離 15")
same(r(E7A, E7AV, 4), vec(18, 34), "演習7 t=4 の A")
same(r(E7B, E7BV, 4), vec(30, 25), "演習7 t=4 の B")
same(AB7.subs(t, 4), vec(12, -9), "演習7 t=4 の AB")
eq(mag(AB7.subs(t, 4)), 15, "その長さは 15")
# 平方完成を (t-4)^2+16 と間違えると 20 になる
eq(5 * sp.sqrt(16), 20, "誤答なら 20")
chk(20 != 15, "直接計算と食い違う")

E8A, E8AV = (1, 2, 3), (1, 0, -1)
E8B, E8BV = (5, 2, -1), (-1, 0, 1)
AB8 = sp.expand(r(E8B, E8BV, t) - r(E8A, E8AV, t))
same(AB8, vec(4 - 2 * t, 0, -4 + 2 * t), "演習8 の AB")
chk(zeros_of(AB8[1]) is None, "演習8 の 2 つ目の成分は恒等的に 0")
chk(collide(E8A, E8AV, E8B, E8BV) == 2, "演習8 は t=2 で衝突")
same(r(E8A, E8AV, 2), vec(3, 2, 1), "演習8 の位置（A）")
same(r(E8B, E8BV, 2), vec(3, 2, 1), "演習8 の位置（B）")

same(r((0, 0), (12, 5), sp.Rational(5, 2)), vec(30, sp.Rational(25, 2)), "演習9 の位置")
eq(mag(vec(12, 5)), 13, "演習9 の速さ")
eq(mag(r((0, 0), (12, 5), sp.Rational(5, 2))), sp.Rational(65, 2), "港からの距離 32.5")
eq(sp.Rational(5, 2) * 13, sp.Rational(65, 2), "速さ × 時間 でも 32.5")

E10A, E10AV = (2, 1), (1, 3)
E10B, E10BV = (8, -5), (-1, 3)
s10 = sp.solve([E10A[0] + lam * E10AV[0] - (E10B[0] + mu * E10BV[0]),
                E10A[1] + lam * E10AV[1] - (E10B[1] + mu * E10BV[1])], [lam, mu])
chk(s10[lam] == 2 and s10[mu] == 4, "演習10 λ=2, μ=4")
same(r(E10A, E10AV, 2), vec(4, 7), "演習10 の交点（A）")
same(r(E10B, E10BV, 4), vec(4, 7), "演習10 の交点（B）")
AB10 = sp.expand(r(E10B, E10BV, t) - r(E10A, E10AV, t))
same(AB10, vec(6 - 2 * t, -6), "演習10 の AB")
chk(zeros_of(AB10[1]) == [], "2 つ目の成分は 0 にならない")
chk(collide(E10A, E10AV, E10B, E10BV) is None, "演習10 は衝突しない")

# ══════════════════════════════════════════════════════════
# 4. 条件の付け方
# ══════════════════════════════════════════════════════════
in_text("**$t \\geq 0$ でそろえば衝突**です", "衝突判定に t>=0 が付いている")
not_in_text("**そろえば衝突**です（@exm", "条件のない古い書き方")
# t<0 でそろう反例が本当にある
chk(collide((0, 0), (2, 3), (4, 6), (4, 6)) is None,
    "t=-2 でそろう例は衝突と数えない")
ABneg = sp.expand(r((4, 6), (4, 6), t) - r((0, 0), (2, 3), t))
same(ABneg, vec(4 + 2 * t, 6 + 3 * t), "その AB")
chk(sp.solve(sp.Eq(ABneg[0], 0), t) == [-2] and sp.solve(sp.Eq(ABneg[1], 0), t) == [-2],
    "成分は両方 t=-2 でそろう")
in_text("**relative velocity（相対速度）$\\mathbf{v}_B - \\mathbf{v}_A$ が $\\mathbf{0}$ でなければ**",
        "2 次式になる条件が付いている")
in_text("**相対速度が $\\mathbf{0}$ でないとき**の手順です。", "手順の表にも条件が付いている")
in_text("最接近を聞かれても、$d^2$ は $t$ の $2$ 次式にならず、定数です",
        "d ではなく d² と書いている")
not_in_text("最接近を聞かれても、$d$ は $t$ の $2$ 次式にならず", "d を 2 次式と呼んだ古い書き方")
in_text("**ただし $t \\geq 0$ なので、実際に通るのは半分（半直線）だけ**です。",
        "経路が半直線であることを書いている")
in_text("ここでの $\\mathbf{r}_0$ は **$t = 0$ にその物体が実際にいる点**でなければなりません。",
        "r0 が自由でないことを書いている")
in_text("**ただし $t = 0$ だけでは足りません。**", "t=0 の検算の限界")
not_in_text("**検算は $t = 0$ を入れること**です。出発点が出れば合っています。",
            "言いすぎの古い書き方")
# t=0 だけでは v の符号ミスを捕まえられない
same(r(P0, (4, 2), 0), vec(*P0), "v を誤っても t=0 では出発点が出る")
chk(sp.simplify(r(P0, (4, 2), 1) - r(P0, PV, 1)) != sp.zeros(2, 1),
    "t=1 なら捕まる")
# d² と d の最小が同じ t
chk(sp.solve(sp.diff(sp.sqrt(d2), t), t) == sp.solve(sp.diff(d2, t), t),
    "d と d² は同じ t で最小")
in_text("**$d^2$ ではなく $d$ を答える**", "答えるのは d")

# ══════════════════════════════════════════════════════════
# 5. シラバス・公式集
# ══════════════════════════════════════════════════════════
in_text("**ありません。$1$ 行もありません。**", "公式集に AHL 3.12 の欄がない")
in_text("シラバスの **Guidance 欄**に書かれているだけです", "r=r0+vt は Guidance")
in_text("> Vector applications to kinematics.\n> Modelling linear motion with constant velocity "
        "in two and three dimensions.", "Content 1 行目は 2 文（1 つの引用にまとめてある）")
in_text("**$1$ 行目に対応する Guidance は、次の $3$ 行**です。", "Guidance の数え方が限定的")
not_in_text("Guidance 欄には、次の $3$ 行があります。", "3.12 全体の Guidance と読める古い書き方")
for g in ["> Finding positions, intersections, describing paths, finding times and distances "
          "when two objects are closest to each other.",
          "> $\\boldsymbol{r} = \\boldsymbol{r}_0 + \\boldsymbol{v}t$.",
          "> Relative position of B from A is $\\overrightarrow{\\text{AB}}$."]:
    in_text(g, "Guidance の逐語引用")
in_text("**AHL 3.12 の Connections 欄は、空です。**", "Connections が空")
in_text("[AHL 3.12b](ahl-3-12b.qmd) です。", "2 行目は次のページ")
in_text("衝突の判定**（[第4節](#cross-vs-collide)〜[第6節](#collide-test)）を加えて扱います。",
        "5 つに衝突を足していると書いている")
not_in_text("このページは、この $5$ つを順に扱います。", "衝突を落とした古い書き方")

# ══════════════════════════════════════════════════════════
# 6. GDC
# ══════════════════════════════════════════════════════════
for claim in ["menu → 3: Algebra", "Solve System of Linear Equations",
              "`ctrl` を押してから `var`", "menu → Actions → Clear a-z",
              "menu → Analyze Graph → Minimum", "ctrl + doc", "ctrl + T"]:
    in_text(claim, "GDC の記述")
for absent in ["unitV(", "norm(", "solve(", "nSolve("]:
    chk(absent not in TEXT, "非 CAS で確認できていない関数を使っていない: " + absent)
in_text("**表の刻みは、はじめ $1$ です**（変えられます）。", "表の刻みは変えられる")
not_in_text("**表は $1$ 刻みなので、頂点がちょうど整数でないときは見つけられません。**",
            "刻みを固定と書いた古い書き方")
in_text("$25,\\ 22.36,\\ 20.62,\\ 20,\\ 20.62,\\ 22.36$", "表の値が電卓の桁で書いてある")
for T, val in [(0, 25), (1, 22.3607), (2, 20.6155), (3, 20), (4, 20.6155), (5, 22.3607)]:
    near(sp.sqrt(d2.subs(t, T)), val, tol=5e-3, msg=f"表の値 t={T}")
in_text("**これは関数のグラフなので `Analyze Graph` が使えます。**", "3.11 との違い")

# ══════════════════════════════════════════════════════════
# 7. 図が本文と合っているか
# ══════════════════════════════════════════════════════════
chk("R0 = np.array([1.0, 2.0])" in FIG and "VV = np.array([2.0, 1.0])" in FIG,
    "図1 の直線が本文と同じ")
chk("per unit of time" in FIG, "図1(a) の見出しが単位時間になっている")
chk("per second" not in FIG, "秒に決めつけた古い見出しが残っていない")
in_text("**単位時間ごとに、ちょうど $\\mathbf{v}$ だけ進みます。**"
        .replace("単位時間", "$1$ 秒"), "本文の言い方（図と合わせる前）") if False else None
# 図1(b) は Q を先に描いて、P が隠れないようにしてある
chk(FIG.index("QQ = dots") < FIG.index("PP = dots"), "図1(b) は Q を先に描いている")
chk("color=LINE, ha=\"center\", va=\"center\", zorder=10" in FIG
    and "color=GREEN, ha=\"center\", va=\"center\", zorder=10" in FIG,
    "図1(b) の凡例が色分けされている")
chk("Aa, Av = np.array([1.0, 2.0]), np.array([2.0, 3.0])" in FIG, "図2 の A")
chk("Ba, Bv = np.array([13.0, 0.0]), np.array([-2.0, 1.0])" in FIG, "図2(a) の B")
chk("Ca, Cv = np.array([5.0, 4.0]), np.array([-2.0, 1.0])" in FIG, "図2(b) の B")
chk("$A$ is there at $t = 1$, $B$ at $t = 5$" in FIG, "図2(a) の注記")
chk("collision at $t = 1$" in FIG, "図2(b) の注記")
chk("Sa, Sv = np.array([0.0, 0.0]), np.array([3.0, 0.0])" in FIG, "図3 の A")
chk("Ta, Tv = np.array([25.0, 0.0]), np.array([0.0, 4.0])" in FIG, "図3 の B")
chk("dy = -2.6 if T == 0 else 0.0" in FIG, "図3(a) の t=0 の線分をずらして描いている")
chk("$25$ km at $t = 0$" in FIG, "図3(a) が t=0 の距離を示している")
chk("$d = 5\\\\sqrt{(t-3)^2+16}$" in FIG, "図3(b) の式")
in_text("点線は、そのときどきの $A$ と $B$ を結ぶ線分で、その長さが $\\lvert \\overrightarrow{AB} \\rvert$ です。",
        "図3(a) の点線の説明が正確")
not_in_text("点線が、そのときどきの $\\overrightarrow{AB}$ です。", "矢印でないものを矢印と呼んだ古い書き方")

# ══════════════════════════════════════════════════════════
# 8. 体裁の不変量
# ══════════════════════════════════════════════════════════
chk(len(re.findall(r"(?m)^---\s*$", TEXT)) == 6, "--- は front matter 2 + 例題 4")
chk(TEXT.count('<details class="jp-trans"') == 14, "日本語訳の折りたたみが 14")
chk(TEXT.count(".ex-sep") == 9, "演習の区切りが 9")
chk(TEXT.count("model-answer") == 6, "model-answer が 6")
chk(re.findall(r"\[(\d+)\]\{\.ex-no\}", TEXT) == [str(i) for i in range(1, 11)],
    "演習の番号が 1..10")
chk(len(re.findall(r"(?m)^::: \{#exm-ahl312a-", TEXT)) == 4, "例題が 4 つ")
ideas = re.findall(r"(?m)^### (\d+)\.", TEXT)
chk(ideas == [str(i) for i in range(1, 10)] + [str(i) for i in range(1, 7)],
    "The idea 1..9 と GDC 1..6 の連番: " + ",".join(ideas))
heads = [h for h in re.findall(r"(?m)^## (.*)", TEXT)
         if h in ("What you should be able to do", "The idea", "Why it works",
                  "Worked examples", "Common errors",
                  "Using your GDC (TI-Nspire CX II)", "Exercises")]
chk(heads == ["What you should be able to do", "The idea", "Why it works",
              "Worked examples", "Common errors",
              "Using your GDC (TI-Nspire CX II)", "Exercises"],
    "7 つの見出しの順序")
chk(TEXT.count("**検算") >= 14, "検算が 14 か所以上: %d" % TEXT.count("**検算"))
chk("**確かめ" not in TEXT and "確かめます。" not in TEXT,
    "検算のラベルに「確かめ」を使っていない")
for w in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん", "当たり前", "そのとおり"]:
    chk(w not in TEXT, "禁止語を使っていない: " + w)
for m in re.finditer(r"`[^`\n]*`", TEXT):
    chk("$" not in m.group(0), "コードスパンの中の数式 :: " + m.group(0)[:60])
for line_ in TEXT.split("\n"):
    if line_.startswith("|") and "$" in line_:
        for mm in re.finditer(r"\$[^$]*\$", line_):
            chk("|" not in mm.group(0), "表のセルの数式の中の | :: " + line_[:60])
chk(TEXT.count("\\left") == TEXT.count("\\right"), "\\left と \\right の対応")
chk("@sec-" not in TEXT, "他ページを @ で参照していない")
chk(TEXT.count("$$") % 2 == 0, "$$ の個数が偶数")
for m in re.finditer(r"\$\$(.*?)\$\$", TEXT, re.S):
    chk(not any(c in m.group(1) for c in "✓✗①②"),
        "display math の中の ✓/✗ :: " + m.group(1)[:60].replace("\n", " "))
_rest = re.sub(r"\$\$.*?\$\$", " ", TEXT, flags=re.S)
for line_ in _rest.split("\n"):
    parts = line_.split("$")
    for i in range(1, len(parts), 2):
        chk(not any(c in parts[i] for c in "✓✗①②"),
            "inline math の中の ✓/✗ :: " + parts[i][:50])
defined = set(re.findall(r"\{#([a-zA-Z0-9\-]+)[ }]", TEXT))
atrefs = set(re.findall(r"@((?:eq|fig|tbl|exm)-[a-zA-Z0-9\-]+)", TEXT))
links = set(re.findall(r"\]\(#([a-zA-Z0-9\-]+)\)", TEXT))
chk(not (atrefs - defined), "未定義の @ 参照: %s" % sorted(atrefs - defined))
chk(not (links - defined - {"why-it-works"}),
    "未定義のリンク先: %s" % sorted(links - defined - {"why-it-works"}))
unused = sorted(d for d in defined
                if d.split("-")[0] in ("eq", "fig", "tbl", "exm")
                and d not in atrefs and d not in links)
chk(not unused, "使われていない番号: %s" % unused)
IMG = os.path.join(BASE, "img")
for name in ["ahl-3-12a-idea.svg", "ahl-3-12a-cross.svg", "ahl-3-12a-closest.svg"]:
    chk(os.path.exists(os.path.join(IMG, name)), "図がある: " + name)
    chk("img/" + name in TEXT, "図を本文で使っている: " + name)
for fn, an in re.findall(r"\]\((ahl-3-[0-9a-z]+)\.qmd#([a-z0-9-]+)\)", TEXT):
    f = os.path.join(BASE, fn + ".qmd")
    if os.path.exists(f):
        src = open(f, encoding="utf-8").read()
        chk("{#" + an + "}" in src or an in ("why-it-works", "common-errors"),
            "リンク先のアンカーがある: %s#%s" % (fn, an))

# ══════════════════════════════════════════════════════════
# 9. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(HERE, "..", "..", "_quarto-draft.yml"),
             encoding="utf-8").read()
chk("ai-hl/03-geometry-and-trigonometry/ahl-3-12a.qmd" in DRAFT,
    "_quarto-draft.yml に登録されている")
chk(DRAFT.index("ahl-3-11.qmd") < DRAFT.index("ahl-3-12a.qmd")
    < DRAFT.index("ahl-3-14.qmd"), "サイドバーの並びが 3.11 → 3.12a → 3.14")
PUB = open(os.path.join(HERE, "..", "..", "_quarto.yml"), encoding="utf-8").read()
chk("ahl-3-12a" not in PUB, "公開用の _quarto.yml は SL だけのまま")
IDX = open(os.path.join(HERE, "..", "..", "ai-hl", "index.qmd"),
           encoding="utf-8").read()
chk("[AHL 3.12a — Kinematics: constant velocity]"
    "(03-geometry-and-trigonometry/ahl-3-12a.qmd)" in IDX, "index の一覧にある")
_row = [x for x in re.findall(r"^\| (?:\*\*)?AHL [0-9.]+(?:\*\*)? \|(.*)\|$", IDX, re.M)
        if "ahl-3-12a.qmd" in x]
_b_exists = os.path.exists(os.path.join(
    HERE, "..", "..", "ai-hl", "03-geometry-and-trigonometry", "ahl-3-12b.qmd"))
if _b_exists:
    chk(len(_row) == 1 and "✅" in _row[0] and "ahl-3-12b.qmd" in _row[0],
        "3.12b があるので、AHL 3.12 の行は 3.12b へのリンクと ✅ を持つ")
else:
    chk(len(_row) == 1 and "✅" not in _row[0],
        "AHL 3.12 の行は、3.12b が書けるまで ✅ を付けない")
_left = int(_m.group(1)) if (_m := re.search(r"残りの(\d+)項目", IDX)) else 0
_rows = re.findall(r"^\| (?:\*\*)?AHL [0-9.]+(?:\*\*)? \|(.*)\|$", IDX, re.M)
chk(_left == len([x for x in _rows if "✅" not in x]),
    "「残りの N 項目」が、まだ ✅ の付いていない行の数と合う")
GLO = open(os.path.join(HERE, "..", "..", "glossary-ai.qmd"),
           encoding="utf-8").read()
for term in ["| constant velocity |", "| collide / collision |", "| relative position |",
             "| relative velocity |", "| closest approach |", "| path |",
             "| particle |"]:
    chk(term in GLO, "対訳表にある: " + term)

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
