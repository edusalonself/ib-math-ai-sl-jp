"""AHL 3.14 の本文・例題・演習の数値を独立に検算する。
   本文を書くコードとは【別に】書いて、答えが一致するかを見る。
   実行: python3 figs/ai-hl/check_ahl_3_14.py
"""
import sympy as sp
from itertools import combinations

ok, ng = 0, 0


def eq(name, got, want):
    global ok, ng
    good = got == want
    print(("  OK   " if good else "  ★NG★ ") + name +
          ("" if good else f"   got {got}  want {want}"))
    ok, ng = ok + good, ng + (not good)


def degrees(vertices, edges):
    d = {v: 0 for v in vertices}
    for u, v in edges:
        d[u] += 1
        d[v] += 1
    return d


def reachable(vertices, arcs, start, directed=True):
    seen = {start}
    stack = [start]
    while stack:
        x = stack.pop()
        for u, v in arcs:
            for a, b in ((u, v),) if directed else ((u, v), (v, u)):
                if a == x and b not in seen:
                    seen.add(b)
                    stack.append(b)
    return seen


def complete_edges(n):
    return n * (n - 1) // 2


print("══════════ The idea：グラフ G ══════════")
V = ["A", "B", "C", "D", "E"]
E = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "D"), ("D", "E")]
d = degrees(V, E)
eq("頂点の数", len(V), 5)
eq("辺の数", len(E), 6)
eq("degree", [d[v] for v in V], [2, 3, 3, 3, 1])
eq("degree の合計 = 2 x 辺の数", sum(d.values()), 2 * len(E))
eq("G は connected", reachable(V, E, "A", directed=False), set(V))
eq("G は simple（重複辺なし）", len(set(map(frozenset, E))), len(E))
eq("tree の辺の数は 頂点 - 1", len(V) - 1, 4)

print("══════════ complete graph ══════════")
for n in (4, 5, 6, 7, 10):
    eq(f"K_{n} の辺の数", complete_edges(n), len(list(combinations(range(n), 2))))
eq("K_5 の辺の数", complete_edges(5), 10)
eq("K_5 の各頂点の degree", 5 - 1, 4)

print("══════════ The idea：directed graph ══════════")
DV = ["A", "B", "C", "D"]
DA = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("B", "D")]
ind = {v: sum(1 for u, w in DA if w == v) for v in DV}
outd = {v: sum(1 for u, w in DA if u == v) for v in DV}
eq("in degree", [ind[v] for v in DV], [1, 1, 1, 2])
eq("out degree", [outd[v] for v in DV], [1, 2, 1, 1])
eq("in の合計 = 矢印の数", sum(ind.values()), len(DA))
eq("out の合計 = 矢印の数", sum(outd.values()), len(DA))

print("══════════ 例題1 ══════════")
V1 = ["A", "B", "C", "D", "E"]
E1 = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "D"),
      ("C", "E"), ("D", "E")]
d1 = degrees(V1, E1)
eq("(a) 辺の数", len(E1), 7)
eq("(b) degree", [d1[v] for v in V1], [2, 3, 4, 3, 2])
eq("(b) 合計", sum(d1.values()), 14)
eq("(b) 2 x 辺の数", 2 * len(E1), 14)
eq("(c) simple", len(set(map(frozenset, E1))) == len(E1)
   and all(u != v for u, v in E1), True)

print("══════════ 例題2（directed） ══════════")
V2 = ["P", "Q", "R", "S", "T"]
A2 = [("P", "Q"), ("Q", "R"), ("R", "S"), ("S", "T"), ("T", "P"),
      ("Q", "S"), ("R", "P")]
i2 = {v: sum(1 for u, w in A2 if w == v) for v in V2}
o2 = {v: sum(1 for u, w in A2 if u == v) for v in V2}
eq("(a) in degree", [i2[v] for v in V2], [2, 1, 1, 2, 1])
eq("(a) out degree", [o2[v] for v in V2], [1, 2, 2, 1, 1])
eq("(a) in の合計", sum(i2.values()), 7)
eq("(a) out の合計", sum(o2.values()), 7)
eq("(b) strongly connected",
   all(reachable(V2, A2, s) == set(V2) for s in V2), True)

print("══════════ 例題3（complete graph） ══════════")
n = sp.Symbol("n", positive=True, integer=True)
sol = sp.solve(sp.Eq(n * (n - 1) / 2, 45), n)
eq("(a) 辺が 45 本の complete graph の頂点数", sol, [10])
eq("(a) 検算 10*9/2", complete_edges(10), 45)
eq("(b) 各頂点の degree", 10 - 1, 9)
eq("(b) degree の合計 = 2 x 45", 10 * 9, 90)

print("══════════ 例題4（weighted） ══════════")
V4 = ["H", "S", "L", "P", "M"]
E4 = [("H", "S", 6), ("H", "L", 4), ("S", "L", 3), ("S", "P", 7),
      ("L", "M", 8), ("P", "M", 5)]
d4 = degrees(V4, [(u, v) for u, v, w in E4])
eq("(a) L の degree", d4["L"], 3)
eq("(b) complete なら辺は 10 本", complete_edges(5), 10)
eq("(b) 実際の辺の数", len(E4), 6)
w = {frozenset((u, v)): x for u, v, x in E4}
path = [("H", "S"), ("S", "P"), ("P", "M")]
eq("(c) H-S-P-M の重み", sum(w[frozenset(p)] for p in path), 18)
adjS = sorted({v for u, v, _ in E4 if u == "S"} |
              {u for u, v, _ in E4 if v == "S"})
eq("(d) S に adjacent な頂点", adjS, ["H", "L", "P"])

print("══════════ 演習 ══════════")
Vx = ["A", "B", "C", "D", "E", "F"]
Ex = [("A", "B"), ("A", "C"), ("A", "D"), ("B", "C"), ("C", "D"),
      ("D", "E"), ("E", "F"), ("C", "F")]
dx = degrees(Vx, Ex)
eq("1  頂点の数", len(Vx), 6)
eq("1  辺の数", len(Ex), 8)
eq("1  degree", [dx[v] for v in Vx], [3, 2, 4, 3, 2, 2])
eq("1  合計 = 2 x 8", sum(dx.values()), 16)
eq("2  辺 9 本ですべて degree 3 なら頂点は 6", 2 * 9 // 3, 6)
eq("3  K_7 の辺の数", complete_edges(7), 21)
eq("3  K_7 の degree", 7 - 1, 6)
eq("4  3 が 5 個の合計は奇数", (3 * 5) % 2, 1)
V5 = ["A", "B", "C", "D"]
A5 = [("A", "B"), ("B", "C"), ("C", "A"), ("C", "D"), ("D", "B")]
i5 = {v: sum(1 for u, w in A5 if w == v) for v in V5}
o5 = {v: sum(1 for u, w in A5 if u == v) for v in V5}
eq("5  in degree", [i5[v] for v in V5], [1, 2, 1, 1])
eq("5  out degree", [o5[v] for v in V5], [1, 1, 2, 1])
eq("5  合計はどちらも 5", (sum(i5.values()), sum(o5.values())), (5, 5))
eq("6  この directed graph は strongly connected",
   all(reachable(V5, A5, s) == set(V5) for s in V5), True)
V6 = ["P", "Q", "R", "S"]
A6 = [("P", "Q"), ("Q", "R"), ("R", "S"), ("P", "S")]
eq("6  こちらは strongly connected でない",
   all(reachable(V6, A6, s) == set(V6) for s in V6), False)
eq("6  もとにして無向にすれば connected",
   reachable(V6, A6, "S", directed=False), set(V6))
eq("7  頂点 12 の tree の辺の数", 12 - 1, 11)
eq("8  部分グラフ A,B,C と辺 AB, BC, AC の辺の数", 3, 3)
Vr = ["Hall", "Kitchen", "Lounge", "Study", "Garden"]
Er = [("Hall", "Kitchen"), ("Hall", "Lounge"), ("Hall", "Study"),
      ("Kitchen", "Garden"), ("Lounge", "Garden")]
dr = degrees(Vr, Er)
eq("9  Hall の degree", dr["Hall"], 3)
eq("9  degree の合計", sum(dr.values()), 2 * len(Er))
eq("9  connected", reachable(Vr, Er, "Study", directed=False), set(Vr))
w10 = {frozenset(("A", "B")): 5, frozenset(("B", "C")): 8,
       frozenset(("C", "D")): 4, frozenset(("A", "D")): 9,
       frozenset(("B", "D")): 6}
eq("10 A-B-D-C の重み",
   w10[frozenset(("A", "B"))] + w10[frozenset(("B", "D"))]
   + w10[frozenset(("C", "D"))], 15)
eq("10 A-D-C の重み",
   w10[frozenset(("A", "D"))] + w10[frozenset(("C", "D"))], 13)
eq("10 degree of D", 3, 3)

print()
print(f"══════════ OK {ok} / NG {ng} ══════════")
