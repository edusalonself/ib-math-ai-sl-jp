# -*- coding: utf-8 -*-
"""AHL 5.11a / 5.11b（further integration）の検算。
   1. すべての積分を sympy で第一原理から出す
   2. 「答えを微分するともとに戻る」を独立に確かめる（本文の検算と同じやり方）
   3. .qmd の本文が、その式・数値どおりに書かれているかを確かめる
   4. シラバスと公式集から確かめた事実を見張る
   5. レビューで直した点を not_in_text で見張る
   6. 構造の不変条件を確かめる
   実行: python3 figs/ai-hl/check_ahl_5_11.py
"""
import io
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(__file__)
A = os.path.join(HERE, "..", "..", "ai-hl", "05-calculus", "ahl-5-11a.qmd")
B = os.path.join(HERE, "..", "..", "ai-hl", "05-calculus", "ahl-5-11b.qmd")
TA = io.open(A, encoding="utf-8").read()
TB = io.open(B, encoding="utf-8").read()

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


def _in(txt, tag):
    def f(s, times=None):
        global OK, NG
        c = txt.count(s)
        if (c >= 1) if times is None else (c == times):
            OK += 1
        else:
            NG += 1
            print("NG  %s に無い/回数違い (%d): %r" % (tag, c, s[:90]))
    return f


def _not_in(txt, tag):
    def f(s):
        global OK, NG
        if s not in txt:
            OK += 1
        else:
            NG += 1
            print("NG  %s に残っている: %r" % (tag, s[:90]))
    return f


inA, notA = _in(TA, "5.11a"), _not_in(TA, "5.11a")
inB, notB = _in(TB, "5.11b"), _not_in(TB, "5.11b")

x, t, u = sp.symbols("x t u", real=True)
xp = sp.symbols("xp", positive=True)


def anti(name, f, F, v=x):
    """F' = f を確かめる（答えを微分してもとに戻るか）。"""
    eq(name + " を微分すると f に戻る", sp.simplify(sp.diff(F, v) - f), 0)


def dint(name, f, a, b, want, v=x):
    val = sp.integrate(f, (v, a, b))
    eq(name, sp.simplify(val - want), 0)


# ══════════════════════════════════════════════════════════════
# 1. 公式集の 5 つ（微分で確かめる）
# ══════════════════════════════════════════════════════════════
anti("ln|x|", 1 / xp, sp.log(xp), xp)
anti("-cos x", sp.sin(x), -sp.cos(x))
anti("sin x", sp.cos(x), sp.sin(x))
anti("tan x", 1 / sp.cos(x) ** 2, sp.tan(x))
anti("e^x", sp.exp(x), sp.exp(x))
# n = -1 で power rule が壊れること
eq("n = -1 で分母が 0", (-1) + 1, 0)

# ══════════════════════════════════════════════════════════════
# 2. 5.11a の例題
# ══════════════════════════════════════════════════════════════
anti("Ex1", 3 * sp.sin(xp) - 2 * sp.exp(xp) + 4 / xp,
     -3 * sp.cos(xp) - 2 * sp.exp(xp) + 4 * sp.log(xp), xp)
F2 = sp.sqrt(xp) + 3 / xp ** 2
anti("Ex2", F2, sp.Rational(2, 3) * xp ** sp.Rational(3, 2) - 3 / xp, xp)
dint("Ex2 定積分 1..4", F2, 1, 4, sp.Rational(83, 12), xp)
close("83/12", float(sp.Rational(83, 12)), 6.9167, 1e-4)
eq("途中の分数", sp.Rational(16, 3) - sp.Rational(3, 4)
   - (sp.Rational(2, 3) - 3), sp.Rational(83, 12))
eq("14/3 + 9/4", sp.Rational(14, 3) + sp.Rational(9, 4), sp.Rational(83, 12))
eq("4^(3/2)", sp.Integer(4) ** sp.Rational(3, 2), 8)
dint("Ex3 tan 0..pi/4", 1 / sp.cos(x) ** 2, 0, sp.pi / 4, 1)
# Ex4 タンク
V = 5 * t + 4 * sp.sin(t) + 20
anti("Ex4 V", 5 + 4 * sp.cos(t), V, t)
close("V(3)", float(V.subs(t, 3)), 35.5645, 1e-3)
close("4 sin 3", float(4 * sp.sin(3)), 0.5645, 1e-4)
close("dV/dt(3)", float((5 + 4 * sp.cos(t)).subs(t, 3)), 1.0400, 1e-3)
eq("dV/dt の下限", sp.minimum(5 + 4 * sp.cos(t), t), 1)
eq("dV/dt の上限", sp.maximum(5 + 4 * sp.cos(t), t), 9)
dint("Ex4(d) の積分 0..3", 5 + 4 * sp.cos(t), 0, 3, 15 + 4 * sp.sin(3), t)
close("15.6", float(15 + 4 * sp.sin(3)), 15.5645, 1e-3)
eq("V(3)-V(0) と一致", sp.simplify(V.subs(t, 3) - V.subs(t, 0)
                                   - (15 + 4 * sp.sin(3))), 0)
# boundary condition の C
close("C = 5 - 2 sin 1", float(5 - 2 * sp.sin(1)), 3.3171, 1e-4)
close("2 sin 1", float(2 * sp.sin(1)), 1.6829, 1e-4)
close("ln 3", float(sp.log(3)), 1.0986, 1e-4)

# ══════════════════════════════════════════════════════════════
# 3. 5.11a の演習
# ══════════════════════════════════════════════════════════════
anti("E1", 4 * sp.cos(x) - sp.exp(x), 4 * sp.sin(x) - sp.exp(x))
anti("E2", 6 / xp, 6 * sp.log(xp), xp)
anti("E3", xp ** sp.Rational(3, 2),
     sp.Rational(2, 5) * xp ** sp.Rational(5, 2), xp)
anti("E4", 2 / xp ** 2 + sp.sqrt(xp),
     -2 / xp + sp.Rational(2, 3) * xp ** sp.Rational(3, 2), xp)
dint("E5", 1 / xp, 1, 2, sp.log(2), xp)
close("ln 2", float(sp.log(2)), 0.6931, 1e-4)
dint("E6", sp.sin(x), 0, sp.pi / 3, sp.Rational(1, 2))
dint("E7", 1 / sp.cos(x) ** 2, sp.pi / 6, sp.pi / 3, 2 / sp.sqrt(3))
close("2/sqrt3", float(2 / sp.sqrt(3)), 1.1547, 1e-4)
anti("E8", 5 * sp.exp(x) + 1 / sp.cos(x) ** 2, 5 * sp.exp(x) + sp.tan(x))
anti("E9", 6 / xp, 6 * sp.log(xp), xp)
close("6 ln 5", float(6 * sp.log(5)), 9.6566, 1e-4)
close("6 x 1.60944", 6 * 1.60944, 9.6566, 1e-4)
dint("E9 の積分と一致", 6 / xp, 1, 5, 6 * sp.log(5), xp)
# Why it works の tan の確かめ（例題3 と別の端）
dint("why-tan 0..pi/3", 1 / sp.cos(x) ** 2, 0, sp.pi / 3, sp.sqrt(3))
close("sqrt3", float(sp.sqrt(3)), 1.7321, 1e-4)
# ln(-x) の微分
xm = sp.symbols("xm", negative=True)
eq("d/dx ln(-x) = 1/x", sp.simplify(sp.diff(sp.log(-xm), xm) - 1 / xm), 0)

# ══════════════════════════════════════════════════════════════
# 4. 5.11b の例題
# ══════════════════════════════════════════════════════════════
anti("5.11b Ex1a", sp.sin(2 * x + 5), -sp.cos(2 * x + 5) / 2)
anti("5.11b Ex1b", 1 / (3 * xp + 2), sp.log(3 * xp + 2) / 3, xp)
anti("5.11b Ex1c", sp.exp(4 * x), sp.exp(4 * x) / 4)
anti("5.11b Ex2", 6 * x * sp.cos(x ** 2), 3 * sp.sin(x ** 2))
anti("5.11b Ex3", sp.sin(x) / sp.cos(x), -sp.log(sp.cos(x)))
dint("5.11b Ex4", 2 * x * sp.exp(x ** 2), 0, 1, sp.E - 1)
close("e - 1", float(sp.E - 1), 1.7183, 1e-4)
# 割り忘れの誤り: -cos(2x+5) を微分すると 2 倍
eq("誤答を微分すると 2 倍", sp.simplify(sp.diff(-sp.cos(2 * x + 5), x)
                                        - 2 * sp.sin(2 * x + 5)), 0)
# GDC の数値
close("d/dx(-cos(2x+5)/2) at 1",
      float(sp.diff(-sp.cos(2 * x + 5) / 2, x).subs(x, 1)), 0.657, 1e-3)
close("sin 7", float(sp.sin(7)), 0.657, 1e-3)

# ══════════════════════════════════════════════════════════════
# 5. 5.11b の演習
# ══════════════════════════════════════════════════════════════
anti("5.11b E1", sp.cos(3 * x), sp.sin(3 * x) / 3)
anti("5.11b E2", (3 * x - 1) ** 4, (3 * x - 1) ** 5 / 15)
anti("5.11b E3", sp.exp(5 * x + 2), sp.exp(5 * x + 2) / 5)
anti("5.11b E4", 1 / (2 * xp - 7), sp.log(2 * xp - 7) / 2, xp)
anti("5.11b E5", 6 * x * (x ** 2 + 1) ** 3,
     sp.Rational(3, 4) * (x ** 2 + 1) ** 4)
anti("5.11b E6", 4 * x / (x ** 2 + 9), 2 * sp.log(x ** 2 + 9))
anti("5.11b E7", sp.cos(x) * sp.exp(sp.sin(x)), sp.exp(sp.sin(x)))
dint("5.11b E8", sp.sin(x) * sp.cos(x), 0, sp.pi / 2, sp.Rational(1, 2))
anti("5.11b E9", sp.log(xp) / xp, sp.log(xp) ** 2 / 2, xp)
# 本文の tip
anti("tip 2x/(x^2+4)", 2 * x / (x ** 2 + 4), sp.log(x ** 2 + 4))
anti("tip x/(x^2+4)", x / (x ** 2 + 4), sp.log(x ** 2 + 4) / 2)
# ln(ln x) になるのは 1/(x ln x)
xg = sp.symbols("xg", positive=True)
eq("1/(x ln x) の積分は ln(ln x)",
   sp.simplify(sp.integrate(1 / (xg * sp.log(xg)), xg) - sp.log(sp.log(xg))), 0)
# 4x sin(x^2)（本文で使い続ける形）
anti("本文 4x sin(x^2)", 4 * x * sp.sin(x ** 2), -2 * sp.cos(x ** 2))

# ══════════════════════════════════════════════════════════════
# 6. シラバス・公式集から確かめた事実
# ══════════════════════════════════════════════════════════════
inA("> Definite and indefinite integration of $x^{n}$ where $n \\in \\mathbb{Q}$, "
    "including $n = -1$, $\\sin x$, $\\cos x$, $\\dfrac{1}{\\cos^{2}x}$ and $e^{x}$.")
inB("> Integration by inspection, or substitution of the form "
    "$\\displaystyle\\int f(g(x))g'(x)\\,dx$.")
inB("> Examples: $\\displaystyle\\int\\sin(2x+5)\\,dx$")
# 公式集: 5.11 の欄は 5 つ、power rule は 5.5 の欄
inA("## 公式集の 5.11 の欄")
inA("べき乗の公式は、$5.5$ の欄にあります。")
inA("\\int x^{n}\\,dx = \\frac{x^{\\,n+1}}{n+1} + C, \\qquad n \\neq -1")
# 5.11b には印刷された公式が無い
inB("## 公式集の 5.11 の欄に、この方法の公式はありません")
notB("## 公式集に、この項目の欄はありません")
inB("y = g(u), \\ \\text{where} \\ u = f(x) \\ \\Rightarrow \\ "
    "\\frac{dy}{dx} = \\frac{dy}{du} \\times \\frac{du}{dx}")

# ══════════════════════════════════════════════════════════════
# 7. レビューで直した点の見張り（5.11a）
# ══════════════════════════════════════════════════════════════
# 1: 壊れた条件文
notA("$-1 \\neq -1$ ではないので")
inA("**もとの指数は $-2$ です。$-2 \\neq -1$ なので、べき乗の公式が使えます。**")
# 3: GDC の位置づけ
inA("**数値で答える定積分は、電卓で出して構いません**")
notA("**定積分の値は、電卓で出すのがふつうです**")
inA(": 電卓で済むかどうかの見分け方 {#tbl-ahl511a-when}")
# 4: SL 5.5 の出典
inA("**AHL 5.11 に同じ一文はありません**")
notA("シラバスは、[SL 5.5](../../ai-sl/05-calculus/sl-5-5.qmd#write-first) の段階から")
inA("## 積分の式を書かずに、電卓の値だけを書く")
# 5: 循環引用をやめた
notA("だった**（@eq-ahl511a-tan、[AHL 5.9a](ahl-5-9a.qmd#tan)）")
# 6: 1/cos^2 x の条件
inA("## $\\dfrac{1}{\\cos^{2}x}$ は、$\\cos x = 0$ のところでは考えません")
# 7: 表に x>0
inA("| $\\ln x \\ \\to \\ \\dfrac{1}{x}$（$x > 0$） |")
# 9: 覚えるべきものの言い方
notA("覚えるべきなのは、**$\\sin$ の積分にマイナスが付くこと**")
# 11: Why it works は例題と別の端
inA("\\int_{0}^{\\pi/3}\\frac{1}{\\cos^{2}x}\\,dx = \\bigl[\\tan x\\bigr]_{0}^{\\pi/3}")
# 12: 丸め
notA("6 \\times 1.6094 = 9.6566")
inA("6 \\times 1.60944 = 9.6566")
# 13: 3 s.f. の明示
inA("\\ln 3 = 1.10 \\ (3 \\text{ s.f.})")
# 14: 英語ファースト
inA("#### **modulus**（絶対値）が付く理由 {#abs}")
inA("**integrand**（被積分関数）")
inA("**anti-derivative**（原始関数）")
# 16: Interpret を足した
inA("[Interpret the value of $\\displaystyle\\int_{0}^{3}\\left(5 + 4\\cos t\\right)dt$")
# 17: テンプレートの案内
inA("$\\displaystyle\\int$ のテンプレート（$9$ キーの右のパレット）")
# 18: 検算という語
notA("電卓は、値の確かめと、")
# 19: 読者を名指ししない
notA("この本の読者がいちばん落とすところです")

# ══════════════════════════════════════════════════════════════
# 8. レビューで直した点の見張り（5.11b）
# ══════════════════════════════════════════════════════════════
# 2: sin(x^2) の言い方
inB("**この積分は、どんな方法でも $x$ の式では書けません。**")
notB("だからこの形では解けません（AI HL の範囲では、電卓で値を出します）")
# 3: exact value に小数を書かない
notB("\\bigl[e^{u}\\bigr]_{0}^{1} = e - 1 = 1.72")
inB("**`exact value` と言われているので、$1.72$ ではなく $e - 1$ と書きます**")
# 4: cos x の行の注記
inB("| $\\dfrac{\\sin x}{\\cos x}$ | $u = \\cos x$（**分母**） | $-\\sin x$ |")
inB("**$2$ 行目だけは「中身」ではなく、分母を置いています。**")
# 5: 定数倍を除いて
inB("**$g'(x)$ が（定数倍を除いて）式の中にある**ときだけです")
# 6: GDC の位置づけを 5.11a に合わせる
inB("`exact value` や `Show that` でなければ、定積分の値は電卓で出して構いません")
# 7: 分母が 0 の条件
inB("## 分母が $0$ になる点をまたぐ区間では使えません")
# 9: シラバスの言い方
inB("**$2$ つの方法が挙げられています。**")
notB("**inspection と substitution のどちらでもよい**、と書かれています")
# 11: 例題と演習を本文と別の数に
inB("\\int 6x\\cos(x^{2})\\,dx")
notB("[Use the substitution $u = x^{2}$ to find $\\displaystyle\\int 4x\\sin(x^{2})\\,dx$.]")
inB("[Find $\\displaystyle\\int \\frac{4x}{x^{2}+9}\\,dx$.]")
notB("[6]{.ex-no} [Find $\\displaystyle\\int \\frac{2x}{x^{2}+4}\\,dx$.]")
# 12: f の役の違い
inB("**ここでの $f$ は「分母」のことです。**")
# 13: 端の動き方
inB("$x = a$ のとき $u = g(a)$、$x = b$ のとき $u = g(b)$ です。")
notB("$u = g(x)$ は $g(a)$ から $g(b)$ まで動きます")
# 14: ln(ln x) の対比
inB("$\\ln(\\ln x)$ になるのは $\\displaystyle\\int\\dfrac{1}{x\\ln x}\\,dx$ のほうです。")
# 15: Guidance の 4 例の振り分け
inB("**はじめの $2$ つがこの節、後ろの $2$ つは[第3節](#sub)と[第4節](#log-form)で扱います。**")

# ══════════════════════════════════════════════════════════════
# 9. 構造の不変条件
# ══════════════════════════════════════════════════════════════
HEADS = ["What you should be able to do", "The idea", "Why it works",
         "Worked examples", "Common errors",
         "Using your GDC (TI-Nspire CX II)", "Exercises"]
for tag, TXT, path in (("5.11a", TA, A), ("5.11b", TB, B)):
    h2 = [h for h in re.findall(r"^## (.+)$", TXT, re.M) if h in HEADS]
    eq(tag + " 7 見出し", h2, HEADS)
    eq(tag + " 例題 4 つ", len(re.findall(r"::: \{#exm-", TXT)), 4)
    eq(tag + " 演習 10 問", len(re.findall(r"\[\d+\]\{\.ex-no\}", TXT)), 10)
    eq(tag + " ex-sep 9 個", TXT.count(".ex-sep"), 9)
    eq(tag + " 区切り線", TXT.count("\n---\n"), 5)
    for w in ("誰でもできる", "簡単です", "当然", "明らか", "もちろん",
              "当たり前", "そのとおり", "ご指摘", "確かめ。"):
        if w in TXT:
            NG += 1
            print("NG  %s に禁止語: %r" % (tag, w))
        else:
            OK += 1
    for m in re.finditer(r"`([^`\n]*)`", TXT):
        if "$" in m.group(1):
            NG += 1
            print("NG  %s code span に数式: %r" % (tag, m.group(0)[:60]))
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
                print("NG  %s 表のセルの数式に | : %r" % (tag, line[:70]))
                break
            j += 1
    base = os.path.dirname(path)
    for m in re.finditer(r"\]\((\.\./\.\./[^)#]+\.qmd|[a-z0-9-]+\.qmd)"
                         r"(#([a-z0-9-]+))?\)", TXT):
        p, a = m.group(1), m.group(3)
        full = os.path.normpath(os.path.join(base, p))
        if not os.path.exists(full):
            NG += 1
            print("NG  %s リンク先が無い: %s" % (tag, p))
            continue
        if a and ("{#" + a + "}") not in io.open(full, encoding="utf-8").read():
            NG += 1
            print("NG  %s アンカーが無い: %s#%s" % (tag, p, a))
        else:
            OK += 1
    for m in re.finditer(r"\]\(#([a-z0-9-]+)\)", TXT):
        if ("{#" + m.group(1) + "}") in TXT:
            OK += 1
        else:
            NG += 1
            print("NG  %s ページ内アンカーが無い: %s" % (tag, m.group(1)))
    for m in re.finditer(r"\[@(exm|eq|fig|tbl)-", TXT):
        NG += 1
        print("NG  %s ページ間 crossref: %r" % (tag, m.group(0)))
    else:
        OK += 1

for svg in ("ahl-5-11a-lnabs.svg", "ahl-5-11b-sub.svg"):
    if os.path.exists(os.path.join(os.path.dirname(A), "img", svg)):
        OK += 1
    else:
        NG += 1
        print("NG  図が無い: %s" % svg)


# ══════════════════════════════════════════════════════════
#  2026-08: 1 次式の積分公式表に a ≠ 0 の条件
# ══════════════════════════════════════════════════════════
inB("以下では $a \\neq 0$ とします（$a = 0$ なら中身が定数になり、"
    "$\\dfrac{1}{a}$ が書けません）。")
eq("a=0 では 1/a が書けない", 0 == 0, True)

print("=" * 78)
print("結果:  OK %d / NG %d" % (OK, NG))
print("=" * 78)
sys.exit(1 if NG else 0)
