# -*- coding: utf-8 -*-
"""AHL 5.12a / 5.12b（areas and volumes of revolution）の検算。
   1. すべての面積・体積を sympy で第一原理から出す
   2. 図形の公式（円錐・円柱・三角形）で、独立に突き合わせる
   3. .qmd の本文が、その式・数値どおりに書かれているかを確かめる
   4. シラバスと公式集から確かめた事実を見張る
   5. レビューで直した点を not_in_text で見張る
   6. 構造の不変条件を確かめる
   実行: python3 figs/ai-hl/check_ahl_5_12.py
"""
import io
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(__file__)
A = os.path.join(HERE, "..", "..", "ai-hl", "05-calculus", "ahl-5-12a.qmd")
B = os.path.join(HERE, "..", "..", "ai-hl", "05-calculus", "ahl-5-12b.qmd")
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


inA, notA = _in(TA, "5.12a"), _not_in(TA, "5.12a")
inB, notB = _in(TB, "5.12b"), _not_in(TB, "5.12b")

x, y, t = sp.symbols("x y t", real=True)
yp = sp.symbols("yp", positive=True)


def integ(f, a, b, v=x):
    return sp.integrate(f, (v, a, b))


def area(f, a, b, roots, v=x):
    """区間の内側の根で区切り、絶対値をとって足す。"""
    pts = [a] + sorted(r for r in roots if a < r < b) + [b]
    return sum(abs(sp.integrate(f, (v, pts[i], pts[i + 1])))
               for i in range(len(pts) - 1))


def vol(f, a, b, v=x):
    return sp.integrate(sp.pi * f ** 2, (v, a, b))


# ══════════════════════════════════════════════════════════════
# 1. 5.12a  走らせる例  y = x^2 - 4
# ══════════════════════════════════════════════════════════════
F = x ** 2 - 4
eq("定積分 0..3", integ(F, 0, 3), -3)
eq("0..2 の部分", integ(F, 0, 2), sp.Rational(-16, 3))
eq("2..3 の部分", integ(F, 2, 3), sp.Rational(7, 3))
eq("面積 0..3", area(F, 0, 3, [2]), sp.Rational(23, 3))
close("23/3", float(sp.Rational(23, 3)), 7.6667, 1e-4)
eq("部分の和が全体", integ(F, 0, 2) + integ(F, 2, 3), integ(F, 0, 3))
eq("y = 0 の解", sorted(sp.solve(F, x)), [-2, 2])
# 誤答（全体の絶対値）は 3
eq("全体の絶対値は 3", abs(integ(F, 0, 3)), 3)

# 5.12a 例題 2  sin
eq("sin 0..2pi", integ(sp.sin(x), 0, 2 * sp.pi), 0)
eq("sin 面積 0..2pi", area(sp.sin(x), 0, 2 * sp.pi, [sp.pi]), 4)
eq("sin 0..pi", integ(sp.sin(x), 0, sp.pi), 2)

# 5.12a 例題 3  y 軸
eq("int sqrt(y) 0..4", integ(sp.sqrt(yp), 0, 4, yp), sp.Rational(16, 3))
eq("長方形 8 と曲線の下 8/3", 8 - integ(x ** 2, 0, 2), sp.Rational(16, 3))
eq("4^(3/2)", sp.Integer(4) ** sp.Rational(3, 2), 8)
close("16/3", float(sp.Rational(16, 3)), 5.3333, 1e-4)

# 5.12a 例題 4  x^3 - 4x
G = x ** 3 - 4 * x
eq("G の根", sorted(sp.solve(G, x)), [-2, 0, 2])
eq("G 定積分 -1..2", integ(G, -1, 2), sp.Rational(-9, 4))
eq("G -1..0", integ(G, -1, 0), sp.Rational(7, 4))
eq("G 0..2", integ(G, 0, 2), -4)
eq("G 面積 -1..2", area(G, -1, 2, [0]), sp.Rational(23, 4))
close("23/4", float(sp.Rational(23, 4)), 5.75)
# ★レビュー 1: 交点が 3 つある曲線では領域が 2 つ
eq("G の -2..2 の面積は 8", area(G, -2, 2, [0]), 8)

# ══════════════════════════════════════════════════════════════
# 2. 5.12a の演習
# ══════════════════════════════════════════════════════════════
eq("E1", integ(x ** 2, 0, 3), 9)
eq("E2 定積分", integ(x - 3, 0, 4), -4)
eq("E2 面積", area(x - 3, 0, 4, [3]), 5)
eq("E2 三角形で確かめる", sp.Rational(1, 2) * 3 * 3 + sp.Rational(1, 2) * 1 * 1, 5)
eq("E3 定積分", integ(x ** 2 - 9, 0, 3), -18)
eq("E3 面積", area(x ** 2 - 9, 0, 3, []), 18)
eq("E3 は符号が変わらない",
   sp.sign(integ(x ** 2 - 9, 0, 1)) == sp.sign(integ(x ** 2 - 9, 1, 2)), True)
eq("E4 定積分", integ(sp.cos(x), 0, sp.pi), 0)
eq("E4 面積", area(sp.cos(x), 0, sp.pi, [sp.pi / 2]), 2)
eq("E5", integ(yp ** sp.Rational(1, 3), 0, 8, yp), 12)
eq("E5 長方形で確かめる", 16 - integ(x ** 3, 0, 2), 12)
eq("E5 8^(4/3)", sp.Integer(8) ** sp.Rational(4, 3), 16)
eq("E6", integ(yp / 2, 0, 6, yp), 9)
eq("E6 三角形で確かめる", sp.Rational(1, 2) * 3 * 6, 9)
H = x ** 3 - 3 * x ** 2 + 2 * x
eq("E7 の根", sorted(sp.solve(H, x)), [0, 1, 2])
eq("E7 定積分", integ(H, 0, 2), 0)
eq("E7 面積", area(H, 0, 2, [1]), sp.Rational(1, 2))
eq("E8 の根", sorted(sp.solve(4 - x ** 2, x)), [-2, 2])
eq("E8", integ(4 - x ** 2, -2, 2), sp.Rational(32, 3))
close("32/3", float(sp.Rational(32, 3)), 10.667, 1e-3)

# ══════════════════════════════════════════════════════════════
# 3. 5.12b の例題
# ══════════════════════════════════════════════════════════════
eq("Ex1 x 軸 y=x^2 0..2", vol(x ** 2, 0, 2), sp.Rational(32, 5) * sp.pi)
close("32pi/5", float(sp.Rational(32, 5) * sp.pi), 20.106, 1e-3)
eq("(x^2)^2 = x^4", sp.expand((x ** 2) ** 2), x ** 4)
eq("Ex2 y 軸 x^2=y 0..4", sp.integrate(sp.pi * yp, (yp, 0, 4)), 8 * sp.pi)
close("8pi", float(8 * sp.pi), 25.133, 1e-3)
# 包む円柱と内側の円錐（Ex2 の検算）
eq("包む円柱 半径2 高さ4", sp.pi * 4 * 4, 16 * sp.pi)
eq("内側の円錐", sp.Rational(1, 3) * sp.pi * 4 * 4, sp.Rational(16, 3) * sp.pi)
eq("16pi/3 < 8pi < 16pi",
   (sp.Rational(16, 3) * sp.pi < 8 * sp.pi, 8 * sp.pi < 16 * sp.pi),
   (True, True))
# Ex3 円錐
eq("Ex3 円錐", vol(x / 2, 0, 6), 18 * sp.pi)
eq("円錐の公式", sp.Rational(1, 3) * sp.pi * 9 * 6, 18 * sp.pi)
# Ex4 ボウル
eq("ボウルの口の半径", sp.solve(sp.Eq(9, x ** 2 / 4), x), [-6, 6])
eq("ボウルの体積", sp.integrate(sp.pi * 4 * yp, (yp, 0, 9)), 162 * sp.pi)
close("162pi", float(162 * sp.pi), 508.94, 1e-2)
eq("包む円柱 半径6 高さ9", sp.pi * 36 * 9, 324 * sp.pi)
eq("ちょうど半分", sp.simplify(162 * sp.pi / (324 * sp.pi)), sp.Rational(1, 2))
close("509 - 500", float(162 * sp.pi) - 500, 8.94, 1e-2)
# ★レビュー 3: 半分になるのは y=ax^2 を y=0 から y 軸で回したときだけ
a, k = sp.symbols("a k", positive=True)
eq("y=ax^2 を y 軸で 0..k はいつも半分",
   sp.simplify(sp.integrate(sp.pi * yp / a, (yp, 0, k)) / (sp.pi * (k / a) * k)),
   sp.Rational(1, 2))
eq("x 軸なら半分にならない（32pi/5 vs 32pi）",
   sp.simplify(sp.Rational(32, 5) * sp.pi / (32 * sp.pi)), sp.Rational(1, 5))
eq("y=0 から始まらないと半分にならない",
   sp.simplify(sp.integrate(sp.pi * yp, (yp, 1, 4)) / (sp.pi * 4 * 3)),
   sp.Rational(5, 8))
# ★レビュー 1: 軸を横切っても重なりは起きない
eq("x^3-4x を -2..2 で回した体積",
   sp.integrate(sp.pi * (x ** 3 - 4 * x) ** 2, (x, -2, 2)),
   sp.Rational(2048, 105) * sp.pi)
close("2048pi/105", float(sp.Rational(2048, 105) * sp.pi), 61.276, 1e-3)

# ══════════════════════════════════════════════════════════════
# 4. 5.12b の演習
# ══════════════════════════════════════════════════════════════
eq("E1", vol(2 * x, 0, 3), 36 * sp.pi)
eq("E1 円錐で確かめる", sp.Rational(1, 3) * sp.pi * 36 * 3, 36 * sp.pi)
eq("E2", vol(x ** 3, 0, 1), sp.pi / 7)
close("pi/7", float(sp.pi / 7), 0.449, 1e-3)
eq("E3", vol(sp.sqrt(x), 1, 4), sp.Rational(15, 2) * sp.pi)
close("15pi/2", float(sp.Rational(15, 2) * sp.pi), 23.562, 1e-3)
eq("E4", sp.simplify(vol(sp.exp(x), 0, 1) - sp.pi * (sp.exp(2) - 1) / 2), 0)
close("pi(e^2-1)/2", float(sp.pi * (sp.exp(2) - 1) / 2), 10.036, 1e-3)
close("e^2-1", float(sp.exp(2) - 1), 6.389, 1e-3)
eq("E5", sp.integrate(sp.pi * yp, (yp, 0, 9)), sp.Rational(81, 2) * sp.pi)
close("81pi/2", float(sp.Rational(81, 2) * sp.pi), 127.23, 1e-2)
eq("E5 円柱の半分", sp.simplify(sp.Rational(81, 2) * sp.pi / (sp.pi * 9 * 9)),
   sp.Rational(1, 2))
eq("E6", sp.integrate(sp.pi * (yp / 3) ** 2, (yp, 0, 6)), 8 * sp.pi)
eq("E6 円錐で確かめる", sp.Rational(1, 3) * sp.pi * 4 * 6, 8 * sp.pi)
eq("E7", vol(1 / x, 1, 3), sp.Rational(2, 3) * sp.pi)
close("2pi/3", float(sp.Rational(2, 3) * sp.pi), 2.0944, 1e-3)
m, h, r = sp.symbols("m h r", positive=True)
eq("E8 Show that", sp.simplify(sp.integrate(sp.pi * (m * x) ** 2, (x, 0, h))),
   sp.pi * m ** 2 * h ** 3 / 3)
eq("E8 r = mh に直す", sp.simplify((sp.pi * m ** 2 * h ** 3 / 3).subs(m, r / h)
                                   - sp.pi * r ** 2 * h / 3), 0)
# E10 の誤答
eq("E10 の誤答は面積", integ(x ** 2, 0, 2), sp.Rational(8, 3))
close("8/3", float(sp.Rational(8, 3)), 2.667, 1e-3)
# ★レビュー 5: 包む円柱の上限では pi 落としも 2 乗落としも見つからない
eq("包む円柱 32pi", sp.pi * 16 * 2, 32 * sp.pi)
close("32pi は 101", float(32 * sp.pi), 100.53, 1e-2)
eq("pi 落とし 6.4 も 2 乗落とし 8pi/3 も円柱より小さい",
   (sp.Rational(32, 5) < 32 * sp.pi, sp.Rational(8, 3) * sp.pi < 32 * sp.pi),
   (True, True))

# ══════════════════════════════════════════════════════════════
# 5. シラバス・公式集から確かめた事実
# ══════════════════════════════════════════════════════════════
inA("A = \\int_{a}^{b} |y|\\,dx")
inA("A = \\int_{a}^{b} |x|\\,dy")
inA("見出しは「**Area of region enclosed by a curve and $x$ or $y$-axes**」で、")
inA("> Including negative integrals.")
inA("シラバスの Guidance 欄も、一言だけ書いています。")
inB("V = \\int_{a}^{b}\\pi y^{2}\\,dx")
inB("V = \\int_{a}^{b}\\pi x^{2}\\,dy")
# 冒頭の 2 つの囲みは削除し、第1節に一文でまとめた
notB("## 公式集の 5.12 の欄（体積）")
inB("見出しは「**Volume of revolution about $x$ or $y$-axes**」で、")
inB("**公式集の $5.12$ の欄にあります。配られるので、覚える必要はありません。**")
# 円柱・円の面積は Prior learning、円錐は 3.1
inB("（公式集の Prior learning の欄）", 2)
inB("円錐の公式（公式集の $3.1$ の欄）")

# ══════════════════════════════════════════════════════════════
# 6. レビューで直した点の見張り（5.12a）
# ══════════════════════════════════════════════════════════════
# 1: 交点が 3 つ以上のとき
inA("**交点が $3$ つ以上ある曲線では、領域も $2$ つ以上になります。**")
notA("「曲線と $x$ 軸で囲まれた領域」と言われたら、**曲線が軸と交わる $2$ 点のあいだ**が区間です。")
# 2+3: 演習3 の条件
inA("**符号が変わらないときに限り**")
notA("**答え全体の絶対値をとるだけ**で済みます")
notA("*The curve is below the $x$-axis throughout, so*")
# 4: HL 公式集に SL の欄は無い
inA("**HL の公式集には、この欄そのものがありません。**")
notA("HL の公式集では、その条件が消えて**絶対値**に変わります。")
# 5: 高さ → 面積
inA("その部分が $+\\dfrac{16}{3}$ の面積として数えられます")
notA("折り返せば高さが $+\\dfrac{16}{3}$ 分として数えられます")
# 6: 短ざくの向き
notA("$x$ 軸のときは縦の短ざく（幅 $y$、厚み $dx$）でしたが")
# 8+9: modulus と「覚える必要はありません」
inA("**公式集の $5.12$ の欄にあります。配られるので、覚える必要はありません。**")
inA("**違うのは modulus（絶対値）だけ**です。")
# 10: ± の枝を表の前に
inA("**$2$ 乗のように偶数乗の式は、$x$ について解くと $2$ つになります。**")
# 11: 「答えだけでよいとき…」の囲みは削除した
notA("## 答えだけでよいときと、区切って書くべきときがあります")
# 12a: タイトル
inA("# AHL 5.12a — Area of a region enclosed by a curve and the $x$ or $y$-axes")
# 12d: 訳語
inA("**distance travelled**（進んだ道のり）")

# ══════════════════════════════════════════════════════════════
# 7. レビューで直した点の見張り（5.12b）
# ══════════════════════════════════════════════════════════════
# 1+7: 誤った「重なる」警告を消した
notB("**重なった立体**を作ります")
notB("**AI HL の問題では、こうした形は出ません。**")
inB("**曲線が軸を横切っても、そのまま積分して構いません。**")
inB("\\dfrac{2048\\pi}{105} = 61.3")
# 2: 同じ曲線
inB("**同じ曲線でも、軸が変われば領域も立体も変わります。**")
notB("同じ領域でも、回す軸が変われば別の立体になります。")
# 3: 半分になる条件
inB("**$y = ax^{2}$ を、$y = 0$ から $y$ 軸のまわりに回した形は、いつも外側の円柱の"
    "ちょうど半分になります**")
notB("**放物線を回した形は、外側の円柱のちょうど半分の体積になります**")
notB("放物線を $y$ 軸で回すと、いつも外側の円柱の半分になります")
# 5+6: 上限としての確かめ / 32pi = 101
inB("**答えが円柱の体積より大きくなっていたら、どこかで間違えています。**")
notB("$32\\pi = 100$")
inB("$32\\pi \\approx 101$", 2)
# 8: Common errors から移した
notB("## 面積のときの絶対値を、体積にも付ける")
notB("$V = \\displaystyle\\int_{a}^{b}\\pi\\lvert y \\rvert^{2}\\,dx$ と書いても、"
     "値は同じなので点は引かれません。")
# 9: 英語ファースト
inB("**disc**（円板）")
inB("**cylinder**（円柱）")
inB("**cone**（円錐）")
inB("面積の式には modulus（絶対値）が付いていましたが")
# 13: 表示桁と 6.4 の扱い
inB("$\\pi$ を入れたつもりなのに $6.4$ のような値が出たら")
# 「$6.4$ が出たら疑え」は、$\pi$ を入れたつもりのときに限ってしか書かない
eq("6.4 の警告は pi 条件つきのみ",
   TB.count("$6.4$ のような値が出たら"),
   TB.count("$\\pi$ を入れたつもりなのに $6.4$ のような値が出たら"))
# 15: 円錐の向き
inB("**原点をとがった先とする**半径 $2$・高さ $4$ の円錐")

# ══════════════════════════════════════════════════════════════
# 8. 構造の不変条件
# ══════════════════════════════════════════════════════════════
HEADS = ["What you should be able to do", "The idea", "Why it works",
         "Worked examples", "Common errors",
         "Using your GDC (TI-Nspire CX II)", "Exercises"]
for tag, TXT, path in (("5.12a", TA, A), ("5.12b", TB, B)):
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
        p, a2 = m.group(1), m.group(3)
        full = os.path.normpath(os.path.join(base, p))
        if not os.path.exists(full):
            NG += 1
            print("NG  %s リンク先が無い: %s" % (tag, p))
            continue
        if a2 and ("{#" + a2 + "}") not in io.open(full, encoding="utf-8").read():
            NG += 1
            print("NG  %s アンカーが無い: %s#%s" % (tag, p, a2))
        else:
            OK += 1
    for m in re.finditer(r"\]\(#([a-z0-9-]+)\)", TXT):
        if ("{#" + m.group(1) + "}") in TXT or m.group(1) == "common-errors":
            OK += 1
        else:
            NG += 1
            print("NG  %s ページ内アンカーが無い: %s" % (tag, m.group(1)))
    for m in re.finditer(r"\[@(exm|eq|fig|tbl)-", TXT):
        NG += 1
        print("NG  %s ページ間 crossref: %r" % (tag, m.group(0)))
    else:
        OK += 1

for svg in ("ahl-5-12a-below.svg", "ahl-5-12a-yaxis.svg",
            "ahl-5-12b-disc.svg", "ahl-5-12b-cone.svg"):
    if os.path.exists(os.path.join(os.path.dirname(A), "img", svg)):
        OK += 1
    else:
        NG += 1
        print("NG  図が無い: %s" % svg)

print("=" * 78)
print("結果:  OK %d / NG %d" % (OK, NG))
print("=" * 78)
sys.exit(1 if NG else 0)
