"""AHL 3.16 の本文・例題・演習の数値を独立に検算する。
   MST は Kruskal と Prim の【2 通り】で出し、TSP は全部の Hamiltonian cycle を
   数え上げて、上界・下界がそれを正しくはさんでいるかを見る。
   実行: python3 figs/ai-hl/check_ahl_3_16.py
"""
import heapq
import itertools
import math

ok, ng = 0, 0


def eq(name, got, want):
    global ok, ng
    good = got == want
    print(("  OK   " if good else "  ★NG★ ") + name +
          ("" if good else f"   got {got}  want {want}"))
    ok, ng = ok + good, ng + (not good)


# ── 道具 ────────────────────────────────────────────────
def degrees(V, E):
    return {v: sum(1 for e in E if v in e) for v in V}


def kruskal(V, E):
    par = {v: v for v in V}

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    chosen, total = [], 0
    for (u, v), w in sorted(E.items(), key=lambda kv: (kv[1], kv[0])):
        if find(u) != find(v):
            par[find(u)] = find(v)
            chosen.append(((u, v), w))
            total += w
    return chosen, total


def prim(V, E, start):
    inT, chosen, total = {start}, [], 0
    while len(inT) < len(V):
        best = None
        for (u, v), w in sorted(E.items(), key=lambda kv: (kv[1], kv[0])):
            if (u in inT) ^ (v in inT):
                if best is None or w < best[1]:
                    best = ((u, v), w)
        chosen.append(best)
        total += best[1]
        inT |= set(best[0])
    return chosen, total


def shortest(V, E, s, t):
    adj = {v: [] for v in V}
    for (u, v), w in E.items():
        adj[u].append((v, w))
        adj[v].append((u, w))
    d = {v: math.inf for v in V}
    d[s] = 0
    prev, pq = {}, [(0, s)]
    while pq:
        dd, x = heapq.heappop(pq)
        if dd > d[x]:
            continue
        for y, w in adj[x]:
            if dd + w < d[y]:
                d[y] = dd + w
                prev[y] = x
                heapq.heappush(pq, (d[y], y))
    path = [t]
    while path[-1] != s:
        path.append(prev[path[-1]])
    return d[t], list(reversed(path))


def wt(W, a, b):
    return W[frozenset((a, b))]


def nearest_neighbour(V, W, start):
    cur, unv, route, total = start, set(V) - {start}, [start], 0
    while unv:
        nxt = min(sorted(unv), key=lambda x: wt(W, cur, x))
        total += wt(W, cur, nxt)
        route.append(nxt)
        unv.remove(nxt)
        cur = nxt
    total += wt(W, cur, start)
    route.append(start)
    return total, route


def best_cycle(V, W, start):
    rest = [v for v in V if v != start]
    best = (math.inf, None)
    for p in itertools.permutations(rest):
        c = (start,) + p + (start,)
        t = sum(wt(W, c[i], c[i + 1]) for i in range(len(V)))
        if t < best[0]:
            best = (t, c)
    return best


def deleted_vertex(V, W, drop):
    rest = [v for v in V if v != drop]
    E = {(a, b): wt(W, a, b) for a, b in itertools.combinations(rest, 2)}
    _, mst = kruskal(rest, E)
    two = sorted(wt(W, drop, x) for x in rest)[:2]
    return mst, two, mst + sum(two)


# ══════════════ この項目でずっと使うグラフ G ══════════════
print("══════════ The idea：グラフ G ══════════")
V = list("ABCDE")
E = {("A", "B"): 4, ("A", "C"): 6, ("A", "D"): 8, ("B", "C"): 3,
     ("B", "D"): 7, ("C", "D"): 5, ("C", "E"): 9, ("D", "E"): 2}
d = degrees(V, E)
eq("degree", [d[v] for v in V], [3, 3, 4, 4, 2])
eq("degree の合計 = 2 x 辺の数", sum(d.values()), 2 * len(E))
eq("奇数次数の頂点", [v for v in V if d[v] % 2], ["A", "B"])
eq("辺の重みの合計", sum(E.values()), 44)
eq("奇数が 2 個なので Eulerian trail はある",
   len([v for v in V if d[v] % 2]) == 2, True)
eq("Eulerian circuit はない", len([v for v in V if d[v] % 2]) == 0, False)

print("══════════ minimum spanning tree ══════════")
kr, ktot = kruskal(V, E)
eq("Kruskal が選ぶ辺の順", [e for e, w in kr],
   [("D", "E"), ("B", "C"), ("A", "B"), ("C", "D")])
eq("Kruskal の重み", [w for e, w in kr], [2, 3, 4, 5])
eq("MST の重み", ktot, 14)
eq("MST の辺の数 = 頂点 - 1", len(kr), len(V) - 1)
pr, ptot = prim(V, E, "A")
eq("Prim（A から）が選ぶ辺の順", [e for e, w in pr],
   [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E")])
eq("Prim の重み", [w for e, w in pr], [4, 3, 5, 2])
eq("Prim と Kruskal は同じ重み", ptot, ktot)
eq("同じ辺の集合", sorted(tuple(sorted(e)) for e, w in kr),
   sorted(tuple(sorted(e)) for e, w in pr))
for s in V:
    _, t = prim(V, E, s)
    eq(f"Prim をどこから始めても {t}", t, 14)

print("══════════ Chinese postman ══════════")
dist, path = shortest(V, E, "A", "B")
eq("A から B への最短", dist, 4)
eq("その道", path, ["A", "B"])
eq("A-C-B は 9", E[("A", "C")] + E[("B", "C")], 9)
eq("A-D-B は 15", E[("A", "D")] + E[("B", "D")], 15)
eq("Chinese postman の長さ", sum(E.values()) + dist, 48)

print("══════════ 第12・13節（TSP：完全グラフ） ══════════")
TV = list("PQRS")
W = {frozenset(("P", "Q")): 5, frozenset(("P", "R")): 9,
     frozenset(("P", "S")): 7, frozenset(("Q", "R")): 6,
     frozenset(("Q", "S")): 8, frozenset(("R", "S")): 4}
eq("完全グラフの辺の数", len(W), 4 * 3 // 2)
nn, route = nearest_neighbour(TV, W, "P")
eq("(a) nearest neighbour の経路", route, ["P", "Q", "R", "S", "P"])
eq("(a) 上界", nn, 22)
mst, two, lb = deleted_vertex(TV, W, "P")
eq("(b) 残りの MST", mst, 10)
eq("(b) P からの小さい 2 本", two, [5, 7])
eq("(b) 下界", lb, 22)
best, cyc = best_cycle(TV, W, "P")
eq("(c) 本当の最短", best, 22)
eq("(c) 上界と下界が一致するので、これが最適", nn == lb == best, True)
allc = sorted(sum(wt(W, (("P",) + p + ("P",))[i], (("P",) + p + ("P",))[i + 1])
                  for i in range(4))
              for p in itertools.permutations("QRS"))
eq("すべての Hamiltonian cycle", allc, [22, 22, 26, 26, 30, 30])

print("══════════ table of least distances ══════════")
LV = list("LMN")
LE = {("L", "M"): 5, ("M", "N"): 6, ("L", "N"): 12}
eq("直接の L-N は 12", LE[("L", "N")], 12)
eq("L-M-N は 11", LE[("L", "M")] + LE[("M", "N")], 11)
eq("最短距離は 11", shortest(LV, LE, "L", "N")[0], 11)
eq("その道", shortest(LV, LE, "L", "N")[1], ["L", "M", "N"])

print("══════════ 演習 ══════════")
# 2 Euler の判定
X2 = list("ABCD")
E2 = {("A", "B"): 1, ("A", "C"): 1, ("A", "D"): 1, ("B", "C"): 1,
      ("B", "D"): 1, ("C", "D"): 1}
d2 = degrees(X2, E2)
eq("2  K_4 の degree", [d2[v] for v in X2], [3, 3, 3, 3])
eq("2  奇数次数は 4 個", len([v for v in X2 if d2[v] % 2]), 4)
eq("2  Eulerian trail も circuit もない",
   len([v for v in X2 if d2[v] % 2]) not in (0, 2), True)
# 3 Kruskal
V3 = list("ABCDE")
E3 = {("A", "B"): 7, ("A", "C"): 3, ("B", "C"): 5, ("B", "D"): 4,
      ("C", "D"): 6, ("C", "E"): 8, ("D", "E"): 2}
k3, t3 = kruskal(V3, E3)
eq("3  Kruskal の選ぶ順", [e for e, w in k3],
   [("D", "E"), ("A", "C"), ("B", "D"), ("B", "C")])
eq("3  重み", [w for e, w in k3], [2, 3, 4, 5])
eq("3  MST の重み", t3, 14)
# 1 用語（同じグラフを使う）
eq("1  A-C-B-D-E の辺がすべて存在する（path）",
   [(("A", "C") in E3), (("B", "C") in E3), (("B", "D") in E3),
    (("D", "E") in E3)], [True, True, True, True])
eq("1  A-B-C-A は cycle（辺 3 本）",
   [(("A", "B") in E3), (("B", "C") in E3), (("A", "C") in E3)],
   [True, True, True])
# 4 Prim（同じグラフ、A から）
p4, t4 = prim(V3, E3, "A")
eq("4  Prim（A から）の順", [e for e, w in p4],
   [("A", "C"), ("B", "C"), ("B", "D"), ("D", "E")])
eq("4  重み", [w for e, w in p4], [3, 5, 4, 2])
eq("4  合計は Kruskal と同じ", t4, t3)
# 5 Chinese postman（同じグラフ）
d3 = degrees(V3, E3)
eq("5  degree", [d3[v] for v in V3], [2, 3, 4, 3, 2])
eq("5  奇数次数", [v for v in V3 if d3[v] % 2], ["B", "D"])
eq("5  辺の重みの合計", sum(E3.values()), 35)
sd, sp_ = shortest(V3, E3, "B", "D")
eq("5  B から D への最短", sd, 4)
eq("5  その道", sp_, ["B", "D"])
eq("5  Chinese postman の長さ", sum(E3.values()) + sd, 39)
# 6, 7 TSP
TV2 = list("FHJK")
W2 = {frozenset(("F", "H")): 19, frozenset(("F", "J")): 5,
      frozenset(("F", "K")): 13, frozenset(("H", "J")): 11,
      frozenset(("H", "K")): 2, frozenset(("J", "K")): 10}
n6, r6 = nearest_neighbour(TV2, W2, "F")
eq("6  NN（F から）の経路", r6, ["F", "J", "K", "H", "F"])
eq("6  NN（F から）の上界", n6, 36)
n6b, r6b = nearest_neighbour(TV2, W2, "J")
eq("6  NN（J から）の経路", r6b, ["J", "F", "K", "H", "J"])
eq("6  NN（J から）の上界", n6b, 31)
eq("6  小さいほうを採る", min(n6, n6b), 31)
m7, two7, lb7 = deleted_vertex(TV2, W2, "F")
eq("7  残りの MST", m7, 12)
eq("7  F からの小さい 2 本", two7, [5, 13])
eq("7  下界", lb7, 30)
b7, c7 = best_cycle(TV2, W2, "F")
eq("7  本当の最短", b7, 31)
eq("7  下界 <= 最短 <= 上界", lb7 <= b7 <= 31, True)
# 8 table of least distances
V8 = list("ABCD")
E8 = {("A", "B"): 6, ("B", "C"): 5, ("C", "D"): 4, ("A", "D"): 20,
      ("B", "D"): 9}
eq("8  A-D 直接は 20", E8[("A", "D")], 20)
eq("8  A-B-C-D は 15", 6 + 5 + 4, 15)
eq("8  A-B-D は 15", 6 + 9, 15)
eq("8  最短距離は 15", shortest(V8, E8, "A", "D")[0], 15)
eq("8  A-C は直接ないので 11", shortest(V8, E8, "A", "C")[0], 11)

print()
print(f"══════════ OK {ok} / NG {ng} ══════════")

print("══════════ 例題5（odd vertex が 4 個の Chinese postman） ══════════")
V4 = list("WXYZ")
E4 = {("W", "X"): 3, ("X", "Y"): 4, ("Y", "Z"): 3, ("W", "Z"): 4,
      ("W", "Y"): 5, ("X", "Z"): 6}
d4 = degrees(V4, E4)
eq("4  degree", [d4[v] for v in V4], [3, 3, 3, 3])
eq("4  奇数次数は 4 個", [v for v in V4 if d4[v] % 2], ["W", "X", "Y", "Z"])
eq("4  辺の重みの合計", sum(E4.values()), 25)
sp = {}
for a, b in itertools.combinations(V4, 2):
    sp[(a, b)] = shortest(V4, E4, a, b)[0]
eq("4  最短 W-X", sp[("W", "X")], 3)
eq("4  最短 Y-Z", sp[("Y", "Z")], 3)
eq("4  最短 W-Y", sp[("W", "Y")], 5)
eq("4  最短 X-Z", sp[("X", "Z")], 6)
eq("4  最短 W-Z", sp[("W", "Z")], 4)
eq("4  最短 X-Y", sp[("X", "Y")], 4)
pairings = [(("W", "X"), ("Y", "Z")), (("W", "Y"), ("X", "Z")),
            (("W", "Z"), ("X", "Y"))]
sums = [sp[p] + sp[q] for p, q in pairings]
eq("4  3 通りのペアの合計", sums, [6, 11, 8])
eq("4  いちばん小さいのは 6", min(sums), 6)
eq("4  Chinese postman の長さ", sum(E4.values()) + min(sums), 31)

print("══════════ すべての単純な道（数え落としの確認） ══════════")


def all_paths(V, E, s, t):
    adj = {v: [] for v in V}
    for (u, v), w in E.items():
        adj[u].append((v, w))
        adj[v].append((u, w))
    out = []

    def go(x, seen, tot, route):
        if x == t:
            out.append((route, tot))
            return
        for y, w in adj[x]:
            if y not in seen:
                go(y, seen | {y}, tot + w, route + [y])
    go(s, {s}, 0, [s])
    return sorted(out, key=lambda r: r[1])


ab = all_paths(V, E, "A", "B")
eq("G の A-B の単純な道は 7 通り", len(ab), 7)
eq("その長さ", [t for r, t in ab], [4, 9, 15, 16, 18, 22, 24])
bd = all_paths(V3, E3, "B", "D")
eq("演習グラフの B-D の単純な道は 5 通り", len(bd), 5)
eq("その長さ", [t for r, t in bd], [4, 11, 15, 16, 20])
ac8 = all_paths(V8, E8, "A", "C")
eq("演習8 の A-C の単純な道は 4 通り", len(ac8), 4)
eq("その長さ", [t for r, t in ac8], [11, 19, 24, 34])
ad8 = all_paths(V8, E8, "A", "D")
eq("演習8 の A-D の単純な道は 3 通り", len(ad8), 3)
eq("その長さ", [t for r, t in ad8], [15, 15, 20])

print("══════════ 演習6 のグラフは、最短距離の表になっていない ══════════")
eq("F-H は直接 19、F-K-H は 15", wt(W2, "F", "K") + wt(W2, "K", "H"), 15)

print("══════════ 追加：演習10（nearest neighbour の同点） ══════════")
W10 = {frozenset(("P", "Q")): 4, frozenset(("P", "R")): 4,
       frozenset(("P", "S")): 12, frozenset(("Q", "R")): 3,
       frozenset(("Q", "S")): 11, frozenset(("R", "S")): 5}
V10 = list("PQRS")
eq("P から見て Q と R はどちらも 4", wt(W10, "P", "Q"), wt(W10, "P", "R"))
eq("P-S = 12 がいちばん遠い",
   max(wt(W10, "P", x) for x in "QRS"), 12)
a10 = 4 + wt(W10, "Q", "R") + wt(W10, "R", "S") + wt(W10, "S", "P")
eq("P-Q-R-S-P = 4+3+5+12 = 24", a10, 24)
b10 = 4 + wt(W10, "R", "Q") + wt(W10, "Q", "S") + wt(W10, "S", "P")
eq("P-R-Q-S-P = 4+3+11+12 = 30", b10, 30)
eq("同点の選び方で上界が変わる", a10 != b10, True)
eq("よいほうは 24", min(a10, b10), 24)
bt10, bc10 = best_cycle(V10, W10, "P")
eq("実際の最短も 24", bt10, 24)
eq("nearest neighbour（Q を先に）は正しい上界", a10 >= bt10, True)
# 3 通りの cycle をすべて出して確かめる
tot = sorted(set(
    sum(wt(W10, c[i], c[i + 1]) for i in range(4))
    for pmt in itertools.permutations("QRS")
    for c in [("P",) + pmt + ("P",)]))
eq("cycle の重みは 24 と 30 の 2 種類", tot, [24, 30])
lb10 = deleted_vertex(V10, W10, "P")
eq("P を消した下界の内訳（MST, 2 本）", (lb10[0], lb10[1]), (8, [4, 4]))
eq("P を消した下界は 16", lb10[2], 16)
eq("16 <= 24", lb10[2] <= bt10, True)

print()
print(f"══════════ 追加分を入れて OK {ok} / NG {ng} ══════════")

print("══════════ 例題6（TSP：R から / S を消す） ══════════")
nnR, rtR = nearest_neighbour(TV, W, "R")
eq("例題6 (a) NN（R から）の経路", rtR, ["R", "S", "P", "Q", "R"])
eq("例題6 (a) 上界", nnR, 22)
mS, twoS, lbS = deleted_vertex(TV, W, "S")
eq("例題6 (b) 残りの MST", mS, 11)
eq("例題6 (b) S からの小さい 2 本", twoS, [4, 7])
eq("例題6 (b) 下界", lbS, 22)
eq("例題6 (c) どちらも 22 なので確定", nnR == lbS == 22, True)
for v in TV:
    eq(f"NN をどこから始めても 22（{v}）", nearest_neighbour(TV, W, v)[0], 22)
    eq(f"どの点を消しても下界 22（{v}）", deleted_vertex(TV, W, v)[2], 22)

print("══════════ 演習9（odd vertex が 4 個） ══════════")
V9 = list("ABCDE")
E9 = {("A", "B"): 8, ("A", "C"): 5, ("B", "C"): 6, ("B", "D"): 7,
      ("C", "D"): 4, ("C", "E"): 9, ("D", "E"): 3, ("A", "E"): 6}
d9 = degrees(V9, E9)
eq("9  degree", [d9[v] for v in V9], [3, 3, 4, 3, 3])
eq("9  奇数次数", [v for v in V9 if d9[v] % 2], ["A", "B", "D", "E"])
eq("9  辺の重みの合計", sum(E9.values()), 48)
eq("9  最短 A-B", shortest(V9, E9, "A", "B")[0], 8)
eq("9  最短 D-E", shortest(V9, E9, "D", "E")[0], 3)
eq("9  最短 A-D", shortest(V9, E9, "A", "D")[0], 9)
eq("9  A-D は直接の辺がない", ("A", "D") not in E9 and ("D", "A") not in E9,
   True)
eq("9  A-C-D は 9", E9[("A", "C")] + E9[("C", "D")], 9)
eq("9  A-E-D は 9", E9[("A", "E")] + E9[("D", "E")], 9)
eq("9  最短 B-E", shortest(V9, E9, "B", "E")[0], 10)
eq("9  B-D-E は 10", E9[("B", "D")] + E9[("D", "E")], 10)
s9 = [shortest(V9, E9, "A", "B")[0] + shortest(V9, E9, "D", "E")[0],
      shortest(V9, E9, "A", "D")[0] + shortest(V9, E9, "B", "E")[0],
      shortest(V9, E9, "A", "E")[0] + shortest(V9, E9, "B", "D")[0]]
eq("9  3 通りのペアの合計", s9, [11, 19, 13])
eq("9  いちばん小さいのは 11", min(s9), 11)
eq("9  Chinese postman の長さ", sum(E9.values()) + min(s9), 59)

print()
print(f"══════════ 最終 OK {ok} / NG {ng} ══════════")

print("══════════ 追加：同じ重みが並ぶとき、MST は 1 つに決まらない ══════════")
TV = list("PQRS")
TE = {("P", "Q"): 2, ("P", "R"): 2, ("Q", "R"): 3, ("Q", "S"): 4,
      ("R", "S"): 4}
_, tk = kruskal(TV, TE)
eq("Kruskal の合計は 8", tk, 8)
for st in TV:
    _, tp = prim(TV, TE, st)
    eq(f"Prim（{st} から）も 8", tp, 8)
# 全部の spanning tree を数え上げて、最小合計が 8、それを達成する木が 2 つ
trees = []
for comb in itertools.combinations(TE.items(), 3):
    es = [c[0] for c in comb]
    par = {v: v for v in TV}

    def find(x, par=par):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    okt = True
    for u, v in es:
        if find(u) == find(v):
            okt = False
            break
        par[find(u)] = find(v)
    if okt:
        trees.append((sum(c[1] for c in comb), frozenset(es)))
best = min(t[0] for t in trees)
eq("最小の合計は 8", best, 8)
mins = sorted(t[1] for t in trees if t[0] == best)
eq("最小を達成する spanning tree は 2 つ", len(mins), 2)
eq("その 2 つは QS を採るものと RS を採るもの",
   sorted(sorted(m) for m in mins),
   [[("P", "Q"), ("P", "R"), ("Q", "S")],
    [("P", "Q"), ("P", "R"), ("R", "S")]])
eq("どちらも 3 本 = 4 - 1", [len(m) for m in mins], [3, 3])

print("══════════ 追加：TSP の cycle の数 (n-1)!/2 ══════════")
for n in (4, 5, 6, 8):
    eq(f"n = {n} なら {math.factorial(n - 1) // 2} 通り",
       math.factorial(n - 1) // 2, {4: 3, 5: 12, 6: 60, 8: 2520}[n])
# 4 点で、出発点を固定して逆回りを同一視すると本当に 3 通りか
seen = set()
for p in itertools.permutations("QRS"):
    c = ("P",) + p
    seen.add(min(tuple(c), tuple([c[0]] + list(reversed(c[1:])))))
eq("4 点の実際の cycle は 3 通り", len(seen), 3)

print("══════════ 追加：deleted vertex の下界の根拠 ══════════")
# 完全グラフ（例題6の P,Q,R,S）で、どの Hamiltonian cycle も
# 「v を除いた spanning path の重み + v に付く 2 本」に分解できる
W6 = {frozenset(("P", "Q")): 5, frozenset(("P", "R")): 9,
      frozenset(("P", "S")): 7, frozenset(("Q", "R")): 6,
      frozenset(("Q", "S")): 8, frozenset(("R", "S")): 4}
V6 = list("PQRS")
for drop in V6:
    rest = [v for v in V6 if v != drop]
    E6 = {(a, b): wt(W6, a, b) for a, b in itertools.combinations(rest, 2)}
    _, mstw = kruskal(rest, E6)
    lb = deleted_vertex(V6, W6, drop)[2]
    # すべての Hamiltonian cycle を回して、分解を確かめる
    worst = math.inf
    for p in itertools.permutations([v for v in V6 if v != "P"]):
        c = ("P",) + p + ("P",)
        tot = sum(wt(W6, c[i], c[i + 1]) for i in range(4))
        # drop を取り除くと、残りは spanning path になる
        i = list(c[:-1]).index(drop)
        seq = list(c[:-1])[i + 1:] + list(c[:-1])[:i]
        pathw = sum(wt(W6, seq[k], seq[k + 1]) for k in range(len(seq) - 1))
        eq_pair = pathw + wt(W6, drop, seq[0]) + wt(W6, drop, seq[-1])
        assert eq_pair == tot
        worst = min(worst, tot)
    eq(f"{drop} を消した残りの MST は spanning path 以下（下界 {lb} <= 最短 {worst}）",
       lb <= worst, True)
    eq(f"{drop} を消した MST は {mstw}", mstw >= 0, True)

print("══════════ 追加：nearest neighbour で同点が出るグラフ ══════════")
WT = {frozenset(("A", "B")): 3, frozenset(("A", "C")): 3,
      frozenset(("A", "D")): 10, frozenset(("B", "C")): 2,
      frozenset(("B", "D")): 9, frozenset(("C", "D")): 4}
VT = list("ABCD")
eq("A から見て B と C はどちらも 3", wt(WT, "A", "B"), wt(WT, "A", "C"))
r1 = 3 + wt(WT, "B", "C") + wt(WT, "C", "D") + wt(WT, "D", "A")
eq("A-B-C-D-A = 3+2+4+10 = 19", r1, 19)
r2 = 3 + wt(WT, "C", "B") + wt(WT, "B", "D") + wt(WT, "D", "A")
eq("A-C-B-D-A = 3+2+9+10 = 24", r2, 24)
eq("同点の選び方で上界が変わる", r1 != r2, True)
eq("よいほう（小さいほう）は 19", min(r1, r2), 19)
bt, bc = best_cycle(VT, WT, "A")
eq("実際の最短は 19", bt, 19)
eq("上界 19 は最短以上", r1 >= bt, True)
lbA = deleted_vertex(VT, WT, "A")
eq("A を消した下界の内訳（MST, 2 本）", (lbA[0], lbA[1]), (6, [3, 3]))
eq("A を消した下界は 12", lbA[2], 12)
eq("12 <= 19", lbA[2] <= bt, True)

print()
print(f"══════════ 追加分を入れて OK {ok} / NG {ng} ══════════")
