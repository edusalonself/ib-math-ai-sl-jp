# -*- coding: utf-8 -*-
"""AHL 1.10（有理数の指数）と AHL 1.11（無限等比級数）の検算。
   1. すべての値を sympy で第一原理から出す
   2. 級数は「部分和を直に足す」独立な方法とも突き合わせる
   3. .qmd の本文が、その式・数値どおりに書かれているかを確かめる
   4. シラバスと公式集から確かめた事実を見張る
   5. レビューで直した点を not_in_text で見張る
   6. 構造の不変条件を確かめる
   実行: python3 figs/ai-hl/check_ahl_1_10_11.py
"""
import io
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(__file__)
A = os.path.join(HERE, "..", "..", "ai-hl", "01-number-and-algebra",
                 "ahl-1-10.qmd")
B = os.path.join(HERE, "..", "..", "ai-hl", "01-number-and-algebra",
                 "ahl-1-11.qmd")
TA = io.open(A, encoding="utf-8").read()
TB = io.open(B, encoding="utf-8").read()

OK = NG = 0
R = sp.Rational
x, y = sp.symbols("x y", positive=True)


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


inA, notA = _in(TA, "1.10"), _not_in(TA, "1.10")
inB, notB = _in(TB, "1.11"), _not_in(TB, "1.11")


# ══════════════════════════════════════════════════════════════
# 1. AHL 1.10 の値
# ══════════════════════════════════════════════════════════════
eq("2/3+5/6", R(2, 3) + R(5, 6), R(3, 2))
eq("5/4-1/2", R(5, 4) - R(1, 2), R(3, 4))
eq("1/4+7/12", R(1, 4) + R(7, 12), R(5, 6))
eq("5/6-1/3", R(5, 6) - R(1, 3), R(1, 2))
eq("1/2+1/3", R(1, 2) + R(1, 3), R(5, 6))
eq("3/4-1/2", R(3, 4) - R(1, 2), R(1, 4))
inA("\\frac{2}{3} + \\frac{5}{6} = \\frac{4}{6} + \\frac{5}{6} = \\frac{9}{6} = \\frac{3}{2}")
inA("\\frac{5}{4} - \\frac{1}{2} = \\frac{5}{4} - \\frac{2}{4} = \\frac{3}{4}")

# 数値
eq("81^(3/4)", sp.Integer(81) ** R(3, 4), 27)
eq("9^(1/2)", sp.Integer(9) ** R(1, 2), 3)
eq("8^(1/3)", sp.Integer(8) ** R(1, 3), 2)
eq("32^(1/5)", sp.Integer(32) ** R(1, 5), 2)
eq("32^(3/5)", sp.Integer(32) ** R(3, 5), 8)
eq("32^3", sp.Integer(32) ** 3, 32768)
eq("32768^(1/5)", sp.Integer(32768) ** R(1, 5), 8)
eq("64^(2/3)", sp.Integer(64) ** R(2, 3), 16)
eq("16^(3/4)", sp.Integer(16) ** R(3, 4), 8)
eq("8^(2/3)", sp.Integer(8) ** R(2, 3), 4)
eq("125^(2/3)", sp.Integer(125) ** R(2, 3), 25)
eq("(25/4)^(-1/2)", R(25, 4) ** R(-1, 2), R(2, 5))
eq("2^(-3)", sp.Integer(2) ** -3, R(1, 8))
eq("4^(1/2)", sp.Integer(4) ** R(1, 2), 2)
eq("4^(3/2)", sp.Integer(4) ** R(3, 2), 8)
# 誤った読み方（Common errors と演習 10）
close("cbrt(32^5)", (sp.Integer(32) ** 5) ** R(1, 3), 322.5397887, 5e-6)
inA("$322.5\\ldots$")
# 根号の分配は成り立たない（Common errors）
eq("sqrt(9+16)", sp.sqrt(25), 5)
eq("sqrt9+sqrt16", sp.sqrt(9) + sp.sqrt(16), 7)
eq("その 2 つは違う", sp.sqrt(25) == sp.sqrt(9) + sp.sqrt(16), False)
# 底が負のときの食い違い（callout）
eq("(-8)^(1/3) は -2", sp.real_root(-8, 3), -2)
eq("(-8)^(2/6) の実 6 乗根は 2", sp.real_root(64, 6), 2)
eq("(-3)^2 = 9", sp.Integer(-3) ** 2, 9)

# 文字式
eq("x^{3/2}sqrt x / x^{-1/2}",
   sp.simplify(x ** R(3, 2) * sp.sqrt(x) / x ** R(-1, 2)), x ** R(5, 2))
eq("(8y^6)^{2/3}", sp.simplify((8 * y ** 6) ** R(2, 3)), 4 * y ** 4)
eq("3/cbrt(x^2)", sp.simplify(3 / (x ** 2) ** R(1, 3)), 3 * x ** R(-2, 3))
eq("(16x^8)^{3/4}", sp.simplify((16 * x ** 8) ** R(3, 4)), 8 * x ** 6)
eq("(x^2)^{3/2}/(x^{1/2}sqrt x)",
   sp.simplify((x ** 2) ** R(3, 2) / (x ** R(1, 2) * sp.sqrt(x))), x ** 2)
eq("x^{3/2}=27 の解", sp.solve(sp.Eq(x ** R(3, 2), 27), x), [9])
eq("9^{3/2} で戻る", sp.Integer(9) ** R(3, 2), 27)
# 本文の検算（x = 4 を入れる）
eq("x=4 での左辺",
   sp.simplify((4 ** R(3, 2) * sp.sqrt(4)) / 4 ** R(-1, 2)), 32)
eq("x=4 での右辺", sp.Integer(4) ** R(5, 2), 32)
inA("\\frac{4^{3/2}\\sqrt{4}}{4^{-1/2}} = \\frac{8 \\times 2}{0.5} = 32, \\qquad 4^{5/2} = 32")
# 演習 7 の検算
eq("x=4 で分子", sp.Integer(4) ** 3, 64)
eq("x=4 で答え", sp.Integer(4) ** 2, 16)

# モデル
eq("E = 290*16^{3/4}", 290 * sp.Integer(16) ** R(3, 4), 2320)
eq("S = 4.8*125^{2/3}", sp.Rational(48, 10) * sp.Integer(125) ** R(2, 3), 120)
inA("E = 290 \\times 8 = 2320")
inA("S = 4.8 \\times 25 = 120 \\text{ cm}^{2}")

# GDC のかっこ
eq("81^3/4 は 531441/4", R(81 ** 3, 4), R(531441, 4))
close("531441/4 の小数", R(531441, 4), 132860.25, 1e-9)
inA("\\dfrac{81^{3}}{4}$（`enter` なら $\\dfrac{531441}{4}$、`ctrl + enter` なら $132860.25$）")
# 根を先にとるのがいつも楽とは限らない（レビュー 4）
eq("(1/8)^(1/3) は 1/2", R(1, 8) ** R(1, 3), R(1, 2))
eq("(1/8)^2 は 1/64", R(1, 8) ** 2, R(1, 64))
close("cbrt5", sp.Integer(5) ** R(1, 3), 1.7099759, 5e-7)
inA("$\\sqrt[3]{5} = 1.7099\\ldots$")

# ══════════════════════════════════════════════════════════════
# 2. AHL 1.11 の値
# ══════════════════════════════════════════════════════════════
def sinf(u, r):
    return sp.nsimplify(sp.Rational(u) / (1 - sp.Rational(r)))


def partial(u, r, n):
    """部分和を、公式を使わずに直に足す（独立な検算）。"""
    return sum(sp.Rational(u) * sp.Rational(r) ** k for k in range(n))


eq("12,1/3 -> 18", sinf(12, R(1, 3)), 18)
eq("直に足した部分和と一致 (n=40)",
   sp.N(partial(12, R(1, 3), 40), 12), sp.N(sp.Integer(18), 12))
eq("24,-3/4", sinf(24, R(-3, 4)), R(96, 7))
close("24,-3/4 の値", sinf(24, R(-3, 4)), 13.7143, 5e-5)
eq("40,1/4", sinf(40, R(1, 4)), R(160, 3))
close("40,1/4 の値", sinf(40, R(1, 4)), 53.3333, 5e-5)
eq("18,1/3", sinf(18, R(1, 3)), 27)
eq("5,-2/5", sinf(5, R(-2, 5)), R(25, 7))
close("5,-2/5 の値", sinf(5, R(-2, 5)), 3.57143, 5e-5)
eq("u1=20,Sinf=50 -> r", sp.solve(sp.Eq(20 / (1 - sp.Symbol("r")), 50)),
   [R(3, 5)])
eq("Sinf=60,r=2/5 -> u1", 60 * (1 - R(2, 5)), 36)
eq("u1=8,Sinf=12 -> r", sp.solve(sp.Eq(8 / (1 - sp.Symbol("r")), 12)),
   [R(1, 3)])
eq("u3 = 8*(1/3)^2", 8 * R(1, 3) ** 2, R(8, 9))
eq("u2=6,u3=4 -> r", R(4, 6), R(2, 3))
eq("u1 = 6/r", 6 / R(2, 3), 9)
eq("9,2/3 -> 27", sinf(9, R(2, 3)), 27)
eq("drug 60,1/4 -> 80", sinf(60, R(1, 4)), 80)
eq("80*0.75 = 60", 80 * R(3, 4), 60)
eq("誤った r=-1.5 の計算そのものは 2.4", 6 / (1 - R(-3, 2)), R(12, 5))
eq("r=2 の数列 3,6,12,24 -> r", R(6, 3), 2)
eq("r=-1.5 の項", [6 * R(-3, 2) ** k for k in range(4)],
   [6, -9, R(27, 2), R(-81, 4)])
close("13.5", R(27, 2), 13.5, 1e-9)
close("-20.25", R(-81, 4), -20.25, 1e-9)

# 弾むボール（級数と、直に足す方法の 2 通り）
ball = 2 + 2 * sinf(sp.Rational(12, 10), sp.Rational(6, 10))
eq("ball = 8", ball, 8)
direct = 2 + 2 * sum(2 * sp.Rational(6, 10) ** k for k in range(1, 400))
close("ball を直に 400 項足しても 8", sp.N(direct, 12), 8, 1e-9)
eq("最初の落下を忘れると 6", 2 * sinf(sp.Rational(12, 10),
                                sp.Rational(6, 10)), 6)
eq("2 倍を忘れると 5", 2 + sinf(sp.Rational(12, 10), sp.Rational(6, 10)), 5)
inB("\\text{total} = 2 + 2(3) = 8 \\text{ m}")
eq("1 回目の高さ", 2 * sp.Rational(6, 10), sp.Rational(6, 5))
eq("2 回目の高さ", 2 * sp.Rational(6, 10) ** 2, sp.Rational(18, 25))
close("0.72", sp.Rational(18, 25), 0.72, 1e-9)
close("0.432", 2 * sp.Rational(6, 10) ** 3, 0.432, 1e-9)

# r^n の表（レビュー 1 で直した行）
for r, want in ((R(9, 10), ("0.349", "0.00515", "2.66e-5")),
                (R(-3, 4), ("0.0563", "5.66e-7", "3.21e-13")),
                (R(11, 10), ("2.59", "117.", "1.38e+4"))):
    got = tuple(str(sp.N(r ** n, 3)) for n in (10, 50, 100))
    eq("r^n の表 r=%s" % r, got, want)
eq("(-3/4)^50 は正", sp.N(R(-3, 4) ** 50, 3) > 0, True)
close("(-3/4)^51", R(-3, 4) ** 51, -4.25e-7, 5e-10)
inB("| $-0.75$ | $0.0563$ | $0.000000566$ | $0.000000000000321$ |")
inB("$(-0.75)^{51} = -0.000000425$")

# 部分和の値（GDC の節）
for n, want in ((3, 17.3333), (5, 17.9259), (10, 17.9997)):
    close("S_%d" % n, partial(12, R(1, 3), n), want, 5e-4)
inB("$17.333\\ldots$、$17.926\\ldots$、$17.9997$")
close("S4 = 17.77", partial(12, R(1, 3), 4), 17.7778, 5e-4)
close("8+8/3+8/9+8/27", partial(8, R(1, 3), 4), 11.8519, 5e-4)
close("5-2+0.8-0.32", partial(5, R(-2, 5), 4), 3.48, 5e-3)

# r = -1 の部分和（表の行）
eq("r=-1 の部分和は u1,0,u1,0",
   [partial(1, -1, n) for n in (1, 2, 3, 4)], [1, 0, 1, 0])
# レビュー 2・3 の反例
eq("u1<0 では Sinf < u1", sinf(-10, R(1, 2)) < -10, True)
eq("u1<0, r<0 では Sinf > u1", sinf(-5, R(-2, 5)) > -5, True)

# ══════════════════════════════════════════════════════════════
# 3. シラバス・公式集から確かめた事実
# ══════════════════════════════════════════════════════════════
inA("> Simplifying expressions, both numerically and algebraically, involving rational exponents.")
inA("32^{\\frac{3}{5}} = 8$, $\\quad x^{-\\frac{1}{2}} = \\dfrac{1}{\\sqrt{x}}$")
inA("**AHL 1.10 の欄はありません。**")
inA("a^{x} = b \\iff x = \\log_{a} b, \\quad a > 0,\\ b > 0,\\ a \\neq 1")
inB("S_{\\infty} = \\frac{u_1}{1-r}, \\quad \\lvert r \\rvert < 1")
inB("見出しは「**The sum of an infinite geometric sequence**」です。")
inB("> The sum of infinite geometric sequences.")
inB("> **Link to:** the concept of a limit (SL 5.1), fractals (AHL 3.9), and Markov chains (AHL 4.19).")
inB("> **Other contexts:** Total distance travelled by a bouncing ball.")
inB("> **TOK:** Is it possible to know about things of which we can have no experience, such as infinity?")
inB("S_n = \\frac{u_1\\left(1-r^{n}\\right)}{1-r}, \\quad r \\neq 1")

# ══════════════════════════════════════════════════════════════
# 4. GDC（機種の制約）
# ══════════════════════════════════════════════════════════════
for T, tag in ((TA, "1.10"), (TB, "1.11")):
    eq(tag + " ctrl+doc は Document Settings に使わない",
       "ctrl + doc → Document Settings" in T, False)
inA("TI-Nspire CX II（非CAS）は Numeric なので")
inA("**$9$ キーの右にあるテンプレートのパレット**")
inB("$\\Sigma$ のテンプレート（$9$ キーの右のパレット）")
inB("sum(seq(12×(1/3)^(n-1), n, 1, 10))")
inB("ctrl + doc → 4: Add Lists & Spreadsheet")

# ══════════════════════════════════════════════════════════════
# 5. レビューで直した点の見張り
# ══════════════════════════════════════════════════════════════
# 1.10 — 1・3: 非CAS は根号を残さない
notA("`enter` なら $2\\sqrt{3}$、`ctrl + enter` なら $3.4641\\ldots$ です。")
notA("| `81^3/4` | $\\dfrac{81^{3}}{4} = 132860.25$ |")
inA("は `enter` でも $3.4641\\ldots$ と小数で返ります")
# 2: 図の説明
notA("$y = x^{1/2}$ と $y = x^{3/2}$ は、$y = x^{1}$ と $y = x^{2}$ の**間に入る**曲線です。")
inA("$y = x^{1/2}$ のほうは $y = x^{1}$ より**下**です。")
# 4: 根を先に、の条件
notA("手で計算するときは、いつも根を先にとってください。")
inA("そういうときは、電卓に `5^(2/3)` とそのまま入れます。")
# 5: half-life の参照
notA("$2^{-t/T}$ のような形が出ます")
inA("[AHL 1.9](ahl-1-9.qmd) では $M = 200e^{-0.03t}$ のような形で扱います。")
# 6: n 乗根のパレットの場所
notA("$n$ 乗根は、その右のパレットにある")
# 7: 偶数乗根の符号
inA("$n$ が偶数のときは、$(-3)^{2} = 9$ のように**負の数を $n$ 乗しても $a$ になります。**")
# 8: The idea と Why it works の重複を解消
eq("1.10 で導出は 1 回だけ",
   TA.count("\\left(a^{1/n}\\right)^{n} = a^{\\frac{1}{n} \\times n} = a^{1} = a"), 1)
inA("[Why it works](#why-it-works) にあります")
# 小さい点
notA("$3$ 行も $4$ 行も続く変形は出てきません。")
notA("$b$ はふつう分数になります")
inA("**power model**（べき乗モデル）")
inA("**power rule**（累乗の微分の法則）")
inA("そこで止まってエラーの表示が出ます。")
inA("where $x > 0$")

# 1.11 — 2・3: u1 > 0 の条件
notB("$\\lvert r \\rvert < 1$ で $r > 0$ のときは、$1-r$ が $1$ より小さいので、**$S_{\\infty}$ は必ず $u_1$ より大きく**なります。")
inB("$u_1 > 0$ で $0 < r < 1$ のときは")
inB("**$u_1$ が負のときは、向きがそっくり逆になります。**")
notB("$r$ が負のときは、これで正しくなります。項が交互に引かれるからです。")
inB("$u_1 > 0$ で $r$ が負のときは、これで正しい向きです。")
# 4: 採点の断定をやめ、解答例に条件を足した
notB("これを書かないと $1$ 点落とします")
notB("ここが取られやすい $1$ 点です。")
eq("1.11 の解答例に条件の行が 8 か所",
   TB.count("so the sum to infinity exists") +
   TB.count("so the sum to infinity does exist"), 9)
# 5: Sigma の書き方
notB("Σ(12·(1/3)^(n-1), n, 1, 20)")
# 6: ボールの model answer
notB("a real ball stops bouncing after a finite time")
inB("a real ball stops after a finite number of bounces")
notB("ただし実際のボールは有限の時間で止まり")
# 7: n=20 では差が見えない
notB("$n = 20$ まで足した値が返ります。$18$ にどれだけ近いかを見てください。")
inB("$n = 20$ まで行くと画面には $18$ と出ます。")
# 8: 訳語
notB("ひとつの値に近づく（**converge**） |")
inB("**converge**・収束する")
inB("**limit**（極限）")
# 9: 丸めた部分和
notB("= 17.78$ で、$18$ に近づいています")
notB("= 11.85$ で、$12$ に近づいています")
inB("= 17.77\\ldots$ で、$18$ に近づいています")
# 10: 符号だけで判断しない
inB("**それらしい数が出てしまう**場合もあります（演習 $10$）")
# 小さい点
inB("(a) の**青いほうの点**が、そのまま表になります。")

# ══════════════════════════════════════════════════════════════
# 6. 構造の不変条件
# ══════════════════════════════════════════════════════════════
HEADS = ["What you should be able to do", "The idea", "Why it works",
         "Worked examples", "Common errors",
         "Using your GDC (TI-Nspire CX II)", "Exercises"]
for tag, TXT, pref in (("1.10", TA, "ahl110"), ("1.11", TB, "ahl111")):
    h2 = [h for h in re.findall(r"^## (.+)$", TXT, re.M) if h in HEADS]
    eq(tag + " 7 見出し", h2, HEADS)
    eq(tag + " 例題 4 つ", len(re.findall(r"::: \{#exm-", TXT)), 4)
    eq(tag + " 演習 10 問", len(re.findall(r"\[\d+\]\{\.ex-no\}", TXT)), 10)
    eq(tag + " ex-sep 9 個", TXT.count(".ex-sep"), 9)
    eq(tag + " --- は 6 個", len(re.findall(r"^---$", TXT, re.M)), 6)
    eq(tag + " 日本語訳 14 個", TXT.count('<details class="jp-trans">'), 14)
    nums = [int(n) for n in re.findall(r"^### (\d+)\.", TXT, re.M)]
    cut = nums.index(1, 1)
    eq(tag + " The idea の節番号が連番", nums[:cut],
       list(range(1, cut + 1)))
    eq(tag + " GDC の節番号が連番", nums[cut:],
       list(range(1, len(nums) - cut + 1)))
    for w in ("誰でもできる", "簡単です", "当然", "明らか", "もちろん",
              "当たり前", "確かめ。", "そのとおり", "ご指摘"):
        eq(tag + " 禁止語 " + w, w in TXT, False)
    eq(tag + " 検算がある", TXT.count("**検算。**") >= 3, True)
    bad = [m for m in re.findall(r"`[^`\n]*`", TXT) if "$" in m]
    eq(tag + " コードスパンに数式なし", bad, [])
    pipes = []
    for line in TXT.split("\n"):
        if line.strip().startswith("|"):
            pipes += [m for m in re.findall(r"\$[^$]*\$", line) if "|" in m]
    eq(tag + " 表の数式に | なし", pipes, [])
    lines = TXT.split("\n")
    nob = [i + 1 for i, l in enumerate(lines)
           if l.startswith("::: {") and i > 0 and lines[i - 1].strip() != ""]
    eq(tag + " ::: の前に空行", nob, [])
    ids = set(re.findall(r"\{#([A-Za-z0-9\-_]+)\}", TXT))
    miss = [a for a in re.findall(r"\]\(#([A-Za-z0-9\-_]+)\)", TXT)
            if a not in ids and a not in ("common-errors", "why-it-works")]
    eq(tag + " ページ内リンクが解決", miss, [])
    xref = re.findall(r"@(?:exm|eq|fig|tbl)-([A-Za-z0-9]+)", TXT)
    eq(tag + " 他ページの crossref なし",
       [k for k in xref if not k.startswith(pref)], [])

eq("1.10 の model-answer 3 個", TA.count(".model-answer"), 3)
eq("1.11 の model-answer 5 個", TB.count(".model-answer"), 5)

IMG = os.path.join(HERE, "..", "..", "ai-hl", "01-number-and-algebra", "img")
for f in ("ahl-1-10-powers.svg", "ahl-1-11-sum.svg"):
    eq("図 " + f, os.path.exists(os.path.join(IMG, f)), True)
eq("png を残していない",
   [f for f in os.listdir(IMG)
    if (f.startswith("ahl-1-10") or f.startswith("ahl-1-11"))
    and f.endswith(".png")], [])

# 登録
QY = io.open(os.path.join(HERE, "..", "..", "_quarto-draft.yml"),
             encoding="utf-8").read()
IX = io.open(os.path.join(HERE, "..", "..", "ai-hl", "index.qmd"),
             encoding="utf-8").read()
GL = io.open(os.path.join(HERE, "..", "..", "glossary-ai.qmd"),
             encoding="utf-8").read()
for s in ("ai-hl/01-number-and-algebra/ahl-1-10.qmd",
          "ai-hl/01-number-and-algebra/ahl-1-11.qmd",
          "AHL 1.10 — Rational exponents",
          "AHL 1.11 — The sum of an infinite geometric sequence"):
    eq("_quarto-draft.yml に " + s[:44], s in QY, True)
for s in ("01-number-and-algebra/ahl-1-10.qmd",
          "01-number-and-algebra/ahl-1-11.qmd"):
    eq("index.qmd に " + s[:44], s in IX, True)
# 「残りの N 項目」が、✅ の付いていない項目表の行数と合っているか
_rows = re.findall(r"^\| (?:\*\*)?AHL [0-9.]+(?:\*\*)? \|(.*)\|$", IX, re.M)
_left_rows = [r for r in _rows if "\u2705" not in r]
_left = re.search(r"残りの(\d+)項目", IX)
eq("残りの N 項目 があるか、全部の行に ✅ が付いている",
   _left is not None or len(_left_rows) == 0, True)
if _left:
    eq("残りの N 項目 が、まだ書いていない行の数と合う",
       len(_left_rows), int(_left.group(1)))
for s in ("| rational exponent | 有理数の指数 |", "| partial sum | 部分和 |",
          "| sum to infinity | 無限級数の和 |", "| to converge | 収束する |",
          "| to diverge | 発散する |", "| limit | 極限 |",
          "| $n$th root | $n$ 乗根 |", "| to approach | 近づく |"):
    eq("glossary に " + s[:34], s in GL, True)


# ══════════════════════════════════════════════════════════════
#  2026-08 の修正
# ══════════════════════════════════════════════════════════════
# 1.10 — 負の底: 既約分数の分母が奇数なら実数になる場合がある
eq("(-8)^(1/3) は実数 -2", R(-8) ** R(1, 3) == -2 or sp.real_root(-8, 3) == -2, True)
eq("(-8)^(2/6) を 6 乗根で読むと 2（食い違う）", sp.root(sp.Integer(64), 6), 2)
inA("負の底でも、指数を**既約分数**にしたときの**分母が奇数**なら、実数として扱える場合はあります")
inA("ですからこのページでは、**底 $a$ は正の数に限ります。**")
notA("分数の指数を使うときは、**$a > 0$ に限る**のが約束です。")
# 1.10 — √ は非負
inA("$\\sqrt{\\ }$ は非負の値を表すと決めておかないと")
notA("$\\sqrt{\\ }$ をいつも正の数と決めておかないと")

# 1.11 — 発散の場合分け（u1 != 0 を前提にする）
def parts(u, r, n):
    return [partial(u, r, k) for k in range(1, n + 1)]

# r > 1: 大きさが際限なく大きくなる（u1 が負でも「増え続ける」とは限らない）
eq("r=2, u1=-3 の部分和は減り続ける", all(a > b for a, b in
   zip(parts(-3, 2, 8), parts(-3, 2, 8)[1:])), True)
eq("r=2, u1=-3 でも |S_n| は増え続ける", all(abs(a) < abs(b) for a, b in
   zip(parts(-3, 2, 8), parts(-3, 2, 8)[1:])), True)
# r < -1: 符号を変えながら大きくなる
sgn = [1 if v > 0 else -1 for v in parts(1, -2, 8)]
eq("r=-2 の部分和は符号が変わる", len(set(sgn)) == 2, True)
eq("r=-2 の |S_n| は際限なく大きくなる", abs(partial(1, -2, 20)) > 1e5, True)
# r = 1: S_n = n u1
eq("r=1 は S_n = n u1", partial(5, 1, 7), 35)
# r = -1: u1, 0, u1, 0, ...
eq("r=-1 の部分和は u1,0,u1,0", parts(5, -1, 4), [5, 0, 5, 0])
inB("以下では、ふつうの等比数列として **$u_1 \\neq 0$** を考えます")
inB("$r$ が何であっても $S_{\\infty} = 0$ が存在する、という例外があります）")
inB("### 6. $u_1 \\neq 0$ で $\\lvert r \\rvert \\geq 1$ なら、和が存在しません {#diverge}")
inB("- **$u_1 \\neq 0$ で $\\lvert r \\rvert \\geq 1$ なら和が存在しない**ことを、理由とともに説明できる。")
notB("### 6. $\\lvert r \\rvert \\geq 1$ のときは、和が存在しません {#diverge}")
notB("- **$\\lvert r \\rvert \\geq 1$ のときは和が存在しない**ことを")
# u1 = 0 なら、どの r でも部分和はすべて 0
eq("u1=0, r=5 の部分和は全部 0", [partial(0, 5, k) for k in range(1, 6)],
   [0, 0, 0, 0, 0])
eq("u1=0, r=-3 の部分和は全部 0", [partial(0, -3, k) for k in range(1, 6)],
   [0, 0, 0, 0, 0])
# 1.10 の囲みの見出しは「このページ」
inA("## このページでは、底 $a$ は正の数とします")
# exact value を「整数」と同一視しない
inA("**(c)** `exact value` なので、小数近似ではなく正確な値で答えます。")
notA("`exact value` なので、小数ではなく整数で答えます。")
notA("## この本では、底 $a$ は正の数とします")
inB("| $r > 1$ | 一定の値に近づかず、大きさが際限なく大きくなる | **存在しない** |")
inB("| $r < -1$ | 符号を変えながら、大きさが際限なく大きくなる | **存在しない** |")
inB("| $r = 1$ | $S_n = n\\,u_1$。一定の値に近づかない | **存在しない** |")
inB("| $r = -1$ | $u_1,\\ 0,\\ u_1,\\ 0,\\ \\ldots$ と振動し、一定の値に近づかない | **存在しない** |")
inB(": $r$ で決まること（$u_1 \\neq 0$） {#tbl-ahl111-cases}")
notB("| $r > 1$ または $r < -1$ | 大きさが増え続ける | **存在しない** |")
notB("| $r = 1$ | $S_n = n\\,u_1$ で増え続ける | **存在しない** |")

print("=" * 78)
print("結果:  OK %d / NG %d" % (OK, NG))
print("=" * 78)
sys.exit(1 if NG else 0)
