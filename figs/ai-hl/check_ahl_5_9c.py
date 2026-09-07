# -*- coding: utf-8 -*-
"""AHL 5.9c（related rates of change）の検算。
   1. すべての rate を第一原理から出す（公式を微分して chain rule に入れる）
   2. 微小変化の差分で、独立に突き合わせる（本文の検算と同じやり方）
   3. .qmd の本文が、その数値どおりに書かれているかを確かめる
   4. 公式集のどの欄にあるかを見張る（Prior learning と 3.1 は別）
   5. レビューで直した点を not_in_text で見張る
   6. 構造の不変条件を確かめる
   実行: python3 figs/ai-hl/check_ahl_5_9c.py
"""
import io
import os
import re
import sys

import sympy as sp

QMD = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "05-calculus", "ahl-5-9c.qmd")
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


def sf3(v):
    """有効数字 3 桁に丸めた文字列。"""
    return "%s" % sp.N(v, 3)


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


r, h, xx, w = sp.symbols("r h x w", positive=True)


def rate(expr, var, at, given, unknown="out"):
    """chain rule。given が d(expr)/dt なら d(var)/dt を、
       given が d(var)/dt なら d(expr)/dt を返す。"""
    dedv = sp.diff(expr, var).subs(var, at)
    return (given / dedv) if unknown == "in" else (dedv * given)


# ══════════════════════════════════════════════════════════════
# 1. 例題 1  円  A = pi r^2、dr/dt = 0.2、r = 10
# ══════════════════════════════════════════════════════════════
A_circ = sp.pi * r ** 2
eq("dA/dr at 10", sp.diff(A_circ, r).subs(r, 10), 20 * sp.pi)
dAdt = rate(A_circ, r, 10, sp.Rational(1, 5))
eq("dA/dt = 4pi", sp.simplify(dAdt), 4 * sp.pi)
close("dA/dt", sp.N(dAdt, 12), 12.5663706144)
# 独立確認: 実際の面積差
diff_area = sp.pi * (sp.Rational(1004, 100) ** 2 - 100)
close("0.2 秒での面積差", sp.N(diff_area, 12), 2.51826, 1e-4)
close("1 秒あたりに直すと", sp.N(diff_area / sp.Rational(1, 5), 12), 12.5913, 1e-3)
in_text(r"$\pi(10.04^{2} - 10^{2}) = 2.52$ m$^{2}$")
not_in_text("$2\\pi(10)(0.04) = 2.51$")

# ══════════════════════════════════════════════════════════════
# 2. 例題 2  球  V = 4/3 pi r^3、dV/dt = 30
# ══════════════════════════════════════════════════════════════
V_sph = sp.Rational(4, 3) * sp.pi * r ** 3
eq("dV/dr at 5", sp.diff(V_sph, r).subs(r, 5), 100 * sp.pi)
eq("dV/dr at 10", sp.diff(V_sph, r).subs(r, 10), 400 * sp.pi)
d5 = rate(V_sph, r, 5, 30, "in")
d10 = rate(V_sph, r, 10, 30, "in")
close("dr/dt at 5", sp.N(d5, 12), 0.0954929658551)
close("dr/dt at 10", sp.N(d10, 12), 0.0238732414638)
eq("ちょうど 4 倍", sp.simplify(d5 / d10), 4)
close("0.0955/0.0239", 0.0955 / 0.0239, 4.0, 5e-3)
# 丸め警告
close("30/314", 30 / 314, 0.0955414, 1e-6)
eq("314 で割っても 3 桁は同じ", sf3(30 / sp.Integer(314)), sf3(sp.N(d5, 12)))
in_text("**$4$ 桁目からはもうずれています。**")
not_in_text("$0.09554$ になります。$3$ 桁目がずれます。")
# Why it works の掛け算
close("100pi * 0.0955", float(100 * sp.pi * sp.Rational(955, 10000)), 30.0, 3e-3)

# ══════════════════════════════════════════════════════════════
# 3. 例題 3  円錐  r = h/2
# ══════════════════════════════════════════════════════════════
V_cone = sp.Rational(1, 3) * sp.pi * (h / 2) ** 2 * h
eq("V = pi h^3/12", sp.simplify(V_cone), sp.pi * h ** 3 / 12)
eq("dV/dh", sp.simplify(sp.diff(V_cone, h)), sp.pi * h ** 2 / 4)
eq("dV/dh at 6", sp.diff(V_cone, h).subs(h, 6), 9 * sp.pi)
dh = rate(V_cone, h, 6, 20, "in")
close("dh/dt at 6", sp.N(dh, 12), 0.707355302596)
close("9pi", float(9 * sp.pi), 28.2743, 1e-4)
# dV/dh は水面の面積そのもの
eq("dV/dh = 水面の面積", sp.simplify(sp.diff(V_cone, h) - sp.pi * (h / 2) ** 2), 0)
close("h=6 のときの水面の面積", float(sp.pi * 9), 28.2743, 1e-4)
close("20/28.3", 20 / 28.3, 0.7067, 1e-3)
in_text("**これは偶然ではありません。**")
in_text("水面の形をした**薄い板**が $1$ 枚乗ります")

# ══════════════════════════════════════════════════════════════
# 4. 例題 4  立方体
# ══════════════════════════════════════════════════════════════
eq("dV/dx at 5", sp.diff(xx ** 3, xx).subs(xx, 5), 75)
close("dV/dt", float(rate(xx ** 3, xx, 5, sp.Rational(1, 10))), 7.5)
eq("dS/dx at 5", sp.diff(6 * xx ** 2, xx).subs(xx, 5), 60)
close("dS/dt", float(rate(6 * xx ** 2, xx, 5, sp.Rational(1, 10))), 6.0)
# 検算（差分）
close("5.01^3 - 5^3", 5.01 ** 3 - 125, 0.751501, 1e-6)
close("×10", (5.01 ** 3 - 125) * 10, 7.515, 1e-3)
close("6(5.01^2) - 150", 6 * 5.01 ** 2 - 150, 0.6006, 1e-6)
close("×10", (6 * 5.01 ** 2 - 150) * 10, 6.006, 1e-3)

# ══════════════════════════════════════════════════════════════
# 5. 演習 1〜10
# ══════════════════════════════════════════════════════════════
close("E1 dA/dt", float(rate(xx ** 2, xx, 8, sp.Rational(3, 10))), 4.8)
e2 = rate(4 * sp.pi * r ** 2, r, 4, sp.Rational(1, 20))
eq("E2 = 1.6pi", sp.simplify(e2), sp.Rational(8, 5) * sp.pi)
close("E2 dS/dt", sp.N(e2, 12), 5.02654824574)
e3 = rate(9 * sp.pi * h, h, 1, 15, "in")
close("E3 dh/dt", sp.N(e3, 12), 0.530516476973)
e4 = rate(A_circ, r, 4, 8, "in")
eq("E4 = 1/pi", sp.simplify(e4), 1 / sp.pi)
close("E4 dr/dt", sp.N(e4, 12), 0.318309886184)
close("E4 検算 8pi*0.3183", float(8 * sp.pi * sp.Rational(3183, 10000)), 8.0, 1e-3)
e5 = rate(xx ** 3, xx, 2, 12, "in")
eq("E5 dx/dt", sp.simplify(e5), 1)
CST = 500 + 20 * xx + sp.Rational(1, 10) * xx ** 2
eq("E6 dC/dx at 100", sp.diff(CST, xx).subs(xx, 100), 40)
eq("E6 dC/dt", sp.simplify(rate(CST, xx, 100, 5)), 200)
e7 = rate(V_sph, r, 10, 50, "in")
close("E7 dr/dt", sp.N(e7, 12), 0.0397887357729)
close("E7 検算 0.0239*50/30", 0.0238732414638 * 50 / 30, 0.0397887, 1e-6)
close("E7 50/1257", 50 / 1257, 0.0397772, 1e-6)
eq("E7 1257 でも 3 桁は同じ", sf3(50 / sp.Integer(1257)), sf3(sp.N(e7, 12)))
# E9 の誤答
close("E9 誤答 20pi", float(20 * sp.pi), 62.8319, 1e-3)
close("E9 正答", sp.N(dAdt, 12), 12.5663706144)
# E10 長方形
eq("E10 A = 2w^2", sp.simplify(w * (2 * w)), 2 * w ** 2)
eq("E10 dA/dw at 3", sp.diff(2 * w ** 2, w).subs(w, 3), 12)
close("E10 dA/dt", float(rate(2 * w ** 2, w, 3, sp.Rational(1, 2))), 6.0)
close("E10 検算 2(3.05)^2-18", 2 * 3.05 ** 2 - 18, 0.605, 1e-9)
close("E10 ×10", (2 * 3.05 ** 2 - 18) * 10, 6.05, 1e-8)

# ══════════════════════════════════════════════════════════════
# 6. 公式集のどの欄にあるか（Prior learning と 3.1 は別）
# ══════════════════════════════════════════════════════════════
in_text("円の面積 $A = \\pi r^{2}$、円柱の体積 $V = \\pi r^{2}h$ は "
        "**Prior learning** の欄に")
in_text("**3.1** の欄にあります")
in_text("**(a)** 円の面積の公式です（公式集の Prior learning の欄）。")
not_in_text("**(a)** 円の面積の公式です（公式集の $3.1$ の欄）。")
# 載っていないものは自分で作る
in_text("正方形の面積 $A = x^{2}$ や、立方体の表面積 $A = 6x^{2}$ は印刷されていません。")
not_in_text("**ですから、この項目で覚えるものはありません。**")
in_text("**これは公式集にありません。**")
# 公式集 5.9 の chain rule をそのまま
in_text(r"y = g(u), \ \text{where} \ u = f(x) \ \Rightarrow \ "
        r"\frac{dy}{dx} = \frac{dy}{du} \times \frac{du}{dx}")
in_text("## 公式集に「related rates」という欄はありません")

# ══════════════════════════════════════════════════════════════
# 7. レビューで直した点の見張り
# ══════════════════════════════════════════════════════════════
# 1: dA/dr の単位は m（m^2 ではない）
in_text("単位も m$^{2}$ ÷ m $=$ m で、答えの m$^{2}$ s$^{-1}$ になっていません。")
not_in_text("単位も m$^{2}$ で、m$^{2}$ s$^{-1}$ になっていません。")
# 4: 丸めの警告
in_text("$4$ 桁目からずれます")
not_in_text("$3$ 桁目がぎりぎりです")
# 7: 「微分してから代入」は変わる文字についての話
in_text("これは**変わる文字**についての話です。")
in_text("「微分してから代入」の順を守るのは**変わる文字**についてで")
# 8: pi キーの言い方
in_text("キーボードの **$\\pi$ のキー**を使ってください。")
not_in_text("`ctrl` + キーボードの記号パレット")
# 11: 表示桁
in_text("返るのは $314.159$")
not_in_text("返るのは $314.16$")
# 12: 表を参照する / ドルの行
in_text("残りの $1$ つが出ます**（@tbl-ahl59c-two）")
in_text("| $\\dfrac{dC}{dt}$ | ドル／日 | $1$ 日あたり何ドル |")
in_text("\\approx \\ 30 \\ \\text{cm}^{3}")

# ══════════════════════════════════════════════════════════════
# 8. 構造の不変条件
# ══════════════════════════════════════════════════════════════
h2 = re.findall(r"^## (.+)$", TXT, re.M)
top = [x for x in h2 if x in ("What you should be able to do", "The idea",
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
# 記述問題には model-answer
eq("model-answer は 3 つ", TXT.count("::: {.model-answer}"), 3)
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
