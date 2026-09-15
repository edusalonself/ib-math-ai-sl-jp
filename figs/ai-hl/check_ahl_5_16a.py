"""AHL 5.16a（Euler's method）の数値と本文を、独立に検算する。
   実行: python3 figs/ai-hl/check_ahl_5_16a.py

   方針（他ページの checker と同じ）
   1. Euler 法を第一原理から実装する（ページの値を信用しない）
   2. 厳密解は sympy で微分して、もとの右辺に戻ることを確かめる
   3. 誤差の向きは、2 階微分の符号から独立に予測して突き合わせる
   4. .qmd を読んで、本文の文字列が計算結果と合っているか確かめる
   5. code span の中に数式・markdown が無いこと／開き fence の前に空行があること
"""
import os
import re
import numpy as np
import sympy as sp

QMD = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "05-calculus", "ahl-5-16a.qmd")
TXT = open(QMD, encoding="utf-8").read()

OK = NG = 0


def eq(label, got, want, tol=None):
    global OK, NG
    good = (got == want) if tol is None else abs(got - want) <= tol
    if good:
        OK += 1
        print("  OK  %-60s %s" % (label, got))
    else:
        NG += 1
        print("  NG  %-60s got %s, want %s" % (label, got, want))


def in_text(label, s):
    global OK, NG
    if s in TXT:
        OK += 1
        print("  OK  %-60s (本文にある)" % label)
    else:
        NG += 1
        print("  NG  %-60s 本文に無い: %r" % (label, s))


def not_in_text(label, s):
    global OK, NG
    if s not in TXT:
        OK += 1
        print("  OK  %-60s (本文に無い)" % label)
    else:
        NG += 1
        print("  NG  %-60s 本文にある（あってはいけない）: %r" % (label, s))


def euler(f, x0, y0, h, n):
    """Euler 法を第一原理で。各行 (n, x_n, y_n, f_n) を返す。"""
    rows = []
    x, y = x0, y0
    for i in range(n):
        s = f(x, y)
        rows.append((i, x, y, s))
        y = y + h * s
        x = x + h
    rows.append((n, x, y, f(x, y)))
    return rows


x, t = sp.symbols("x t")


def check_exact(label, sol, rhs, var=x, dep=None):
    """sol を微分して rhs（sol を代入）と一致するか。"""
    dep = dep if dep is not None else sp.Symbol("y")
    lhs = sp.simplify(sp.diff(sol, var))
    r = sp.simplify(rhs.subs(dep, sol))
    eq(label, sp.simplify(lhs - r) == 0, True)


def curvature_sign(sol, var, at):
    """厳密解の 2 階微分の符号（+1 convex / -1 concave）。"""
    v = float(sp.diff(sol, var, 2).subs(var, at))
    return 1 if v > 0 else (-1 if v < 0 else 0)


print("=" * 78)
print("1.  例題1  dy/dx = x + y, y(0)=1, h=0.1, 3 歩")
print("=" * 78)
r = euler(lambda a, b: a + b, 0.0, 1.0, 0.1, 3)
for n, xx, yy, ff in r:
    print("     n=%d  x=%.4g  y=%.6g  f=%.6g" % (n, xx, yy, ff))
eq("y1", round(r[1][2], 10), 1.1, 1e-9)
eq("y2", round(r[2][2], 10), 1.22, 1e-9)
eq("y3（答え）", round(r[3][2], 10), 1.362, 1e-9)
eq("f(0,1)", r[0][3], 1.0, 1e-12)
eq("f(0.1,1.1)", round(r[1][3], 10), 1.2, 1e-9)
eq("f(0.2,1.22)", round(r[2][3], 10), 1.42, 1e-9)

y = sp.Symbol("y")
EX1 = 2 * sp.exp(x) - x - 1
check_exact("厳密解 y = 2e^x - x - 1 が dy/dx = x+y を満たす", EX1, x + y)
e1 = float(EX1.subs(x, 0.3))
eq("exact y(0.3)", round(e1, 5), 1.39972, 1e-5)
eq("誤差 (c)", round(e1 - 1.362, 4), 0.0377, 1e-4)
eq("convex（2階微分>0）→ Euler は小さめ", curvature_sign(EX1, x, 0.15), 1)
eq("実際に小さめ", 1.362 < e1, True)

in_text("例題1 の y1", "y_1 = 1 + 0.1 \\times 1 = 1.1")
in_text("例題1 の y2", "y_2 = 1.1 + 0.1 \\times 1.2 = 1.22")
in_text("例題1 の y3", "y_3 = 1.22 + 0.1 \\times 1.42 = 1.362")
in_text("例題1 (b)", "2e^{0.3} - 0.3 - 1 = 2(1.34985\\ldots) - 1.3 = 1.39972")
in_text("例題1 (c)", "1.39972 - 1.362 = 0.0377")

print()
print("=" * 78)
print("2.  例題2  同じ式を h=0.05 で 6 歩")
print("=" * 78)
r2 = euler(lambda a, b: a + b, 0.0, 1.0, 0.05, 6)
eq("歩数 0.3/0.05", int(round(0.3 / 0.05)), 6)
eq("y(0.3) with h=0.05", round(r2[-1][2], 3), 1.380, 1e-9)
err_a, err_b = e1 - 1.362, e1 - round(r2[-1][2], 3)
eq("h=0.05 の誤差", round(err_b, 4), 0.0197, 1e-4)
eq("誤差の比（およそ 2）", round(err_a / err_b, 2), 1.91, 1e-2)
in_text("例題2 の誤差", "1.39972 - 1.380 = 0.0197")
in_text("例題2 の比", "\\frac{0.0377}{0.0197} = 1.91 \\approx 2")
in_text("例題2 の歩数", "\\frac{0.3 - 0}{0.05} = 6 \\ \\text{歩}")

print()
print("=" * 78)
print("3.  例題3  冷却 dθ/dt = -0.1(θ-20), θ(0)=90, h=1, 3 歩")
print("=" * 78)
r3 = euler(lambda a, b: -0.1 * (b - 20), 0.0, 90.0, 1.0, 3)
for n, xx, yy, ff in r3:
    print("     n=%d  t=%g  θ=%.6g  f=%.6g" % (n, xx, yy, ff))
eq("θ1", round(r3[1][2], 10), 83.0, 1e-9)
eq("θ2", round(r3[2][2], 10), 76.7, 1e-9)
eq("θ3", round(r3[3][2], 10), 71.03, 1e-9)
eq("f0", round(r3[0][3], 10), -7.0, 1e-9)
eq("f1", round(r3[1][3], 10), -6.3, 1e-9)
eq("f2", round(r3[2][3], 10), -5.67, 1e-9)
th = sp.Symbol("y")
EX3 = 20 + 70 * sp.exp(-sp.Rational(1, 10) * t)
check_exact("厳密解 θ = 20+70e^{-0.1t}", EX3, -sp.Rational(1, 10) * (th - 20),
            var=t)
e3 = float(EX3.subs(t, 3))
eq("exact θ(3)（3桁）", round(e3, 1), 71.9, 1e-9)
eq("差はおよそ 0.9", round(e3 - 71.03, 1), 0.8, 1e-9)
eq("convex → 小さめ", curvature_sign(EX3, t, 1.5), 1)
eq("実際に小さめ", 71.03 < e3, True)
in_text("例題3 の f0", "-0.1(90 - 20) = -0.1 \\times 70 = -7")
in_text("例題3 のθ1", "\\theta_1 = 90 + 1 \\times (-7) = 83")
in_text("例題3 のθ2", "\\theta_2 = 83 + 1 \\times (-6.3) = 76.7")
in_text("例題3 のθ3", "\\theta_3 = 76.7 + 1 \\times (-5.67) = 71.03")

print()
print("=" * 78)
print("4.  例題4  dy/dx = 2 - y, y(0)=0, h=0.5, 4 歩（concave）")
print("=" * 78)
r4 = euler(lambda a, b: 2 - b, 0.0, 0.0, 0.5, 4)
eq("y の並び", [round(v[2], 6) for v in r4], [0.0, 1.0, 1.5, 1.75, 1.875])
eq("f の並び", [round(v[3], 6) for v in r4][:4], [2.0, 1.0, 0.5, 0.25])
EX4 = 2 - 2 * sp.exp(-x)
check_exact("厳密解 y = 2-2e^{-x}", EX4, 2 - y)
e4 = float(EX4.subs(x, 2))
eq("exact y(2)（3桁）", round(e4, 2), 1.73, 1e-9)
eq("concave（2階微分<0）→ Euler は大きめ", curvature_sign(EX4, x, 1.0), -1)
eq("実際に大きめ", 1.875 > e4, True)
# h = 1.5 だと平衡解 y=2 を飛び越える
eq("h=1.5 の 1 歩で y=3（平衡解を越える）",
   round(euler(lambda a, b: 2 - b, 0.0, 0.0, 1.5, 1)[1][2], 6), 3.0, 1e-9)
in_text("例題4 の h=1.5", "y_1 = 0 + 1.5 \\times 2 = 3")

print()
print("=" * 78)
print("5.  図の誤差（make_ahl_5_16a.py と同じ値か）")
print("=" * 78)


def EXACT(v):
    return 2 * np.exp(v) - v - 1


for h, n, want in ((0.45, 2, 0.714), (0.3, 3, 0.525),
                   (0.15, 6, 0.293), (0.075, 12, 0.156)):
    rr = euler(lambda a, b: a + b, 0.0, 1.0, h, n)
    eq("h=%g の x=0.9 での誤差" % h,
       round(float(EXACT(0.9)) - rr[-1][2], 3), want, 1e-3)
in_text("表の h=0.45", "| $0.45$ | $2$ | $0.714$ |")
in_text("表の h=0.3", "| $0.3$ | $3$ | $0.525$ |")
in_text("表の h=0.15", "| $0.15$ | $6$ | $0.293$ |")
in_text("表の h=0.075", "| $0.075$ | $12$ | $0.156$ |")

print()
print("=" * 78)
print("6.  演習の数値")
print("=" * 78)
# 演習1
r = euler(lambda a, b: a ** 2 + b, 1.0, 2.0, 0.2, 1)
eq("演習1 f(1,2)", r[0][3], 3.0, 1e-12)
eq("演習1 の点", (round(r[1][1], 6), round(r[1][2], 6)), (1.2, 2.6))
in_text("演習1 解答", "y_1 = 2 + 0.2 \\times 3 = 2.6, \\qquad x_1 = 1 + 0.2 = 1.2")

# 演習2
r = euler(lambda a, b: a - b, 0.0, 1.0, 0.25, 4)
eq("演習2 y の並び", [round(v[2], 7) for v in r],
   [1.0, 0.75, 0.625, 0.59375, 0.6328125])
eq("演習2 f の並び", [round(v[3], 7) for v in r][:4],
   [-1.0, -0.5, -0.125, 0.15625])
EX2 = x - 1 + 2 * sp.exp(-x)
check_exact("演習2 厳密解 y = x-1+2e^{-x}", EX2, x - y)
e2 = float(EX2.subs(x, 1))
eq("演習2 exact（3桁）", round(e2, 3), 0.736, 1e-9)
eq("演習2 誤差", round(0.736 - 0.633, 3), 0.103, 1e-9)
eq("演習2 convex → 小さめ", curvature_sign(EX2, x, 0.5), 1)
in_text("演習2 の答え", "| $4$ | $1$ | $0.6328125$ | |")

# 演習3
r = euler(lambda a, b: a - b, 0.0, 1.0, 0.5, 2)
eq("演習3 y の並び", [round(v[2], 6) for v in r], [1.0, 0.5, 0.5])
eq("演習3 f1 = 0", round(r[1][3], 12), 0.0, 1e-12)
eq("演習3 誤差の比", round((0.736 - 0.5) / (0.736 - 0.633), 2), 2.29, 1e-2)
in_text("演習3 の比", "\\dfrac{0.236}{0.103} = 2.29")
in_text("演習3 の誤差", "0.736 - 0.5 = 0.236")

# 演習4
r = euler(lambda a, b: 2 * a * b, 0.0, 1.0, 0.1, 3)
eq("演習4 y の並び", [round(v[2], 6) for v in r], [1.0, 1.0, 1.02, 1.0608])
eq("演習4 f の並び", [round(v[3], 6) for v in r][:3], [0.0, 0.2, 0.408])
EX4b = sp.exp(x ** 2)
check_exact("演習4 厳密解 y = e^{x^2}", EX4b, 2 * x * y)
eq("演習4 exact y(0.3)", round(float(EX4b.subs(x, 0.3)), 4), 1.0942, 1e-4)
eq("演習4 convex → 小さめ", curvature_sign(EX4b, x, 0.15), 1)
in_text("演習4 の f", "f(0.2,\\ 1.02) = 2 \\times 0.2 \\times 1.02 = 0.408")

# 演習5
r = euler(lambda a, b: 0.2 * b * (1 - b / 500), 0.0, 100.0, 2.0, 3)
eq("演習5 P1", round(r[1][2], 6), 132.0, 1e-6)
eq("演習5 P2（1桁）", round(r[2][2], 1), 170.9, 1e-9)
eq("演習5 P3（1桁）", round(r[3][2], 1), 215.9, 1e-9)
eq("演習5 f0", round(r[0][3], 6), 16.0, 1e-6)
eq("演習5 f1（2桁）", round(r[1][3], 2), 19.43, 1e-9)
eq("演習5 f2（2桁）", round(r[2][3], 2), 22.49, 1e-9)
eq("演習5 傾きは増えている", r[0][3] < r[1][3] < r[2][3], True)
eq("演習5 増加が最大になる P", 500 / 2, 250.0, 1e-9)
in_text("演習5 の f0", "20 \\times 0.8 = 16")
in_text("演習5 の P1", "P_1 = 100 + 2 \\times 16 = 132")

# 演習6
r = euler(lambda a, b: 3 - b, 0.0, 0.0, 0.5, 4)
eq("演習6 y の並び", [round(v[2], 6) for v in r],
   [0.0, 1.5, 2.25, 2.625, 2.8125])
eq("演習6 f の並び", [round(v[3], 6) for v in r][:4], [3.0, 1.5, 0.75, 0.375])
EX6 = 3 - 3 * sp.exp(-x)
check_exact("演習6 厳密解 y = 3-3e^{-x}", EX6, 3 - y)
eq("演習6 exact（3桁）", round(float(EX6.subs(x, 2)), 2), 2.59, 1e-9)
eq("演習6 concave → 大きめ", curvature_sign(EX6, x, 1.0), -1)
eq("演習6 実際に大きめ", 2.8125 > float(EX6.subs(x, 2)), True)
# 「毎回ちょうど半分」の主張
eq("演習6 f が毎回半分",
   [round(r[i + 1][3] / r[i][3], 9) for i in range(3)], [0.5, 0.5, 0.5])

# 演習7
eq("演習7 f(0,1)", 0 + 2 * 1, 2)
eq("演習7 正しい y1", round(1 + 0.1 * 2, 6), 1.2, 1e-9)
eq("演習7 正しい x1", round(0 + 0.1, 6), 0.1, 1e-9)
in_text("演習7 の答え", "y_1 = 1 + 0.1 \\times 2 = 1.2, \\qquad x_1 = 0 + 0.1 = 0.1")

# 演習9（比）
eq("演習9 比1", round(0.096 / 0.049, 2), 1.96, 1e-2)
eq("演習9 比2", round(0.049 / 0.025, 2), 1.96, 1e-2)
eq("演習9 4分の1", round(0.096 / 0.025, 2), 3.84, 1e-2)
in_text("演習9 の比", "\\frac{0.096}{0.049} = 1.96, \\qquad \\frac{0.049}{0.025} = 1.96")

# 演習10
import math
r = euler(lambda a, b: 6 - 2 * math.sqrt(b), 0.0, 4.0, 0.5, 3)
eq("演習10 f0", round(r[0][3], 6), 2.0, 1e-9)
eq("演習10 H1", round(r[1][2], 6), 5.0, 1e-9)
eq("演習10 f1（4桁）", round(r[1][3], 4), 1.5279, 1e-4)
eq("演習10 H2（4桁）", round(r[2][2], 4), 5.7639, 1e-4)
eq("演習10 f2（4桁）", round(r[2][3], 4), 1.1984, 1e-4)
eq("演習10 H3（4桁）", round(r[3][2], 4), 6.3631, 1e-4)
eq("演習10 H3（3桁）", round(r[3][2], 2), 6.36, 1e-9)
eq("演習10 平衡 H", (6 / 2) ** 2, 9.0, 1e-12)
eq("演習10 H=9 で f=0", 6 - 2 * math.sqrt(9), 0.0, 1e-12)
eq("演習10 6.36 < 9", r[3][2] < 9, True)
eq("演習10 傾きは減っている", r[0][3] > r[1][3] > r[2][3], True)
eq("演習10 h=3 なら 1 歩で 10 > 9",
   round(euler(lambda a, b: 6 - 2 * math.sqrt(b), 0.0, 4.0, 3.0, 1)[1][2], 6),
   10.0, 1e-9)
in_text("演習10 の f1", "6 - 2\\sqrt{5} = 6 - 4.4721 = 1.5279")
in_text("演習10 の H2", "H_2 = 5 + 0.7639 = 5.7639")
in_text("演習10 の f2", "6 - 2\\sqrt{5.7639} = 6 - 4.8016 = 1.1984")
in_text("演習10 の H3", "H_3 = 5.7639 + 0.5992 = 6.3631")
in_text("演習10 の平衡", "\\sqrt{H} = 3, \\qquad H = 9")
in_text("演習10 の h=3", "H_1 = 4 + 3 \\times 2 = 10 > 9")

print()
print("=" * 78)
print("7.  構成・表記の検査")
print("=" * 78)
nos = re.findall(r"\[(\d+)\]\{\.ex-no\}", TXT)
eq("演習の番号", nos, [str(i) for i in range(1, 11)])
eq("ex-sep は 9 個", TXT.count("::: {.ex-sep}"), 9)
eq("exercise-block は 1 個", TXT.count("::: {.exercise-block}"), 1)

for fid in ("step", "h", "error", "field"):
    in_text("図 %s の定義" % fid, "{#fig-ahl516a-%s" % fid)
    eq("図 %s が参照されている" % fid, TXT.count("@fig-ahl516a-%s" % fid) >= 1,
       True)
    p = os.path.join(os.path.dirname(QMD), "img", "ahl-5-16a-%s.svg" % fid)
    eq("SVG %s が存在する" % fid, os.path.exists(p), True)

for e in ("basic", "smaller", "cooling", "over"):
    in_text("例題 %s" % e, "{#exm-ahl516a-%s}" % e)

for a in ("idea", "formula", "table", "h", "error", "field", "tech", "why",
          "why-error", "why-accumulate", "gdc-sheet", "gdc-home"):
    in_text("アンカー #%s" % a, "{#%s}" % a)

anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TXT))
anchors |= {"common-errors"}          # 英語見出しの自動 id
targets = set(re.findall(r"\]\(#([a-z0-9-]+)\)", TXT))
eq("章内リンクの飛び先がすべて存在する", sorted(targets - anchors), [])

defined = set(re.findall(r"\{#((?:fig|tbl|exm|eq)-[a-z0-9-]+)", TXT))
used = set(re.findall(r"@((?:fig|tbl|exm|eq)-[a-z0-9-]+)", TXT))
eq("crossref の飛び先がすべて存在する", sorted(used - defined), [])

eq("表のキャプション数", len(re.findall(r"^: .*\{#tbl-", TXT, re.M)),
   len(re.findall(r"\{#tbl-ahl516a-", TXT)))

for w in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん", "当たり前"]:
    not_in_text("禁止語 %s" % w, w)
bad_k = [TXT[m.start():m.start() + 6]
         for m in re.finditer(r"確かめ(?![方らてるればよな])", TXT)]
eq("「確かめ」の単独名詞用法が無い", bad_k, [])

eq("**検算。** が 8 個以上", TXT.count("**検算。**") >= 8, True)
eq("model-answer が 12 個以上", TXT.count("::: {.model-answer}") >= 12, True)

bad = [m for m in re.findall(r"`[^`\n]+`", TXT) if "$" in m or "**" in m]
eq("code span の中に数式・markdown が無い", bad, [])

L = TXT.split("\n")
nb = [i + 1 for i, l in enumerate(L)
      if re.match(r"^:{3,} *\{", l) and i > 0
      and L[i - 1].strip() != "" and not L[i - 1].lstrip().startswith("#")]
eq("開き fence の前に空行がある", nb, [])
eq("fence の開閉が一致",
   len([l for l in L if re.match(r"^:{3,} *\{", l)]),
   len([l for l in L if re.match(r"^:{3,} *$", l)]))

in_text("Worked examples の定型 callout",
        "問題文は英語です。意味が理解できなかったら、問題文の下の"
        "「**日本語訳**」を開いてください。解説は日本語です。")
in_text("例題の解答例の見出し", "## 解答例（答案用紙にはこう書く）")
in_text("演習の解答例の見出し", "## 解答例（答案用紙に書くこと）")
in_text("GDC の見出し", "## Using your GDC (TI-Nspire CX II)")

# 公式集・シラバス
in_text("公式集の式", "y_{n+1} = y_n + h \\times f(x_n,\\ y_n), \\qquad x_{n+1} = x_n + h")
in_text("公式集に載っている旨", "使う式は**公式集に載っています（5.16 の欄）。覚える必要はありません。**")
in_text("シラバス語 approximate", "シラバスも **`approximate`**（近似）と書いています。")
in_text("シラバス Guidance",
        "Spreadsheets should be used to find approximate solutions to "
        "differential equations.")
in_text("試験モードで使える旨", "## この項目は、試験モードでも使えます")

# レビュー修正の固定（回帰防止）
not_in_text("「変数分離できない」という誤った主張が無い",
            "it cannot be written as such a product, so the variables cannot be separated")
in_text("積分ができない、と書いている",
        "Evaluating it needs a substitution beyond the methods of AHL 5.14")
in_text("変数分離自体はできると書いている", "## 「変数分離できない」と書かないでください")
not_in_text("ctrl + : という存在しないキーが無い", "`ctrl` + `:`")
not_in_text("enter を押すだけで進む、と書いていない",
            "`enter` を押すたびに $1$ 歩進みます")
in_text("履歴から呼び出す手順", "`\u25b2` で $1$ つ前の入力を選び")
not_in_text("SL 5.3 を store 矢印の出典にしていない",
            "（[SL 5.3](../../ai-sl/05-calculus/sl-5-3.qmd)）")
in_text("store 矢印の書き方", "矢印は `ctrl` + `var` です。")
in_text("Document Settings の道すじ", "doc \u2192 Settings \u2192 Document Settings")
in_text("列の数が表と合っている", "列は、$n$ を入れて $5$ つです。")
not_in_text("解答例に日本語が混ざっていない", "\\text{ のとき、}")
in_text("Fill の但し書き", "**列ごとに $1$ つずつ** `Fill` してください")
in_text("concave-down のときの書きかえも示している",
        "**concave-down のときは、②だけを入れかえます。**")
in_text("シラバス語 concave-up / concave-down を使っている",
        "**concave-up / concave-down は、シラバスが名指ししている言葉です**")
not_in_text("旧表記 convex が残っていない", "convex")
not_in_text("旧表記の断り書きが残っていない",
            "convex / concave という語は、シラバスには出てきません")

# 存在しないページへのリンクが無い
for dead in ["ahl-5-11.qmd", "ahl-5-17.qmd"]:
    not_in_text("存在しないページ %s へのリンクが無い" % dead, "](%s" % dead)


# ══════════════════════════════════════════════════════════
#  2026-08: 表の分数表記を \dfrac にそろえた
# ══════════════════════════════════════════════════════════
in_text("演習5 の表見出し",
        "| $n$ | $t_n$ | $P_n$ | $f = 0.2P_n\\left(1 - \\dfrac{P_n}{500}\\right)$ |")
not_in_text("旧・スラッシュ表記",
            "| $n$ | $t_n$ | $P_n$ | $f = 0.2P_n(1 - P_n/500)$ |")

print()
print("=" * 78)
print("結果:  OK %d / NG %d" % (OK, NG))
print("=" * 78)
raise SystemExit(1 if NG else 0)
