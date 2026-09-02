"""AHL 5.15（slope fields）の数値と本文を、独立に検算する。
   実行: python3 figs/ai-hl/check_ahl_5_15.py

   方針（他ページの checker と同じ）
   1. すべて第一原理から計算する（ページの値を信用しない）
   2. 解が主張されているものは sympy で微分して、もとの右辺と一致するか確かめる
   3. .qmd を読んで、本文の文字列が計算結果と合っているか確かめる
   4. code span の中に数式・markdown が無いこと
   5. 開き fence の前に空行があること
"""
import os
import re
import math
import numpy as np
import sympy as sp

QMD = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "05-calculus", "ahl-5-15.qmd")
TXT = open(QMD, encoding="utf-8").read()

OK = NG = 0


def eq(label, got, want, tol=None):
    global OK, NG
    if tol is None:
        good = got == want
    else:
        good = abs(got - want) <= tol
    if good:
        OK += 1
        print("  OK  %-62s %s" % (label, got))
    else:
        NG += 1
        print("  NG  %-62s got %s, want %s" % (label, got, want))


def in_text(label, s):
    global OK, NG
    if s in TXT:
        OK += 1
        print("  OK  %-62s (本文にある)" % label)
    else:
        NG += 1
        print("  NG  %-62s 本文に無い: %r" % (label, s))


def not_in_text(label, s):
    global OK, NG
    if s not in TXT:
        OK += 1
        print("  OK  %-62s (本文に無い)" % label)
    else:
        NG += 1
        print("  NG  %-62s 本文にある（あってはいけない）: %r" % (label, s))


x, y, t, h, P = sp.symbols("x y t h P")


def verify_solution(label, sol, rhs_expr, var=x, dep=y):
    """sol を微分し、rhs に sol を代入したものと一致するか。"""
    lhs = sp.simplify(sp.diff(sol, var))
    rhs = sp.simplify(rhs_expr.subs(dep, sol))
    eq(label, sp.simplify(lhs - rhs) == 0, True)


print("=" * 78)
print("1.  dy/dx = x - y  の傾き")
print("=" * 78)


def f1(a, b):
    return a - b


eq("(0, 0)", f1(0, 0), 0)
eq("(1, 2)", f1(1, 2), -1)
eq("(-1, 2)", f1(-1, 2), -3)
eq("(2, 1)", f1(2, 1), 1)

# 水平になるのは y = x
eq("y = x 上で水平（(2,2)）", f1(2, 2), 0)
eq("y = x 上で水平（(-3,-3)）", f1(-3, -3), 0)
# 傾き -1 になるのは y = x + 1
for a in (-1, 0, 1, 2):
    eq("y = x+1 上で傾き -1 （x=%d）" % a, f1(a, a + 1), -1)

in_text("(a) の (0,0)", "(0,\\ 0): \\ 0 - 0 = 0")
in_text("(a) の (1,2)", "(1,\\ 2): \\ 1 - 2 = -1")
in_text("(a) の (-1,2)", "(-1,\\ 2): \\ -1 - 2 = -3")
in_text("(a) の (2,1)", "(2,\\ 1): \\ 2 - 1 = 1")
in_text("(b) の答え y = x", "x - y = 0 \\ \\Longrightarrow \\ y = x")
in_text("(c) の答え y = x+1", "x - y = -1 \\ \\Longrightarrow \\ y = x + 1")

print()
print("=" * 78)
print("2.  y = x - 1 は dy/dx = x - y の解か")
print("=" * 78)
verify_solution("y = x - 1 が解", x - 1, x - y)
# 一般解 y = C e^{-x} + x - 1
C = sp.Symbol("C")
verify_solution("y = C e^{-x} + x - 1 が解", C * sp.exp(-x) + x - 1, x - y)

print()
print("=" * 78)
print("3.  ロジスティック  dP/dt = 0.4 P (1 - P/50)")
print("=" * 78)


def flog(p):
    return 0.4 * p * (1 - p / 50)


eq("P = 50 で 0", flog(50), 0.0, 1e-12)
eq("P = 0 で 0", flog(0), 0.0, 1e-12)
eq("P = 5", flog(5), 1.8, 1e-12)
eq("P = 30", flog(30), 4.8, 1e-12)
eq("P = 60", flog(60), -4.8, 1e-12)
eq("P = 25（最大）", flog(25), 5.0, 1e-12)
# 最大は L/2 のところ
grid = np.linspace(0, 50, 100001)
eq("増加が最大になる P", round(float(grid[np.argmax(flog(grid))]), 3), 25.0,
   1e-3)

in_text("(a) の計算", "0.4 \\times 50 \\times \\left(1 - \\frac{50}{50}\\right) = 20 \\times (1 - 1) = 20 \\times 0 = 0")
in_text("(c) の計算", "0.4 \\times 5 \\times \\left(1 - \\frac{5}{50}\\right) = 2 \\times 0.9 = 1.8 > 0")
in_text("(d) の計算", "0.4 \\times 60 \\times \\left(1 - \\frac{60}{50}\\right) = 24 \\times (-0.2) = -4.8 < 0")
in_text("検算の P = 30", "0.4 \\times 30 \\times (1 - 0.6) = 4.8 > 0")

print()
print("=" * 78)
print("4.  match の 4 式：水平になる場所と、2 点での傾き")
print("=" * 78)
EQS = {"x": lambda a, b: a,
       "y": lambda a, b: b,
       "x-y": lambda a, b: a - b,
       "xy": lambda a, b: a * b}

# (2,1) では x と xy が 2、y と x-y が 1 で、区別できない
v21 = {k: f(2, 1) for k, f in EQS.items()}
eq("(2,1) で x → 2", v21["x"], 2)
eq("(2,1) で y → 1", v21["y"], 1)
eq("(2,1) で x-y → 1", v21["x-y"], 1)
eq("(2,1) で xy → 2", v21["xy"], 2)
eq("(2,1) だけでは 4 つを区別できない", len(set(v21.values())) < 4, True)

v12 = {k: f(1, 2) for k, f in EQS.items()}
eq("(1,2) で x → 1", v12["x"], 1)
eq("(1,2) で y → 2", v12["y"], 2)
eq("(1,2) で x-y → -1", v12["x-y"], -1)
eq("(1,2) で xy → 2", v12["xy"], 2)
pairs = {k: (v21[k], v12[k]) for k in EQS}
eq("(2,1) と (1,2) の 2 点なら 4 つ全部区別できる",
   len(set(pairs.values())) == 4, True)

in_text("2 点で区別できると書いてある",
        "$(1,\\ 2)$ を足すと、$4$ つの式の傾きは順に $1$、$2$、$-1$、$2$ です。")
not_in_text("(0,2) を使う古い記述が残っていない", "$(0,\\ 2)$ の $2$ 点なら")

# 水平になる場所
eq("dy/dx = x が水平なのは x = 0", EQS["x"](0, 7), 0)
eq("dy/dx = y が水平なのは y = 0", EQS["y"](7, 0), 0)
eq("dy/dx = x-y が水平なのは y = x", EQS["x-y"](7, 7), 0)
eq("dy/dx = xy が水平なのは x = 0", EQS["xy"](0, 7), 0)
eq("dy/dx = xy が水平なのは y = 0 でも", EQS["xy"](7, 0), 0)

print()
print("=" * 78)
print("5.  演習1   dy/dx = x + y")
print("=" * 78)


def f2(a, b):
    return a + b


eq("(0,0)", f2(0, 0), 0)
eq("(1,1)", f2(1, 1), 2)
eq("(2,-1)", f2(2, -1), 1)
eq("(-2,-1)", f2(-2, -1), -3)
eq("y = -x 上で水平", f2(3, -3), 0)
eq("y = 2-x 上で傾き 2", f2(-1, 3), 2)
in_text("演習1 の解答", "(0,\\ 0): \\ 0, \\qquad (1,\\ 1): \\ 2, \\qquad (2,\\ -1): \\ 1, \\qquad (-2,\\ -1): \\ -3")

print()
print("=" * 78)
print("6.  演習2   4 つの場の対応")
print("=" * 78)
FIELDS = {"P": lambda a, b: 2 - b,
          "Q": lambda a, b: a + b,
          "R": lambda a, b: b * (4 - b),
          "S": lambda a, b: a ** 2}
eq("P は y = 2 で水平", FIELDS["P"](5, 2), 0)
eq("P は y = 2 以外では水平でない", FIELDS["P"](5, 1) != 0, True)
eq("Q は y = -x で水平", FIELDS["Q"](2, -2), 0)
eq("R は y = 0 で水平", FIELDS["R"](5, 0), 0)
eq("R は y = 4 で水平", FIELDS["R"](5, 4), 0)
eq("S は x = 0 で水平", FIELDS["S"](0, 5), 0)
eq("S の傾きは決して負にならない",
   all(FIELDS["S"](a, 0) >= 0 for a in np.linspace(-4, 4, 401)), True)
in_text("演習2 の解答", "\\text{P} \\to \\text{(ii)}, \\qquad \\text{Q} \\to \\text{(iv)}, \\qquad \\text{R} \\to \\text{(iii)}, \\qquad \\text{S} \\to \\text{(i)}")

print()
print("=" * 78)
print("7.  演習3   dy/dx = 2 - y")
print("=" * 78)
verify_solution("y = 2 は解（平衡解）", sp.Integer(2), 2 - y)
verify_solution("y = 2 - 2e^{-x} は解", 2 - 2 * sp.exp(-x), 2 - y)
sol3 = 2 - 2 * sp.exp(-x)
eq("y(0) = 0", float(sol3.subs(x, 0)), 0.0, 1e-12)
eq("(0,0) での傾きは 2", 2 - 0, 2)
eq("x -> ∞ で y -> 2", float(sp.limit(sol3, x, sp.oo)), 2.0, 1e-12)
in_text("演習3 の検算の解", "y = 2 - 2e^{-x}")

print()
print("=" * 78)
print("8.  演習4   dy/dx = y(4 - y)")
print("=" * 78)


def f4(b):
    return b * (4 - b)


eq("y = 0 で 0", f4(0), 0)
eq("y = 4 で 0", f4(4), 0)
eq("y = 1 で 3", f4(1), 3)
eq("y = 5 で -5", f4(5), -5)
eq("y = -1 で -5", f4(-1), -5)
eq("y = 2 で 4（最大）", f4(2), 4)
eq("y = 3 で 3", f4(3), 3)
g = np.linspace(0, 4, 40001)
eq("0<y<4 で最大になる y", round(float(g[np.argmax(f4(g))]), 4), 2.0, 1e-4)
in_text("演習4 (b) の傾き", "the slope is $1 \\times 3 = 3 > 0$")
in_text("演習4 (c) の傾き", "the slope is $5 \\times (-1) = -5 < 0$")
in_text("演習4 検算の y=2", "$2 \\times 2 = 4$")
in_text("演習4 検算の y=-1", "$-1 \\times 5 = -5$")

print()
print("=" * 78)
print("9.  演習5   dy/dx = x^2")
print("=" * 78)
verify_solution("y = x^3/3 + C は解", x ** 3 / 3 + C, x ** 2 + 0 * y)
eq("x^2 は常に 0 以上",
   all(a ** 2 >= 0 for a in np.linspace(-5, 5, 1001)), True)
eq("水平になるのは x = 0 だけ",
   [a for a in (-2, -1, 0, 1, 2) if a ** 2 == 0], [0])
in_text("演習5 検算の解", "y = \\dfrac{x^3}{3} + C")

print()
print("=" * 78)
print("10. 演習6   dy/dx = x - y、y(0) = 3")
print("=" * 78)
sol6 = x - 1 + 4 * sp.exp(-x)
verify_solution("y = x - 1 + 4e^{-x} は解", sol6, x - y)
eq("y(0) = 3", float(sol6.subs(x, 0)), 3.0, 1e-12)
xmin = sp.solve(sp.diff(sol6, x), x)
xmin = float(xmin[0])
eq("極小の x = ln 4", xmin, math.log(4), 1e-12)
eq("極小の x（小数）", round(xmin, 3), 1.386, 1e-9)
ymin = float(sol6.subs(x, xmin))
eq("極小の y は x と等しい（y = x 上）", round(ymin - xmin, 12), 0.0, 1e-9)
eq("極小の y（小数）", round(ymin, 3), 1.386, 1e-9)
eq("(0,3) での傾きは -3", f1(0, 3), -3)
in_text("演習6 検算の解", "y = x - 1 + 4e^{-x}")
in_text("演習6 の ln 4", "x = \\ln 4 = 1.386\\ldots")
in_text("演習6 の読み取り値", "(1.4,\\ 1.4)")

print()
print("=" * 78)
print("11. 演習7   dy/dx = x + y、y = -x - 1")
print("=" * 78)
verify_solution("y = -x - 1 は解", -x - 1, x + y)
A = sp.Symbol("A")
verify_solution("y = A e^{x} - x - 1 は解", A * sp.exp(x) - x - 1, x + y)
eq("y = -x-1 の傾きは -1", float(sp.diff(-x - 1, x)), -1.0, 1e-12)
eq("y = -x-1 上で右辺も -1", float((x + y).subs({x: 3, y: -4})), -1.0, 1e-12)
in_text("演習7 の A e^x", "y = Ae^{x} - x - 1")

print()
print("=" * 78)
print("12. 演習8   dy/dx = y、(0, 2)")
print("=" * 78)
sol8 = 2 * sp.exp(x)
verify_solution("y = 2e^x は解", sol8, y)
eq("y(0) = 2", float(sol8.subs(x, 0)), 2.0, 1e-12)
eq("(0,2) での傾きは +2", 2, 2)
eq("x=1 での y", round(float(sol8.subs(x, 1)), 2), 5.44, 1e-9)
eq("x=-1 での y", round(float(sol8.subs(x, -1)), 3), 0.736, 1e-9)
eq("x=-3 での y", round(float(sol8.subs(x, -3)), 4), 0.0996, 1e-9)
eq("y は決して 0 にならない",
   all(float(sol8.subs(x, a)) > 0 for a in (-20, -5, 0, 5)), True)
verify_solution("y = 0 も解", sp.Integer(0), y)
in_text("演習8 の 5.44", "$x = 1$ で $5.44$")
in_text("演習8 の 0.736", "$x = -1$ で $0.736$")
in_text("演習8 の 0.0996", "$x = -3$ で $0.0996$")

print()
print("=" * 78)
print("13. 演習9   dh/dt = 0.5 h (1 - h/40)")
print("=" * 78)


def f9(v):
    return 0.5 * v * (1 - v / 40)


eq("h = 40 で 0", f9(40), 0.0, 1e-12)
eq("h = 0 で 0", f9(0), 0.0, 1e-12)
eq("h = 10", f9(10), 3.75, 1e-12)
eq("h = 20", f9(20), 5.0, 1e-12)
eq("h = 5", round(f9(5), 4), 2.1875, 1e-9)
eq("h = 5（2 桁）", round(f9(5), 2), 2.19, 1e-9)
eq("h = 30", f9(30), 3.75, 1e-12)
eq("h=10 と h=30 が同じ", f9(10) == f9(30), True)
g9 = np.linspace(0, 40, 40001)
eq("伸びが最大になる h", round(float(g9[np.argmax(f9(g9))]), 4), 20.0, 1e-4)
in_text("演習9 h=10 の計算", "0.5(10)(1 - 0.25) = 5 \\times 0.75 = 3.75")
in_text("演習9 h=20 の計算", "0.5(20)(1 - 0.5) = 10 \\times 0.5 = 5")
in_text("演習9 (a) の計算", "0.5(40)\\left(1 - \\frac{40}{40}\\right) = 20 \\times 0 = 0")

print()
print("=" * 78)
print("14. 演習10   dy/dx = y - x^2")
print("=" * 78)


def f10(a, b):
    return b - a ** 2


eq("(0,1)", f10(0, 1), 1)
eq("(1,1)", f10(1, 1), 0)
eq("(2,1)", f10(2, 1), -3)
eq("水平なのは y = x^2 上（(3,9)）", f10(3, 9), 0)
eq("水平なのは y = x^2 上（(-2,4)）", f10(-2, 4), 0)
eq("dy/dx = y なら 3 点とも 1", [1, 1, 1], [1, 1, 1])
in_text("演習10 の解答", "(0,\\ 1): \\ 1 - 0 = 1, \\qquad (1,\\ 1): \\ 1 - 1 = 0, \\qquad (2,\\ 1): \\ 1 - 4 = -3")
in_text("演習10 (a) の答え", "y - x^2 = 0, \\qquad y = x^2")

print()
print("=" * 78)
print("15. 構成・表記の検査")
print("=" * 78)

# 演習が 10 問あり、番号が 1..10
nos = re.findall(r"\[(\d+)\]\{\.ex-no\}", TXT)
eq("演習の番号", nos, [str(i) for i in range(1, 11)])
eq("ex-sep は 9 個", TXT.count("::: {.ex-sep}"), 9)
eq("exercise-block は 1 個", TXT.count("::: {.exercise-block}"), 1)

# 図の参照
for fid in ("build", "follow", "match", "features", "exercises"):
    in_text("図 %s の定義" % fid, "{#fig-ahl515-%s" % fid)
    eq("図 %s が本文から参照されている" % fid,
       TXT.count("@fig-ahl515-%s" % fid) >= 1, True)
    p = os.path.join(os.path.dirname(QMD), "img", "ahl-5-15-%s.svg" % fid)
    eq("SVG %s が存在する" % fid, os.path.exists(p), True)

# 例題 id
for e in ("values", "match", "sketch", "logistic"):
    in_text("例題 %s" % e, "{#exm-ahl515-%s}" % e)

# 章内アンカー
for a in ("idea", "build", "follow", "particular", "read", "match", "limits",
          "why", "unique", "equilibrium-why", "gdc-plot", "gdc-window",
          "gdc-caution"):
    in_text("アンカー #%s" % a, "{#%s}" % a)

# 章内リンクの飛び先が存在するか
anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TXT))
targets = set(re.findall(r"\]\(#([a-z0-9-]+)\)", TXT))
eq("章内リンクの飛び先がすべて存在する", sorted(targets - anchors), [])

# crossref の飛び先が存在するか
defined = set(re.findall(r"\{#((?:fig|tbl|exm|eq)-[a-z0-9-]+)", TXT))
used = set(re.findall(r"@((?:fig|tbl|exm|eq)-[a-z0-9-]+)", TXT))
eq("crossref の飛び先がすべて存在する", sorted(used - defined), [])

# 表にはキャプションが要る
eq("表のキャプション数", len(re.findall(r"^: .+\{#tbl-", TXT, re.M)),
   len(re.findall(r"\{#tbl-ahl515-", TXT)))

# 禁止語
for w in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん", "当たり前"]:
    not_in_text("禁止語 %s" % w, w)
# 「確かめ」単独の名詞（確かめ方・確かめられ… は可）
bad_kakume = [m for m in re.finditer(r"確かめ(?![方らてるればよな])", TXT)]
eq("「確かめ」の単独名詞用法が無い", [TXT[m.start():m.start() + 6]
                                     for m in bad_kakume], [])

# 検算が入っている
eq("**検算。** の数", TXT.count("**検算。**") >= 8, True)

# code span の中に数式・markdown が無い
bad = [m for m in re.findall(r"`[^`\n]+`", TXT) if "$" in m or "**" in m]
eq("code span の中に数式・markdown が無い", bad, [])

# 開き fence の前に空行がある
L = TXT.split("\n")
nb = [i + 1 for i, l in enumerate(L)
      if re.match(r"^:{3,} *\{", l) and i > 0
      and L[i - 1].strip() != "" and not L[i - 1].lstrip().startswith("#")]
eq("開き fence の前に空行がある", nb, [])

# fence の開閉が合っている
opens = len([l for l in L if re.match(r"^:{3,} *\{", l)])
closes = len([l for l in L if re.match(r"^:{3,} *$", l)])
eq("fence の開きと閉じの数が一致", opens, closes)

# Worked examples の冒頭 callout が定型どおり
in_text("Worked examples の定型 callout",
        "問題文は英語です。意味が理解できなかったら、問題文の下の"
        "「**日本語訳**」を開いてください。解説は日本語です。")

# 見出しの表記
in_text("例題の解答例の見出し", "## 解答例（答案用紙にはこう書く）")
in_text("演習の解答例の見出し", "## 解答例（答案用紙に書くこと）")

# Describe / Explain / Justify / Comment / Identify を含む設問には model-answer
eq("model-answer の数", TXT.count("::: {.model-answer}") >= 12, True)

# GDC は TI-Nspire CX II（非 CAS）
in_text("GDC の見出し", "## Using your GDC (TI-Nspire CX II)")
not_in_text("deSolve を使うと書いていない", "deSolve を使")

# GDC: Press-to-Test で微分方程式機能が使えないことを書いている
in_text("Press-to-Test の注意",
        "## Press-to-Test（試験モード）では、微分方程式の機能が使えません")
not_in_text("menu → Settings を Field Resolution の場所として書いていない",
            "menu → Settings")
not_in_text("「必ずどこかにあります」と断言していない", "必ずどこかにあります")

# row / column の用語が一貫している
not_in_text("演習5 が column を問うていない",
            "Explain why every column of the field looks the same")
in_text("演習5 は row を問うている",
        "Explain why every row of the field looks the same")
in_text("演習10 は column で答えている",
        "every vertical column of the field is identical to every other column")

# features 図に (a)-(d) のラベルが入っている
MK = open(os.path.join(os.path.dirname(__file__), "make_ahl_5_15.py"),
          encoding="utf-8").read()
for lab in ("(a)  slope depends on $x$ only", "(b)  slope depends on $y$ only",
            "(c)  $\\\\dfrac{dP}{dt}", "(d)  $\\\\dfrac{dy}{dx} = y$"):
    eq("features 図のパネル label %s" % lab[:3], lab in MK, True)
# 平衡解 P = 0, 50 が格子に乗っている
eq("logistic の格子が P = 50 を含む",
   "PY = np.arange(0, 62.5, 5.0)" in MK, True)
eq("平衡解の線分を赤で描き直している",
   "slopefield(ax, FLOG, TX, [0.0, 50.0], TR, PR, col=ACC" in MK, True)

# GDC の初期条件の例が図 (d) と一致している
in_text("初期条件の例が図 (d) と一致", "y1_0 = 1, -1, 3")

# AI HL の範囲外であることを断っている
in_text("演習6 の範囲外の断り", "**この解き方（一階線形微分方程式）は AI HL の範囲外です。**")
in_text("演習7 の範囲外の断り", "**この解き方は AI HL の範囲外です。**")
in_text("ロジスティックの範囲外の断り",
        "その積分は AI HL の範囲を超えます。")

# 公式集の記述
in_text("公式集に 5.15 の欄が無いこと", "**5.14 と 5.15 の欄はありません。**")

# シラバスの文言
in_text("シラバス Content", "Slope fields and their diagrams.")
in_text("シラバス Guidance",
        "Students will be required to use and interpret slope fields.")

print()
print("=" * 78)
print("結果:  OK %d / NG %d" % (OK, NG))
print("=" * 78)
raise SystemExit(1 if NG else 0)
