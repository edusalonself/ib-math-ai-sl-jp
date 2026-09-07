# -*- coding: utf-8 -*-
"""AHL 1.12a / 1.12b（complex numbers）の検算。
   1. すべての複素数の計算を sympy で第一原理から出す
   2. 図形（直角三角形・象限）と、解と係数の関係で独立に突き合わせる
   3. .qmd の本文が、その式・数値どおりに書かれているかを確かめる
   4. シラバスと公式集から確かめた事実を見張る
   5. レビューで直した点を not_in_text で見張る
   6. 構造の不変条件を確かめる
   実行: python3 figs/ai-hl/check_ahl_1_12.py
"""
import io
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(__file__)
A = os.path.join(HERE, "..", "..", "ai-hl", "01-number-and-algebra",
                 "ahl-1-12a.qmd")
B = os.path.join(HERE, "..", "..", "ai-hl", "01-number-and-algebra",
                 "ahl-1-12b.qmd")
TA = io.open(A, encoding="utf-8").read()
TB = io.open(B, encoding="utf-8").read()

OK = NG = 0
I = sp.I
x = sp.symbols("x")


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


inA, notA = _in(TA, "1.12a"), _not_in(TA, "1.12a")
inB, notB = _in(TB, "1.12b"), _not_in(TB, "1.12b")


def sf3(v):
    """有効数字 3 桁の文字列（本文の書き方に合わせる）。"""
    return sp.N(v, 3)


# ══════════════════════════════════════════════════════════════
# 1. 1.12a の四則
# ══════════════════════════════════════════════════════════════
z1, z2 = 3 + 2 * I, 1 - 5 * I
eq("z1+z2", sp.expand(z1 + z2), 4 - 3 * I)
eq("z1-z2", sp.expand(z1 - z2), 2 + 7 * I)
eq("z1*z2", sp.expand(z1 * z2), 13 - 13 * I)
quot = sp.nsimplify(sp.simplify(z1 / z2))
eq("z1/z2", quot, sp.Rational(-7, 26) + sp.Rational(17, 26) * I)
close("z1/z2 re", sp.re(quot), -0.269, 5e-4)
close("z1/z2 im", sp.im(quot), 0.654, 5e-4)
# 商の検算（本文の逆算）
eq("quot*z2 = z1", sp.expand(quot * z2), z1)
# 分母は実数になる
eq("(1-5i)(1+5i)", sp.expand((1 - 5 * I) * (1 + 5 * I)), 26)
eq("分子 (3+2i)(1+5i)", sp.expand((3 + 2 * I) * (1 + 5 * I)), -7 + 17 * I)

inA("(3+2i)(1-5i) &= 3 - 15i + 2i - 10i^{2}")
inA("= 13 - 13i")
inA("(3 + 2i) + (1 - 5i) = (3+1) + (2-5)i = 4 - 3i")
inA("(3 + 2i) - (1 - 5i) = (3-1) + (2+5)i = 2 + 7i")
inA("(3+2i)(1+5i) = 3 + 15i + 2i + 10i^{2} = -7 + 17i")
inA("\\frac{-7+17i}{26} = -\\frac{7}{26} + \\frac{17}{26}\\,i")
inA("$-0.269 + 0.654i$")

# conjugate
zc = 4 - I
eq("conj(4-i)", sp.conjugate(zc), 4 + I)
eq("z+z*", sp.expand(zc + sp.conjugate(zc)), 8)
eq("z z*", sp.expand(zc * sp.conjugate(zc)), 17)
eq("z-z*", sp.expand(zc - sp.conjugate(zc)), -2 * I)
inA("z + z^{*} = (4-i)+(4+i) = 8")
inA("z z^{*} = 4^{2} + (-1)^{2} = 16 + 1 = 17")
inA("z - z^{*} = (4-i) - (4+i) = -2i")

# i の累乗
eq("i^2", sp.expand(I ** 2), -1)
eq("i^3", sp.expand(I ** 3), -I)
eq("i^4", sp.expand(I ** 4), 1)
eq("i^23", sp.expand(I ** 23), -I)
eq("i^50", sp.expand(I ** 50), -1)
eq("50 = 4*12+2", (50 // 4, 50 % 4), (12, 2))
eq("23 = 4*5+3", (23 // 4, 23 % 4), (5, 3))
inA("i^{23} = i^{20} \\cdot i^{3} = (i^{4})^{5} \\cdot i^{3} = 1 \\cdot (-i) = -i")
inA("i^{50} = (i^{4})^{12} \\times i^{2} = 1^{12} \\times (-1) = -1")

# (1+i) の累乗
eq("(1+i)^2", sp.expand((1 + I) ** 2), 2 * I)
eq("(2i)^4", sp.expand((2 * I) ** 4), 16)
eq("(1+i)^8", sp.expand((1 + I) ** 8), 16)
inA("(1+i)^{2} = 1 + 2i + i^{2} = 1 + 2i - 1 = 2i")
inA("z^{8} = (z^{2})^{4} = (2i)^{4} = 16\\,i^{4} = 16")

# 根号の扱い
eq("sqrt(-36) = 6i", sp.sqrt(-36), 6 * I)
eq("sqrt(-20) = 2sqrt5 i", sp.sqrt(-20), 2 * sp.sqrt(5) * I)
inA("\\sqrt{-36} = \\sqrt{36}\\,i = 6i, \\qquad \\sqrt{-20} = \\sqrt{20}\\,i = 2\\sqrt{5}\\,i")

# ══════════════════════════════════════════════════════════════
# 2. 1.12a の 2 次方程式
# ══════════════════════════════════════════════════════════════
def disc(p):
    return sp.discriminant(p, x)


def roots(p):
    return sorted(sp.solve(p, x), key=lambda t: sp.im(t))


cases = [
    (x ** 2 - 4 * x + 13, -36, [2 - 3 * I, 2 + 3 * I]),
    (2 * x ** 2 + 2 * x + 5, -36,
     [sp.Rational(-1, 2) - sp.Rational(3, 2) * I,
      sp.Rational(-1, 2) + sp.Rational(3, 2) * I]),
    (x ** 2 - 6 * x + 25, -64, [3 - 4 * I, 3 + 4 * I]),
    (3 * x ** 2 + 4 * x + 3, -20,
     [sp.Rational(-2, 3) - sp.sqrt(5) * I / 3,
      sp.Rational(-2, 3) + sp.sqrt(5) * I / 3]),
    (x ** 2 + 9, -36, [-3 * I, 3 * I]),
    (x ** 2 + 6 * x + 10, -4, [-3 - I, -3 + I]),
    (x ** 2 + 4 * x + 20, -64, [-2 - 4 * I, -2 + 4 * I]),
    (x ** 2 - 2 * x + 10, -36, [1 - 3 * I, 1 + 3 * I]),
    (x ** 2 - 4 * x + 29, -100, [2 - 5 * I, 2 + 5 * I]),
]
for poly, d, rs in cases:
    eq("Delta %s" % poly, disc(poly), d)
    eq("roots %s" % poly, roots(poly), rs)

# 判別式が正・0 の 3 本（図の (a)）
eq("x^2-4x+3 disc", disc(x ** 2 - 4 * x + 3), 4)
eq("x^2-4x+3 roots", sorted(sp.solve(x ** 2 - 4 * x + 3, x)), [1, 3])
eq("x^2-4x+4 disc", disc(x ** 2 - 4 * x + 4), 0)
eq("x^2-4x+4 root", sp.solve(x ** 2 - 4 * x + 4, x), [2])
eq("x^2-4x+5 disc", disc(x ** 2 - 4 * x + 5), -4)
eq("x^2-4x+5 roots", roots(x ** 2 - 4 * x + 5), [2 - I, 2 + I])

# 代入による検算（本文の 検算 と同じ式）
zq = sp.Rational(-1, 2) + sp.Rational(3, 2) * I
eq("(-1/2+3/2 i)^2", sp.expand(zq ** 2), -2 - sp.Rational(3, 2) * I)
eq("代入 2z^2+2z+5", sp.expand(2 * zq ** 2 + 2 * zq + 5), 0)
inA("2\\left(-2-\\tfrac{3}{2}i\\right) + 2\\left(-\\tfrac{1}{2}+\\tfrac{3}{2}i\\right) + 5 = -4 - 3i - 1 + 3i + 5 = 0")
z6 = 3 + 4 * I
eq("(3+4i)^2", sp.expand(z6 ** 2), -7 + 24 * I)
eq("代入 z^2-6z+25", sp.expand(z6 ** 2 - 6 * z6 + 25), 0)
inA("(-7+24i) - 6(3+4i) + 25 = -7 + 24i - 18 - 24i + 25 = 0")
eq("(2+3i)代入", sp.expand((2 + 3 * I) ** 2 - 4 * (2 + 3 * I) + 13), 0)

# 3 s.f.
close("3x^2+4x+3 re", sp.re(roots(3 * x ** 2 + 4 * x + 3)[1]), -0.667, 5e-4)
close("3x^2+4x+3 im", sp.im(roots(3 * x ** 2 + 4 * x + 3)[1]), 0.745, 5e-4)
inA("x = -0.667 + 0.745i \\quad \\text{or} \\quad x = -0.667 - 0.745i")

# 頂点（グラフとの関係）
eq("2x^2+2x+5 の頂点 y", sp.Rational(2) * sp.Rational(1, 4) - 1 + 5,
   sp.Rational(9, 2))
# k の最大値
close("sqrt40", float(sp.sqrt(40)), 6.32456, 1e-4)
eq("k=6 は Delta<0", disc(x ** 2 + 6 * x + 10) < 0, True)
eq("k=7 は Delta>0", disc(x ** 2 + 7 * x + 10) > 0, True)
eq("k=6 の Delta", disc(x ** 2 + 6 * x + 10), -4)
inA("\\sqrt{40} = 6.32\\ldots")
inA("\\Delta = 6^{2}-4(1)(10) = -4$, which is negative")

# その他の演習
eq("(5+3i)+(2-4i)", sp.expand((5 + 3 * I) + (2 - 4 * I)), 7 - I)
eq("(5+3i)-(2-4i)", sp.expand((5 + 3 * I) - (2 - 4 * I)), 3 + 7 * I)
eq("3z1+2z2", sp.expand(3 * (5 + 3 * I) + 2 * (2 - 4 * I)), 19 + I)
eq("(4-3i)(2+5i)", sp.expand((4 - 3 * I) * (2 + 5 * I)), 23 + 14 * I)
eq("(2+i)/(3-i)", sp.nsimplify(sp.simplify((2 + I) / (3 - I))),
   sp.Rational(1, 2) + sp.Rational(1, 2) * I)
eq("検算 (1/2+1/2 i)(3-i)",
   sp.expand((sp.Rational(1, 2) + sp.Rational(1, 2) * I) * (3 - I)), 2 + I)
eq("(3-7i) conj", sp.conjugate(3 - 7 * I), 3 + 7 * I)
eq("(3-7i)+(3+7i)", sp.expand((3 - 7 * I) + (3 + 7 * I)), 6)
eq("(3-7i)(3+7i)", sp.expand((3 - 7 * I) * (3 + 7 * I)), 58)
eq("(2+i)^2", sp.expand((2 + I) ** 2), 3 + 4 * I)
eq("(2+i)^4", sp.expand((2 + I) ** 4), -7 + 24 * I)
inA("(4-3i)(2+5i) = 8 + 20i - 6i - 15i^{2} = 8 + 14i + 15 = 23 + 14i")
inA("\\frac{5+5i}{10} = \\frac{1}{2} + \\frac{1}{2}i")
inA("z z^{*} = 3^{2} + 7^{2} = 9 + 49 = 58")
inA("(3+4i)^{2} = 9 + 24i + 16i^{2} = 9 + 24i - 16 = -7 + 24i")
inA("x = \\pm\\sqrt{9}\\,i = \\pm 3i")

# ══════════════════════════════════════════════════════════════
# 3. 1.12b の modulus と argument
# ══════════════════════════════════════════════════════════════
def mod(z):
    return sp.Abs(sp.sympify(z))


def arg(z):
    return sp.arg(sp.sympify(z))


eq("|3+2i|", mod(3 + 2 * I), sp.sqrt(13))
close("|3+2i| 3sf", mod(3 + 2 * I), 3.61, 5e-3)
close("arg(3+2i)", arg(3 + 2 * I), 0.588, 5e-4)
eq("|-3+2i|", mod(-3 + 2 * I), sp.sqrt(13))
close("arg(-3+2i)", arg(-3 + 2 * I), 2.55359, 5e-4)
close("arctan(2/-3)", sp.atan(sp.Rational(2, -3)), -0.588003, 5e-6)
close("-0.588+pi", -0.588003 + float(sp.pi), 2.55359, 1e-4)
# 象限の規則が -pi < theta <= pi に収まることを、たくさんの点で確かめる
for a in (-4, -3, -1, 1, 3, 5):
    for b in (-4, -2, -1, 1, 2, 6):
        z = a + b * I
        t = float(arg(z))
        eq("範囲 %s" % z, (-sp.pi < arg(z)) and (arg(z) <= sp.pi), True)
        if a > 0:
            close("Q1/Q4 %s" % z, t, float(sp.atan(sp.Rational(b, a))), 1e-9)
        elif b > 0:
            close("Q2 %s" % z, t,
                  float(sp.atan(sp.Rational(b, a)) + sp.pi), 1e-9)
        else:
            close("Q3 %s" % z, t,
                  float(sp.atan(sp.Rational(b, a)) - sp.pi), 1e-9)
# 軸の上の点
eq("arg(2i)", arg(2 * I), sp.pi / 2)
eq("arg(-2i)", arg(-2 * I), -sp.pi / 2)
eq("arg(5)", arg(sp.Integer(5)), 0)
eq("arg(-5)", arg(sp.Integer(-5)), sp.pi)
eq("arctan(0/-5) は 0（だから図では決まらない）", sp.atan(sp.Rational(0, -5)), 0)

inB("\\lvert 3+2i \\rvert = \\sqrt{3^{2}+2^{2}} = \\sqrt{13} = 3.61")
inB("\\arg z = \\arctan\\frac{2}{3} = 0.588")
inB("\\arctan\\frac{2}{-3} = -0.588")
inB("\\arg w = -0.588 + \\pi = 2.55")
inB("| 正の実軸上（$a>0$、$b=0$） | $0$ |")
inB("| 負の実軸上（$a<0$、$b=0$） | $\\pi$ |")
# ★ レビュー: 「〜の上」→「〜上」（軸の上に乗っている、の意味で統一）
inB("| 正の虚軸上（$a=0$、$b>0$） | $\\dfrac{\\pi}{2}$ |")
inB("| 負の虚軸上（$a=0$、$b<0$） | $-\\dfrac{\\pi}{2}$ |")
notB("正の実軸の上（")
notB("負の実軸の上（")
notB("虚軸の上（")
notB("虚軸の下（")

# 例題・演習の値
eq("|5-12i|", mod(5 - 12 * I), 13)
eq("|-1+i|", mod(-1 + I), sp.sqrt(2))
eq("arg(-1+i)", arg(-1 + I), 3 * sp.pi / 4)
eq("arg(-2-2i)", arg(-2 - 2 * I), -3 * sp.pi / 4)
close("3pi/4", 3 * sp.pi / 4, 2.35619, 5e-5)
eq("|4+3i|", mod(4 + 3 * I), 5)
eq("|4-3i|", mod(4 - 3 * I), 5)
eq("|-2+4i|", mod(-2 + 4 * I), sp.sqrt(20))
close("sqrt20", sp.sqrt(20), 4.47, 5e-3)
eq("|1+3i|", mod(1 + 3 * I), sp.sqrt(10))
close("sqrt10", sp.sqrt(10), 3.16, 5e-3)
eq("|40+30i|", mod(40 + 30 * I), 50)
close("arg(40+30i)", arg(40 + 30 * I), 0.643501, 5e-6)
close("arg(40+30i) deg", sp.deg(arg(40 + 30 * I)), 36.8699, 1e-4)
eq("|60+80i|", mod(60 + 80 * I), 100)
close("arg(60+80i)", arg(60 + 80 * I), 0.927295, 5e-6)
eq("|z1-z2| = 5", mod((2 + 3 * I) - (-1 - I)), 5)
eq("z1-z2", sp.expand((2 + 3 * I) - (-1 - I)), 3 + 4 * I)
eq("|3+ki|=5 の k", sorted(sp.solve(sp.Eq(9 + sp.Symbol("k") ** 2, 25))),
   [-4, 4])
eq("arg(-4+4i)", arg(-4 + 4 * I), 3 * sp.pi / 4)
eq("arctan(4/-4)", sp.atan(sp.Rational(4, -4)), -sp.pi / 4)
# 共役な組の関係
for z in (1 + 3 * I, -2 + 4 * I, 3 + 2 * I, -3 + 2 * I, 5 - 12 * I):
    eq("|z|=|z*| %s" % z, mod(z), mod(sp.conjugate(z)))
    eq("arg(z*)=-arg(z) %s" % z, arg(sp.conjugate(z)), -arg(z))

inB("\\lvert z \\rvert = \\sqrt{5^{2}+(-12)^{2}} = \\sqrt{25+144} = \\sqrt{169} = 13")
inB("\\arg z = -\\frac{\\pi}{4} + \\pi = \\frac{3\\pi}{4}")
inB("\\arg z = \\frac{\\pi}{4} - \\pi = -\\frac{3\\pi}{4}")
inB("\\lvert Z \\rvert = \\sqrt{40^{2}+30^{2}} = \\sqrt{2500} = 50")
inB("\\arg Z = \\arctan\\frac{30}{40} = \\arctan 0.75 = 0.644")
inB("\\lvert Z \\rvert = \\sqrt{60^{2}+80^{2}} = \\sqrt{10000} = 100 \\text{ ohms}")
inB("\\arg Z = \\arctan\\frac{80}{60} = 0.927 \\text{ radians}")
inB("\\lvert z_1 - z_2 \\rvert = \\sqrt{3^{2}+4^{2}} = 5")
inB("k^{2} = 16 \\ \\Rightarrow \\ k = 4")
inB("\\lvert -2 \\pm 4i \\rvert = \\sqrt{(-2)^{2}+4^{2}} = \\sqrt{20} = 4.47")
inB("0.644$ radian は $36.9^{\\circ}$")

# ══════════════════════════════════════════════════════════════
# 4. 図形・解と係数の関係による独立な突き合わせ
# ══════════════════════════════════════════════════════════════
# |z|^2 = c/a （係数が実数で Delta < 0 のとき）
for poly in (x ** 2 - 2 * x + 10, x ** 2 + 4 * x + 20, x ** 2 - 4 * x + 29,
             2 * x ** 2 + 2 * x + 5, x ** 2 - 6 * x + 25):
    p = sp.Poly(poly, x)
    a, b, c = p.all_coeffs()
    r = roots(poly)[0]
    eq("|z|^2 = c/a %s" % poly, sp.simplify(mod(r) ** 2 - sp.Rational(c, a)), 0)
# 反例：Delta > 0 では成り立たない
eq("x^2-4 は c/a が負", sp.Rational(-4, 1) < 0, True)
eq("x^2-4 の解は実数", sorted(sp.solve(x ** 2 - 4, x)), [-2, 2])
inB("$x^{2}-4 = 0$ では $\\dfrac{c}{a} = -4$ と負になり")
# 解の和と積（演習 6）
eq("和 (2+5i)+(2-5i)", sp.expand((2 + 5 * I) + (2 - 5 * I)), 4)
eq("積 (2+5i)(2-5i)", sp.expand((2 + 5 * I) * (2 - 5 * I)), 29)
eq("x^2-4x+29 の解", roots(x ** 2 - 4 * x + 29), [2 - 5 * I, 2 + 5 * I])
# Pythagoras との突き合わせ（3-4-5 と 5-12-13）
eq("3-4-5", sp.sqrt(3 ** 2 + 4 ** 2), 5)
eq("5-12-13", sp.sqrt(5 ** 2 + 12 ** 2), 13)
eq("40-30-50", sp.sqrt(40 ** 2 + 30 ** 2), 50)

# ══════════════════════════════════════════════════════════════
# 5. シラバス・公式集から確かめた事実
# ══════════════════════════════════════════════════════════════
inA("> Complex numbers: the number $i$ such that $i^{2} = -1$.")
inA("> Calculating powers of complex numbers, in Cartesian form, with technology.")
inA("> Quadratic formula and the link with the graph of $f(x) = ax^{2}+bx+c$.")
inA("**Topic 2 の「Prior learning – HL」**の欄に、解の公式そのものが載っています。")
inA("$2$ つ目の見出しは「**Discriminant**」（判別式）です。")
inA("AI **SL** の公式集を最後まで見ても、$x = \\dfrac{-b \\pm \\sqrt{b^{2}-4ac}}{2a}$ は出てきません。")
inB("> On HL examination papers radian measure should be assumed unless otherwise indicated.")
inB("> Use and draw Argand diagrams.")
inB("> Cartesian form: $z=a+bi$; the terms real part, imaginary part, conjugate, **modulus and argument**.")
inB("z = r(\\cos\\theta + i\\sin\\theta) = r\\,e^{i\\theta} = r\\operatorname{cis}\\theta")
inB("**$a$ と $b$ から $r$ と $\\theta$ を出す式は、どこにも印刷されていません。**")
inB("d = \\sqrt{(x_1-x_2)^{2}+(y_1-y_2)^{2}}")
# 「Content 欄は 1 行」という誤りが復活していないこと
notB("Content 欄は $1$ 行です。")
notB("Guidance 欄も $1$ 行です。")

# ══════════════════════════════════════════════════════════════
# 6. GDC の記述（TI 公式のガイドで確かめたもの）
# ══════════════════════════════════════════════════════════════
# Document Settings は doc → Settings、ページ追加は ctrl + doc
for T, tag in ((TA, "1.12a"), (TB, "1.12b")):
    eq(tag + " ctrl+doc は Document Settings に使わない",
       "ctrl + doc → Document Settings" in T, False)
inA("doc → Settings → Document Settings")
inB("doc → Settings → Document Settings → Angle: Radian")
inB("ctrl + doc → Add Lists & Spreadsheet")
inA("`Real or Complex` を **`Rectangular`** にしてください。")
inA("TI 公式のガイドでは、handheld で `ctrl` と `k` を押すとパレットが開く、と書かれています。")
inB("TI 公式のガイドでは、handheld で `ctrl` と `k` を押すとパレットが開く、と書かれています。")
inA("`conj(3+2i)`")
inA("`real(3+2i)`")
inA("`imag(3+2i)`")
inB("abs(3+2i)")
inB("angle(-3+2i)")

# ══════════════════════════════════════════════════════════════
# 7. レビューで直した点の見張り
# ══════════════════════════════════════════════════════════════
# 1.12a — 1: sqrt の法則に条件を付けた
inA("$\\sqrt{a} \\times \\sqrt{b} = \\sqrt{ab}$ という法則が使えるのは、**$a \\geq 0$ かつ $b \\geq 0$ のとき**だけ")
notA("\\sqrt{-36} = \\sqrt{36 \\times (-1)} = 6i")
# 2: 非CAS の挙動
notA("そのときは、答えが計算されずに式のまま返ってきます。")
inA("非CAS の CX II は値の入っていない変数を計算できないので、そこで止まってエラーの表示が出ます。")
inA("`i^2` と打つのがいちばん速い確かめ方です。")
# 3: 検算は代入に変えた
notA("$2$ つの解の積は $\\left(-\\tfrac{1}{2}\\right)^{2} + \\left(\\tfrac{3}{2}\\right)^{2}")
notA("$2$ つの解の積は $3^{2}+4^{2} = 25$ で、$\\dfrac{c}{a} = 25$ と一致します")
inA("**検算。** 解を元の式に入れ直します。")
# 4: without using technology を消した
notA("without using technology")
notA("技術を使わずに $z^{8}$ を求めなさい")
# 5: 4 乗という誤った案内を消した
notA("手で $4$ 乗くらいまでを出す方法は")
# 6: Polynomial Root Finder は小数を返す
inA("返ってくるのは $-0.5 + 1.5\\,i$ と $-0.5 - 1.5\\,i$ のような**小数**です。")
# 8: 過去形をやめた
notA("[AHL 5.17b](../05-calculus/ahl-5-17b.qmd#gdc-complex) でも同じ設定を使いました。")
# 9: 英語ファースト
inA("**complex plane**（複素平面）と **modulus**（絶対値）・**argument**（偏角）")
notA("複素平面（complex plane）と modulus・argument は")
inA("#### なぜ、いつも **conjugate pair**（共役な組）になるのか {#why-pair}")
# 10: 符号の説明
notA("符号が $2$ 回ひっくり返ります。")
notA("**符号が $2$ 回ひっくり返る**ところなので")
inA("**負の数どうしをかけると正になる**ので、符号が $-$ から $+$ に変わります。")
# 12: 表の行
inA("| $\\Delta < 0$ | 交わらない | **実数ではない複素数が $2$ つ** |")

# 1.12b — 1: シラバスの引用を直した
inB("AHL 1.12 の Content 欄は $5$ 行あり")
inB("**modulus と argument は、Content 欄に名前が挙がっています。**")
# 2: 実軸の行を足した
inB("$b = 0$ の行、つまり実軸上の点は、どの象限にも入りません。")
notB("実軸の上の点は")
inB("$\\pi$ と $-\\pi$ が図の上で**同じ向き**を指すので、絵を見ても決まりません。")
# 3: 条件
notB("**この式が使えるのは $\\Delta < 0$ のときだけ**です。解が実数の $2$ つなら")
inB("**この式が使えるのは、係数が実数で $\\Delta < 0$ のとき**です。")
# 4: tan の含意を直した
notB("\\tan\\theta = \\frac{2}{3} \\quad \\Longrightarrow \\quad \\theta = \\arctan\\frac{2}{3} = 0.588")
inB("です。点 $(3,\\ 2)$ は第 $1$ 象限にあるので、この $\\theta$ は")
# 5: 番号つきリスト
notB("$1$. **点をかいて、どの象限にあるか見る**")
inB("1. **点をかいて、どの象限にあるか見る**")
# 6: 見出しに条件
inB("### 6. $\\Delta < 0$ のとき、$2$ つの解は実軸に関して対称に並びます {#roots}")
notB("### 6. $2$ 次方程式の解は、実軸に関して対称に並びます {#roots}")
inB("- 実数係数の $2$ 次方程式で $\\Delta < 0$ のとき、解が実軸に関して**対称な $2$ 点**になることを説明できる。")
# 7: principal argument の条件
notB("**principal argument**（主偏角）といい、GDC もこの範囲で返します。")
inB("GDC の `angle()` も、`Angle` を `Radian` にしてあれば、この範囲の値を返します。")
# 8: 訳語の統一
notB("**Argand diagram**（複素平面の図）")
eq("1.12b Argand diagram の訳は 1 通り（冒頭の箇条書きと初出の 2 か所）",
   TB.count("Argand diagram**（アルガン図）"), 2)
# 10: GDC の検算の言い方
notB("$3$ つ目は、解そのものを打ち直さずに済むので速く終わります。")
inB("$3$ つ目は、元の方程式に代入し直さずに済むので速く終わります。")
# 11: 列に名前を付ける
inB("**名前を付けないと、Data & Statistics ページで軸に選べません。**")
# 12: つぶれた三角形
inB("$a$ と $b$ のどちらかが $0$ のときは三角形がつぶれますが")
# 14: arctan の値域の言い方
notB("$\\arctan$ が返すのは $-\\dfrac{\\pi}{2}$ から $\\dfrac{\\pi}{2}$ までの角")
eq("1.12b strictly between が 3 か所",
   TB.count("strictly between $-\\frac{\\pi}{2}$ and $\\frac{\\pi}{2}$"), 3)

# ══════════════════════════════════════════════════════════════
# 8. 構造の不変条件
# ══════════════════════════════════════════════════════════════
HEADS = ["What you should be able to do", "The idea", "Why it works",
         "Worked examples", "Common errors",
         "Using your GDC (TI-Nspire CX II)", "Exercises"]
for tag, TXT in (("1.12a", TA), ("1.12b", TB)):
    h2 = [h for h in re.findall(r"^## (.+)$", TXT, re.M) if h in HEADS]
    eq(tag + " 7 見出し", h2, HEADS)
    eq(tag + " 例題 4 つ", len(re.findall(r"::: \{#exm-", TXT)), 4)
    eq(tag + " 演習 10 問", len(re.findall(r"\[\d+\]\{\.ex-no\}", TXT)), 10)
    eq(tag + " ex-sep 9 個", TXT.count(".ex-sep"), 9)
    eq(tag + " --- は 6 個（front matter 2 + 例題 4）",
       len(re.findall(r"^---$", TXT, re.M)), 6)
    eq(tag + " 日本語訳の折りたたみ 14 個",
       TXT.count('<details class="jp-trans">'), 14)
    # 禁止語
    for w in ("誰でもできる", "簡単です", "当然", "明らか", "もちろん",
              "当たり前", "確かめ。", "そのとおり", "ご指摘"):
        eq(tag + " 禁止語 " + w, w in TXT, False)
    # 検算の表記
    eq(tag + " 検算がある", TXT.count("**検算。**") >= 3, True)
    # コードスパンに数式を入れない
    bad = [m for m in re.findall(r"`[^`\n]*`", TXT) if "$" in m]
    eq(tag + " コードスパンに数式なし", bad, [])
    # 表のセルの $…$ に | を入れない
    pipes = []
    for line in TXT.split("\n"):
        if line.strip().startswith("|"):
            pipes += [m for m in re.findall(r"\$[^$]*\$", line) if "|" in m]
    eq(tag + " 表の数式に | なし", pipes, [])
    # ::: の前に空行
    lines = TXT.split("\n")
    nob = [i + 1 for i, l in enumerate(lines)
           if l.startswith("::: {") and i > 0 and lines[i - 1].strip() != ""]
    eq(tag + " ::: の前に空行", nob, [])
    # ページ内アンカーが解決する
    ids = set(re.findall(r"\{#([A-Za-z0-9\-_]+)\}", TXT))
    miss = [a for a in re.findall(r"\]\(#([A-Za-z0-9\-_]+)\)", TXT)
            if a not in ids and a != "common-errors"]
    eq(tag + " ページ内リンクが解決", miss, [])
    # ページをまたぐ crossref を使わない
    xref = re.findall(r"@(?:exm|eq|fig|tbl)-([A-Za-z0-9]+)", TXT)
    pref = "ahl112a" if tag == "1.12a" else "ahl112b"
    eq(tag + " 他ページの crossref なし",
       [k for k in xref if not k.startswith(pref)], [])

eq("1.12a の model-answer 3 個", TA.count(".model-answer"), 3)
eq("1.12b の model-answer 6 個", TB.count(".model-answer"), 6)

# 図が存在する
IMG = os.path.join(HERE, "..", "..", "ai-hl", "01-number-and-algebra", "img")
for f in ("ahl-1-12a-disc.svg", "ahl-1-12b-argand.svg",
          "ahl-1-12b-roots.svg"):
    eq("図 " + f, os.path.exists(os.path.join(IMG, f)), True)
# 一時的な png を残さない
eq("png を残していない",
   [f for f in os.listdir(IMG) if f.startswith("ahl-1-12")
    and f.endswith(".png")], [])

# 登録
QY = io.open(os.path.join(HERE, "..", "..", "_quarto-draft.yml"),
             encoding="utf-8").read()
IX = io.open(os.path.join(HERE, "..", "..", "ai-hl", "index.qmd"),
             encoding="utf-8").read()
GL = io.open(os.path.join(HERE, "..", "..", "glossary-ai.qmd"),
             encoding="utf-8").read()
for s in ("ai-hl/01-number-and-algebra/ahl-1-12a.qmd",
          "ai-hl/01-number-and-algebra/ahl-1-12b.qmd",
          "AHL 1.12a — Complex numbers in Cartesian form",
          "AHL 1.12b — The complex plane"):
    eq("_quarto-draft.yml に " + s[:44], s in QY, True)
for s in ("01-number-and-algebra/ahl-1-12a.qmd",
          "01-number-and-algebra/ahl-1-12b.qmd"):
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
for s in ("| discriminant | 判別式 |", "| Argand diagram | アルガン図 |",
          "| argument | 偏角 |", "| principal argument | 主偏角 |",
          "| complex plane | 複素平面 |", "| imaginary unit | 虚数単位 |",
          "| Cartesian form | 直交形式 |", "| conjugate | 共役複素数 |",
          "| impedance | インピーダンス |", "| phase angle | 位相角 |"):
    eq("glossary に " + s[:34], s in GL, True)
# AA に discriminant がない、という誤った記述を消した
eq("glossary の AA の例から discriminant を外した",
   "proof や discriminant のように AI では出てこない" in GL, False)


# ══════════════════════════════════════════════════════════
#  2026-08 の修正: z = 0 の例外を第5節にも引き継いだ
# ══════════════════════════════════════════════════════════
inB("$z = 0$ のときは向きが決まらないので、argument は定義されません。")
inB("**$z \\neq 0$ なら**、この $2$ つがそろえば、点の場所は $1$ つに決まります。")
notB("$\\arg z$ は「どの向きか」です。この $2$ つがそろえば、点の場所は $1$ つに決まります。")

print("=" * 78)
print("結果:  OK %d / NG %d" % (OK, NG))
print("=" * 78)
sys.exit(1 if NG else 0)
