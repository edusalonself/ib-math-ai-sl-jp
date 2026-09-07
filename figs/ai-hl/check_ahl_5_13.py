# -*- coding: utf-8 -*-
"""AHL 5.13（kinematics）の検算。
   1. すべての値を第一原理から出す（微分・積分を自分で組み立てる）
   2. sympy と scipy の数値積分で、独立に突き合わせる
   3. .qmd の本文が、その数値どおりに書かれているかを確かめる
   4. シラバスと公式集から確かめた事実を見張る
   5. 構造の不変条件を確かめる
   実行: python3 figs/ai-hl/check_ahl_5_13.py
"""
import io
import math
import os
import re
import sys

import sympy as sp
from scipy.integrate import quad

QMD = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "05-calculus", "ahl-5-13.qmd")
TXT = io.open(QMD, encoding="utf-8").read()

OK = NG = 0


def eq(name, got, want):
    global OK, NG
    if got == want:
        OK += 1
    else:
        NG += 1
        print("NG  %s\n     got : %r\n     want: %r" % (name, got, want))


def close(name, got, want, tol=5e-4):
    global OK, NG
    if abs(got - want) <= tol:
        OK += 1
    else:
        NG += 1
        print("NG  %s  got %r want %r" % (name, got, want))


def in_text(s, times=None):
    global OK, NG
    c = TXT.count(s)
    if (c >= 1) if times is None else (c == times):
        OK += 1
    else:
        NG += 1
        print("NG  本文に無い/回数違い (%d): %r" % (c, s[:90]))


def not_in_text(s):
    global OK, NG
    if s not in TXT:
        OK += 1
    else:
        NG += 1
        print("NG  本文に残っている: %r" % (s[:90],))


t, s = sp.symbols("t s", real=True)


def displacement(vexpr, a, b):
    return sp.integrate(vexpr, (t, a, b))


def distance(vexpr, a, b, roots):
    pts = [a] + sorted(r for r in roots if a < r < b) + [b]
    return sum(abs(sp.integrate(vexpr, (t, pts[i], pts[i + 1])))
               for i in range(len(pts) - 1))


# ══════════════════════════════════════════════════════════════
# 1. 走らせる例  v = t^2 - 4t + 3
# ══════════════════════════════════════════════════════════════
V = t ** 2 - 4 * t + 3
eq("v = 0 の解", sorted(sp.solve(V, t)), [1, 3])
A = sp.diff(V, t)
eq("a = dv/dt", sp.expand(A), sp.expand(2 * t - 4))
eq("a = 0 の解", sp.solve(A, t), [2])
S = sp.integrate(V, t)
eq("s(t)（s(0)=0）", sp.expand(S), sp.expand(t ** 3 / 3 - 2 * t ** 2 + 3 * t))
eq("s'' が a に等しい", sp.simplify(sp.diff(S, t, 2) - A), 0)
eq("displacement 0..4", displacement(V, 0, 4), sp.Rational(4, 3))
eq("total distance 0..4", distance(V, 0, 4, [1, 3]), 4)
eq("区間ごとの積分",
   [sp.integrate(V, (t, x, y)) for x, y in ((0, 1), (1, 3), (3, 4))],
   [sp.Rational(4, 3), sp.Rational(-4, 3), sp.Rational(4, 3)])
close("displacement を 3 桁で", round(float(sp.Rational(4, 3)), 2), 1.33)
# 数値積分で独立に確かめる
fv = sp.lambdify(t, V)
close("quad displacement", quad(fv, 0, 4)[0], 4 / 3)
close("quad distance", quad(lambda z: abs(fv(z)), 0, 4)[0], 4.0)
# s の値（図 (d) の根拠）
for tv, want in ((0, 0), (1, sp.Rational(4, 3)), (3, 0), (4, sp.Rational(4, 3))):
    eq("s(%s)" % tv, S.subs(t, tv), want)
# 最大の speed（1 <= t <= 3）
eq("v(2)", V.subs(t, 2), -1)
eq("v(1) と v(3)", [V.subs(t, 1), V.subs(t, 3)], [0, 0])
eq("1<=t<=3 の最大 speed", max(abs(V.subs(t, x)) for x in (1, 2, 3)), 1)
# 0<=t<=4 では speed の最大は 3（本文の注意の根拠）
eq("0<=t<=4 の最大 speed", max(abs(V.subs(t, x)) for x in (0, 2, 4)), 3)
# a を 1 点で確かめる（GDC 第3節）
eq("a(3)", A.subs(t, 3), 2)

# ══════════════════════════════════════════════════════════════
# 2. a = v dv/ds  の例
# ══════════════════════════════════════════════════════════════
VS = sp.sqrt(9 + 4 * s)
eq("dv/ds", sp.simplify(sp.diff(VS, s) - 2 / sp.sqrt(9 + 4 * s)), 0)
eq("a = v dv/ds は定数 2", sp.simplify(VS * sp.diff(VS, s)), 2)
eq("v^2 = 9 + 4s", sp.expand(VS ** 2), sp.expand(9 + 4 * s))
eq("v^2 = u^2 + 2as の形（u=3, a=2）", (3 ** 2, 2 * 2), (9, 4))
# 演習5
eq("演習5 s=4 での v", sp.sqrt(9 + 4 * 4), 5)
eq("演習5 dv/ds(4)", sp.diff(sp.sqrt(9 + 4 * s), s).subs(s, 4), sp.Rational(2, 5))
eq("演習5 a", sp.simplify(sp.sqrt(9 + 4 * s) * sp.diff(sp.sqrt(9 + 4 * s), s)), 2)
# 第4節・例題3 の線形の場合
VL = 2 * s + 3
eq("第4節 a の式", sp.expand(VL * sp.diff(VL, s)), sp.expand(4 * s + 6))
eq("例題3 a(4)", (VL * sp.diff(VL, s)).subs(s, 4), 22)
eq("例題3 a(0)", (VL * sp.diff(VL, s)).subs(s, 0), 6)
eq("例題3 v(4)", VL.subs(s, 4), 11)

# ══════════════════════════════════════════════════════════════
# 3. GDC の例  v = 5 - e^{0.4t}
# ══════════════════════════════════════════════════════════════
VC = 5 - sp.exp(sp.Rational(2, 5) * t)
root = float(sp.log(5) / sp.Rational(2, 5))
close("v = 0 の時刻", round(root, 2), 4.02)
fc = sp.lambdify(t, VC)
disp = quad(fc, 0, 6)[0]
dist = quad(lambda z: abs(fc(z)), 0, 6)[0]
close("displacement 0..6", round(disp, 2), 4.94)
close("total distance 0..6", round(dist, 1), 15.3)
close("前半の積分", round(quad(fc, 0, root)[0], 1), 10.1)
close("後半の積分", round(quad(fc, root, 6)[0], 2), -5.18)
close("sympy でも同じ displacement", float(sp.integrate(VC, (t, 0, 6))), disp)
eq("道のりは変位より大きい", dist > abs(disp), True)

# ══════════════════════════════════════════════════════════════
# 4. 演習の数値
# ══════════════════════════════════════════════════════════════
V1 = 3 * t ** 2 - 12 * t
eq("演習1 a", sp.expand(sp.diff(V1, t)), sp.expand(6 * t - 12))
eq("演習1 v=0", sorted(sp.solve(V1, t)), [0, 4])

S2 = t ** 3 - 3 * t ** 2 - 9 * t
eq("演習2 v", sp.expand(sp.diff(S2, t)), sp.expand(3 * t ** 2 - 6 * t - 9))
eq("演習2 a", sp.expand(sp.diff(S2, t, 2)), sp.expand(6 * t - 6))
eq("演習2 v=0", sorted(sp.solve(sp.diff(S2, t), t)), [-1, 3])

V3 = 2 * t - 6
eq("演習3 displacement", displacement(V3, 0, 5), -5)
eq("演習3 区間ごと",
   [sp.integrate(V3, (t, 0, 3)), sp.integrate(V3, (t, 3, 5))], [-9, 4])
eq("演習3 distance", distance(V3, 0, 5, [3]), 13)

V4 = t ** 2 - 5 * t + 4
eq("演習4 v(3)", V4.subs(t, 3), -2)
eq("演習4 speed(3)", abs(V4.subs(t, 3)), 2)

V6 = t * sp.sin(t)
f6 = sp.lambdify(t, V6)
close("演習6 displacement", round(quad(f6, 0, 4)[0], 2), 1.86)
close("演習6 distance", round(quad(lambda z: abs(f6(z)), 0, 4)[0], 2), 4.43)
close("演習6 v=0 は t=pi", round(math.pi, 2), 3.14)
close("演習6 前半", round(quad(f6, 0, math.pi)[0], 2), 3.14)
close("演習6 後半", round(quad(f6, math.pi, 4)[0], 2), -1.28)

A7 = 6 * t - 4
eq("演習7 v の式", sp.expand(sp.integrate(A7, t) + 5),
   sp.expand(3 * t ** 2 - 4 * t + 5))
eq("演習7 v(2)", (3 * t ** 2 - 4 * t + 5).subs(t, 2), 9)
eq("演習7 v を微分すると a", sp.expand(sp.diff(3 * t ** 2 - 4 * t + 5, t)),
   sp.expand(A7))

# 演習8：F + B = 20, F - B = 4
F_, B_ = sp.symbols("F B")
eq("演習8 の連立", sp.solve([F_ + B_ - 20, F_ - B_ - 4], [F_, B_]),
   {F_: 12, B_: 8})

# ══════════════════════════════════════════════════════════════
# 5. 本文が、その数値どおりに書かれているか
# ══════════════════════════════════════════════════════════════
in_text("= \\frac{64}{3} - 32 + 12 = \\frac{4}{3}")
in_text("\\text{total distance} = \\frac{4}{3} + \\frac{4}{3} + \\frac{4}{3} = 4")
in_text("v(2) = 4 - 8 + 3 = -1")
in_text("a = v\\frac{dv}{ds} = (2s + 3) \\times 2 = 4s + 6")
in_text("t = 4.02 \\ \\text{s}")
in_text("\\int_{0}^{6} v\\,dt = 4.94 \\ \\text{m}")
in_text("\\int_{0}^{6} |v|\\,dt = 15.3 \\ \\text{m}")
in_text("前半が $+10.12$、後半が $-5.176$ です")
in_text("a = v\\frac{dv}{ds} = 5 \\times 0.4 = 2 \\ \\text{m s}^{-2}")
in_text("\\int_{0}^{4} t \\sin t \\, dt = 1.86 \\ \\text{m}")
in_text("\\int_{0}^{4} \\left|t \\sin t\\right| dt = 4.43 \\ \\text{m}")
in_text("前半が $+3.142$、後半が $-1.284$")
in_text("v = 3t^{2} - 4t + 5 \\ \\text{m s}^{-1}")
in_text("v(2) = 12 - 8 + 5 = 9 \\ \\text{m s}^{-1}")
in_text("2F = 24 \\quad \\Longrightarrow \\quad F = 12, \\qquad B = 8")
in_text("\\text{total distance} = 9 + 4 = 13 \\ \\text{m}")

# ══════════════════════════════════════════════════════════════
# 6. シラバス・公式集から確かめた事実
# ══════════════════════════════════════════════════════════════
in_text("> **Speed is the magnitude of velocity.**")
in_text("> Use of $\\dot{x} = \\dfrac{dx}{dt}$ and $\\ddot{x} = \\dfrac{d^{2}x}{dt^{2}}$.")
in_text("> **Links to other subjects:** Kinematics (physics).")
in_text("a = \\frac{dv}{dt} = \\frac{d^{2}s}{dt^{2}} = v\\frac{dv}{ds}")
in_text("\\text{distance travelled from } t_1 \\text{ to } t_2 = \\int_{t_1}^{t_2} |v(t)|\\,dt")
in_text("\\text{displacement from } t_1 \\text{ to } t_2 = \\int_{t_1}^{t_2} v(t)\\,dt")
in_text("**ただし、$v = \\dfrac{ds}{dt}$ は印刷されていません。**")
in_text("**この式は AI の公式集にもありません。** 検算に使うだけにしてください。")
# at rest / changes direction
in_text("## `at rest`（静止している）は $v = 0$ です。$a = 0$ ではありません")
in_text("$v = (t-2)^{2}$ のような式だと、$t = 2$ で $v = 0$ になりますが**符号は変わりません。**")
eq("(t-2)^2 は t=2 で 0 だが符号は変わらない",
   [((x - 2) ** 2 > 0) for x in (1, 3)], [True, True])
# v が s の式か t の式か
in_text("| $v$ が **$t$ の式**")
in_text("| $v$ が **$s$ の式**")

# ══════════════════════════════════════════════════════════════
# 7. 構造の不変条件
# ══════════════════════════════════════════════════════════════
bad = [m for m in re.findall(r"`[^`\n]+`", TXT) if "$" in m or "**" in m]
eq("code span の中に数式・markdown が無い", bad, [])

# 表のセルの中の数式に | が入っていない（| は列の区切りになってしまう）
tb = []
for line in TXT.split("\n"):
    if not line.startswith("|"):
        continue
    parts = line.split("$")
    for k in range(1, len(parts), 2):
        if "|" in parts[k]:
            tb.append(line)
            break
eq("表のセルの数式に | が無い", tb, [])

L = TXT.split("\n")
nb = [i + 1 for i, l in enumerate(L)
      if re.match(r"^:{3,} *\{", l) and i > 0
      and L[i - 1].strip() != "" and not L[i - 1].lstrip().startswith("#")]
eq("開き fence の前に空行がある", nb, [])

eq("演習は 10 問", TXT.count("]{.ex-no}"), 10)
eq("区切りは 9 個", TXT.count("::: {.ex-sep}"), 9)
eq("exercise-block は 1 つ", TXT.count("::: {.exercise-block}"), 1)
eq("例題は 4 つ", TXT.count("::: {#exm-ahl513-"), 4)
eq("日本語訳の折りたたみ", TXT.count('<details class="jp-trans">'), 14)

i_we = TXT.index("## Worked examples")
i_ce = TXT.index("## Common errors")
we = TXT[i_we:i_ce]
eq("例題の日本語訳の下に区切り線がある",
   we.count("</details>\n\n---\n\n"), we.count("</details>"))
eq("演習には区切り線を入れない", TXT[i_ce:].count("\n---\n"), 0)

chapters = [l[3:] for i, l in enumerate(L)
            if l.startswith("## ") and not (i and L[i - 1].lstrip().startswith(":::"))]
eq("章見出しは _TEMPLATE の順どおり", chapters == [
    "The idea", "Why it works", "Worked examples", "Common errors",
    "Using your GDC (TI-Nspire CX II)", "Exercises"], True)
in_text("::: {.callout-note}\n## What you should be able to do")

anchors = set(re.findall(r"\{#([A-Za-z0-9\-]+)\}", TXT))
links = set(re.findall(r"\]\(#([A-Za-z0-9\-]+)\)", TXT))
eq("ページ内リンクの行き先がすべてある", sorted(links - anchors), [])

for w in ("誰でもできる", "簡単です", "当然", "明らか", "もちろん", "当たり前"):
    not_in_text(w)

eq("検算が書かれている", TXT.count("**検算。**") >= 6, True)
eq("model-answer がある", TXT.count("::: {.model-answer}") >= 5, True)
in_text("![How the three graphs of one motion fit together](img/ahl-5-13-links.svg)")
in_text("![Displacement and total distance are the same picture with and without the modulus](img/ahl-5-13-area.svg)")



# ══════════════════════════════════════════════════════════════
# 8. レビューで直した点（元に戻っていないか）
# ══════════════════════════════════════════════════════════════
# SL の範囲を超える微分を、教える側に置かない
not_in_text(r"\frac{1}{2}(9 + 4s)^{-\frac{1}{2}}")
not_in_text("chain rule です（[SL 5.3](../../ai-sl/05-calculus/sl-5-3.qmd)）")
in_text("これは [AHL 5.9b](ahl-5-9b.qmd#chain) の内容です。")
in_text("この分け方を **chain rule**（合成関数の微分法）といいます。一般の形は [AHL 5.9b](ahl-5-9b.qmd#chain) で扱います。")
in_text("$v = 2s + 3$ と書かれていると")
in_text("| $v$ が **$s$ の式**（例：$v = 2s + 3$） |")
# suvat の条件
in_text("**使えるのは $a$ が一定のときだけ**です。")
in_text("## $v^{2} = u^{2} + 2as$ との関係")
# 道のりと変位の差は min の 2 倍
in_text(r"\text{道のり} - |\text{変位}| = (P + N) - |P - N| = 2\min(P,\ N)")
not_in_text("**下の面積が大きいほど、変位と道のりの差が大きく**なります")
eq("差は min の 2 倍（P=8/3, N=4/3）",
   sp.Rational(8, 3) + sp.Rational(4, 3) - abs(sp.Rational(8, 3) - sp.Rational(4, 3)),
   2 * min(sp.Rational(8, 3), sp.Rational(4, 3)))
# paper の数
in_text("AI HL は**$3$ つの paper すべてで電卓が使えます。**")
not_in_text("AI HL は**両方の paper で電卓が使えます。**")
# radian の理由と往復
in_text("三角関数の中身に $^{\circ}$ が付いていないときは、その数は **radian**（弧度。角を度ではなく実数で測る測り方）です")
not_in_text("kinematics の $t$ は**時間**なので、三角関数の中身は radian です")
in_text("doc → Settings → Document Settings → Angle: Radian")
in_text("**この項目が終わったら Degree に戻してください。**")
# シラバスの位置づけ
not_in_text("シラバスは、この項目を「物理の運動学と同じ内容」と位置づけています")
in_text("シラバスは、この項目に次の注記を付けています。")
# 公式集の行の呼び方
in_text("公式集の $1$ 行目にある、$3$ 番目の書き方です（@eq-ahl513-acc）")
in_text("公式集の $3$ 行目です（@eq-ahl513-disp）")
not_in_text("公式集の $3$ つ目の形です")
# 覚える式が 1 つある、という予告
in_text("**新しい計算のやり方は出てきません。**（覚える式が $1$ つだけあります。次の欄で見ます。）")
# displacement の二義性
in_text("## `displacement` は、$2$ つの意味で使われます")
in_text("そこから**位置がどれだけ変わったか**を表します")
not_in_text("そこから**どれだけ動いたか**を表します")
# particle の初出
in_text("**particle**（粒子。大きさを考えない、点のような物体）")
# 1 点落とす、という根拠のない主張を外した
not_in_text("$1$ 点落とします")
in_text("**答えそのものが違う値**になります")
# a -> v の worked block
in_text("**$a$ から $v$ に戻るときも、まったく同じです。**")
in_text("5 = 0 - 0 + C \\quad \\Longrightarrow \\quad C = 5")
# 第7節の例が主張に合っている
in_text("$v$ の最大は $0$（$t = 1$ と $t = 3$）ですが、speed の最大は $1$（$t = 2$）です")
eq("[1,3] では max v = 0、max speed = 1",
   (max(V.subs(t, x) for x in (1, 2, 3)), max(abs(V.subs(t, x)) for x in (1, 2, 3))),
   (0, 1))
# ドット記法を演習で使う
in_text(r"Find $\dot{x}$ and $\ddot{x}$")
in_text(r"\dot{x} = 3t^{2} - 6t - 9 \ \text{m s}^{-1}")
in_text(r"\ddot{x} = 6t - 6 \ \text{m s}^{-2}")
# 図は 4 つの絵
in_text("$4$ つの絵で見たものです")
not_in_text("で動く物体の $3$ つのグラフです")
# 単位は s
not_in_text(r"\text{秒}")
# リンク先
in_text("[AHL 5.16a](ahl-5-16a.qmd#gdc-home)")
not_in_text("[AHL 5.16a](ahl-5-16a.qmd#gdc-sheet)")

in_text("# AHL 5.13 — Kinematics（運動力学） {#sec-ahl-5-13}")
not_in_text("Kinematics（運動の記述）")


# ══════════════════════════════════════════════════════════
#  2026-08: v=0 / a=0 の読み方
# ══════════════════════════════════════════════════════════
in_text("| $v = 0$ | **一瞬静止する。** 前後で $v$ の**符号が変われば**、向きも変わる | $t = 1$、$t = 3$ |")
in_text("| $a = 0$ | **velocity（速度）が極大・極小になる候補。** 前後で $a$ の符号が変わるかを確かめる | $t = 2$ |")
not_in_text("| $v = 0$ | **一瞬止まる。** 向きが変わる瞬間 | $t = 1$、$t = 3$ |")
not_in_text("| $a = 0$ | 速度が**増えるか減るかの境目** | $t = 2$ |")
in_text("です。$a = 0$ を解くと、**velocity（速度）が極大・極小になる候補**が得られます。")
not_in_text("です。$a = 0$ を解くと、**いちばん速い（または遅い）瞬間**が出てきます。別のものです。")
in_text("1. **$a = 0$ になる時刻**（velocity が極大・極小になる候補）")
not_in_text("1. **$a = 0$ になる時刻**（$v$ が折り返すところ）")
in_text("**正しくは**：$v = 0$ を解きます。$a = 0$ が出すのは、velocity（速度）が極大・極小になる候補の時刻です。")
not_in_text("$a = 0$ が出すのは、速度が折り返す時刻です。")
# v = (t-2)^2 は t=2 で v=0 だが符号が変わらない（向きは変わらない）
_v = lambda t: (t - 2) ** 2
eq("v=(t-2)^2 は t=2 の前後で符号が変わらない",
   _v(1.9) > 0 and _v(2.1) > 0 and abs(_v(2.0)) < 1e-15, True)
# a=0 でも v の極値とは限らない例: v = t^3 なら a = 3t^2 = 0 が t=0、
# しかし a の符号は変わらず v は単調増加
eq("v=t^3 では a=0 でも v の極値ではない",
   (0.0 - (-1.0) ** 3) > 0 and (1.0 ** 3 - 0.0) > 0, True)
eq("そのとき a=3t^2 は t=0 の前後で符号が変わらない",
   3 * (-0.1) ** 2 > 0 and 3 * (0.1) ** 2 > 0, True)

print("=" * 78)
print("結果:  OK %d / NG %d" % (OK, NG))
print("=" * 78)
sys.exit(1 if NG else 0)
