"""AHL 3.13a（scalar product）の内容を検算する。

    python3 figs/ai-hl/check_ahl_3_13a.py

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
QMD = os.path.join(BASE, "ahl-3-13a.qmd")
TEXT = open(QMD, encoding="utf-8").read()
FIG = open(os.path.join(HERE, "make_ahl_3_13a.py"), encoding="utf-8").read()
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


def ang(u, v):
    """u, v のあいだの角（度）。acos は主値なので 0..180 に入る。"""
    return sp.deg(sp.acos(u.dot(v) / (mag(u) * mag(v))))


def eq(a, b, msg=""):
    chk(sp.simplify(a - b) == 0, msg + f"  ({a} vs {b})")


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
# 0. 定義そのもの — 成分形と幾何形が一致するか
# ══════════════════════════════════════════════════════════
# 乱数ではなく、格子点をひととおり回して、公式集の 2 つの形が
# 同じ数を与えることを確かめる（Why it works の主張）。
_bad = 0
for a1 in range(-3, 4):
    for a2 in range(-3, 4):
        for b1 in range(-3, 4):
            for b2 in range(-3, 4):
                u, v = vec(a1, a2), vec(b1, b2)
                if u.norm() == 0 or v.norm() == 0:
                    continue
                lhs = u.dot(v)
                rhs = mag(u) * mag(v) * sp.cos(sp.acos(
                    sp.Rational(lhs, 1) / (mag(u) * mag(v))))
                if sp.simplify(lhs - rhs) != 0:
                    _bad += 1
chk(_bad == 0, "成分形と |v||w|cosθ が、すべての格子点で一致する")

# v.v = |v|^2
for u in [vec(3, 4), vec(1, 2, 2), vec(-6, 3), vec(2, -1, 4)]:
    eq(u.dot(u), mag(u)**2, "v・v = |v|²")

# 順番を入れかえても同じ（本文の検算の根拠）
for u, v in [(vec(3, 4), vec(2, -5)), (vec(2, -1, 4), vec(3, 6, 1))]:
    eq(u.dot(v), v.dot(u), "v・w = w・v")

# (kv)・w = k(v・w)（第9節・Why it works で使う）
_k = sp.Symbol("k")
_u, _v = vec(3, 4), vec(2, -5)
eq(sp.expand((_k * _u).dot(_v)), sp.expand(_k * _u.dot(_v)), "(kv)・w = k(v・w)")

# ══════════════════════════════════════════════════════════
# 1. 例題 1 — 内積そのもの
# ══════════════════════════════════════════════════════════
V, W = vec(3, 4), vec(2, -5)
P, Q = vec(1, 2, 2), vec(4, 0, -3)
eq(V.dot(W), -14, "例題1(a) v・w = -14")
eq(P.dot(Q), -2, "例題1(b) p・q = -2")
eq(vec(6, 3).dot(vec(-1, 2)), 0, "例題1(c) 垂直")
eq(P.dot(P), 9, "例題1(d) p・p = 9")
eq(mag(P), 3, "例題1(d) |p| = 3")
in_text("\\mathbf{v} \\cdot \\mathbf{w} = 3(2) + 4(-5) = 6 - 20 = -14",
        "例題1(a) の式")
in_text("\\mathbf{p} \\cdot \\mathbf{q} = 1(4) + 2(0) + 2(-3) = 4 + 0 - 6 = -2",
        "例題1(b) の式")

# 例題1(d) の検算：後ろ 2 成分だけの長さが下限になるか、
# そしてそれが「2 乗し忘れ」を本当にはじくか
eq(mag(vec(2, 2)), 2 * sp.sqrt(2), "後ろ 2 成分の長さ")
near(mag(vec(2, 2)), 2.82842, msg="2√2 の小数（本文 2.83）")
chk(float(mag(P)) >= float(mag(vec(2, 2))), "正しい |p| は下限を満たす")
_wrong_pp = 1 + 2 + 2                       # かけ算をせずに足した誤り
near(sp.sqrt(_wrong_pp), 2.23607, msg="誤答 √5 の小数（本文 2.24）")
chk(float(sp.sqrt(_wrong_pp)) < float(mag(vec(2, 2))),
    "誤答 √5 は下限 2.83 を下回る（検算が本当にはじく）")
in_text("$3 \\geq 2.83$", "例題1(d) の検算の不等式")
not_in_text("$2$ 通りで同じ $3$ になりました",
            "循環していた検算（レビュー16）")

# ══════════════════════════════════════════════════════════
# 2. 例題 2 — 角
# ══════════════════════════════════════════════════════════
eq(mag(V), 5, "|v| = 5")
eq(mag(W), sp.sqrt(29), "|w| = √29")
eq(mag(Q), 5, "|q| = 5")
near(V.dot(W) / (mag(V) * mag(W)), -0.5199469, msg="cosθ (2D)")
near(ang(V, W), 121.3286929, msg="例題2(a) の角")
chk(sf3(ang(V, W)) == 121.0, "121.32… は 3 桁で 121")
near(ang(P, Q), 97.66225566, msg="例題2(b) の角")
chk(sf3(ang(P, Q)) == 97.7, "97.66… は 3 桁で 97.7")
eq(P.dot(Q) / (mag(P) * mag(Q)), sp.Rational(-2, 15), "cosθ = -2/15")

# 検算(a)：|w| を 29 としたときに何が起きるか
_wrong_ang = sp.deg(sp.acos(sp.Rational(-14, 145)))
near(_wrong_ang, 95.5406377, msg="|w|=29 のときに出る角")
_back = 5 * sp.sqrt(29) * sp.cos(sp.rad(_wrong_ang))
near(_back, -2.5997347, msg="正しい大きさで戻したときの値（本文 -2.60）")
chk(abs(float(_back) - (-14)) > 1, "誤りの道すじは -14 に戻らない（検算が効く）")
# 同じ誤りを、誤った大きさのまま戻すと -14 に戻ってしまう（循環）ことも記録
near(5 * 29 * sp.cos(sp.rad(_wrong_ang)), -14, tol=1e-6,
     msg="誤った大きさのまま戻すと -14（だからそう書いてはいけない）")
not_in_text("ここで $-75.4$ になり", "循環していた検算（レビュー1）")
in_text("$\\theta = 95.5^{\\circ}$ を出していたら、正しい $5\\sqrt{29}$ で戻したとき"
        " $-2.60$ になり", "例題2(a) の直した検算")

# 検算(b)：符号を落とすと 82.3°
near(sp.deg(sp.acos(sp.Rational(2, 15))), 82.3377443, msg="符号を落とした誤答")
chk(float(sp.deg(sp.acos(sp.Rational(2, 15)))) < 90
    < float(ang(P, Q)), "符号の有無で 90° をまたぐ（検算が効く）")

# 第4節の「途中で丸めない」例
near(sp.deg(sp.acos(sp.Rational(-1, 2))), 120, msg="acos(-0.5) は 120°")
chk(sf3(sp.deg(sp.acos(sp.Rational(-1, 2)))) != sf3(ang(V, W)),
    "-0.5 に丸めた 120° は、正しい 121° と 3 桁で食い違う")
# 直す前に書いていた -0.520 は、3 桁でも 2 桁小数でも区別が付かない
near(sp.deg(sp.acos(sp.Float("-0.520"))), 121.3322508, msg="acos(-0.520)")
chk(round(float(sp.deg(sp.acos(sp.Float("-0.520")))), 2)
    == round(float(ang(V, W)), 2), "-0.520 では差が出ない（だから例を変えた）")
not_in_text("$-0.520$ に丸めてから", "効かない丸めの例（レビュー2）")

# ══════════════════════════════════════════════════════════
# 3. 例題 3 — 2 直線のあいだの acute angle
# ══════════════════════════════════════════════════════════
D1, D2 = vec(2, 3), vec(-4, 1)
eq(D1.dot(D2), -5, "d1・d2 = -5")
eq(mag(D1) * mag(D2), sp.sqrt(221), "|d1||d2| = √221")
near(ang(D1, D2), 109.6538241, msg="方向ベクトルのあいだの角")
chk(round(float(ang(D1, D2)), 1) == 109.7, "1 桁小数で 109.7")
near(180 - ang(D1, D2), 70.3461759, msg="acute angle")
chk(sf3(180 - ang(D1, D2)) == 70.3, "3 桁で 70.3")
# -d1 でやり直しても同じ acute angle（例題3の検算）
eq((-D1).dot(D2), 5, "(-d1)・d2 = 5")
near(ang(-D1, D2), 70.3461759, msg="-d1 でやり直した角")
chk(abs(float(ang(-D1, D2)) - float(ang(D1, D2))) > 30,
    "-d1 の角は d1 の角と別（検算が同じ計算の繰り返しでない）")
# 先に丸めてから引くと 70 になってしまう
chk(180 - round(float(ang(D1, D2))) == 70, "110 から引くと 70（本文の警告）")
chk(sf3(180 - ang(D1, D2)) != 70.0, "正しい答えは 70 ではない")

E1, E2 = vec(1, 2, 2), vec(2, -1, 2)
eq(E1.dot(E2), 4, "3D の d1・d2 = 4")
eq(mag(E1), 3, "|d1| = 3")
eq(mag(E2), 3, "|d2| = 3")
eq(E1.dot(E2) / (mag(E1) * mag(E2)), sp.Rational(4, 9), "cosθ = 4/9")
near(ang(E1, E2), 63.6122000, msg="例題3(c) の角")
chk(sf3(ang(E1, E2)) == 63.6, "3 桁で 63.6")
chk(float(ang(E1, E2)) < 90, "正なのでもう鋭角（180 から引かない）")
# 検算：cos 60° = 1/2 との比較が本当に効くか
chk(sp.Rational(4, 9) < sp.Rational(1, 2), "4/9 < 1/2 なので 60° より大きい")
near(sp.deg(sp.acos(sp.Rational(4, 6))), 48.1896851, msg="|d1||d2| を 6 とした誤答")
chk(float(sp.deg(sp.acos(sp.Rational(4, 6)))) < 60,
    "誤答 48.2° は 60° より小さい（検算が効く）")

# 境目：垂直と平行
chk(vec(1, 0).dot(vec(0, 1)) == 0, "垂直な方向ベクトル")
near(ang(vec(1, 0), vec(0, 1)), 90, msg="垂直なら 90°")
near(ang(vec(2, 3), vec(4, 6)), 0, msg="平行なら 0°")
in_text("垂直なら $90^{\\circ}$、平行なら $0^{\\circ}$ が返ります",
        "1 行の形の境目の注意（レビュー14）")

# ══════════════════════════════════════════════════════════
# 4. 例題 4 — b の向きの成分
# ══════════════════════════════════════════════════════════
A, B = vec(4, 7), vec(3, -4)
eq(A.dot(B), -16, "a・b = -16")
eq(mag(B), 5, "|b| = 5")
eq(mag(A), sp.sqrt(65), "|a| = √65")
eq(A.dot(B) / mag(B), sp.Rational(-16, 5), "例題4(a) = -3.2")
near(A.dot(B) / mag(A), -1.9845558, msg="例題4(b)")
chk(sf3(A.dot(B) / mag(A)) == -1.98, "3 桁で -1.98")
chk(sp.simplify(A.dot(B) / mag(B) - A.dot(B) / mag(A)) != 0,
    "(a) と (b) は別の数")
near(A.dot(B) / (mag(A) * mag(B)), -0.3969107, msg="cosθ（本文 -0.39691）")
in_text("\\approx -0.39691", "例題4 の cosθ の桁（レビュー11）")
not_in_text("\\approx -0.39693", "丸めが違っていた値")
near(mag(A), 8.0622577, msg="√65 の小数（本文 8.0623）")
near(sp.Float("8.0623") * sp.Float("-0.39691"), -3.2, tol=2e-4,
     msg="|a|cosθ が -3.2 に戻る")
# |a|cosθ は (a・b)/|b| と恒等的に等しい ＝ 内積そのものは検算できない
eq(sp.simplify(mag(A) * (A.dot(B) / (mag(A) * mag(B))) - A.dot(B) / mag(B)), 0,
   "|a|cosθ ≡ (a・b)/|b|（本文が「独立でない」と書いている根拠）")
in_text("内積 $-16$ そのものは、どちらの道でも同じものを使っています",
        "独立性を言い過ぎない書き方（レビュー17）")
not_in_text("**この $2$ 通りは別の道すじです。**", "言い過ぎだった文（レビュー17）")

F3, D3 = vec(6, 2, 3), vec(2, -1, 2)
eq(F3.dot(D3), 16, "例題4(c) の内積")
eq(mag(D3), 3, "|d| = 3")
eq(mag(F3), 7, "|F| = 7")
near(sp.Rational(16, 3), 5.3333333, msg="例題4(c) = 16/3")
chk(sf3(sp.Rational(16, 3)) == 5.33, "3 桁で 5.33")
chk(float(sp.Rational(16, 3)) < float(mag(F3)), "成分は元の長さを超えない")
near(sp.Rational(16, 7), 2.2857143, msg="|a| で割った誤答 16/7")
chk(float(sp.Rational(16, 7)) < float(mag(F3)),
    "誤答も 7 未満（＝この検算だけでは足りない、と本文が書いているとおり）")
in_text("この検算だけでは足りません", "検算の限界を明記している")
near(sp.deg(sp.acos(A.dot(B) / (mag(A) * mag(B)))), 113.3852211,
     msg="例題4(d) の角")
chk(sf3(sp.deg(sp.acos(A.dot(B) / (mag(A) * mag(B))))) == 113.0,
    "3 桁で 113")

# ══════════════════════════════════════════════════════════
# 5. 演習 1〜10
# ══════════════════════════════════════════════════════════
eq(vec(7, -2).dot(vec(3, 5)), 11, "演習1")
chk(vec(7, -2).dot(vec(3, 5)) > 0, "演習1 は正（鋭角）")
near(ang(vec(7, -2), vec(3, 5)), 74.9816394, msg="演習1 の角（鋭角の裏付け）")

eq(vec(2, -1, 4).dot(vec(3, 6, 1)), 4, "演習2")
# 演習2 の検算：項の順を逆にすると、打ち消し合う 2 項が先頭でなくなる
eq(4 * 1 + (-1) * 6 + 2 * 3, 4, "演習2 の逆順の和")
chk((2 * 3) + (-1 * 6) == 0, "先頭 2 項は打ち消し合う（誤りの入り口）")
chk((4 * 1) + (-1 * 6) != 0, "逆順では先頭 2 項が打ち消し合わない（検算が効く）")
not_in_text("順番を入れかえます。$3(2) + 6(-1) + 1(4)",
            "順序を保存していた検算（レビュー6）")

R3A, R3B = vec(5, 2), vec(-1, 4)
eq(R3A.dot(R3B), 3, "演習3 の内積")
eq(mag(R3A) * mag(R3B), sp.sqrt(493), "演習3 の |v||w|")
near(ang(R3A, R3B), 82.2348340, msg="演習3 の角")
chk(sf3(ang(R3A, R3B)) == 82.2, "演習3 は 3 桁で 82.2")
near(sp.deg(sp.acos(3 / sp.sqrt(46))), 63.7476249,
     msg="大きさを足した誤答（本文 63.7）")
chk(abs(float(sp.deg(sp.acos(3 / sp.sqrt(46)))) - float(ang(R3A, R3B))) > 15,
    "足し算の誤りは大きくずれる（検算が効く）")

R4A, R4B = vec(3, 0, 4), vec(1, 2, 2)
eq(R4A.dot(R4B), 11, "演習4 の内積")
eq(mag(R4A), 5, "演習4 |v| = 5")
eq(mag(R4B), 3, "演習4 |w| = 3")
near(ang(R4A, R4B), 42.8334281, msg="演習4 の角")
chk(sf3(ang(R4A, R4B)) == 42.8, "演習4 は 3 桁で 42.8")
# 0 の成分を落とした誤り：|v| も内積も変わらず、|w| だけ √5 になる
eq(vec(3, 4).dot(vec(1, 2)), 11, "0 を落としても内積は 11 のまま")
eq(mag(vec(3, 4)), 5, "0 を落としても |v| は 5 のまま")
near(sp.deg(sp.acos(11 / (5 * sp.sqrt(5)))), 10.3048465,
     msg="0 を落とした誤答（本文 10.3）")
chk(sf3(sp.deg(sp.acos(11 / (5 * sp.sqrt(5))))) == 10.3, "誤答は 3 桁で 10.3")
not_in_text("$\\theta = 10.2^{\\circ}$", "丸めが違っていた誤答の値")

_k = sp.Symbol("k")
_e5 = vec(_k, 4).dot(vec(_k, -9))
eq(sp.expand(_e5), _k**2 - 36, "演習5 の方程式")
chk(sorted(sp.solve(_e5, _k)) == [-6, 6], "演習5 の解は ±6")
for _kv in (6, -6):
    eq(vec(_kv, 4).dot(vec(_kv, -9)), 0, f"演習5 k={_kv} で内積 0")
    chk(mag(vec(_kv, 4)) != 0 and mag(vec(_kv, -9)) != 0,
        f"演習5 k={_kv} でどちらも 0 ベクトルでない")
in_text("$k = -6$：$\\begin{pmatrix} -6 \\\\ 4 \\end{pmatrix}",
        "演習5 の検算が成分に戻っている（レビュー19）")

S1, S2 = vec(1, 5), vec(3, -1)
eq(S1.dot(S2), -2, "演習6 の内積")
eq(mag(S1) * mag(S2), sp.sqrt(260), "演習6 の |d1||d2|")
near(ang(S1, S2), 97.1250163, msg="演習6 の方向ベクトルの角")
near(180 - ang(S1, S2), 82.8749837, msg="演習6 の acute angle")
chk(sf3(180 - ang(S1, S2)) == 82.9, "演習6 は 3 桁で 82.9")
near(ang(-S1, S2), 82.8749837, msg="演習6 の検算（-d1 でやり直す）")
chk(abs(float(ang(-S1, S2)) - float(ang(S1, S2))) > 10,
    "-d1 の角は別（検算が繰り返しでない）")

E7A, E7B = vec(9, 2), vec(4, 3)
eq(E7A.dot(E7B), 42, "演習7 の内積")
eq(mag(E7B), 5, "演習7 |b| = 5")
eq(E7A.dot(E7B) / mag(E7B), sp.Rational(42, 5), "演習7 = 8.4")
eq(mag(E7A), sp.sqrt(85), "演習7 |a| = √85")
near(mag(E7A), 9.2195445, msg="√85 の小数（本文 9.22）")
chk(float(sp.Rational(42, 5)) < float(mag(E7A)), "8.4 < 9.22")
near(E7A.dot(E7B) / mag(E7A), 4.5555396, msg="|a| で割った誤答（本文 4.56）")
chk(float(E7A.dot(E7B) / mag(E7A)) < float(mag(E7A)),
    "誤答も 9.22 未満（＝幅の検算では見つからない、と本文が書くとおり）")
near(E7A.dot(E7B) / (mag(E7A) * mag(E7B)), 0.9111079, msg="演習7 の cosθ")
near(mag(E7A) * (E7A.dot(E7B) / (mag(E7A) * mag(E7B))), sp.Rational(42, 5),
     msg="|a|cosθ で 8.4 に戻る（誤答 4.56 とは合わない）")

PA, PB, PC = vec(1, 2), vec(5, 4), vec(3, 8)
AB, BC, CA = PB - PA, PC - PB, PA - PC
chk(list(AB) == [4, 2], "演習8 AB")
chk(list(BC) == [-2, 4], "演習8 BC")
chk(list(CA) == [-2, -6], "演習8 CA")
eq(AB.dot(BC), 0, "演習8 AB・BC = 0")
eq((-AB).dot(BC), 0, "演習8 BA・BC = 0（符号を変えても 0）")
eq(AB.dot(PC - PA), 20, "演習8 AB・AC = 20（A では直角でない）")
eq(CA.dot(PB - PC), 20, "演習8 CA・CB = 20（C でも直角でない）")
chk(AB.dot(PC - PA) != 0 and CA.dot(PB - PC) != 0 and AB.dot(BC) == 0,
    "直角は B だけ（(c) の主張の根拠）")
eq(mag(AB)**2 + mag(BC)**2, mag(CA)**2, "演習8 の Pythagoras 20+20=40")
chk(mag(CA) > mag(AB) and mag(CA) > mag(BC), "CA がいちばん長い辺")
in_text("$\\overrightarrow{BA} = -\\overrightarrow{AB}$, so"
        " $\\overrightarrow{BA} \\cdot \\overrightarrow{BC} = 0$ as well",
        "演習8(b) の解答例が頂点 B を正しく扱う（レビュー19）")

FF, DD = vec(12, -5), vec(4, 3)
eq(FF.dot(DD), 33, "演習9 の仕事 33")
eq(mag(FF), 13, "|F| = 13")
eq(mag(DD), 5, "|d| = 5")
eq(FF.dot(DD) / (mag(FF) * mag(DD)), sp.Rational(33, 65), "演習9 の cosθ")
near(ang(FF, DD), 59.4897626, msg="演習9 の角")
chk(sf3(ang(FF, DD)) == 59.5, "演習9 は 3 桁で 59.5")
# 検算：x 軸となす角の差（内積を使わない別の道すじ）
_aF = sp.deg(sp.atan2(-5, 12))
_aD = sp.deg(sp.atan2(3, 4))
near(_aF, -22.6198649, msg="F の向きの角")
near(_aD, 36.8698976, msg="d の向きの角")
near(_aD - _aF, 59.4897626, msg="差が内積の答えと一致する")
# その道すじは |F| の取り違えに影響されない
near(sp.deg(sp.acos(sp.Rational(33, 169 * 5))), 87.7621459,
     msg="|F| を 169 とした誤答")
chk(abs(float(sp.deg(sp.acos(sp.Rational(33, 169 * 5))))
        - float(_aD - _aF)) > 20, "角の差の方法は誤答をはじく（検算が効く）")
not_in_text("$169 \\times 5 \\times 0.039 = 33$ とはなるものの",
            "循環していた検算（レビュー旧稿）")

T1, T2 = vec(2, -3), vec(-4, 1)
eq(T1.dot(T2), -11, "演習10 の内積")
eq(mag(T1) * mag(T2), sp.sqrt(221), "演習10 の |v||w|")
near(T1.dot(T2) / (mag(T1) * mag(T2)), -0.7399401, msg="演習10 の cosθ")
near(ang(T1, T2), 137.7263110, msg="演習10 の正しい角")
chk(sf3(ang(T1, T2)) == 138.0, "137.7… は 3 桁で 138")
near(180 - ang(T1, T2), 42.2736890, msg="生徒の誤答 42.3")
chk(sf3(180 - ang(T1, T2)) == 42.3, "誤答は 3 桁で 42.3")
chk(float(ang(T1, T2)) > 90 > float(180 - ang(T1, T2)),
    "内積が負なら鈍角。符号を見るだけで誤答が分かる（検算が効く）")

# ══════════════════════════════════════════════════════════
# 6. 符号の表が、境目で嘘になっていないか
# ══════════════════════════════════════════════════════════
# θ=0（同じ向き）は正だが鋭角ではない、θ=180 は負だが鈍角ではない
chk(vec(1, 0).dot(vec(2, 0)) > 0 and float(ang(vec(1, 0), vec(2, 0))) == 0,
    "θ=0 でも内積は正（表が < 90 だけでは足りない）")
chk(vec(1, 0).dot(vec(-1, 0)) < 0
    and abs(float(ang(vec(1, 0), vec(-1, 0))) - 180) < 1e-9,
    "θ=180 でも内積は負")
in_text("$\\theta = 0^{\\circ}$、つまり同じ向きも正になります",
        "符号の表の境目（レビュー3）")
in_text("$\\theta = 180^{\\circ}$、つまり反対向きも負になります",
        "符号の表の境目（レビュー3）")
not_in_text("$0^{\\circ} \\leq \\theta < 90^{\\circ}$ |", "直す前の表の範囲")
not_in_text("$90^{\\circ} < \\theta \\leq 180^{\\circ}$ |", "直す前の表の範囲")
in_text("$\\mathbf{v}$ と $\\mathbf{w}$ が $\\mathbf{0}$ でなければ"
        " $\\lvert \\mathbf{v} \\rvert > 0$",
        "第5節の条件（レビュー15）")

# ══════════════════════════════════════════════════════════
# 7. 公式集とシラバスの引用が正しいか
# ══════════════════════════════════════════════════════════
in_text("$\\mathbf{v} \\cdot \\mathbf{w} = v_1w_1 + v_2w_2 + v_3w_3$",
        "公式集の成分形")
in_text("$\\mathbf{v} \\cdot \\mathbf{w} = \\lvert \\mathbf{v} \\rvert"
        " \\lvert \\mathbf{w} \\rvert \\cos\\theta$", "公式集の幾何形")
in_text("Definition and calculation of the scalar product of two vectors.",
        "Content の 1 行目")
in_text("The angle between two vectors; the acute angle between two lines.",
        "Content の 2 行目")
in_text("ascertain whether the vectors are perpendicular", "Guidance の引用")
in_text("Not required:", "Not required の引用")
in_text("The component of vector $\\mathbf{a}$ acting in the direction of"
        " vector $\\mathbf{b}$", "Components of vectors の Guidance")
in_text("公式集にありません", "(a・b)/|b| が公式集にないこと")
in_text("On HL examination papers radian measure should be assumed unless"
        " otherwise indicated.", "Topic 3 の前置き")
in_text("Guidance 欄のうち、角についての行は次の $1$ 行です。",
        "Guidance の行数の言い方（レビュー9）")
not_in_text("Guidance 欄は、次の $1$ 行です。", "Guidance を 1 行と言い切る文")
# 3.13b に回すものを、このページで説明していないこと
for banned in ["right-hand screw", "unit normal"]:
    chk(banned not in TEXT, "vector product はこのページで扱わない: " + banned)
# crossP( と × が出てよいのは「3.13b に回す」と言っている行だけ
for _ln in TEXT.splitlines():
    if "crossP(" in _ln:
        chk("3-13b" in _ln, "crossP( を 3.13b の案内以外で使っている")
# × が出てよいのは「3.13b に回す」と言っている行だけ
for _ln in TEXT.splitlines():
    if "\\times \\mathbf{w}" in _ln:
        chk("3-13b" in _ln, "× を 3.13b の案内以外で使っている: " + _ln[:50])
chk(TEXT.count("ahl-3-13b.qmd") >= 3, "3.13b への前方リンクがある")

# ══════════════════════════════════════════════════════════
# 8. GDC の記述
# ══════════════════════════════════════════════════════════
in_text("menu → 7: Matrix & Vector → C: Vector", "dotP の場所")
in_text("`ctrl` を押してから `var`", "ストアの押し方")
in_text("menu → Actions → Clear a-z", "変数を消す")
in_text("doc → Settings → Document Settings", "角度設定")
in_text("dotP([3;4],[2;-5])", "dotP の例")
in_text("- **Radian** なら $2.118$", "radian の値（レビュー10）")
not_in_text("$2.117$", "切り捨てていた radian の値")
near(sp.acos(sp.Rational(-14, 1) / (5 * sp.sqrt(29))), 2.1175852,
     msg="121.33° を radian にすると 2.118")
chk(round(float(sp.acos(sp.Rational(-14, 1) / (5 * sp.sqrt(29)))), 3) == 2.118,
    "3 桁小数で 2.118")
# 非 CAS にない命令を勧めていないか
for bad in ["nDeriv(", "nDerivative(", "unitV(", "solve("]:
    not_in_text(bad, "非 CAS にない命令")
chk("norm(" not in TEXT, "norm( を勧めていない")
not_in_text("`180-Ans`", "Ans を使っていた説明（レビュー18）")
not_in_text("$\\mathrm{Ans}$", "Ans を使っていた説明（レビュー18）")
in_text("演習 $5$ のように値が $2$ つ出たら", "演習5 の答えを先に書かない（レビュー5）")
not_in_text("演習 $5$ で $k = 6$ と $k = -6$ が出たら", "答えを先に書いていた文")

# ══════════════════════════════════════════════════════════
# 9. 構成の不変量
# ══════════════════════════════════════════════════════════
chk(len([l for l in TEXT.splitlines() if l.rstrip() == "---"]) == 6,
    "--- は 6 本（front matter 2 + 例題 4）")
chk(TEXT.count('<details class="jp-trans">') == 14, "日本語訳が 14")
chk(TEXT.count("{.ex-sep}") == 9, "ex-sep が 9")
chk(TEXT.count("{.model-answer}") == 6, "model-answer が 6")
chk(TEXT.count("{.ex-no}") == 10, "演習が 10")
chk(len(re.findall(r"^::: \{#exm-ahl313a-", TEXT, re.M)) == 4, "例題が 4")
_h2 = re.findall(r"^## (.+)$", TEXT, re.M)
_want = ["The idea", "Why it works", "Worked examples", "Common errors",
         "Using your GDC (TI-Nspire CX II)", "Exercises"]
chk([h for h in _h2 if h in _want] == _want, "7 つの見出しが所定の順")
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
# 他ページへの @-ref が混ざっていないか（クロスページの @ は動かない）
for _r in set(re.findall(r"@(?:exm|eq|fig|tbl)-([a-z0-9]+)-", TEXT)):
    chk(_r == "ahl313a", "他ページの @-ref を使っている: " + _r)

# ══════════════════════════════════════════════════════════
# 10. 図
# ══════════════════════════════════════════════════════════
for name in ["ahl-3-13a-idea.svg", "ahl-3-13a-lines.svg",
             "ahl-3-13a-component.svg"]:
    chk(os.path.exists(os.path.join(BASE, "img", name)), "図がある: " + name)
    chk("](img/" + name + ")" in TEXT, "本文が図を貼っている: " + name)
# matplotlib が読めない書き方を使っていないか
for bad in ["pmatrix", "\\lvert", "\\rvert"]:
    chk(bad not in FIGCODE, "図で使えない記法: " + bad)
in_fig("\\binom", "図は binom を使う")
# 図 1 の数値
in_fig("3(2)+4(-5) = -14", "図1 の内積")
in_fig(r"\theta \approx 121^{\circ}", "図1 の角")
# 図 2 は、丸める前の値で引いている
in_fig("109.7^{\\circ}", "図2 の方向ベクトルの角")
in_fig("180^{\\circ}-109.7^{\\circ} = 70.3^{\\circ}", "図2 の引き算")
for _ln in FIGSTR.splitlines():
    if "110^{\\circ}" in _ln:
        chk("do not round" in _ln,
            "図2 が 110° を答えとして載せている: " + _ln[:50])
# 図 3 の成分は |b| を超えない（矢印が b を隠さない）
for _a, _b, _lab in [((-1, 6), (4, 3), "2.8"), ((4, 7), (3, -4), "-3.2")]:
    _u, _v = vec(*_a), vec(*_b)
    _c = _u.dot(_v) / mag(_v)
    chk(abs(float(_c)) < float(mag(_v)),
        f"図3 の影が |b| を超えない: {float(_c)} vs {float(mag(_v))}")
    in_fig(_lab, "図3 のラベル " + _lab)
eq(vec(-1, 6).dot(vec(4, 3)) / mag(vec(4, 3)), sp.Rational(14, 5),
   "図3(a) の成分 2.8")
eq(vec(4, 7).dot(vec(3, -4)) / mag(vec(3, -4)), sp.Rational(-16, 5),
   "図3(b) の成分 -3.2")
in_fig("\\mathbf{a}\\cdot\\mathbf{b} = 14", "図3(a) の内積")
chk("= 26" not in FIGSTR and "5.2" not in FIGSTR,
    "図3(a) の古い数値が残っていない")
# 図が演習の答えを漏らしていないか
for leak in ["8.4", "82.9", "42.8", "82.2", "59.5", "10.3", "4.4",
             "$138", "= 33"]:
    chk(leak not in FIGSTR, "図が演習の答えを載せている: " + leak)

# ══════════════════════════════════════════════════════════
# 11. 登録
# ══════════════════════════════════════════════════════════
DRAFT = open(os.path.join(HERE, "..", "..", "_quarto-draft.yml"),
             encoding="utf-8").read()
chk("ai-hl/03-geometry-and-trigonometry/ahl-3-13a.qmd" in DRAFT,
    "_quarto-draft.yml に登録されている")
chk(DRAFT.index("ahl-3-12b.qmd") < DRAFT.index("ahl-3-13a.qmd")
    < DRAFT.index("ahl-3-14.qmd"), "サイドバーの並びが 3.12b → 3.13a → 3.14")
PUB = open(os.path.join(HERE, "..", "..", "_quarto.yml"), encoding="utf-8").read()
chk("ahl-3-13a" not in PUB, "公開用の _quarto.yml は SL だけのまま")
IDX = open(os.path.join(HERE, "..", "..", "ai-hl", "index.qmd"),
           encoding="utf-8").read()
chk("[AHL 3.13a — The scalar product]"
    "(03-geometry-and-trigonometry/ahl-3-13a.qmd)" in IDX, "index の一覧にある")
_row = [x for x in re.findall(r"^\| (?:\*\*)?AHL [0-9.]+(?:\*\*)? \|(.*)\|$",
                              IDX, re.M) if "ahl-3-13a.qmd" in x]
_b_exists = os.path.exists(os.path.join(BASE, "ahl-3-13b.qmd"))
if _b_exists:
    chk(len(_row) == 1 and "✅" in _row[0] and "ahl-3-13b.qmd" in _row[0],
        "3.13b があるので、AHL 3.13 の行は 3.13b へのリンクと ✅ を持つ")
else:
    chk(len(_row) == 1 and "✅" not in _row[0],
        "AHL 3.13 の行は、3.13b が書けるまで ✅ を付けない")
_left = int(_m.group(1)) if (_m := re.search(r"残りの(\d+)項目", IDX)) else 0
_rows = re.findall(r"^\| (?:\*\*)?AHL [0-9.]+(?:\*\*)? \|(.*)\|$", IDX, re.M)
chk(_left == len([x for x in _rows if "✅" not in x]),
    "「残りの N 項目」が、まだ ✅ の付いていない行の数と合う")
GLO = open(os.path.join(HERE, "..", "..", "glossary-ai.qmd"),
           encoding="utf-8").read()
for term in ["| scalar product |", "| dot product |",
             "| the angle between two vectors |",
             "| the acute angle between two lines |",
             "| perpendicular（ベクトルが） |", "| non-zero |",
             "| projection |", "| work done |"]:
    chk(term in GLO, "対訳表にある: " + term)

print()
print("OK", OK, "/ NG", NG)
sys.exit(1 if NG else 0)
