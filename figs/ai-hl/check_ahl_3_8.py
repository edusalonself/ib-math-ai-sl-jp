"""AHL 3.8（単位円と三角比の恒等式）の内容を検算する。

    python3 figs/ai-hl/check_ahl_3_8.py
"""
import math
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
QMD = os.path.join(HERE, "..", "..", "ai-hl", "03-geometry-and-trigonometry",
                   "ahl-3-8.qmd")
TEXT = open(QMD, encoding="utf-8").read()

OK = NG = 0


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def near(a, b, tol=5e-4, msg=""):
    chk(abs(float(a) - float(b)) < tol, msg + f"  ({float(a)} vs {float(b)})")


def sf(v, n=3):
    return float(f"{v:.{n}g}")


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている（直したはず）: " + msg + " :: " + sub[:70])


D = math.degrees
R = math.radians

# ══════════════════════════════════════════════════════════
# 1. 単位円の定義と、直角三角形との関係
# ══════════════════════════════════════════════════════════
# 第 1 象限では、座標と「長さ」が一致する
for t in (0.2, 0.7, 1.4):
    chk(math.cos(t) > 0 and math.sin(t) > 0, "第1象限では両方正 (t=%g)" % t)
    near(math.cos(t), abs(math.cos(t)), msg="第1象限で cos = 長さ")
# 第 2 象限では一致しない（図の θ = 2.2 が反例）
near(math.cos(2.2), -0.588501, msg="cos(2.2)")
near(abs(math.cos(2.2)), 0.588501, msg="|cos(2.2)| は長さ")
chk(math.cos(2.2) < 0 < abs(math.cos(2.2)), "第2象限では座標と長さの符号が違う")
in_text("**$\\theta$ が第 $1$ 象限にあるとき**を考えます。", "SL の定義との一致を第1象限に限定")
in_text("垂線で作った三角形の底辺の**長さ**は $0.589$ ですが、$\\cos\\theta$ は $-0.589$ です。")
in_text("**長さは正、座標は符号つき**")
near(2.2 * 180 / math.pi, 126.05, tol=5e-3, msg="図の θ = 2.2 rad は約126度")
chk(math.pi / 2 < 2.2 < math.pi, "2.2 rad は第2象限")
in_text("$\\theta = 2$ ラジアン（約 $115^{\\circ}$）")
near(2 * 180 / math.pi, 114.59, tol=5e-3, msg="2 rad ≈ 115 度")

# ══════════════════════════════════════════════════════════
# 2. 象限と符号
# ══════════════════════════════════════════════════════════
QUAD = [(0.7, "+", "+", "+"), (2.2, "-", "+", "-"),
        (3.9, "-", "-", "+"), (5.4, "+", "-", "-")]
for t, sc, ss, st in QUAD:
    for val, want, name in ((math.cos(t), sc, "cos"), (math.sin(t), ss, "sin"),
                            (math.tan(t), st, "tan")):
        chk((val > 0) == (want == "+"), "t=%g の %s の符号" % (t, name))
in_text("| 第 $1$ 象限 $\\left(0 < \\theta < \\dfrac{\\pi}{2}\\right)$ | $+$ | $+$ | $+$ |")
in_text("| 第 $2$ 象限 $\\left(\\dfrac{\\pi}{2} < \\theta < \\pi\\right)$ | $-$ | $+$ | $-$ |")
in_text("| 第 $3$ 象限 $\\left(\\pi < \\theta < \\dfrac{3\\pi}{2}\\right)$ | $-$ | $-$ | $+$ |")
in_text("| 第 $4$ 象限 $\\left(\\dfrac{3\\pi}{2} < \\theta < 2\\pi\\right)$ | $+$ | $-$ | $-$ |")
# arcsin は 1 つしか返さない
near(math.asin(0.5), math.pi / 6, msg="arcsin(0.5) = π/6")
near(math.sin(5 * math.pi / 6), 0.5, msg="5π/6 も sin = 0.5")
chk(abs(math.asin(0.5) - 5 * math.pi / 6) > 1, "arcsin は 5π/6 を返さない")

# ══════════════════════════════════════════════════════════
# 3. exact values の表（= ではなく ≈ を使っているか）
# ══════════════════════════════════════════════════════════
near(float(sp.sqrt(3) / 2), 0.8660254, msg="√3/2")
near(float(sp.sqrt(2) / 2), 0.7071068, msg="√2/2")
near(float(sp.sqrt(3) / 3), 0.5773503, msg="√3/3 = tan30")
near(float(sp.sqrt(3)), 1.7320508, msg="√3 = tan60")
near(math.tan(R(30)), float(sp.sqrt(3) / 3), msg="tan30 = √3/3")
near(math.tan(R(60)), float(sp.sqrt(3)), msg="tan60 = √3")
chk(f"{float(sp.sqrt(3)/2):.3f}" == "0.866", "√3/2 は 3 d.p. で 0.866")
chk(f"{float(sp.sqrt(2)/2):.3f}" == "0.707", "√2/2 は 3 d.p. で 0.707")
chk(f"{float(sp.sqrt(3)/3):.3f}" == "0.577", "√3/3 は 3 d.p. で 0.577")
chk(f"{float(sp.sqrt(3)):.3f}" == "1.732", "√3 は 3 d.p. で 1.732")
# ★ レビュー6: 厳密値と丸めた小数を = で結ばない
in_text("$\\dfrac{\\sqrt{3}}{2} \\approx 0.866$", "≈ を使う")
in_text("$\\dfrac{\\sqrt{3}}{3} \\approx 0.577$", "tan の欄も厳密値で")
in_text("$\\sqrt{3} \\approx 1.732$", "tan の欄も厳密値で")
not_in_text("$\\dfrac{\\sqrt{3}}{2} = 0.866$", "= で結んでいない")
not_in_text("$\\dfrac{\\sqrt{2}}{2} = 0.707$", "= で結んでいない")
# ★ レビュー19: 見出しは「暗記は問われません」
in_text("### 4. よく出る角の値 — 暗記は問われません {#exact}")
not_in_text("### 4. よく出る角の値 — 試験には出ません {#exact}")
in_text("> Knowledge of exact values of $\\cos\\theta$, $\\sin\\theta$, and "
        "$\\tan\\theta$ will not be assessed on examinations", "Guidance の引用")
# π/2 の点は (0, 1)
near(math.cos(math.pi / 2), 0, msg="cos(π/2) = 0")
near(math.sin(math.pi / 2), 1, msg="sin(π/2) = 1")

# ══════════════════════════════════════════════════════════
# 4. Pythagorean identity と tan
# ══════════════════════════════════════════════════════════
for t in (0.0, 0.7, 2.2, 3.9, 5.4, -1.3):
    near(math.cos(t) ** 2 + math.sin(t) ** 2, 1.0, tol=1e-12,
         msg="cos²+sin² = 1 (t=%g)" % t)
# cos²2 と cos(2²) は別
near(math.cos(2) ** 2, 0.1731782, msg="cos²2")
near(math.cos(4), -0.6536436, msg="cos 4")
chk(f"{math.cos(2)**2:.4f}" == "0.1732", "cos²2 は 4 d.p. で 0.1732")
in_text("$\\cos^{2}2 = (-0.416147\\ldots)^{2} = 0.1732$", "丸めた値から等号でつながない")
not_in_text("$\\cos^{2}2 = (-0.4161)^{2} = 0.1732$", "レビュー13")
# ★ レビュー2: tan が定義されない θ は n∈Z
in_text("\\theta = \\frac{\\pi}{2} + n\\pi, \\ n \\text{ は整数}", "負の θ も含める")
in_text("**$\\dfrac{\\pi}{2}$ から、両向きに $\\pi$ おき**")
not_in_text("です。**$\\dfrac{\\pi}{2}$ から $\\pi$ おき**、と覚えておけば十分です。", "レビュー2")
for n in (-2, -1, 0, 1, 2):
    near(math.cos(math.pi / 2 + n * math.pi), 0, tol=1e-12,
         msg="cos(π/2 + %dπ) = 0" % n)

# ══════════════════════════════════════════════════════════
# 5. Worked example 1: cos = 0.6, 第4象限
# ══════════════════════════════════════════════════════════
near(1 - 0.6 ** 2, 0.64, msg="sin² = 0.64")
near(math.sqrt(0.64), 0.8, msg="√0.64 = 0.8")
near(-0.8 / 0.6, -4 / 3, msg="tan = -4/3")
chk(sf(-4 / 3, 3) == -1.33, "tan は 3 s.f. で -1.33")
near(math.acos(0.6), 0.9272952, msg="arccos(0.6)")
near(2 * math.pi - math.acos(0.6), 5.3558901, msg="第4象限側の θ")
near(math.sin(2 * math.pi - math.acos(0.6)), -0.8, msg="その θ の sin は -0.8")
chk(3 * math.pi / 2 < 5.3559 < 2 * math.pi, "5.356 は第4象限")
# ★ レビュー9: 循環した検算を、独立な検算に差し替えた
in_text("$\\arccos(0.6) = 0.9273$ で、第 $4$ 象限側は $\\theta = 2\\pi - 0.9273 = 5.356$ です。")
in_text("$\\cos^{2}\\theta+\\sin^{2}\\theta$ を足す検算は、ここでは**役に立ちません。**")
not_in_text("**検算。** $\\cos^{2}\\theta+\\sin^{2}\\theta = 0.36 + 0.64 = 1$ ✓ また $\\tan\\theta$ は第 $4$ 象限で",
            "レビュー9")
# その検算が「符号の誤り」を実際に落とすか
chk(abs(math.sin(5.3559) - 0.8) > 1.5, "sin(5.356) = -0.8 は +0.8 と明確に違う")
chk(abs((0.6 ** 2 + 0.8 ** 2) - (0.6 ** 2 + (-0.8) ** 2)) < 1e-15,
    "cos²+sin² は符号を区別できない（だから検算にならない）")

# ══════════════════════════════════════════════════════════
# 6. Worked example 2: cos のグラフ
# ══════════════════════════════════════════════════════════
near(math.cos(0), 1, msg="cos 0 = 1")
near(math.cos(2 * math.pi), 1, msg="cos 2π = 1")
near(math.cos(math.pi), -1, msg="cos π = -1")
near(math.cos(math.pi / 2), 0, tol=1e-15, msg="cos(π/2) = 0")
near(math.cos(3 * math.pi / 2), 0, tol=1e-15, msg="cos(3π/2) = 0")
near(math.pi, (0 + 2 * math.pi) / 2, msg="π は 0 と 2π のちょうど中間")
# ★ レビュー10: 循環した検算を差し替えた
in_text("**検算。** 電卓で $\\cos 0 = 1$、$\\cos 2\\pi = 1$ ✓ (a) と合います。")
in_text("$\\cos\\pi = -1$ が最小で、これは $0$ と $2\\pi$ の**ちょうど中間**です ✓")
not_in_text("**検算。** (b) の $2$ つは、$\\tan x$ が定義されない $x$ でもあります（[第6節](#tan)）。"
            "$\\cos x = 0$ が分母になるからです ✓ つじつまが合っています。", "レビュー10")

# ══════════════════════════════════════════════════════════
# 7. ambiguous case の理論
# ══════════════════════════════════════════════════════════
def sine_rule_B(A_deg, a, b):
    return b * math.sin(R(A_deg)) / a


def triangles(A_deg, a, b):
    """(A, a, b) から出る三角形を、実際に成り立つものだけ返す。"""
    k = sine_rule_B(A_deg, a, b)
    if k > 1 + 1e-12:
        return []
    B1 = D(math.asin(min(k, 1.0)))
    out = []
    for B in ({B1, 180 - B1} if k < 1 - 1e-12 else {90.0}):
        if A_deg + B < 180 - 1e-9:
            C = 180 - A_deg - B
            out.append((B, C, a * math.sin(R(C)) / math.sin(R(A_deg))))
    return sorted(out)


# (b) sin B > 1 なら三角形なし
chk(sine_rule_B(50, 3, 8) > 1, "A=50,a=3,b=8 は sinB>1")
chk(triangles(50, 3, 8) == [], "そのとき三角形は存在しない")
# (c) a >= b なら B2 は必ず落ちる（無作為に多数試す）
import random
random.seed(38)
bad = 0
for _ in range(4000):
    A_ = random.uniform(1, 179)
    a_ = random.uniform(1, 20)
    b_ = random.uniform(0.1, a_)          # a >= b
    k = sine_rule_B(A_, a_, b_)
    if k > 1 - 1e-12:
        continue
    B1 = D(math.asin(min(k, 1.0)))
    if A_ + (180 - B1) < 180 - 1e-9:
        bad += 1
chk(bad == 0, "a >= b なら鈍角の候補は必ず落ちる（反例 %d 件）" % bad)
# B1 は「三角形が存在すれば」必ず通る、とはかぎらない → 4 段目は両方に必要
b1fail = triangles(100, 6, 6.05)
chk(len(b1fail) == 0 or all(B < 90 for B, _, _ in b1fail),
    "A=100,a=6,b=6.05 の確認")
k_ = sine_rule_B(100, 6, 6.05)
B1_ = D(math.asin(k_))
chk(100 + B1_ > 180, "A=100,a=6,b=6.05 では鋭角の候補も落ちる（4段目は両方に要る）")
# (a) sin B = 1 のときは 1 つだけ
near(sine_rule_B(30, 4, 8), 1.0, tol=1e-12, msg="A=30,a=4,b=8 で sinB = 1")
chk(len(triangles(30, 4, 8)) == 1, "sinB=1 なら三角形は 1 つ")
# ★ レビュー16: 「2 つある」は値が 1 未満のとき
in_text("（値が $1$ より小さいとき。ちょうど $1$ なら $\\dfrac{\\pi}{2}$ の $1$ つだけです）")
in_text("（$k = 1$ なら $B = 90^{\\circ}$ の $1$ つだけ）")
in_text("a value of $\\sin B$ less than $1$ comes from two different angles")
in_text("a value of $\\sin B$ below $1$ corresponds to two angles")
# ★ レビュー8: arcsin(sin B) をやめて arcsin k に
in_text("| $1$ | sine rule で、$\\sin B$ の**値** $k$ を出す |")
in_text("| $2$ | $k > 1$ なら、**三角形は存在しません**。そこで終わり |")
in_text("| $3$ | $B_1 = \\arcsin k$ と $B_2 = 180^{\\circ} - B_1$ の $2$ つを書く")
not_in_text("$B_1 = \\arcsin(\\sin B)$", "レビュー8")
# ★ レビュー3: a<b は必要条件であって十分条件ではない
in_text("**検算。** $a < b$ は、$2$ つ出るための**必要条件**にすぎません")
in_text("**検算。** $a < b$ は $2$ つ出るための**必要条件**です")
not_in_text("$2$ つ出る条件を満たしています", "レビュー3: 十分条件のように書かない")
chk(sine_rule_B(30, 4, 8) <= 1 and 4 < 8 and len(triangles(30, 4, 8)) == 1,
    "a<b でも 1 つしか出ない例がある（十分条件でない）")
chk(4 < 8 and sine_rule_B(50, 3, 8) > 1,
    "a<b でも 0 個の例がある（十分条件でない）")

# ══════════════════════════════════════════════════════════
# 8. Worked example 3 と演習 6・7 の数値
# ══════════════════════════════════════════════════════════
near(sine_rule_B(32, 5.4, 8.1), 0.7948789, msg="WE3 sinB")
T3 = triangles(32, 5.4, 8.1)
chk(len(T3) == 2, "WE3 は三角形 2 つ")
near(T3[0][0], 52.6438, tol=5e-4, msg="WE3 B1")
near(T3[1][0], 127.3562, tol=5e-4, msg="WE3 B2")
near(T3[0][1], 95.3562, tol=5e-4, msg="WE3 C1")
near(T3[1][1], 20.6438, tol=5e-4, msg="WE3 C2")
near(T3[0][2], 10.1457, tol=5e-4, msg="WE3 c1")
near(T3[1][2], 3.5926, tol=5e-4, msg="WE3 c2")
chk(sf(T3[0][2], 3) == 10.1 and sf(T3[1][2], 3) == 3.59, "WE3 の c は 10.1 と 3.59")
# 最大角と最長辺の対応（与えられた辺と比べる、意味のある検算）
chk(8.1 > 5.4 > 3.5926, "B=127.4° の側は b が最長")
chk(10.1457 > 8.1 > 5.4, "C=95.4° の側は c が最長")
in_text("$8.1 > 5.4 > 3.59$ ✓")
in_text("$10.1 > 8.1 > 5.4$ ✓")
# A=40, a=9, b=6 の callout
near(sine_rule_B(40, 9, 6), 0.4285251, msg="callout sinB")
near(D(math.asin(sine_rule_B(40, 9, 6))), 25.374, tol=5e-3, msg="callout B1")
near(180 - 25.374, 154.626, tol=5e-3, msg="callout B2")
near(40 + 154.626, 194.626, tol=5e-3, msg="callout 合計")
chk(len(triangles(40, 9, 6)) == 1, "callout は三角形 1 つ")
# 演習 6
near(sine_rule_B(28, 6.2, 9.5), 0.7193516, msg="ex6 sinB")
T6 = triangles(28, 6.2, 9.5)
chk(len(T6) == 2, "ex6 は 2 つ")
near(T6[0][0], 46.0010, tol=5e-4, msg="ex6 B1")
near(T6[1][0], 133.9990, tol=5e-4, msg="ex6 B2")
near(T6[0][2], 12.6948, tol=5e-4, msg="ex6 c1")
near(T6[1][2], 4.0812, tol=5e-4, msg="ex6 c2")
chk(9.5 > 6.2 > 4.0812 and 12.6948 > 9.5 > 6.2, "ex6 の最長辺の対応")
# 演習 7
near(sine_rule_B(55, 12, 9), 0.6143640, msg="ex7 sinB")
T7 = triangles(55, 12, 9)
chk(len(T7) == 1, "ex7 は 1 つだけ")
near(T7[0][0], 37.9057, tol=5e-4, msg="ex7 B")
near(180 - 37.9057, 142.0943, tol=5e-4, msg="ex7 落ちるほうの B")
near(55 + 142.0943, 197.0943, tol=5e-4, msg="ex7 合計 > 180")
near(T7[0][1], 87.0943, tol=5e-4, msg="ex7 C")
near(T7[0][2], 14.6305, tol=5e-4, msg="ex7 c")
chk(14.6305 > 12 > 9, "ex7 の最長辺は c")
# 演習 8 の数値例
near(math.sin(R(40)), math.sin(R(140)), tol=1e-12, msg="sin40 = sin140")
near(math.sin(R(40)), 0.6427876, msg="sin40")
near(math.cos(R(40)), 0.7660444, msg="cos40")
near(math.cos(R(140)), -0.7660444, msg="cos140")
# cosine rule は一意（cos は (0,180) で単調）
prev = 2.0
for d in range(1, 180):
    v = math.cos(R(d))
    chk(v < prev, "cos は 0<θ<180 で単調減少 (%d)" % d) if d in (1, 90, 179) else None
    prev = v

# ══════════════════════════════════════════════════════════
# 9. 有限区間の三角方程式
# ══════════════════════════════════════════════════════════
def solve_grid(f, lo, hi, n=2000000):
    """符号変化で解を拾う（グラフの交点に相当する独立な方法）。"""
    xs = [lo + (hi - lo) * i / n for i in range(n + 1)]
    out = []
    prev = f(xs[0])
    for i in range(1, len(xs)):
        cur = f(xs[i])
        if prev == 0:
            out.append(xs[i - 1])
        elif prev * cur < 0:
            a_, b_ = xs[i - 1], xs[i]
            for _ in range(60):
                m = (a_ + b_) / 2
                if f(a_) * f(m) <= 0:
                    b_ = m
                else:
                    a_ = m
            out.append((a_ + b_) / 2)
        prev = cur
    return out


g = lambda x: 4 * math.cos(2 * x) + 1 - 3      # noqa: E731
S = solve_grid(g, 0, 2 * math.pi, 200000)
chk(len(S) == 4, "4cos(2x)+1=3 は [0,2π] で 4 解: %s" % [round(v, 4) for v in S])
for got, want in zip(S, [math.pi / 6, 5 * math.pi / 6, 7 * math.pi / 6,
                         11 * math.pi / 6]):
    near(got, want, tol=1e-6, msg="解の値")
chk([sf(v, 3) for v in S] == [0.524, 2.62, 3.67, 5.76],
    "3 s.f. で 0.524, 2.62, 3.67, 5.76: %s" % [sf(v, 3) for v in S])
S2 = solve_grid(g, 0, math.pi, 200000)
chk(len(S2) == 2, "[0,π] なら 2 解")
in_text("x = 0.524, \\quad 2.62, \\quad 3.67, \\quad 5.76")
in_text("同じ式でも、$0 \\leq x \\leq \\pi$ なら解は $0.524$ と $2.62$ の $2$ つだけです。")
# ★ レビュー17: 解が無いこともある
in_text("**三角関数はくり返すので、解があるときは無限にあります。**")
not_in_text("**三角関数はくり返すので、方程式の解は無限にあります。**", "レビュー17")
chk(solve_grid(lambda x: math.sin(x) - 2, 0, 2 * math.pi, 20000) == [],
    "sin x = 2 は解なし")
# ★ レビュー18: 端で山が切れていると数え方が変わる
h = lambda t: 6.4 + 2.5 * math.sin(0.5 * t) - 8   # noqa: E731
chk(len(solve_grid(h, 0, 4, 40000)) == 1, "[0,4] では山が切れて交点 1 つ")
in_text("**区間の端で山が切れているときは、この数え方が使えません。**")

# ══════════════════════════════════════════════════════════
# 10. Worked example 4（港）と演習 9（温室）
# ══════════════════════════════════════════════════════════
H = solve_grid(h, 0, 24, 240000)
chk(len(H) == 4, "港の解は 4 つ")
for got, want in zip(H, [1.388997, 4.894189, 13.955367, 17.460559]):
    near(got, want, tol=1e-5, msg="港の解")
chk([sf(v, 3) for v in H] == [1.39, 4.89, 14.0, 17.5], "3 s.f. で 1.39,4.89,14.0,17.5")
near(6.4 + 2.5, 8.9, msg="最大水深")
near(2 * math.pi / 0.5, 12.566, tol=5e-3, msg="周期 12.6")
near(6.4 + 2.5 * math.sin(0.5 * 3), 8.8940, tol=5e-4, msg="h(3) = 8.89")
near(6.4 + 2.5 * math.sin(0.5 * 8), 4.50799, tol=5e-4, msg="h(8) = 4.51")
chk(sf(6.4 + 2.5 * math.sin(0.5 * 8), 3) == 4.51, "h(8) は 3 s.f. で 4.51")
chk(6.4 + 2.5 * math.sin(0.5 * 3) > 8 > 6.4 + 2.5 * math.sin(0.5 * 8),
    "t=3 は窓の中、t=8 は外（検算が実際に効く）")
near(4.894189 - 1.388997, 3.5052, tol=5e-4, msg="窓の長さ 3.5 時間")
# 時刻への変換（★ レビュー7: 14:00 ではなく 13:57）
for t_, hh, mm in ((1.388997, 1, 23), (4.894189, 4, 53), (13.955367, 13, 57),
                   (17.460559, 17, 27)):
    chk(int(t_) == hh, "時 (%g)" % t_)
in_text("from about $13{:}57$ to about $17{:}28$")
not_in_text("from about $14{:}00$ to about $17{:}28$", "レビュー7")
not_in_text("$14{:}00$ から $17{:}28$ までである", "レビュー7")
# 演習 9
g9 = lambda t: 18 + 7 * math.sin(math.pi * t / 12) - 22   # noqa: E731
G9 = solve_grid(g9, 0, 24, 240000)
chk(len(G9) == 2, "温室は 2 解")
for got, want in zip(G9, [2.3233270, 9.6766730]):
    near(got, want, tol=1e-5, msg="温室の解")
chk([sf(v, 3) for v in G9] == [2.32, 9.68], "3 s.f. で 2.32, 9.68")
near(2 * math.pi / (math.pi / 12), 24, msg="温室の周期 24")
near(18 + 7 * math.sin(math.pi * 6 / 12), 25, msg="T(6) = 25")
near(18 + 7 * math.sin(math.pi * 15 / 12), 13.0503, tol=5e-4, msg="T(15) = 13.0")
chk(18 + 7 * math.sin(math.pi * 6 / 12) > 22 > 18 + 7 * math.sin(math.pi * 15 / 12),
    "t=6 は中、t=15 は外（検算が効く）")
near(9.6766730 - 2.3233270, 7.353346, tol=5e-4, msg="7.4 時間")
chk(sf(9.6766730 - 2.3233270, 2) == 7.4, "窓の長さは 2 s.f. で 7.4 時間")

# ══════════════════════════════════════════════════════════
# 11. 演習 1〜5、10 の数値
# ══════════════════════════════════════════════════════════
# ex1: sin = 0.28, 第2象限
near(1 - 0.28 ** 2, 0.9216, msg="ex1 cos²")
near(math.sqrt(0.9216), 0.96, msg="ex1 |cos|")
near(0.28 / -0.96, -0.2916667, msg="ex1 tan")
chk(sf(-0.2916667, 3) == -0.292, "ex1 tan は 3 s.f. で -0.292")
in_text("\\cos\\theta = \\pm 0.960", "3 s.f. 指定に合わせる")
not_in_text("\\cos\\theta = \\pm 0.96$$", "レビュー15")
# ex2: θ = 4
chk(math.pi < 4 < 3 * math.pi / 2, "4 rad は第3象限")
near(math.cos(4), -0.6536436, msg="cos4")
near(math.sin(4), -0.7568025, msg="sin4")
near(math.tan(4), 1.1578213, msg="tan4")
chk([sf(math.cos(4), 3), sf(math.sin(4), 3), sf(math.tan(4), 3)]
    == [-0.654, -0.757, 1.16], "ex2 の 3 s.f.")
# ex3: cos = -0.35, 第2象限
near(1 - 0.35 ** 2, 0.8775, msg="ex3 sin²")
near(math.sqrt(0.8775), 0.9367497, msg="ex3 sin")
near(0.9367497 / -0.35, -2.6764277, msg="ex3 tan")
chk(sf(0.9367497, 3) == 0.937 and sf(-2.6764277, 3) == -2.68, "ex3 の 3 s.f.")
near(math.acos(-0.35), 1.9283674, msg="ex3 θ")
chk(math.pi / 2 < 1.9283674 < math.pi, "ex3 の θ は第2象限")
near(math.sin(1.9283674), 0.9367497, msg="ex3 独立な検算")
in_text("$\\theta = \\arccos(-0.35) = 1.928$")
not_in_text("$0.937^{2}+0.35^{2} = 0.878+0.123 = 1.00$ ✓", "レビュー14")
# ex4: θ = π
near(math.sin(math.pi), 0, tol=1e-15, msg="sinπ")
near(math.cos(math.pi), -1, msg="cosπ")
# ex5: cos = 0.8
near(1 - 0.8 ** 2, 0.36, msg="ex5 sin²")
near(math.acos(0.8), 0.6435011, msg="ex5 θ1")
near(math.sin(math.acos(0.8)), 0.6, msg="ex5 sin θ1")
near(2 * math.pi - math.acos(0.8), 5.6396842, msg="ex5 θ2")
near(math.sin(2 * math.pi - math.acos(0.8)), -0.6, msg="ex5 sin θ2")
in_text("$\\theta = \\arccos(0.8) = 0.6435$ なら $\\sin\\theta = 0.6$")
not_in_text("$0.8^{2}+(-0.6)^{2}$ も同じく $1$ ✓", "レビュー11")
# ex10: sin x = 0.5
near(math.pi / 6, 0.5235988, msg="π/6")
near(math.pi - math.pi / 6, 2.6179939, msg="π - π/6")
chk(sf(math.pi / 6, 3) == 0.524 and sf(5 * math.pi / 6, 3) == 2.62, "ex10 の 3 s.f.")

# ══════════════════════════════════════════════════════════
# 12. GDC
# ══════════════════════════════════════════════════════════
in_text("doc → Settings → Document Settings")
in_text("`Angle` を **Radian** にしておきます。")
in_text("`ctrl` と `k` を押すとパレットが開く")
near(math.cos(2), -0.4161468, msg="GDC cos(2)")
near(math.sin(2), 0.9092974, msg="GDC sin(2)")
near(math.sin(R(32)), 0.5299193, msg="sin32°")
near(math.sin(32), 0.5514267, msg="sin32 rad")
chk(abs(math.sin(R(32)) - math.sin(32)) > 0.01, "度とラジアンで別の数になる")
# ★ レビュー4: Radian 設定では arcsin の出力もラジアン
near(math.asin(0.7949), 0.9188427, msg="asin(0.7949) rad")
near(0.9188 * 180 / math.pi, 52.6434, tol=5e-3, msg="0.9188×180/π = 52.6")
in_text("Radian 設定のままなら、$0.9188$ **radians** が返ります。")
in_text("0.9188*180/π")
not_in_text("$52.6^{\\circ}$（Degree 設定のとき）が返ります。", "レビュー4")
# ★ レビュー5: cos²+sin² は答えの検算にならない
in_text("## $\\cos^{2}\\theta+\\sin^{2}\\theta$ は、答えの検算になりません")
in_text("- **出た値を、もとの式に戻す。** $h(1.39) = 8.00$ ✓ のように。これがいちばん強い検算です")
not_in_text("$1$ つ目が、いちばん手早い検算です。**$1$ にならなければ、その先は全部ずれます。**",
            "レビュー5")
near(6.4 + 2.5 * math.sin(0.5 * 1.389), 8.0000, tol=5e-4, msg="h(1.39) = 8.00")
chk("solve(" not in TEXT.replace("nSolve(", ""), "CAS 専用の solve( を使っていない")
near(0.5 * 6 ** 2, 18, msg="ダミー（sympy 読み込み確認）")

# ══════════════════════════════════════════════════════════
# 13. シラバス・公式集の引用
# ══════════════════════════════════════════════════════════
in_text("\\cos^{2}\\theta + \\sin^{2}\\theta = 1, \\qquad \\tan\\theta = \\frac{\\sin\\theta}{\\cos\\theta}")
in_text("**$2$ 行あります。** 見出しは `Identities` です。")
in_text("> The definitions of $\\cos\\theta$ and $\\sin\\theta$ in terms of the unit circle.")
in_text("> The Pythagorean identity: $\\cos^{2}\\theta + \\sin^{2}\\theta = 1$")
in_text("> Definition of $\\tan\\theta$ as $\\dfrac{\\sin\\theta}{\\cos\\theta}$")
in_text("> Extension of the sine rule to the ambiguous case.")
in_text("> Graphical methods of solving trigonometric equations in a finite interval.")
in_text("> Students should understand how the graphs of $f(x) = \\sin x$ and "
        "$f(x) = \\cos x$ can be constructed from the unit circle.")
in_text("> **Link to:** sinusoidal models (SL2.5 and AHL2.9).")
in_text("> On HL examination papers radian measure should be assumed unless otherwise indicated.")
in_text("Recommended teaching hours は $28$ 時間です")
in_text("> **Other contexts:** Generation of sinusoidal voltage in electrical engineering.")
in_text("The origin of the word \"sine\"")
in_text("> **Use of technology:** Animation applets that show the development of a "
        "trigometric function graph from the unit circle.")
in_text("**ambiguous case のための追加の公式はありません**")

# ══════════════════════════════════════════════════════════
# 14. 構造
# ══════════════════════════════════════════════════════════
chk(sum(1 for l in TEXT.split("\n") if l.strip() == "---") == 6,
    "--- は 6 本（front matter 2 + 例題 4）")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳は 14 個")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep は 9 個")
chk(len(re.findall(r"\{#exm-", TEXT)) == 4, "worked example は 4 個")
chk(re.findall(r"\[(\d+)\]\{\.ex-no\}", TEXT) == [str(i) for i in range(1, 11)],
    "演習は 1..10 の連番")
idea = re.findall(r"(?m)^### (\d+)\.", TEXT)
chk(idea == [str(i) for i in range(1, 10)] + [str(i) for i in range(1, 6)],
    "The idea 1..9 と GDC 1..5 の連番: " + str(idea))
chk(TEXT.count("::: {.model-answer}") == 6, "model-answer は 6 個")
for h in ["## What you should be able to do", "## The idea", "## Why it works",
          "## Worked examples", "## Common errors",
          "## Using your GDC (TI-Nspire CX II)", "## Exercises"]:
    in_text(h, "固定見出し")
for cmd in ["Explain why", "Explain, using the unit circle", "Interpret",
            "Identify the error", "Show that"]:
    in_text(cmd, "command term")
for w in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん", "当たり前",
          "確かめ。", "そのとおり"]:
    not_in_text(w, "禁止表現")
in_text("**unit circle**（単位円）", "英語→日本語の順")
in_text("**quadrant**（象限）", "英語→日本語の順")
in_text("![What $\\cos\\theta$ and $\\sin\\theta$ mean, and the signs in each quadrant](img/ahl-3-8-unit-circle.svg)")
in_text("![From one lap of the circle to one period of the graph](img/ahl-3-8-graphs.svg)")
in_text("![Why two triangles can fit the same information](img/ahl-3-8-ambiguous.svg)")
for svg in ["ahl-3-8-unit-circle.svg", "ahl-3-8-graphs.svg",
            "ahl-3-8-ambiguous.svg"]:
    chk(os.path.exists(os.path.join(HERE, "..", "..", "ai-hl",
                                    "03-geometry-and-trigonometry", "img", svg)),
        "図がある: " + svg)
anchors = set(re.findall(r"\{#([a-z0-9-]+)[\s\}]", TEXT)) | {"common-errors",
                                                             "why-it-works"}
for anc in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(anc in anchors, "内部アンカーがない: #" + anc)
refs = set(re.findall(r"@((?:eq|fig|tbl|exm)-[a-z0-9-]+)", TEXT))
for rf in refs:
    chk(rf in anchors, "crossref の先がない: @" + rf)
for a_ in anchors:
    if re.match(r"(eq|fig|tbl|exm)-", a_):
        chk(a_ in refs, "使われていない crossref アンカー: " + a_)
for m in re.findall(r"`[^`\n]*`", TEXT):
    chk("$" not in m, "コードスパンに $ が入っている: " + m[:50])
for line in TEXT.split("\n"):
    if line.startswith("|") and "$" in line:
        inner = re.sub(r"^\||\|$", "", line)
        chk("\\lvert" in line or "|" not in inner.replace(" | ", ""),
            "表のセルの中の | :: " + line[:60])
chk("@sec-" not in TEXT, "他ページを @ で参照していない")
chk(TEXT.count("\\left") == TEXT.count("\\right"), "\\left と \\right の対応")
for link in ["[SL 3.2](../../ai-sl/03-geometry-and-trigonometry/sl-3-2.qmd#sine-rule)",
             "[SL 3.2](../../ai-sl/03-geometry-and-trigonometry/sl-3-2.qmd#sohcahtoa)",
             "[SL 3.2](../../ai-sl/03-geometry-and-trigonometry/sl-3-2.qmd#ambiguous)",
             "[SL 2.5](../../ai-sl/02-functions/sl-2-5.qmd#sinusoidal)",
             "[AHL 2.9a](../02-functions/ahl-2-9a.qmd#four-letters)",
             "[AHL 2.8](../02-functions/ahl-2-8.qmd#vstretch)",
             "[AHL 3.7](ahl-3-7.qmd#full-turn)"]:
    in_text(link, "他ページへのリンク")

# 登録されているか
DRAFT = open(os.path.join(HERE, "..", "..", "_quarto-draft.yml"),
             encoding="utf-8").read()
chk("ai-hl/03-geometry-and-trigonometry/ahl-3-8.qmd" in DRAFT,
    "_quarto-draft.yml に登録されている")
chk(DRAFT.index("ahl-3-7.qmd") < DRAFT.index("ahl-3-8.qmd") < DRAFT.index("ahl-3-9.qmd"),
    "サイドバーの並びが 3.7 → 3.8 → 3.9")
IDX = open(os.path.join(HERE, "..", "..", "ai-hl", "index.qmd"),
           encoding="utf-8").read()
chk("[AHL 3.8 — The unit circle and identities](03-geometry-and-trigonometry/ahl-3-8.qmd)"
    in IDX, "index の一覧にある")
chk("| **AHL 3.8** | **[The unit circle and identities]"
    "(03-geometry-and-trigonometry/ahl-3-8.qmd)** ✅ |" in IDX,
    "index の表が ✅ になっている")
_left = int(_m.group(1)) if (_m := re.search(r"残りの(\d+)項目", IDX)) else 0
_rows = re.findall(r"^\| (?:\*\*)?AHL [0-9.]+(?:\*\*)? \|(.*)\|$", IDX, re.M)
chk(_left == len([r for r in _rows if "\u2705" not in r]),
    "「残りの N 項目」が、まだ ✅ の付いていない行の数と合う")
GLO = open(os.path.join(HERE, "..", "..", "glossary-ai.qmd"),
           encoding="utf-8").read()
for term in ["| unit circle |", "| quadrant |", "| Pythagorean identity |",
             "| ambiguous case |", "| finite interval |", "| harbour |"]:
    chk(term in GLO, "対訳表にある: " + term)

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
