# -*- coding: utf-8 -*-
"""AHL 5.18（2階微分方程式）の検算。
   1. すべての数値を第一原理から計算する（Euler は手順どおりに回す）
   2. sympy による独立な実装と突き合わせる（厳密解・固有値）
   3. .qmd の本文が、その数値どおりに書かれているかを確かめる
   4. シラバスと公式集から確かめた事実が、あとで変わっていないかを見張る
   5. 構造の不変条件を確かめる
   実行: python3 figs/ai-hl/check_ahl_5_18.py
"""
import io
import math
import os
import re
import sys

import sympy as sp

QMD = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "05-calculus", "ahl-5-18.qmd")
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


# ══════════════════════════════════════════════════════════════
# 1. Euler 法を、手順どおりに回す（図を描くためではなく検算のため）
# ══════════════════════════════════════════════════════════════
def euler(f, x0, y0, h, n, t0=0.0):
    """dx/dt = y, dy/dt = f(x, y, t) を Euler 法で n 歩。"""
    rows = [(t0, x0, y0)]
    t, x, y = t0, x0, y0
    for _ in range(n):
        xn = x + h * y             # ★ 古い y を使う
        yn = y + h * f(x, y, t)    # ★ 古い x, y を使う
        t, x, y = t + h, xn, yn
        rows.append((t, x, y))
    return rows


# 例題1・例題2 の式  x'' + 3x' + 2x = 0
fA = lambda x, y, t: -2 * x - 3 * y
rA = euler(fA, 1.0, 0.0, 0.1, 2)
eq("例題1 x1", round(rA[1][1], 10), 1.0)
eq("例題1 y1", round(rA[1][2], 10), -0.2)
eq("例題1 x2", round(rA[2][1], 10), 0.98)
eq("例題1 y2", round(rA[2][2], 10), -0.34)
# 「古い値を使う」を破ると値が変わることを確かめる（Common errors の根拠）
y2_wrong = -0.2 + 0.1 * (-2 * 0.98 - 3 * (-0.2))
close("新しい x を使うと答えが変わる", round(y2_wrong, 4), -0.336)

# 演習3 の式  x'' + 4x' + 3x = 0
fB = lambda x, y, t: -3 * x - 4 * y
rB = euler(fB, 2.0, 0.0, 0.1, 2)
eq("演習3 x1", round(rB[1][1], 10), 2.0)
eq("演習3 y1", round(rB[1][2], 10), -0.6)
eq("演習3 x2", round(rB[2][1], 10), 1.94)
eq("演習3 y2", round(rB[2][2], 10), -0.96)

# 例題4 の式  x'' = sin t - 0.5 x' - x
fC = lambda x, y, t: math.sin(t) - 0.5 * y - x
rC = euler(fC, 0.0, 1.0, 0.1, 2)
close("例題4 x1", rC[1][1], 0.1)
close("例題4 y1", rC[1][2], 0.95)
close("例題4 x2", rC[2][1], 0.195)
close("例題4 y2 (3桁)", round(rC[2][2], 3), 0.902)
close("sin 0.1 は radian で 0.0998", round(math.sin(0.1), 4), 0.0998)
close("degree のままだと 0.00175", round(math.sin(math.radians(0.1)), 5), 0.00175)


# ══════════════════════════════════════════════════════════════
# 2. sympy による独立な実装（厳密解・固有値）
# ══════════════════════════════════════════════════════════════
t = sp.symbols("t")
lam = sp.symbols("lambda")


def matrix_of(a, b):
    return sp.Matrix([[0, 1], [-b, -a]])


def eigen(a, b):
    return sorted(matrix_of(a, b).eigenvals().keys(), key=lambda z: sp.re(z))


def solve_ivp(a, b, x0, v0):
    x = sp.Function("x")
    ode = sp.Derivative(x(t), t, 2) + a * sp.Derivative(x(t), t) + b * x(t)
    s = sp.dsolve(ode, x(t),
                  ics={x(0): x0, sp.Derivative(x(t), t).subs(t, 0): v0})
    return sp.simplify(s.rhs)


# ── x'' + 3x' + 2x = 0 ────────────────────────────────────────
eq("例題2 行列", matrix_of(3, 2), sp.Matrix([[0, 1], [-2, -3]]))
eq("例題2 特性方程式", sp.expand(matrix_of(3, 2).charpoly(lam).as_expr()),
   sp.expand(lam ** 2 + 3 * lam + 2))
eq("例題2 固有値", eigen(3, 2), [-2, -1])
XA = 2 * sp.exp(-t) - sp.exp(-2 * t)
eq("例題2 厳密解が sympy と一致",
   sp.simplify(solve_ivp(3, 2, 1, 0) - XA), 0)
eq("例題2 解が式をみたす",
   sp.simplify(sp.diff(XA, t, 2) + 3 * sp.diff(XA, t) + 2 * XA), 0)
eq("例題2 x(0) = 1", XA.subs(t, 0), 1)
eq("例題2 x'(0) = 0", sp.diff(XA, t).subs(t, 0), 0)
close("例題2 x(0.2) = 0.967", round(float(XA.subs(t, sp.Rational(1, 5))), 3), 0.967)
close("Euler との差", round(0.98 - float(XA.subs(t, sp.Rational(1, 5))), 3), 0.013)
close("Euler との差は約 1.4%",
      round(100 * (0.98 - float(XA.subs(t, sp.Rational(1, 5))))
            / float(XA.subs(t, sp.Rational(1, 5))), 1), 1.3)

# eigenvector が (1, lambda) になること
for a, b in ((3, 2), (5, 6), (4, 3), (0, -1)):
    M = matrix_of(a, b)
    for l in M.eigenvals():
        v = sp.Matrix([1, l])
        eq("(1, lambda) が固有ベクトル (a=%s,b=%s,l=%s)" % (a, b, l),
           sp.simplify(M * v - l * v), sp.Matrix([0, 0]))

# ── x'' + 2x' + 5x = 0（複素） ─────────────────────────────────
eq("例題3 行列", matrix_of(2, 5), sp.Matrix([[0, 1], [-5, -2]]))
eq("例題3 判別式", 2 ** 2 - 4 * 5, -16)
eq("例題3 固有値", sorted(matrix_of(2, 5).eigenvals().keys(), key=sp.im),
   [-1 - 2 * sp.I, -1 + 2 * sp.I])

# ── x'' + 4x = 0（純虚数） ────────────────────────────────────
eq("純虚数の場合の固有値",
   sorted(matrix_of(0, 4).eigenvals().keys(), key=sp.im),
   [-2 * sp.I, 2 * sp.I])

# ── 演習4・5  x'' + 5x' + 6x = 0 ──────────────────────────────
eq("演習4 行列", matrix_of(5, 6), sp.Matrix([[0, 1], [-6, -5]]))
eq("演習4 固有値", eigen(5, 6), [-3, -2])
eq("演習4 trace", matrix_of(5, 6).trace(), -5)
eq("演習4 det", matrix_of(5, 6).det(), 6)
XB = 3 * sp.exp(-2 * t) - 2 * sp.exp(-3 * t)
eq("演習5 厳密解が sympy と一致", sp.simplify(solve_ivp(5, 6, 1, 0) - XB), 0)
eq("演習5 解が式をみたす",
   sp.simplify(sp.diff(XB, t, 2) + 5 * sp.diff(XB, t) + 6 * XB), 0)
eq("演習5 x(0) = 1", XB.subs(t, 0), 1)
eq("演習5 x'(0) = 0", sp.diff(XB, t).subs(t, 0), 0)
# A + B = 1, -2A - 3B = 0 の解
A_, B_ = sp.symbols("A B")
eq("演習5 A と B", sp.solve([A_ + B_ - 1, -2 * A_ - 3 * B_], [A_, B_]),
   {A_: 3, B_: -2})

# ── 演習6 の 3 つ ─────────────────────────────────────────────
eq("演習6(a) 固有値", eigen(6, 5), [-5, -1])
eq("演習6(a) 判別式", 6 ** 2 - 4 * 5, 16)
eq("演習6(b) 判別式", 1 ** 2 - 4 * 4, -15)
eq("演習6(b) 実部", sp.re(list(matrix_of(1, 4).eigenvals())[0]),
   sp.Rational(-1, 2))
eq("演習6(c) 固有値",
   sorted(matrix_of(0, 9).eigenvals().keys(), key=sp.im),
   [-3 * sp.I, 3 * sp.I])

# ── 演習7  x'' - x = 0（saddle） ──────────────────────────────
eq("演習7 行列", matrix_of(0, -1), sp.Matrix([[0, 1], [1, 0]]))
eq("演習7 固有値", eigen(0, -1), [-1, 1])
eq("演習7 判別式", 0 ** 2 - 4 * (-1), 4)
eq("演習7 det が負", matrix_of(0, -1).det() < 0, True)

# ── 演習10  x'' + 7x' + 12x = 0 ───────────────────────────────
eq("演習10 正しい行列", matrix_of(7, 12), sp.Matrix([[0, 1], [-12, -7]]))
eq("演習10 固有値", eigen(7, 12), [-4, -3])

# ── 一般の性質：charpoly が lambda^2 + a lambda + b ─────────────
a_, b_ = sp.symbols("a b")
eq("特性方程式は lambda^2 + a lambda + b",
   sp.expand(sp.Matrix([[0, 1], [-b_, -a_]]).charpoly(lam).as_expr()),
   sp.expand(lam ** 2 + a_ * lam + b_))


# ══════════════════════════════════════════════════════════════
# 3. 本文が、その数値どおりに書かれているか
# ══════════════════════════════════════════════════════════════
in_text("y_1 = 0 + 0.1 \\times (-2 \\times 1 - 3 \\times 0) = -0.2")
in_text("x_2 = 1 + 0.1 \\times (-0.2) = 0.98")
in_text("y_2 = -0.2 + 0.1 \\times (-2 \\times 1 - 3 \\times (-0.2)) = -0.2 + 0.1 \\times (-1.4) = -0.34")
in_text("x = 2e^{-t} - e^{-2t}")
in_text("x(0.2) = 2e^{-0.2} - e^{-0.4} = 0.967")
in_text("x = 3e^{-2t} - 2e^{-3t}")
in_text("\\lambda = -1 \\pm 2i")
in_text("x_2 = 0.1 + 0.1 \\times 0.95 = 0.195")
in_text("x_2 = 2 + 0.1 \\times (-0.6) = 1.94")
in_text("y_2 = -0.6 + 0.1 \\times (-3 \\times 2 - 4 \\times (-0.6)) = -0.6 + 0.1 \\times (-3.6) = -0.96")
in_text("M = \\begin{pmatrix} 0 & 1 \\\\ -2 & -3 \\end{pmatrix}")
in_text("M = \\begin{pmatrix} 0 & 1 \\\\ -6 & -5 \\end{pmatrix}")
in_text("M = \\begin{pmatrix} 0 & 1 \\\\ -12 & -7 \\end{pmatrix}")
in_text("\\Delta = 2^{2} - 4 \\times 5 = -16 < 0")
in_text("$\\Delta = 36 - 20 = 16 > 0$")
in_text("$\\Delta = 1 - 16 = -15 < 0$")
in_text("$\\Delta = a^{2} - 4b = 0 + 4 = 4 > 0$")


# ══════════════════════════════════════════════════════════════
# 4. シラバス・公式集から確かめた事実
# ══════════════════════════════════════════════════════════════
# 4-1 シラバスの引用（Guidance 欄）
in_text("> Write as coupled first order equations $\\dfrac{dx}{dt} = y$ and "
        "$\\dfrac{dy}{dt} = f(x,\\ y,\\ t)$.")
in_text("can also be investigated using the phase portrait method in AHL 5.17 above.")
in_text("> Understanding the occurrence of simple second order differential equations "
        "in physical phenomena would aid understanding but **in examinations the equation "
        "will be given.**")
in_text("> Use of spreadsheets to generate values.")
# 4-2 公式集に 5.18 の欄は無い
in_text("公式集に 5.18 の欄は無く")
# 4-3 厳密解は固有値が異なる 2 つの実数のときだけ
in_text("Calculation of exact solutions is only required for the case of "
        "**real distinct eigenvalues**.")
in_text("固有値が**重解**（$\\lambda_1 = \\lambda_2$）になる場合は、**この課程では出題されません。**")
# 4-4 overdamped などはシラバスの語ではない
in_text("**AI HL のシラバスにはこれらの語はありません。**")
not_in_text("overdamped と呼びます。答案では")

# 変換と行列の要点
in_text("\\boxed{\\ \\frac{d^{2}x}{dt^{2}} = f\\!\\left(x,\\ \\frac{dx}{dt},\\ t\\right) "
        "\\quad \\Longrightarrow \\quad \\frac{dx}{dt} = y, \\qquad \\frac{dy}{dt} = f(x,\\ y,\\ t)\\ }")
in_text("## eigenvector は、いつも $\\binom{1}{\\lambda}$ です")
in_text("\\mathbf{p} = \\binom{1}{\\lambda}")
in_text("## $1$ 行目は、いつも $(0,\\ 1)$ です")
in_text("**`from rest`（静止した状態から）は $y = 0$** という意味です。")
in_text("`released from rest`（静かに手をはなす）と書かれ、そのときの位置が $x = 1$ なら")
in_text("## $y$ は、新しい未知の関数です")
in_text("\\det(M - \\lambda I) = \\lambda^{2} + a\\lambda + b = 0")
in_text("これは**検算に使ってください。**")

# 相図の縦軸は速度
in_text("**縦軸 $y = \\dfrac{dx}{dt}$** … いまの速度")
in_text("| $x$ 軸を横切る（$y = 0$） | **速度が $0$**。折り返す瞬間です |")


# ══════════════════════════════════════════════════════════════
# 5. 構造の不変条件
# ══════════════════════════════════════════════════════════════
bad = [m for m in re.findall(r"`[^`\n]+`", TXT) if "$" in m or "**" in m]
eq("code span の中に数式・markdown が無い", bad, [])

L = TXT.split("\n")
nb = [i + 1 for i, l in enumerate(L)
      if re.match(r"^:{3,} *\{", l) and i > 0
      and L[i - 1].strip() != "" and not L[i - 1].lstrip().startswith("#")]
eq("開き fence の前に空行がある", nb, [])

eq("演習は 10 問", TXT.count("]{.ex-no}"), 10)
eq("区切りは 9 個", TXT.count("::: {.ex-sep}"), 9)
eq("exercise-block は 1 つ", TXT.count("::: {.exercise-block}"), 1)
eq("例題は 4 つ", TXT.count("::: {#exm-ahl518-"), 4)
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

eq("検算が書かれている", TXT.count("**検算。**") >= 5, True)
eq("model-answer がある", TXT.count("::: {.model-answer}") >= 8, True)
in_text("![Euler's method and the exact solution for the same equation](img/ahl-5-18-euler.svg)")
in_text("![What the eigenvalues say about the motion](img/ahl-5-18-motion.svg)")



# ══════════════════════════════════════════════════════════════
# 6. レビューで直した点（元に戻っていないか）
# ══════════════════════════════════════════════════════════════
in_text("## この課程で厳密解を求めるのは、固有値が異なる $2$ つの実数のときだけです")
in_text("複素数の固有値でも、解の式そのものは存在します。ただし、**この課程では求められていません。**")
not_in_text("## 厳密解を書けるのは、実で異なる固有値のときだけです")
not_in_text("実で異なる")
in_text("> Systems will have **distinct, non-zero, eigenvalues**.")
close("誤差の百分率", round(100 * (0.98 - (2 * math.exp(-0.2) - math.exp(-0.4)))
                        / (2 * math.exp(-0.2) - math.exp(-0.4)), 1), 1.3)
in_text("which is about $1.3\\%$")
not_in_text("which is about $1.4\\%$")
in_text("境目は $\\Delta = a^{2} - 4b = 0$、つまり $a = 2\\sqrt{b}$ です")
in_text("- $0 < a < 2\\sqrt{b}$（$\\Delta < 0$）")
in_text("- $a > 2\\sqrt{b}$（$\\Delta > 0$）")
not_in_text("- $a$ が小さい … **揺れながら")
in_text("右辺はどちらも **$x$ と $y$ の一次式だけ**で、定数項も $t$ もありません。")
not_in_text("右辺が **$x$ と $y$ の一次式だけ**なので")
in_text("| $a < 0$、$b > 0$、$\\Delta < 0$ | 複素数、**実部が正** |")
in_text("\\lambda = \\frac{-a \\pm \\sqrt{\\Delta}}{2}")
in_text("**$\\Delta < 0$ のとき、$2$ つの固有値の実部はどちらも $-\\dfrac{a}{2}$** です")
in_text("この式そのものが誤りというわけではありませんが、**この課程では求められていません。**")
in_text("y_{n+1} = y_n + h \\times f(x_n,\\ y_n)")
in_text("ですから文字を $y \\to x$、$x \\to t$ と読みかえます")
in_text("y_{n+1} = y_n + h \\times f_2(x_n,\\ y_n,\\ t_n)")
in_text("$f_2$ のほうは、**もとの $2$ 階の式の右辺 $f$ そのもの**です")
in_text("$\\det(M - \\lambda I) = 0$ は**公式集に載っていない**")
in_text("**$2$ 階の式を、自分で立てる必要はありません**")
not_in_text("**式の立て方は、試験では問われません。**")
in_text("速さに比例する抵抗")
not_in_text("（空気の抵抗や摩擦）")
in_text("**検算。** 対角の和は $-5$、$\\det M$ は $6$ です")
not_in_text("**検算。** trace は $-5$")
in_text("**$e$ は `e^x` のキーで入れてください。**")
in_text("左が [AHL 5.17a](ahl-5-17a.qmd#sketch)、中と右が [AHL 5.17b](ahl-5-17b.qmd) と同じ絵ですが")
in_text("右は、そのうち $h = 0.4$ の計算を $(x,\\ y)$ 平面に描いたものです")
in_text(": $h = 0.1$ の Euler 法 {#tbl-ahl518-table}")
in_text("\\binom{x}{y} = A\\binom{1}{-2}e^{-2t} + B\\binom{1}{-3}e^{-3t}")
in_text("解答例が *almost every* と書いているのは、**例外が $1$ 本だけある**からです")
in_text("**$M$ を書かずに $\\lambda^{2} + a\\lambda + b = 0$ から始めると、どこから出したのかが読めません。**")
not_in_text("[第6節の表](#tbl-ahl518-cases)")
eq("a = 2 sqrt(b) が境目（例: b=5 なら a=2sqrt5=4.47）",
   round(2 * math.sqrt(5), 2), 4.47)
eq("a=1,b=0.01 は Delta>0（振動しない）", 1 ** 2 - 4 * 0.01 > 0, True)
eq("a=3,b=100 は Delta<0（振動する）", 3 ** 2 - 4 * 100 < 0, True)



# 2026-08: saddle の行を「ほとんどの出発点で」に直した
import os as _os
_T18 = open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                          "..", "..", "ai-hl", "05-calculus", "ahl-5-18.qmd"),
            encoding="utf-8").read()
eq("5.18 の saddle 行",
   "| $b < 0$ | 異なる $2$ つの実数、**異符号** | ほとんどの出発点で**離れていく**"
   "（saddle point） | [AHL 5.17a](ahl-5-17a.qmd#saddle) |" in _T18, True)
eq("5.18 から無条件の「離れていく」を外した",
   "| $b < 0$ | 実で異なる、**異符号** | **離れていく**（saddle point） |" in _T18,
   False)

print("=" * 78)
print("結果:  OK %d / NG %d" % (OK, NG))
print("=" * 78)
sys.exit(1 if NG else 0)
