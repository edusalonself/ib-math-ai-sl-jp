"""AHL 3.13b（vector product）の内容を検算する。

    python3 figs/ai-hl/check_ahl_3_13b.py

方針は他のページのチェッカーと同じです。

  * 数値は sympy で第一原理から出し直す（本文の式を写さない）
  * 「こう間違えたら、こうなる」と書いた検算は、実際にその
    間違いをして、本当に別の値になることを確かめる
  * レビューで直した箇所には not_in_text の見張りを置く
  * 構成の不変量（例題 4・演習 10・節番号など）を数える
  * 登録先（_quarto-draft.yml、index.qmd、glossary-ai.qmd）を見る
"""
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "..", "..", "ai-hl", "03-geometry-and-trigonometry")
QMD = os.path.join(BASE, "ahl-3-13b.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_ahl_3_13b.py"), encoding="utf-8").read()
# 図の中で「実際に紙に出る文字」だけを集める。座標や lim の数と
# 混同しないように、文字列リテラルの中身だけを見る。
FIGSTR = "\n".join(re.findall(r'r?"((?:[^"\\]|\\.)*)"', FIG))
# 使えない記法の見張りは、冒頭の注意書き（docstring）を除いて見る。
FIGCODE = FIG.split('"""', 2)[-1]

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


def mag(u):
    return sp.sqrt(sum(x**2 for x in u))


def cross(u, w):
    return u.cross(w)


def ang(u, w):
    return sp.deg(sp.acos(u.dot(w) / (mag(u) * mag(w))))


def eq(a, b, msg=""):
    chk(sp.simplify(a - b) == 0, msg + f"  ({a} vs {b})")


def same(u, w, msg=""):
    chk(sp.simplify(u - w) == sp.zeros(*u.shape),
        msg + f"  ({list(u)} vs {list(w)})")


def near(a, b, tol=5e-4, msg=""):
    chk(abs(float(a) - float(b)) < tol, msg + f"  ({float(a)} vs {float(b)})")


def sf3(x):
    """有効数字 3 桁に丸めた float。"""
    return float("%.3g" % float(sp.N(x, 25)))


def in_text(sub, msg=""):
    chk(sub in TEXT, "本文に見つからない: " + msg + " :: " + sub[:70])


def not_in_text(sub, msg=""):
    chk(sub not in TEXT, "本文に残っている（直したはず）: " + msg + " :: " + sub[:70])


def in_fig(sub, msg=""):
    chk(sub in FIG, "図のスクリプトに見つからない: " + msg + " :: " + sub[:70])


# ══════════════════════════════════════════════════════════
# 0. 公式集の成分式そのもの
# ══════════════════════════════════════════════════════════
_v = sp.Matrix(sp.symbols("v1 v2 v3"))
_w = sp.Matrix(sp.symbols("w1 w2 w3"))
same(cross(_v, _w),
     vec(_v[1] * _w[2] - _v[2] * _w[1],
         _v[2] * _w[0] - _v[0] * _w[2],
         _v[0] * _w[1] - _v[1] * _w[0]),
     "公式集の 3 行が、sympy の外積と一致する")
# 2 行目の順番（本文がいちばん強調しているところ）
chk(sp.simplify(cross(_v, _w)[1] - (_v[0] * _w[2] - _v[2] * _w[0])) != 0,
    "2 行目は v1w3-v3w1 ではない（符号が逆）")
# 反交換、v×v = 0
same(cross(_w, _v), -cross(_v, _w), "w×v = -(v×w)")
same(cross(_v, _v), sp.zeros(3, 1), "v×v = 0")
# 両方に垂直（恒等式）
eq(sp.expand(_v.dot(cross(_v, _w))), 0, "v・(v×w) = 0 は恒等式")
eq(sp.expand(_w.dot(cross(_v, _w))), 0, "w・(v×w) = 0 は恒等式")
# |v×w|² + (v・w)² = |v|²|w|²（sin²+cos² の正体。検算の根拠）
eq(sp.expand(cross(_v, _w).dot(cross(_v, _w)) + _v.dot(_w)**2
             - (_v.dot(_v)) * (_w.dot(_w))), 0,
   "|v×w|² + (v・w)² = |v|²|w|²")
# 2 次元は、第 3 成分だけが残る
_a = sp.Matrix(list(sp.symbols("a1 a2")) + [0])
_b = sp.Matrix(list(sp.symbols("b1 b2")) + [0])
same(cross(_a, _b), vec(0, 0, _a[0] * _b[1] - _a[1] * _b[0]),
     "2 次元は (0, 0, a1b2-a2b1)")
# 三角形の面積は、どの頂点から取っても同じ（本文 Why it works の主張）
_A = sp.Matrix(sp.symbols("Ax Ay Az"))
_B = sp.Matrix(sp.symbols("Bx By Bz"))
_C = sp.Matrix(sp.symbols("Cx Cy Cz"))
_AA = cross(_B - _A, _C - _A)
same(sp.expand(cross(_A - _B, _C - _B)), sp.expand(-_AA),
     "B から取ると符号が逆になる")
same(sp.expand(cross(_A - _C, _B - _C)), sp.expand(_AA),
     "C から取ると、符号も変わらない（model answer の主張）")
same(sp.expand(cross(_B - _A, _C - _B)), sp.expand(_AA),
     "AB×BC も AB×AC と等しい（「使ってはいけない」は誤り）")
in_text("$\\overrightarrow{AB} \\times \\overrightarrow{BC} ="
        " \\overrightarrow{AB} \\times \\overrightarrow{AC}$",
        "AB×BC も同じ値だと書いている（レビュー1）")
not_in_text("$\\overrightarrow{AB}$ と $\\overrightarrow{BC}$ を使ってはいけません。",
            "誤りだった禁止（レビュー1）")
not_in_text("Only the sign changes", "C では符号が変わらない（レビュー2）")
in_text("changes the vector product by at most a sign",
        "直した model answer（レビュー2）")

# ══════════════════════════════════════════════════════════
# 1. 例題 1・2 — v = (2,-1,2), w = (4,3,0)
# ══════════════════════════════════════════════════════════
V, W = vec(2, -1, 2), vec(4, 3, 0)
CR = cross(V, W)
same(CR, vec(-6, 8, 10), "例題1(a) v×w")
eq(V.dot(CR), 0, "例題1(b) v・(v×w) = 0")
eq(W.dot(CR), 0, "例題1(b) w・(v×w) = 0")
same(cross(W, V), vec(6, -8, -10), "例題1(c) w×v")
eq(mag(CR), 10 * sp.sqrt(2), "|v×w| = 10√2")
near(mag(CR), 14.142136, msg="10√2 の小数")
eq(mag(V), 3, "|v| = 3")
eq(mag(W), 5, "|w| = 5")
eq(V.dot(W), 5, "v・w = 5")
in_text("\\begin{pmatrix} (-1)(0) - (2)(3) \\\\ (2)(4) - (2)(0) \\\\"
        " (2)(3) - (-1)(4) \\end{pmatrix}", "成分をあてはめた式を書いている")

# 例題1(b) が (a) の検算になっているか — 2 行目の符号ミスを捕まえるか
_wrong2 = vec(-6, -8, 10)
chk(V.dot(_wrong2) != 0, "2 行目を -8 にしたら v との内積が 0 でない")
eq(V.dot(_wrong2), 16, "そのとき 16 になる（本文の値）")
in_text("$\\mathbf{v}$ との内積が $-12+8+20 = 16 \\neq 0$ になります",
        "その値を本文に書いている")

# 例題1(d) の単位ベクトルの検算（循環していたので直した）
eq(sp.Rational(36 + 64 + 100, 200), 1, "正しい割り方なら 1 になる")
eq(sp.Rational(36 + 64 + 100, 100), 2, "10 で割っていたら 2 になる（検算が効く）")
in_text("\\frac{36+64+100}{200} = 1", "直した検算（レビュー4）")
not_in_text("$\\dfrac{1}{10\\sqrt{2}} \\times 10\\sqrt{2} = 1$",
            "循環していた検算（レビュー4）")

# 例題 2 — sin から角が決まらないこと
_sin = mag(CR) / (mag(V) * mag(W))
eq(_sin, 2 * sp.sqrt(2) / 3, "sinθ = 2√2/3")
near(_sin, 0.9428090, msg="sinθ の小数")
near(sp.deg(sp.asin(_sin)), 70.5287794, msg="sin⁻¹ の値")
chk(sf3(sp.deg(sp.asin(_sin))) == 70.5, "3 桁で 70.5")
near(180 - sp.deg(sp.asin(_sin)), 109.4712206, msg="もう 1 つの角")
chk(sf3(180 - sp.deg(sp.asin(_sin))) == 109.0, "109.47 は 3 桁で 109")
in_text("$\\sin 109.5^{\\circ}$ も同じ値です", "第5節のあいまいさの説明")
near(sp.sin(sp.rad(109.4712206)), float(_sin), msg="109.47° の sin は同じ")
# cos の側から出すと 1 つに決まる
eq(V.dot(W) / (mag(V) * mag(W)), sp.Rational(1, 3), "cosθ = 1/3")
near(ang(V, W), 70.5287794, msg="cos から出した角")
eq(sp.simplify(_sin**2 + sp.Rational(1, 3)**2), 1, "sin²+cos² = 1")
chk(V.dot(W) > 0, "内積が正なので鋭角（70.5 を選ぶ根拠）")

# ══════════════════════════════════════════════════════════
# 2. 例題 3 — 面積
# ══════════════════════════════════════════════════════════
eq(mag(CR), 10 * sp.sqrt(2), "例題3(a) 平行四辺形の面積")
A3, B3, C3 = vec(1, 0, 2), vec(3, 2, 1), vec(2, -1, 4)
AB, AC = B3 - A3, C3 - A3
same(AB, vec(2, 2, -1), "AB")
same(AC, vec(1, -1, 2), "AC")
same(cross(AB, AC), vec(3, -5, -4), "AB×AC")
eq(mag(cross(AB, AC)), 5 * sp.sqrt(2), "|AB×AC| = 5√2")
near(mag(cross(AB, AC)) / 2, 3.5355339, msg="三角形の面積")
chk(sf3(mag(cross(AB, AC)) / 2) == 3.54, "3 桁で 3.54")
# 検算：B から取ると符号が逆になる
same(cross(A3 - B3, C3 - B3), vec(-3, 5, 4), "BA×BC は符号が逆")
eq(mag(cross(A3 - B3, C3 - B3)), 5 * sp.sqrt(2), "大きさは同じ")
in_text("**成分がすべて符号違いになっている**", "その特徴を本文に書いている")
# 2 次元の三角形
P3, Q3, R3 = vec(1, 1, 0), vec(5, 2, 0), vec(2, 6, 0)
same(cross(Q3 - P3, R3 - P3), vec(0, 0, 19), "PQ×PR は (0,0,19)")
eq(sp.Rational(19, 2), sp.Rational(19, 2), "面積 9.5")
# 検算：長方形から 3 つの直角三角形を引く（外積を使わない別の道）
_rect = 4 * 5
_tris = sp.Rational(1, 2) * 4 * 1 + sp.Rational(1, 2) * 1 * 5 \
    + sp.Rational(1, 2) * 3 * 4
eq(_rect - _tris, sp.Rational(19, 2), "囲い込み法でも 9.5")
chk(_rect - _tris != 19, "1/2 を忘れた 19 とは合わない（検算が効く）")

# ══════════════════════════════════════════════════════════
# 3. 例題 4 — 垂直な成分
# ══════════════════════════════════════════════════════════
AA, BB = vec(-1, 6, 0), vec(4, 3, 0)
same(cross(AA, BB), vec(0, 0, -27), "a×b は (0,0,-27)")
eq(mag(cross(AA, BB)), 27, "|a×b| = 27")
eq(mag(BB), 5, "|b| = 5")
eq(mag(cross(AA, BB)) / mag(BB), sp.Rational(27, 5), "垂直な成分 5.4")
eq(AA.dot(BB), 14, "a・b = 14")
eq(sp.Rational(14, 5), sp.Rational(14, 5), "平行な成分 2.8")
eq(mag(AA)**2, 37, "|a|² = 37")
eq(sp.Rational(14, 5)**2 + sp.Rational(27, 5)**2, 37, "Pythagoras で 37")
# 検算：sinθ を内積から独立に出す（循環を避けた）
_cos = sp.Rational(14, 1) / (5 * sp.sqrt(37))
near(_cos, 0.4603202, msg="cosθ（本文 0.46032）")
near(sp.deg(sp.acos(_cos)), 62.5924246, msg="θ（本文 62.59°）")
near(sp.sin(sp.acos(_cos)), 0.8877545, msg="sinθ（本文 0.88775）")
near(sp.sqrt(37) * sp.sin(sp.acos(_cos)), sp.Rational(27, 5),
     msg="|a|sinθ が 5.4 に戻る")
in_text("**外積を使わずに** scalar product から出します",
        "循環しない検算に直した（レビュー6）")
not_in_text("$\\sin\\theta = \\dfrac{27}{5\\sqrt{37}} \\approx 0.88775$ なので",
            "循環していた書き方（レビュー6）")
# |a| で割った誤答は Pythagoras で落ちる
near(sp.Rational(27, 1) / sp.sqrt(37), 4.4386, msg="|a| で割った誤答 4.44")
near(sp.Rational(14, 5)**2 + (sp.Rational(27, 1) / sp.sqrt(37))**2, 27.5432,
     msg="誤答では 27.5（37 にならない）")
chk(abs(float(sp.Rational(14, 5)**2
              + (sp.Rational(27, 1) / sp.sqrt(37))**2) - 37) > 1,
    "誤答は Pythagoras で落ちる（検算が効く）")
# 3 次元の垂直な成分
eq(mag(CR) / mag(W), 2 * sp.sqrt(2), "例題4(c) = 2√2")
near(2 * sp.sqrt(2), 2.8284271, msg="2√2 の小数")
chk(float(2 * sp.sqrt(2)) < float(mag(V)), "成分は |v| = 3 を超えない")
eq((V.dot(W) / mag(W))**2 + (mag(CR) / mag(W))**2, 9,
   "1² + (2√2)² = 9 = |v|²")

# ══════════════════════════════════════════════════════════
# 4. 演習 1〜10
# ══════════════════════════════════════════════════════════
E1v, E1w = vec(3, 1, -2), vec(2, 4, 1)
same(cross(E1v, E1w), vec(9, -7, 10), "演習1")
eq(E1v.dot(cross(E1v, E1w)), 0, "演習1 の検算 1")
eq(E1w.dot(cross(E1v, E1w)), 0, "演習1 の検算 2")
# 2 行目の順番ミス
_e1wrong = vec(9, 7, 10)
eq(E1v.dot(_e1wrong), 14, "順番を逆にすると内積が 14")
chk(E1v.dot(_e1wrong) != 0, "検算が順番ミスを捕まえる")
in_text("$1$ つ目が $27+7-20 = 14 \\neq 0$ になって", "その値を本文に書いている")

E2v, E2w = vec(2, 0, -1), vec(1, 3, 2)
same(cross(E2v, E2w), vec(3, -5, 6), "演習2")
same(cross(E2w, E2v), vec(-3, 5, -6), "演習2 の入れかえ")
eq(E2v.dot(cross(E2v, E2w)), 0, "演習2 の垂直 1")
eq(E2w.dot(cross(E2v, E2w)), 0, "演習2 の垂直 2")
# 入れかえの検算は、2 行目の順番ミスを捕まえられない（本文で断っている）


def wrongcross(u, w):
    return vec(u[1] * w[2] - u[2] * w[1],
               u[0] * w[2] - u[2] * w[0],
               u[0] * w[1] - u[1] * w[0])


same(wrongcross(E2v, E2w), vec(3, 5, 6), "誤った 2 行目での v×w")
same(wrongcross(E2w, E2v), vec(-3, -5, -6), "誤った 2 行目での w×v")
same(wrongcross(E2w, E2v), -wrongcross(E2v, E2w),
     "誤答どうしでも符号違いになる（入れかえの検算では捕まらない）")
# この演習では v の 2 行目が 0 なので、v との内積は誤答でも 0 になる。
# 捕まえるのは w との内積のほう。
eq(E2v.dot(wrongcross(E2v, E2w)), 0,
   "v の 2 行目が 0 なので、v との内積では捕まらない")
eq(E2w.dot(wrongcross(E2v, E2w)), 30, "w との内積は 30 になる（捕まる）")
chk(E2w.dot(cross(E2v, E2w)) == 0 and E2w.dot(wrongcross(E2v, E2w)) != 0,
    "w との内積が、正誤を分ける")
in_text("**内積は、$\\mathbf{v}$ と $\\mathbf{w}$ の両方で出してください。**",
        "両方の内積を出させている（レビュー5）")
in_text("$\\mathbf{w}$ との内積が $3+15+12 = 30 \\neq 0$",
        "捕まえるのは w のほうだと書いている")

E3v, E3w = vec(2, 3, 1), vec(1, 0, 4)
same(cross(E3v, E3w), vec(12, -7, -3), "演習3")
eq(mag(cross(E3v, E3w)), sp.sqrt(202), "|v×w| = √202")
chk(sf3(sp.sqrt(202)) == 14.2, "3 桁で 14.2")
eq(E3v.dot(cross(E3v, E3w)), 0, "演習3 の垂直 1")
eq(E3w.dot(cross(E3v, E3w)), 0, "演習3 の垂直 2")
near(mag(E3v) * mag(E3w), 15.4272, msg="|v||w| = √238")
chk(float(sp.sqrt(202)) < float(mag(E3v) * mag(E3w)), "面積は |v||w| を超えない")
near(sp.sqrt(202) / 2, 7.1063, msg="1/2 を付けた誤答 7.11")

E4A, E4B, E4C = vec(2, 0, 1), vec(4, 3, 2), vec(1, 1, 4)
same(E4B - E4A, vec(2, 3, 1), "演習4 AB")
same(E4C - E4A, vec(-1, 1, 3), "演習4 AC")
same(cross(E4B - E4A, E4C - E4A), vec(8, -7, 5), "演習4 AB×AC")
eq(mag(cross(E4B - E4A, E4C - E4A)), sp.sqrt(138), "√138")
chk(sf3(sp.sqrt(138) / 2) == 5.87, "3 桁で 5.87")
same(E4A - E4C, vec(1, -1, -3), "演習4 CA")
same(E4B - E4C, vec(3, 2, -2), "演習4 CB")
same(cross(E4A - E4C, E4B - E4C), vec(8, -7, 5), "演習4 の検算（C から）")
not_in_text("頂点をそろえずに取っていたら、ここで合いません",
            "誤りだった検算の主張（レビュー1）")

E5P, E5Q, E5R = vec(2, 1, 0), vec(6, 3, 0), vec(3, 7, 0)
same(cross(E5Q - E5P, E5R - E5P), vec(0, 0, 22), "演習5 の外積")
eq(sp.Rational(22, 2), 11, "演習5 の面積 11")
_r5 = 4 * 6
_t5 = sp.Rational(1, 2) * 4 * 2 + sp.Rational(1, 2) * 1 * 6 \
    + sp.Rational(1, 2) * 3 * 4
eq(_r5 - _t5, 11, "囲い込み法でも 11")
chk(_r5 - _t5 != 22, "1/2 を忘れた 22 とは合わない")

E6v, E6w = vec(2, -4, 6), vec(-3, 6, -9)
same(cross(E6v, E6w), sp.zeros(3, 1), "演習6 は 0 ベクトル")
same(sp.Rational(-3, 2) * E6v, E6w, "k = -3/2 でそろう")
chk(mag(E6v) != 0 and mag(E6w) != 0, "どちらも 0 ベクトルでない")

E7a, E7b = vec(5, 2, 1), vec(1, 2, 2)
same(cross(E7a, E7b), vec(2, -9, 8), "演習7 の外積")
eq(mag(cross(E7a, E7b)), sp.sqrt(149), "√149")
eq(mag(E7b), 3, "|b| = 3")
near(sp.sqrt(149) / 3, 4.0688519, msg="演習7 の答え")
chk(sf3(sp.sqrt(149) / 3) == 4.07, "3 桁で 4.07")
eq(E7a.dot(E7b), 11, "a・b = 11")
eq(sp.Rational(11, 3)**2 + sp.Rational(149, 9), 30, "Pythagoras で 30")
eq(mag(E7a)**2, 30, "|a|² = 30")
near(sp.sqrt(149) / sp.sqrt(30), 2.2286, msg="|a| で割った誤答 2.23")
near(sp.Rational(11, 3)**2 + sp.Rational(149, 30), 18.4111,
     msg="誤答では 18.4（30 にならない）")
chk(abs(float(sp.Rational(11, 3)**2 + sp.Rational(149, 30)) - 30) > 1,
    "誤答は Pythagoras で落ちる")
in_text("\\left(\\frac{11}{3}\\right)^2 + \\left(\\frac{\\sqrt{149}}{3}\\right)^2"
        " = \\frac{121+149}{9} = 30", "分数で書き直した検算（レビュー15）")
not_in_text("$3.667^2 + 4.069^2 = 13.44 + 16.56 = 30$", "小数を混ぜていた式")

E8v, E8w = vec(1, -2, 2), vec(-2, 2, 1)
same(cross(E8v, E8w), vec(-6, -5, -2), "演習8 の外積")
eq(mag(cross(E8v, E8w)), sp.sqrt(65), "√65")
eq(mag(E8v), 3, "|v| = 3")
eq(mag(E8w), 3, "|w| = 3")
eq(E8v.dot(E8w), -4, "v・w = -4")
near(sp.deg(sp.asin(sp.sqrt(65) / 9)), 63.6122000, msg="sin⁻¹ の値")
chk(sf3(sp.deg(sp.asin(sp.sqrt(65) / 9))) == 63.6, "3 桁で 63.6")
near(ang(E8v, E8w), 116.3878000, msg="正しい角")
chk(sf3(ang(E8v, E8w)) == 116.0, "116.39 は 3 桁で 116")
eq(sp.simplify((sp.sqrt(65) / 9)**2 + sp.Rational(-4, 9)**2), 1,
   "sin²+cos² = 1")
chk(E8v.dot(E8w) < 0, "内積が負なので鈍角")
# 丸めてから acos に入れると 116.38 になる
near(sp.deg(sp.acos(sp.Float("-0.4444"))), 116.3849573,
     msg="-0.4444 に丸めてから入れた値")
chk(round(float(sp.deg(sp.acos(sp.Float("-0.4444")))), 2)
    != round(float(ang(E8v, E8w)), 2), "丸めると 2 桁小数で食い違う")
in_text("$-0.4444$ に丸めてから入れると $116.38^{\\circ}$ になります",
        "丸めの注意（レビュー7）")
not_in_text("$\\cos^{-1}(-0.4444) = 116.39^{\\circ}$", "丸めた値を入れていた式")

E9v, E9w = vec(3, 1, -1), vec(2, -2, 4)
eq(E9v.dot(E9w), 0, "演習9 は垂直")
same(cross(E9v, E9w), vec(2, -14, -8), "演習9 の外積")
eq(mag(cross(E9v, E9w)), 2 * sp.sqrt(66), "2√66")
eq(sp.simplify(mag(cross(E9v, E9w)) - mag(E9v) * mag(E9w)), 0,
   "垂直なので |v×w| = |v||w|")
near(mag(cross(E9v, E9w)), 16.2480768, msg="√264 の小数")
_e9wrong = vec(2, 14, -8)
eq(E9v.dot(_e9wrong), 28, "2 行目の符号を逆にすると内積 28")
eq(mag(_e9wrong), 2 * sp.sqrt(66), "その誤答でも大きさは同じ（大きさでは捕まらない）")
in_text("$\\mathbf{v}$ との内積が $6 + 14 + 8 = 28 \\neq 0$ になって見つかります",
        "その値を本文に書いている")

E10v, E10w = vec(2, 3, 1), vec(4, -1, 5)
same(cross(E10v, E10w), vec(16, -6, -14), "演習10 の正しい答え")
same(wrongcross(E10v, E10w), vec(16, 6, -14), "生徒の答え")
eq(E10v.dot(vec(16, 6, -14)), 36, "生徒の答えでは内積が 36")
eq(E10v.dot(vec(16, -6, -14)), 0, "正しい答えでは 0")
eq(E10w.dot(vec(16, -6, -14)), 0, "w との内積も 0")
chk(E10v.dot(vec(16, 6, -14)) != 0, "検算が生徒の誤りを捕まえる")
eq(sp.Rational(1, 1) * (1 * 4 - 2 * 5), -6, "正しい 2 行目 v3w1-v1w3 = -6")
eq(sp.Rational(1, 1) * (2 * 5 - 1 * 4), 6, "生徒の 2 行目 v1w3-v3w1 = 6")

# ══════════════════════════════════════════════════════════
# 5. 境目の主張が正しいか
# ══════════════════════════════════════════════════════════
# 0 ベクトルを入れると、平行の同値が崩れる
same(cross(sp.zeros(3, 1), vec(1, 2, 3)), sp.zeros(3, 1),
     "0×w = 0（けれど平行とは言わない）")
in_text("$\\mathbf{0}$ は向きを持たないので「平行」とは言いません",
        "0 ベクトルの断り")
in_text("| $0$ になるのは（どちらも $\\mathbf{0}$ でないとき） |",
        "くらべ表の条件（レビュー8）")
not_in_text("| $0$ になるのは | **垂直**のとき | **平行**のとき |",
            "無条件だった行（レビュー8）")
not_in_text("| 大きさ | $\\lvert \\mathbf{v} \\rvert \\lvert \\mathbf{w} \\rvert"
            " \\cos\\theta$", "cosθ を「大きさ」と呼んでいた行（レビュー8）")
in_text("### 3. $\\mathbf{v} \\times \\mathbf{w}$ は、$\\mathbf{0}$ でなければ両方に垂直です",
        "見出しの条件（レビュー14）")
in_text("$\\mathbf{v}$ と $\\mathbf{w}$ が平行のとき、またはどちらかが $\\mathbf{0}$ のとき",
        "n が決まらない条件（レビュー12）")
# sinθ >= 0 は 0..180 で正しい
chk(all(float(sp.sin(sp.rad(d))) >= -1e-12 for d in range(0, 181)),
    "0..180 で sinθ >= 0")

# ══════════════════════════════════════════════════════════
# 6. 公式集とシラバスの引用
# ══════════════════════════════════════════════════════════
in_text("Definition and calculation of the vector product of two vectors.",
        "Content の引用 1")
in_text("Geometric interpretation of $\\lvert \\mathbf{v} \\times \\mathbf{w}"
        " \\rvert$.", "Content の引用 2")
in_text("Components of vectors.", "Content の引用 3")
in_text("is the unit normal vector whose direction is given by the right-hand"
        " screw rule.", "Guidance の引用 1")
in_text("Use of $\\lvert \\mathbf{v} \\times \\mathbf{w} \\rvert$ to find the"
        " area of a parallelogram (and hence a triangle).", "Guidance の引用 2")
in_text("acting perpendicular to vector $\\mathbf{b}$, in the plane formed by"
        " the two vectors", "Guidance の引用 3")
in_text("**Not required:** generalized properties and proofs of scalar and"
        " cross product.", "Not required の引用")
in_text("公式集にありません", "|a×b|/|b| が公式集にないこと")
in_text("覚える必要はありません", "公式集にあるものを暗記させていない")
in_text("`(and hence a triangle)` はシラバスの Guidance にあります",
        "三角形は Guidance だと書いている")
chk(TEXT.count("ahl-3-13a.qmd") >= 8, "3.13a への後方リンクがある")
# 3.13a の内容をこのページで重ねて説明していないか
for banned in ["\\cos\\theta = \\frac{v_1w_1", "acute angle between two lines"]:
    not_in_text(banned, "3.13a の内容をこのページに持ち込んでいない")

# ══════════════════════════════════════════════════════════
# 7. GDC の記述
# ══════════════════════════════════════════════════════════
in_text("menu → 7: Matrix & Vector → C: Vector", "crossP の場所")
in_text("crossP([2;-1;2],[4;3;0])", "crossP の例")
in_text("`ctrl` を押してから `var`", "ストアの押し方")
in_text("menu → Actions → Clear a-z", "変数を消す")
in_text("doc → Settings → Document Settings", "角度設定")
in_text("`ctrl` を押してから `x²`", "√ のテンプレート")
for bad in ["nDeriv(", "nDerivative(", "unitV(", "solve("]:
    not_in_text(bad, "非 CAS にない命令")
chk("norm(" not in TEXT, "norm( を勧めていない")
not_in_text("$3$ 成分でなければ受け付けません", "未確認だった主張（レビュー3）")
not_in_text("と打つと、エラーになります", "未確認だった主張（レビュー3）")
in_text("これが $10\\sqrt{2}$ の小数です", "電卓は小数を返す（レビュー18）")
not_in_text("$14.142\\ldots$、つまり $10\\sqrt{2}$ が返ります",
            "電卓が根号を返すように読めた書き方")
in_text("**ただし $2$ 次元（第 $3$ 成分が $0$）のときは別です。**",
        "2 次元では内積の検算が効かないこと（レビュー13）")
# 2 次元では、3 行目を何にしても内積が 0 になる
_2dv, _2dw = vec(4, 1, 0), vec(1, 5, 0)
for z in (19, 17, -3, 0):
    eq(_2dv.dot(vec(0, 0, z)), 0, f"2 次元では z={z} でも内積 0")
    eq(_2dw.dot(vec(0, 0, z)), 0, f"2 次元では z={z} でも内積 0（w）")
near(sp.rad(70.5287794), 1.2309594, msg="70.5° は 1.231 rad（本文 1.23）")
in_text("$70.5$ ではなく $1.23$ が返ります", "角度設定の注意（レビュー20）")

# ══════════════════════════════════════════════════════════
# 8. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6,
    "--- は 6 本（front matter 2 + 例題 4）")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("</details>") == 14, "</details> も 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.model-answer}") == 6, "model-answer が 6")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(len(re.findall(r"^::: \{#exm-ahl313b-", TEXT, re.M)) == 4, "例題が 4")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Worked examples", "Common errors",
         "Using your GDC (TI-Nspire CX II)", "Exercises"]
chk([h for h in _h2 if h in _want] == _want, "6 つの見出しが所定の順")
_idea = [int(m) for m in re.findall(r"^### (\d+)\. .*\{#(?!gdc-)", TEXT, re.M)]
chk(_idea == list(range(1, 10)), f"The idea が 1..9 で連番: {_idea}")
_gdc = [int(m) for m in re.findall(r"^### (\d+)\. .*\{#gdc-", TEXT, re.M)]
chk(_gdc == list(range(1, 7)), f"GDC が 1..6 で連番: {_gdc}")
chk(TEXT.count("**検算") >= 14, "検算が十分ある")
chk("**確かめ。**" not in TEXT and "**確かめます。**" not in TEXT,
    "検算の見出しに「確かめ。」を使っていない")
for word in ["誰でもできる", "簡単です", "当然", "明らか", "もちろん",
             "当たり前", "そのとおり"]:
    not_in_text(word, "禁止語")
# ✓ ✗ が数式の中に入っていないか
for _blk in re.findall(r"\$\$(.*?)\$\$", TEXT, re.S):
    chk("✓" not in _blk and "✗" not in _blk,
        "表示数式の中に ✓/✗ がある: " + _blk[:40])
for _blk in re.findall(r"(?<!\$)\$([^$\n]+)\$(?!\$)", TEXT):
    chk("✓" not in _blk and "✗" not in _blk,
        "インライン数式の中に ✓/✗ がある: " + _blk[:40])
# 解答例と model-answer に日本語が混ざっていないか
for _blk in re.findall(r"::: \{\.model-answer\}(.*?):::", TEXT, re.S):
    _body = _blk.replace("**試験ではこう書く**", "")
    chk(not re.search(r"[ぁ-んァ-ン一-龥]", _body),
        "model-answer に日本語が混ざっている: " + _body[:40])
# ページ内アンカーが全部あるか
_anchors = set(re.findall(r"\{#([a-z0-9-]+)\}", TEXT))
for _a in set(re.findall(r"\]\(#([a-z0-9-]+)\)", TEXT)):
    chk(_a in _anchors or _a in {"why-it-works", "common-errors"},
        "ページ内リンク先がない: #" + _a)
# 他ページへの @-ref が混ざっていないか
for _r in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r == "ahl313b", "他ページの @-ref を使っている: " + _r)
# 他ページへのリンク先ファイルが実在するか
for _f in set(re.findall(r"\]\((\.\./)?([a-z0-9/-]+\.qmd)#", TEXT)):
    _path = os.path.join(BASE, _f[0] + _f[1]) if _f[0] else \
        os.path.join(BASE, _f[1])
    chk(os.path.exists(_path), "リンク先のファイルがない: " + _f[1])

# ══════════════════════════════════════════════════════════
# 9. 図
# ══════════════════════════════════════════════════════════
for name in ["ahl-3-13b-idea.svg", "ahl-3-13b-area.svg",
             "ahl-3-13b-component.svg"]:
    chk(os.path.exists(os.path.join(BASE, "img", name)), "図がある: " + name)
    chk("](img/" + name + ")" in TEXT, "本文が図を貼っている: " + name)
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
in_fig("\\binom", "図は binom を使う")
# 図 1・2 の数値（v=(3,0), w=(1,2) → 面積 6、三角形 3）
same(cross(vec(3, 0, 0), vec(1, 2, 0)), vec(0, 0, 6), "図の v×w は (0,0,6)")
in_fig("= |\\\\mathbf{v}\\\\times\\\\mathbf{w}| = 6", "図2 の面積 6")
in_fig("\\\\frac{1}{2}|\\\\mathbf{v}\\\\times\\\\mathbf{w}|", "図2 の三角形")
in_fig("$=|\\\\mathbf{w}|\\\\sin\\\\theta = 2$", "図2 の高さ 2")
in_fig("base $=|\\\\mathbf{v}| = 3$", "図2 の底辺 3")
in_fig("drawn shorter than its true length", "縮尺を断っている（レビュー11）")
in_fig("the other\\nhalf", "図2(b) のラベル（レビュー10）")
# 図 3 の数値（3.13a と同じ a, b）
same(cross(vec(-1, 6, 0), vec(4, 3, 0)), vec(0, 0, -27), "図3 の a×b")
in_fig("{|\\\\mathbf{b}|} = 5.4", "図3 の垂直な成分")
in_fig("{|\\\\mathbf{b}|} = 2.8", "図3 の平行な成分")
in_fig("$2.8^2 + 5.4^2 = 37 = |\\\\mathbf{a}|^2$", "図3 の Pythagoras")
# 3.13a の図と同じ a, b であること
A13 = open(os.path.join(HERE, "make_ahl_3_13a.py"), encoding="utf-8").read()
chk("(-1, 6), (4, 3)" in A13, "3.13a の図も a=(-1,6), b=(4,3) を使っている")
in_text("**同じ $\\mathbf{a}$、$\\mathbf{b}$**", "同じ図だと書いている")
# 図が演習の答えを漏らしていないか
for leak in ["14.2", "5.87", "4.07", "63.6", "116", "9.5", "22", "$11",
             "(9, -7", "(3, -5", "(12, -7", "(8, -7", "(2, -9", "(-6, -5",
             "(2, -14", "(16, -6"]:
    chk(leak not in FIGSTR, "図が演習の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 10. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(HERE, "..", "..", "_quarto-draft.yml"),
             encoding="utf-8").read()
chk("ai-hl/03-geometry-and-trigonometry/ahl-3-13b.qmd" in DRAFT,
    "_quarto-draft.yml に登録されている")
chk(DRAFT.index("ahl-3-13a.qmd") < DRAFT.index("ahl-3-13b.qmd")
    < DRAFT.index("ahl-3-14.qmd"), "サイドバーの並びが 3.13a → 3.13b → 3.14")
PUB = open(os.path.join(HERE, "..", "..", "_quarto.yml"), encoding="utf-8").read()
chk("ahl-3-13b" not in PUB, "公開用の _quarto.yml は SL だけのまま")
IDX = open(os.path.join(HERE, "..", "..", "ai-hl", "index.qmd"),
           encoding="utf-8").read()
chk("[AHL 3.13b — The vector product]"
    "(03-geometry-and-trigonometry/ahl-3-13b.qmd)" in IDX, "index の一覧にある")
_row = [x for x in re.findall(r"^\| (?:\*\*)?AHL [0-9.]+(?:\*\*)? \|(.*)\|$",
                              IDX, re.M) if "ahl-3-13b.qmd" in x]
chk(len(_row) == 1 and "✅" in _row[0] and "ahl-3-13a.qmd" in _row[0],
    "AHL 3.13 の行が、両方へのリンクと ✅ を持つ")
_rows = re.findall(r"^\| (?:\*\*)?AHL [0-9.]+(?:\*\*)? \|(.*)\|$", IDX, re.M)
_left_rows = [x for x in _rows if "✅" not in x]
_m = re.search(r"残りの(\d+)項目", IDX)
if _m:
    chk(int(_m.group(1)) == len(_left_rows),
        "「残りの N 項目」が、まだ ✅ の付いていない行の数と合う")
else:
    chk(len(_left_rows) == 0,
        "「残りの N 項目」が無いなら、全部の行に ✅ が付いている")
GLO = open(os.path.join(HERE, "..", "..", "glossary-ai.qmd"),
           encoding="utf-8").read()
for term in ["| vector product |", "| cross product |",
             "| unit normal vector |", "| right-hand screw rule |",
             "| parallelogram |", "| adjacent sides |",
             "| area of a parallelogram |", "| torque |",
             "| in exact form |"]:
    chk(term in GLO, "対訳表にある: " + term)

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
