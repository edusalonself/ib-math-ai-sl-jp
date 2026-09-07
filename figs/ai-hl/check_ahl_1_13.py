# -*- coding: utf-8 -*-
"""AHL 1.13a / 1.13b（polar・exponential form と正弦波の合成）の検算。
   1. すべての変換・積・商・べき乗・合成を sympy で第一原理から出す
   2. 恒等式は t の 8 点で数値照合し、図形（三角形・平行四辺形）とも突き合わせる
   3. .qmd の本文が、その式・数値どおりに書かれているかを確かめる
   4. シラバスと公式集から確かめた事実を見張る
   5. レビューで直した点を not_in_text で見張る
   6. 構造の不変条件を確かめる
   実行: python3 figs/ai-hl/check_ahl_1_13.py
"""
import cmath
import io
import math
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(__file__)
A = os.path.join(HERE, "..", "..", "ai-hl", "01-number-and-algebra",
                 "ahl-1-13a.qmd")
B = os.path.join(HERE, "..", "..", "ai-hl", "01-number-and-algebra",
                 "ahl-1-13b.qmd")
TA = io.open(A, encoding="utf-8").read()
TB = io.open(B, encoding="utf-8").read()

OK = NG = 0
I = sp.I
TPTS = (0.0, 0.017, 0.13, 0.37, 1.0, 2.5, -0.8, 3.7)


def eq(name, got, want):
    global OK, NG
    if got == want:
        OK += 1
    else:
        NG += 1
        print("NG  %s\n     got : %r\n     want: %r" % (name, got, want))


def close(name, got, want, tol=5e-4):
    global OK, NG
    if abs(float(got) - float(want)) <= tol:
        OK += 1
    else:
        NG += 1
        print("NG  %s  got %r want %r" % (name, got, want))


def _in(txt, tag):
    def f(s, times=None):
        global OK, NG
        c = txt.count(s)
        if (c >= 1) if times is None else (c == times):
            OK += 1
        else:
            NG += 1
            print("NG  %s に無い/回数違い (%d): %r" % (tag, c, s[:90]))
    return f


def _not_in(txt, tag):
    def f(s):
        global OK, NG
        if s not in txt:
            OK += 1
        else:
            NG += 1
            print("NG  %s に残っている: %r" % (tag, s[:90]))
    return f


inA, notA = _in(TA, "1.13a"), _not_in(TA, "1.13a")
inB, notB = _in(TB, "1.13b"), _not_in(TB, "1.13b")


def identity(name, f, g, tol=1e-9):
    """2 つの関数が t の 8 点で一致するか。"""
    bad = [(t, f(t) - g(t)) for t in TPTS if abs(f(t) - g(t)) > tol]
    eq(name, bad, [])


# ══════════════════════════════════════════════════════════════
# 1. 1.13a  Cartesian ⇄ polar ⇄ exponential
# ══════════════════════════════════════════════════════════════
z = 1 + sp.sqrt(3) * I
eq("|1+sqrt3 i|", sp.Abs(z), 2)
eq("arg(1+sqrt3 i)", sp.arg(z), sp.pi / 3)
close("pi/3", sp.pi / 3, 1.0472, 5e-5)
eq("2cos(pi/3)", 2 * sp.cos(sp.pi / 3), 1)
eq("2sin(pi/3)", 2 * sp.sin(sp.pi / 3), sp.sqrt(3))
inA("r = \\sqrt{1^{2}+(\\sqrt{3})^{2}} = \\sqrt{4} = 2")
inA("z = 2\\left(\\cos\\frac{\\pi}{3} + i\\sin\\frac{\\pi}{3}\\right) = 2\\operatorname{cis}\\frac{\\pi}{3}")
inA("z = 2e^{i\\pi/3}")

w = 4 * (sp.cos(2 * sp.pi / 3) + I * sp.sin(2 * sp.pi / 3))
eq("4cis(2pi/3)", sp.expand(w), -2 + 2 * sp.sqrt(3) * I)
eq("|4cis(2pi/3)|", sp.Abs(sp.expand(w)), 4)
close("2sqrt3", 2 * sp.sqrt(3), 3.4641, 5e-5)
inA("a = 4\\cos\\frac{2\\pi}{3} = 4\\left(-\\frac{1}{2}\\right) = -2")
inA("b = 4\\sin\\frac{2\\pi}{3} = 4\\left(\\frac{\\sqrt{3}}{2}\\right) = 2\\sqrt{3}")

# 積・商
eq("pi/3+pi/4", sp.nsimplify(sp.pi / 3 + sp.pi / 4), 7 * sp.pi / 12)
eq("pi/3-pi/4", sp.nsimplify(sp.pi / 3 - sp.pi / 4), sp.pi / 12)
close("7pi/12", 7 * sp.pi / 12, 1.83260, 5e-5)
z1 = 2 * sp.exp(I * sp.pi / 3)
z2 = 3 * sp.exp(I * sp.pi / 4)
eq("z1z2 = 6cis(7pi/12)",
   sp.simplify(z1 * z2 - 6 * sp.exp(I * 7 * sp.pi / 12)), 0)
eq("z1/z2 = 2/3 cis(pi/12)",
   sp.simplify(z1 / z2 - sp.Rational(2, 3) * sp.exp(I * sp.pi / 12)), 0)
inA("z_1 z_2 = (2)(3)\\operatorname{cis}\\left(\\frac{\\pi}{3}+\\frac{\\pi}{4}\\right) = 6\\operatorname{cis}\\frac{7\\pi}{12}")

# べき乗
eq("(1+sqrt3 i)^6", sp.expand(z ** 6), 64)
eq("cis(2pi)", sp.cos(2 * sp.pi) + I * sp.sin(2 * sp.pi), 1)
eq("|1+i|", sp.Abs(1 + I), sp.sqrt(2))
eq("arg(1+i)", sp.arg(1 + I), sp.pi / 4)
eq("(sqrt2)^8", sp.sqrt(2) ** 8, 16)
eq("(1+i)^8", sp.expand((1 + I) ** 8), 16)
inA("z^{6} = 2^{6}\\operatorname{cis}\\left(6 \\times \\frac{\\pi}{3}\\right) = 64\\operatorname{cis}(2\\pi) = 64")
inA("z^{8} = \\left(\\sqrt{2}\\right)^{8}e^{i(8)(\\pi/4)} = 16e^{2\\pi i} = 16")

# 範囲の直し
eq("3pi/4+pi/2", sp.nsimplify(3 * sp.pi / 4 + sp.pi / 2), 5 * sp.pi / 4)
eq("5pi/4-2pi", sp.nsimplify(5 * sp.pi / 4 - 2 * sp.pi), -3 * sp.pi / 4)
close("5pi/4", 5 * sp.pi / 4, 3.92699, 5e-5)
inA("\\frac{5\\pi}{4} - 2\\pi = -\\frac{3\\pi}{4}")
# ★レビュー 1・2・3: principal argument では arg(z1z2) が足し算にならない例
eq("arg((-1+i)^2) は arg の和ではない",
   sp.arg(sp.expand((-1 + I) ** 2)) == 2 * sp.arg(-1 + I), False)
eq("arg(i*(-1)) は -pi/2", sp.arg(I * (-1)), -sp.pi / 2)
eq("arg(-1)+pi/2 は 3pi/2", sp.arg(sp.Integer(-1)) + sp.pi / 2, 3 * sp.pi / 2)

# 幾何的解釈
eq("i*(3+i)", sp.expand(I * (3 + I)), -1 + 3 * I)
eq("2*(3+i)", sp.expand(2 * (3 + I)), 6 + 2 * I)
eq("|i(3+i)| = |3+i|", sp.Abs(-1 + 3 * I), sp.Abs(3 + I))
eq("(4+i)+(1+3i)", sp.expand((4 + I) + (1 + 3 * I)), 5 + 4 * I)
eq("三角不等式", sp.Abs(5 + 4 * I) <= sp.Abs(4 + I) + sp.Abs(1 + 3 * I), True)

# 演習
eq("|3+4i|", sp.Abs(3 + 4 * I), 5)
close("arctan(4/3)", sp.atan(sp.Rational(4, 3)), 0.927295, 5e-6)
eq("|-2+2i|", sp.Abs(-2 + 2 * I), 2 * sp.sqrt(2))
eq("arg(-2+2i)", sp.arg(-2 + 2 * I), 3 * sp.pi / 4)
eq("5cis(pi/6)", sp.expand(5 * (sp.cos(sp.pi / 6) + I * sp.sin(sp.pi / 6))),
   5 * sp.sqrt(3) / 2 + sp.Rational(5, 2) * I)
eq("3e^{-i pi/2}", sp.expand(3 * sp.exp(-I * sp.pi / 2)), -3 * I)
eq("pi/5+pi/10", sp.nsimplify(sp.pi / 5 + sp.pi / 10), 3 * sp.pi / 10)
eq("pi/5-pi/10", sp.nsimplify(sp.pi / 5 - sp.pi / 10), sp.pi / 10)
eq("(2cis(pi/6))^4",
   sp.expand((2 * (sp.cos(sp.pi / 6) + I * sp.sin(sp.pi / 6))) ** 4),
   -8 + 8 * sp.sqrt(3) * I)
eq("|-8+8sqrt3 i|", sp.Abs(-8 + 8 * sp.sqrt(3) * I), 16)
rot = sp.expand((3 + 4 * I) * sp.exp(I * sp.pi / 3))
eq("回転後の modulus", sp.simplify(sp.Abs(rot)), 5)
close("回転後の Re", sp.re(rot), -1.96410, 5e-5)
close("回転後の Im", sp.im(rot), 4.59808, 5e-5)
inA("= \\frac{3}{2} - 2\\sqrt{3} + \\left(2 + \\frac{3\\sqrt{3}}{2}\\right)i = -1.96 + 4.60i")
close("60 度は pi/3", sp.rad(60), sp.pi / 3, 1e-12)
close("60 rad は 9.55 周", 60 / (2 * math.pi), 9.5493, 5e-4)
inA("$60 \\div (2\\pi) = 9.55$")

# ══════════════════════════════════════════════════════════════
# 2. 1.13b  正弦波の合成（すべて t の 8 点で数値照合）
# ══════════════════════════════════════════════════════════════
def phasor_sum(terms):
    """terms = [(A, phi)] -> (A, B) の複素和"""
    s = sum(a * cmath.exp(1j * p) for a, p in terms)
    return s, abs(s), cmath.phase(s)


def cos_wave(terms, w):
    return lambda t: sum(a * math.cos(w * t + p) for a, p in terms)


def sin_wave(terms, w):
    return lambda t: sum(a * math.sin(w * t + p) for a, p in terms)


PI = math.pi

# 例題 1
s, Aa, Bb = phasor_sum([(3, 0), (4, PI / 2)])
eq("W1 phasor", (round(s.real, 12), round(s.imag, 12)), (3.0, 4.0))
close("W1 A", Aa, 5, 1e-12)
close("W1 B", Bb, 0.927295, 5e-6)
identity("W1 恒等式", cos_wave([(3, 0), (4, PI / 2)], 50),
         lambda t: 5 * math.cos(50 * t + Bb))
inB("3\\cos 50t + 4\\cos\\left(50t+\\frac{\\pi}{2}\\right) = 5\\cos(50t + 0.927)")

# 例題 2
s, Aa, Bb = phasor_sum([(5, PI / 3), (5, -PI / 3)])
close("W2 sum は実数 5", s.real, 5, 1e-12)
close("W2 虚部 0", s.imag, 0, 1e-12)
close("W2 B", Bb, 0, 1e-12)
identity("W2 恒等式", cos_wave([(5, PI / 3), (5, -PI / 3)], 40),
         lambda t: 5 * math.cos(40 * t))
close("5cos(pi/3)", 5 * math.cos(PI / 3), 2.5, 1e-12)
close("5sin(pi/3)", 5 * math.sin(PI / 3), 4.3301, 5e-5)
inB("y_1 + y_2 = 5\\cos 40t")

# 例題 3（sin でそろえる）
s, Aa, Bb = phasor_sum([(4, 0), (3, PI / 2)])
close("W3 A", Aa, 5, 1e-12)
close("W3 B", Bb, 0.643501, 5e-6)
identity("W3 恒等式", lambda t: 4 * math.sin(2 * t) + 3 * math.cos(2 * t),
         lambda t: 5 * math.sin(2 * t + Bb))
inB("y = 5\\sin(2t + 0.644)")

# 例題 4
s, Aa, Bb = phasor_sum([(8, 0), (8, 2 * PI / 3)])
close("W4 A", Aa, 8, 1e-12)
close("W4 B", Bb, PI / 3, 1e-12)
identity("W4 恒等式", sin_wave([(8, 0), (8, 2 * PI / 3)], 3),
         lambda t: 8 * math.sin(3 * t + PI / 3))
eq("8cis(2pi/3)",
   sp.expand(8 * (sp.cos(2 * sp.pi / 3) + I * sp.sin(2 * sp.pi / 3))),
   -4 + 4 * sp.sqrt(3) * I)
eq("|4+4sqrt3 i|", sp.Abs(4 + 4 * sp.sqrt(3) * I), 8)
eq("arctan(sqrt3)", sp.atan(sp.sqrt(3)), sp.pi / 3)
inB("y_1 + y_2 = 8\\sin\\left(3t + \\frac{\\pi}{3}\\right)")

# 演習 1
eq("6cis(pi/4)", sp.expand(6 * (sp.cos(sp.pi / 4) + I * sp.sin(sp.pi / 4))),
   3 * sp.sqrt(2) + 3 * sp.sqrt(2) * I)
eq("|3sqrt2+3sqrt2 i|", sp.Abs(3 * sp.sqrt(2) + 3 * sp.sqrt(2) * I), 6)

# 演習 2（第 2 象限）★レビューで差し替えた問題
s, Aa, Bb = phasor_sum([(6, 0), (10, 5 * PI / 6)])
close("E2 Re", s.real, -2.66025, 5e-5)
close("E2 Im", s.imag, 5.0, 1e-12)
close("E2 A", Aa, 5.66365, 5e-5)
close("E2 B", Bb, 2.05975, 5e-5)
close("E2 arctan 生値", math.atan(s.imag / s.real), -1.08184, 5e-5)
eq("E2 は第 2 象限", (s.real < 0, s.imag > 0), (True, True))
identity("E2 恒等式", cos_wave([(6, 0), (10, 5 * PI / 6)], 40),
         lambda t: Aa * math.cos(40 * t + Bb))
eq("10cos(5pi/6)", sp.expand(10 * sp.cos(5 * sp.pi / 6)), -5 * sp.sqrt(3))
eq("10sin(5pi/6)", sp.expand(10 * sp.sin(5 * sp.pi / 6)), 5)
inB("$$B = -1.08 + \\pi = 2.06$$")
inB("V_1 + V_2 = 5.66\\cos(40t + 2.06)")
inB("**この問題が、このページで唯一 $\\arctan$ の直しが要る問題です。**")
close("E2 検算 t=0 左辺", 6 + 10 * math.cos(5 * PI / 6), -2.66025, 5e-5)
close("E2 検算 t=0 右辺", 5.66 * math.cos(2.06), -2.66, 5e-3)

# 演習 3
s, Aa, Bb = phasor_sum([(7, 0), (7, PI / 2)])
close("E3 A", Aa, 7 * math.sqrt(2), 1e-12)
close("E3 B", Bb, PI / 4, 1e-12)
close("7sqrt2", 7 * math.sqrt(2), 9.89949, 5e-5)
identity("E3 恒等式", sin_wave([(7, 0), (7, PI / 2)], 4),
         lambda t: 7 * math.sqrt(2) * math.sin(4 * t + PI / 4))

# 演習 4
s, Aa, Bb = phasor_sum([(2, 0), (2, PI / 3)])
close("E4 Re", s.real, 3.0, 1e-12)
close("E4 Im", s.imag, math.sqrt(3), 1e-12)
close("E4 A", Aa, 2 * math.sqrt(3), 1e-12)
close("E4 B", Bb, PI / 6, 1e-12)
close("2sqrt3", 2 * math.sqrt(3), 3.4641, 5e-5)
identity("E4 恒等式", cos_wave([(2, 0), (2, PI / 3)], 3),
         lambda t: 2 * math.sqrt(3) * math.cos(3 * t + PI / 6))
eq("arctan(sqrt3/3)", sp.atan(sp.sqrt(3) / 3), sp.pi / 6)

# 演習 5
s, Aa, Bb = phasor_sum([(3, 0), (4, PI / 2)])
close("E5 A", Aa, 5, 1e-12)
close("E5 B", Bb, 0.927295, 5e-6)
identity("E5 恒等式", lambda t: 3 * math.sin(2 * t) + 4 * math.cos(2 * t),
         lambda t: 5 * math.sin(2 * t + Bb))

# 演習 6（三相 → 0）
s, Aa, Bb = phasor_sum([(4, 0), (4, 2 * PI / 3), (4, -2 * PI / 3)])
close("E6 和は 0", abs(s), 0, 1e-12)
identity("E6 恒等式", cos_wave([(4, 0), (4, 2 * PI / 3), (4, -2 * PI / 3)],
                              60), lambda t: 0.0)
eq("4cis(2pi/3)",
   sp.expand(4 * (sp.cos(2 * sp.pi / 3) + I * sp.sin(2 * sp.pi / 3))),
   -2 + 2 * sp.sqrt(3) * I)

# 演習 7
eq("sqrt(25+k^2)=13 の k",
   sorted(sp.solve(sp.Eq(25 + sp.Symbol("k") ** 2, 169))), [-12, 12])
eq("5+k=13 は 8（誤答）", 13 - 5, 8)

# 演習 9（完全な打ち消し）
s, Aa, Bb = phasor_sum([(0.6, 0), (0.6, PI)])
close("E9 和は 0", abs(s), 0, 1e-12)
identity("E9 恒等式", cos_wave([(0.6, 0), (0.6, PI)], 880), lambda t: 0.0)

# 演習 10（sin を cos に直す）
s, Aa, Bb = phasor_sum([(3, 0), (4, -PI / 2)])
close("E10 A", Aa, 5, 1e-12)
close("E10 B", Bb, -0.927295, 5e-6)
eq("E10 は第 4 象限", (s.real > 0, s.imag < 0), (True, True))
identity("E10 恒等式", lambda t: 3 * math.cos(2 * t) + 4 * math.sin(2 * t),
         lambda t: 5 * math.cos(2 * t + Bb))
inB("y = 5\\cos(2t - 0.927)")

# 変換の恒等式そのもの
identity("sin = cos(θ-π/2)", math.sin, lambda x: math.cos(x - PI / 2))
identity("cos = sin(θ+π/2)", math.cos, lambda x: math.sin(x + PI / 2))
inB("\\sin\\theta = \\cos\\left(\\theta - \\frac{\\pi}{2}\\right), \\qquad "
    "\\cos\\theta = \\sin\\left(\\theta + \\frac{\\pi}{2}\\right)")

# B の向き（leading / lagging）
close("B>0 なら山は t<0", -0.927295 / 50, -0.018546, 5e-6)
inB("-\\frac{0.927}{50} = -0.0185 \\ \\text{秒}")
inB("で、**左へ $0.0185$ 秒移動します。**")
notB("$t = -\\dfrac{0.927}{50} = -0.0185$ 秒です。")
# 三角不等式の等号条件
s1, A1, _ = phasor_sum([(3, 0.4), (4, 0.4)])
close("同じ向きなら A = A1+A2", A1, 7, 1e-12)
s2, A2, _ = phasor_sum([(3, 0.4), (4, 0.9)])
eq("向きが違えば小さい", A2 < 7, True)
# 「真ん中」が成り立たない例（レビュー 3）
s3, A3, B3 = phasor_sum([(4, 2 * PI / 3), (4, -2 * PI / 3)])
close("差が π を超えると真ん中にならない", abs(B3), PI, 1e-12)
eq("その真ん中は 0 で、B とは違う", abs(B3 - 0.0) > 1, True)
# シラバスの Example
s4, A4, B4 = phasor_sum([(10, 0), (20, 10)])
close("Guidance の例 A", A4, 12.8207, 5e-4)
close("Guidance の例 B", B4, -2.12815, 5e-5)
eq("Guidance の例は第 3 象限", (s4.real < 0, s4.imag < 0), (True, True))

# ══════════════════════════════════════════════════════════════
# 3. シラバス・公式集から確かめた事実
# ══════════════════════════════════════════════════════════════
inA("z = r(\\cos\\theta + i\\sin\\theta) = r\\,e^{i\\theta} = r\\operatorname{cis}\\theta")
inA("見出しは「**Modulus-argument (polar) and exponential (Euler) form**」です。")
inA("> Modulus–argument (polar) form: $z = r(\\cos\\theta + i\\sin\\theta) = r\\operatorname{cis}\\theta$.")
inA("> Exponential form: $z = re^{i\\theta}$.")
inA("> Conversion between Cartesian, polar and exponential forms, by hand and with technology.")
inA("> Calculate products, quotients and integer powers in polar or exponential forms.")
inA("> Geometric interpretation of complex numbers.")
inA("> Exponential form is sometimes called the Euler form.")
inA("> In examinations students will not be required to find the roots of complex numbers.")
inA("> Addition and subtraction of complex numbers can be represented as vector addition and subtraction.")
inA("> Multiplication of complex numbers can be represented as a rotation and a stretch in the Argand diagram.")
inA("**積・商・べき乗の規則はどこにも印刷されていません。**")
inB("> Adding sinusoidal functions with the same frequencies but different phase shift angles.")
inB("> Phase shift and voltage in circuits as complex quantities.")
inB("> **Example:** Two AC voltage sources are connected in a circuit. "
    "If $V_1 = 10\\cos(40t)$ and $V_2 = 20\\cos(40t+10)$ find an expression "
    "for the total voltage in the form $V = A\\cos(40t+B)$.")
inB("> Knowledge of exact values of $\\cos\\theta$, $\\sin\\theta$, and "
    "$\\tan\\theta$ will not be assessed on examinations, but may aid "
    "student understanding of trigonometric functions.")

# ══════════════════════════════════════════════════════════════
# 4. GDC（TI 公式のガイドで確かめたもの）
# ══════════════════════════════════════════════════════════════
for T, tag in ((TA, "1.13a"), (TB, "1.13b")):
    eq(tag + " ctrl+doc は Document Settings に使わない",
       "ctrl + doc → Document Settings" in T, False)
inA("doc → Settings → Document Settings")
inB("doc → Settings → Document Settings")
inB("ctrl + doc → 2: Add Graphs")
inA("| `Real`（初期値） | 複素数の答えは出ず、`Error: Non-real result` のようになります |")

# ══════════════════════════════════════════════════════════════
# 5. レビューで直した点の見張り
# ══════════════════════════════════════════════════════════════
# 1.13a — 1: arg(iz) に z != 0 と範囲の但し書き
notA("$\\arg(iz) = \\arg z + \\frac{\\pi}{2}$ for every $z$.")
inA("for any $z \\neq 0$")
inA("$z = 0$ は原点そのもので、回しても動きません。")
# 2: GDC の angle() の範囲
inA("**`angle()` はいつも $-\\pi < \\theta \\leq \\pi$ で返す**")
# 3: arg の和の条件
# ★ 2026-08: arg の積は z1, z2 ≠ 0 が要る／2π の整数倍を除いて成り立つ
inA("- $\\arg(z_1 z_2) = \\arg z_1 + \\arg z_2$（**角は足し算**、$z_1 \\neq 0$、$z_2 \\neq 0$）")
inA("$1$ つ目は $z_1$、$z_2$ が何であっても成り立ちますが、$2$ つ目には条件が付きます。")
inA("**$z = 0$ の argument は定義されない**からです")
# 商のほうにも同じ条件を付けた
inA("argument の引き算も、$z_1 \\neq 0$、$z_2 \\neq 0$ のとき、**$2\\pi$ の整数倍のちがいを除いて**成り立ちます")
# 「実軸の上／虚軸の上」を「実軸上／虚軸上」にそろえた
notA("は虚軸の上なので")
notA("虚軸の下にある点")
notB("正の実軸の上の点なので")
inA("**そして、この足し算は $2\\pi$ の整数倍のちがいを除いて成り立ちます。**")
inA("principal argument として答えるときは、最後に $2\\pi$ を足し引きしてこの範囲へ戻してください")
notA("$2$ つ目は、$\\theta_1+\\theta_2$ が $-\\pi < \\theta \\leq \\pi$ の中にあるときの書き方です。")
inA("ここでは $z_2 \\neq 0$、つまり $r_2 \\neq 0$ とします。")
inA("ここでは $z_2 \\neq 0$、つまり $r_2 \\neq 0$ とします。")
# 4: Guidance の行数
notA("Guidance 欄には、次の $2$ 行があります。")
inA("Guidance 欄のうち、このページに関わるのは次の $2$ 行です。")
inA("Guidance 欄には、図の上での読み方を書いた $2$ 行")
# 5: AHL 3.8 は公式集の話
notA("（AHL 3.8 にあるのは $\\cos^{2}\\theta + \\sin^{2}\\theta = 1$ と "
     "$\\tan\\theta = \\dfrac{\\sin\\theta}{\\cos\\theta}$ だけです）")
inA("公式集の $3.8$ の欄に印刷されている identity も")
notB("**AI HL のシラバスに、加法定理はありません。** AHL 3.8 にあるのは")
inB("公式集の $3.8$ の欄に印刷されている identity も")
# 6: 回転と拡大の条件
notA("一般に $w$ をかけることは、**$\\arg w$ だけ回して、$\\lvert w \\rvert$ 倍に伸ばす**ことです。")
inA("$\\lvert w \\rvert < 1$ なら**縮み**")
inA("$w = 0$ をかけると、どの点も原点に移ります。")
# 7: 負の n には z != 0
notA("です。$n$ は整数なら、負でも構いません。")
inA("**$z \\neq 0$ なら $n$ は負の整数でも構いません。**")
# 8: GDC は小数で返す
notA("を `Polar` で打つと $2e^{(\\pi/3)i}$ のように返り")
inA("$2e^{1.05i}$ のように**小数の角**で返ります。")
notA("$2$ と $\\dfrac{\\pi}{3}$ が返ります。使い方は")
inA("$2$ と $1.05$ が返ります。$1.05 = \\dfrac{\\pi}{3}$ です。")
# 9: 三角不等式を本文に置いた
inA("$\\lvert z_1+z_2 \\rvert \\leq \\lvert z_1 \\rvert + \\lvert z_2 \\rvert$ です（@fig-ahl113a-mult の (b) の注記）")
# 10: 2pi の言い方
notA("**$2\\pi$ 足しても引いても同じ点**なので、値そのものは変わりません。")
inA("**$2\\pi$ 足しても引いても、指している点は同じ**です。")
# 12: 検算を独立なものに
notA("**検算。** $\\operatorname{cis}(2\\pi) = \\cos 2\\pi + i\\sin 2\\pi = 1 + 0i = 1$ です ✓")
inA("**検算。** $(1+\\sqrt{3}\\,i)^{6}$ を Cartesian form のまま展開しても $64$ になります")
# 13: 演習 1 の言い回し
notA("**$e^{0.927}$ と $i$ を落とさないでください。**")
inA("**$e^{0.927}$ のように、$i$ を落とさないでください。**")
# 14: 公式を裸で置かない
inA("Cartesian form でかけ算をするときは、$4$ 回かけて $i^{2} = -1$ を処理する必要がありました")
# 15: de Moivre
notA("**AI HL のシラバスには、この名前は出てきません。**")
inA("**AI HL のシラバスにも公式集にも、de Moivre's theorem という定理名は出てきません。**")

# 1.13b — 1: 0 になる場合
notB("### 1. 同じ周期の波を足すと、また同じ周期の波になります {#idea}")
inB("### 1. 同じ周期の波を足すと、同じ周期の波か、$0$ になります {#idea}")
notB("つまり、答えはいつも次の形に書けます。")
# ★ 2026-08: A = 0 のときは「書けない」ではなく「B が一意に決まらない」
inB("このとき $0\\cos(\\omega t + B)$ は**どの $B$ でも同じ $0$** になるので、**$B$ が $1$ つに決まりません。**")
inB("@eq-ahl113b-goal の右辺は、ふつう **$A > 0$** として求められるものなので、**その形では表せません。**")
notB("$A = 0$ で、$B$ は決まりません。")
notB("@eq-ahl113b-goal の形には書けないので、答えは $0$ とだけ書きます")
inB("足した複素数が $0$ になったときは、argument が決まりません。")
# 3: 「真ん中」の条件
notB("振幅が同じ $2$ つを足すと、合成の向きは**ちょうど真ん中**になります。")
inB("**いつでも真ん中、ではありません。**")
# 4: Guidance の Example と Content の行数
notB("Content 欄の $1$ 行です。")
inB("AHL 1.13 の Content 欄は $6$ 行あり")
inB("**この Example が、IB がこの項目について示している唯一の具体例**です。")
# 5: B は角
notB("$B$ は、合成した波が**もとの $\\cos\\omega t$ からどれだけ横にずれたか**を表します。")
# ★ 2026-08: phase の B と、時間軸の符号付き移動量 -B/ω を区別する
inB("これは **phase**（位相）であって、時間そのものではありません。")
inB("-\\frac{B}{\\omega} \\ \\text{秒}")
inB("ずれの**大きさ**だけを言うなら $\\dfrac{\\lvert B \\rvert}{\\omega}$ 秒です。")
inB("- $B > 0$ … $-\\dfrac{B}{\\omega} < 0$ なので**左**へ移動する（波が先に来る、**leading**）")
inB("- $B < 0$ … $-\\dfrac{B}{\\omega} > 0$ なので**右**へ移動する（波が遅れて来る、**lagging**）")
notB("時間でいうと $\\dfrac{B}{\\omega}$ 秒のずれです。")
notB("波は**左**にずれる（早く山が来る、**leading**）")
notB("波は**右**にずれる（遅れて山が来る、**lagging**）")
inB("**$0.927$ 秒ずれるのではありません。**")
# 6: sin 版の Why it works
inB("$\\sin\\theta = \\operatorname{Im}\\left(e^{i\\theta}\\right)$ から出発して")
# 7: exact values は問われない
inB("## 三角比の値そのものは、試験では聞かれません")
# 8: 図の描き方
inB("$3$ の矢印の先から $4i$ の矢印を**つないで**描いてあります。")
notB("矢印を足すと $3+4i$ になり、その modulus が $5$")
# 9: 三相の言い方
notB("これが三相交流で、家庭に届く電気の作り方そのものです。")
inB("発電所から送電線までの電気は、この $3$ 本の形で運ばれています。")
# 10: GDC の細部
inB("**$y$ の範囲も $-6 \\leq y \\leq 6$ にしてください。**")
inB("非CAS の CX II は数値で計算するので、どちらの表示でも**小数**で返ります。")

# ══════════════════════════════════════════════════════════════
# 6. 構造の不変条件
# ══════════════════════════════════════════════════════════════
HEADS = ["What you should be able to do", "The idea", "Why it works",
         "Worked examples", "Common errors",
         "Using your GDC (TI-Nspire CX II)", "Exercises"]
for tag, TXT, pref in (("1.13a", TA, "ahl113a"), ("1.13b", TB, "ahl113b")):
    h2 = [h for h in re.findall(r"^## (.+)$", TXT, re.M) if h in HEADS]
    eq(tag + " 7 見出し", h2, HEADS)
    eq(tag + " 例題 4 つ", len(re.findall(r"::: \{#exm-", TXT)), 4)
    eq(tag + " 演習 10 問", len(re.findall(r"\[\d+\]\{\.ex-no\}", TXT)), 10)
    eq(tag + " ex-sep 9 個", TXT.count(".ex-sep"), 9)
    eq(tag + " --- は 6 個", len(re.findall(r"^---$", TXT, re.M)), 6)
    eq(tag + " 日本語訳 14 個", TXT.count('<details class="jp-trans">'), 14)
    # 節番号が飛んでいない
    nums = [int(n) for n in re.findall(r"^### (\d+)\.", TXT, re.M)]
    idea = nums[:nums.index(1, 1)] if 1 in nums[1:] else nums
    eq(tag + " The idea の節番号が連番", idea, list(range(1, len(idea) + 1)))
    gdc = nums[nums.index(1, 1):]
    eq(tag + " GDC の節番号が連番", gdc, list(range(1, len(gdc) + 1)))
    for w in ("誰でもできる", "簡単です", "当然", "明らか", "もちろん",
              "当たり前", "確かめ。", "そのとおり", "ご指摘"):
        eq(tag + " 禁止語 " + w, w in TXT, False)
    eq(tag + " 検算がある", TXT.count("**検算。**") >= 3, True)
    bad = [m for m in re.findall(r"`[^`\n]*`", TXT) if "$" in m]
    eq(tag + " コードスパンに数式なし", bad, [])
    pipes = []
    for line in TXT.split("\n"):
        if line.strip().startswith("|"):
            pipes += [m for m in re.findall(r"\$[^$]*\$", line) if "|" in m]
    eq(tag + " 表の数式に | なし", pipes, [])
    lines = TXT.split("\n")
    nob = [i + 1 for i, l in enumerate(lines)
           if l.startswith("::: {") and i > 0 and lines[i - 1].strip() != ""]
    eq(tag + " ::: の前に空行", nob, [])
    ids = set(re.findall(r"\{#([A-Za-z0-9\-_]+)\}", TXT))
    miss = [a for a in re.findall(r"\]\(#([A-Za-z0-9\-_]+)\)", TXT)
            if a not in ids and a not in ("common-errors", "why-it-works",
                                          "exercises")]
    eq(tag + " ページ内リンクが解決", miss, [])
    xref = re.findall(r"@(?:exm|eq|fig|tbl)-([A-Za-z0-9]+)", TXT)
    eq(tag + " 他ページの crossref なし",
       [k for k in xref if not k.startswith(pref)], [])

eq("1.13a の model-answer 4 個", TA.count(".model-answer"), 4)
eq("1.13b の model-answer 5 個", TB.count(".model-answer"), 5)

IMG = os.path.join(HERE, "..", "..", "ai-hl", "01-number-and-algebra", "img")
for f in ("ahl-1-13a-forms.svg", "ahl-1-13a-mult.svg",
          "ahl-1-13b-add.svg", "ahl-1-13b-cancel.svg"):
    eq("図 " + f, os.path.exists(os.path.join(IMG, f)), True)
eq("png を残していない",
   [f for f in os.listdir(IMG) if f.startswith("ahl-1-13")
    and f.endswith(".png")], [])

# 登録
QY = io.open(os.path.join(HERE, "..", "..", "_quarto-draft.yml"),
             encoding="utf-8").read()
IX = io.open(os.path.join(HERE, "..", "..", "ai-hl", "index.qmd"),
             encoding="utf-8").read()
GL = io.open(os.path.join(HERE, "..", "..", "glossary-ai.qmd"),
             encoding="utf-8").read()
for s in ("ai-hl/01-number-and-algebra/ahl-1-13a.qmd",
          "ai-hl/01-number-and-algebra/ahl-1-13b.qmd",
          "AHL 1.13a — Polar and exponential form",
          "AHL 1.13b — Adding sinusoidal functions"):
    eq("_quarto-draft.yml に " + s[:44], s in QY, True)
for s in ("01-number-and-algebra/ahl-1-13a.qmd",
          "01-number-and-algebra/ahl-1-13b.qmd"):
    eq("index.qmd に " + s[:44], s in IX, True)
# 「残りの N 項目」が、✅ の付いていない項目表の行数と合っているか
_rows = re.findall(r"^\| (?:\*\*)?AHL [0-9.]+(?:\*\*)? \|(.*)\|$", IX, re.M)
_left_rows = [r for r in _rows if "\u2705" not in r]
_left = re.search(r"残りの(\d+)項目", IX)
eq("残りの N 項目 があるか、全部の行に ✅ が付いている",
   _left is not None or len(_left_rows) == 0, True)
if _left:
    eq("残りの N 項目 が、まだ書いていない行の数と合う",
       len(_left_rows), int(_left.group(1)))
for s in ("| polar form | 極形式 |", "| exponential form | 指数形式 |",
          "| Euler form | オイラー形式 |", "| cis | シス |",
          "| phasor | フェーザ |", "| frequency | 周波数 |",
          "| phase shift | 位相のずれ |", "| out of phase | 位相がずれている |",
          "| leading / lagging | 進み／遅れ |", "| rotation | 回転 |",
          "| stretch | 拡大・縮小 |",
          "| alternating current (AC) | 交流 |"):
    eq("glossary に " + s[:34], s in GL, True)
# ★ 2026-08: glossary でも phase angle と時間のずれを区別する
eq("glossary の phase shift 行",
   "| phase shift | 位相のずれ | **HL** $A\\cos(\\omega t + B)$ の $B$（角）。"
   "時間の移動量は $-\\dfrac{B}{\\omega}$ 秒 |" in GL, True)
eq("glossary が B を SL 2.5 の平行移動と同一視していない",
   "の $B$。SL 2.5 の横の平行移動" in GL, False)


# ══════════════════════════════════════════════════════════════
#  2026-08 の修正: cis は関数として扱ってよい（略記であることは残す）
# ══════════════════════════════════════════════════════════════
inA("## $\\operatorname{cis}\\theta$ は $1$ つのまとまりです")
inA("$\\operatorname{cis}$ は **c**osine と **i** **s**ine を組み合わせた**略記**で、")
inA("\\operatorname{cis}\\theta = \\cos\\theta + i\\sin\\theta")
inA("$\\cos\\theta \\times i \\times \\sin\\theta$ ではありません。")
notA("## $\\operatorname{cis}\\theta$ は「$\\operatorname{cis}$ という関数」ではありません")
notA("という関数」ではありません")
notA("関数ではありません")
# cis は関数として筋が通っている: |cis θ| = 1 と cis θ · cis φ = cis(θ+φ)
def _cis(t):
    return complex(math.cos(t), math.sin(t))


for _t in (0.0, 0.7, 2.5, -1.3, PI):
    close("|cis(%.2f)| = 1" % _t, abs(_cis(_t)), 1.0, 1e-12)
for _t, _u in ((0.7, 2.5), (-1.3, 0.4), (PI / 3, PI / 4)):
    close("cis(%.2f)cis(%.2f) = cis(和)" % (_t, _u),
          abs(_cis(_t) * _cis(_u) - _cis(_t + _u)), 0.0, 1e-12)
# 掛け算だと読んだ場合とは、まったく別の値になる
for _t in (0.7, 2.5):
    eq("cos·i·sin は cis と違う (%.1f)" % _t,
       abs(_cis(_t) - complex(0, math.cos(_t) * math.sin(_t))) > 0.5, True)

print("=" * 78)
print("結果:  OK %d / NG %d" % (OK, NG))
print("=" * 78)
sys.exit(1 if NG else 0)
