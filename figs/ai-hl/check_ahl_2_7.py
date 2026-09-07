"""AHL 2.7（合成関数と逆関数）の内容を検算する。

    python3 figs/ai-hl/check_ahl_2_7.py

方針
  1. すべての数値・式を sympy で第一原理から出す
  2. 別の方法（数値代入・グラフ的な条件）で交差検証する
  3. ページの本文がその結果と一致しているかを in_text で確かめる
  4. レビューで直した箇所は not_in_text で再発を防ぐ
  5. 構造（見出し・例題数・演習数・区切り）を確かめる
"""
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
QMD = os.path.join(HERE, "..", "..", "ai-hl", "02-functions", "ahl-2-7.qmd")
TEXT = open(QMD, encoding="utf-8").read()

OK = NG = 0


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def eq(a, b, msg):
    chk(sp.simplify(sp.sympify(a) - sp.sympify(b)) == 0, msg)


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている（直したはず）: " + msg + " :: " + sub[:70])


x, y = sp.symbols("x y", real=True)

# ══════════════════════════════════════════════════════════
# 1. The idea — 合成の基本（f(x)=2x+1, g(x)=x^2）
# ══════════════════════════════════════════════════════════
f = 2 * x + 1
g = x ** 2


def comp(outer, inner):
    """outer ∘ inner"""
    return sp.expand(outer.subs(x, inner))


fg = comp(f, g)          # (f∘g)(x)
gf = comp(g, f)          # (g∘f)(x)

eq(fg, 2 * x ** 2 + 1, "(f∘g)(x) = 2x^2+1")
eq(gf, 4 * x ** 2 + 4 * x + 1, "(g∘f)(x) = 4x^2+4x+1")
eq(gf, sp.expand((2 * x + 1) ** 2), "(g∘f)(x) = (2x+1)^2")

chk(fg.subs(x, 3) == 19, "(f∘g)(3) = 19")
chk(gf.subs(x, 3) == 49, "(g∘f)(3) = 49")
chk(g.subs(x, 3) == 9 and f.subs(x, 9) == 19, "3 → g → 9 → f → 19")
chk(f.subs(x, 3) == 7 and g.subs(x, 7) == 49, "3 → f → 7 → g → 49")

in_text("f(g(3)) = f(9) = 2(9)+1 = 19")
in_text("g(f(3)) = g(7) = 7^{2} = 49")
in_text("(f \\circ g)(x) = f\\left(x^{2}\\right) = 2x^{2}+1")
in_text("(g \\circ f)(x) = g(2x+1) = (2x+1)^{2} = 4x^{2}+4x+1")

# かけ算は合成と別もの
eq(sp.expand(f * g), 2 * x ** 3 + x ** 2, "f(x)g(x) = 2x^3+x^2")
in_text("f(x) \\times g(x) = (2x+1)\\left(x^{2}\\right) = 2x^{3}+x^{2}")

# GDC 検算に使っている値
chk(fg.subs(x, 4) == 33, "(f∘g)(4) = 33")
in_text("どちらも $33$ になれば")

# 次数の主張（レビュー 7）: 合成は次数の積、かけ算は和
chk(sp.degree(fg, x) == 2 and sp.degree(sp.expand(f * g), x) == 3,
    "合成 2 次・かけ算 3 次")
c1 = comp(x ** 2, x ** 2 + 1)
c2 = sp.expand((x ** 2) * (x ** 2 + 1))
chk(sp.degree(c1, x) == 4 and sp.degree(c2, x) == 4 and sp.simplify(c1 - c2) != 0,
    "次数が同じでも別の関数になる反例（x^2 と x^2+1）")
in_text("かけ算は次数を足し、合成は次数をかけます")
in_text("どちらも $4$ 次です。それでも別の関数です")
not_in_text("**次数からして違います。** 掛け算なら次数が足されますが、合成では足されません",
            "レビュー7: 次数だけで見分けられるという主張")

# ══════════════════════════════════════════════════════════
# 2. 文脈（割引と税）
# ══════════════════════════════════════════════════════════
d = x - 500
t = sp.Rational(11, 10) * x

td = sp.expand(comp(t, d))       # 割引してから課税
dt = sp.expand(comp(d, t))       # 課税してから割引
eq(td, sp.Rational(11, 10) * x - 550, "(t∘d)(x) = 1.1x-550")
eq(dt, sp.Rational(11, 10) * x - 500, "(d∘t)(x) = 1.1x-500")
chk(td.subs(x, 3000) == 2750, "(t∘d)(3000) = 2750")
chk(dt.subs(x, 3000) == 2800, "(d∘t)(3000) = 2800")
chk(sp.simplify(dt - td) == 50, "差はいつも 50 円")
chk(sp.Rational(11, 10) * 500 - 500 == 50, "1.1×500-500 = 50")
in_text("1.1 \\times 500 - 500 = 550 - 500 = 50")
# 文脈の domain（レビュー 15）
chk(d.subs(x, 500) == 0, "x=500 で割引後がちょうど 0")
chk(d.subs(x, 499) < 0, "x<500 では割引後が負")
in_text("この $2$ つは、$x \\geq 500$ の商品に使います")

# ══════════════════════════════════════════════════════════
# 3. 逆関数の作り方（f(x)=3/(x-2)）
# ══════════════════════════════════════════════════════════
F = 3 / (x - 2)
sol = sp.solve(sp.Eq(y, F), x)
chk(len(sol) == 1, "3/(x-2) は x について 1 つに解ける")
Finv = sp.simplify(sol[0].subs(y, x))
eq(Finv, 3 / x + 2, "f^{-1}(x) = 3/x + 2")
eq(sp.simplify(F.subs(x, Finv)), x, "(f∘f^{-1})(x) = x")
eq(sp.simplify(Finv.subs(x, F)), x, "(f^{-1}∘f)(x) = x")
chk(F.subs(x, 5) == 1 and Finv.subs(x, 1) == 5, "f(5)=1, f^{-1}(1)=5")
in_text("f^{-1}(x) = \\frac{3}{x} + 2")
in_text("両辺を $y$ で割ります（$f$ の range は $y \\neq 0$ なので、これができます）")
not_in_text("**手順 2。** $x$ を左に出します。分母を払って、",
            "レビュー14: y で割る手順を書かずに進んでいた")

# ══════════════════════════════════════════════════════════
# 4. domain restriction（シラバスの Example）
# ══════════════════════════════════════════════════════════
P = (x - 3) ** 2 - 2
chk(P.subs(x, 1) == 2 and P.subs(x, 5) == 2, "f(1)=f(5)=2（one-to-one でない）")
chk(P.subs(x, 3) == -2, "頂点 (3, -2)")
roots = sp.solve(sp.Eq(P, 2), x)
chk(sorted(roots) == [1, 5], "f(x)=2 の解は 1 と 5")

up = 3 + sp.sqrt(x + 2)     # x>=3 に制限したときの逆関数
lo = 3 - sp.sqrt(x + 2)     # x<=3 に制限したときの逆関数
eq(sp.simplify(P.subs(x, up)), x, "上の枝: f(f^{-1}(x)) = x")
eq(sp.simplify(P.subs(x, lo)), x, "下の枝: f(f^{-1}(x)) = x")
chk(up.subs(x, 2) == 5, "f^{-1}(2) = 5（x>=3 の枝）")
chk(lo.subs(x, 2) == 1, "f^{-1}(2) = 1（x<=3 の枝）")
chk(sp.simplify(up.subs(x, -2)) == 3 and sp.simplify(lo.subs(x, -2)) == 3,
    "どちらの枝も x=-2 で 3")

# ★ レビュー 1 の核心: f∘f^{-1} は枝の取りちがえを検出できない
chk(sp.simplify(P.subs(x, up) - x) == 0 and sp.simplify(P.subs(x, lo) - x) == 0,
    "f(f^{-1}(x)) = x は両方の枝で成り立つ（＝検出できない）")
# 逆向きなら検出できる
back = sp.simplify(up.subs(x, P))          # f^{-1}(f(x)) with the wrong branch
chk(sp.simplify(back - (3 + sp.Abs(x - 3))) == 0,
    "誤った枝では f^{-1}(f(x)) = 3+|x-3|")
chk(back.subs(x, 1) == 5 and back.subs(x, 1) != 1,
    "x=1（x<=3 側）では x に戻らない → 検出できる")
in_text("f\\left(3+\\sqrt{x+2}\\right) = \\left(\\left(3+\\sqrt{x+2}\\right)-3\\right)^{2}-2 = (x+2)-2 = x")
in_text("**この向きの検算は、枝の取りちがえを見つけられません。**")
in_text("f^{-1}(f(x)) = 3+\\lvert x-3 \\rvert")
not_in_text("**逆関数を求めたあとの検算にそのまま使えます。** 求めた $f^{-1}$ を $f$ に入れて $x$ に戻れば、合っています。",
            "レビュー1: 枝の誤りを見逃す検算を万能と書いていた")

# 枝の表
in_text("| $x \\geq 3$ | $x-3 \\geq 0$ | $+$ | $3 + \\sqrt{x+2}$ | $x \\geq -2$ |")
in_text("| $x \\leq 3$ | $x-3 \\leq 0$ | $-$ | $3 - \\sqrt{x+2}$ | $x \\geq -2$ |")

# ± が出る＝制限が必要、ではない（レビュー 10）
in_text("**range の中の $y$ を $1$ つ決めると、$x$ が $2$ つ返ってくる**")
in_text("$2$ つのうち片方は domain の外にあるので、そこで自動的に $1$ つに決まります")
not_in_text("**$y$ を $1$ つ決めても $x$ が $2$ つ返ってくる**ということです。$1$ つの入力に $2$ つの出力を返すものは、関数ではありません。\n\n$\\pm$",
            "レビュー10: 条件のない ± の主張")
chk(sp.solve(sp.Eq(P, -3), x) == [] or all(not v.is_real for v in sp.solve(sp.Eq(P, -3), x)),
    "range の外（y=-3）では実数解がない")

# ══════════════════════════════════════════════════════════
# 5. Worked example 2（写真の拡大と縁）
# ══════════════════════════════════════════════════════════
e_ = sp.Rational(3, 2) * x
b_ = x + 4
be = sp.expand(comp(b_, e_))      # 拡大してから縁
eb = sp.expand(comp(e_, b_))      # 縁を付けてから拡大
eq(be, sp.Rational(3, 2) * x + 4, "(b∘e)(x) = 1.5x+4")
eq(eb, sp.Rational(3, 2) * x + 6, "(e∘b)(x) = 1.5x+6")
chk(be.subs(x, 20) == 34, "(b∘e)(20) = 34")
chk(eb.subs(x, 20) == 36, "(e∘b)(20) = 36")
chk(sp.simplify(eb - be) == 2, "差はいつも 2 cm")
chk(sp.Rational(3, 2) * 4 - 4 == 2, "1.5×4-4 = 2")
chk(sp.Rational(3, 2) * 2 == 3, "2 cm の縁が 3 cm になる")
in_text("1.5(20+4) = 1.5(24) = 36")
in_text("縁は $2$ cm ずつのはずが、$3$ cm ずつになります")

# ══════════════════════════════════════════════════════════
# 6. Exercises
# ══════════════════════════════════════════════════════════
# 1
e1f, e1g = 3 * x - 5, x + 2
chk(comp(e1f, e1g).subs(x, 4) == 13, "演習1 (f∘g)(4) = 13")
chk(comp(e1g, e1f).subs(x, 4) == 9, "演習1 (g∘f)(4) = 9")
chk(e1g.subs(x, 4) == 6 and e1f.subs(x, 6) == 13, "演習1 途中値 6")
chk(e1f.subs(x, 4) == 7 and e1g.subs(x, 7) == 9, "演習1 途中値 7")

# 2
e2f, e2g = x ** 2, x - 3
eq(comp(e2f, e2g), x ** 2 - 6 * x + 9, "演習2 (f∘g)(x) = x^2-6x+9")
eq(comp(e2g, e2f), x ** 2 - 3, "演習2 (g∘f)(x) = x^2-3")
chk(comp(e2f, e2g).subs(x, 5) == 4, "演習2 検算 (f∘g)(5) = 4")
chk(comp(e2g, e2f).subs(x, 5) == 22, "演習2 検算 (g∘f)(5) = 22")
chk(sp.expand((x - 3) ** 2) != x ** 2 - 9, "(x-3)^2 は x^2-9 ではない")

# 3
a_, b3 = x ** 2 - 1, 3 * x
ab = sp.expand(comp(a_, b3))
ba = sp.expand(comp(b3, a_))
eq(ab, 9 * x ** 2 - 1, "演習3 (a∘b)(x) = 9x^2-1")
eq(ba, 3 * x ** 2 - 3, "演習3 (b∘a)(x) = 3x^2-3")
chk(sp.solve(sp.Eq(ab, ba), x) == [] or
    all(not v.is_real for v in sp.solve(sp.Eq(ab, ba), x)),
    "演習3 実数解なし")
eq(sp.expand(ab - ba), 6 * x ** 2 + 2, "演習3 差は 6x^2+2")
disc = 0 ** 2 - 4 * 6 * 2
chk(disc == -48, "演習3 判別式 -48")
chk(ab.subs(x, 1) == 8 and a_.subs(x, b3.subs(x, 1)) == 8, "演習3 検算 x=1 で 8")
chk(ba.subs(x, 1) == 0 and b3.subs(x, a_.subs(x, 1)) == 0, "演習3 検算 x=1 で 0")
# 誤答 3x^2-1 では 2 つの式を比べるだけでは気づけない（レビュー 6）
wrong = 3 * x ** 2 - 1
chk(sp.solve(sp.Eq(wrong, ba), x) == [], "誤答でも『実数解なし』に着地してしまう")
chk(wrong.subs(x, 1) != ab.subs(x, 1), "もとの関数に入れれば誤答は見破れる")
in_text("$2$ つの式どうしを見くらべるだけでは、この誤りは見つかりません")
not_in_text("**検算。** $x = 0$ で $-1$ と $-3$、$x = 1$ で $8$ と $0$。$(a \\circ b)$ のほうがいつも大きくなっています",
            "レビュー6: 誤りを検出できない検算")

# 4, 5
i4 = sp.solve(sp.Eq(y, 3 * x - 5), x)[0].subs(y, x)
eq(i4, (x + 5) / 3, "演習4 f^{-1}(x) = (x+5)/3")
chk((3 * x - 5).subs(x, 4) == 7 and i4.subs(x, 7) == 4, "演習4 検算 4↔7")
i5 = sp.solve(sp.Eq(y, (x + 1) / 4), x)[0].subs(y, x)
eq(i5, 4 * x - 1, "演習5 f^{-1}(x) = 4x-1")
chk(((x + 1) / 4).subs(x, 7) == 2 and i5.subs(x, 2) == 7, "演習5 検算 7↔2")

# 6
f6 = 2 / (x + 3)
i6 = sp.simplify(sp.solve(sp.Eq(y, f6), x)[0].subs(y, x))
eq(i6, 2 / x - 3, "演習6 f^{-1}(x) = 2/x-3")
eq(sp.simplify(f6.subs(x, i6)), x, "演習6 (f∘f^{-1})(x) = x")
chk(f6.subs(x, -1) == 1 and i6.subs(x, 1) == -1, "演習6 検算 -1↔1")
chk(sp.solve(sp.Eq(f6, 0), x) == [], "演習6 f は 0 にならない → domain x≠0")

# 7
f7 = x ** 2 + 4
i7 = sp.sqrt(x - 4)
eq(sp.simplify(f7.subs(x, i7)), x, "演習7 (f∘f^{-1})(x) = x")
chk(f7.subs(x, 3) == 13 and i7.subs(x, 13) == 3, "演習7 検算 3↔13")
chk(sp.minimum(f7, x, sp.Interval(0, sp.oo)) == 4, "演習7 x>=0 での f の最小値 4")
# ★ レビュー 2: domain of f^{-1} = range of f。制限すると根号の見方はずれる
chk(sp.minimum(f7, x, sp.Interval(1, sp.oo)) == 5,
    "x>=1 に制限すると range は y>=5（根号の見方の x>=4 とずれる）")
in_text("$f^{-1}$ の domain は、**$f$ の range** です")
in_text("$f^{-1}$ の domain は $x \\geq 5$ です。根号だけを見ると $x \\geq 4$ となって、**広すぎる答え**になります")
not_in_text("**どちらでも同じ答えになります。** 一致しなければ、どこかで間違えています。",
            "レビュー2: 2 つの見方がいつも一致するという主張")
not_in_text("この $2$ か所で決まることがほとんどです。$f$ の range と一致しているかどうかで、検算もできます",
            "レビュー2: Common errors 側の同じ主張")

# 8 — 反例の選び方（レビュー 11）
chk(f7.subs(x, 3) == f7.subs(x, -3) == 13, "演習8 f(3)=f(-3)=13")
chk(P.subs(x, -1) != P.subs(x, 1), "(x-3)^2-2 では ±1 は反例にならない")
in_text("**頂点をはさんで同じだけ離れた $2$ つ**を選びます")
not_in_text("$3$ と $-3$ のように、$0$ をはさんで対称な $2$ つを選んでください",
            "レビュー11: 頂点が 0 のときにしか使えない反例の選び方")

# 9 — 温度
c9 = sp.Rational(5, 9) * (x - 32)
k9 = x + sp.Rational(27315, 100)
kc = comp(k9, c9)
chk(c9.subs(x, 68) == 20, "演習9 68°F = 20°C")
chk(sp.nsimplify(kc.subs(x, 68)) == sp.Rational(29315, 100), "演習9 = 293.15 K")
chk(k9.subs(x, 0) == sp.Rational(27315, 100), "0°C = 273.15 K")
chk(sp.solve(sp.Eq(c9, 0), x) == [32], "32°F = 0°C")
in_text("\\frac{5}{9}(68-32) + 273.15 = \\frac{5}{9}(36) + 273.15 = 20 + 273.15 = 293.15")

# 10 — 誤答の指摘
in_text("To make the student's expression correct, the restriction must be $x \\geq 3$")
in_text("この生徒の式をそのまま使うなら、制限は $x \\geq 3$ でなければなりません")
not_in_text("**答えは「domain を $x \\geq 3$ に制限する必要がある」**です",
            "レビュー8: x<=3 を否定して読める書き方")
not_in_text("The domain of $f$ must be restricted, for example to $x \\geq 3$",
            "レビュー8: for example では生徒の式が正しくならない")

# ══════════════════════════════════════════════════════════
# 7. GDC の記述
# ══════════════════════════════════════════════════════════
in_text("menu → 1: Actions → 1: Define", "Define のメニュー位置")
in_text("ctrl + doc → 2: Add Graphs", "ページ追加のキー")
in_text("menu → Window/Zoom → Zoom - Square", "レビュー5: 目盛りをそろえる")
in_text("piecewise((x-3)^2-2,x≥3)", "レビュー3: 制限つきのグラフ")
in_text("TI 公式のヘルプでは、グラフの入力欄に `piecewise(3,x>-2 and x<2)` のように書く")
in_text("を選ぶと、入力欄に `Define` の文字が出ます", "レビュー13: Define の二重打ちを防ぐ")
in_text("合っている見込みが高いといえます。 画面に映っているのは".replace(" ", "")
        if False else "式が合っている見込みが高いといえます", "レビュー4: 断定しない")
in_text("Calculator ページの $x$ は「まだ何も入っていない文字」ですが", "レビュー12")
not_in_text("**$2$ 本が完全に重なれば、式が合っています。**", "レビュー4: 断定していた")
not_in_text("## 制限した domain は、電卓には映りません", "レビュー3: 制限は描けないという誤り")
not_in_text("$x \\geq 3$ の部分だけをかいてはくれません", "レビュー3: 同上")
# 非 CAS であることの断り
in_text("**TI-Nspire CX II は Numeric（非 CAS）です。**")
for cas in ["expand(", "factor(", "solve(", "csolve(", "Polar"]:
    not_in_text("`" + cas, "非 CAS では使えない命令 " + cas)

# ══════════════════════════════════════════════════════════
# 8. シラバス・公式集についての記述
# ══════════════════════════════════════════════════════════
in_text("Content 欄は $4$ 行です。")
in_text("Guidance 欄には $2$ 行あります。")
in_text("Connections 欄には、何も挙がっていません。")
in_text("Recommended teaching hours は $11$ 時間です。")
in_text("(f \\circ f^{-1})(x) = (f^{-1} \\circ f)(x) = x$.")
in_text("has an inverse if the domain is restricted to $x \\geq 3$ or to $x \\leq 3$")
chk(TEXT.count("> ") >= 6, "引用行が 6 行以上ある（Content 4 + Guidance 2）")
# 公式集にない、と言い切っている
in_text("## 公式集の AHL 2.7 の欄\n**ありません。**")
not_in_text("公式集に載っているので覚える必要はありません", "公式集にない項目で誤った安心を与えない")

# ══════════════════════════════════════════════════════════
# 9. 構造
# ══════════════════════════════════════════════════════════
heads = re.findall(r"(?m)^## (.+)$", TEXT)
need = ["What you should be able to do", "The idea", "Why it works",
        "Worked examples", "Common errors",
        "Using your GDC (TI-Nspire CX II)", "Exercises"]
for h in need:
    chk(h in heads, "見出しがない: " + h)
chk([h for h in heads if h in need] == need, "7 つの見出しの順序")

chk(len(re.findall(r"(?m)^---$", TEXT)) == 6, "--- は 6 個（front matter 2 + 例題 4）")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳は 14 個")
chk(TEXT.count("::: {.ex-sep}") == 9, ".ex-sep は 9 個")
chk(len(re.findall(r"::: \{#exm-ahl27-[\w-]+\}", TEXT)) == 4, "worked example は 4 個")
nums = re.findall(r"\[(\d+)\]\{\.ex-no\}", TEXT)
chk(nums == [str(i) for i in range(1, 11)], "演習は 1..10 の連番")

idea = re.findall(r"(?m)^### (\d+)\.", TEXT)
chk(idea == [str(i) for i in range(1, 9)] + [str(i) for i in range(1, 5)],
    "The idea 1..8 と GDC 1..4 の連番: " + str(idea))

# .model-answer が要る設問（Explain why / Interpret / Identify the error）
chk(TEXT.count("::: {.model-answer}") == 5, ".model-answer は 5 個")
for cmd in ["Explain why the finished photograph would be wider",
            "Explain why $f$ does not have an inverse",
            "Explain why the function $f(x) = x^{2}+4$ has no inverse",
            "Interpret the composite function",
            "Identify the error"]:
    in_text(cmd, "command term")

# 禁止表現
for w in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん", "当たり前",
          "確かめ。", "そのとおり"]:
    not_in_text(w, "禁止表現")
chk(TEXT.count("**検算。**") == 10, "検算。は 10 個: " + str(TEXT.count("**検算。**")))

# 用語は英語が先、日本語は括弧書き
for term in ["**composite function**（合成関数）",
             "**domain**（定義域）", "**range**（値域）",
             "**one-to-one**（$1$ 対 $1$）",
             "**horizontal line test**（水平線テスト）"]:
    in_text(term, "英語→日本語の順")

# 図
in_text("![Two machines in a row, and the two orders](img/ahl-2-7-composite.svg)")
in_text("![Why a restriction is needed, and what it fixes](img/ahl-2-7-inverse.svg)")
for svg in ["ahl-2-7-composite.svg", "ahl-2-7-inverse.svg"]:
    chk(os.path.exists(os.path.join(HERE, "..", "..", "ai-hl", "02-functions",
                                    "img", svg)), "図がある: " + svg)

# 交差参照（同一ページ内なので @ が使える）
for ref in ["@fig-ahl27-composite", "@fig-ahl27-inverse", "@eq-ahl27-notation",
            "@eq-ahl27-undo", "@eq-ahl27-example", "@tbl-ahl27-notation",
            "@tbl-ahl27-shop", "@tbl-ahl27-branch", "@exm-ahl27-basic",
            "@exm-ahl27-photo", "@exm-ahl27-find", "@exm-ahl27-restrict"]:
    in_text(ref, "交差参照")

# 他ページへは markdown リンク（@ は効かない）
chk("@sec-sl-2-2" not in TEXT, "他ページを @ で参照していない")
in_text("[SL 2.2](../../ai-sl/02-functions/sl-2-2.qmd#inverse)")
in_text("[SL 2.2](../../ai-sl/02-functions/sl-2-2.qmd#horizontal-test)")
in_text("[AHL 1.12a](../01-number-and-algebra/ahl-1-12a.qmd#quadratic)")

# 内部アンカーがすべて存在するか
anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT)) | {"common-errors"}
for a in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(a in anchors, "内部アンカーがない: #" + a)

# コードスパンの中に数式を入れていない
for m in re.findall(r"`[^`\n]*`", TEXT):
    chk("$" not in m, "コードスパンに $ が入っている: " + m[:50])

# 表のセルの中で | を裸で使っていない
for line in TEXT.split("\n"):
    if line.startswith("|") and "$" in line:
        chk("\\lvert" in line or "|" not in re.sub(r"^\||\|$", "", line).replace(" | ", ""),
            "表のセルの中の | :: " + line[:60])


# ══════════════════════════════════════════════════════════
#  2026-08 の修正
# ══════════════════════════════════════════════════════════
# 1. 逆関数との合成が成り立つ x の範囲
in_text("## $2$ つの式は、成り立つ $x$ の範囲が違います")
in_text("f^{-1}\\left(f(x)\\right) = x \\qquad (x \\in \\operatorname{Dom} f)")
in_text("f\\left(f^{-1}(x)\\right) = x \\qquad "
        "(x \\in \\operatorname{Range} f = \\operatorname{Dom} f^{-1})")
in_text("最初に $f$ へ入れるので、$x$ は **$f$ の domain** に入っていなければなりません")
in_text("最初に $f^{-1}$ へ入れるので、$x$ は **$f^{-1}$ の domain**、"
        "つまり **$f$ の range** に入っていなければなりません")
in_text("どちらの順でも、**使える範囲の中でなら**同じです。")
not_in_text("**$f$ で進んで $f^{-1}$ で戻れば、元の場所に返る。** どちらの順でも同じです。")
chk("{#eq-ahl27-undo1}" in TEXT and "{#eq-ahl27-undo2}" in TEXT,
    "2 つの向きの式にラベルが付いている")

# 範囲を外れると本当に計算できない: f(x)=(x-3)^2-2, x>=3 の逆は 3+sqrt(x+2)
# Range f = [-2, inf) なので、x = -5 では f^{-1} が定義されない
chk((-5) + 2 < 0, "x = -5 は Range f = [-2, ∞) の外なので f(f^-1(x)) が書けない")
chk(all(abs((3 + ((x + 2) ** 0.5)) - x) >= 0 for x in (-2, 0, 7)),
    "x >= -2 でだけ f^{-1}(x) が計算できる")
# f^{-1}(f(x)) = x は Dom f = [3, ∞) の中でだけ成り立つ
for _x in (3.0, 4.0, 7.0):
    chk(abs((3 + (((_x - 3) ** 2 - 2) + 2) ** 0.5) - _x) < 1e-12,
        "x=%g（Dom f の中）では f^{-1}(f(x)) = x" % _x)
for _x in (0.0, 2.0):
    chk(abs((3 + (((_x - 3) ** 2 - 2) + 2) ** 0.5) - _x) > 1e-6,
        "x=%g（Dom f の外）では f^{-1}(f(x)) ≠ x" % _x)

# 2. domain restriction を「左右に切る」と一般化しない
in_text("そこで、**この放物線では domain を頂点の左右どちらか一方に制限します。**")
in_text("この放物線では、$\\pm$ の片方だけを残すために、"
        "**domain を頂点の左右どちらか一方に制限します。**")
in_text("どこをどう制限するかは関数によって変わりますが、"
        "**「one-to-one になるまで domain を絞る」という目的は同じ**です。")
not_in_text("そこで **domain を片側だけに切ります。**", "一般化した言い方")
not_in_text("**もともとの $f$ の domain を片側に切っておく**しかありません",
            "一般化した言い方")
not_in_text("**切っていなければ、自分で切るしかありません。**", "一般化した言い方")


# レビューで追加: 参照先と、例題の domain 条件
in_text("[第5節](#inverse-recap)で見たとおり、$f^{-1}$ の domain は $f$ の range です。")
not_in_text("[第6節](#finding)で見たとおり、$f^{-1}$ の domain は $f$ の range です。")
in_text("- @eq-ahl27-undo1 … 最初に $f$ へ入れるので")
in_text("- @eq-ahl27-undo2 … 最初に $f^{-1}$ へ入れるので")
in_text("= \\frac{3}{\\frac{3}{x}} = x \\qquad (x \\neq 0)")
in_text("$x \\neq 0$ が付くのは、$f^{-1}$ の domain が $x \\neq 0$ だからです（@eq-ahl27-undo2）。")
in_text("（この等式が使えるのは、(b) で求めた $f^{-1}$ の domain、つまり $x \\neq 0$ の範囲です。@eq-ahl27-undo2）")
# f(x) = 3/(x-2) の range は y != 0 なので、f^{-1} の domain も x != 0
chk(all(abs(3 / (x - 2)) > 0 for x in (0.0, 1.0, 3.0, 100.0)),
    "f(x)=3/(x-2) は 0 を値に取らない → Range f は y≠0")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
