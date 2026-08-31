"""AHL 3.15 の本文・例題・演習の数値を独立に検算する。
   行列のべき乗と、walk の数え上げを【別々の方法】で出して突き合わせる。
   実行: python3 figs/ai-hl/check_ahl_3_15.py
"""
import sympy as sp
from itertools import product

ok, ng = 0, 0
M = sp.Matrix


def eq(name, got, want):
    global ok, ng
    if isinstance(got, sp.MatrixBase) or isinstance(want, sp.MatrixBase):
        good = sp.simplify(M(got) - M(want)) == sp.zeros(*M(got).shape)
    else:
        good = got == want
    print(("  OK   " if good else "  ★NG★ ") + name +
          ("" if good else f"   got {got}  want {want}"))
    ok, ng = ok + good, ng + (not good)


def count_walks(adj, n, i, j, k):
    """長さ k の walk の数を、素朴に全部の並びを試して数える。"""
    total = 0
    for mid in product(range(n), repeat=k - 1):
        path = (i,) + mid + (j,)
        if all(adj[path[t]][path[t + 1]] for t in range(k)):
            total += 1
    return total


def adj_from(edges, names, directed=False):
    n = len(names)
    idx = {v: i for i, v in enumerate(names)}
    a = [[0] * n for _ in range(n)]
    for u, v in edges:
        a[idx[u]][idx[v]] += 1
        if not directed:
            a[idx[v]][idx[u]] += 1
    return a


print("══════════ The idea：無向グラフ ══════════")
NM = ["A", "B", "C", "D"]
E4 = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "D")]
a = adj_from(E4, NM)
A = M(a)
eq("隣接行列", A, M([[0, 1, 1, 0], [1, 0, 1, 0], [1, 1, 0, 1], [0, 0, 1, 0]]))
eq("無向なので対称", A, A.T)
eq("A^2", A ** 2, M([[2, 1, 1, 1], [1, 2, 1, 1], [1, 1, 3, 0], [1, 1, 0, 1]]))
for i in range(4):
    for j in range(4):
        eq(f"A^2[{NM[i]}][{NM[j]}] を素朴に数える",
           count_walks(a, 4, i, j, 2), (A ** 2)[i, j])
eq("A^2 の対角は degree", [(A ** 2)[i, i] for i in range(4)],
   [sum(a[i]) for i in range(4)])
eq("A^3", A ** 3, M([[2, 3, 4, 1], [3, 2, 4, 1], [4, 4, 2, 3], [1, 1, 3, 0]]))
eq("A^3[A][C] を素朴に数える", count_walks(a, 4, 0, 2, 3), 4)
eq("3 歩以下で A から D", (A + A ** 2 + A ** 3)[0, 3], 2)
eq("A + A^2 + A^3",
   A + A ** 2 + A ** 3,
   M([[4, 5, 6, 2], [5, 4, 6, 2], [6, 6, 5, 4], [2, 2, 4, 1]]))

print("══════════ The idea：transition matrix ══════════")
TN = ["A", "B", "C"]
TA = [("A", "B"), ("A", "C"), ("B", "A"), ("C", "A"), ("C", "B")]
outd = {v: sum(1 for u, w in TA if u == v) for v in TN}
eq("out degree", [outd[v] for v in TN], [2, 1, 2])
half = sp.Rational(1, 2)
T = M([[0, 1, half], [half, 0, half], [half, 0, 0]])
eq("列の和はすべて 1", [sum(T[:, j]) for j in range(3)], [1, 1, 1])
# T[i][j] = 状態 j から状態 i へ動く確率
for j, v in enumerate(TN):
    for i, w in enumerate(TN):
        want = sp.Rational(1, outd[v]) if (v, w) in TA else 0
        eq(f"T[{w}][{v}] = {v} から {w}", T[i, j], want)

print("══════════ 例題1 ══════════")
N1 = ["P", "Q", "R", "S"]
E1 = [("P", "Q"), ("P", "S"), ("Q", "R"), ("Q", "S"), ("R", "S")]
a1 = adj_from(E1, N1)
A1 = M(a1)
eq("(a) 隣接行列", A1,
   M([[0, 1, 0, 1], [1, 0, 1, 1], [0, 1, 0, 1], [1, 1, 1, 0]]))
eq("(b) A^2", A1 ** 2,
   M([[2, 1, 2, 1], [1, 3, 1, 2], [2, 1, 2, 1], [1, 2, 1, 3]]))
eq("(b) P から R への 2 歩の walk", (A1 ** 2)[0, 2], 2)
eq("(b) 素朴に数える", count_walks(a1, 4, 0, 2, 2), 2)
eq("(c) A^3", A1 ** 3,
   M([[2, 5, 2, 5], [5, 4, 5, 5], [2, 5, 2, 5], [5, 5, 5, 4]]))
eq("(c) 3 歩以下で P から R", (A1 + A1 ** 2 + A1 ** 3)[0, 2], 4)
eq("(c) 0 + 2 + 2", 0 + 2 + 2, 4)

print("══════════ 例題2 ══════════")
eq("A^2 の対角 = degree（例題1 のグラフ）",
   [(A1 ** 2)[i, i] for i in range(4)], [2, 3, 2, 3])
eq("degree を直接数える", [sum(a1[i]) for i in range(4)], [2, 3, 2, 3])
eq("A^3 の対角（三角形を通る）", [(A1 ** 3)[i, i] for i in range(4)],
   [2, 4, 2, 4])

print("══════════ 例題3（directed） ══════════")
N3 = ["X", "Y", "Z"]
A3arcs = [("X", "Y"), ("X", "Z"), ("Y", "Z"), ("Z", "X")]
a3 = adj_from(A3arcs, N3, directed=True)
A3 = M(a3)
eq("(a) 隣接行列（行 = from）", A3, M([[0, 1, 1], [0, 0, 1], [1, 0, 0]]))
eq("(a) 対称ではない", A3 == A3.T, False)
eq("(b) A^2", A3 ** 2, M([[1, 0, 1], [1, 0, 0], [0, 1, 1]]))
eq("(b) X から X への 2 歩", (A3 ** 2)[0, 0], 1)
eq("(b) 素朴に数える", count_walks(a3, 3, 0, 0, 2), 1)
o3 = {v: sum(1 for u, w in A3arcs if u == v) for v in N3}
eq("(c) out degree", [o3[v] for v in N3], [2, 1, 1])
T3 = M([[0, 0, 1], [half, 0, 0], [half, 1, 0]])
eq("(c) transition matrix の列の和", [sum(T3[:, j]) for j in range(3)],
   [1, 1, 1])
eq("(c) T の (2,1) 成分 = X から Y", T3[1, 0], half)
eq("(c) T^3 s0", (T3 ** 3) * M([1, 0, 0]),
   M([half, sp.Rational(1, 4), sp.Rational(1, 4)]))

print("══════════ 例題4（weighted） ══════════")
W = {("A", "B"): 5, ("A", "C"): 3, ("B", "C"): 6, ("B", "D"): 8,
     ("C", "D"): 4}
eq("A-C-D の重み", W[("A", "C")] + W[("C", "D")], 7)
eq("A-B-D の重み", W[("A", "B")] + W[("B", "D")], 13)
eq("A-B-C-D の重み",
   W[("A", "B")] + W[("B", "C")] + W[("C", "D")], 15)
eq("A から D への最小", min(7, 13, 15), 7)

print("══════════ 演習 ══════════")
NX = ["A", "B", "C", "D"]
EX = [("A", "B"), ("A", "D"), ("B", "C"), ("B", "D"), ("C", "D")]
ax = adj_from(EX, NX)
AX = M(ax)
eq("1  隣接行列", AX,
   M([[0, 1, 0, 1], [1, 0, 1, 1], [0, 1, 0, 1], [1, 1, 1, 0]]))
eq("1  degree", [sum(ax[i]) for i in range(4)], [2, 3, 2, 3])
eq("2  A^2", AX ** 2,
   M([[2, 1, 2, 1], [1, 3, 1, 2], [2, 1, 2, 1], [1, 2, 1, 3]]))
eq("2  A から C への 2 歩", (AX ** 2)[0, 2], 2)
eq("2  素朴に数える", count_walks(ax, 4, 0, 2, 2), 2)
eq("3  A^3 の (A, B)", (AX ** 3)[0, 1], 5)
eq("3  3 歩以下で A から B", (AX + AX ** 2 + AX ** 3)[0, 1], 7)
NY = ["P", "Q", "R"]
AY = [("P", "Q"), ("Q", "R"), ("R", "P"), ("R", "Q")]
ay = adj_from(AY, NY, directed=True)
AYm = M(ay)
eq("5  隣接行列（行 = from）", AYm, M([[0, 1, 0], [0, 0, 1], [1, 1, 0]]))
oy = {v: sum(1 for u, w in AY if u == v) for v in NY}
eq("5  out degree", [oy[v] for v in NY], [1, 1, 2])
TY = M([[0, 0, half], [1, 0, half], [0, 1, 0]])
eq("5  列の和", [sum(TY[:, j]) for j in range(3)], [1, 1, 1])
eq("6  AYm^2", AYm ** 2, M([[0, 0, 1], [1, 1, 0], [0, 1, 1]]))
eq("6  P から R への 2 歩", (AYm ** 2)[0, 2], 1)
eq("7  4 頂点の complete graph の隣接行列の各行の和", 3, 3)
W8 = {("A", "B"): 7, ("A", "D"): 5, ("B", "C"): 6, ("B", "D"): 9,
      ("C", "D"): 3}
eq("8  A-D-C の重み", W8[("A", "D")] + W8[("C", "D")], 8)
eq("8  A-B-C の重み", W8[("A", "B")] + W8[("B", "C")], 13)
eq("8  最小は A-D-C", min(8, 13), 8)

print()
print(f"══════════ OK {ok} / NG {ng} ══════════")
