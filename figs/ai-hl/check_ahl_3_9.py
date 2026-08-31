"""AHL 3.9 の本文・例題・演習の数値を独立に検算する。
   本文を書くコードとは【別に】書いて、答えが一致するかを見る。
   実行: python3 figs/ai-hl/check_ahl_3_9.py
"""
import sympy as sp

ok, ng = 0, 0
M = sp.Matrix


def eq(name, got, want):
    global ok, ng
    if isinstance(got, sp.MatrixBase) or isinstance(want, sp.MatrixBase):
        good = sp.simplify(sp.Matrix(got) - sp.Matrix(want)) == sp.zeros(
            *sp.Matrix(got).shape)
    else:
        good = sp.simplify(sp.nsimplify(got) - sp.nsimplify(want)) == 0
    print(("  OK   " if good else "  ★NG★ ") + name +
          ("" if good else f"   got {got}  want {want}"))
    ok, ng = ok + good, ng + (not good)


def rot(deg):
    """公式集：anticlockwise rotation of angle theta about the origin"""
    t = sp.rad(deg)
    return M([[sp.cos(t), -sp.sin(t)], [sp.sin(t), sp.cos(t)]])


def rot_cw(deg):
    """公式集：clockwise rotation of angle theta about the origin"""
    t = sp.rad(deg)
    return M([[sp.cos(t), sp.sin(t)], [-sp.sin(t), sp.cos(t)]])


def refl(deg):
    """公式集：reflection in the line y = (tan theta) x"""
    t = sp.rad(2 * deg)
    return M([[sp.cos(t), sp.sin(t)], [sp.sin(t), -sp.cos(t)]])


def hstretch(k):
    return M([[k, 0], [0, 1]])


def vstretch(k):
    return M([[1, 0], [0, k]])


def enlarge(k):
    return M([[k, 0], [0, k]])


def tri_area(P, Q, R):
    return sp.Rational(1, 2) * sp.Abs((Q[0] - P[0]) * (R[1] - P[1])
                                      - (R[0] - P[0]) * (Q[1] - P[1]))


print("══════════ 公式集の 6 つを、特別な角で確かめる ══════════")
eq("reflection theta=0 は x 軸", refl(0), M([[1, 0], [0, -1]]))
eq("reflection theta=90 は y 軸", refl(90), M([[-1, 0], [0, 1]]))
eq("reflection theta=45 は y=x", refl(45), M([[0, 1], [1, 0]]))
eq("reflection theta=135 は y=-x", refl(135), M([[0, -1], [-1, 0]]))
eq("rotation 90 anticlockwise", rot(90), M([[0, -1], [1, 0]]))
eq("rotation 180", rot(180), M([[-1, 0], [0, -1]]))
eq("rotation 270 anticlockwise", rot(270), M([[0, 1], [-1, 0]]))
eq("rotation 90 clockwise = rotation 270 anticlockwise", rot_cw(90), rot(270))
eq("reflection の det は -1", sp.det(refl(37)), -1)
eq("rotation の det は 1", sp.simplify(sp.det(rot(37))), 1)

print("══════════ The idea ══════════")
# 1. 列は i と j の行き先
A = M([[3, 1], [1, 2]])
eq("A(1,0) は 1 列目", A * M([1, 0]), M([3, 1]))
eq("A(0,1) は 2 列目", A * M([0, 1]), M([1, 2]))
# 2. 点 P(3,1) を 90 度回す
eq("90度回転で (3,1)->(-1,3)", rot(90) * M([3, 1]), M([-1, 3]))
# 3. 図形をまとめて動かす（三角形の3頂点を並べる）
T = M([[1, 4, 1], [1, 1, 3]])          # A(1,1) B(4,1) C(1,3)
eq("3点まとめて90度回転", rot(90) * T, M([[-1, -1, -3], [1, 4, 1]]))
# 4. translation
eq("拡大してから平行移動", enlarge(2) * M([3, 1]) + M([1, -3]), M([7, -1]))
# 5. determinant と面積
eq("det(3 1;1 2) = 5", sp.det(A), 5)
eq("もとの三角形の面積", tri_area((0, 0), (4, 0), (0, 2)), 4)
im = [A * M([0, 0]), A * M([4, 0]), A * M([0, 2])]
eq("像の面積 = |det| x もとの面積",
   tri_area((im[0][0], im[0][1]), (im[1][0], im[1][1]),
            (im[2][0], im[2][1])), 5 * 4)

print("══════════ 例題1 ══════════")
M1 = M([[0, -1], [1, 0]])
eq("(a) P(4,2) の像", M1 * M([4, 2]), M([-2, 4]))
eq("(b) M1 は 90 度反時計回り", M1, rot(90))

print("══════════ 例題2 ══════════")
M2 = M([[2, 1], [0, 3]])
eq("(a) A(4,0) の像", M2 * M([4, 0]), M([8, 0]))
eq("(a) B(0,3) の像", M2 * M([0, 3]), M([3, 9]))
eq("(b) det M2", sp.det(M2), 6)
eq("もとの三角形 OAB の面積", tri_area((0, 0), (4, 0), (0, 3)), 6)
eq("(c) 像の面積", tri_area((0, 0), (8, 0), (3, 9)), 36)
eq("(c) |det| x 6", sp.Abs(sp.det(M2)) * 6, 36)

print("══════════ 例題3 ══════════")
P = M([[1, 0], [0, -1]])               # x 軸に関する reflection
Q = rot(90)                            # 90 度反時計回り
eq("P は theta=0 の reflection", P, refl(0))
eq("(b) QP", Q * P, M([[0, 1], [1, 0]]))
eq("(b) QP は y=x の reflection", Q * P, refl(45))
eq("(c) PQ", P * Q, M([[0, -1], [-1, 0]]))
eq("(c) PQ は y=-x の reflection", P * Q, refl(135))
eq("QP と PQ は違う", 1 if (Q * P) != (P * Q) else 0, 1)

print("══════════ 例題4 ══════════")
M4 = M([[3, 1], [2, 1]])
t4 = M([4, -1])
eq("(a) (2,1) の像", M4 * M([2, 1]) + t4, M([11, 4]))
eq("(b) det M4", sp.det(M4), 1)
eq("(b) 面積は変わらない", sp.Abs(sp.det(M4)) * 6, 6)
eq("(c) 逆行列", M4.inv(), M([[1, -1], [-2, 3]]))
eq("(c) (12,5) にうつる点", M4.inv() * (M([12, 5]) - t4), M([2, 2]))
eq("(c) 検算：(2,2) の像", M4 * M([2, 2]) + t4, M([12, 5]))

print("══════════ 例題5（Sierpinski） ══════════")
S = M([[sp.Rational(1, 2), 0], [0, sp.Rational(1, 2)]])
eq("(a) S は scale factor 1/2 の enlargement", S, enlarge(sp.Rational(1, 2)))
eq("(a) det S", sp.det(S), sp.Rational(1, 4))
r = sp.Rational(3, 4)
eq("(b) 1 回で面積は 3/4 倍", 3 * sp.Rational(1, 4), r)
eq("(c) 64 x (3/4)^5", 64 * r ** 5, sp.Rational(243, 16))
eq("(c) 小数", sp.nsimplify(sp.Rational(243, 16)), sp.Rational(15.1875))
print("       64 x (3/4)^5 =", sp.N(64 * r ** 5, 8), " → 3 s.f. 15.2")
eq("(d) n->無限大で 0", sp.limit(64 * r ** sp.Symbol('n', positive=True),
                                 sp.Symbol('n', positive=True), sp.oo), 0)

print("══════════ 演習 ══════════")
eq("1  180度回転で (5,-2)->(-5,2)", rot(180) * M([5, -2]), M([-5, 2]))
eq("2  y 軸に関する reflection", refl(90), M([[-1, 0], [0, 1]]))
eq("2  (3,7) の像", refl(90) * M([3, 7]), M([-3, 7]))
eq("3  enlargement k=3 で (2,-1)", enlarge(3) * M([2, -1]), M([6, -3]))
eq("3  面積は 9 倍", sp.det(enlarge(3)), 9)
E4 = rot(90) * hstretch(2)             # 先に stretch、あとで rotation
eq("4  RS の順", E4, M([[0, -1], [2, 0]]))
eq("4  (3,2) の像", E4 * M([3, 2]), M([-2, 6]))
eq("4  逆の順 SR", hstretch(2) * rot(90), M([[0, -2], [1, 0]]))
M5 = M([[4, 2], [1, 3]])
eq("5  det M5", sp.det(M5), 10)
eq("5  もとの三角形の面積", tri_area((0, 0), (3, 0), (0, 2)), 3)
eq("5  像の面積", sp.Abs(sp.det(M5)) * 3, 30)
im5 = [M5 * M([0, 0]), M5 * M([3, 0]), M5 * M([0, 2])]
eq("5  像を直接計算", tri_area((im5[0][0], im5[0][1]), (im5[1][0], im5[1][1]),
                              (im5[2][0], im5[2][1])), 30)
eq("5  A(3,0) の像", M5 * M([3, 0]), M([12, 3]))
eq("5  B(0,2) の像", M5 * M([0, 2]), M([4, 6]))
M6 = M([[1, 0], [0, -1]])
eq("6  (x,y)->(x, -y)+(0,6) で (2,1)", M6 * M([2, 1]) + M([0, 6]), M([2, 5]))
eq("6  (5,-3) の像", M6 * M([5, -3]) + M([0, 6]), M([5, 9]))
eq("7  (0 1;1 0) は y=x の reflection", M([[0, 1], [1, 0]]), refl(45))
M8 = M([[2, 3], [1, 2]])
eq("8  det M8", sp.det(M8), 1)
eq("8  逆行列", M8.inv(), M([[2, -3], [-1, 2]]))
eq("8  (8,5) にうつる点", M8.inv() * M([8, 5]), M([1, 2]))
eq("8  検算", M8 * M([1, 2]), M([8, 5]))
R60 = rot(60)
print("9  rotation 60 の成分 =", [sp.N(x, 8) for x in R60])
eq("9  cos60", R60[0, 0], sp.Rational(1, 2))
p9 = R60 * M([5, 0])
print("9  (5,0) の像 =", [sp.N(x, 8) for x in p9], " → (2.5, 4.33)")
eq("9  x 座標", p9[0], sp.Rational(5, 2))
eq("9  y 座標", sp.simplify(p9[1]), 5 * sp.sqrt(3) / 2)
print("9  y = ", sp.N(5 * sp.sqrt(3) / 2, 8))
# 10 Koch snowflake の周の長さ
L0 = 27
eq("10 1回後の周", L0 * sp.Rational(4, 3), 36)
eq("10 4回後の周", L0 * sp.Rational(4, 3) ** 4, sp.Rational(256, 3))
print("10 27 x (4/3)^4 =", sp.N(L0 * sp.Rational(4, 3) ** 4, 8),
      " → 3 s.f. 85.3")
_n = sp.Symbol('n', positive=True)
eq("10 n->無限大で発散",
   1 if sp.limit(L0 * sp.Rational(4, 3) ** _n, _n, sp.oo) is sp.oo else 0, 1)

print()
print(f"══════════ OK {ok} / NG {ng} ══════════")
