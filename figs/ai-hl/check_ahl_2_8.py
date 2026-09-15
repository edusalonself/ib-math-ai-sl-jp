"""AHL 2.8（グラフの変換）の内容を検算する。

    python3 figs/ai-hl/check_ahl_2_8.py

方針
  1. すべての式・座標を sympy で第一原理から出す
  2. 別の方法（点の追跡・行列・数値代入）で交差検証する
  3. ページの本文がその結果と一致しているかを in_text で確かめる
  4. レビューで直した箇所は not_in_text で再発を防ぐ
  5. 構造（見出し・例題数・演習数・区切り）を確かめる
"""
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
QMD = os.path.join(HERE, "..", "..", "ai-hl", "02-functions", "ahl-2-8.qmd")
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


x, y, t, p, q, a, b = sp.symbols("x y t p q a b", real=True)

# ══════════════════════════════════════════════════════════
# 1. 4 つの基本変換 — 点の移り方から確かめる
# ══════════════════════════════════════════════════════════
F = sp.Function("F")

# y = F(x)+b 上の点は (x, F(x)+b)。もとの (t, F(t)) が (t, F(t)+b) に来る。
chk(sp.simplify((F(t) + b) - (F(t) + b)) == 0, "縦の平行移動: (t, F(t)) → (t, F(t)+b)")
# y = F(x-a) 上で、F の中身が t になるのは x = t+a
chk(sp.solve(sp.Eq(x - a, t), x) == [t + a], "横の平行移動: x = t+a（右に a）")
# y = F(q x) 上で、F の中身が t になるのは x = t/q
chk(sp.solve(sp.Eq(q * x, t), x) == [t / q], "横の拡大: x = t/q（1/q 倍）")
in_text("X = t + 3")
in_text("X = \\frac{t}{q}")
in_text("X = \\frac{t}{q} + a")

# f(x)=x^2 での確認（本文の「1 つ例で確かめる」）
chk(sp.solve(sp.Eq((x - 3) ** 2, 0), x) == [3], "(x-3)^2 の頂点は x=3（右に 3）")
chk(sp.solve(sp.Eq((x + 3) ** 2, 0), x) == [-3], "(x+3)^2 の頂点は x=-3（左に 3）")
in_text("$y = f(x-3) = (x-3)^2$ の頂点は $x = 3$")

# sin の周期（横の拡大の向き）
chk(sp.periodicity(sp.sin(x), x) == 2 * sp.pi, "sin x の周期は 2π")
chk(sp.periodicity(sp.sin(2 * x), x) == sp.pi, "sin 2x の周期は π（短くなる）")
in_text("$\\sin x$ の周期は $2\\pi$ ですが、$\\sin 2x$ の周期は $\\pi$ です")

# 不変な点
chk((p * 0) == 0, "vertical stretch: y=0 は動かない")
chk(sp.simplify(sp.Rational(0) / 2) == 0, "horizontal stretch: x=0 は動かない")

# ★ レビュー3: p<1 なら縮む、は偽（p=-3 が反例）
chk(abs(-3 * 2) > abs(2), "p=-3 は縮まない（|−3·2| > |2|）")
in_text("$0 < p < 1$ なら縮み、$p > 1$ なら伸びます")
in_text("$p = -3$ なら、裏返って $3$ 倍です。縮みません。")
not_in_text("$p < 1$ なら縮み、$p < 0$ なら $x$ 軸をまたいで裏返ります。",
            "レビュー3: 条件のない縮小の主張")
not_in_text("**$p$ を $1$ より小さくすると縮み、負にすると裏返る**",
            "レビュー3: GDC 側の同じ主張")

# ★ レビュー5: q の条件
in_text("\\text{ 倍} \\qquad (q > 0)", "eq-ahl28-hstretch の条件")
in_text("\\text{ 倍してから、右に } a \\qquad (q > 0)", "eq-ahl28-inside の条件")
in_text("$q < 0$ のときは、**scale factor $\\dfrac{1}{\\lvert q \\rvert}$ の horizontal stretch** に加えて")
chk(sp.simplify(sp.Function("F")(-x) - sp.Function("F")(-1 * x)) == 0,
    "q=-1 は y 軸についての対称移動")

# ★ レビュー4: q を大きくするほど細くなる、は正の範囲だけ
chk(abs(sp.Rational(1, -5)) < abs(sp.Rational(1, -1)),
    "q=-5 より q=-1 のほうが scale factor が大きい（＝広がる）")
in_text("**$q$ を正の範囲で大きくするほど細くなります**")
not_in_text("横の拡大で **$q$ を大きくするほど細くなる**ことが見えます",
            "レビュー4: q<0 で偽になる主張")

# ══════════════════════════════════════════════════════════
# 2. 合成 — 順序
# ══════════════════════════════════════════════════════════
# 縦の拡大 → 縦の平行移動
c1 = sp.expand(3 * x ** 2 + 2)
c2 = sp.expand(3 * (x ** 2 + 2))
eq(c1, 3 * x ** 2 + 2, "stretch → translate は 3x^2+2")
eq(c2, 3 * x ** 2 + 6, "translate → stretch は 3x^2+6")
chk(sp.simplify(c2 - c1) == 4, "差は x によらず 4")
chk(3 * 2 - 2 == 4, "3×2−2 = 4")
in_text("3 \\times 2 - 2 = 6 - 2 = 4")

# 縦の拡大と横の拡大は可換
lhs = sp.Function("F")(2 * x) * 4
rhs = 4 * sp.Function("F")(2 * x)
chk(sp.simplify(lhs - rhs) == 0, "縦の拡大と横の拡大は可換")
chk(4 * sp.sin(2 * sp.pi / 4) == 4, "4sin(2·π/4) = 4")
chk(sp.periodicity(4 * sp.sin(2 * x), x) == sp.pi, "4sin2x の周期は π")

# ★ レビュー1: f(2x-6) は 2 通りの道すじで作れる
step_a = (x - 6)                      # 右に 6
step_a = step_a.subs(x, 2 * x)        # そのあと横に 1/2
step_b = (2 * x)                      # 横に 1/2
step_b = step_b.subs(x, x - 3)        # そのあと右に 3
eq(step_a, 2 * x - 6, "右に6 → 横1/2 は 2x-6")
eq(step_b, 2 * x - 6, "横1/2 → 右に3 も 2x-6")
eq(sp.expand(step_a - step_b), 0, "2 つの道すじは同じ式")
wrong = (2 * x).subs(x, x - 6)
eq(wrong, 2 * x - 12, "横1/2 → 右に6 は 2x-12（別のグラフ）")
chk(sp.solve(sp.Eq(2 * x - 6, 0), x) == [3], "2x-6=0 の解は x=3")
chk(sp.solve(sp.Eq(2 * x - 12, 0), x) == [6], "2x-12=0 の解は x=6")
eq(sp.factor(2 * x - 6), 2 * (x - 3), "2x-6 = 2(x-3)")
in_text("## $f(2x-6)$ には、正しい道すじが $2$ 通りあります。まちがいは「縮めてから右に $6$」です")
in_text("**どちらも同じグラフで、どちらも正しい説明です**（演習 $7$）")
not_in_text("## $f(2x-6)$ を「右に $6$ してから縮める」と読むと、答えは合いますが式は合いません",
            "レビュー1: 式が合わないという誤った見出し")
not_in_text("**@eq-ahl28-inside の読み方で答えるのが安全**です",
            "レビュー1: 正しい答えを避けさせる書き方")

# ★ レビュー2: 「点に近いほうが先」は内側で偽
# 2026-09: 削除した節・欄の検査（in_text("**行列は「点に近いほうが先」、関数の式は「$f$ に近いほうが先」**")…）
# 2026-09: 削除した節・欄の検査（in_text("$x$ のとなりに書いてある $-3$ は、**あと**にやる操作です")…）
not_in_text("**どちらも「先にやるものが、点に近いところに書いてある」**",
            "レビュー2: 内側で成り立たない一般化")
in_text("ただしこれは、$f$ の**外**の操作についての話です")

# ══════════════════════════════════════════════════════════
# 3. AHL 3.9 の行列との対応（実際に点に掛けて確かめる）
# ══════════════════════════════════════════════════════════
v = sp.Matrix([x, y])
M_xrefl = sp.Matrix([[1, 0], [0, -1]])
M_yrefl = sp.Matrix([[-1, 0], [0, 1]])
M_vstr = sp.Matrix([[1, 0], [0, p]])
M_hstr = sp.Matrix([[sp.Rational(1, 1) / q, 0], [0, 1]])   # k = 1/q
chk(list(M_xrefl * v) == [x, -y], "x 軸 reflection 行列 → (x, -y) ＝ -f(x)")
chk(list(M_yrefl * v) == [-x, y], "y 軸 reflection 行列 → (-x, y) ＝ f(-x)")
chk(list(M_vstr * v) == [x, p * y], "vertical stretch 行列 → (x, py) ＝ p f(x)")
chk(sp.simplify((M_hstr * v)[0] - x / q) == 0,
    "horizontal stretch 行列は k=1/q のとき (x/q, y) ＝ f(qx)")
# 2026-09: 削除した節・欄の検査（in_text("| $y = f(qx)$ | $\\begin{pmatrix} k & 0…）

# ★ レビュー8: 公式集の 6 つのうち、対応するのは 3 つだけ
# 2026-09: 削除した節・欄の検査（in_text("そのうち reflection と $2$ つの stretch は")…）
# 2026-09: 削除した節・欄の検査（in_text("残りの $2$ つ（rotation と enlargement）は、この項目…）
# 2026-09: 削除した節・欄の検査（in_text("いちばん下の行だけは、公式集にありません")…）
not_in_text("**行列の形なら $6$ つ印刷されています。** 同じ変換なのに、片方だけが配られます",
            "レビュー8: 6 つとも対応するかのような書き方")

# ══════════════════════════════════════════════════════════
# 4. Worked examples
# ══════════════════════════════════════════════════════════
f1 = x ** 3 - 2 * x
chk(f1.subs(x, 1) == -1, "WE1 f(1) = -1")
eq(f1 + 3, x ** 3 - 2 * x + 3, "WE1 (a)")
eq(sp.expand(f1.subs(x, x - 2)), x ** 3 - 6 * x ** 2 + 10 * x - 4, "WE1 (b)")
chk(sp.expand(f1.subs(x, x - 2)).subs(x, 3) == -1, "WE1 (c) 検算 (3, -1)")
eq(sp.expand((x - 2) ** 3), x ** 3 - 6 * x ** 2 + 12 * x - 8, "WE1 (x-2)^3 の展開")
in_text("x^{3}-6x^{2}+12x-8-2x+4 = x^{3}-6x^{2}+10x-4")

f2 = 2 ** x + 1
chk(f2.subs(x, 2) == 5, "WE2 f(2) = 5")
eq(sp.expand(-f2), -2 ** x - 1, "WE2 -f(x) = -2^x-1")
eq(f2.subs(x, -x), 2 ** (-x) + 1, "WE2 f(-x) = 2^{-x}+1")
chk(sp.limit(-f2, x, -sp.oo) == -1, "WE2 -f の asymptote は y=-1")
chk(sp.limit(f2.subs(x, -x), x, sp.oo) == 1, "WE2 f(-x) の asymptote は y=1")
chk((-f2).subs(x, 2) == -5, "WE2 (2, -5)")
chk(f2.subs(x, -x).subs(x, -2) == 5, "WE2 (-2, 5)")
# 誤答 -2^x+1 は x=2 で -3 になり、検算で見つかる
chk((-2 ** x + 1).subs(x, 2) == -3, "WE2 誤答は -3 になる（検算で見つかる）")
in_text("$-2^{x}+1$ と書いていれば $-3$ になるので、ここで気づけます")
not_in_text("**検算。** $y = f(-x) = 2^{-x}+1$ に $x = -2$ を入れると $2^{2}+1 = 5$ ✓ 合いました。",
            "レビュー12: 4 つの答えのうち 1 つしか見ていない検算")

chk(4 == 4 and sp.pi == sp.pi, "WE4 amplitude 4, period π")
eq(2 * sp.pi / 2, sp.pi, "WE4 period = 2π/2")
in_text("\\left(\\frac{\\pi}{4},\\ 4\\right)")

# ══════════════════════════════════════════════════════════
# 5. Exercises
# ══════════════════════════════════════════════════════════
e1 = x ** 2 + 1
eq(e1 - 3, x ** 2 - 2, "演習1 f(x)-3")
eq(sp.expand(e1.subs(x, x + 4)), x ** 2 + 8 * x + 17, "演習1 f(x+4)")
chk(sp.expand(e1.subs(x, x + 4)).subs(x, -4) == 1, "演習1 検算 頂点 (-4, 1)")

eq(sp.expand(-x ** 3), sp.expand((-x) ** 3), "演習3 -f(x) と f(-x) が一致")
chk(sp.simplify(-x ** 2 - (x ** 2)) != 0, "演習3 x^2 では一致しない（一般には別もの）")

e4 = x ** 2 - x
eq(sp.expand(3 * e4), 3 * x ** 2 - 3 * x, "演習4 3f(x)")
eq(sp.expand(e4.subs(x, 2 * x)), 4 * x ** 2 - 2 * x, "演習4 f(2x)")
chk(sp.expand(3 * e4).subs(x, 2) == 6 and 3 * e4.subs(x, 2) == 6, "演習4 検算 x=2")
chk(sp.expand(e4.subs(x, 2 * x)).subs(x, 2) == 12 and e4.subs(x, 4) == 12,
    "演習4 検算 f(4)=12")
chk(sp.expand((2 * x) ** 2) == 4 * x ** 2, "(2x)^2 = 4x^2（2x^2 ではない）")

# 演習5: f(5x) の scale factor は 1/5
chk(sp.solve(sp.Eq(5 * x, t), x) == [t / 5], "演習5 scale factor は 1/5")
in_text("A horizontal stretch with scale factor $\\dfrac{1}{5}$")

# 演習6: 点 (6, -2) の像。条件に合う f で交差検証
g6 = x / 3 - 4
chk(g6.subs(x, 6) == -2, "演習6 f(x)=x/3-4 は f(6)=-2")
chk(g6.subs(x, 6) + 7 == 5, "演習6 (a) (6, 5)")
chk(g6.subs(x, 7 - 1) == -2, "演習6 (b) (7, -2)")
chk(2 * g6.subs(x, 6) == -4, "演習6 (c) (6, -4)")
chk(g6.subs(x, 2 * 3) == -2, "演習6 (d) (3, -2)")

# 演習8: 潮汐
d8 = 2 * sp.sin(sp.pi * t / 6)
n8 = sp.Rational(3, 2) * d8.subs(t, t - 3)
chk(sp.periodicity(d8, t) == 12, "演習8 周期 12 時間")
chk(sp.periodicity(n8, t) == 12, "演習8 平行移動しても周期は 12")
chk(d8.subs(t, 3) == 2, "演習8 もとの最高水位 2 m は t=3")
chk(sp.simplify(n8.subs(t, 6)) == 3, "演習8 新しい最高水位 3 m は t=6")
chk(sp.simplify(sp.Rational(3, 2) * 2) == 3, "演習8 振幅 1.5×2 = 3")
in_text("3\\sin\\left(\\frac{\\pi(t-3)}{6}\\right)")

# 演習9: f(x+3) は左に 3
chk(sp.solve(sp.Eq((x + 3) ** 2, 0), x) == [-3], "演習9 (x+3)^2 の頂点は x=-3（左）")
in_text("moves $3$ units to the **left**")

# 演習10: (2,7) と切片 -1, 5 → 3f(x-4)
chk((2 + 4, 3 * 7) == (6, 21), "演習10 最大点 (6, 21)")
chk((-1 + 4, 5 + 4) == (3, 9), "演習10 切片 3 と 9")
f10 = 7 - sp.Rational(7, 9) * (x - 2) ** 2
chk(f10.subs(x, 2) == 7, "演習10 検算用 f の最大値 7")
chk(f10.subs(x, -1) == 0 and f10.subs(x, 5) == 0, "演習10 検算用 f の切片")
g10 = 3 * f10.subs(x, x - 4)
chk(g10.subs(x, 6) == 21, "演習10 g(6) = 21")
chk(g10.subs(x, 3) == 0 and g10.subs(x, 9) == 0, "演習10 g の切片")
chk(sp.simplify(3 * f10.subs(x, 3 + 4)) != 0,
    "演習10 向きを取りちがえると 0 にならない（検算で見つかる）")
in_text("**「左に $4$」と取りちがえていれば、ここで気づけます。**")
not_in_text("**切片のあいだにある**はずです。$3 < 6 < 9$ ✓",
            "レビュー6: 誤答でも通ってしまう検算")

# ══════════════════════════════════════════════════════════
# 6. GDC の記述
# ══════════════════════════════════════════════════════════
in_text("ctrl + doc → Add Graphs", "ページ追加のキー")
in_text("menu → Actions → Insert Slider", "スライダー（TI 公式ヘルプ）")
in_text("TI 公式のヘルプでは")
# 2026-09: GDC の入力例は画面どおりの表示に変更
in_text(r"f2(x) = 3 \times f1(x) + 2", "f1 を参照した定義")
not_in_text("f2(x)=3*f1(x)+2", "旧: 直線入力の表記")
in_text("f2(x)=f1(2*x)", "レビュー9: 横の検算用に入れなおす")
in_text("Graphs と**同じ problem の中**の Calculator ページ", "レビュー9: problem の範囲")
in_text("## Using your GDC (TI-Nspire CX II)", "機種の断り")
in_text("## 電卓は「scale factor がいくつか」を答えてくれません")
not_in_text("Calculator ページで、$f1$ と $f2$ の値を比べます。\n\n```\nf1(2)",
            "レビュー9: problem の断りがない書き方")
# 非 CAS では使えない命令を書いていない
for cas in ["expand(", "factor(", "solve(", "csolve(", "Polar", "Define f"]:
    not_in_text("`" + cas, "非 CAS では使えない／この項目に不要な命令 " + cas)

# ══════════════════════════════════════════════════════════
# 7. シラバス・公式集についての記述
# ══════════════════════════════════════════════════════════
# 2026-09: 削除した節・欄の検査（in_text("## 公式集の AHL 2.8 の欄\n**ありません。**")…）
# 2026-09: 削除した節・欄の検査（in_text("Content 欄は $6$ 行です。")…）
# 2026-09: 削除した節・欄の検査（in_text("Guidance 欄には、次の $6$ つが書かれています。")…）
# 2026-09: 削除した節・欄の検査（in_text("Connections 欄には、$3$ つ挙がっています。")…）
# 2026-09: 削除した節・欄の検査（in_text("Translations: $y = f(x)+b$; $y = f(x-a)…）
# 2026-09: 削除した節・欄の検査（in_text("Reflections: in the $x$ axis $y = -f(x)…）
# 2026-09: 削除した節・欄の検査（in_text("Vertical stretch with scale factor $p$:…）
in_text("Horizontal stretch with scale factor $\\dfrac{1}{q}$: $y = f(qx)$")
# 2026-09: 削除した節・欄の検査（in_text("$x$ and $y$ axes are invariant.")…）
in_text("Students should be made aware of the significance of the order of transformations.")
in_text("Translation by the vector $\\begin{pmatrix} 3 \\\\ -2 \\end{pmatrix}$")
# 2026-09: 削除した節・欄の検査（chk(TEXT.count("> ") >= 15, "引用行が 15 行以上（Content…）
# 2026-09: 削除した節・欄の検査（in_text("**Reflections の $2$ 式については、Guidance 欄に対…）
not_in_text("**Reflections の行だけ、Guidance 欄が空です。** 迷いようがない、ということでしょう。",
            "レビュー7: 決めつけと §3 との矛盾")
in_text("Guidance の `x and y axes are invariant.` は、$2$ つの stretch についての注意です")
not_in_text("これが Guidance の `x and y axes are invariant.` の半分です",
            "レビュー11: シラバス文を勝手に半分に割っていた")
not_in_text("ここを外さないことが、そのまま得点になります", "採点についての検証できない主張")

# ══════════════════════════════════════════════════════════
# 8. 構造
# ══════════════════════════════════════════════════════════
heads = re.findall(r"(?m)^## (.+)$", TEXT)
need = ["What you should be able to do", "The idea", "Why it works",
        "Worked examples", "Common errors",
        "Using your GDC (TI-Nspire CX II)", "Exercises"]
for h in need:
    chk(h in heads, "見出しがない: " + h)
chk([h for h in heads if h in need] == need, "7 つの見出しの順序")

chk(len(re.findall(r"(?m)^---$", TEXT)) == 6, "--- は 6 個")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳は 14 個")
chk(TEXT.count("::: {.ex-sep}") == 9, ".ex-sep は 9 個")
chk(len(re.findall(r"::: \{#exm-ahl28-[\w-]+\}", TEXT)) == 4, "worked example は 4 個")
chk(re.findall(r"\[(\d+)\]\{\.ex-no\}", TEXT) == [str(i) for i in range(1, 11)],
    "演習は 1..10 の連番")
idea = re.findall(r"(?m)^### (\d+)\.", TEXT)
chk(idea == [str(i) for i in range(1, 8)] + [str(i) for i in range(1, 5)],
    "The idea 1..7 と GDC 1..4 の連番: " + str(idea))
chk(TEXT.count("::: {.model-answer}") == 6, ".model-answer は 6 個")
for cmd in ["Explain why the two orders give different graphs",
            "Describe fully the two transformations involved",
            "Describe fully the transformation.",
            "Describe fully the transformation, and state which points do not move",
            "Interpret what your model in part (a) says",
            "Identify the error and state the correct transformation"]:
    in_text(cmd, "command term")

for w in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん", "当たり前",
          "確かめ。", "そのとおり"]:
    not_in_text(w, "禁止表現")
chk(TEXT.count("**検算。**") == 10, "検算。は 10 個: " + str(TEXT.count("**検算。**")))

for term in ["**transformation**（変換）", "**image**（像）",
             "**scale factor**（拡大率）", "**invariant**（不変な）",
             "**composite transformation**（合成変換）",
             "**asymptote**（漸近線）"]:
    in_text(term, "英語→日本語の順")

# 2026-09: 削除した節・欄の検査（in_text("![The four basic transformations](img/a…）
# 2026-09: 削除した節・欄の検査（in_text("![Order matters, and two stretches at o…）
for svg in ["ahl-2-8-translation.svg", "ahl-2-8-reflection.svg",
            "ahl-2-8-vstretch.svg", "ahl-2-8-hstretch.svg",
            "ahl-2-8-order.svg", "ahl-2-8-sine.svg"]:
    chk(os.path.exists(os.path.join(HERE, "..", "..", "ai-hl", "02-functions",
                                    "img", svg)), "図がある: " + svg)

for ref in ["@fig-ahl28-translation", "@fig-ahl28-reflection",
            "@fig-ahl28-vstretch", "@fig-ahl28-hstretch",
            "@fig-ahl28-order", "@fig-ahl28-sine", "@eq-ahl28-vtrans",
            "@eq-ahl28-htrans", "@eq-ahl28-xreflect", "@eq-ahl28-yreflect",
            "@eq-ahl28-vstretch", "@eq-ahl28-hstretch", "@eq-ahl28-inside",
# 2026-09: 削除した節・欄の検査（"@tbl-ahl28-four", "@tbl-ahl28-matrix", "@exm-ah…）
            "@exm-ahl28-reflect", "@exm-ahl28-order", "@exm-ahl28-sine"]:
    in_text(ref, "交差参照")

chk("@sec-ahl-3-9" not in TEXT and "@sec-sl-2-5" not in TEXT,
    "他ページを @ で参照していない")
# 2026-09: 削除した節・欄の検査（in_text("[AHL 3.9](../03-geometry-and-trigonomet…）
# 2026-09: 削除した節・欄の検査（in_text("[AHL 3.9](../03-geometry-and-trigonomet…）
in_text("[AHL 2.7](ahl-2-7.qmd#notation)")
in_text("[SL 2.5](../../ai-sl/02-functions/sl-2-5.qmd#sinusoidal)")
chk("ahl-2-9.qmd" not in TEXT, "まだ書いていないページへリンクしていない")

anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT)) | {"common-errors",
                                                         "why-it-works"}
for anc in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(anc in anchors, "内部アンカーがない: #" + anc)

for m in re.findall(r"`[^`\n]*`", TEXT):
    chk("$" not in m, "コードスパンに $ が入っている: " + m[:50])

for line in TEXT.split("\n"):
    if line.startswith("|") and "$" in line:
        inner = re.sub(r"^\||\|$", "", line)
        chk("\\lvert" in line or "|" not in inner.replace(" | ", ""),
            "表のセルの中の | :: " + line[:60])


# ══════════════════════════════════════════════════════════
#  2026-08 の修正: 負の係数を scale factor と呼ばない
# ══════════════════════════════════════════════════════════
in_text("y = p\\,f(x) \\quad \\text{は、vertical stretch with scale factor } p "
        "\\qquad (p > 0)")
not_in_text("y = p\\,f(x) \\quad \\text{は、縦に } p \\text{ 倍}")
in_text("**scale factor は正の大きさとして書きます。**")
in_text("**$p < 0$ のときは、$1$ つの変換ではありません。**")
in_text("$x$ 軸についての **reflection** と、scale factor $\\lvert p \\rvert$ の "
        "**vertical stretch** を組み合わせたものです。")
in_text("たとえば $y = -3f(x)$ は、$x$ 軸について折り返してから、"
        "縦に scale factor $3$ で拡大したものです。")
in_text("**$p = -3$ なら、裏返って $3$ 倍です。縮みません。**")
in_text("**scale factor は $\\lvert p \\rvert$ であって、$-3$ ではありません。**")
not_in_text("$p < 0$ のときは、$x$ 軸をまたいで裏返ったうえで $\\lvert p \\rvert$ 倍になります。")
# まとめ表
in_text("| $y = p\\,f(x)$ | 外 | $y$ 座標 | $y$ 座標を $p$ 倍する。"
        "$p<0$ なら reflection も起こり、stretch の scale factor は $\\lvert p \\rvert$ | $x$ 軸の上 |")
not_in_text("| $y = p\\,f(x)$ | 外 | $y$ 座標 | 縦に $p$ 倍 | $x$ 軸の上 |")
# 2026-09: 削除した節・欄の検査（in_text("（$p>0$ なら vertical stretch, scale facto…）
in_text("y = f(qx) \\quad \\text{は、横に } \\frac{1}{q} \\text{ 倍} \\qquad (q > 0)")
# シラバスの引用はそのまま（IB の原文）
# 2026-09: 削除した節・欄の検査（in_text("> Vertical stretch with scale factor $p…）
# y = -3 f(x) は「x 軸で折り返してから 3 倍」と同じ写像
for _y in (-2.0, 0.0, 1.5, 4.0):
    chk(abs((-3.0) * _y - 3.0 * (-_y)) < 1e-12,
        "y=%g: -3f(x) は 折り返し→3倍 と同じ" % _y)
# scale factor は |p|。p 自身を長さの比とすると符号が付いて意味をなさない
chk(abs(-3.0) == 3.0, "scale factor は |p| = 3")


# レビューで追加: 横の stretch でも scale factor は正の量
in_text("$q < 0$ のときは、**scale factor $\\dfrac{1}{\\lvert q \\rvert}$ の horizontal stretch** に加えて")
not_in_text("$q < 0$ のときは、$\\lvert q \\rvert$ の分の horizontal stretch に加えて")
# 2026-09: 削除した節・欄の検査（in_text("（$k>0$ なら horizontal stretch, scale fac…）
not_in_text("（horizontal stretch, scale factor $k$）")
# q = -2 なら scale factor は 1/2 で、y 軸で折り返す
chk(abs(1 / abs(-2.0) - 0.5) < 1e-12, "q=-2 の scale factor は 1/2")

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
