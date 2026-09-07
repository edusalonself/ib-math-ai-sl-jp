"""AHL 3.10b（大きさ・位置ベクトル・単位ベクトル）の内容を検算する。

    python3 figs/ai-hl/check_ahl_3_10b.py
"""
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
QMD = os.path.join(HERE, "..", "..", "ai-hl", "03-geometry-and-trigonometry",
                   "ahl-3-10b.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_ahl_3_10b.py"), encoding="utf-8").read()

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


def mag(v):
    return sp.sqrt(sum(x**2 for x in v))


def eq(a, b, msg=""):
    chk(sp.simplify(sp.nsimplify(a) - sp.nsimplify(b)) == 0,
        msg + f"  ({a} vs {b})")


def same(u, v, msg=""):
    chk(sp.simplify(u - v) == sp.zeros(*u.shape), msg + f"  ({list(u)} vs {list(v)})")


def near(a, b, tol=5e-4, msg=""):
    chk(abs(float(a) - float(b)) < tol, msg + f"  ({float(a)} vs {float(b)})")


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている（直したはず）: " + msg + " :: " + sub[:70])


def band(v):
    """max|vi| < |v| < sum|vi| （0 でない成分が 2 つ以上のとき）"""
    lo = max(abs(x) for x in v)
    hi = sum(abs(x) for x in v)
    return lo, mag(v), hi


D = sp.deg

# ══════════════════════════════════════════════════════════
# 1. 大きさの式そのもの
# ══════════════════════════════════════════════════════════
v1, v2, v3, k = sp.symbols("v1 v2 v3 k", real=True)
# 3 次元の 2 段階が、公式集の形になる
step = sp.sqrt(sp.sqrt(v1**2 + v2**2)**2 + v3**2)
eq(sp.simplify(step), sp.sqrt(v1**2 + v2**2 + v3**2), "2 段の三平方が公式集の形になる")
# |kv| = |k||v|
eq(sp.simplify(sp.sqrt((k*3)**2 + (k*4)**2)), 5*sp.Abs(k), "|kv| = |k||v|")
chk(sp.sqrt(sp.Integer(-2)**2) == 2, "√(k²) は |k| であって k ではない")
# v/|v| の長さは 1
u = vec(3, 4) / mag(vec(3, 4))
eq(mag(u), 1, "単位ベクトルの長さは 1")
in_text("\\sqrt{k^2} = \\lvert k \\rvert", "√(k²)=|k| を Why it works に書いている")
in_text("**$k$ ではありません。**", "k ではないと明記している")

# ══════════════════════════════════════════════════════════
# 2. 検算に使う「幅」の性質
# ══════════════════════════════════════════════════════════
for w in [(5, -12), (2, -3, 6), (3, -5), (6, -8), (2.5, 6), (8, -15), (7, -4),
          (1, -2, 2), (4, 4, -7), (4, 3), (-6, 8), (-12, 16), (10, 24),
          (70, 240), (2, -3, 6), (9, -12)]:
    lo, m, hi = band(w)
    chk(lo < m < hi, f"幅が成り立つ: {w}")
# 0 でない成分が 1 つ以下のときだけ、等号になる
lo, m, hi = band((0, 7))
chk(lo == m == hi, "0 でない成分が 1 つなら、上下とも等号")
lo, m, hi = band((0, 0))
chk(lo == m == hi == 0, "零ベクトルでも等号")
# 「成分をそのまま足す」誤りは、必ず上限ちょうどになる
chk(sum(abs(x) for x in (3, 4)) == 7 and float(mag(vec(3, 4))) == 5.0,
    "(3,4) をそのまま足すと 7、正しくは 5")
in_text("**$0$ でない成分が $2$ つ以上あるときは、どちらも「等しい」にはなりません。**",
        "幅が厳密であることを、検算の定義のところに書いている")
in_text("**上限に等しくなるのは、$0$ でない成分が $1$ つ以下のときだけ**",
        "等号の条件が「1 つ以下」になっている")
not_in_text("**上限に等しくなるのは、$0$ でない成分が $1$ つしかないときだけ**",
            "零ベクトルを落とした古い条件")
# 幅の表示は、すべて狭義不等号
for s2 in ["$12 < 13 < 5+12 = 17$", "$6 < 7 < 2+3+6 = 11$", "$5 < 5.83 < 3+5 = 8$",
           "$8 < 10 < 6+8 = 14$", "$6 < 6.5 < 2.5+6 = 8.5$",
           "$15 < 17 < 8+15 = 23$", "$7 < 8.06 < 7+4 = 11$",
           "$2 < 3 < 1+2+2 = 5$", "$7 < 9 < 4+4+7 = 15$",
           "$240 < 250 < 70+240 = 310$", "$12 < 15 < 9+12 = 21$"]:
    in_text(s2, "幅の表示が狭義不等号")
chk("\\leq 13 \\leq" not in TEXT and "\\leq 6.5 \\leq" not in TEXT,
    "広義不等号の古い表示が残っていない")
# 幅が捕まえる誤りの例（演習 10）
near(sp.sqrt(119), 10.9087, msg="生徒の誤答 √119")
chk(float(sp.sqrt(119)) < 12, "√119 は、いちばん大きい成分 12 より小さい（幅の外）")
in_text("演習 $10$ のように $(-5)^2$ を $-25$ としてしまうと $\\sqrt{-25+144} = "
        "\\sqrt{119} \\approx 10.9$ となり、いちばん大きい成分 $12$ より小さくなって、"
        "この幅から外れます。", "幅が実際に捕まえる誤りを挙げている")
not_in_text("$\\sqrt{25-144}$", "実数にならない例（幅では判定できない）を挙げていない")

# ══════════════════════════════════════════════════════════
# 3. 例題の数値
# ══════════════════════════════════════════════════════════
eq(mag(vec(5, -12)), 13, "例題1(a)")
eq(mag(vec(2, -3, 6)), 7, "例題1(b)")
eq(mag(vec(3, -5)), sp.sqrt(34), "例題1(c) 正確な値")
near(sp.sqrt(34), 5.83095, msg="例題1(c) の小数")
chk(round(float(sp.sqrt(34)), 2) == 5.83, "例題1(c) は 3 桁で 5.83")
in_text("\\sqrt{34} \\approx 5.83", "5.83 と書いている")
not_in_text("\\sqrt{34} \\approx 8.06", "√65 の値を取りちがえた古い数字")

A, B = vec(1, 4), vec(7, -4)
same(B - A, vec(6, -8), "例題2(b) AB")
eq(mag(B - A), 10, "例題2(c) |AB|")
same(A + (B - A), B, "例題2 の検算（足し算に戻す）")
# a-b と取りちがえた誤答は、この検算で落ちる
chk(sp.simplify((A + (A - B)) - B) != sp.zeros(2, 1),
    "例題2 の検算は AB の向き違いを捕まえる")
same(A + (A - B), vec(-5, 12), "その誤答は (-5,12) になる")
in_text("\\begin{pmatrix} -5 \\\\ 12 \\end{pmatrix}$ になり、$\\mathbf{b}$ に戻りません",
        "誤答の行き先を明示している")

W = vec(3, 4)
eq(mag(W), 5, "例題3(a)")
same(W / 5, vec(sp.Rational(3, 5), sp.Rational(4, 5)), "例題3(b) 単位ベクトル")
same(7 * W / 5, vec(sp.Rational(21, 5), sp.Rational(28, 5)), "例題3(c)")
eq(mag(7 * W / 5), 7, "例題3(c) の長さは 7")
eq(mag(7 * W), 35, "7(3i+4j) の長さは 35")
in_text("whose magnitude is $7 \\times 5 = 35$, not $7$", "35 を model answer に書いている")
# 1 成分だけ割った誤答は、長さが 1 にならない
near(mag(vec(sp.Rational(3, 5), 4)), 4.04475, msg="例題3 の誤答の長さ")
in_text("\\approx 4.04$ になり、$1$ になりません", "その誤答の長さを書いている")

boat = vec(sp.Rational(5, 2), 6)
eq(mag(boat), sp.Rational(13, 2), "例題4(b) 速さ 6.5")
th = sp.atan(sp.Rational(5, 2) / 6)
near(D(th), 22.6199, msg="例題4(c) の角")
chk(round(float(D(th))) == 23, "例題4(c) は 023°")
near(D(sp.atan(6 / sp.Rational(5, 2))), 67.3801,
     msg="分母分子を逆にすると 67.4°")
chk(float(D(sp.atan(6 / sp.Rational(5, 2)))) > 45, "逆にすると 45° より大きい（検算が効く）")
in_text("$67.4^{\\circ}$ になり、$045^{\\circ}$ より大きくなって、この検算に引っかかります",
        "例題4 の方位の検算が、誤りを名指ししている")

# ══════════════════════════════════════════════════════════
# 4. 演習の数値
# ══════════════════════════════════════════════════════════
eq(mag(vec(8, -15)), 17, "演習1(a)")
eq(mag(vec(7, -4)), sp.sqrt(65), "演習1(b) 正確な値")
chk(round(float(sp.sqrt(65)), 2) == 8.06, "演習1(b) は 3 桁で 8.06")
eq(mag(vec(1, -2, 2)), 3, "演習2(a)")
eq(mag(vec(4, 4, -7)), 9, "演習2(b)")

A3, B3 = vec(2, -1), vec(6, 2)
same(B3 - A3, vec(4, 3), "演習3 AB")
eq(mag(B3 - A3), 5, "演習3 |AB|")
same(A3 + (B3 - A3), B3, "演習3 の検算")
chk(sp.simplify((A3 + vec(4, 1)) - B3) != sp.zeros(2, 1),
    "演習3 の検算は 2-(-1)=1 の誤りを捕まえる")
same(A3 + vec(4, 1), vec(6, 0), "その誤答は (6,0) になる")

e4 = vec(-6, 8)
eq(mag(e4), 10, "演習4 の大きさ")
same(e4 / 10, vec(sp.Rational(-3, 5), sp.Rational(4, 5)), "演習4 の単位ベクトル")
eq(mag(e4 / 10), 1, "演習4 の検算")
near(mag(vec(sp.Rational(-3, 5), 8)), 8.02247, msg="演習4 の誤答の長さ")

e5 = vec(-3, 4)
eq(mag(e5), 5, "演習5 の向きの長さ")
same(20 * e5 / 5, vec(-12, 16), "演習5 の速度")
eq(mag(vec(-12, 16)), 20, "演習5 の検算")
eq(mag(20 * e5), 100, "20(-3i+4j) の長さは 100")
in_text("これは長さ $100$ です", "誤答の長さを書いている")

e6 = vec(5, 12)
eq(mag(e6), 13, "演習6 の向きの長さ")
same(26 * e6 / 13, vec(10, 24), "演習6 の答え")
eq(mag(vec(10, 24)), 26, "演習6 の検算 1")
chk(sp.Rational(10, 5) == 2 and sp.Rational(24, 12) == 2, "演習6 の検算 2（比）")

e7 = vec(70, 240)
eq(mag(e7), 250, "演習7 の対地速度")
th7 = sp.atan(sp.Rational(70, 240))
near(D(th7), 16.2602, msg="演習7 の角")
chk(round(float(D(th7))) == 16, "演習7 は 016°")
near(D(sp.atan(sp.Rational(240, 70))), 73.7398, msg="逆にすると 73.7°")
in_text("$73.7^{\\circ}$ になり、この検算に引っかかります", "演習7 の方位の検算")

e8 = vec(2, -3, 6)
eq(mag(e8), 7, "演習8 の大きさ")
same(e8 / 7, vec(sp.Rational(2, 7), sp.Rational(-3, 7), sp.Rational(6, 7)),
     "演習8 の単位ベクトル")
eq(mag(e8 / 7), 1, "演習8 の検算")
for x, d in [(sp.Rational(2, 7), 0.286), (sp.Rational(3, 7), 0.429),
             (sp.Rational(6, 7), 0.857)]:
    chk(round(float(x), 3) == d, f"演習8 の小数表示 {d}")
in_text("\\left(-\\frac{3}{7}\\right)^{2}", "負の成分をかっこ付きで 2 乗している")
not_in_text("+\\left(\\frac{3}{7}\\right)^{2}+", "かっこの中の符号を落とした古い書き方")

A9, B9 = vec(-4, 7), vec(5, -5)
same(B9 - A9, vec(9, -12), "演習9 AB")
eq(mag(B9 - A9), 15, "演習9 |AB|")
eq(mag(A9 - B9), 15, "|BA| も 15")
same(A9 + (B9 - A9), B9, "演習9 の検算")

e10 = vec(-5, 12)
eq(mag(e10), 13, "演習10 の正しい答え")
chk((-5)**2 == 25, "(-5)² = 25")
chk(-5**2 == -25, "-5² = -25（かっこの有無で変わる）")

# ══════════════════════════════════════════════════════════
# 5. 条件の付け方
# ══════════════════════════════════════════════════════════
in_text("**大きさを出すときは、成分の符号を気にしなくてかまいません。**",
        "「符号を気にしない」を大きさに限定している")
not_in_text("**成分の符号は、気にしなくてかまいません。**", "無条件の古い書き方")
in_text("**$L > 0$ のとき**、長さ $L$ で $\\mathbf{v}$ の向きのベクトルは",
        "rescale の式に L>0 が付いている")
in_text("**この形がそのまま使えるのは、東向きの成分も北向きの成分も正のとき**です。",
        "方位の式に、成分が正であるという条件が付いている")
in_text("$\\tan^{-1}$ が返す値をそのまま方位にはできません", "負の成分のときの注意")
in_text("$\\mathbf{v} \\neq \\mathbf{0}$ が @eq-ahl310b-unit の条件です。",
        "単位ベクトルに v≠0 の条件")
in_text("$\\lvert \\mathbf{v} \\rvert = 0$ になるのは $\\mathbf{v} = \\mathbf{0}$ "
        "のときだけです", "|v|=0 の条件")
in_text("$\\lvert \\mathbf{v} \\rvert \\geq 0$ です。**長さが負になることはありません。**",
        "|v| は非負")
# 方位の反例（成分が負のとき）を数値で確認
chk(float(D(sp.atan(sp.Rational(-5, 2) / 6))) < 0,
    "東向きが負なら atan は負を返す（そのままでは方位にならない）")

# ══════════════════════════════════════════════════════════
# 6. シラバス・公式集
# ══════════════════════════════════════════════════════════
in_text("> Position vectors $\\overrightarrow{\\text{OA}} = \\boldsymbol{a}$.",
        "Content の逐語引用 1")
in_text("> Rescaling and normalizing vectors.", "Content の逐語引用 2")
in_text("$\\dfrac{\\boldsymbol{v}}{\\lvert \\boldsymbol{v} \\rvert}$, the unit normal vector.",
        "Guidance の逐語引用")
in_text("Find the velocity of a particle with speed $7\\,\\text{ms}^{-1}$ in the "
        "direction $3\\boldsymbol{i} + 4\\boldsymbol{j}$.", "Example の逐語引用")
in_text("> The resultant as the sum of two or more vectors.", "resultant の Guidance")
in_text("**$1$ 行だけです。**", "公式集 AHL 3.10 は 1 行")
in_text("**単位ベクトルの式 $\\dfrac{\\mathbf{v}}{\\lvert \\mathbf{v} \\rvert} は、公式集にありません。**"
        .replace(" は、", "$ は、"), "v/|v| は公式集にないと書いている")
in_text("**@eq-ahl310b-mag は試験中に見られます。暗記は問われません。**",
        "公式集にあるものを暗記させていない")
# normal の説明が、意図ではなく対象を述べている
in_text("**ここに書かれている式 $\\dfrac{\\mathbf{v}}{\\lvert \\mathbf{v} \\rvert}$ は、"
        "長さを $1$ にそろえた（normalize した）ベクトル**です。**垂直**という意味ではありません。",
        "normal の説明")
not_in_text("ここでの `normal` は、**normalize（長さを $1$ にそろえる）した**という意味です。",
            "IB の意図を断定した古い書き方")
in_text("$\\mathbf{v}$ に垂直ではありません", "垂直ではないと明記")

# ══════════════════════════════════════════════════════════
# 7. GDC（TI-Nspire CX II、非 CAS）
# ══════════════════════════════════════════════════════════
for claim in ["`ctrl` を押してから `x²`", "`ctrl` を押してから `var`",
              "`sto` というキーはありません",
              "menu → 7: Matrix & Vector → C: Vector",
              "doc → Settings → Document Settings",
              "menu → Actions → Clear a-z",
              "dotP("]:
    in_text(claim, "GDC の記述")
chk("unitV(" in TEXT and "`unitV(` や `norm(` は載っていません" in TEXT,
    "unitV / norm は「載っていない」と書く 1 か所だけ")
chk(TEXT.count("unitV(") == 1 and TEXT.count("norm(") == 1,
    "unitV / norm を使ってはいない")
chk("nSolve" not in TEXT and "solve(" not in TEXT, "solve 系を使っていない")
in_text("設定が **Radian** のままでよいときは、$\\dfrac{180}{\\pi}$ を掛けます。"
        "**Degree 設定のまま", "×180/π が Radian 設定のときだと書いている")
not_in_text("設定を変えずに済ませたいときは、$\\dfrac{180}{\\pi}$ を掛けます。",
            "設定を書いていない古い言い方")
near(float(sp.atan(sp.Rational(5, 2) / 6)), 0.394791, msg="Radian 設定での値")
in_text("$0.3948$", "radian の値を書いている")
near(float(D(sp.atan(sp.Rational(5, 2) / 6))) * 180 / float(sp.pi),
     1296.02, tol=0.5, msg="Degree 設定で ×180/π をやったときの値")
in_text("$1296$ になります。", "Degree 設定での誤った値を書いている")
# dotP を使った大きさが正しい
eq(sp.sqrt(vec(2, -3, 6).dot(vec(2, -3, 6))), 7, "√(dotP(v,v)) = 7")
eq(sp.Rational(1, 5) * 3, sp.Rational(3, 5), "1/5*[3;4] の 1 つ目")
# GDC 節への参照だと分かる書き方
in_text("[GDC 第5節](#gdc-angle)", "GDC 節への参照 1")
in_text("[GDC 第4節](#gdc-unit)", "GDC 節への参照 2")
in_text("[AHL 3.10a の GDC 第2節](ahl-3-10a.qmd#gdc-store)", "GDC 節への参照 3")
not_in_text("（[第5節](#gdc-angle)）", "本文の節番号と紛れる古い書き方")

# ══════════════════════════════════════════════════════════
# 8. 図が本文と合っているか
# ══════════════════════════════════════════════════════════
# 図 1(b): 床の対角線が、脚より長く見える向きになっている
import numpy as np
ey = np.array([float(x) for x in
               re.search(r"ey = np\.array\(\[([-\d.]+), ([-\d.]+)\]\)", FIG).groups()])
ex = np.array([1.0, 0.0])
a_, b_, c_ = 2.0, 3.0, 6.0
leg_x = np.linalg.norm(a_ * ex)
leg_y = np.linalg.norm(b_ * ey)
floor = np.linalg.norm(a_ * ex + b_ * ey)
chk(floor > leg_x and floor > leg_y,
    "図1(b) の床の対角線が、両方の辺より長く描かれている "
    f"({floor:.2f} vs {leg_x:.2f}, {leg_y:.2f})")
space = a_ * ex + b_ * ey + np.array([0.0, c_])
tilt = np.degrees(np.arctan2(abs(space[0]), abs(space[1])))
chk(tilt > 15, f"図1(b) の立体対角線が、高さの辺と見分けられる ({tilt:.1f}°)")
chk("the middle square root is never worked out" in FIG,
    "図1(b) の見出しが「途中の √ は出さない」")
in_text("**途中の $\\sqrt{13}$ は、計算しません。**", "本文も同じことを言っている")
eq(sp.sqrt(2**2 + 3**2), sp.sqrt(13), "途中の値は √13")
# 図 3(b): 3i+4j がずらして描かれ、隠れていない
chk("OFFB" in FIG and "arrow(ax, tuple(OFFB), tuple(W + OFFB)" in FIG,
    "図3(b) の 3i+4j はずらして描いている")
chk("(length $5$, not $7$)" in FIG, "図3(b) のラベルが長さ 5 を言っている")
not_in_text("(direction only)", "図の古いラベル")
chk("(direction only)" not in FIG, "図の古いラベルが残っていない")
# 図 2: 座標と本文が一致
same(vec(7, -4) - vec(1, 4), vec(6, -8), "図2 の AB")
chk("A = np.array([1.0, 4.0])" in FIG and "B = np.array([7.0, -4.0])" in FIG,
    "図2 の点が本文と同じ")
chk("$6$ across" in FIG and "$8$ down" in FIG, "図2(b) のラベル")
chk("\\sqrt{6^2+(-8)^2} = 10" in FIG, "図2(b) の式")
# 図 1(a)
chk("\\sqrt{3^2+4^2} = 5" in FIG, "図1(a) の式")

# ══════════════════════════════════════════════════════════
# 9. 用語・言い回し
# ══════════════════════════════════════════════════════════
in_text("**bearing**（方位）", "英語が先")
not_in_text("**方位（bearing）**", "日本語が先の古い書き方")
in_text("（**normalize**、正規化）", "normalize の初出に訳語")
in_text("（**rescale**、長さの付け替え）", "rescale の初出に訳語")
not_in_text("**たしかめ方は、長さを出し直すことです。**", "検算のラベルでない古い言い方")
chk("**確かめ" not in TEXT and "確かめます。" not in TEXT,
    "検算のラベルに「確かめ」を使っていない")
for w in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん", "当たり前", "そのとおり"]:
    chk(w not in TEXT, "禁止語を使っていない: " + w)

# ══════════════════════════════════════════════════════════
# 10. 体裁の不変量
# ══════════════════════════════════════════════════════════
chk(len(re.findall(r"(?m)^---\s*$", TEXT)) == 6, "--- は front matter 2 + 例題 4")
chk(TEXT.count('<details class="jp-trans"') == 14, "日本語訳の折りたたみが 14")
chk(TEXT.count(".ex-sep") == 9, "演習の区切りが 9")
chk(TEXT.count("model-answer") == 6, "model-answer が 6")
chk(re.findall(r"\[(\d+)\]\{\.ex-no\}", TEXT) == [str(i) for i in range(1, 11)],
    "演習の番号が 1..10")
chk(len(re.findall(r"(?m)^::: \{#exm-ahl310b-", TEXT)) == 4, "例題が 4 つ")
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
for m in re.finditer(r"`[^`\n]*`", TEXT):
    chk("$" not in m.group(0), "コードスパンの中の数式 :: " + m.group(0)[:60])
for line in TEXT.split("\n"):
    if line.startswith("|") and "$" in line:
        for mm in re.finditer(r"\$[^$]*\$", line):
            chk("|" not in mm.group(0), "表のセルの数式の中の | :: " + line[:60])
chk(TEXT.count("\\left") == TEXT.count("\\right"), "\\left と \\right の対応")
chk("@sec-" not in TEXT, "他ページを @ で参照していない")
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
IMG = os.path.join(HERE, "..", "..", "ai-hl", "03-geometry-and-trigonometry", "img")
for name in ["ahl-3-10b-magnitude.svg", "ahl-3-10b-position.svg",
             "ahl-3-10b-unit.svg"]:
    chk(os.path.exists(os.path.join(IMG, name)), "図がある: " + name)
    chk("img/" + name in TEXT, "図を本文で使っている: " + name)

# 他ページへのリンクが、実在するアンカーを指している
BASE = os.path.join(HERE, "..", "..", "ai-hl", "03-geometry-and-trigonometry")
for link in re.findall(r"\]\((ahl-3-[0-9a-z]+)\.qmd#([a-z0-9-]+)\)", TEXT):
    f = os.path.join(BASE, link[0] + ".qmd")
    if os.path.exists(f):
        chk("{#" + link[1] + "}" in open(f, encoding="utf-8").read(),
            "リンク先のアンカーがある: %s#%s" % link)

# ══════════════════════════════════════════════════════════
# 11. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(HERE, "..", "..", "_quarto-draft.yml"),
             encoding="utf-8").read()
chk("ai-hl/03-geometry-and-trigonometry/ahl-3-10b.qmd" in DRAFT,
    "_quarto-draft.yml に登録されている")
chk(DRAFT.index("ahl-3-10a.qmd") < DRAFT.index("ahl-3-10b.qmd")
    < DRAFT.index("ahl-3-14.qmd"), "サイドバーの並びが 3.10a → 3.10b → 3.14")
PUB = open(os.path.join(HERE, "..", "..", "_quarto.yml"), encoding="utf-8").read()
chk("ahl-3-10b" not in PUB, "公開用の _quarto.yml は SL だけのまま")
IDX = open(os.path.join(HERE, "..", "..", "ai-hl", "index.qmd"),
           encoding="utf-8").read()
chk("[AHL 3.10b — Magnitude, position and unit vectors]"
    "(03-geometry-and-trigonometry/ahl-3-10b.qmd)" in IDX, "index の一覧にある")
chk("| **AHL 3.10** | **[Vectors: the basics]"
    "(03-geometry-and-trigonometry/ahl-3-10a.qmd)** ／ "
    "**[Magnitude, position and unit vectors]"
    "(03-geometry-and-trigonometry/ahl-3-10b.qmd)** ✅ |" in IDX,
    "index の表が両方そろって ✅ になっている")
_left = int(_m.group(1)) if (_m := re.search(r"残りの(\d+)項目", IDX)) else 0
_rows = re.findall(r"^\| (?:\*\*)?AHL [0-9.]+(?:\*\*)? \|(.*)\|$", IDX, re.M)
chk(_left == len([r for r in _rows if "✅" not in r]),
    "「残りの N 項目」が、まだ ✅ の付いていない行の数と合う")
GLO = open(os.path.join(HERE, "..", "..", "glossary-ai.qmd"),
           encoding="utf-8").read()
for term in ["| magnitude |", "| position vector |", "| normalize |",
             "| rescale |", "| bearing |", "| ground speed |",
             "| exact value |", "| to the nearest degree |"]:
    chk(term in GLO, "対訳表にある: " + term)

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
