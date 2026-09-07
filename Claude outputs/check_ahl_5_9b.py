# -*- coding: utf-8 -*-
"""AHL 5.9b（chain / product / quotient rule）の検算。
   1. すべての導関数を sympy で第一原理から出す
   2. mpmath の数値微分で、独立に突き合わせる
   3. .qmd の本文が、その数値どおりに書かれているかを確かめる
   4. 公式集の 3 つのルールを、印刷されている形どおりに写しているか見張る
   5. レビューで直した点を not_in_text で見張る
   6. 構造の不変条件を確かめる
   実行: python3 figs/ai-hl/check_ahl_5_9b.py
"""
import io
import os
import re
import sys

import sympy as sp
import mpmath as mp

QMD = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "05-calculus", "ahl-5-9b.qmd")
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
    if abs(float(got) - float(want)) <= tol:
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


x = sp.symbols("x", positive=True)


def zero(name, a, b):
    eq(name, sp.simplify(sp.expand(a - b)), 0)


def val(f, pt):
    return sp.simplify(sp.diff(f, x).subs(x, pt))


# ══════════════════════════════════════════════════════════════
# 1. chain rule — 例と表
# ══════════════════════════════════════════════════════════════
zero("(2x+1)^5", sp.diff((2 * x + 1) ** 5, x), 10 * (2 * x + 1) ** 4)
eq("(2x+1)^5 at 1", val((2 * x + 1) ** 5, 1), 810)
close("数値微分 (2x+1)^5 at 1",
      float(mp.diff(lambda v: (2 * v + 1) ** 5, 1.0)), 810.0, 1e-6)
eq("掛け忘れの値", 5 * (2 * 1 + 1) ** 4, 405)
zero("e^(3x)", sp.diff(sp.exp(3 * x), x), 3 * sp.exp(3 * x))
zero("sin 4x", sp.diff(sp.sin(4 * x), x), 4 * sp.cos(4 * x))
zero("ln(x^2+1)", sp.diff(sp.log(x ** 2 + 1), x), 2 * x / (x ** 2 + 1))
zero("sqrt(3x+4)", sp.diff(sp.sqrt(3 * x + 4), x), 3 / (2 * sp.sqrt(3 * x + 4)))
eq("sqrt(3x+4) at 4", val(sp.sqrt(3 * x + 4), 4), sp.Rational(3, 8))
# 表 tbl-ahl59b-common を記号のまま確かめる
a, b, n = sp.symbols("a b n", positive=True)
zero("(ax+b)^n", sp.diff((a * x + b) ** n, x), a * n * (a * x + b) ** (n - 1))
zero("e^(ax)", sp.diff(sp.exp(a * x), x), a * sp.exp(a * x))
zero("sin(ax)", sp.diff(sp.sin(a * x), x), a * sp.cos(a * x))
zero("cos(ax)", sp.diff(sp.cos(a * x), x), -a * sp.sin(a * x))
# 図の主張: sin4x と e^3x の 0 での傾き
close("sin4x' at 0", float(sp.diff(sp.sin(4 * x), x).subs(x, 0)), 4.0)
close("sinx' at 0", float(sp.diff(sp.sin(x), x).subs(x, 0)), 1.0)
close("e^3x' at 0", float(sp.diff(sp.exp(3 * x), x).subs(x, 0)), 3.0)

# ══════════════════════════════════════════════════════════════
# 2. product rule
# ══════════════════════════════════════════════════════════════
P = x ** 2 * sp.exp(x)
zero("x^2 e^x", sp.diff(P, x), x * sp.exp(x) * (x + 2))
close("x^2e^x f'(1)", sp.N(val(P, 1), 12), 8.15484548538)
close("3e", float(3 * sp.E), 8.1548, 1e-4)
Xr = sp.symbols("Xr", real=True)
eq("x^2 e^x の停留点", sorted(sp.solve(sp.diff(Xr ** 2 * sp.exp(Xr), Xr), Xr)),
   [-2, 0])
zero("x sin x", sp.diff(x * sp.sin(x), x), sp.sin(x) + x * sp.cos(x))
eq("x sin x at pi/2", val(x * sp.sin(x), sp.pi / 2), 1)
# 誤った形は x=-2 で 0 にならない
eq("2x e^x は x=-2 で 0 でない", sp.simplify(2 * (-2) * sp.exp(-2)) != 0, True)

# ══════════════════════════════════════════════════════════════
# 3. quotient rule
# ══════════════════════════════════════════════════════════════
Q = x / (x ** 2 + 1)
zero("x/(x^2+1)", sp.diff(Q, x), (1 - x ** 2) / (x ** 2 + 1) ** 2)
eq("x/(x^2+1) at 2", val(Q, 2), sp.Rational(-3, 25))
close("-3/25", float(sp.Rational(-3, 25)), -0.12)
eq("x/(x^2+1) の停留点",
   sorted(sp.solve(sp.diff(Xr / (Xr ** 2 + 1), Xr), Xr)), [-1, 1])
eq("y at x=1", sp.Rational(1, 2), sp.Rational(1, 1) / 2)
eq("y at x=-1", sp.Rational(-1, 2), -sp.Rational(1, 2))
# 逆順に書くと符号が反対
zero("逆順は -1 倍",
     sp.diff(Q, x), -(x ** 2 - 1) / (x ** 2 + 1) ** 2)
close("逆順の値", float(sp.Rational(3, 25)), 0.12)
R = sp.exp(x) / x
zero("e^x/x", sp.diff(R, x), sp.exp(x) * (x - 1) / x ** 2)
close("e^x/x at 2", sp.N(val(R, 2), 12), 1.84726402474)
close("e^2/4", float(sp.exp(2) / 4), 1.8473, 1e-4)
close("e^2", float(sp.exp(2)), 7.389, 1e-3)
# 書き直せば済む分数
zero("(x^2+3x)/x", sp.diff((x ** 2 + 3 * x) / x, x), sp.Integer(1))
zero("5/x^3", sp.diff(5 / x ** 3, x), -15 * x ** -4)

# ══════════════════════════════════════════════════════════════
# 4. ルールが重なる形
# ══════════════════════════════════════════════════════════════
C = x ** 2 * sp.sin(3 * x)
zero("x^2 sin3x", sp.diff(C, x),
     3 * x ** 2 * sp.cos(3 * x) + 2 * x * sp.sin(3 * x))
close("x^2 sin3x at pi/6", sp.N(val(C, sp.pi / 6), 12), float(sp.pi / 3))
close("pi/3", float(sp.pi / 3), 1.0472, 1e-4)
close("y at pi/6", float((sp.pi / 6) ** 2), 0.27416, 1e-5)
close("接線の切片", float((sp.pi / 6) ** 2 - (sp.pi / 3) * (sp.pi / 6)),
      -0.27416, 1e-5)
close("接点の確認", 1.0472 * 0.5236 - 0.2742, 0.2742, 5e-4)
# cos(x^2) と (cos x)^2 は別
zero("cos(x^2)", sp.diff(sp.cos(x ** 2), x), -2 * x * sp.sin(x ** 2))
zero("(cos x)^2", sp.diff(sp.cos(x) ** 2, x), -2 * sp.cos(x) * sp.sin(x))

# ══════════════════════════════════════════════════════════════
# 5. 文脈の例題  C(t) = 5t e^{-0.5t}
# ══════════════════════════════════════════════════════════════
M = 5 * x * sp.exp(-x / 2)
zero("C'(t)", sp.diff(M, x),
     sp.Rational(5, 2) * sp.exp(-x / 2) * (2 - x))
close("C'(1)", sp.N(val(M, 1), 12), 1.51632664928)
close("2.5 e^-0.5", float(sp.Rational(5, 2) * sp.exp(-sp.Rational(1, 2))),
      1.5163, 1e-4)
close("e^-0.5", float(sp.exp(-sp.Rational(1, 2))), 0.6065, 1e-4)
eq("C の停留点", sp.solve(sp.diff(M, x), x), [2])
close("C(2)", float(M.subs(x, 2)), 3.6788, 1e-4)
close("e^-1", float(sp.exp(-1)), 0.3679, 1e-4)
close("C'(3)", sp.N(val(M, 3), 12), -0.557825404163)
eq("C'(1) > 0 かつ C'(3) < 0", (val(M, 1) > 0, val(M, 3) < 0), (True, True))

# ══════════════════════════════════════════════════════════════
# 6. 演習 1〜10
# ══════════════════════════════════════════════════════════════
zero("E1 (3x-2)^4", sp.diff((3 * x - 2) ** 4, x), 12 * (3 * x - 2) ** 3)
eq("E1 at 1", val((3 * x - 2) ** 4, 1), 12)
zero("E2", sp.diff(sp.exp(5 * x) + sp.sin(2 * x), x),
     5 * sp.exp(5 * x) + 2 * sp.cos(2 * x))
eq("E3 f'(2)", val(sp.log(x ** 2 + 1), 2), sp.Rational(4, 5))
eq("E4 at 4", val(sp.sqrt(3 * x + 4), 4), sp.Rational(3, 8))
close("E4 3/8", float(sp.Rational(3, 8)), 0.375)
eq("E5 停留点", sorted(sp.solve(sp.diff(Xr ** 2 * sp.exp(Xr), Xr), Xr)), [-2, 0])
eq("E6 at pi/2", val(x * sp.sin(x), sp.pi / 2), 1)
eq("E7 at 2", val(Q, 2), sp.Rational(-3, 25))
close("E8 f'(2)", sp.N(val(R, 2), 12), 1.84726402474)
zero("E9", sp.diff(C, x), 3 * x ** 2 * sp.cos(3 * x) + 2 * x * sp.sin(3 * x))
zero("E10 正しい形", sp.diff(P, x), x * sp.exp(x) * (x + 2))

# ══════════════════════════════════════════════════════════════
# 7. 公式集どおりの形
# ══════════════════════════════════════════════════════════════
in_text(r"y = g(u), \ \text{where} \ u = f(x) \ \Rightarrow \ "
        r"\frac{dy}{dx} = \frac{dy}{du} \times \frac{du}{dx}")
in_text(r"y = uv \ \Rightarrow \ \frac{dy}{dx} = u\frac{dv}{dx} + v\frac{du}{dx}")
in_text(r"y = \frac{u}{v} \ \Rightarrow \ \frac{dy}{dx} = "
        r"\frac{v\dfrac{du}{dx} - u\dfrac{dv}{dx}}{v^{2}}")
in_text("**試験中に配られるので、覚える必要はありません。**")

# ══════════════════════════════════════════════════════════════
# 8. レビューで直した点の見張り
# ══════════════════════════════════════════════════════════════
# 1: 書き直しで済むのは「分子も分母も」べき乗のときだけ
in_text("**分子も分母も $x$ のべき乗だけ**なら")
not_in_text("**分母が $x$ のべき乗だけ**なら、書き直したほうが早いです")
not_in_text("**分母に $x$ 以外のものが混じっているとき**（$x^{2}+1$、$e^{x}+1$ など）"
            "だけ、quotient rule が必要です。")
# 2: 表は「代入」であって電卓の微分ではない
in_text("**$2$ 行目は、電卓の微分機能に入れるのではありません。**")
not_in_text("| 自分の $f'(x)$ | $10(2x+1)^{4}$、$x = 1$ | $810$ ✓ |")
# 3: Radian の見出しから e^x を外す
in_text("## $\\sin$、$\\cos$、$\\tan$ が入っているときは Radian に")
not_in_text("## $\\sin$、$\\cos$、$\\tan$、$e^{x}$ が入っているときは Radian に")
# 4: nSolve は範囲を分けた 2 回
in_text("nSolve(x*e^(x)*(x+2)=0, x, -3, -1)")
not_in_text("nSolve(x*e^(x)*(x+2)=0, x, -5, 5)")
# 5: 先に割ってから角を落とす
in_text(r"v\frac{\delta u}{\delta x} \ + \ u\frac{\delta v}{\delta x} \ + \ "
        r"\delta u\frac{\delta v}{\delta x}")
not_in_text("この角の部分だけが先に消えます")
# 6: 見出しは英語のまま
in_text("### 3. stationary point を確かめる {#gdc-stat}")
not_in_text("### 3. 停留点を確かめる")
# 8: cos(x^2) の誤り例
in_text("**誤り**：$y = \\cos(x^{2})$ を微分して $-2x\\sin x$ と書く")
not_in_text("$-\\sin x \\times 2x$ と書くつもりが")
# 10: 「1 増える」を避ける
in_text("$x$ が**少し**増えると、$u$ はその $\\dfrac{du}{dx}$ 倍だけ増える")
not_in_text("$x$ が $1$ 増えると、$u$ は $\\dfrac{du}{dx}$ だけ増える")
# 11: 箇条書きの順を公式に合わせる
in_text("- $v$ を微分して $u$ を掛ける\n- $u$ を微分して $v$ を掛ける")
# 12: (d) を付ける
in_text("**(d)** [Hence find the gradient of the curve in part (a) when $x = 1$.]")
# 13: 文脈のある例題と Interpret
in_text("::: {#exm-ahl59b-model}")
in_text("[Interpret your answer to part (b) in the context of the model.]{.q-en}")
in_text("*One hour after the dose, the concentration of the drug is increasing "
        "at a rate of $1.52$ mg per litre per hour.*")
# 14: y = ln u
not_in_text(r"u = x^{2}+1, \qquad f = \ln u")

# ══════════════════════════════════════════════════════════════
# 9. 構造の不変条件
# ══════════════════════════════════════════════════════════════
h2 = re.findall(r"^## (.+)$", TXT, re.M)
top = [h for h in h2 if h in ("What you should be able to do", "The idea",
                              "Why it works", "Worked examples",
                              "Common errors",
                              "Using your GDC (TI-Nspire CX II)", "Exercises")]
eq("テンプレートの 7 見出しが順に並ぶ", top,
   ["What you should be able to do", "The idea", "Why it works",
    "Worked examples", "Common errors",
    "Using your GDC (TI-Nspire CX II)", "Exercises"])
eq("例題は 5 つ", len(re.findall(r"::: \{#exm-", TXT)), 5)
eq("演習は 10 問", len(re.findall(r"\[\d+\]\{\.ex-no\}", TXT)), 10)
eq("ex-sep は 9 個", TXT.count(".ex-sep"), 9)
eq("例題の下の区切り線は 5 本（+ YAML の 1 本）", TXT.count("\n---\n"), 6)
for w in ("誰でもできる", "簡単です", "当然", "明らか", "もちろん", "当たり前",
          "そのとおり", "ご指摘", "確かめ。"):
    not_in_text(w)
for m in re.finditer(r"`([^`\n]*)`", TXT):
    if "$" in m.group(1):
        NG += 1
        print("NG  code span に数式: %r" % m.group(0)[:60])
    else:
        OK += 1
for line in TXT.split("\n"):
    if not line.startswith("|"):
        continue
    inm = False
    j = 0
    bad = False
    while j < len(line):
        c = line[j]
        if c == "\\":
            j += 2
            continue
        if c == "$":
            inm = not inm
        elif c == "|" and inm:
            bad = True
            break
        j += 1
    if bad:
        NG += 1
        print("NG  表のセルの数式に | : %r" % line[:70])
BASE = os.path.dirname(QMD)
for path in set(re.findall(r"\]\((\.\./[^)#]+\.qmd|[a-z0-9-]+\.qmd)", TXT)):
    if os.path.exists(os.path.join(BASE, path)):
        OK += 1
    else:
        NG += 1
        print("NG  リンク先が無い: %s" % path)
for m in re.finditer(r"\[@(exm|eq|fig|tbl)-", TXT):
    NG += 1
    print("NG  ページ間 crossref: %r" % m.group(0))
else:
    OK += 1

print("=" * 78)
print("結果:  OK %d / NG %d" % (OK, NG))
print("=" * 78)
sys.exit(1 if NG else 0)
