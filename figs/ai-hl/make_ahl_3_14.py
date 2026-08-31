"""AHL 3.14 の図を作る。ラベルはすべて英語。
   出力先: ai-hl/03-geometry-and-trigonometry/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_3_14.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from _graph import (INK, LINE, ACC, GREEN, GREY, GOLD, FILL, BOX, R,
                    board, node, edge, arc_edge, loop, wlabel, note, ring)

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "03-geometry-and-trigonometry", "img")
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True)
    plt.close(fig)


# ── この項目でずっと使うグラフ G ────────────────────────────
P = {"A": (0.0, 1.6), "B": (1.6, 2.7), "C": (1.6, 0.5),
     "D": (3.2, 1.6), "E": (4.7, 1.6)}
E6 = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "D"), ("D", "E")]


def draw_G(ax, pos=None, edges=None, ecolor=GREY, ncolor=LINE, elw=2.0,
           names=True, r=R):
    pos = pos or P
    edges = edges if edges is not None else E6
    for u, v in edges:
        edge(ax, pos[u], pos[v], color=ecolor, lw=elw, r=r)
    for k, p in pos.items():
        node(ax, p, k if names else "", color=ncolor, r=r)


# ══════════════ 1. graph の部品 ══════════════
fig, ax = plt.subplots(figsize=(7.6, 4.2))
board(ax, (-0.9, 5.7), (-0.7, 3.9))
draw_G(ax)
note(ax, 0.0, 2.35, "vertex", ACC, 12)
note(ax, 2.5, 3.05, "edge", GOLD, 12)
ax.annotate("", xy=(2.4, 2.15), xytext=(2.5, 2.85),
            arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=1.6), zorder=12)
ax.annotate("", xy=(0.0, 1.95), xytext=(0.0, 2.2),
            arrowprops=dict(arrowstyle="-|>", color=ACC, lw=1.6), zorder=12)
note(ax, 5.55, 1.6, "$5$ vertices\n$6$ edges", INK, 11.5)
fig.tight_layout()
save(fig, "ahl-3-14-parts.svg")

# ══════════════ 2. 同じグラフ、置き方が違うだけ ══════════════
Q = {"A": (0.4, 0.4), "B": (0.2, 2.6), "C": (2.0, 1.3),
     "D": (3.6, 2.7), "E": (3.9, 0.5)}
fig, axs = plt.subplots(1, 2, figsize=(10.0, 4.0))
board(axs[0], (-0.9, 5.7), (-0.4, 3.5))
draw_G(axs[0])
axs[0].set_title("drawing 1", fontsize=12.5, color=INK, pad=6)
board(axs[1], (-0.9, 4.9), (-0.7, 3.5))
draw_G(axs[1], pos=Q)
axs[1].set_title("drawing 2", fontsize=12.5, color=INK, pad=6)
fig.text(0.5, 0.02, "same vertices, same edges — the same graph",
         fontsize=12, ha="center", color=ACC)
fig.tight_layout(rect=(0, 0.05, 1, 1))
save(fig, "ahl-3-14-same.svg")

# ══════════════ 3. degree と handshake ══════════════
DEG = {"A": 2, "B": 3, "C": 3, "D": 3, "E": 1}
OFF = {"A": (-0.95, 0.0), "B": (0.0, 0.62), "C": (0.0, -0.62),
       "D": (0.0, 0.62), "E": (0.95, 0.0)}
fig, ax = plt.subplots(figsize=(7.8, 4.4))
board(ax, (-1.6, 6.4), (-1.3, 3.6))
draw_G(ax)
for k, p in P.items():
    dx, dy = OFF[k]
    note(ax, p[0] + dx, p[1] + dy, f"$\\deg = {DEG[k]}$", ACC, 11)
note(ax, 2.4, -1.0,
     "$2+3+3+3+1 = 12 = 2 \\times 6$ edges", INK, 12.5)
fig.tight_layout()
save(fig, "ahl-3-14-degree.svg")

# ══════════════ 4. グラフの種類 ══════════════
fig, axs = plt.subplots(1, 4, figsize=(13.2, 3.6))

# simple
board(axs[0], (-0.7, 3.9), (-0.6, 3.4))
S = {"P": (0.2, 0.4), "Q": (0.2, 2.6), "R": (2.0, 2.6), "T": (2.0, 0.4)}
for u, v in [("P", "Q"), ("Q", "R"), ("R", "T"), ("P", "R")]:
    edge(axs[0], S[u], S[v])
for k, p in S.items():
    node(axs[0], p, k)
axs[0].set_title("simple graph", fontsize=11.5, color=INK, pad=6)

# not simple
board(axs[1], (-0.7, 3.9), (-0.6, 3.4))
for u, v in [("Q", "R"), ("R", "T"), ("P", "R")]:
    edge(axs[1], S[u], S[v])
arc_edge(axs[1], S["P"], S["Q"], rad=0.35, arrow=False)
arc_edge(axs[1], S["P"], S["Q"], rad=-0.35, arrow=False)
loop(axs[1], S["T"], size=0.42, angle=-45)
for k, p in S.items():
    node(axs[1], p, k)
note(axs[1], 0.15, 1.5, "multiple\nedge", ACC, 9.5)
note(axs[1], 2.95, 0.05, "loop", ACC, 9.5)
axs[1].set_title("not simple", fontsize=11.5, color=ACC, pad=6)

# complete K5
board(axs[2], (-2.3, 2.3), (-2.3, 2.3))
pts = ring(5, rad=1.6)
nm = ["$V_1$", "$V_2$", "$V_3$", "$V_4$", "$V_5$"]
for i in range(5):
    for j in range(i + 1, 5):
        edge(axs[2], pts[i], pts[j], lw=1.7)
for p, n in zip(pts, nm):
    node(axs[2], p, n, fs=10)
axs[2].set_title("complete graph $K_5$", fontsize=11.5, color=INK, pad=6)

# weighted
board(axs[3], (-0.7, 3.9), (-0.6, 3.4))
W = [("P", "Q", "4"), ("Q", "R", "7"), ("R", "T", "5"), ("P", "R", "9")]
for u, v, w in W:
    edge(axs[3], S[u], S[v])
    wlabel(axs[3], S[u], S[v], w)
for k, p in S.items():
    node(axs[3], p, k)
axs[3].set_title("weighted graph", fontsize=11.5, color=INK, pad=6)
fig.tight_layout()
save(fig, "ahl-3-14-kinds.svg")

# ══════════════ 5. directed graph ══════════════
D = {"A": (0.2, 0.4), "B": (0.2, 2.6), "C": (2.2, 2.6), "D": (2.2, 0.4)}
ARCS = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("B", "D")]
fig, ax = plt.subplots(figsize=(7.8, 4.0))
board(ax, (-0.8, 6.3), (-0.7, 3.6))
for u, v in ARCS:
    arc_edge(ax, D[u], D[v], rad=0.0)
for k, p in D.items():
    node(ax, p, k)
rows = [("A", 1, 1), ("B", 1, 2), ("C", 1, 1), ("D", 2, 1)]
note(ax, 4.35, 3.15, "in degree", ACC, 10.5)
note(ax, 5.45, 3.15, "out degree", GREEN, 10.5)
for i, (k, ind, outd) in enumerate(rows):
    y = 2.45 - 0.62 * i
    note(ax, 3.6, y, k, LINE, 12)
    note(ax, 4.35, y, f"${ind}$", ACC, 12)
    note(ax, 5.45, y, f"${outd}$", GREEN, 12)
fig.tight_layout()
save(fig, "ahl-3-14-directed.svg")

# ══════════════ 6. connected / strongly connected ══════════════
fig, axs = plt.subplots(1, 3, figsize=(12.0, 3.8))

board(axs[0], (-0.8, 4.0), (-0.6, 3.4))
for u, v in [("P", "Q"), ("Q", "R"), ("R", "T"), ("P", "T")]:
    edge(axs[0], S[u], S[v])
for k, p in S.items():
    node(axs[0], p, k)
axs[0].set_title("connected", fontsize=11.5, color=GREEN, pad=6)

board(axs[1], (-0.8, 4.0), (-0.6, 3.4))
for u, v in [("P", "Q"), ("R", "T")]:
    edge(axs[1], S[u], S[v])
for k, p in S.items():
    node(axs[1], p, k)
note(axs[1], 1.6, 1.5, "no route", ACC, 11)
axs[1].set_title("not connected", fontsize=11.5, color=ACC, pad=6)

board(axs[2], (-0.8, 4.0), (-0.6, 3.4))
for u, v in [("P", "Q"), ("Q", "R"), ("R", "T"), ("T", "P")]:
    arc_edge(axs[2], S[u], S[v], rad=0.0)
for k, p in S.items():
    node(axs[2], p, k)
axs[2].set_title("strongly connected", fontsize=11.5, color=GREEN, pad=6)
fig.tight_layout()
save(fig, "ahl-3-14-connected.svg")

# ══════════════ 7. subgraph と tree ══════════════
fig, axs = plt.subplots(1, 3, figsize=(12.0, 3.8))

board(axs[0], (-0.9, 5.7), (-0.5, 3.5))
draw_G(axs[0])
axs[0].set_title("the graph $G$", fontsize=11.5, color=INK, pad=6)

board(axs[1], (-0.9, 5.7), (-0.5, 3.5))
for u, v in E6:
    edge(axs[1], P[u], P[v], color="#e6e9ec", lw=1.6)
for u, v in [("A", "B"), ("B", "C")]:
    edge(axs[1], P[u], P[v], color=ACC, lw=2.6)
for k in ("A", "B", "C"):
    node(axs[1], P[k], k, color=ACC)
for k in ("D", "E"):
    node(axs[1], P[k], k, color="#c8cdd3", tc="#c8cdd3")
axs[1].set_title("a subgraph", fontsize=11.5, color=ACC, pad=6)

board(axs[2], (-0.9, 5.7), (-0.5, 3.5))
for u, v in E6:
    edge(axs[2], P[u], P[v], color="#e6e9ec", lw=1.6)
TREE = [("A", "B"), ("B", "C"), ("B", "D"), ("D", "E")]
for u, v in TREE:
    edge(axs[2], P[u], P[v], color=GREEN, lw=2.6)
for k in P:
    node(axs[2], P[k], k, color=GREEN)
axs[2].set_title("a tree: $5$ vertices, $4$ edges, no cycle",
                 fontsize=11.5, color=GREEN, pad=6)
fig.tight_layout()
save(fig, "ahl-3-14-tree.svg")

# ══════════════ 8. 現実のものをグラフにする ══════════════
fig, axs = plt.subplots(1, 2, figsize=(10.4, 4.2))

board(axs[0], (-0.4, 6.4), (-0.4, 4.4))
towns = {"Town A": (0.7, 3.4), "Town B": (2.9, 3.8), "Town C": (1.5, 1.2),
         "Town D": (4.6, 2.2), "Town E": (5.9, 3.7)}
roads = [("Town A", "Town B", "12"), ("Town A", "Town C", "8"),
         ("Town B", "Town C", "9"), ("Town B", "Town D", "15"),
         ("Town C", "Town D", "11"), ("Town D", "Town E", "6")]
for u, v, w in roads:
    axs[0].plot([towns[u][0], towns[v][0]], [towns[u][1], towns[v][1]],
                color="#c9d3dd", lw=6.0, solid_capstyle="round", zorder=2)
for u, v, w in roads:
    wlabel(axs[0], towns[u], towns[v], w + " km", GOLD, 9.5)
for k, p in towns.items():
    axs[0].plot([p[0]], [p[1]], "o", color=LINE, ms=9, zorder=6)
    axs[0].text(p[0], p[1] - 0.42, k, fontsize=9.5, ha="center", va="top",
                color=INK, zorder=7, bbox=BOX)
axs[0].set_title("roads between towns", fontsize=12, color=INK, pad=6)

board(axs[1], (-0.9, 5.9), (-0.6, 3.6))
for (u, v), (_, _, w) in zip(E6, roads):
    edge(axs[1], P[u], P[v])
    wlabel(axs[1], P[u], P[v], w, GOLD, 10)
for k, p in P.items():
    node(axs[1], p, k)
axs[1].set_title("the same information as a weighted graph",
                 fontsize=12, color=ACC, pad=6)
fig.tight_layout()
save(fig, "ahl-3-14-map.svg")

# ══════════════ 例題1 ══════════════
W1 = {"A": (0.2, 2.7), "B": (2.2, 3.1), "C": (1.1, 1.0),
      "D": (3.4, 1.5), "E": (2.6, -0.3)}
W1E = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "D"),
       ("C", "E"), ("D", "E")]
fig, ax = plt.subplots(figsize=(6.4, 4.0))
board(ax, (-0.7, 4.2), (-1.1, 3.9))
for u, v in W1E:
    edge(ax, W1[u], W1[v])
for k, p in W1.items():
    node(ax, p, k)
fig.tight_layout()
save(fig, "ahl-3-14-we1.svg")

# ══════════════ 例題2（directed） ══════════════
W2 = {"P": (0.3, 2.6), "Q": (2.6, 3.2), "R": (3.9, 1.4), "S": (2.0, 0.2),
      "T": (0.2, 0.7)}
W2E = [("P", "Q"), ("Q", "R"), ("R", "S"), ("S", "T"), ("T", "P"),
       ("Q", "S"), ("R", "P")]
fig, ax = plt.subplots(figsize=(6.6, 4.2))
board(ax, (-0.8, 4.8), (-0.6, 4.0))
for u, v in W2E:
    arc_edge(ax, W2[u], W2[v], rad=0.0)
for k, p in W2.items():
    node(ax, p, k)
fig.tight_layout()
save(fig, "ahl-3-14-we2.svg")

# ══════════════ 例題4（重み付き・現実の場面） ══════════════
W4 = {"H": (0.3, 2.4), "S": (2.4, 3.2), "L": (2.0, 0.9),
      "P": (4.3, 2.6), "M": (4.0, 0.4)}
W4E = [("H", "S", "6"), ("H", "L", "4"), ("S", "L", "3"), ("S", "P", "7"),
       ("L", "M", "8"), ("P", "M", "5")]
fig, ax = plt.subplots(figsize=(6.8, 4.2))
board(ax, (-0.8, 5.3), (-0.6, 4.0))
for u, v, w in W4E:
    edge(ax, W4[u], W4[v])
    wlabel(ax, W4[u], W4[v], w)
for k, p in W4.items():
    node(ax, p, k)
fig.tight_layout()
save(fig, "ahl-3-14-we4.svg")

print("figures written to", os.path.normpath(OUT))

# ══════════════ 演習1 ══════════════
X1 = {"A": (0.3, 2.8), "B": (2.3, 3.4), "C": (2.0, 1.6),
      "D": (0.6, 0.5), "E": (3.6, 0.4), "F": (4.4, 2.2)}
X1E = [("A", "B"), ("A", "C"), ("A", "D"), ("B", "C"), ("C", "D"),
       ("D", "E"), ("E", "F"), ("C", "F")]
fig, ax = plt.subplots(figsize=(6.6, 4.0))
board(ax, (-0.7, 5.2), (-0.6, 4.2))
for u, v in X1E:
    edge(ax, X1[u], X1[v])
for k, p in X1.items():
    node(ax, p, k)
fig.tight_layout()
save(fig, "ahl-3-14-ex1.svg")

# ══════════════ 演習5（directed） ══════════════
X5 = {"A": (0.3, 0.4), "B": (0.3, 2.6), "C": (2.5, 2.6), "D": (2.5, 0.4)}
X5A = [("A", "B"), ("B", "C"), ("C", "A"), ("C", "D"), ("D", "B")]
fig, ax = plt.subplots(figsize=(5.2, 4.0))
board(ax, (-0.7, 3.4), (-0.6, 3.4))
for u, v in X5A:
    arc_edge(ax, X5[u], X5[v], rad=0.0)
for k, p in X5.items():
    node(ax, p, k)
fig.tight_layout()
save(fig, "ahl-3-14-ex5.svg")

# ══════════════ 演習6（strongly connected かどうか） ══════════════
X6 = {"P": (0.3, 0.4), "Q": (0.3, 2.6), "R": (2.5, 2.6), "S": (2.5, 0.4)}
fig, axs = plt.subplots(1, 2, figsize=(9.2, 4.0))
for ax, arcs, ttl in ((axs[0], X5A, "graph 1"),
                      (axs[1], [("P", "Q"), ("Q", "R"), ("R", "S"),
                                ("P", "S")], "graph 2")):
    board(ax, (-0.7, 3.4), (-0.6, 3.4))
    pos = X5 if ttl == "graph 1" else X6
    for u, v in arcs:
        arc_edge(ax, pos[u], pos[v], rad=0.0)
    for k, p in pos.items():
        node(ax, p, k)
    ax.set_title(ttl, fontsize=12, color=INK, pad=6)
fig.tight_layout()
save(fig, "ahl-3-14-ex6.svg")

# ══════════════ 演習9（部屋とドア） ══════════════
X9 = {"Hall": (2.1, 1.6), "Kitchen": (0.2, 2.9), "Lounge": (0.2, 0.3),
      "Study": (4.2, 1.6), "Garden": (2.1, -1.0)}
X9E = [("Hall", "Kitchen"), ("Hall", "Lounge"), ("Hall", "Study"),
       ("Kitchen", "Garden"), ("Lounge", "Garden")]
fig, ax = plt.subplots(figsize=(6.4, 4.2))
board(ax, (-1.3, 5.6), (-2.0, 3.9))
for u, v in X9E:
    edge(ax, X9[u], X9[v], r=0.42)
for k, p in X9.items():
    node(ax, p, "", r=0.42)
    note(ax, p[0], p[1], k, LINE, 9.5, box=False)
fig.tight_layout()
save(fig, "ahl-3-14-ex9.svg")

# ══════════════ 演習10（weighted） ══════════════
XW = {"A": (0.3, 2.6), "B": (2.6, 3.0), "C": (3.4, 0.8), "D": (1.2, 0.3)}
XWE = [("A", "B", "5"), ("B", "C", "8"), ("C", "D", "4"), ("A", "D", "9"),
       ("B", "D", "6")]
fig, ax = plt.subplots(figsize=(6.0, 4.0))
board(ax, (-0.8, 4.4), (-0.7, 3.9))
for u, v, w in XWE:
    edge(ax, XW[u], XW[v])
    wlabel(ax, XW[u], XW[v], w)
for k, p in XW.items():
    node(ax, p, k)
fig.tight_layout()
save(fig, "ahl-3-14-ex10.svg")

print("exercise figures written")
