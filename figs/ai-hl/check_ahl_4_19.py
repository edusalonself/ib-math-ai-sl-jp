"""AHL 4.19 の本文・例題・演習の数値を独立に検算する。
   steady state は【2 通り】（連立方程式、行列のべき乗の極限）で出し、
   さらに eigenvector からも出して、3 つが一致するかを見る。
   実行: python3 figs/ai-hl/check_ahl_4_19.py
"""
import sympy as sp

ok, ng = 0, 0
M = sp.Matrix
R = sp.Rational


def eq(name, got, want):
    global ok, ng
    if isinstance(got, sp.MatrixBase) or isinstance(want, sp.MatrixBase):
        good = sp.simplify(M(got) - M(want)) == sp.zeros(*M(got).shape)
    elif isinstance(got, (list, tuple)) or isinstance(want, (list, tuple)):
        good = (len(got) == len(want)
                and all(sp.simplify(sp.sympify(g) - sp.sympify(w)) == 0
                        if not isinstance(g, bool) else g == w
                        for g, w in zip(got, want)))
    elif isinstance(got, bool) or isinstance(want, bool):
        good = got == want
    else:
        good = sp.simplify(sp.sympify(got) - sp.sympify(want)) == 0
    print(("  OK   " if good else "  ★NG★ ") + name +
          ("" if good else f"   got {got}  want {want}"))
    ok, ng = ok + good, ng + (not good)


def cols_ok(T):
    return [sp.simplify(sum(T[:, j])) for j in range(T.shape[1])]


def steady_by_equations(T):
    n = T.shape[0]
    v = sp.symbols(f"v0:{n}")
    s = M(v)
    sol = sp.solve(list(T * s - s) + [sum(v) - 1], list(v), dict=True)
    return M([sol[0][t] for t in v])


def steady_by_eigen(T):
    """固有値 1 の固有ベクトルを、成分の和が 1 になるようにそろえる。"""
    for val, mult, vecs in T.eigenvects():
        if sp.simplify(val - 1) == 0:
            w = vecs[0]
            return sp.simplify(w / sum(w))
    raise ValueError("eigenvalue 1 not found")


print("══════════ The idea：2 状態（スーパー A / B） ══════════")
T = M([[R(8, 10), R(3, 10)], [R(2, 10), R(7, 10)]])
eq("列の和はどちらも 1", cols_ok(T), [1, 1])
s0 = M([1, 0])
want = {1: [R(4, 5), R(1, 5)], 2: [R(7, 10), R(3, 10)],
        3: [R(13, 20), R(7, 20)], 4: [R(5, 8), R(3, 8)]}
for n, w in want.items():
    eq(f"s_{n}", (T ** n) * s0, M(w))
eq("s_1 = 0.8, 0.2", [sp.nsimplify(x) for x in (T ** 1) * s0],
   [R(8, 10), R(2, 10)])
print("       s_4 =", [float(x) for x in (T ** 4) * s0])
print("       s_10 =", [round(float(x), 6) for x in (T ** 10) * s0])
print("       s_20 =", [round(float(x), 8) for x in (T ** 20) * s0])
eq("steady state（連立方程式）", steady_by_equations(T), M([R(3, 5), R(2, 5)]))
eq("steady state（固有ベクトル）", steady_by_eigen(T), M([R(3, 5), R(2, 5)]))
eq("steady state は動かない", T * M([R(3, 5), R(2, 5)]), M([R(3, 5), R(2, 5)]))
eq("固有値", sorted(T.eigenvals().keys()), [R(1, 2), 1])
eq("T はすべて正なので regular", all(x > 0 for x in T), True)
# 出発点を変えても同じところに行く
for start in (M([1, 0]), M([0, 1]), M([R(1, 2), R(1, 2)])):
    v = (T ** 40) * start
    eq(f"出発 {list(start)} でも 40 歩後は 0.6, 0.4 に近い",
       [round(float(x), 6) for x in v], [0.6, 0.4])

print("══════════ 例題1（T を作る） ══════════")
eq("(a) T", T, M([[R(8, 10), R(3, 10)], [R(2, 10), R(7, 10)]]))
s0b = M([R(1, 2), R(1, 2)])
eq("(b) s_1", T * s0b, M([R(11, 20), R(9, 20)]))
print("       s_1 =", [float(x) for x in T * s0b])
eq("(b) 0.55 と 0.45", [sp.nsimplify(x) for x in T * s0b],
   [R(55, 100), R(45, 100)])

print("══════════ 例題2（s_n = T^n s_0） ══════════")
eq("(a) s_4", (T ** 4) * s0, M([R(5, 8), R(3, 8)]))
eq("(a) 小数で 0.625, 0.375", [float(x) for x in (T ** 4) * s0],
   [0.625, 0.375])
eq("(b) 5000 人に直す", [5000 * x for x in (T ** 4) * s0], [3125, 1875])
v10 = (T ** 10) * s0
print("       s_10 =", [float(x) for x in v10])
eq("(c) s_10 の第 1 成分", v10[0], R(1537, 2560))
eq("(c) s_10 の第 2 成分", v10[1], R(1023, 2560))
eq("(c) 3 s.f. は 0.600 と 0.400",
   [round(float(x), 3) for x in v10], [0.6, 0.4])

print("══════════ 例題3（steady state を方程式で） ══════════")
a, b = sp.symbols("a b")
sol = sp.solve([sp.Eq(R(8, 10) * a + R(3, 10) * b, a), sp.Eq(a + b, 1)],
               [a, b])
eq("方程式の解", [sol[a], sol[b]], [R(3, 5), R(2, 5)])
eq("2 本目の式でも同じ", sp.solve(
    [sp.Eq(R(2, 10) * a + R(7, 10) * b, b), sp.Eq(a + b, 1)], [a, b])[a],
   R(3, 5))

print("══════════ 例題4（3 状態） ══════════")
W = M([[R(6, 10), R(1, 10), R(1, 10)],
       [R(1, 10), R(6, 10), R(2, 10)],
       [R(3, 10), R(3, 10), R(7, 10)]])
eq("列の和はすべて 1", cols_ok(W), [1, 1, 1])
eq("すべて正なので regular", all(x > 0 for x in W), True)
w0 = M([1, 0, 0])
eq("(a) s_1", W * w0, M([R(6, 10), R(1, 10), R(3, 10)]))
w2 = (W ** 2) * w0
eq("(b) s_2", w2, M([R(2, 5), R(9, 50), R(21, 50)]))
print("       s_2 =", [float(x) for x in w2])
w3 = (W ** 3) * w0
eq("(b) s_3", w3, M([R(3, 10), R(29, 125), R(117, 250)]))
print("       s_3 =", [float(x) for x in w3])
eq("(c) steady state（方程式）", steady_by_equations(W),
   M([R(1, 5), R(3, 10), R(1, 2)]))
eq("(c) steady state（固有ベクトル）", steady_by_eigen(W),
   M([R(1, 5), R(3, 10), R(1, 2)]))
eq("(c) 動かないことの確認", W * M([R(1, 5), R(3, 10), R(1, 2)]),
   M([R(1, 5), R(3, 10), R(1, 2)]))
print("       s_30 =", [round(float(x), 6) for x in (W ** 30) * w0])

print("══════════ 例題5（eigenvector とのつながり） ══════════")
eq("T の固有値に 1 がある", 1 in T.eigenvals(), True)
w = None
for val, mult, vecs in T.eigenvects():
    if sp.simplify(val - 1) == 0:
        w = vecs[0]
eq("固有ベクトルの 1 つ", sp.simplify(w / w[1]), M([R(3, 2), 1]))
eq("成分の和を 1 にそろえると steady state", sp.simplify(w / sum(w)),
   M([R(3, 5), R(2, 5)]))

print("══════════ 演習 ══════════")
# 1 どれが transition matrix か
c1 = M([[R(3, 10), R(6, 10)], [R(7, 10), R(4, 10)]])
c2 = M([[R(3, 10), R(6, 10)], [R(7, 10), R(3, 10)]])
c3 = M([[R(1, 2), R(1, 4)], [R(1, 2), R(3, 4)]])
eq("1  A は列の和が 1", cols_ok(c1), [1, 1])
eq("1  B は列の和が 1 でない", cols_ok(c2), [1, R(9, 10)])
eq("1  C は列の和が 1", cols_ok(c3), [1, 1])
# 2 図から T を作って s_1
T2 = M([[R(9, 10), R(4, 10)], [R(1, 10), R(6, 10)]])
eq("2  列の和", cols_ok(T2), [1, 1])
eq("2  s_1（s_0 = (0.7, 0.3)）", T2 * M([R(7, 10), R(3, 10)]),
   M([R(75, 100), R(25, 100)]))
# 3 s_5
v5 = (T2 ** 5) * M([1, 0])
print("3  s_5 =", [float(x) for x in v5])
eq("3  s_5 の第 1 成分", v5[0], R(129, 160))
eq("3  s_5 を小数で", [float(x) for x in v5], [0.80625, 0.19375])
# 4 steady state（2 状態）
eq("4  steady state", steady_by_equations(T2), M([R(4, 5), R(1, 5)]))
eq("4  確認", T2 * M([R(4, 5), R(1, 5)]), M([R(4, 5), R(1, 5)]))
# 5, 6 三状態
U = M([[R(5, 10), R(3, 10), R(2, 10)],
       [R(4, 10), R(6, 10), R(2, 10)],
       [R(1, 10), R(1, 10), R(6, 10)]])
eq("5  列の和", cols_ok(U), [1, 1, 1])
u0 = M([R(1, 2), R(1, 4), R(1, 4)])
eq("5  s_1", U * u0, M([R(3, 8), R(2, 5), R(9, 40)]))
u2 = (U ** 2) * u0
print("5  s_2 =", [float(x) for x in u2])
eq("5  s_2", u2, M([R(141, 400), R(87, 200), R(17, 80)]))
eq("6  steady state", steady_by_equations(U), M([R(7, 20), R(9, 20), R(1, 5)]))
eq("6  固有ベクトルからも同じ", steady_by_eigen(U),
   M([R(7, 20), R(9, 20), R(1, 5)]))
eq("6  確認", U * M([R(7, 20), R(9, 20), R(1, 5)]),
   M([R(7, 20), R(9, 20), R(1, 5)]))
# 7 regular でない例
S = M([[0, 1], [1, 0]])
eq("7  列の和は 1", cols_ok(S), [1, 1])
eq("7  S^2 は単位行列", S ** 2, sp.eye(2))
eq("7  どの累乗にも 0 が残る",
   any(x == 0 for x in S ** 5) and any(x == 0 for x in S ** 6), True)
eq("7  s_0 = (1,0) は 1,0 と 0,1 を行き来する",
   [x for n in (1, 2, 3) for x in (S ** n) * M([1, 0])],
   [0, 1, 1, 0, 0, 1])
# 8 人数
eq("8  5000 人の長期分布（2 状態 T）",
   [5000 * x for x in M([R(3, 5), R(2, 5)])], [3000, 2000])
eq("8  20000 人の長期分布（3 状態 W）",
   [20000 * x for x in M([R(1, 5), R(3, 10), R(1, 2)])],
   [4000, 6000, 10000])

print()
print(f"══════════ OK {ok} / NG {ng} ══════════")
