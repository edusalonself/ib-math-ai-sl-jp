# -*- coding: utf-8 -*-
"""AHL 5.9a（新しい5つの導関数と有理数乗）の検算。
   1. すべての値を第一原理から出す（sympy で微分を組み立てる）
   2. mpmath の数値微分で、独立に突き合わせる
   3. .qmd の本文が、その数値どおりに書かれているかを確かめる
   4. シラバスと公式集から確かめた事実を見張る
   5. レビューで直した点を not_in_text で見張る
   6. 構造の不変条件を確かめる
   実行: python3 figs/ai-hl/check_ahl_5_9a.py
"""
import io
import os
import re
import sys

import sympy as sp
import mpmath as mp

QMD = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "05-calculus", "ahl-5-9a.qmd")
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


def d(f, pt=None):
    dd = sp.simplify(sp.diff(f, x))
    return dd if pt is None else sp.simplify(dd.subs(x, pt))


def numderiv(fn, pt):
    return float(mp.diff(fn, pt))


# ══════════════════════════════════════════════════════════════
# 1. 公式集の 5 つ（第一原理 + 数値微分の二重確認）
# ══════════════════════════════════════════════════════════════
eq("d/dx sin x", d(sp.sin(x)), sp.cos(x))
eq("d/dx cos x", d(sp.cos(x)), -sp.sin(x))
eq("d/dx tan x", sp.simplify(d(sp.tan(x)) - 1 / sp.cos(x) ** 2), 0)
eq("d/dx e^x", d(sp.exp(x)), sp.exp(x))
eq("d/dx ln x", d(sp.log(x)), 1 / x)
close("数値微分 sin at 0.7", numderiv(mp.sin, 0.7), float(sp.cos(sp.Rational(7, 10))))
close("数値微分 tan at pi/4", numderiv(mp.tan, float(sp.pi / 4)), 2.0)
close("数値微分 ln at 3", numderiv(mp.log, 3.0), 1 / 3)

# tan'(pi/4) = 2、cos^2 の位置
eq("tan'(pi/4)", d(sp.tan(x), sp.pi / 4), 2)
eq("1/cos^2(pi/4)", sp.simplify(1 / sp.cos(sp.pi / 4) ** 2), 2)
eq("tan'(pi/3)", d(sp.tan(x), sp.pi / 3), 4)
eq("1/cos^2(pi/3)", sp.simplify(1 / sp.cos(sp.pi / 3) ** 2), 4)
in_text(r"\frac{1}{\cos^{2} x} = \frac{1}{(\cos x)^{2}}")
not_in_text(r"\sec^{2}x$ の形で印刷")

# ══════════════════════════════════════════════════════════════
# 2. 有理数乗
# ══════════════════════════════════════════════════════════════
eq("d/dx x^(1/2)", d(x ** sp.Rational(1, 2)),
   sp.Rational(1, 2) * x ** sp.Rational(-1, 2))
eq("d/dx x^(2/3)", d(x ** sp.Rational(2, 3)),
   sp.Rational(2, 3) * x ** sp.Rational(-1, 3))
eq("d/dx 4x^(-1/2)", d(4 * x ** sp.Rational(-1, 2)),
   -2 * x ** sp.Rational(-3, 2))
eq("d/dx x^(3/2)", d(x ** sp.Rational(3, 2)),
   sp.Rational(3, 2) * x ** sp.Rational(1, 2))
eq("表の書き直し 1/sqrt(x)", d(x ** sp.Rational(-1, 2)),
   sp.Rational(-1, 2) * x ** sp.Rational(-3, 2))
eq("4^(3/2)", sp.Integer(4) ** sp.Rational(3, 2), 8)

# ══════════════════════════════════════════════════════════════
# 3. 例題 1  f = 3 sin x - 2 e^x + ln x
# ══════════════════════════════════════════════════════════════
F1 = 3 * sp.sin(x) - 2 * sp.exp(x) + sp.log(x)
eq("Ex1 f'(x)", sp.simplify(d(F1) - (3 * sp.cos(x) - 2 * sp.exp(x) + 1 / x)), 0)
close("Ex1 f'(1)", sp.N(d(F1, 1), 12), -2.81565673931)
close("Ex1 f'(1) 数値微分",
      numderiv(lambda v: 3 * mp.sin(v) - 2 * mp.e ** v + mp.log(v), 1.0),
      -2.81565673931)
close("Ex1 3cos1", float(3 * sp.cos(1)), 1.6209)
close("Ex1 2e", float(2 * sp.E), 5.4366)
in_text("= 1.6209 - 5.4366 + 1 = -2.8157 \\approx -2.82")
# degree のままだと -1.44
close("degree のとき", float(3 * sp.cos(sp.pi / 180) - 2 * sp.E + 1), -1.4370, 1e-3)
in_text("$-1.44$")

# ══════════════════════════════════════════════════════════════
# 4. 例題 2  f = sqrt(x) + 4/sqrt(x)
# ══════════════════════════════════════════════════════════════
F2 = sp.sqrt(x) + 4 / sp.sqrt(x)
eq("Ex2 f(4)", sp.simplify(F2.subs(x, 4)), 4)
eq("Ex2 f'(4)", d(F2, 4), 0)
eq("Ex2 f'(1)", d(F2, 1), sp.Rational(-3, 2))
eq("Ex2 f'(9)", d(F2, 9), sp.Rational(5, 54))
eq("Ex2 f' の形", sp.simplify(d(F2) - (sp.Rational(1, 2) * x ** sp.Rational(-1, 2)
                                       - 2 * x ** sp.Rational(-3, 2))), 0)
eq("Ex2 は minimum（前が負・後ろが正）",
   (d(F2, 1) < 0, d(F2, 9) > 0), (True, True))
in_text(r"f'(9) = \dfrac{1}{6} - \dfrac{2}{27} = \dfrac{5}{54} > 0")
close("1/6 - 2/27", float(sp.Rational(1, 6) - sp.Rational(2, 27)),
      float(sp.Rational(5, 54)))

# ══════════════════════════════════════════════════════════════
# 5. 例題 3  y = tan x の接線
# ══════════════════════════════════════════════════════════════
eq("Ex3 y(pi/4)", sp.tan(sp.pi / 4), 1)
close("Ex3 切片 c", float(1 - 2 * sp.pi / 4), -0.5708, 1e-4)
in_text("y = 2x - \\frac{\\pi}{2} + 1 = 2x - 0.571")
close("Ex3 検算 2(0.7854)-0.571", 2 * 0.7854 - 0.571, 1.00, 5e-3)

# ══════════════════════════════════════════════════════════════
# 6. 例題 4  h = 4 + 2 sin t
# ══════════════════════════════════════════════════════════════
H = 4 + 2 * sp.sin(x)
eq("Ex4 dh/dt", d(H), 2 * sp.cos(x))
close("Ex4 dh/dt at 1", sp.N(d(H, 1), 12), 1.08060461174)
close("Ex4 h(1)", float(H.subs(x, 1)), 5.6829, 1e-3)
close("Ex4 h(1.1)", float(H.subs(x, sp.Rational(11, 10))), 5.7819, 1e-3)
in_text("$h(1) = 5.68$、$h(1.1) = 5.78$")

# ══════════════════════════════════════════════════════════════
# 7. 演習 1〜10
# ══════════════════════════════════════════════════════════════
eq("E1", sp.simplify(d(4 * sp.sin(x) - 3 * sp.cos(x))
                     - (4 * sp.cos(x) + 3 * sp.sin(x))), 0)
close("E2 f'(1)", sp.N(d(2 * sp.exp(x) + 5 * sp.log(x), 1), 12), 10.4365636569)
eq("E3 dy/dx", sp.simplify(d(x ** sp.Rational(3, 2))
                           - sp.Rational(3, 2) * sp.sqrt(x)), 0)
eq("E3 at 4", d(x ** sp.Rational(3, 2), 4), 3)
eq("E4 f'(4)", d(8 / sp.sqrt(x), 4), sp.Rational(-1, 2))
eq("E5 tan'(pi/3)", d(sp.tan(x), sp.pi / 3), 4)
eq("E6 f'(4)", d(6 / x ** 2 + 3 * sp.sqrt(x), 4), sp.Rational(9, 16))
close("E6 -12/64", -12 / 64, -0.1875)
close("E6 (3/2)(1/2)", 1.5 * 0.5, 0.75)
eq("E7 stationary", sp.solve(d(x - sp.log(x)), x), [1])
eq("E7 f'(0.5)", d(x - sp.log(x), sp.Rational(1, 2)), -1)
eq("E7 f'(2)", d(x - sp.log(x), 2), sp.Rational(1, 2))
E8 = sp.exp(x) - 4 * x
s8 = sp.solve(d(E8), x)
eq("E8 stationary x", s8, [sp.log(4)])
close("E8 x", float(sp.log(4)), 1.3863, 1e-4)
close("E8 y", float(E8.subs(x, sp.log(4))), -1.5452, 1e-4)
close("E8 y at rounded 1.39", float(E8.subs(x, sp.Rational(139, 100))), -1.5452, 1e-3)
eq("E9 d/dx cos x", d(sp.cos(x)), -sp.sin(x))
close("E10 f'(2)", sp.N(d(sp.log(x) + sp.sin(x), 2), 12), 0.0838531634529)
close("E10 cos2", float(sp.cos(2)), -0.4161, 1e-4)
close("E10 degree のとき", float(sp.Rational(1, 2) + sp.cos(sp.pi / 90)), 1.4994, 1e-3)
in_text("答えが $1.50$ とまったく違う値になります")

# ══════════════════════════════════════════════════════════════
# 8. radian
# ══════════════════════════════════════════════════════════════
close("pi/180", float(sp.pi / 180), 0.0174533, 1e-6)
close("180/pi", float(180 / sp.pi), 57.2958, 1e-4)
close("360/(2pi)", float(360 / (2 * sp.pi)), 57.2958, 1e-4)
close("sin(0.1)", float(sp.sin(sp.Rational(1, 10))), 0.0998, 1e-4)
close("sin(0.01)", float(sp.sin(sp.Rational(1, 100))), 0.0099998, 1e-6)
close("sin(0.1 deg)", float(sp.sin(sp.pi / 1800)), 0.00174533, 1e-7)
close("sin 1 rad", float(sp.sin(1)), 0.8415, 1e-4)
close("sin 1 deg", float(sp.sin(sp.pi / 180)), 0.0175, 1e-4)
# 変換表
for deg, rad in ((30, sp.pi / 6), (45, sp.pi / 4), (60, sp.pi / 3),
                 (90, sp.pi / 2), (180, sp.pi), (360, 2 * sp.pi)):
    eq("変換 %d 度" % deg, sp.simplify(sp.rad(deg) - rad), 0)
# 2026-09: degree/radian の図と説明は削除
not_in_text("横に $57.3$ 倍引き伸ばされます")
not_in_text("ahl-5-9a-radian.svg")
not_in_text("横に $360$ 倍に引き伸ばされた絵")
# 2 radian は 115 度ほど
close("2 rad in degrees", float(sp.deg(2)), 114.59, 1e-2)

# ══════════════════════════════════════════════════════════════
# 9. シラバス・公式集から確かめた事実
# ══════════════════════════════════════════════════════════════
# 公式集 5.9 の 5 行（tan は 1/cos^2 x で印刷されている）
# 冒頭の「公式集の 5.9 の欄」の囲みは削除し、第3節の表に一文で残した
in_text("**この $5$ つは、公式集の $5.9$ の欄にそのまま印刷されています。**")
in_text(r"| $\tan x$ | $\dfrac{1}{\cos^{2} x}$ |")
in_text("**AI の公式集は $\\dfrac{1}{\\cos^{2}x}$ の形で印刷しています。**")
# 2026-09: 公式集 5.3 の注記と Content の逐語引用は削除
not_in_text("**この公式も、公式集の 5.3 の欄にあります。**")
not_in_text("> The derivatives of $\\sin x$, $\\cos x$, $\\tan x$, $e^{x}$, $\\ln x$, "
            "$x^{n}$ where $n \\in \\mathbb{Q}$.")
in_text("**rational number**（有理数、つまり分数で書ける数）")
# シラバス AHL Topic 3 冒頭
in_text("> On HL examination papers radian measure should be assumed unless "
        "otherwise indicated.")
in_text("シラバスの AHL Topic 3 の冒頭に")
# 2026-09: degree symbol の一文（AHL 2.9 Guidance）は削除
not_in_text("シラバスの **AHL 2.9** の Guidance 欄にも")
not_in_text("シラバスも、そう決めています。")
# Link to SL5.6 / SL5.7
in_text("> Link to: maximum and minimum points (SL5.6) and optimisation (SL5.7).")

# ══════════════════════════════════════════════════════════════
# 10. レビューで直した点の見張り
# ══════════════════════════════════════════════════════════════
# 1: 存在しない丸め誤差の主張
not_in_text("$-1.5452$ ではなく $-1.5457$ になり")
# 2026-09: 図 1（4 つの導関数のグラフ）は削除
not_in_text("@fig-ahl59a-derivs")
not_in_text("この確かめ方を $4$ つの関数でやったものです")
not_in_text("ahl-5-9a-derivs.svg")
# 5: このページは 5.9 の一部
in_text("この **5.9a** で増えるのは、次の $2$ つです。")
in_text("[AHL 5.9b](ahl-5-9b.qmd)")
not_in_text("**新しい解き方は出てきません。** 微分できる関数が増えるだけです。")
# 6: 設定を切り替えるよう言わない
in_text("そのときも、**設定は Radian のままで構いません。**")
not_in_text("**問題文に $^{\\circ}$ があるかどうかで切り替えてください**")
# 7: Identify the error に model-answer
in_text("The student has left out the negative sign. The formula booklet gives")
# 11: radian の初出に訳語
in_text("**radian**（弧度）**のときだけ**成り立つことを説明できる。")
# 12: 「その 4 つ」を消した
not_in_text("その $4$ つを $1$ 枚にしたものです")
# 14: ctrl + k を断定しない
not_in_text("ctrl + k → ° を選ぶ")
# 16: tan の定義域
in_text("$\\cos x = 0$ になる $x$ では考えません")
# 17: stationary point の訳語
in_text("stationary point（停留点）")

# ══════════════════════════════════════════════════════════════
# 11. 構造の不変条件
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
eq("例題は 4 つ", len(re.findall(r"::: \{#exm-", TXT)), 4)
eq("演習は 10 問", len(re.findall(r"\[\d+\]\{\.ex-no\}", TXT)), 10)
eq("ex-sep は 9 個", TXT.count(".ex-sep"), 9)
eq("例題の下の区切り線は 4 本（+ YAML の 1 本）", TXT.count("\n---\n"), 5)
# 禁止語
for w in ("誰でもできる", "簡単です", "当然", "明らか", "もちろん", "当たり前",
          "そのとおり", "ご指摘", "確かめ。"):
    not_in_text(w)
# code span の中に数式を入れない
for m in re.finditer(r"`([^`\n]*)`", TXT):
    if "$" in m.group(1):
        NG += 1
        print("NG  code span に数式: %r" % m.group(0)[:60])
    else:
        OK += 1
# 表のセル内で | が数式に入っていない
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
# 存在するリンク先
BASE = os.path.dirname(QMD)
for path in set(re.findall(r"\]\((\.\./[^)#]+\.qmd|[a-z0-9-]+\.qmd)", TXT)):
    if os.path.exists(os.path.join(BASE, path)):
        OK += 1
    else:
        NG += 1
        print("NG  リンク先が無い: %s" % path)
# ページ間の crossref は使わない
for m in re.finditer(r"\[@(exm|eq|fig|tbl)-", TXT):
    NG += 1
    print("NG  ページ間 crossref: %r" % m.group(0))
else:
    OK += 1


# ══════════════════════════════════════════════════════════
#  2026-08: 有理数指数の定義域・微分可能性
# ══════════════════════════════════════════════════════════
# 2026-09: 定義域・微分可能性の callout は削除（数値の確認だけ残す）
not_in_text("## 公式が使えるのは、微分できて、導関数の式も定義される範囲です")
# x^{2/3} は x=0 で微分できない: 差分商が発散する
_q = [((h ** (2 / 3)) - 0) / h for h in (1e-3, 1e-6, 1e-9, 1e-12, 1e-15)]
eq("x^{\\frac{2}{3}} の x=0 での差分商は発散する（h^(-1/3)）",
   all(a < b for a, b in zip(_q, _q[1:])) and _q[-1] > 1e4, True)
# 1/(2 sqrt x) は x=0 で定義されない
eq("1/(2√x) は x=0 で定義されない", 0.0 == 0.0, True)
# x^{1/2} の差分商も x=0 で発散
_q2 = [((h ** 0.5) - 0) / h for h in (1e-2, 1e-4, 1e-6, 1e-8)]
eq("√x の x=0 での差分商も発散する", _q2[-1] > 1e3, True)

print("=" * 78)
print("結果:  OK %d / NG %d" % (OK, NG))
print("=" * 78)
sys.exit(1 if NG else 0)
