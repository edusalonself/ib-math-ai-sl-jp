"""AHL 5.17a（実固有値の phase portrait）の数値と本文を、独立に検算する。
   実行: python3 figs/ai-hl/check_ahl_5_17a.py

   方針
   1. 固有値・固有ベクトルは sympy に独立に解かせる（ページの値を信用しない）
   2. 厳密解は微分して dx/dt = Mx に戻るかを確かめる
   3. 初期条件・A と B・長期のふるまいを数値で確かめる
   4. .qmd を読んで、本文の文字列が計算結果と合っているか確かめる
   5. code span の中に数式・markdown が無いこと／開き fence の前に空行があること
"""
import os
import re
import numpy as np
import sympy as sp

QMD = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "05-calculus", "ahl-5-17a.qmd")
TXT = open(QMD, encoding="utf-8").read()
OK = NG = 0
t = sp.Symbol("t")


def eq(label, got, want, tol=None):
    global OK, NG
    good = (got == want) if tol is None else abs(got - want) <= tol
    if good:
        OK += 1
        print("  OK  %-56s %s" % (label, got))
    else:
        NG += 1
        print("  NG  %-56s got %s, want %s" % (label, got, want))


def in_text(label, s):
    global OK, NG
    if s in TXT:
        OK += 1
        print("  OK  %-56s (本文にある)" % label)
    else:
        NG += 1
        print("  NG  %-56s 本文に無い: %r" % (label, s))


def not_in_text(label, s):
    global OK, NG
    if s not in TXT:
        OK += 1
        print("  OK  %-56s (本文に無い)" % label)
    else:
        NG += 1
        print("  NG  %-56s 本文にある（あってはいけない）: %r" % (label, s))


def spectrum(M):
    """固有値を昇順で、各固有ベクトルを「最初の非零成分を 1 にした」形で返す。"""
    M = sp.Matrix(M)
    out = []
    for val, mult, vecs in M.eigenvects():
        v = sp.Matrix(vecs[0])
        k = next(c for c in v if c != 0)
        out.append((sp.nsimplify(val), sp.simplify(v / k)))
    out.sort(key=lambda z: sp.re(z[0]))
    return out


def disc_a(M):
    M = sp.Matrix(M)
    return sp.nsimplify(M.trace() ** 2 - 4 * M.det())


def parallel(u, v):
    u, v = sp.Matrix(u), sp.Matrix(v)
    return sp.simplify(u[0] * v[1] - u[1] * v[0]) == 0


def solves(M, sol):
    """sol(t) が dx/dt = M x を満たすか。"""
    M, sol = sp.Matrix(M), sp.Matrix(sol)
    return sp.simplify(sp.diff(sol, t) - M * sol) == sp.zeros(2, 1)


print("=" * 78)
print("1.  例題1  M = [[3,2],[2,3]]  （両方正）")
print("=" * 78)
M1 = [[3, 2], [2, 3]]
sp1 = spectrum(M1)
print("     ", [(v, list(p)) for v, p in sp1])
eq("固有値", sorted([int(v) for v, _ in sp1]), [1, 5])
eq("λ=5 の固有ベクトルは (1,1) に平行",
   parallel([p for v, p in sp1 if v == 5][0], [1, 1]), True)
eq("λ=1 の固有ベクトルは (1,-1) に平行",
   parallel([p for v, p in sp1 if v == 1][0], [1, -1]), True)
eq("対角の和", sp.Matrix(M1).trace(), 6)
eq("det", sp.Matrix(M1).det(), 5)

sol1 = sp.Matrix([2 * sp.exp(5 * t) - sp.exp(t), 2 * sp.exp(5 * t) + sp.exp(t)])
eq("例題1 の特殊解が dx/dt = Mx を満たす", solves(M1, sol1), True)
eq("例題1 x(0)", list(sol1.subs(t, 0)), [1, 3])
eq("例題1 A", 2, 2)
eq("例題1 B", -1, -1)
# A, B を独立に解いて確かめる
A, B = sp.symbols("A B")
s = sp.solve([A + B - 1, A - B - 3], [A, B])
eq("A, B を連立方程式から", (s[A], s[B]), (2, -1))
# 長期：(1,1) 方向に近づく
v = np.array([float(sol1[0].subs(t, 3)), float(sol1[1].subs(t, 3))])
ang = np.degrees(np.arctan2(v[1], v[0]))
eq("t=3 での向きは 45 度に近い", round(ang, 1), 45.0, 0.6)

in_text("例題1 の char eq", "\\lambda^{2} - 6\\lambda + 5 = 0")
in_text("例題1 の λ", "\\lambda_1 = 5, \\qquad \\lambda_2 = 1")
in_text("例題1 の A,B", "A = 2, \\qquad B = -1")
in_text("例題1 の成分", "x = 2e^{5t} - e^{t}$、$y = 2e^{5t} + e^{t}")
in_text("例題1 の検算", "10e^{5t} - e^{t}")

print()
print("=" * 78)
print("2.  例題2  M = [[1,2],[2,1]]  （saddle）")
print("=" * 78)
M2 = [[1, 2], [2, 1]]
sp2 = spectrum(M2)
eq("固有値", sorted([int(v) for v, _ in sp2]), [-1, 3])
eq("λ=3 → (1,1)", parallel([p for v, p in sp2 if v == 3][0], [1, 1]), True)
eq("λ=-1 → (1,-1)", parallel([p for v, p in sp2 if v == -1][0], [1, -1]), True)
eq("det が負（saddle）", sp.Matrix(M2).det() < 0, True)
eq("対角の和", sp.Matrix(M2).trace(), 2)
in_text("例題2 の char eq", "\\lambda^{2} - 2\\lambda - 3 = 0")
in_text("例題2 の saddle 判定",
        "*The eigenvalues $3$ and $-1$ are real and have opposite signs, "
        "so the origin is a saddle point.*")

print()
print("=" * 78)
print("3.  例題3  M = [[-3,2],[2,-3]]  （両方負）")
print("=" * 78)
M3 = [[-3, 2], [2, -3]]
sp3 = spectrum(M3)
eq("固有値", sorted([int(v) for v, _ in sp3]), [-5, -1])
eq("λ=-1 → (1,1)", parallel([p for v, p in sp3 if v == -1][0], [1, 1]), True)
eq("λ=-5 → (1,-1)", parallel([p for v, p in sp3 if v == -5][0], [1, -1]), True)
sol3 = sp.Matrix([2 * sp.exp(-t) + 2 * sp.exp(-5 * t),
                  2 * sp.exp(-t) - 2 * sp.exp(-5 * t)])
eq("例題3 の解が dx/dt = Mx を満たす", solves(M3, sol3), True)
eq("例題3 x(0)", list(sol3.subs(t, 0)), [4, 0])
eq("例題3 t=2 の x（3桁）", round(float(sol3[0].subs(t, 2)), 3), 0.271, 1e-3)
eq("例題3 t=2 の y（3桁）", round(float(sol3[1].subs(t, 2)), 3), 0.271, 1e-3)
eq("例題3 t=2 の 2e^{-10}（4桁）", round(float(2 * sp.exp(-10)), 7), 0.0000908,
   1e-7)
eq("例題3 極限は 0", float(sp.limit(sol3[0], t, sp.oo)), 0.0, 1e-12)
in_text("例題3 の char eq", "\\lambda^{2} + 6\\lambda + 5 = 0")
in_text("例題3 の t=2", "x = 0.271 + 0.0000908 = 0.271")

print()
print("=" * 78)
print("4.  例題4  分類（det と対角の和）")
print("=" * 78)
for M, want, lab in ((( [[4, 1], [1, 4]] ), [3, 5], "(a) unstable node"),
                     (( [[-2, 1], [1, -2]] ), [-3, -1], "(b) stable node"),
                     (( [[0, 1], [2, 1]] ), [-1, 2], "(c) saddle")):
    s_ = spectrum(M)
    eq("例題4 %s の固有値" % lab, sorted([int(v) for v, _ in s_]), want)
eq("例題4 (a) 和", sp.Matrix([[4, 1], [1, 4]]).trace(), 8)
eq("例題4 (a) det", sp.Matrix([[4, 1], [1, 4]]).det(), 15)
eq("例題4 (b) 和", sp.Matrix([[-2, 1], [1, -2]]).trace(), -4)
eq("例題4 (b) det", sp.Matrix([[-2, 1], [1, -2]]).det(), 3)
eq("例題4 (c) 和", sp.Matrix([[0, 1], [2, 1]]).trace(), 1)
eq("例題4 (c) det", sp.Matrix([[0, 1], [2, 1]]).det(), -2)
in_text("例題4 (a)", "\\lambda^{2} - 8\\lambda + 15 = 0 \\ \\Longrightarrow \\ \\lambda = 5,\\ 3")
in_text("例題4 (b)", "\\lambda^{2} + 4\\lambda + 3 = 0 \\ \\Longrightarrow \\ \\lambda = -1,\\ -3")
in_text("例題4 (c)", "\\lambda^{2} - \\lambda - 2 = 0 \\ \\Longrightarrow \\ \\lambda = 2,\\ -1")

print()
print("=" * 78)
print("5.  演習の数値")
print("=" * 78)
# 演習1
_x, _y = sp.symbols("x y")
eq("演習1 の行列", list(sp.Matrix([[3, 4], [1, 0]]) * sp.Matrix([_x, _y])),
   [3 * _x + 4 * _y, _x])
eq("演習1 の固有値",
   sorted([int(v) for v in sp.Matrix([[3, 4], [1, 0]]).eigenvals()]), [-1, 4])
eq("演習1 は実で異なる（このページの範囲）", disc_a([[3, 4], [1, 0]]) > 0, True)
eq("演習1 対角の和/det",
   (sp.Matrix([[3, 4], [1, 0]]).trace(), sp.Matrix([[3, 4], [1, 0]]).det()),
   (3, -4))
in_text("演習1 解答", "\\begin{pmatrix} 3 & 4 \\\\ 1 & 0 \\end{pmatrix}")
in_text("演習1 の char eq", "\\lambda^{2} - 3\\lambda - 4 = 0, \\qquad \\lambda = 4 \\text{ or } -1")

# 演習2
s_ = spectrum([[2, 1], [1, 2]])
eq("演習2 固有値", sorted([int(v) for v, _ in s_]), [1, 3])
eq("演習2 λ=3 → (1,1)", parallel([p for v, p in s_ if v == 3][0], [1, 1]), True)
in_text("演習2 char", "\\lambda^{2} - 4\\lambda + 3 = 0")

# 演習3
M = [[-1, 3], [3, -1]]
s_ = spectrum(M)
eq("演習3 固有値", sorted([int(v) for v, _ in s_]), [-4, 2])
eq("演習3 det", sp.Matrix(M).det(), -8)
eq("演習3 和", sp.Matrix(M).trace(), -2)
in_text("演習3 char", "\\lambda^{2} + 2\\lambda - 8 = 0")
in_text("演習3 直線", "\\Rightarrow \\ y = x \\qquad")

# 演習4
M = [[5, -2], [-2, 2]]
s_ = spectrum(M)
eq("演習4 固有値", sorted([int(v) for v, _ in s_]), [1, 6])
eq("演習4 λ=6 → (2,-1)", parallel([p for v, p in s_ if v == 6][0], [2, -1]), True)
eq("演習4 λ=1 → (1,2)", parallel([p for v, p in s_ if v == 1][0], [1, 2]), True)
eq("演習4 M p1 = 6 p1",
   list(sp.Matrix(M) * sp.Matrix([2, -1])), [12, -6])
eq("演習4 和", sp.Matrix(M).trace(), 7)
eq("演習4 det", sp.Matrix(M).det(), 6)
in_text("演習4 Mp1", "\\begin{pmatrix} 12 \\\\ -6 \\end{pmatrix} = 6\\begin{pmatrix} 2 \\\\ -1 \\end{pmatrix}")

# 演習5
s = sp.solve([A + B - 5, 2 * A - B - 4], [A, B])
eq("演習5 A,B", (s[A], s[B]), (3, 2))
eq("演習5 検算", list(3 * sp.Matrix([1, 2]) + 2 * sp.Matrix([1, -1])), [5, 4])
in_text("演習5 A,B", "*Adding:* $\\ 3A = 9$, *so* $A = 3$ *and* $B = 2$.")

# 演習6
for M, want, lab in (([[-4, 1], [2, -3]], [-5, -2], "(a)"),
                     ([[1, 4], [2, -1]], [-3, 3], "(b)"),
                     ([[3, 1], [0, 1]], [1, 3], "(c)")):
    s_ = spectrum(M)
    eq("演習6 %s 固有値" % lab, sorted([int(v) for v, _ in s_]), want)
eq("演習6 (a) 和/det", (sp.Matrix([[-4, 1], [2, -3]]).trace(),
                        sp.Matrix([[-4, 1], [2, -3]]).det()), (-7, 10))
eq("演習6 (b) 和/det", (sp.Matrix([[1, 4], [2, -1]]).trace(),
                        sp.Matrix([[1, 4], [2, -1]]).det()), (0, -9))
eq("演習6 (c) 和/det", (sp.Matrix([[3, 1], [0, 1]]).trace(),
                        sp.Matrix([[3, 1], [0, 1]]).det()), (4, 3))
in_text("演習6 (a)", "\\lambda^{2} + 7\\lambda + 10 = 0$, $\\ \\lambda = -2,\\ -5$")
in_text("演習6 (b)", "\\lambda^{2} - 9 = 0$, $\\ \\lambda = 3,\\ -3$")
in_text("演習6 (c)", "\\lambda^{2} - 4\\lambda + 3 = 0$, $\\ \\lambda = 3,\\ 1$")

# 演習7
M = [[-2, 1], [1, -2]]
s_ = spectrum(M)
eq("演習7 固有値", sorted([int(v) for v, _ in s_]), [-3, -1])
sol7 = sp.Matrix([4 * sp.exp(-t) + 2 * sp.exp(-3 * t),
                  4 * sp.exp(-t) - 2 * sp.exp(-3 * t)])
eq("演習7 解が満たす", solves(M, sol7), True)
eq("演習7 x(0)", list(sol7.subs(t, 0)), [6, 2])
eq("演習7 y(1)（4桁）", round(float(sol7[1].subs(t, 1)), 4), 1.3719, 1e-4)
eq("演習7 y(1)（3桁）", round(float(sol7[1].subs(t, 1)), 2), 1.37, 1e-9)
eq("演習7 x(1)（4桁）", round(float(sol7[0].subs(t, 1)), 4), 1.5711, 1e-4)
eq("演習7 4e^{-1}", round(float(4 * sp.exp(-1)), 4), 1.4715, 1e-4)
eq("演習7 2e^{-3}", round(float(2 * sp.exp(-3)), 4), 0.0996, 1e-4)
in_text("演習7 の計算", "y = 4e^{-1} - 2e^{-3} = 1.4715 - 0.0996 = 1.3719")
in_text("演習7 の x", "x = 4e^{-1} + 2e^{-3} = 1.4715 + 0.0996 = 1.5711")

# 演習8
M = [[1, 6], [1, 2]]
eq("演習8 det", sp.Matrix(M).det(), -4)
eq("演習8 和", sp.Matrix(M).trace(), 3)
s_ = spectrum(M)
eq("演習8 固有値", sorted([int(v) for v, _ in s_]), [-1, 4])
in_text("演習8 正しい det", "\\det M = 1 \\times 2 - 6 \\times 1 = -4")
in_text("演習8 正しい char", "\\lambda^{2} - 3\\lambda - 4 = 0")

# 演習9
s = sp.solve([A + B - 2, A - B + 1], [A, B])
eq("演習9 A,B", (s[A], s[B]), (sp.Rational(1, 2), sp.Rational(3, 2)))
eq("演習9 A > 0", s[A] > 0, True)
eq("演習9 足し戻す",
   list(sp.Rational(1, 2) * sp.Matrix([1, 1]) + sp.Rational(3, 2) * sp.Matrix([1, -1])),
   [2, -1])
eq("演習9 (2,-1) は y=-x の上", -1 > -2, True)
in_text("演習9 A,B", "A + B = 2, \\qquad A - B = -1, \\qquad A = 0.5, \\qquad B = 1.5")

# 演習10
M = [[-5, 3], [3, -5]]
s_ = spectrum(M)
eq("演習10 固有値", sorted([int(v) for v, _ in s_]), [-8, -2])
eq("演習10 和/det", (sp.Matrix(M).trace(), sp.Matrix(M).det()), (-10, 16))
sol10 = sp.Matrix([5 * sp.exp(-2 * t) + 5 * sp.exp(-8 * t),
                   5 * sp.exp(-2 * t) - 5 * sp.exp(-8 * t)])
eq("演習10 解が満たす", solves(M, sol10), True)
eq("演習10 x(0)", list(sol10.subs(t, 0)), [10, 0])
eq("演習10 x - y = 10e^{-8t}",
   sp.simplify(sol10[0] - sol10[1] - 10 * sp.exp(-8 * t)) == 0, True)
eq("演習10 x=y の解は無い", sp.solve(sp.Eq(10 * sp.exp(-8 * t), 0), t), [])
eq("演習10 t=1 の x（4桁）", round(float(sol10[0].subs(t, 1)), 4), 0.6784, 1e-4)
eq("演習10 t=1 の y（4桁）", round(float(sol10[1].subs(t, 1)), 4), 0.6750, 1e-4)
eq("演習10 5e^{-2}（4桁）", round(float(5 * sp.exp(-2)), 4), 0.6767, 1e-4)
eq("演習10 5e^{-8}（4桁）", round(float(5 * sp.exp(-8)), 4), 0.0017, 1e-4)
in_text("演習10 char", "\\lambda^{2} + 10\\lambda + 16 = 0")
in_text("演習10 差", "x - y = 10e^{-8t}")
in_text("演習10 t=1", "x = 5e^{-2} + 5e^{-8} = 0.6767 + 0.0017 = 0.6784")

print()
print("=" * 78)
print("6.  GDC 節の数値")
print("=" * 78)
dx = sp.diff(sol1[0], t)
eq("t=0.2 での dx/dt（2桁）", round(float(dx.subs(t, 0.2)), 2), 25.96, 1e-2)
val = 3 * float(sol1[0].subs(t, 0.2)) + 2 * float(sol1[1].subs(t, 0.2))
eq("t=0.2 での 3x+2y（2桁）", round(val, 2), 25.96, 1e-2)
# GDC の「1 点で確かめる」節は 2026-09 に削除（AHL 5.9a に集約）

print()
print("=" * 78)
print("7.  図が本文と合っているか")
print("=" * 78)
MK = open(os.path.join(os.path.dirname(__file__), "make_ahl_5_17a.py"),
          encoding="utf-8").read()
eq("図の M_OUT が [[3,2],[2,3]]",
   "M_OUT = [[3, 2], [2, 3]]" in MK, True)
eq("図の M_IN が [[-3,2],[2,-3]]",
   "M_IN = [[-3, 2], [2, -3]]" in MK, True)
eq("図の M_SAD が [[1,2],[2,1]]",
   "M_SAD = [[1, 2], [2, 1]]" in MK, True)
for lab in ("along an eigenvector", "(a)  $\\\\lambda = 5,\\\\ 1$",
            "(b)  $\\\\lambda = -1,\\\\ -5$", "$\\\\lambda = 3,\\\\ -1$"):
    eq("図のパネル %s" % lab[:12], lab in MK, True)
# 鞍点図のラベルが取りちがえられていないか
eq("saddle 図：上から出発 → 右上（青）",
   'traj(ax, M_SAD, (1.4, -1.15), col=LINE' in MK
   and 'color=LINE, bbox=BOX' in MK, True)
eq("(1.4,-1.15) は y=-x の上", -1.15 > -1.4, True)
eq("(1.4,-1.15) の (1,1) 成分は正", (1.4 + (-1.15)) / 2 > 0, True)
eq("(-1.4,1.15) の (1,1) 成分は負", (-1.4 + 1.15) / 2 < 0, True)

print()
print("=" * 78)
print("8.  構成・表記の検査")
print("=" * 78)
nos = re.findall(r"\[(\d+)\]\{\.ex-no\}", TXT)
eq("演習の番号", nos, [str(i) for i in range(1, 11)])
eq("ex-sep は 9 個", TXT.count("::: {.ex-sep}"), 9)
eq("exercise-block は 1 個", TXT.count("::: {.exercise-block}"), 1)

for fid in ("eigen", "nodes", "saddle", "longrun"):
    in_text("図 %s の定義" % fid, "{#fig-ahl517a-%s" % fid)
    eq("図 %s が参照されている" % fid, TXT.count("@fig-ahl517a-%s" % fid) >= 1,
       True)
    p = os.path.join(os.path.dirname(QMD), "img", "ahl-5-17a-%s.svg" % fid)
    eq("SVG %s が存在する" % fid, os.path.exists(p), True)

for e in ("node", "saddle", "stable", "classify"):
    in_text("例題 %s" % e, "{#exm-ahl517a-%s}" % e)
for a in ("idea", "straight", "general", "step1", "step2", "step3",
          "initial", "signs", "saddle",
          "longrun", "sketch", "why", "why-two", "why-saddle", "gdc-eig",
          "gdc-plot"):
    in_text("アンカー #%s" % a, "{#%s}" % a)

anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TXT)) | {"common-errors"}
targets = set(re.findall(r"\]\(#([a-z0-9-]+)\)", TXT))
eq("章内リンクの飛び先がすべて存在する", sorted(targets - anchors), [])
defined = set(re.findall(r"\{#((?:fig|tbl|exm|eq)-[a-z0-9-]+)", TXT))
used = set(re.findall(r"@((?:fig|tbl|exm|eq)-[a-z0-9-]+)", TXT))
eq("crossref の飛び先がすべて存在する", sorted(used - defined), [])
eq("表のキャプション数", len(re.findall(r"^: .*\{#tbl-", TXT, re.M)),
   len(re.findall(r"\{#tbl-ahl517a-", TXT)))

# 存在するページにだけリンクしているか
here = os.path.dirname(QMD)
for m in set(re.findall(r"\]\((ahl-[a-z0-9-]+\.qmd)", TXT)):
    eq("リンク先 %s が存在する" % m, os.path.exists(os.path.join(here, m)), True)
for m in set(re.findall(r"\]\((\.\./[^)#]+\.qmd)", TXT)):
    eq("リンク先 %s が存在する" % m, os.path.exists(os.path.join(here, m)), True)

# レビュー修正の固定（回帰防止）
not_in_text("λ<0 で「同じ向き」と書いていない", "**進む向きが、今いる向きと同じ**です")
in_text("λ の符号は e^{λt} で説明している",
        "- $\\lambda < 0$ なら、$e^{\\lambda t}$ は時間とともに **$0$ へ近づく**")
in_text("trace の別解を AHL 1.15 に送っている",
        "対角に並ぶ $2$ つの数の和（**trace**）と $\\det M$ を使えば")
in_text("node の訳", "**node**（結節点）と **saddle point**（鞍点）")
in_text("unstable node の訳", "**unstable node**（不安定な結節点）")
in_text("早見表に判別式が入っている", "| $\\Delta < 0$ | **複素数** → [AHL 5.17b](ahl-5-17b.qmd) |")
in_text("答案の言い方が表に入っている",
        "`all solutions move away from the origin`")
in_text("答案の言い方2", "`all solutions move towards the origin`")
in_text("答案の言い方3", "`the origin is a saddle point`")
in_text("演習7 の等式が正しい", "1.4715 - 0.0996 = 1.3719 = 1.37 \\ (3 \\text{ s.f.})")
in_text("演習3 に sketch がある",
        "**(c)** [Sketch a phase portrait, showing the two straight lines, "
        "the direction of motion on each, and two other trajectories.]{.q-en}")
not_in_text("常体が残っていない", "固有ベクトルは求めなくてよい。")

for w in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん", "当たり前"]:
    not_in_text("禁止語 %s" % w, w)
bad_k = [TXT[m.start():m.start() + 6]
         for m in re.finditer(r"確かめ(?![方らてるればよなま])", TXT)]
eq("「確かめ」の単独名詞用法が無い", bad_k, [])
eq("**検算。** が 8 個以上", TXT.count("**検算。**") >= 8, True)
eq("model-answer が 10 個以上", TXT.count("::: {.model-answer}") >= 10, True)

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
in_text("公式集の式", "\\mathbf{X} = A\\mathbf{p}_1 e^{\\lambda_1 t} + B\\mathbf{p}_2 e^{\\lambda_2 t}")
not_in_text("状態ベクトルに小文字 x を使っていない", "\\mathbf{x}")
in_text("公式集に載っている旨", "この式は**公式集に載っています（5.17 の欄）。覚える必要はありません。**")
in_text("char eq は覚える", "**$\\det(M - \\lambda I) = 0$ は公式集に載っていません**")
in_text("扱う形", "**右辺が $x$ と $y$ の一次式だけ**という特別な場合")
in_text("厳密解の限定",
        "シラバスで**式による解法が求められている、異なる $2$ つの実固有値**の場合を扱います")
not_in_text("旧・実で異なる", "**実で、異なる**")
in_text("シラバス distinct non-zero",
        'Systems will have **distinct, non-zero**, eigenvalues')


# ══════════════════════════════════════════════════════════
#  2026-08: 分類表と dominant eigenvalue の条件
# ══════════════════════════════════════════════════════════
in_text("unstable node の行",
        "| **両方とも正** | **unstable node**（不安定な結節点） | "
        "原点以外のすべての軌道が原点から**離れる**。")
in_text("stable node の行",
        "| **両方とも負** | **stable node**（安定な結節点） | "
        "原点以外のすべての軌道が原点に**近づく**。")
in_text("saddle の行",
        "| **符号が違う** | **saddle point**（鞍点） | "
        "固有ベクトルの向きによって、**近づく**ものと**離れる**ものがある。")
in_text("表が図を指している", "| @fig-ahl517a-nodes (a) |")
not_in_text("旧 unstable node", "| **両方とも正** | **unstable node**（不安定な結節点） | すべての軌道が原点から**離れる** |")
not_in_text("旧 stable node", "| **両方とも負** | **stable node**（安定な結節点） | すべての軌道が原点に**近づく** |")
not_in_text("旧 saddle", "| **符号が違う** | **saddle point**（鞍点） | 近づいてから、**離れる** |")
in_text("saddle は第6節でくわしく",
        "@fig-ahl517a-saddle（[第6節](#saddle)）")
in_text("答案の言い方を使うよう促している",
        "**表の英語をそのまま使う**のがいちばん安全です")
in_text("第6節の但し書き",
        "**「すべての軌道が、近づいてから離れる」わけではありません。**")
not_in_text("旧・第6節", "そのあいだの軌道は、**いったん近づいてから、向きを変えて離れていきます。**")
# dominant eigenvalue
in_text("A≠0 の条件",
        "\\mathbf{X} \\approx A\\mathbf{p}_1 e^{5t} \\qquad "
        "(A \\neq 0 \\text{ で、} t \\text{ が大きいとき})")
not_in_text("旧・無条件の近似",
            "\\mathbf{X} \\approx A\\mathbf{p}_1 e^{5t} \\qquad (t \\text{ が大きいとき})")
in_text("支配的の言い換え",
        "\\text{係数が } 0 \\text{ でなければ、大きいほうの } \\lambda \\text{ の項が支配的になる}")
not_in_text("旧・いつも勝つ", "\\text{生き残るのは、いつも } \\lambda \\text{ が大きいほう}")
in_text("係数 0 の例外",
        "**ただし、その項の係数が $0$ の場合は例外です。**")
in_text("例外の説明",
        "たとえば初期条件がもう一方の固有ベクトルの上にあると、"
        "大きい固有値に対応する項は**最初から現れません**")
in_text("かき方の3", "3. そのあいだに、**近づいてから $y = x$ の向きへ離れる**曲線を数本")

# 数値で確かめる: A = 0 なら e^{5t} の項は現れない
import numpy as _np
_p1 = _np.array([1.0, 1.0])
_p2 = _np.array([1.0, -1.0])
for _t in (0.0, 1.0, 5.0, 10.0):
    _x = 0.0 * _p1 * _np.exp(5 * _t) + 3.0 * _p2 * _np.exp(_t)
    eq("A=0 なら軌道は p2 の直線上（t=%g）" % _t,
       bool(abs(_x[0] + _x[1]) < 1e-9), True)
# A != 0 なら p1 の向きに近づく
_x = 1e-6 * _p1 * _np.exp(5 * 10.0) + 1e6 * _p2 * _np.exp(10.0)
_u = _x / _np.linalg.norm(_x)
_d = _p1 / _np.linalg.norm(_p1)
eq("A≠0 なら十分大きい t で p1 の向き", bool(abs(abs(_u @ _d) - 1) < 1e-3), True)
# saddle: 負の固有ベクトル上の軌道は原点に近づき続ける（離れない）
_norms = [_np.linalg.norm(0.0 * _p1 * _np.exp(3 * t) + 2.0 * _p2 * _np.exp(-t))
          for t in (0, 1, 2, 5, 10)]
eq("負の固有ベクトル上では、ずっと原点に近づく",
   all(a > b for a, b in zip(_norms, _norms[1:])), True)


# レビューで追加: 「近づいてから離れる」は出発点しだい／交差の理由も一意性に
in_text("saddle の一般軌道は出発点しだい",
        "出発点によっては、その前に**いったん原点に近づいてから向きを変えます。**")
in_text("3 通りの区別", "- $\\lambda = -1$ の固有ベクトルの直線上 … "
        "そのまま原点に近づき続けます（離れません）")
not_in_text("旧・一般軌道は必ず近づいてから",
            "**この $2$ 本の直線の上にない一般の軌道**は、いったん原点の近くまで来てから、")
in_text("交差しない理由も一意性",
        "[AHL 5.15](ahl-5-15.qmd#read) と同じ理由です。ここで扱う系では、"
        "**initial condition から解が $1$ つに定まる**からです。")
not_in_text("旧・傾きが1つだから",
            "$1$ 点での $\\dfrac{d\\mathbf{x}}{dt}$ は $1$ つしかありません。")
# 一般の軌道が「必ず近づいてから離れる」わけではないことを数値で示す
_A0, _B0 = 2.0, 1.0          # (3, 1) から出発（どちらの固有直線上でもない）
_r = [_np.linalg.norm(_A0 * _p1 * _np.exp(3 * t) + _B0 * _p2 * _np.exp(-t))
      for t in [0, 0.1, 0.3, 1.0, 2.0]]
eq("A,B とも正なら、最初から離れる一方（近づく段階がない）",
   all(a < b for a, b in zip(_r, _r[1:])), True)
_A1, _B1 = 0.05, 1.95        # こちらは近づいてから離れる
_r2 = [_np.linalg.norm(_A1 * _p1 * _np.exp(3 * t) + _B1 * _p2 * _np.exp(-t))
       for t in [0, 0.4, 0.78, 1.5, 3.0]]
eq("A が小さいときは、いったん近づいてから離れる",
   min(_r2) < _r2[0] and _r2[-1] > _r2[0], True)
# 図の脚注も直した
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
eq("図のファイルがある",
   _os.path.exists(_os.path.join(_HERE, "..", "..", "ai-hl", "05-calculus",
                                 "img", "ahl-5-17a-longrun.svg")), True)
_SRC = open(_os.path.join(_HERE, "make_ahl_5_17a.py"), encoding="utf-8").read()
eq("図の脚注に「係数が 0 でなければ」",
   "whenever its coefficient is not zero" in _SRC, True)
eq("図の脚注から「come in along it, then turn」を外した",
   "paths come in " in _SRC, False)

print()
print("=" * 78)
print("結果:  OK %d / NG %d" % (OK, NG))
print("=" * 78)
raise SystemExit(1 if NG else 0)
