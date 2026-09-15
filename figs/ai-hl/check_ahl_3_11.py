"""AHL 3.11（直線のベクトル方程式）の内容を検算する。

    python3 figs/ai-hl/check_ahl_3_11.py
"""
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "..", "..", "ai-hl", "03-geometry-and-trigonometry")
QMD = os.path.join(BASE, "ahl-3-11.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_ahl_3_11.py"), encoding="utf-8").read()

OK = NG = 0


def chk(cond, msg):
    global OK, NG
    if cond:
        OK += 1
    else:
        NG += 1
        print("NG :", msg)


def vec(*a):
    return sp.Matrix(list(a))


def same(u, v, msg=""):
    chk(sp.simplify(u - v) == sp.zeros(*u.shape), msg + f"  ({list(u)} vs {list(v)})")


def differ(u, v, msg=""):
    chk(sp.simplify(u - v) != sp.zeros(*u.shape), msg + f"  ({list(u)} vs {list(v)})")


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている（直したはず）: " + msg + " :: " + sub[:70])


lam, mu = sp.symbols("lambda mu")


def line(a, b, p):
    return vec(*a) + p * vec(*b)


def on_line(a, b, P):
    """点 P が直線 a+λb 上にあるか。1 成分から λ を出し、全成分で確かめる。"""
    a, b, P = vec(*a), vec(*b), vec(*P)
    for i in range(len(b)):
        if b[i] != 0:
            k = sp.Rational(P[i] - a[i], b[i])
            return sp.simplify(a + k * b - P) == sp.zeros(len(b), 1), k
    return None, None


# ══════════════════════════════════════════════════════════
# 1. 主例の直線 r = (1,2) + λ(3,-1)
# ══════════════════════════════════════════════════════════
A0, B0 = (1, 2), (3, -1)
for p, pt in [(-1, (-2, 3)), (0, (1, 2)), (1, (4, 1)), (2, (7, 0))]:
    same(line(A0, B0, p), vec(*pt), f"λ={p} の点")
    in_text("$(%d,\\ %d)$" % pt, f"λ={p} の点が表にある")
# λ が 1 増えると b だけ動く
same(line(A0, B0, 1) - line(A0, B0, 0), vec(*B0), "λ が 1 増えると b だけ動く")
in_text("**$\\lambda$ が $1$ 増えるごとに、$\\mathbf{b}$ だけ動きます。**", "その説明")
# 直交座標形 x+3y=7 と傾き -1/3
for p in (-1, 0, 1, 2, sp.Rational(1, 2)):
    P = line(A0, B0, p)
    chk(sp.simplify(P[0] + 3 * P[1] - 7) == 0, f"x+3y=7 が λ={p} で成り立つ")
chk(sp.Rational(-1, 3) == sp.Rational(B0[1], B0[0]), "傾きは b の たて/よこ")
in_text("x + 3y = 7", "直交座標形")
# 垂直な direction では y=mx+c にならない（見出しが直したことの確認）
in_text("## $2$ 次元なら、$\\lambda$ を消して直線の式に戻せます", "見出しが y=mx+c を約束していない")
not_in_text("## $2$ 次元なら、$\\lambda$ を消して $y = mx + c$ に戻せます", "古い見出し")
in_text("縦向きの直線では傾きが定まりません", "縦向きの例外を書いている")

# ══════════════════════════════════════════════════════════
# 2. 同じ直線を別の式で書く
# ══════════════════════════════════════════════════════════
A1, B1 = (7, 0), (-6, 2)
same(vec(*B1), -2 * vec(*B0), "方向ベクトルは -2 倍")
ok, k = on_line(A0, B0, A1)
chk(ok and k == 2, "(7,0) は λ=2 で主例の直線上")
# μ を動かすと同じ点集合になる（数値で確認）
# μ の点は、λ = 2 - 2μ の点と一致する（代数的に確認）
chk(sp.simplify(vec(*A1) + mu * vec(*B1) - (vec(*A0) + (2 - 2 * mu) * vec(*B0)))
    == sp.zeros(2, 1), "2 つ目の式の点は、すべて 1 つ目の直線上（λ = 2-2μ）")
for m_ in (-2, sp.Rational(-1, 3), 0, sp.Rational(3, 4), 5):
    okm, _ = on_line(A0, B0, tuple(line(A1, B1, m_)))
    chk(okm, f"μ={m_} の点は 1 つ目の直線上")

# ══════════════════════════════════════════════════════════
# 3. 例題の数値
# ══════════════════════════════════════════════════════════
# 例題 1: A(2,-1), B(6,1), C(10,3)
PA, PB, PC = (2, -1), (6, 1), (10, 3)
same(vec(*PB) - vec(*PA), vec(4, 2), "例題1(a) AB")
same(line(PA, (4, 2), 0), vec(*PA), "λ=0 で A")
same(line(PA, (4, 2), 1), vec(*PB), "λ=1 で B")
ok, k = on_line(PA, (4, 2), PC)
chk(ok and k == 2, "例題1(d) C は λ=2 で線上")
# a と b を取りちがえた誤りは、λ=0 で捕まる
same(line((4, 2), (2, -1), 0), vec(4, 2), "取りちがえた式の λ=0 は (4,2)")
differ(line((4, 2), (2, -1), 0), vec(*PA), "それは A ではない")
in_text("$\\lambda = 0$ で $(4,\\ 2)$ になり、$A$ に戻りません", "その誤りを名指ししている")
# b に B の位置ベクトルを使う誤りは λ=0 では捕まらず、λ=1 で捕まる
same(line(PA, PB, 0), vec(*PA), "b に B を使っても λ=0 は A になってしまう")
differ(line(PA, PB, 1), vec(*PB), "λ=1 なら捕まる")
same(line(PA, PB, 1), vec(8, 0), "その誤答は (8,0)")
in_text("$\\lambda = 0$ だけだと、$\\mathbf{b}$ に $B$ の位置ベクトルを使ってしまった誤りを見落とします。",
        "検算の限界を書いている")
not_in_text("**$\\mathbf{a}$ と $\\mathbf{b}$ の取りちがえは、これで必ず見つかります。**",
            "言いすぎの古い書き方")

# 例題 2: 3 次元
A2, B2 = (1, 2, -3), (2, -1, 4)
same(line(A2, B2, 3), vec(7, -1, 9), "例題2(a)")
okP, kP = on_line(A2, B2, (5, 0, 1))
chk(not okP and kP == 2, "P(5,0,1) は線上にない（λ=2 で z が合わない）")
same(line(A2, B2, 2), vec(5, 0, 5), "λ=2 の点は (5,0,5)")
chk(line(A2, B2, 2)[1] == 0, "y だけは合ってしまう（意地悪なところ）")
okQ, kQ = on_line(A2, B2, (-3, 4, -11))
chk(okQ and kQ == -2, "Q(-3,4,-11) は λ=-2 で線上")
# 例題 2 の検算：点から a を引くと b のスカラー倍
d = vec(7, -1, 9) - vec(*A2)
same(d, 3 * vec(*B2), "例題2 の検算（差が b の 3 倍）")
dw = vec(7, -1, 15) - vec(*A2)          # z を 15 と誤った答え
chk(sp.simplify(dw - 3 * vec(*B2)) != sp.zeros(3, 1),
    "誤答 z=15 は b のスカラー倍にならない")
same(dw, vec(6, -3, 18), "その差は (6,-3,18)")
in_text("$\\begin{pmatrix} 6 \\\\ -3 \\\\ 18 \\end{pmatrix}$ になり、$\\mathbf{b}$ のスカラー倍になりません",
        "その誤りを名指ししている")

# 例題 4: 交点
La, Lb = (1, 2), (3, -1)
Ma, Mb = (2, -3), (1, 2)
sol = sp.solve([La[0] + lam * Lb[0] - (Ma[0] + mu * Mb[0]),
                La[1] + lam * Lb[1] - (Ma[1] + mu * Mb[1])], [lam, mu])
chk(sol[lam] == 1 and sol[mu] == 2, "例題4 λ=1, μ=2")
same(line(La, Lb, 1), vec(4, 1), "例題4 の交点（L1 から）")
same(line(Ma, Mb, 2), vec(4, 1), "例題4 の交点（L2 から）")
chk(sol[lam] != sol[mu], "λ と μ は一致しない")
chk(Lb[0] * Mb[1] - Lb[1] * Mb[0] != 0, "例題4 の 2 直線は平行でない")
in_text("$\\lambda = 1$ に、$L_2$ では $\\mu = 2$".replace("$\\lambda = 1$ に、", "$\\lambda = 1$、"),
        "交点での 2 つの値が違うと書いている")
# 同じ文字にすると解が無い
chk(sp.solve([La[0] + lam * Lb[0] - (Ma[0] + lam * Mb[0]),
              La[1] + lam * Lb[1] - (Ma[1] + lam * Mb[1])], [lam]) == [],
    "同じ文字にすると解が無くなる（交点を見落とす）")

# ══════════════════════════════════════════════════════════
# 4. 演習の数値
# ══════════════════════════════════════════════════════════
E1a, E1b = (4, -1), (2, 5)
for p, pt in [(0, (4, -1)), (1, (6, 4)), (-2, (0, -11))]:
    same(line(E1a, E1b, p), vec(*pt), f"演習1 λ={p}")
same(line(E1a, E1b, 1) - line(E1a, E1b, 0), vec(*E1b), "演習1 の検算 1")
same(line(E1a, E1b, -2) - line(E1a, E1b, 0), -2 * vec(*E1b), "演習1 の検算 2")
chk(sp.simplify((vec(0, 9) - vec(*E1a)) - (-2) * vec(*E1b)) != sp.zeros(2, 1),
    "演習1 の検算は -11 を 9 とした誤りを捕まえる")

E2a, E2b = (-3, 5, 2), (1, -4, 6)
same(line(E2a, E2b, 1), vec(-2, 1, 8), "演習2 の検算（λ=1）")
in_text("x = -3+\\lambda, \\qquad y = 5-4\\lambda, \\qquad z = 2+6\\lambda",
        "演習2 の parametric form")

P3, Q3 = (1, 3), (5, -1)
same(vec(*Q3) - vec(*P3), vec(4, -4), "演習3 PQ")
same(line(P3, (4, -4), 1), vec(*Q3), "演習3 の検算")
okq, kq = on_line(P3, (1, -1), Q3)
chk(okq and kq == 4, "方向 (1,-1) なら Q は λ=4")
same(line(P3, (-4, 4), 1), vec(-3, 7), "QP と取りちがえた誤答は (-3,7)")
in_text("$\\lambda = 1$ で $(-3,\\ 7)$ になり、$Q$ に届きません", "その誤りを名指ししている")

ok4, k4 = on_line((1, 2), (5, 6), (11, 14))
chk(ok4 and k4 == 2, "演習4 は線上（λ=2）")
same(vec(11, 14) - vec(1, 2), 2 * vec(5, 6), "演習4 の検算")

ok5, k5 = on_line((1, -2, 3), (2, 1, 2), (7, 1, 10))
chk(not ok5 and k5 == 3, "演習5 は線上にない（λ=3 で z が合わない）")
same(line((1, -2, 3), (2, 1, 2), 3), vec(7, 1, 9), "演習5 の λ=3 の点は z=9")
d5 = vec(7, 1, 10) - vec(1, -2, 3)
same(d5, vec(6, 3, 7), "演習5 の検算の差")
chk([sp.Rational(d5[i], (2, 1, 2)[i]) for i in range(3)]
    == [3, 3, sp.Rational(7, 2)], "その比は 3, 3, 3.5 でそろわない")

base6 = (2, -3)
for cand, par in [((-6, 9), True), ((3, -2), False), ((4, -6), True)]:
    det = base6[0] * cand[1] - base6[1] * cand[0]
    chk((det == 0) == par, f"演習6 {cand} の平行判定")
chk(sp.Rational(-6, 2) == -3 and sp.Rational(9, -3) == -3, "演習6 (i) の k は -3")
chk(sp.Rational(4, 2) == 2 and sp.Rational(-6, -3) == 2, "演習6 (iii) の k は 2")
# 傾きで見る検算が、(ii) を落とすか
for cand, g in [((2, -3), sp.Rational(-3, 2)), ((-6, 9), sp.Rational(9, -6)),
                ((4, -6), sp.Rational(-6, 4))]:
    chk(sp.Rational(cand[1], cand[0]) == sp.Rational(-3, 2), f"傾きで見て {cand} は -1.5")
chk(sp.Rational(-2, 3) != sp.Rational(-3, 2), "(ii) の傾きは違う")
in_text("[第4節](#parametric) の傾きで見ます。", "演習6 の検算が独立になっている")
not_in_text("(i) と (iii) について、比を両方の成分で見ます。", "循環していた古い検算")

L7a, L7b = (2, 1), (1, 3)
M7a, M7b = (7, 6), (-1, 2)
s7 = sp.solve([L7a[0] + lam * L7b[0] - (M7a[0] + mu * M7b[0]),
               L7a[1] + lam * L7b[1] - (M7a[1] + mu * M7b[1])], [lam, mu])
chk(s7[lam] == 3 and s7[mu] == 2, "演習7 λ=3, μ=2")
same(line(L7a, L7b, 3), vec(5, 10), "演習7 の交点（L1）")
same(line(M7a, M7b, 2), vec(5, 10), "演習7 の交点（L2、独立な検算）")

L8a, L8b = (3, 1, -2), (1, -2, 3)
M8a, M8b = (5, -3, 4), (2, -4, 6)
same(vec(*M8b), 2 * vec(*L8b), "演習8 方向は 2 倍")
ok8, k8 = on_line(L8a, L8b, M8a)
chk(ok8 and k8 == 2, "演習8 M8a は λ=2 で L1 上")
same(line(M8a, M8b, 1), vec(7, -7, 10), "演習8 の検算に使う点")
ok8b, k8b = on_line(L8a, L8b, (7, -7, 10))
chk(ok8b and k8b == 4, "その点も λ=4 で L1 上")

ok9, k9 = on_line((5, -1), (-1, 2), (0, 9))
chk(ok9 and k9 == 5, "演習9 は λ=5 で (0,9)")
# λ を消した形 y = 9-2x
for p in (0, 1, 5, -2):
    P = line((5, -1), (-1, 2), p)
    chk(sp.simplify(P[1] - (9 - 2 * P[0])) == 0, f"y=9-2x が λ={p} で成り立つ")
chk(sp.solve(-1 + 2 * lam, lam) == [sp.Rational(1, 2)], "x 軸との交点は λ=1/2")
same(line((5, -1), (-1, 2), sp.Rational(1, 2)), vec(sp.Rational(9, 2), 0),
     "そのとき x=4.5（y 軸上ではない）")
in_text("$y = 9-2x$", "演習9 の独立な検算")
not_in_text("$\\lambda = 5$ を、もとのベクトル形に入れ直します", "同じ計算をなぞる古い検算")

# 演習 10: a と b の取りちがえ
okA, kA = on_line((4, -3), (2, 5), (2, 5))
chk(not okA and kA == -1, "演習10 A は生徒の直線上にすらない（λ=-1 で y=-8）")
same(line((4, -3), (2, 5), -1), vec(2, -8), "その点は (2,-8)")
same(line((2, 5), (4, -3), 0), vec(2, 5), "正しい式は λ=0 で A")

# ══════════════════════════════════════════════════════════
# 5. 条件と、言い過ぎの防止
# ══════════════════════════════════════════════════════════
in_text("## $\\mathbf{b} = \\mathbf{0}$ では、直線になりません", "b≠0 の条件")
in_text("$2$ 点 $A$、$B$（$A \\neq B$）が与えられたら", "2 点は相異なる")
in_text("**$3$ 次元では、平行でなくても交わらないことがある**"
        .replace("**", "").join(["（", "）"]), "到達目標に 3 次元の例外")
in_text("**$2$ 次元で、$\\mathbf{b}_1$ と $\\mathbf{b}_2$ が平行でなければ**",
        "2 次元の可解性に条件が付いている")
not_in_text("**$2$ 次元では、$2$ 本の式で $2$ 個の未知数**なので、ふつうに解けます。",
            "無条件の古い書き方")
in_text("**平行なのに解こうとすると、$0 = 4$ のような式になります。**",
        "平行なときに何が起きるかを書いている")
in_text("$\\lambda$ と $\\mu$ が**両方とも決まる $2$ 本**を選んで解き",
        "3 次元で選ぶ 2 本に条件が付いている")
in_text("## $\\lambda$ は、距離でも時刻でもありません", "λ の見出しが正確")
not_in_text("## $\\lambda$ には、それ自体の意味はありません", "言い過ぎの古い見出し")
in_text("**$\\lambda$ が負なら、逆向きに進みます。**", "負の λ の説明")
not_in_text("$\\mathbf{b}$ の向きに $\\lambda$ 歩だけ進みます", "負の λ を無視した古い書き方")
in_text("**$k$ が負なので矢印の向きは逆ですが、通る点の集まりは変わりません。**",
        "「同じ向き」という矛盾した言い方をしていない")
not_in_text("向きは逆ですが、直線としては同じ向きです", "矛盾した古い言い方")
in_text("**$t$ が時刻という決まった意味を持つので、$\\mathbf{b}$ を勝手にスカラー倍することは、もうできません**",
        "3.12 への注意")
# 3 次元で平行でないのに交わらない例が本当にある
u1, v1 = vec(1, 0, 0), vec(0, 1, 0)
chk(sp.Matrix([[1, 0], [0, 1], [0, 0]]).rank() == 2, "2 方向は平行でない")
sysol = sp.solve([lam - 0, 0 - (1 + mu), 0 - 1], [lam, mu])
chk(not sysol, "(0,0,0)+λ(1,0,0) と (0,1,1)+μ(0,1,0) は交わらない")
in_text("**平行でもないのに交わらない**という、$3$ 次元だけの状態です", "その説明がある")

# ══════════════════════════════════════════════════════════
# 6. シラバス・公式集
# ══════════════════════════════════════════════════════════
in_text("> $\\boldsymbol{r} = \\boldsymbol{a} + \\lambda\\boldsymbol{b}$, where "
        "$\\boldsymbol{b}$ is a direction vector of the line.", "Content の逐語引用")
in_text("> Convert to parametric form: $x = x_0 + \\lambda l$, $y = y_0 + \\lambda m$, "
        "$z = z_0 + \\lambda n$.", "Guidance の逐語引用")
in_text("**`a direction vector` の `a` に注目してください。**", "a と the の違い")
in_text("**$2$ 行あります。どちらも与えられます。**", "公式集は 2 行")
in_text("暗記は問われません", "暗記させていない")
# 2026-09: 「交点は 3.12 の欄」callout は削除（交点はこのページで扱う）
not_in_text("**AHL 3.12（運動）の欄**", "削除した 3.12 の欄の callout が残っていない")
chk("Mathematics and the knower" in TEXT, "TOK の逐語引用")

# ══════════════════════════════════════════════════════════
# 7. GDC（TI-Nspire CX II、非 CAS）
# ══════════════════════════════════════════════════════════
for claim in ["linSolve", "menu → Algebra", "Solve System of Linear Equations",
              "`ctrl` を押してから `var`", "menu → Actions → Clear a-z",
              "menu → Graph Entry/Edit → Parametric",
              "menu → Geometry → Points & Lines → Intersection Point(s)"]:
    in_text(claim, "GDC の記述")
for absent in ["unitV(", "norm(", "solve(", "nSolve("]:
    chk(absent not in TEXT.replace("linSolve(", ""),
        "非 CAS で確認できていない関数を使っていない: " + absent)
in_text("`Window Settings` にあるのは $x$ と $y$ の範囲だけで、`tmin` はそこにはありません。",
        "tmin の場所を直している")
not_in_text("`menu → Window/Zoom → Window Settings` で `tmin` を負にします",
            "tmin の場所を誤った古い書き方")
in_text("**`Analyze Graph` は関数のグラフ用**で、parametric では使えません。",
        "Analyze Graph の限界")
not_in_text("交点は `menu → Analyze Graph → Intersection` で出ます", "古い交点の出し方")
in_text("**電卓の parameter は $t$ です。**", "電卓の文字が t であること")

# ══════════════════════════════════════════════════════════
# 8. 図が本文と合っているか
# ══════════════════════════════════════════════════════════
chk("A0 = np.array([1.0, 2.0])" in FIG and "B0 = np.array([3.0, -1.0])" in FIG,
    "図1 の直線が本文と同じ")
chk("A1 = np.array([7.0, 0.0])" in FIG and "B1 = np.array([-6.0, 2.0])" in FIG,
    "図1b の別表現が本文と同じ")
chk("PA = np.array([2.0, -1.0])" in FIG and "PB = np.array([6.0, 1.0])" in FIG,
    "図2 の 2 点が本文と同じ")
chk("OFFP = np.array([8.0, 3.0])" in FIG, "図2(b) の D(8,3)")
same(line((2, -1), (4, 2), sp.Rational(3, 2)), vec(8, 2), "D の x から出る λ は 1.5、y は 2")
chk("$\\\\lambda = 1.5$ works for both" in FIG, "図2(b) のラベル")
chk("L2a, L2b = np.array([2.0, -3.0]), np.array([1.0, 2.0])" in FIG,
    "図3(a) の L2 が本文と同じ")
chk("X = np.array([4.0, 1.0])" in FIG, "図3(a) の交点")
chk("$\\\\lambda = 1$ on $L_1$" in FIG and "$\\\\mu = 2$ on $L_2$" in FIG,
    "図3(a) が λ=1, μ=2 を示している")
# 図3(b) の L3 は、例題 3 の「同じ直線」と別の方向ベクトルにしてある
chk("np.array([-3.0, 1.0])" in FIG, "図3(b) の L3 は方向 (-3,1)")
chk("np.array([-6.0, 2.0]), -0.7" not in FIG,
    "図3(b) が、例題3 の (-6,2) を使い回していない")
chk("$(1,\\\\ -2)$ is on $L_3$" in FIG, "図3(b) が L3 上の点を名指ししている")
# L3 は L1 と平行で、(1,-2) は L1 上にない
same(vec(-3, 1), -1 * vec(3, -1), "L3 の方向は L1 に平行")
okL3, _ = on_line((1, 2), (3, -1), (1, -2))
chk(not okL3, "(1,-2) は L1 上にない")

# ══════════════════════════════════════════════════════════
# 9. 体裁の不変量
# ══════════════════════════════════════════════════════════
chk(len(re.findall(r"(?m)^---\s*$", TEXT)) == 6, "--- は front matter 2 + 例題 4")
chk(TEXT.count('<details class="jp-trans"') == 14, "日本語訳の折りたたみが 14")
chk(TEXT.count(".ex-sep") == 9, "演習の区切りが 9")
chk(TEXT.count("model-answer") == 6, "model-answer が 6")
chk(re.findall(r"\[(\d+)\]\{\.ex-no\}", TEXT) == [str(i) for i in range(1, 11)],
    "演習の番号が 1..10")
chk(len(re.findall(r"(?m)^::: \{#exm-ahl311-", TEXT)) == 4, "例題が 4 つ")
ideas = re.findall(r"(?m)^### (\d+)\.", TEXT)
chk(ideas == [str(i) for i in range(1, 10)] + [str(i) for i in range(1, 7)],
    "The idea 1..9 と GDC 1..6 の連番: " + ",".join(ideas))
heads = [h for h in re.findall(r"(?m)^## (.*)", TEXT)
         if h in ("What you should be able to do", "The idea", "Why it works",
                  "Worked examples", "Common errors",
                  "Using your GDC (TI-Nspire CX II)", "Exercises")]
chk(heads == ["What you should be able to do", "The idea", "Why it works",
              "Worked examples", "Common errors",
              "Using your GDC (TI-Nspire CX II)", "Exercises"],
    "7 つの見出しの順序")
chk(TEXT.count("**検算") >= 12, "検算が 12 か所以上: %d" % TEXT.count("**検算"))
chk("**確かめ" not in TEXT and "確かめます。" not in TEXT,
    "検算のラベルに「確かめ」を使っていない")
for w in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん", "当たり前", "そのとおり"]:
    chk(w not in TEXT, "禁止語を使っていない: " + w)
for m in re.finditer(r"`[^`\n]*`", TEXT):
    chk("$" not in m.group(0), "コードスパンの中の数式 :: " + m.group(0)[:60])
for line_ in TEXT.split("\n"):
    if line_.startswith("|") and "$" in line_:
        for mm in re.finditer(r"\$[^$]*\$", line_):
            chk("|" not in mm.group(0), "表のセルの数式の中の | :: " + line_[:60])
chk(TEXT.count("\\left") == TEXT.count("\\right"), "\\left と \\right の対応")
chk("@sec-" not in TEXT, "他ページを @ で参照していない")
# ✓ / ✗ が数式の中に無い（KaTeX に字形が無い）
chk(TEXT.count("$$") % 2 == 0, "$$ の個数が偶数")
_rest = TEXT
for _m in re.finditer(r"\$\$(.*?)\$\$", TEXT, re.S):
    chk(not any(c in _m.group(1) for c in "✓✗①②"),
        "display math の中の ✓/✗/丸数字 :: "
        + _m.group(1)[:60].replace("\n", " "))
_rest = re.sub(r"\$\$.*?\$\$", " ", TEXT, flags=re.S)
for line_ in _rest.split("\n"):
    parts = line_.split("$")
    for i in range(1, len(parts), 2):
        chk(not any(c in parts[i] for c in "✓✗①②"),
            "inline math の中の ✓/✗/丸数字 :: " + parts[i][:50])
defined = set(re.findall(r"\{#([a-zA-Z0-9\-]+)[ }]", TEXT))
atrefs = set(re.findall(r"@((?:eq|fig|tbl|exm)-[a-zA-Z0-9\-]+)", TEXT))
links = set(re.findall(r"\]\(#([a-zA-Z0-9\-]+)\)", TEXT))
chk(not (atrefs - defined), "未定義の @ 参照: %s" % sorted(atrefs - defined))
chk(not (links - defined - {"why-it-works"}),
    "未定義のリンク先: %s" % sorted(links - defined - {"why-it-works"}))
unused = sorted(d for d in defined
                if d.split("-")[0] in ("eq", "fig", "tbl", "exm")
                and d not in atrefs and d not in links)
chk(not unused, "使われていない番号: %s" % unused)
IMG = os.path.join(BASE, "img")
for name in ["ahl-3-11-idea.svg", "ahl-3-11-notunique.svg",
             "ahl-3-11-point.svg", "ahl-3-11-intersect.svg"]:
    chk(os.path.exists(os.path.join(IMG, name)), "図がある: " + name)
    chk("img/" + name in TEXT, "図を本文で使っている: " + name)
for fn, an in re.findall(r"\]\((ahl-3-[0-9a-z]+)\.qmd#([a-z0-9-]+)\)", TEXT):
    f = os.path.join(BASE, fn + ".qmd")
    if os.path.exists(f):
        chk("{#" + an + "}" in open(f, encoding="utf-8").read(),
            "リンク先のアンカーがある: %s#%s" % (fn, an))
chk("ahl-3-10b.qmd#unit)" not in TEXT, "「速さ×向き」の参照は #direction を指している")

# ══════════════════════════════════════════════════════════
# 10. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(HERE, "..", "..", "_quarto-draft.yml"),
             encoding="utf-8").read()
chk("ai-hl/03-geometry-and-trigonometry/ahl-3-11.qmd" in DRAFT,
    "_quarto-draft.yml に登録されている")
chk(DRAFT.index("ahl-3-10b.qmd") < DRAFT.index("ahl-3-11.qmd")
    < DRAFT.index("ahl-3-14.qmd"), "サイドバーの並びが 3.10b → 3.11 → 3.14")
PUB = open(os.path.join(HERE, "..", "..", "_quarto.yml"), encoding="utf-8").read()
chk("ahl-3-11" not in PUB, "公開用の _quarto.yml は SL だけのまま")
IDX = open(os.path.join(HERE, "..", "..", "ai-hl", "index.qmd"),
           encoding="utf-8").read()
chk("[AHL 3.11 — Vector equation of a line]"
    "(03-geometry-and-trigonometry/ahl-3-11.qmd)" in IDX, "index の一覧にある")
chk("| **AHL 3.11** | **[Vector equation of a line]"
    "(03-geometry-and-trigonometry/ahl-3-11.qmd)** ✅ |" in IDX,
    "index の表が ✅ になっている")
_left = int(_m.group(1)) if (_m := re.search(r"残りの(\d+)項目", IDX)) else 0
_rows = re.findall(r"^\| (?:\*\*)?AHL [0-9.]+(?:\*\*)? \|(.*)\|$", IDX, re.M)
chk(_left == len([r for r in _rows if "✅" not in r]),
    "「残りの N 項目」が、まだ ✅ の付いていない行の数と合う")
GLO = open(os.path.join(HERE, "..", "..", "glossary-ai.qmd"),
           encoding="utf-8").read()
for term in ["| direction vector |", "| parameter |", "| parametric form |",
             "| vector equation (of a line) |", "| point of intersection |",
             "| lies on the line |", "| skew |"]:
    chk(term in GLO, "対訳表にある: " + term)

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
