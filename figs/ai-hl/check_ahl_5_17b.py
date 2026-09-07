"""AHL 5.17b（複素固有値の phase portrait）の数値と本文を、独立に検算する。
   実行: python3 figs/ai-hl/check_ahl_5_17b.py

   方針
   1. 固有値は sympy に独立に解かせる（ページの値を信用しない）
   2. 回る向きは、行列を (1,0) に掛けて dy/dt の符号から独立に判定する
   3. 円・楕円は「保存量の微分が 0」を sympy で確かめる
   4. .qmd を読んで、本文の文字列が計算結果と合っているか確かめる
   5. code span の中に数式・markdown が無いこと／開き fence の前に空行があること
"""
import os
import re
import sympy as sp

QMD = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "05-calculus", "ahl-5-17b.qmd")
TXT = open(QMD, encoding="utf-8").read()
OK = NG = 0
t = sp.Symbol("t")
I = sp.I


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


def eigs(M):
    """固有値を sympy に解かせ、(実部, 虚部の絶対値) の組で返す。"""
    vals = sorted(sp.Matrix(M).eigenvals().keys(), key=lambda z: sp.im(z))
    return [(sp.nsimplify(sp.re(v)), sp.nsimplify(sp.im(v))) for v in vals]


def disc(M):
    M = sp.Matrix(M)
    return sp.nsimplify(M.trace() ** 2 - 4 * M.det())


def turn(M):
    """(1,0) を代入したときの dy/dt の符号 → 回る向き。"""
    c = sp.Matrix(M)[1, 0]
    return "anticlockwise" if c > 0 else ("clockwise" if c < 0 else "none")


def conserved(M, expr):
    """expr(x, y) が軌道に沿って一定か（d/dt を鎖則で展開して 0 か）。"""
    x, y = sp.symbols("x y")
    M = sp.Matrix(M)
    dx = M[0, 0] * x + M[0, 1] * y
    dy = M[1, 0] * x + M[1, 1] * y
    return sp.simplify(sp.diff(expr, x) * dx + sp.diff(expr, y) * dy) == 0


x, y = sp.symbols("x y")

print("=" * 78)
print("1.  例題1  M = [[-1,-2],[2,-1]]")
print("=" * 78)
M1 = [[-1, -2], [2, -1]]
e = eigs(M1)
print("     固有値:", sp.Matrix(M1).eigenvals())
eq("実部", sorted({r for r, _ in e}), [-1])
eq("虚部", sorted({im for _, im in e}), [-2, 2])
eq("判別式", disc(M1), -16)
eq("対角の和", sp.Matrix(M1).trace(), -2)
eq("det", sp.Matrix(M1).det(), 5)
eq("実部が負 → 内向き", all(r < 0 for r, _ in e), True)
eq("(1,0) での dy/dt", sp.Matrix(M1)[1, 0], 2)
eq("回る向き", turn(M1), "anticlockwise")
eq("(1,0) での dx/dt", sp.Matrix(M1)[0, 0], -1)
in_text("例題1 の char eq", "\\lambda^{2} + 2\\lambda + 5 = 0")
in_text("例題1 の固有値", "\\frac{-2 \\pm 4i}{2} = -1 \\pm 2i")
in_text("例題1 の判別式", "(-2)^{2} - 4(5) = 4 - 20 = -16 < 0")
in_text("例題1 の代入", "\\frac{dx}{dt} = -1 - 0 = -1, \\qquad \\frac{dy}{dt} = 2 - 0 = 2")
in_text("例題1 の向き", "the trajectories are traced anticlockwise")

print()
print("=" * 78)
print("2.  例題2  M = [[0,-2],[2,0]]（円）")
print("=" * 78)
M2 = [[0, -2], [2, 0]]
e = eigs(M2)
eq("実部は 0", sorted({r for r, _ in e}), [0])
eq("虚部", sorted({im for _, im in e}), [-2, 2])
eq("対角の和", sp.Matrix(M2).trace(), 0)
eq("det", sp.Matrix(M2).det(), 4)
eq("x^2+y^2 が保存される（円）", conserved(M2, x ** 2 + y ** 2), True)
eq("回る向き", turn(M2), "anticlockwise")
in_text("例題2 の char eq", "\\lambda^{2} - 0\\lambda + 4 = 0 \\ \\Longrightarrow \\ \\lambda^{2} = -4 \\ \\Longrightarrow \\ \\lambda = \\pm 2i")
in_text("例題2 の (c)", "2x(-2y) + 2y(2x) = -4xy + 4xy = 0")
in_text("例題2 の答えは円または楕円",
        "*The eigenvalues are purely imaginary, so the trajectories are "
        "closed curves: circles or ellipses.*")

print()
print("=" * 78)
print("3.  楕円の例  M = [[0,-1],[4,0]]")
print("=" * 78)
M_E = [[0, -1], [4, 0]]
e = eigs(M_E)
eq("実部は 0", sorted({r for r, _ in e}), [0])
eq("虚部は ±2", sorted({im for _, im in e}), [-2, 2])
eq("det", sp.Matrix(M_E).det(), 4)
eq("4x^2+y^2 が保存される（楕円）", conserved(M_E, 4 * x ** 2 + y ** 2), True)
eq("x^2+y^2 は保存されない", conserved(M_E, x ** 2 + y ** 2), False)
eq("円の系と同じ固有値", eigs(M2) == eigs(M_E), True)
in_text("Why it works の楕円", "8x(-y) + 2y(4x) = -8xy + 8xy = 0")

print()
print("=" * 78)
print("4.  例題3  分類")
print("=" * 78)
for M, wr, wi, wd, lab in ((( [[2, -1], [1, 2]] ), 2, 1, -4, "(a) 2±i"),
                           (( [[-2, -3], [3, -2]] ), -2, 3, -36, "(b) -2±3i"),
                           (( [[3, 1], [1, 3]] ), None, None, 4, "(c) 実数")):
    d = disc(M)
    eq("例題3 %s の判別式" % lab, d, wd)
    if wr is not None:
        e = eigs(M)
        eq("例題3 %s の実部" % lab, sorted({r for r, _ in e}), [wr])
        eq("例題3 %s の虚部" % lab, sorted({im for _, im in e}), [-wi, wi])
eq("例題3 (c) の固有値",
   sorted([int(v) for v in sp.Matrix([[3, 1], [1, 3]]).eigenvals()]), [2, 4])
eq("(2+i)(2-i)", sp.expand((2 + I) * (2 - I)), 5)
eq("(-2+3i)(-2-3i)", sp.expand((-2 + 3 * I) * (-2 - 3 * I)), 13)
in_text("例題3 (a)", "\\lambda^{2} - 4\\lambda + 5 = 0 \\ \\Longrightarrow \\ \\lambda = \\frac{4 \\pm \\sqrt{-4}}{2} = 2 \\pm i")
in_text("例題3 (b)", "\\lambda^{2} + 4\\lambda + 13 = 0 \\ \\Longrightarrow \\ \\lambda = \\frac{-4 \\pm \\sqrt{-36}}{2} = -2 \\pm 3i")
in_text("例題3 (c)", "\\lambda^{2} - 6\\lambda + 8 = 0 \\ \\Longrightarrow \\ \\lambda = 4,\\ 2")

print()
print("=" * 78)
print("5.  例題4  タンク  M = [[-0.2,-3],[3,-0.2]]")
print("=" * 78)
M4 = [[sp.Rational(-1, 5), -3], [3, sp.Rational(-1, 5)]]
e = eigs(M4)
eq("実部", sorted({r for r, _ in e}), [sp.Rational(-1, 5)])
eq("虚部", sorted({im for _, im in e}), [-3, 3])
eq("det", sp.nsimplify(sp.Matrix(M4).det()), sp.Rational(226, 25))
eq("det を小数で", float(sp.Matrix(M4).det()), 9.04, 1e-12)
eq("対角の和", sp.nsimplify(sp.Matrix(M4).trace()), sp.Rational(-2, 5))
eq("判別式", float(disc(M4)), -36.0, 1e-12)
eq("回る向き", turn(M4), "anticlockwise")
in_text("例題4 の char eq", "\\lambda^{2} + 0.4\\lambda + 9.04 = 0")
in_text("例題4 の固有値", "\\frac{-0.4 \\pm 6i}{2} = -0.2 \\pm 3i")
in_text("例題4 の判別式", "0.16 - 4(9.04) = 0.16 - 36.16 = -36 < 0")

print()
print("=" * 78)
print("6.  演習の数値")
print("=" * 78)
# 演習1
M = [[2, -1], [1, 2]]
e = eigs(M)
eq("演習1 実部", sorted({r for r, _ in e}), [2])
eq("演習1 虚部", sorted({im for _, im in e}), [-1, 1])
eq("演習1 判別式", disc(M), -4)
in_text("演習1 解答", "\\lambda = \\frac{4 \\pm \\sqrt{16 - 20}}{2} = \\frac{4 \\pm 2i}{2} = 2 \\pm i")

# 演習2
M = [[-2, -3], [3, -2]]
e = eigs(M)
eq("演習2 実部", sorted({r for r, _ in e}), [-2])
eq("演習2 虚部", sorted({im for _, im in e}), [-3, 3])
eq("演習2 判別式", disc(M), -36)
in_text("演習2 解答", "\\lambda^{2} + 4\\lambda + 13 = 0, \\qquad \\lambda = \\frac{-4 \\pm \\sqrt{-36}}{2} = -2 \\pm 3i")

# 演習3
M = [[0, -3], [3, 0]]
e = eigs(M)
eq("演習3 実部は 0", sorted({r for r, _ in e}), [0])
eq("演習3 虚部は ±3", sorted({im for _, im in e}), [-3, 3])
eq("演習3 det", sp.Matrix(M).det(), 9)
eq("演習3 向き", turn(M), "anticlockwise")
eq("演習3 x^2+y^2 保存（円）", conserved(M, x ** 2 + y ** 2), True)
in_text("演習3 解答", "\\lambda^{2} + 9 = 0, \\qquad \\lambda = \\pm 3i")
in_text("演習3 検算", "2x(-3y) + 2y(3x) = 0")

# 演習4
M = [[0, 4], [-1, 0]]
e = eigs(M)
eq("演習4 実部は 0", sorted({r for r, _ in e}), [0])
eq("演習4 虚部は ±2", sorted({im for _, im in e}), [-2, 2])
eq("演習4 det", sp.Matrix(M).det(), 4)
eq("演習4 向きは時計回り", turn(M), "clockwise")
eq("演習4 x^2+4y^2 保存（楕円）", conserved(M, x ** 2 + 4 * y ** 2), True)
eq("演習4 x^2+y^2 は保存されない", conserved(M, x ** 2 + y ** 2), False)
in_text("演習4 det", "\\det = 0 - (4)(-1) = 4")
in_text("演習4 向き", "the trajectories are traced clockwise")
in_text("演習4 検算", "2x(4y) + 8y(-x) = 8xy - 8xy = 0")

# 演習5
for M, wd, lab in (([[1, -2], [2, 1]], -16, "(a)"),
                   ([[2, 3], [1, 0]], 16, "(b)"),
                   ([[-1, -5], [1, 1]], -16, "(c)")):
    eq("演習5 %s 判別式" % lab, disc(M), wd)
eq("演習5 (a) 実部", sorted({r for r, _ in eigs([[1, -2], [2, 1]])}), [1])
eq("演習5 (a) 虚部", sorted({im for _, im in eigs([[1, -2], [2, 1]])}), [-2, 2])
eq("演習5 (b) 固有値",
   sorted([int(v) for v in sp.Matrix([[2, 3], [1, 0]]).eigenvals()]), [-1, 3])
eq("演習5 (b) det が負（saddle）", sp.Matrix([[2, 3], [1, 0]]).det() < 0, True)
eq("演習5 (c) 実部は 0", sorted({r for r, _ in eigs([[-1, -5], [1, 1]])}), [0])
eq("演習5 (c) 虚部は ±2",
   sorted({im for _, im in eigs([[-1, -5], [1, 1]])}), [-2, 2])
eq("演習5 (c) det", sp.Matrix([[-1, -5], [1, 1]]).det(), 4)
eq("演習5 (c) 対角の和", sp.Matrix([[-1, -5], [1, 1]]).trace(), 0)
in_text("演習5 (c) det", "\\det = (-1)(1) - (-5)(1) = -1 + 5 = 4")

# 演習6（-0.5 ± 4i）
eq("演習6 1 周の時間", round(float(2 * sp.pi / 4), 2), 1.57, 1e-2)
eq("演習6 1 周での減り", round(float(sp.exp(sp.Rational(-1, 2) * 2 * sp.pi / 4)), 3),
   0.456, 1e-3)
eq("演習6 虚部は実部の 8 倍", 4 / 0.5, 8.0, 1e-12)
in_text("演習6 の 1.57", "t = \\dfrac{2\\pi}{4} \\approx 1.57")
in_text("演習6 の 0.456", "e^{-0.785} = 0.456")

# 演習7
M = [[-1, -4], [1, -1]]
e = eigs(M)
eq("演習7 正しい実部", sorted({r for r, _ in e}), [-1])
eq("演習7 正しい虚部", sorted({im for _, im in e}), [-2, 2])
eq("演習7 char eq は生徒のもので合っている",
   (sp.Matrix(M).trace(), sp.Matrix(M).det()), (-2, 5))
eq("演習7 生徒の答えの和は -4（対角の和 -2 と合わない）",
   sp.expand((-2 + 4 * I) + (-2 - 4 * I)), -4)
eq("演習7 生徒の答えの積は 20（det 5 と合わない）",
   sp.expand((-2 + 4 * I) * (-2 - 4 * I)), 20)
in_text("演習7 正しい値", "\\dfrac{-2 \\pm 4i}{2} = -1 \\pm 2i$, not $-2 \\pm 4i$")
in_text("演習7 検算の 20", "$4 + 16 = 20$")

# 演習9
M9 = [[sp.Rational(-1, 10), -2], [2, sp.Rational(-1, 10)]]
e = eigs(M9)
eq("演習9 実部", sorted({r for r, _ in e}), [sp.Rational(-1, 10)])
eq("演習9 虚部", sorted({im for _, im in e}), [-2, 2])
eq("演習9 det", float(sp.Matrix(M9).det()), 4.01, 1e-12)
eq("演習9 判別式", float(disc(M9)), -16.0, 1e-12)
eq("演習9 向き", turn(M9), "anticlockwise")
eq("演習9 1 周の時間", round(float(2 * sp.pi / 2), 2), 3.14, 1e-2)
eq("演習9 1 周での減り",
   round(float(sp.exp(sp.Rational(-1, 10) * sp.pi)), 2), 0.73, 1e-2)
in_text("演習9 char eq", "\\lambda^{2} + 0.2\\lambda + 4.01 = 0")
in_text("演習9 固有値", "\\frac{-0.2 \\pm 4i}{2} = -0.1 \\pm 2i")
in_text("演習9 判別式", "0.04 - 16.04 = -16")
in_text("演習9 の 0.73", "e^{-0.1 \\times 3.14} = 0.73")

# 演習10（k ± i）
k = sp.Symbol("k", real=True)
Mk = sp.Matrix([[k, -1], [1, k]])
eq("演習10 対角の和", sp.simplify(Mk.trace()), 2 * k)
eq("演習10 det", sp.simplify(Mk.det()), k ** 2 + 1)
eq("演習10 判別式は -4（k によらない）",
   sp.simplify(Mk.trace() ** 2 - 4 * Mk.det()), -4)
ek = sorted(Mk.eigenvals().keys(), key=lambda z: sp.im(z))
eq("演習10 固有値は k ± i",
   [sp.simplify(v) for v in ek], [k - I, k + I])
eq("演習10 k=0 なら円の系", turn([[0, -1], [1, 0]]), "anticlockwise")
in_text("演習10 判別式", "4k^{2} - 4(k^{2} + 1) = 4k^{2} - 4k^{2} - 4 = -4")
in_text("演習10 固有値", "\\frac{2k \\pm 2i}{2} = k \\pm i")

print()
print("=" * 78)
print("7.  図が本文と合っているか")
print("=" * 78)
MK = open(os.path.join(os.path.dirname(__file__), "make_ahl_5_17b.py"),
          encoding="utf-8").read()
eq("図の M_IN", "M_IN = [[-1, -2], [2, -1]]" in MK, True)
eq("図の M_OUT", "M_OUT = [[1, -2], [2, 1]]" in MK, True)
eq("図の M_CIR", "M_CIR = [[0, -2], [2, 0]]" in MK, True)
eq("図の M_ELL", "M_ELL = [[0, -1], [4, 0]]" in MK, True)
eq("図の M_CW", "M_CW = [[0, 2], [-2, 0]]" in MK, True)
eq("図に \\u2192 のエスケープが残っていない", "\\u2192" in MK, False)
for lab in ("(a)  $\\\\lambda = -1 \\\\pm 2i$", "(b)  $\\\\lambda = 1 \\\\pm 2i$",
            "(c)  $\\\\lambda = \\\\pm 2i$", "(d)  $\\\\lambda = \\\\pm 2i$"):
    eq("図のパネル %s" % lab[:8], lab in MK, True)
eq("図の M_CW は時計回り", turn([[0, 2], [-2, 0]]), "clockwise")
eq("図の M_CIR は反時計回り", turn([[0, -2], [2, 0]]), "anticlockwise")
eq("図の M_OUT の実部は正",
   all(r > 0 for r, _ in eigs([[1, -2], [2, 1]])), True)

print()
print("=" * 78)
print("8.  構成・表記の検査")
print("=" * 78)
nos = re.findall(r"\[(\d+)\]\{\.ex-no\}", TXT)
eq("演習の番号", nos, [str(i) for i in range(1, 11)])
eq("ex-sep は 9 個", TXT.count("::: {.ex-sep}"), 9)
eq("exercise-block は 1 個", TXT.count("::: {.exercise-block}"), 1)

for fid in ("cases", "direction"):
    in_text("図 %s の定義" % fid, "{#fig-ahl517b-%s" % fid)
    eq("図 %s が参照されている" % fid, TXT.count("@fig-ahl517b-%s" % fid) >= 1,
       True)
    p = os.path.join(os.path.dirname(QMD), "img", "ahl-5-17b-%s.svg" % fid)
    eq("SVG %s が存在する" % fid, os.path.exists(p), True)

for e_ in ("spiral", "circle", "classify", "context"):
    in_text("例題 %s" % e_, "{#exm-ahl517b-%s}" % e_)
for a in ("complex", "real-part", "imaginary", "direction", "five", "sketch",
          "context", "why", "why-spiral", "why-ellipse", "gdc-complex",
          "gdc-disc", "gdc-plot"):
    in_text("アンカー #%s" % a, "{#%s}" % a)

anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TXT)) | {"common-errors"}
targets = set(re.findall(r"\]\(#([a-z0-9-]+)\)", TXT))
eq("章内リンクの飛び先がすべて存在する", sorted(targets - anchors), [])
defined = set(re.findall(r"\{#((?:fig|tbl|exm|eq)-[a-z0-9-]+)", TXT))
used = set(re.findall(r"@((?:fig|tbl|exm|eq)-[a-z0-9-]+)", TXT))
eq("crossref の飛び先がすべて存在する（ページ内のみ）",
   sorted(used - defined), [])
eq("表のキャプション数", len(re.findall(r"^: .*\{#tbl-", TXT, re.M)),
   len(re.findall(r"\{#tbl-ahl517b-", TXT)))

here = os.path.dirname(QMD)
for m in set(re.findall(r"\]\((ahl-[a-z0-9-]+\.qmd)", TXT)):
    eq("リンク先 %s が存在する" % m, os.path.exists(os.path.join(here, m)), True)
for m in set(re.findall(r"\]\((\.\./[^)#]+\.qmd)", TXT)):
    eq("リンク先 %s が存在する" % m, os.path.exists(os.path.join(here, m)), True)

for w in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん", "当たり前"]:
    not_in_text("禁止語 %s" % w, w)
bad_k = [TXT[m.start():m.start() + 6]
         for m in re.finditer(r"確かめ(?![方らてるればよなま])", TXT)]
eq("「確かめ」の単独名詞用法が無い", bad_k, [])
eq("**検算。** が 8 個以上", TXT.count("**検算。**") >= 8, True)
eq("model-answer が 14 個以上", TXT.count("::: {.model-answer}") >= 14, True)

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
in_text("厳密解は要らない旨", "## このページでは、厳密解を求めません")
in_text("AHL 1.15 との違い",
        "## [AHL 1.15](../01-number-and-algebra/ahl-1-15.qmd) との違いに注意してください")
in_text("シラバス Guidance",
        "Qualitative analysis of future paths for distinct, real, complex "
        "and imaginary eigenvalues.")
in_text("シラバス 5 つの場合", "the solutions form a circle or ellipse")
in_text("シラバス key features",
        "**equilibrium points**, **stable populations** and **saddle points**")
in_text("node と centre はシラバス語でない旨",
        "## `node` と `centre` は、シラバスには出てこない語です")
# レビュー修正の固定（回帰防止）
in_text("公式集の説明がある", "公式集の **5.17** の欄には")
in_text("6 通りと書いている", "- $6$ 通りの場合を、すべて見分けられる。")
not_in_text("5 つの表という誤った枠組みが無い", "シラバスが挙げている $5$ つを、$1$ つの表にします。")
not_in_text("text{} の中に markdown 斜体が無い", "\\text{— *")
not_in_text("模範解答に本のページ参照が無い", "This is the case covered in AHL 5.17a")
in_text("アンカーが例題を指している", "ahl-5-17a.qmd#exm-ahl517a-stable")
in_text("anticlockwise を English first で", "**anticlockwise**（反時計回り）です。")
not_in_text("Determinant のメニュー番号を書いていない", "3: Determinant")
in_text("演習2 に sketch がある",
        "**(c)** [Sketch the phase portrait, showing the direction of motion.]{.q-en}")
in_text("演習9(b) に model-answer",
        "*The motion is upwards on the positive $x$-axis, so the trajectory "
        "is traced anticlockwise.*")


# ══════════════════════════════════════════════════════════
#  2026-08: 6 通りの表を AHL 5.17a と同じ書き方にそろえた
# ══════════════════════════════════════════════════════════
in_text("unstable node の行", "| 実数、**両方正** | unstable node | 原点以外の軌道は原点から**離れる** |")
in_text("stable node の行", "| 実数、**両方負** | stable node | 原点以外の軌道は原点に**近づく** |")
in_text("saddle の行",
        "| 実数、**符号が違う** | **saddle point** | 向きによって**近づく**ものと"
        "**離れる**ものがある（[AHL 5.17a](ahl-5-17a.qmd#saddle)） |")
not_in_text("旧 saddle 行", "| 実数、**符号が違う** | **saddle point** | 近づいてから離れる |")


# レビューで追加: 対訳表の saddle 行もそろえた
_GL = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "glossary-ai.qmd"), encoding="utf-8").read()
eq("対訳表の saddle 行",
   "| saddle point | 鞍点 | **HL** 固有値が実数で**異符号**。"
   "固有ベクトルの向きによって、近づくものと離れるものがある |" in _GL, True)
eq("対訳表から「近づいてから離れる」を外した",
   "**異符号**。近づいてから離れる" in _GL, False)

print()
print("=" * 78)
print("結果:  OK %d / NG %d" % (OK, NG))
print("=" * 78)
raise SystemExit(1 if NG else 0)
