# -*- coding: utf-8 -*-
"""AHL 5.10（second derivative）の検算。
   1. すべての値を第一原理から出す（sympy で 2 回微分する）
   2. mpmath の数値微分で、独立に突き合わせる
   3. .qmd の本文が、その数値どおりに書かれているかを確かめる
   4. シラバスと公式集から確かめた事実を見張る
   5. レビューで直した点を not_in_text で見張る
   6. 構造の不変条件を確かめる
   実行: python3 figs/ai-hl/check_ahl_5_10.py
"""
import io
import os
import re
import sys

import sympy as sp
import mpmath as mp

QMD = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "05-calculus", "ahl-5-10.qmd")
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


x, t = sp.symbols("x t", real=True)


def d1(f, v=x):
    return sp.expand(sp.diff(f, v))


def d2(f, v=x):
    return sp.expand(sp.diff(f, v, 2))


def classify(f, a, v=x):
    """f''(a) の符号から 'max'/'min'/'test fails' を返す。"""
    s = sp.simplify(sp.diff(f, v, 2).subs(v, a))
    return "max" if s < 0 else ("min" if s > 0 else "test fails")


def sign_change(f, a, delta=1, v=x):
    """a の前後での f' の符号。"""
    lo = sp.sign(sp.diff(f, v).subs(v, a - delta))
    hi = sp.sign(sp.diff(f, v).subs(v, a + delta))
    return (int(lo), int(hi))


# ══════════════════════════════════════════════════════════════
# 1. 走らせる例  f = x^3 - 3x^2 - 9x + 5
# ══════════════════════════════════════════════════════════════
F = x ** 3 - 3 * x ** 2 - 9 * x + 5
eq("f'", d1(F), sp.expand(3 * x ** 2 - 6 * x - 9))
eq("f''", d2(F), sp.expand(6 * x - 6))
eq("f' の因数分解", sp.factor(d1(F)), sp.factor(3 * (x - 3) * (x + 1)))
eq("stationary points", sorted(sp.solve(d1(F), x)), [-1, 3])
eq("f(-1)", F.subs(x, -1), 10)
eq("f(3)", F.subs(x, 3), -22)
eq("f''(-1)", d2(F).subs(x, -1), -12)
eq("f''(3)", d2(F).subs(x, 3), 12)
eq("x=-1 は max", classify(F, -1), "max")
eq("x=3 は min", classify(F, 3), "min")
eq("f'' = 0 は x=1", sp.solve(d2(F), x), [1])
eq("f(1)", F.subs(x, 1), -6)
eq("f'(1) は f' の最小値", sp.simplify(d1(F).subs(x, 1)), -12)
eq("f' の最小値も -12", sp.minimum(d1(F), x), -12)
eq("f'(0)", d1(F).subs(x, 0), -9)
eq("f'(-2)", d1(F).subs(x, -2), 15)
eq("x=-1 の前後で + -> -", sign_change(F, -1), (1, -1))
# concave-up は x > 1
eq("concave-up の区間", sp.solve(d2(F) > 0, x), sp.StrictLessThan(1, x))
# 数値微分で独立に確かめる
fn = sp.lambdify(x, F, "mpmath")
close("数値 2 階微分 at -1", float(mp.diff(fn, -1.0, 2)), -12.0, 1e-5)
close("数値 2 階微分 at 3", float(mp.diff(fn, 3.0, 2)), 12.0, 1e-5)

# ══════════════════════════════════════════════════════════════
# 2. 例題 2  T = 20 + 60 e^{-0.2t}
# ══════════════════════════════════════════════════════════════
T = 20 + 60 * sp.exp(-sp.Rational(1, 5) * t)
eq("T'", sp.simplify(d1(T, t)), sp.simplify(-12 * sp.exp(-t / 5)))
eq("T''", sp.simplify(d2(T, t)), sp.simplify(sp.Rational(12, 5) * sp.exp(-t / 5)))
close("T'(5)", sp.N(d1(T, t).subs(t, 5), 12), -4.41455327557)
close("T''(5)", sp.N(d2(T, t).subs(t, 5), 12), 0.882910655113)
close("e^-1", float(sp.exp(-1)), 0.3679, 1e-4)
close("T(5)", float(T.subs(t, 5)), 42.0728, 1e-3)
close("T(6)", float(T.subs(t, 6)), 38.0717, 1e-3)
close("T(10)", float(T.subs(t, 10)), 28.1201, 1e-3)
close("T(11)", float(T.subs(t, 11)), 26.6482, 1e-3)
close("5->6 の下がり幅", float(T.subs(t, 5) - T.subs(t, 6)), 4.0, 5e-2)
close("10->11 の下がり幅", float(T.subs(t, 10) - T.subs(t, 11)), 1.5, 5e-2)
eq("T'' はつねに正", sp.simplify(d2(T, t) > 0), True)

# ══════════════════════════════════════════════════════════════
# 3. 例題 3  f = x^4 - 4x^3（test が効かない例）
# ══════════════════════════════════════════════════════════════
G = x ** 4 - 4 * x ** 3
eq("g'", sp.factor(d1(G)), sp.factor(4 * x ** 2 * (x - 3)))
eq("g''", d2(G), sp.expand(12 * x ** 2 - 24 * x))
eq("stationary", sorted(sp.solve(d1(G), x)), [0, 3])
eq("g''(3)", d2(G).subs(x, 3), 36)
eq("x=3 は min", classify(G, 3), "min")
eq("g(3)", G.subs(x, 3), -27)
eq("g''(0) = 0 で決まらない", classify(G, 0), "test fails")
eq("g'(-1)", d1(G).subs(x, -1), -16)
eq("g'(1)", d1(G).subs(x, 1), -8)
eq("x=0 の前後で符号は変わらない", sign_change(G, 0), (-1, -1))

# ══════════════════════════════════════════════════════════════
# 4. tbl-ahl510-fails の 2 つ
# ══════════════════════════════════════════════════════════════
eq("x^4: f'", d1(x ** 4), sp.expand(4 * x ** 3))
eq("x^4: f''", d2(x ** 4), sp.expand(12 * x ** 2))
eq("x^4: f''(0) = 0", d2(x ** 4).subs(x, 0), 0)
eq("x^4 は x=0 で minimum", sign_change(x ** 4, 0), (-1, 1))
eq("x^3: f''", d2(x ** 3), sp.expand(6 * x))
eq("x^3: f''(0) = 0", d2(x ** 3).subs(x, 0), 0)
eq("x^3 は符号が変わらない", sign_change(x ** 3, 0), (1, 1))
eq("x^4 と x^3 で結論が違う",
   (sign_change(x ** 4, 0) == (-1, 1), sign_change(x ** 3, 0) == (1, 1)),
   (True, True))

# ══════════════════════════════════════════════════════════════
# 5. 例題 4  s = t^3 - 6t^2 + 9t
# ══════════════════════════════════════════════════════════════
S = t ** 3 - 6 * t ** 2 + 9 * t
eq("sdot", d1(S, t), sp.expand(3 * t ** 2 - 12 * t + 9))
eq("sddot", d2(S, t), sp.expand(6 * t - 12))
eq("v = 0", sorted(sp.solve(d1(S, t), t)), [1, 3])
eq("s(1)", S.subs(t, 1), 4)
eq("s(3)", S.subs(t, 3), 0)
eq("sddot(1)", d2(S, t).subs(t, 1), -6)
eq("sddot(3)", d2(S, t).subs(t, 3), 6)
# ★レビュー 2: s=4 は local max であって、いちばん遠い地点ではない
eq("s(4)", S.subs(t, 4), 4)
eq("s(5)", S.subs(t, 5), 20)
eq("t>3 では s が 4 を超える", bool(S.subs(t, 5) > S.subs(t, 1)), True)

# ══════════════════════════════════════════════════════════════
# 6. 演習 1〜10
# ══════════════════════════════════════════════════════════════
E1 = x ** 3 - 6 * x ** 2 + 5
eq("E1 y'", d1(E1), sp.expand(3 * x ** 2 - 12 * x))
eq("E1 y''", d2(E1), sp.expand(6 * x - 12))
E2 = 2 * x ** 3 + 3 * x ** 2 - 12 * x
eq("E2 f'", sp.factor(d1(E2)), sp.factor(6 * (x + 2) * (x - 1)))
eq("E2 stationary", sorted(sp.solve(d1(E2), x)), [-2, 1])
eq("E2 f(-2)", E2.subs(x, -2), 20)
eq("E2 f(1)", E2.subs(x, 1), -7)
eq("E2 f''", d2(E2), sp.expand(12 * x + 6))
eq("E2 f''(-2)", d2(E2).subs(x, -2), -18)
eq("E2 f''(1)", d2(E2).subs(x, 1), 18)
eq("E2 x=-2 は max", classify(E2, -2), "max")
eq("E2 x=1 は min", classify(E2, 1), "min")
eq("E2 f'(0)", d1(E2).subs(x, 0), -12)
E3 = sp.exp(x) - 3 * x
eq("E3 stationary", sp.solve(sp.diff(E3, x), x), [sp.log(3)])
close("E3 x", float(sp.log(3)), 1.0986, 1e-4)
close("E3 y", float(E3.subs(x, sp.log(3))), -0.29584, 1e-5)
eq("E3 f''(ln3)", sp.simplify(sp.diff(E3, x, 2).subs(x, sp.log(3))), 3)
eq("E3 は min", classify(E3, sp.log(3)), "min")
eq("E4 y''", d2(x ** 2 - 4 * x), 2)
eq("E5 f''", d2(x ** 3), sp.expand(6 * x))
eq("E5 concave-up は x>0", sp.solve(d2(x ** 3) > 0, x), sp.StrictLessThan(0, x))
xp = sp.symbols("xp", positive=True)
eq("E6 y'", sp.diff(sp.log(xp), xp), 1 / xp)
eq("E6 y''", sp.simplify(sp.diff(sp.log(xp), xp, 2)), -1 / xp ** 2)
eq("E6 は concave-down", sp.simplify(sp.diff(sp.log(xp), xp, 2) < 0), True)
eq("E8 f'(0)", d1(x ** 4).subs(x, 0), 0)
eq("E8 f''(0)", d2(x ** 4).subs(x, 0), 0)
eq("E8 f'(-1)", d1(x ** 4).subs(x, -1), -4)
eq("E8 f'(1)", d1(x ** 4).subs(x, 1), 4)
S9 = t ** 3 - 3 * t ** 2
eq("E9 sdot", d1(S9, t), sp.expand(3 * t ** 2 - 6 * t))
eq("E9 sddot", d2(S9, t), sp.expand(6 * t - 6))
eq("E9 a = 0", sp.solve(d2(S9, t), t), [1])
eq("E9 sdot の最小値", sp.minimum(d1(S9, t), t), -3)
eq("E9 平方完成", sp.expand(3 * (t - 1) ** 2 - 3), d1(S9, t))
# E10 の誤り: f''>0 は minimum
eq("f''>0 は minimum", classify(x ** 2, 0), "min")

# ══════════════════════════════════════════════════════════════
# 7. シラバス・公式集から確かめた事実
# ══════════════════════════════════════════════════════════════
in_text("公式集の Topic 5（HL）には、$5.3$、$5.9$、$5.5$、$5.8$、$5.11$、$5.12$、"
        "$5.13$、$5.16$、$5.17$ の欄がありますが、**$5.10$ の欄はありません。**")
in_text("> Both forms of notation, $\\dfrac{d^{2}y}{dx^{2}}$ and $f''(x)$ "
        "for the second derivative.")
in_text('> Use of the terms "concave-up" for $f\'\'(x) > 0$, and "concave-down" '
        'for $f\'\'(x) < 0$.')
in_text("> Awareness that a point of inflexion is a point at which the "
        "concavity changes and interpretation of this in context.")
in_text("> Link to: kinematics (AHL5.13) and second order differential "
        "equations (AHL5.18).")

# ══════════════════════════════════════════════════════════════
# 8. レビューで直した点の見張り
# ══════════════════════════════════════════════════════════════
# 1: test には f'(a)=0 の前提が要る
in_text("f'(a) = 0 \\ \\text{のとき} \\qquad f''(a) < 0")
in_text("**$f'(a) = 0$ が前提です。**")
not_in_text("f''(a) < 0 \\ \\Rightarrow \\ \\text{maximum} \\qquad\\qquad "
            "f''(a) > 0")
# 2: local max であって最遠点ではない
in_text("**$t = 1$ までは前へ進み、そこで折り返します（$s = 4$ m）。")
not_in_text("いちばん前まで進み")
in_text("$s(4) = 4$、$s(5) = 20$ です。")
# 4: 変曲点は「折り返し」であって、いつも最強ではない
in_text("| concave-down → concave-up | 増え方（勢い）が**いちばん弱かった**瞬間 |")
not_in_text("意味は「**増え方（または減り方）が、いちばん強かった瞬間**」です。")
# 5: Why it works の向き
in_text("いま $f'(a) = 0$ で、$f''(a) < 0$ だとします。")
not_in_text("ですから、その付近で $f'' < 0$ です。")
# 6: GDC のフォールバックが本物の検算
in_text("**自分の $f''(x)$ に代入するだけでは検算になりません。**")
not_in_text("確かめとしては同じことです。")
# 9: point of inflexion の前振り
in_text("（**point of inflexion**（変曲点）そのものについては、[第5節](#inflexion)で説明します。）")
# 10: 5.13 は後のページ
in_text("**この節は、[AHL 5.13](ahl-5-13.qmd) を読む前でも後でも構いません。**")
not_in_text("[AHL 5.13](ahl-5-13.qmd#dot) で出てきたものと同じです")
# 13: local の注意
in_text("**local maximum・local minimum**（極大・極小）です。")
# 14: classify は IB の command term ではない
not_in_text("classify")
in_text("determine the nature of")
# 15: 3 通りの書き方
in_text("- $f''(x)$、$\\dfrac{d^{2}y}{dx^{2}}$、$\\ddot{x}$ という書き方を読み、使い分けられる。")

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
eq("例題は 4 つ", len(re.findall(r"::: \{#exm-", TXT)), 4)
eq("演習は 10 問", len(re.findall(r"\[\d+\]\{\.ex-no\}", TXT)), 10)
eq("ex-sep は 9 個", TXT.count(".ex-sep"), 9)
eq("例題の下の区切り線は 4 本（+ YAML の 1 本）", TXT.count("\n---\n"), 5)
eq("model-answer は 7 つ", TXT.count("::: {.model-answer}"), 7)
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
    while j < len(line):
        c = line[j]
        if c == "\\":
            j += 2
            continue
        if c == "$":
            inm = not inm
        elif c == "|" and inm:
            NG += 1
            print("NG  表のセルの数式に | : %r" % line[:70])
            break
        j += 1
BASE = os.path.dirname(QMD)
for m in re.finditer(r"\]\((\.\./\.\./[^)#]+\.qmd|[a-z0-9-]+\.qmd)(#([a-z0-9-]+))?\)",
                     TXT):
    path, anch = m.group(1), m.group(3)
    full = os.path.normpath(os.path.join(BASE, path))
    if not os.path.exists(full):
        NG += 1
        print("NG  リンク先が無い: %s" % path)
        continue
    if anch and ("{#" + anch + "}") not in io.open(full, encoding="utf-8").read():
        NG += 1
        print("NG  アンカーが無い: %s#%s" % (path, anch))
    else:
        OK += 1
for m in re.finditer(r"\[@(exm|eq|fig|tbl)-", TXT):
    NG += 1
    print("NG  ページ間 crossref: %r" % m.group(0))
else:
    OK += 1
# 図が存在する
for svg in ("ahl-5-10-test.svg", "ahl-5-10-four.svg"):
    if os.path.exists(os.path.join(BASE, "img", svg)):
        OK += 1
    else:
        NG += 1
        print("NG  図が無い: %s" % svg)

print("=" * 78)
print("結果:  OK %d / NG %d" % (OK, NG))
print("=" * 78)
sys.exit(1 if NG else 0)
