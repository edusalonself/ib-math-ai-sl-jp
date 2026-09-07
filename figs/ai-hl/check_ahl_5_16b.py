"""AHL 5.16b（連立系の Euler 法）の数値と本文を、独立に検算する。
   実行: python3 figs/ai-hl/check_ahl_5_16b.py

   方針
   1. 連立系の Euler 法を第一原理から実装する（★ 古い値で両方を計算する）
   2. 平衡点は sympy で連立方程式を解いて求める
   3. 「prey が先にピーク」「反時計回り」は細かい h の数値解から独立に判定する
   4. .qmd を読んで、本文の文字列が計算結果と合っているか確かめる
   5. code span の中に数式・markdown が無いこと／開き fence の前に空行があること
"""
import os
import re
import numpy as np
import sympy as sp

QMD = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "05-calculus", "ahl-5-16b.qmd")
TXT = open(QMD, encoding="utf-8").read()

OK = NG = 0


def eq(label, got, want, tol=None):
    global OK, NG
    good = (got == want) if tol is None else abs(got - want) <= tol
    if good:
        OK += 1
        print("  OK  %-58s %s" % (label, got))
    else:
        NG += 1
        print("  NG  %-58s got %s, want %s" % (label, got, want))


def in_text(label, s):
    global OK, NG
    if s in TXT:
        OK += 1
        print("  OK  %-58s (本文にある)" % label)
    else:
        NG += 1
        print("  NG  %-58s 本文に無い: %r" % (label, s))


def not_in_text(label, s):
    global OK, NG
    if s not in TXT:
        OK += 1
        print("  OK  %-58s (本文に無い)" % label)
    else:
        NG += 1
        print("  NG  %-58s 本文にある（あってはいけない）: %r" % (label, s))


def ceuler(f1, f2, t0, x0, y0, h, n):
    """★ 古い x, y で f1 と f2 を両方計算してから、まとめて更新する。"""
    rows = []
    t, x, y = t0, x0, y0
    for i in range(n):
        a, b = f1(t, x, y), f2(t, x, y)
        rows.append((i, t, x, y, a, b))
        x, y = x + h * a, y + h * b
        t = t + h
    rows.append((n, t, x, y, f1(t, x, y), f2(t, x, y)))
    return rows


print("=" * 78)
print("1.  例題1  dx/dt = x+2y, dy/dt = 3x-y, (1,2), h=0.1, 2 歩")
print("=" * 78)
r = ceuler(lambda t, x, y: x + 2 * y, lambda t, x, y: 3 * x - y,
           0, 1.0, 2.0, 0.1, 2)
for n, tt, xx, yy, a, b in r:
    print("     n=%d t=%.2g x=%.6g y=%.6g f1=%.6g f2=%.6g"
          % (n, tt, xx, yy, a, b))
eq("f1(0)", r[0][4], 5.0, 1e-12)
eq("f2(0)", r[0][5], 1.0, 1e-12)
eq("x1", round(r[1][2], 10), 1.5, 1e-9)
eq("y1", round(r[1][3], 10), 2.1, 1e-9)
eq("f1(1)", round(r[1][4], 10), 5.7, 1e-9)
eq("f2(1)", round(r[1][5], 10), 2.4, 1e-9)
eq("x2", round(r[2][2], 10), 2.07, 1e-9)
eq("y2", round(r[2][3], 10), 2.34, 1e-9)
# 間違ったやり方（新しい x を使う）
eq("誤ったやり方の y1", round(2 + 0.1 * (3 * 1.5 - 2), 10), 2.25, 1e-9)
eq("正しい y1 と違う", 2.1 != 2.25, True)
eq("差", round(2.25 - 2.1, 10), 0.15, 1e-9)

in_text("例題1 f1", "f_1 = 1 + 2(2) = 5, \\qquad f_2 = 3(1) - 2 = 1")
in_text("例題1 x1,y1", "x_1 = 1 + 0.1(5) = 1.5, \\qquad y_1 = 2 + 0.1(1) = 2.1")
in_text("例題1 2歩目 f", "f_1 = 1.5 + 2(2.1) = 5.7, \\qquad f_2 = 3(1.5) - 2.1 = 2.4")
in_text("例題1 答え", "x_2 = 1.5 + 0.1(5.7) = 2.07, \\qquad y_2 = 2.1 + 0.1(2.4) = 2.34")
in_text("誤り例の 2.25", "y_1 = 2 + 0.1(2.5) = 2.25")

print()
print("=" * 78)
print("2.  例題3  predator–prey  (400,100), h=1, 2 歩")
print("=" * 78)


def P1(t, x, y):
    return 0.4 * x - 0.002 * x * y


def P2(t, x, y):
    return -0.3 * y + 0.001 * x * y


r = ceuler(P1, P2, 0, 400.0, 100.0, 1.0, 2)
for n, tt, xx, yy, a, b in r:
    print("     n=%d t=%g x=%.6g y=%.6g f1=%.6g f2=%.6g" % (n, tt, xx, yy, a, b))
eq("f1(0)", round(r[0][4], 10), 80.0, 1e-9)
eq("f2(0)", round(r[0][5], 10), 10.0, 1e-9)
eq("x1", round(r[1][2], 10), 480.0, 1e-9)
eq("y1", round(r[1][3], 10), 110.0, 1e-9)
eq("f1(1)", round(r[1][4], 10), 86.4, 1e-9)
eq("f2(1)", round(r[1][5], 10), 19.8, 1e-9)
eq("x2", round(r[2][2], 10), 566.4, 1e-9)
eq("y2", round(r[2][3], 10), 129.8, 1e-9)
eq("x2 を整数に", int(round(r[2][2])), 566)
eq("y2 を整数に", int(round(r[2][3])), 130)

# 平衡点を sympy で
xs, ys = sp.symbols("x y", positive=True)
sol = sp.solve([sp.Eq(0.4 * xs - 0.002 * xs * ys, 0),
                sp.Eq(-0.3 * ys + 0.001 * xs * ys, 0)], [xs, ys], dict=True)
pt = [(float(s[xs]), float(s[ys])) for s in sol if xs in s and ys in s]
eq("平衡点（sympy）", [(round(a, 6), round(b, 6)) for a, b in pt],
   [(300.0, 200.0)])
eq("平衡点で f1 = 0", round(P1(0, 300, 200), 10), 0.0, 1e-9)
eq("平衡点で f2 = 0", round(P2(0, 300, 200), 10), 0.0, 1e-9)
eq("x0 > 300 かつ y0 < 200 → 両方増える",
   (400 > 300) and (100 < 200) and P1(0, 400, 100) > 0 and P2(0, 400, 100) > 0,
   True)

in_text("例題3 f1", "0.4(400) - 0.002(400)(100) = 160 - 80 = 80")
in_text("例題3 f2", "-0.3(100) + 0.001(400)(100) = -30 + 40 = 10")
in_text("例題3 2歩目 f1", "0.4(480) - 0.002(480)(110) = 192 - 105.6 = 86.4")
in_text("例題3 2歩目 f2", "-0.3(110) + 0.001(480)(110) = -33 + 52.8 = 19.8")
in_text("例題3 答え", "x_2 = 480 + 86.4 = 566.4, \\qquad y_2 = 110 + 19.8 = 129.8")
in_text("平衡点 (300,200)", "**平衡点は $(300,\\ 200)$ です。**")

print()
print("=" * 78)
print("3.  周期・ピークの順・回る向き（細かい h で独立に判定）")
print("=" * 78)
h = 0.005
t, x, y = 0.0, 400.0, 100.0
T, X, Y = [t], [x], [y]
for _ in range(8000):
    a, b = P1(t, x, y), P2(t, x, y)
    x, y, t = x + h * a, y + h * b, t + h
    T.append(t)
    X.append(x)
    Y.append(y)
T, X, Y = np.array(T), np.array(X), np.array(Y)

sel = (T >= 10) & (T <= 32)
tt, xx, yy = T[sel], X[sel], Y[sel]
tpx, tpy = tt[int(np.argmax(xx))], tt[int(np.argmax(yy))]
print("     prey のピーク t=%.2f、predator のピーク t=%.2f" % (tpx, tpy))
eq("prey のピークが先", tpx < tpy, True)
eq("prey のピークは t≈22", round(tpx), 22)
eq("predator のピークは t≈25〜26", 25 <= tpy <= 26, True)

pk = [i for i in range(1, len(X) - 1) if X[i] > X[i - 1] and X[i] >= X[i + 1]]
per = T[pk[1]] - T[pk[0]]
print("     prey のピーク時刻:", [round(T[i], 2) for i in pk[:3]])
eq("周期はおよそ 19", round(per), 19)

# 右端（x 最大）で y は増えているか → 反時計回り
i = int(np.argmax(X[:5000]))
eq("x が最大の点で y は増加（反時計回り）", Y[i + 1] > Y[i], True)
eq("x が最大の点で y ≈ 200（平衡と同じ高さ）", round(Y[i], -1), 200.0, 1e-9)
in_text("周期およそ19", "**周期はおよそ $19$ 年**です。")
in_text("反時計回り", "**反時計回り**です。")
in_text("右端で上向き", "\\text{右端で上向き} \\ \\Longrightarrow \\ \\text{反時計回り}")

print()
print("=" * 78)
print("4.  演習の数値")
print("=" * 78)
# 演習1・2
r = ceuler(lambda t, x, y: 2 * x - y, lambda t, x, y: x + 3 * y,
           0, 1.0, 0.0, 0.1, 2)
eq("演習1 f1", r[0][4], 2.0, 1e-12)
eq("演習1 f2", r[0][5], 1.0, 1e-12)
eq("演習1 x1", round(r[1][2], 10), 1.2, 1e-9)
eq("演習1 y1", round(r[1][3], 10), 0.1, 1e-9)
eq("演習2 f1", round(r[1][4], 10), 2.3, 1e-9)
eq("演習2 f2", round(r[1][5], 10), 1.5, 1e-9)
eq("演習2 x2", round(r[2][2], 10), 1.43, 1e-9)
eq("演習2 y2", round(r[2][3], 10), 0.25, 1e-9)
# 演習3 の誤ったやり方
eq("演習3 誤った y1", round(0 + 0.1 * (1.2 + 3 * 0), 10), 0.12, 1e-9)
in_text("演習1 解答", "x_1 = 1 + 0.1(2) = 1.2, \\qquad y_1 = 0 + 0.1(1) = 0.1")
in_text("演習2 解答", "x_2 = 1.2 + 0.23 = 1.43, \\qquad y_2 = 0.1 + 0.15 = 0.25")
in_text("演習3 正解", "f_2 = 1 + 3(0) = 1, \\qquad y_1 = 0 + 0.1(1) = 0.1")

# 演習4・5
def Q1(t, x, y):
    return 0.5 * x - 0.004 * x * y


def Q2(t, x, y):
    return -0.2 * y + 0.002 * x * y


r = ceuler(Q1, Q2, 0, 200.0, 50.0, 1.0, 2)
eq("演習4 f1(0)", round(r[0][4], 10), 60.0, 1e-9)
eq("演習4 f2(0)", round(r[0][5], 10), 10.0, 1e-9)
eq("演習4 x1", round(r[1][2], 10), 260.0, 1e-9)
eq("演習4 y1", round(r[1][3], 10), 60.0, 1e-9)
eq("演習4 f1(1)", round(r[1][4], 10), 67.6, 1e-9)
eq("演習4 f2(1)", round(r[1][5], 10), 19.2, 1e-9)
eq("演習4 x2", round(r[2][2], 10), 327.6, 1e-9)
eq("演習4 y2", round(r[2][3], 10), 79.2, 1e-9)
eq("演習4 整数", (int(round(r[2][2])), int(round(r[2][3]))), (328, 79))
eq("演習5 平衡 y", 0.5 / 0.004, 125.0, 1e-9)
eq("演習5 平衡 x", 0.2 / 0.002, 100.0, 1e-9)
eq("演習5 検算 f1", round(Q1(0, 100, 125), 10), 0.0, 1e-9)
eq("演習5 検算 f2", round(Q2(0, 100, 125), 10), 0.0, 1e-9)
in_text("演習4 f1", "0.5(200) - 0.004(200)(50) = 100 - 40 = 60")
in_text("演習4 2歩目", "0.5(260) - 0.004(260)(60) = 130 - 62.4 = 67.6")
in_text("演習5 平衡点", "*The equilibrium point is* $(100,\\ 125)$.")
in_text("演習5 検算1", "0.5(100) - 0.004(100)(125) = 50 - 50 = 0")
in_text("演習5 検算2", "-0.2(125) + 0.002(100)(125) = -25 + 25 = 0")

# 演習8（タンク）
r = ceuler(lambda t, a, b: -0.2 * a + 0.1 * b,
           lambda t, a, b: 0.2 * a - 0.3 * b, 0, 100.0, 0.0, 1.0, 2)
eq("演習8 f1(0)", round(r[0][4], 10), -20.0, 1e-9)
eq("演習8 f2(0)", round(r[0][5], 10), 20.0, 1e-9)
eq("演習8 a1", round(r[1][2], 10), 80.0, 1e-9)
eq("演習8 b1", round(r[1][3], 10), 20.0, 1e-9)
eq("演習8 f1(1)", round(r[1][4], 10), -14.0, 1e-9)
eq("演習8 f2(1)", round(r[1][5], 10), 10.0, 1e-9)
eq("演習8 a2", round(r[2][2], 10), 66.0, 1e-9)
eq("演習8 b2", round(r[2][3], 10), 30.0, 1e-9)
eq("演習8 合計 1 分後は 100", round(80 + 20, 10), 100.0, 1e-9)
eq("演習8 合計 2 分後は 96（保存されない）", round(66 + 30, 10), 96.0, 1e-9)
in_text("演習8 f1(1)", "-0.2(80) + 0.1(20) = -16 + 2 = -14")
in_text("演習8 合計", "$66 + 30 = 96$ で、**減っています。**")

# 演習10（感染）
r = ceuler(lambda t, x, y: 0.3 * x - 0.1 * x, lambda t, x, y: 0.1 * x,
           0, 20.0, 0.0, 1.0, 3)
eq("演習10 x の並び", [round(v[2], 6) for v in r], [20.0, 24.0, 28.8, 34.56])
eq("演習10 y の並び", [round(v[3], 6) for v in r], [0.0, 2.0, 4.4, 7.28])
eq("演習10 f1 の並び", [round(v[4], 6) for v in r][:3], [4.0, 4.8, 5.76])
eq("演習10 f2 の並び", [round(v[5], 6) for v in r][:3], [2.0, 2.4, 2.88])
eq("演習10 毎回 1.2 倍", round(20 * 1.2 ** 3, 6), 34.56, 1e-6)
n500 = min(n for n in range(1, 200) if 20 * 1.2 ** n > 500)
eq("演習10 500 を超えるのは n=18", n500, 18)
in_text("演習10 1.2倍", "20 \\times 1.2^3 = 34.56")
in_text("演習10 18日", "$n \\geq 18$ のときです")

print()
print("=" * 78)
print("5.  構成・表記の検査")
print("=" * 78)
nos = re.findall(r"\[(\d+)\]\{\.ex-no\}", TXT)
eq("演習の番号", nos, [str(i) for i in range(1, 11)])
eq("ex-sep は 9 個", TXT.count("::: {.ex-sep}"), 9)
eq("exercise-block は 1 個", TXT.count("::: {.exercise-block}"), 1)

for fid in ("system", "cycle"):
    in_text("図 %s の定義" % fid, "{#fig-ahl516b-%s" % fid)
    eq("図 %s が参照されている" % fid, TXT.count("@fig-ahl516b-%s" % fid) >= 1,
       True)
    p = os.path.join(os.path.dirname(QMD), "img", "ahl-5-16b-%s.svg" % fid)
    eq("SVG %s が存在する" % fid, os.path.exists(p), True)

for e in ("basic", "error", "predator", "read"):
    in_text("例題 %s" % e, "{#exm-ahl516b-%s}" % e)

for a in ("idea", "formula", "old", "predator", "interpret", "equilibrium",
          "phase", "tech", "why", "why-old", "why-spiral", "gdc-sheet",
          "gdc-plot", "gdc-check"):
    in_text("アンカー #%s" % a, "{#%s}" % a)

anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TXT)) | {"common-errors"}
targets = set(re.findall(r"\]\(#([a-z0-9-]+)\)", TXT))
eq("章内リンクの飛び先がすべて存在する", sorted(targets - anchors), [])

defined = set(re.findall(r"\{#((?:fig|tbl|exm|eq)-[a-z0-9-]+)", TXT))
used = set(re.findall(r"@((?:fig|tbl|exm|eq)-[a-z0-9-]+)", TXT))
eq("crossref の飛び先がすべて存在する", sorted(used - defined), [])
eq("表のキャプション数", len(re.findall(r"^: .*\{#tbl-", TXT, re.M)),
   len(re.findall(r"\{#tbl-ahl516b-", TXT)))

for w in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん", "当たり前"]:
    not_in_text("禁止語 %s" % w, w)
bad_k = [TXT[m.start():m.start() + 6]
         for m in re.finditer(r"確かめ(?![方らてるればよな])", TXT)]
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

# 公式集・シラバス
in_text("公式集の x の式", "x_{n+1} &= x_n + h \\times f_1(x_n,\\ y_n,\\ t_n)")
in_text("公式集の y の式", "y_{n+1} &= y_n + h \\times f_2(x_n,\\ y_n,\\ t_n)")
in_text("公式集の t の式", "t_{n+1} &= t_n + h")
in_text("公式集に載っている旨", "## 公式集に載っています（5.16 の欄、$2$ つ目）")
in_text("シラバス Content",
        "Numerical solution of the coupled system")
in_text("シラバス Guidance", "Contexts could include predator-prey models.")
in_text("Runge-Kutta は試験に出ない", "**試験には出ません。**")

# レビュー修正の固定（回帰防止）
eq("演習8 d(a+b)/dt = -0.2b（係数）",
   [round(-0.2 + 0.2, 12), round(0.1 - 0.3, 12)], [0.0, -0.2])
eq("演習8 b=20 のとき系外へ 4", round(0.2 * 20, 10), 4.0, 1e-9)
eq("演習10 式そのものが 500 を超える t",
   round(float(np.log(25) / 0.2), 1), 16.1, 1e-9)
eq("演習10 Euler(18歩) > 500", 20 * 1.2 ** 18 > 500, True)
eq("演習10 Euler は式より小さめ", 20 * 1.2 ** 16 < 20 * np.exp(0.2 * 16), True)

in_text("タイトルの訳", "（連立系のオイラー法）")
in_text("prey/predator を English first で",
        "$x$ を **prey**（被食者、餌になる動物）、$y$ を **predator**（捕食者）とします。")
in_text("glossary に合わせた訳", "**predator–prey model**（捕食者・被食者モデル）")
in_text("equilibrium point は 5.17 の語だと断っている",
        "シラバルでは" if False else "シラバスでは **AHL 5.17**")
in_text("入れ替わりは predator–prey に限定", "**この predator–prey の形では**")
in_text("ほかの形では違うと書いている", "演習8 では $\\dfrac{da}{dt} = 0$ から $b = 2a$")
in_text("列は 3 つ", "列は $3$ つ（$t$、$x$、$y$）で足ります。")
in_text("周期は system(b) で測る", "@fig-ahl516b-system の (b) には山が $2$ つ見えています。")
in_text("cycle の左では測れないと断っている", "周期はこちらでは測れません。")
in_text("演習8 の正しい検算", "\\frac{d}{dt}(a + b) = (-0.2a + 0.1b) + (0.2a - 0.3b) = -0.2b")
in_text("演習8 の 0.2b", "**残りの $0.2b$ が系の外へ出ていきます。**")
in_text("演習10 の 16.1 日", "$t = 16.1$ 日です")
not_in_text("誤った 0.3-0.2 の説明が無い", "$0.3 - 0.2 = 0.1$ のぶん")
in_text("Fill の但し書き", "**列ごとに $1$ つずつ** `Fill` してください")

# 存在しないページへのリンクが無い
for dead in ["ahl-5-10.qmd", "ahl-5-11.qmd", "ahl-5-17.qmd", "ahl-5-18.qmd"]:
    not_in_text("存在しないページ %s へのリンクが無い" % dead, "](%s" % dead)

print()
print("=" * 78)
print("結果:  OK %d / NG %d" % (OK, NG))
print("=" * 78)
raise SystemExit(1 if NG else 0)
