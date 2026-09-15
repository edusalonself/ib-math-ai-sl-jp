"""AHL 3.12b（速度が変わる運動）の内容を検算する。

    python3 figs/ai-hl/check_ahl_3_12b.py
"""
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "..", "..", "ai-hl", "03-geometry-and-trigonometry")
QMD = os.path.join(BASE, "ahl-3-12b.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_ahl_3_12b.py"), encoding="utf-8").read()

OK = NG = 0
t = sp.Symbol("t", nonnegative=True)


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


# ══════════════════════════════════════════════════════════
# 1. シラバスの例 v = (7, 6-4t)
# ══════════════════════════════════════════════════════════
V = vec(7, 6 - 4 * t)
for T, w in [(0, (7, 6)), (1, (7, 2)), (sp.Rational(3, 2), (7, 0)),
             (2, (7, -2)), (3, (7, -6))]:
    same(V.subs(t, T), vec(*w), f"表の v (t={T})")
eq(sp.expand(V.dot(V)), 16 * t**2 - 48 * t + 85, "|v|² の展開")
eq(sp.expand(V.dot(V) - 49 - (6 - 4 * t)**2), 0, "|v|² = 49 + (6-4t)²")
eq(mag(V.subs(t, 0)), sp.sqrt(85), "|v(0)| = √85")
near(sp.sqrt(85), 9.21954, msg="√85 の小数")
chk(round(float(sp.sqrt(85)), 2) == 9.22, "3 桁で 9.22")
chk(sp.solve(sp.Eq(6 - 4 * t, 0), t) == [sp.Rational(3, 2)], "v_y=0 は t=1.5")
eq(mag(V.subs(t, sp.Rational(3, 2))), 7, "最小の速さ 7")
for T in (1, 2):
    eq(mag(V.subs(t, T)), sp.sqrt(53), f"t={T} では √53")
near(sp.sqrt(53), 7.28011, msg="√53 の小数")
chk(float(sp.sqrt(53)) > 7, "前後は 7 より大きい")
same(sp.diff(V, t), vec(0, -4), "a = (0,-4)")
# 速さは 0 にならない
chk(sp.solve([sp.Eq(V[0], 0), sp.Eq(V[1], 0)], t) == [], "速さは 0 にならない")
in_text("**速さは決して $0$ になりません。**", "その説明")

R = vec(sp.integrate(7, (t, 0, t)), sp.integrate(6 - 4 * t, (t, 0, t)))
same(sp.simplify(R), vec(7 * t, 6 * t - 2 * t**2), "r = (7t, 6t-2t²)")
same(sp.diff(R, t), V, "微分して v に戻る")
same(R.subs(t, 2), vec(14, 4), "r(2)")
same(R.subs(t, 3), vec(21, 0), "r(3)")
same(R.subs(t, sp.Rational(3, 2)), vec(sp.Rational(21, 2), sp.Rational(9, 2)),
     "最高点 (10.5, 4.5)")
chk(sorted(sp.solve(sp.Eq(R[1], 0), t)) == [0, 3], "y=0 は t=0,3")
eq(R[1].subs(t, 2), 4, "y(2)=4")
eq(R[1].subs(t, 4), -8, "y(4)=-8")
eq(R[1].subs(t, sp.Rational(5, 2)), sp.Rational(5, 2), "y(2.5)=2.5（誤答なら 0 でない）")
in_text("$y(2.5) = 15-12.5 = 2.5$ で $0$ になりません", "根そのものを評価する検算")
in_text("まず $y(3) = 18-18 = 0$", "根で 0 になることを先に確かめている")
not_in_text("**$t = 3$ をはさんで符号が変わっています** ✓\n", "根を評価しない古い検算")
# 定数成分を積分し忘れた誤答は、微分で戻らない
chk(sp.diff(sp.Integer(7), t) == 0, "7 のままだと微分して 0 になる")

# ══════════════════════════════════════════════════════════
# 2. 円運動
# ══════════════════════════════════════════════════════════
RC = vec(5 * sp.cos(2 * t), 5 * sp.sin(2 * t))
VC = sp.diff(RC, t)
same(VC, vec(-10 * sp.sin(2 * t), 10 * sp.cos(2 * t)), "円運動の v")
eq(sp.simplify(mag(RC)), 5, "|r| = 5")
eq(sp.simplify(mag(VC)), 10, "|v| = 10")
eq(sp.simplify(RC.dot(VC)), 0, "r と v は垂直（3.13a への布石）")
same(RC.subs(t, 0), vec(5, 0), "t=0 の位置")
same(VC.subs(t, 0), vec(0, 10), "t=0 の速度")
same(RC.subs(t, sp.pi / 4), vec(0, 5), "t=π/4 の位置")
same(VC.subs(t, sp.pi / 4), vec(-10, 0), "t=π/4 の速度")
# chain rule の 2 を落とすと速さが 5 になる
eq(sp.simplify(mag(vec(-5 * sp.sin(2 * t), 5 * sp.cos(2 * t)))), 5,
   "2 を落とすと速さ 5")
in_text("速さが $5$ になってしまいます", "その誤りを名指ししている")
# ω を一般に：|v| = R|ω|
Rr, om = sp.symbols("R omega", positive=True)
gen = sp.Matrix([-Rr * om * sp.sin(om * t), Rr * om * sp.cos(om * t)])
eq(sp.simplify(mag(gen)), Rr * om, "|v| = Rω （R,ω>0）")
in_text("\\lvert \\mathbf{v} \\rvert = R\\lvert \\omega \\rvert", "本文は |ω| で書いてある")
in_text("$\\omega \\neq 0$ なら、その円の上をまわり続けます。", "ω=0 の場合に触れている")
# 円運動では v_y=0 が最低点にもなる（最高点の条件の反例）
chk(sp.solve(sp.Eq(VC[1], 0), t) != [], "円運動でも v_y=0 になる時刻はある")
eq(RC[1].subs(t, 3 * sp.pi / 4), -5, "t=3π/4 では y=-5（最低点）")
in_text("円運動では、$v_y = 0$ が最低点になることもあります", "最高点の条件の反例を書いている")
in_text("**ただし「$v_y = 0$ なら最高点」と言えるのは、$\\mathbf{a}$ が下向き**",
        "最高点に条件が付いている")
not_in_text("**これが最高点**です。$y$ 座標が最大になるのは", "無条件の古い書き方")

# ══════════════════════════════════════════════════════════
# 3. 時間のずらし
# ══════════════════════════════════════════════════════════
VP = vec(3, 4 - 2 * t)
VQ = sp.expand(VP.subs(t, t - 5))
same(VQ, vec(3, 14 - 2 * t), "v_Q = (3, 14-2t)")
chk(sp.solve(sp.Eq(VP[1], 0), t) == [2], "P は t=2")
chk(sp.solve(sp.Eq(VQ[1], 0), t) == [7], "Q は t=7")
same(VQ.subs(t, 5), VP.subs(t, 0), "v_Q(5) = v_P(0)")
eq(mag(VQ.subs(t, 7)), 3, "そのときの速さ 3")
# 符号を逆にした誤り
same(sp.expand(VP.subs(t, t + 5)).subs(t, 5), vec(3, -16), "t+5 なら (3,-16)")
in_text("$\\begin{pmatrix} 3 \\\\ -16 \\end{pmatrix}$ になり", "その誤りを名指ししている")
# f(t-a) と AHL 1.13b の -B/ω の対応
a_, w_ = sp.symbols("a omega", positive=True)
lhs = sp.cos(w_ * (t - a_))
chk(sp.simplify(sp.expand_trig(lhs) - sp.expand_trig(sp.cos(w_ * t + (-w_ * a_)))) == 0,
    "cos(ω(t-a)) = cos(ωt + B) で B = -ωa、つまり a = -B/ω")
in_text("**$f(t-a)$ の $a$ にあたるのが、その $-\\dfrac{B}{\\omega}$ です。**",
        "1.13b との対応を書いている")

# ══════════════════════════════════════════════════════════
# 4. 演習の数値
# ══════════════════════════════════════════════════════════
E1 = vec(2 * t, 3)
same(E1.subs(t, 4), vec(8, 3), "演習1 の v(4)")
eq(mag(E1.subs(t, 4)), sp.sqrt(73), "演習1 の速さ")
near(sp.sqrt(73), 8.544, msg="√73 の小数")
chk(8 < float(sp.sqrt(73)) < 11, "演習1 の幅")

E2 = vec(6, 8 - 2 * t)
chk(sp.solve(sp.Eq(E2[1], 0), t) == [4], "演習2 は t=4")
eq(mag(E2.subs(t, 4)), 6, "演習2 の最小 6")
for T in (3, 5):
    eq(mag(E2.subs(t, T)), sp.sqrt(40), f"演習2 t={T} は √40")
near(sp.sqrt(40), 6.32456, msg="√40 の小数")

E3v = vec(4, 10 - 2 * t)
E3 = vec(1 + sp.integrate(4, (t, 0, t)), sp.integrate(10 - 2 * t, (t, 0, t)))
same(sp.simplify(E3), vec(1 + 4 * t, 10 * t - t**2), "演習3 の r")
same(sp.diff(E3, t), E3v, "演習3 の検算（微分で戻る）")
same(E3.subs(t, 0), vec(1, 0), "演習3 の初期条件")
same(E3.subs(t, 3), vec(13, 21), "演習3 の r(3)")

E4 = vec(3 * t, 12 * t - 3 * t**2)
E4v = sp.diff(E4, t)
same(E4v, vec(3, 12 - 6 * t), "演習4 の v")
same(sp.diff(E4v, t), vec(0, -6), "演習4 の a")
chk(sp.solve(sp.Eq(E4v[1], 0), t) == [2], "演習4 の最高点は t=2")
eq(E4[1].subs(t, 2), 12, "その高さ 12")
eq(E4[1].subs(t, 1), 9, "y(1)=9")
eq(E4[1].subs(t, 3), 9, "y(3)=9")
chk(sp.diff(E4v, t)[1] < 0, "a が下向きなので、v_y=0 は最高点でよい")

E5 = vec(4 * sp.cos(3 * t), 4 * sp.sin(3 * t))
eq(sp.simplify(mag(E5)), 4, "演習5 の半径 4")
same(sp.diff(E5, t), vec(-12 * sp.sin(3 * t), 12 * sp.cos(3 * t)), "演習5 の v")
eq(sp.simplify(mag(sp.diff(E5, t))), 12, "演習5 の速さ 12")

E6P = vec(5, 9 - 3 * t)
E6Q = sp.expand(E6P.subs(t, t - 4))
same(E6Q, vec(5, 21 - 3 * t), "演習6 の v_Q")
chk(sp.solve(sp.Eq(E6P[1], 0), t) == [3], "P は t=3")
chk(sp.solve(sp.Eq(E6Q[1], 0), t) == [7], "Q は t=7")
same(E6Q.subs(t, 4), E6P.subs(t, 0), "演習6 の検算")
same(sp.expand(E6P.subs(t, t + 4)).subs(t, 4), vec(5, -15), "t+4 なら (5,-15)")

E7v = vec(12, 16 - 10 * t)
E7 = vec(sp.integrate(12, (t, 0, t)), sp.integrate(16 - 10 * t, (t, 0, t)))
same(sp.simplify(E7), vec(12 * t, 16 * t - 5 * t**2), "演習7 の r")
chk(sp.solve(sp.Eq(E7v[1], 0), t) == [sp.Rational(8, 5)], "演習7 の最高点 t=1.6")
eq(E7[1].subs(t, sp.Rational(8, 5)), sp.Rational(64, 5), "その高さ 12.8")
chk(sorted(sp.solve(sp.Eq(E7[1], 0), t)) == [0, sp.Rational(16, 5)], "y=0 は t=3.2")
eq(E7[0].subs(t, sp.Rational(16, 5)), sp.Rational(192, 5), "そのときの x = 38.4")
eq(E7[1].subs(t, 1), 11, "y(1)=11")
eq(E7[1].subs(t, sp.Rational(11, 5)), 11, "y(2.2)=11")
eq(2 * sp.Rational(8, 5), sp.Rational(16, 5), "3.2 = 2×1.6")
# 図はもう演習 7 の数値を出していない
chk("19.2" not in FIG and "12.8" not in FIG and "38.4" not in FIG and "3.2" not in FIG,
    "図が演習 7 の答えを先に出していない")
chk("20 * tt - 5 * tt ** 2" in FIG and "15 * tt" in FIG,
    "図の projectile は別の数値 (15, 20-10t)")
F7 = vec(15 * t, 20 * t - 5 * t**2)
same(sp.diff(F7, t), vec(15, 20 - 10 * t), "図の v")
chk(sp.solve(sp.Eq(20 - 10 * t, 0), t) == [2], "図の最高点は t=2")
same(F7.subs(t, 2), vec(30, 20), "図の最高点 (30,20)")
chk(sorted(sp.solve(sp.Eq(F7[1], 0), t)) == [0, 4], "図の着地は t=4")
same(F7.subs(t, 4), vec(60, 0), "図の着地 (60,0)")
in_text("$v_{x0} = 15$、$v_{y0} = 20$、$g = 10$ とした形です。", "本文も図に合わせてある")
not_in_text("$v_{x0} = 12$、$v_{y0} = 16$", "図と食い違う古い数値")

E8A = vec(2 * t, 3 * t)
E8B = vec(2 * t, 5 + 3 * t - t**2)
AB8 = sp.expand(E8B - E8A)
same(AB8, vec(0, 5 - t**2), "演習8 の AB")
chk(sp.expand(AB8[0]) == 0, "1 つ目の成分は恒等的に 0")
chk(sp.solve(sp.Eq(AB8[1], 0), t) == [sp.sqrt(5)], "衝突は t=√5")
near(sp.sqrt(5), 2.23607, msg="√5 の小数")
chk(round(float(sp.sqrt(5)), 2) == 2.24, "3 桁で 2.24")
same(sp.simplify(E8A.subs(t, sp.sqrt(5))), vec(2 * sp.sqrt(5), 3 * sp.sqrt(5)),
     "衝突位置（A）")
same(sp.simplify(E8B.subs(t, sp.sqrt(5))), vec(2 * sp.sqrt(5), 3 * sp.sqrt(5)),
     "衝突位置（B）")

E9 = vec(5 * sp.cos(t), 3 * sp.sin(t))
E9v = sp.diff(E9, t)
same(E9v, vec(-5 * sp.sin(t), 3 * sp.cos(t)), "演習9 の v")
eq(mag(E9v.subs(t, 0)), 3, "|v(0)| = 3")
eq(sp.simplify(mag(E9v.subs(t, sp.pi / 2))), 5, "|v(π/2)| = 5")
eq(mag(E9.subs(t, 0)), 5, "|r(0)| = 5")
eq(sp.simplify(mag(E9.subs(t, sp.pi / 2))), 3, "|r(π/2)| = 3")
chk(sp.simplify(mag(E9)) != 5, "|r| は一定でない（円ではない）")

E10v = vec(6, 8 - 2 * t)
E10 = vec(sp.integrate(6, (t, 0, t)), sp.integrate(8 - 2 * t, (t, 0, t)))
same(sp.simplify(E10), vec(6 * t, 8 * t - t**2), "演習10 の正しい r")
same(sp.diff(vec(sp.Integer(6), 8 * t - t**2), t), vec(0, 8 - 2 * t),
     "生徒の式を微分すると 1 つ目が 0")
chk(sp.diff(vec(sp.Integer(6), 8 * t - t**2), t)[0] != E10v[0],
     "だから v に戻らない")

# ══════════════════════════════════════════════════════════
# 5. 条件の付け方・言い過ぎの防止
# ══════════════════════════════════════════════════════════
in_text("$v_{x0} \\neq 0$ なら $x$ は $t$ の $1$ 次式", "放物線に v_x0≠0 の条件")
in_text("**$v_{x0} = 0$ のときは別**で、真上に投げた形になり、道すじはたて $1$ 本の線分です。",
        "その例外を書いている")
chk(not re.search(r"(?m)^\$x\$ は \$t\$ の \$1\$ 次式、", TEXT),
    "条件のない古い書き出しが残っていない")
in_text("**$\\sqrt{\\ }$ の中が $t$ の $2$ 次式のときは、対称なら頂点も正しい**",
        "対称性の検算に条件が付いている")
not_in_text("どちらも大きく、しかも対称なら頂点が正しい", "無条件の古い書き方")
# 対称でも頂点でない反例（4 次式）
d2q = t**4 - 9 * t**2 + 25
r1, r2 = sp.Rational(1), sp.sqrt(8)
eq(sp.simplify(d2q.subs(t, 1) - d2q.subs(t, sp.sqrt(8))), 0,
   "t=1 と t=√8 で同じ値（対称に見える）")
tm = sp.solve(sp.diff(d2q, t), t)
chk(sp.sqrt(sp.Rational(9, 2)) in tm, "本当の最小は t=√4.5")
chk(abs(float(sp.sqrt(sp.Rational(9, 2))) - (1 + float(sp.sqrt(8))) / 2) > 0.1,
    "その中点は最小の位置ではない")
in_text("**この方法は、$\\lvert \\mathbf{v} \\rvert^2$ が $2$ 次式でないときにも使えます。**",
        "|v|² と書いている")
not_in_text("**この方法は、$\\lvert \\mathbf{v} \\rvert$ が $2$ 次式でないときにも使えます。**",
            "|v| を 2 次式と呼んだ古い書き方")
in_text("**求めた $t$ が問題の範囲の中にあるかを、必ず確かめてください。**",
        "最小が範囲の中にあるかの確認")
in_text("same line of direction", "まっすぐな道すじの言い方が直線になっている")
not_in_text("keeps the same direction.", "向きそのものが変わらない、という古い言い方")
# その反例（向きが反転しても直線）
rev = vec(t - t**2 / 2, t - t**2 / 2)
chk(sp.simplify(rev[0] - rev[1]) == 0, "反例は y=x の上を動く")
same(sp.diff(rev, t), vec(1 - t, 1 - t), "その v は t=1 で反転する")
in_text("**試験で問われる「速度が変わる運動」は $2$ 次元だけ**です",
        "2 次元だけ、がシラバスの話だと書いてある")
in_text("計算のしかた自体は $3$ 次元でも同じですが、シラバスの範囲外です。", "その補足")

# ══════════════════════════════════════════════════════════
# 6. シラバス・公式集
# ══════════════════════════════════════════════════════════
# 2026-09: 公式集 callout は削除
not_in_text("## 公式集の AHL 3.12 の欄", "公式集 callout が残っていない")
in_text("> Motion with variable velocity in two dimensions.", "Content 2 行目の逐語引用")
for g in ["$\\begin{pmatrix} v_x \\\\ v_y \\end{pmatrix} = "
          "\\begin{pmatrix} 7 \\\\ 6-4t \\end{pmatrix}$.",
          "> Projectile motion and circular motion are special cases.",
          "> $f(t-a)$ to indicate a time-shift of $a$.",
          "> **Link to:** kinematics (AHL 5.13) and phase shift (AHL 1.13)."]:
    in_text(g, "Guidance の逐語引用")
in_text("**AHL 3.12 の Connections 欄は、空です。**", "Connections が空")
in_text("**新しく覚える式はありません。**", "暗記させていない")
# 2 次元の弧長（範囲外）を要求していない
chk("弧長" not in TEXT and "arc length" not in TEXT, "2 次元の弧長を持ち出していない")

# ══════════════════════════════════════════════════════════
# 7. GDC
# ══════════════════════════════════════════════════════════
for claim in ["menu → Calculus", "Derivative at a Point",
              "Integral", "menu → Analyze Graph → Minimum",
              "menu → Graph Entry/Edit → Parametric", "ctrl + T",
              "doc → Settings → Document Settings"]:
    in_text(claim, "GDC の記述")
for absent in ["unitV(", "norm(", "solve(", "nDeriv(", "nDerivative("]:
    chk(absent not in TEXT, "非 CAS で確認できていない関数を使っていない: " + absent)
eq(sp.integrate(6 - 4 * t, (t, 0, 2)), 4, "積分テンプレートの値 4")
eq(sp.diff(6 * t - 2 * t**2, t).subs(t, 1), 2, "微分テンプレートの値 2")
in_text("これは $y(2)-y(0)$、つまり**縦の変位**です。", "積分が変位であることを書いている")
not_in_text("$4$ が返ります。これは @exm-ahl312b-position の $y(2)$ です。",
            "位置そのものと書いた古い言い方")
for T, val in [(0, 6), (1, 2), (2, -2), (3, -6)]:
    eq((6 - 4 * t).subs(t, T), val, f"表の値 x={T}")

# ══════════════════════════════════════════════════════════
# 8. 図が本文と合っているか
# ══════════════════════════════════════════════════════════
chk("6 * tt - 2 * tt ** 2" in FIG, "図1(a) の経路が本文と同じ")
chk("np.sqrt(49 + (6 - 4 * tt) ** 2)" in FIG, "図1(b) の速さ")
chk("[1.5], [7]" in FIG, "図1(b) の最小点 (1.5,7)")
chk("5 * np.cos(th)" in FIG and "5 * np.sin(th)" in FIG, "図2(b) の円")
chk("0.30 * vx" in FIG, "図2(b) の速度矢印は縮尺 0.30")
chk("4 - 2 * tt" in FIG and "14 - 2 * tt" in FIG, "図3 の 2 本のグラフ")
chk("shift of $5$ seconds" in FIG, "図3 の注記")
chk("$Q$ does at $t = 7$ what $P$ did at $t = 2$" in FIG, "図3 の見出し")
in_text("$P$ の $v_y$ が $0$ になるのは $t = 2$、$Q$ は $t = 7$ です。", "本文も同じ")

# ══════════════════════════════════════════════════════════
# 9. 体裁の不変量
# ══════════════════════════════════════════════════════════
chk(len(re.findall(r"(?m)^---\s*$", TEXT)) == 6, "--- は front matter 2 + 例題 4")
chk(TEXT.count('<details class="jp-trans"') == 14, "日本語訳の折りたたみが 14")
chk(TEXT.count(".ex-sep") == 9, "演習の区切りが 9")
chk(TEXT.count("model-answer") == 6, "model-answer が 6")
chk(re.findall(r"\[(\d+)\]\{\.ex-no\}", TEXT) == [str(i) for i in range(1, 11)],
    "演習の番号が 1..10")
chk(len(re.findall(r"(?m)^::: \{#exm-ahl312b-", TEXT)) == 4, "例題が 4 つ")
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
atrefs = set(re.findall(r"@((?:eq|fig|tbl|exm)-ahl312b-[a-zA-Z0-9\-]+)", TEXT))
links = set(re.findall(r"\]\(#([a-zA-Z0-9\-]+)\)", TEXT))
chk(not (atrefs - defined), "未定義の @ 参照: %s" % sorted(atrefs - defined))
chk(not (links - defined - {"why-it-works"}),
    "未定義のリンク先: %s" % sorted(links - defined - {"why-it-works"}))
unused = sorted(d for d in defined
                if d.split("-")[0] in ("eq", "fig", "tbl", "exm")
                and d not in atrefs and d not in links)
chk(not unused, "使われていない番号: %s" % unused)
IMG = os.path.join(BASE, "img")
for name in ["ahl-3-12b-idea.svg", "ahl-3-12b-projectile.svg",
             "ahl-3-12b-circular.svg", "ahl-3-12b-shift.svg"]:
    chk(os.path.exists(os.path.join(IMG, name)), "図がある: " + name)
    chk("img/" + name in TEXT, "図を本文で使っている: " + name)
# 他ページへのリンクが実在するアンカーを指している
for rel, an in re.findall(r"\]\((\.\./[a-z0-9-]+/[a-z0-9-]+\.qmd|ahl-3-[0-9a-z]+\.qmd)#([a-z0-9-]+)\)",
                          TEXT):
    f = os.path.join(BASE, rel)
    if os.path.exists(f):
        src = open(f, encoding="utf-8").read()
        chk(re.search(r"\{#" + re.escape(an) + r"[ }]", src) is not None
            or an in ("why-it-works", "common-errors"),
            "リンク先のアンカーがある: %s#%s" % (rel, an))

# ══════════════════════════════════════════════════════════
# 10. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(HERE, "..", "..", "_quarto-draft.yml"),
             encoding="utf-8").read()
chk("ai-hl/03-geometry-and-trigonometry/ahl-3-12b.qmd" in DRAFT,
    "_quarto-draft.yml に登録されている")
chk(DRAFT.index("ahl-3-12a.qmd") < DRAFT.index("ahl-3-12b.qmd")
    < DRAFT.index("ahl-3-14.qmd"), "サイドバーの並びが 3.12a → 3.12b → 3.14")
PUB = open(os.path.join(HERE, "..", "..", "_quarto.yml"), encoding="utf-8").read()
chk("ahl-3-12b" not in PUB, "公開用の _quarto.yml は SL だけのまま")
IDX = open(os.path.join(HERE, "..", "..", "ai-hl", "index.qmd"),
           encoding="utf-8").read()
chk("[AHL 3.12b — Kinematics: variable velocity]"
    "(03-geometry-and-trigonometry/ahl-3-12b.qmd)" in IDX, "index の一覧にある")
chk("| **AHL 3.12** | **[Kinematics: constant velocity]"
    "(03-geometry-and-trigonometry/ahl-3-12a.qmd)** ／ "
    "**[Kinematics: variable velocity]"
    "(03-geometry-and-trigonometry/ahl-3-12b.qmd)** ✅ |" in IDX,
    "index の表が両方そろって ✅ になっている")
_left = int(_m.group(1)) if (_m := re.search(r"残りの(\d+)項目", IDX)) else 0
_rows = re.findall(r"^\| (?:\*\*)?AHL [0-9.]+(?:\*\*)? \|(.*)\|$", IDX, re.M)
chk(_left == len([x for x in _rows if "✅" not in x]),
    "「残りの N 項目」が、まだ ✅ の付いていない行の数と合う")
GLO = open(os.path.join(HERE, "..", "..", "glossary-ai.qmd"),
           encoding="utf-8").read()
for term in ["| variable velocity |", "| projectile motion |",
             "| circular motion |", "| time shift |", "| greatest height |"]:
    chk(term in GLO, "対訳表にある: " + term)

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
