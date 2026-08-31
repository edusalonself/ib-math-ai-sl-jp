"""AHL 3.15 の図を作る。ラベルはすべて英語。
   出力先: ai-hl/03-geometry-and-trigonometry/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_3_15.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from _graph import (INK, LINE, ACC, GREEN, GREY, GOLD, BOX, R,
                    board, node, edge, arc_edge, wlabel, note, ring)
from _matrix import matrix as mtx

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "03-geometry-and-trigonometry", "img")
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True)
    plt.close(fig)


def labelled_matrix(ax, cx, cy, rows, names, cw=0.60, ch=0.52, fs=13,
                    cell_color=None, color=INK):
    """行と列に頂点名を付けた行列。"""
    centres, (x0, y0, w, h) = mtx(ax, cx, cy, rows, cw=cw, ch=ch, fs=fs,
                                  color=color, cell_color=cell_color)
    for c, nm in enumerate(names):
        X = x0 + (c + 0.5) * cw
        ax.text(X, y0 + h + 0.30, nm, fontsize=11.5, ha="center", va="bottom",
                color=LINE, weight="bold")
    for r, nm in enumerate(names):
        Y = y0 + h - (r + 0.5) * ch
        ax.text(x0 - 0.34, Y, nm, fontsize=11.5, ha="right", va="center",
                color=LINE, weight="bold")
    return centres


# ── この項目でずっと使うグラフ ──────────────────────────────
P = {"A": (0.3, 2.5), "B": (2.5, 2.5), "C": (1.4, 0.9), "D": (1.4, -0.8)}
E4 = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "D")]
NM = ["A", "B", "C", "D"]
ADJ = [["0", "1", "1", "0"],
       ["1", "0", "1", "0"],
       ["1", "1", "0", "1"],
       ["0", "0", "1", "0"]]


def draw_base(ax, ecolor=GREY, hl=None, hlc=ACC):
    for u, v in E4:
        c = hlc if hl and (u, v) in hl or hl and (v, u) in hl else ecolor
        lw = 3.0 if c == hlc and hl else 2.0
        edge(ax, P[u], P[v], color=c, lw=lw)
    for k, p in P.items():
        node(ax, p, k)


# ══════════════ 1. graph → adjacency matrix ══════════════
fig, axs = plt.subplots(1, 2, figsize=(10.4, 4.4))
board(axs[0], (-0.7, 3.5), (-1.7, 3.5))
draw_base(axs[0])
axs[0].set_title("the graph", fontsize=12.5, color=LINE, pad=6)

board(axs[1], (0, 5.0), (0, 4.4))
labelled_matrix(axs[1], 2.4, 1.9, ADJ, NM)
axs[1].set_title("its adjacency matrix $A$", fontsize=12.5, color=ACC, pad=6)
axs[1].text(2.4, 0.15, "$1$ if joined, $0$ if not", fontsize=11.5,
            ha="center", va="center", color=GREY)
fig.tight_layout()
save(fig, "ahl-3-15-idea.svg")

# ══════════════ 2. 対称かどうか ══════════════
DP = {"A": (0.3, 2.4), "B": (2.5, 2.4), "C": (1.4, 0.6)}
DA = [("A", "B"), ("B", "C"), ("C", "A")]
fig, axs = plt.subplots(1, 4, figsize=(13.2, 3.6),
                        gridspec_kw={"width_ratios": [1, 1.15, 1, 1.15]})
board(axs[0], (-0.7, 3.5), (-0.4, 3.2))
for u, v in [("A", "B"), ("B", "C"), ("C", "A")]:
    edge(axs[0], DP[u], DP[v])
for k, p in DP.items():
    node(axs[0], p, k)
axs[0].set_title("undirected", fontsize=11.5, color=LINE, pad=6)

board(axs[1], (0, 3.6), (0, 3.2))
labelled_matrix(axs[1], 1.8, 1.4,
                [["0", "1", "1"], ["1", "0", "1"], ["1", "1", "0"]],
                ["A", "B", "C"])
axs[1].set_title("symmetric", fontsize=11.5, color=GREEN, pad=6)

board(axs[2], (-0.7, 3.5), (-0.4, 3.2))
for u, v in DA:
    arc_edge(axs[2], DP[u], DP[v], rad=0.16)
for k, p in DP.items():
    node(axs[2], p, k)
axs[2].set_title("directed", fontsize=11.5, color=LINE, pad=6)

board(axs[3], (0, 3.6), (0, 3.2))
labelled_matrix(axs[3], 1.8, 1.4,
                [["0", "1", "0"], ["0", "0", "1"], ["1", "0", "0"]],
                ["A", "B", "C"],
                cell_color={(0, 1): ACC, (1, 0): ACC})
axs[3].set_title("not symmetric", fontsize=11.5, color=ACC, pad=6)
fig.tight_layout()
save(fig, "ahl-3-15-symmetric.svg")

# ══════════════ 3. walk ══════════════
fig, ax = plt.subplots(figsize=(6.6, 4.2))
board(ax, (-0.9, 3.7), (-1.8, 3.4))
draw_base(ax, hl=[("A", "B"), ("B", "C"), ("C", "D")])
note(ax, 1.4, -1.55, "the walk  $A \\to B \\to C \\to D$   (length $3$)",
     ACC, 12)
fig.tight_layout()
save(fig, "ahl-3-15-walk.svg")

# ══════════════ 4. A^2 が 2 歩の道の数 ══════════════
fig, axs = plt.subplots(1, 2, figsize=(10.6, 4.4))
board(axs[0], (-0.9, 3.7), (-1.7, 3.4))
for u, v in E4:
    edge(axs[0], P[u], P[v], color="#dfe3e8", lw=1.8)
edge(axs[0], P["A"], P["B"], color=ACC, lw=3.0)
edge(axs[0], P["B"], P["C"], color=ACC, lw=3.0)
edge(axs[0], P["A"], P["C"], color=GREEN, lw=3.0)
for k, p in P.items():
    node(axs[0], p, k)
note(axs[0], 2.7, 1.75, "$A \\to B \\to C$", ACC, 11.5)
note(axs[0], -0.15, 1.45, "$A \\to C$", GREEN, 11.5)
axs[0].set_title("walks from $A$ to $C$", fontsize=12, color=INK, pad=6)

board(axs[1], (0, 5.2), (0, 4.4))
labelled_matrix(axs[1], 2.5, 2.0,
                [["2", "1", "1", "1"], ["1", "2", "1", "1"],
                 ["1", "1", "3", "0"], ["1", "1", "0", "1"]],
                NM, cell_color={(0, 2): ACC})
axs[1].set_title("$A^{2}$", fontsize=13, color=ACC, pad=6)
axs[1].text(2.5, 0.25, "$1$ walk of length $2$ from $A$ to $C$",
            fontsize=11.5, ha="center", va="center", color=ACC)
fig.tight_layout()
save(fig, "ahl-3-15-power.svg")

# ══════════════ 5. weighted adjacency table ══════════════
WP = {"A": (0.3, 2.5), "B": (2.6, 2.7), "C": (1.3, 0.7), "D": (3.4, 0.6)}
WE = [("A", "B", "5"), ("A", "C", "3"), ("B", "C", "6"), ("B", "D", "8"),
      ("C", "D", "4")]
fig, axs = plt.subplots(1, 2, figsize=(10.8, 4.2))
board(axs[0], (-0.8, 4.3), (-0.5, 3.6))
for u, v, w in WE:
    edge(axs[0], WP[u], WP[v])
    wlabel(axs[0], WP[u], WP[v], w)
for k, p in WP.items():
    node(axs[0], p, k)
axs[0].set_title("weighted graph", fontsize=12.5, color=LINE, pad=6)

board(axs[1], (0, 5.4), (0, 4.2))
labelled_matrix(axs[1], 2.6, 1.9,
                [["–", "5", "3", "–"], ["5", "–", "6", "8"],
                 ["3", "6", "–", "4"], ["–", "8", "4", "–"]], NM, cw=0.66)
axs[1].set_title("weighted adjacency table", fontsize=12.5, color=ACC, pad=6)
axs[1].text(2.6, 0.2, "“–” means there is no edge", fontsize=11.5,
            ha="center", va="center", color=GREY)
fig.tight_layout()
save(fig, "ahl-3-15-weighted.svg")

# ══════════════ 6. transition matrix ══════════════
TP = {"A": (0.4, 2.4), "B": (3.0, 2.4), "C": (1.7, 0.4)}
TA = [("A", "B"), ("A", "C"), ("B", "A"), ("C", "A"), ("C", "B")]
fig, axs = plt.subplots(1, 2, figsize=(10.8, 4.4))
board(axs[0], (-0.8, 4.0), (-0.6, 3.3))
for u, v in TA:
    arc_edge(axs[0], TP[u], TP[v], rad=0.2)
for k, p in TP.items():
    node(axs[0], p, k)
note(axs[0], 0.4, 3.05, "out degree $2$", GREEN, 10.5)
note(axs[0], 3.0, 3.05, "out degree $1$", GREEN, 10.5)
note(axs[0], 1.7, -0.35, "out degree $2$", GREEN, 10.5)
axs[0].set_title("directed graph", fontsize=12.5, color=LINE, pad=6)

board(axs[1], (0, 5.0), (0, 4.4))
labelled_matrix(axs[1], 2.4, 2.0,
                [["0", "1", r"$\frac{1}{2}$"],
                 [r"$\frac{1}{2}$", "0", r"$\frac{1}{2}$"],
                 [r"$\frac{1}{2}$", "0", "0"]],
                ["A", "B", "C"], cw=0.72, ch=0.66)
axs[1].set_title("transition matrix $T$", fontsize=12.5, color=ACC, pad=6)
axs[1].text(2.4, 0.35, "each column adds up to $1$", fontsize=11.5,
            ha="center", va="center", color=GOLD)
fig.tight_layout()
save(fig, "ahl-3-15-transition.svg")

# ══════════════ 例題1 ══════════════
X1 = {"P": (0.3, 2.6), "Q": (2.7, 2.6), "R": (2.7, 0.4), "S": (0.3, 0.4)}
X1E = [("P", "Q"), ("P", "S"), ("Q", "R"), ("Q", "S"), ("R", "S")]
fig, ax = plt.subplots(figsize=(5.2, 4.0))
board(ax, (-0.7, 3.7), (-0.6, 3.4))
for u, v in X1E:
    edge(ax, X1[u], X1[v])
for k, p in X1.items():
    node(ax, p, k)
fig.tight_layout()
save(fig, "ahl-3-15-we1.svg")

# ══════════════ 例題3（directed、transition matrix） ══════════════
Y = {"X": (0.4, 2.5), "Y": (3.0, 2.5), "Z": (1.7, 0.4)}
YA = [("X", "Y"), ("X", "Z"), ("Y", "Z"), ("Z", "X")]
fig, ax = plt.subplots(figsize=(5.4, 3.8))
board(ax, (-0.8, 4.0), (-0.6, 3.3))
for u, v in YA:
    arc_edge(ax, Y[u], Y[v], rad=0.18)
for k, p in Y.items():
    node(ax, p, k)
fig.tight_layout()
save(fig, "ahl-3-15-we3.svg")

# ══════════════ 演習用 ══════════════
Z1 = {"A": (0.3, 2.6), "B": (2.7, 3.0), "C": (3.4, 0.8), "D": (1.2, 0.2)}
Z1E = [("A", "B"), ("A", "D"), ("B", "C"), ("B", "D"), ("C", "D")]
fig, ax = plt.subplots(figsize=(5.4, 4.0))
board(ax, (-0.7, 4.2), (-0.6, 3.8))
for u, v in Z1E:
    edge(ax, Z1[u], Z1[v])
for k, p in Z1.items():
    node(ax, p, k)
fig.tight_layout()
save(fig, "ahl-3-15-ex1.svg")

Z5 = {"P": (0.4, 2.5), "Q": (3.0, 2.5), "R": (1.7, 0.4)}
Z5A = [("P", "Q"), ("Q", "R"), ("R", "P"), ("R", "Q")]
fig, ax = plt.subplots(figsize=(5.4, 3.8))
board(ax, (-0.8, 4.0), (-0.6, 3.3))
for u, v in Z5A:
    arc_edge(ax, Z5[u], Z5[v], rad=0.18)
for k, p in Z5.items():
    node(ax, p, k)
fig.tight_layout()
save(fig, "ahl-3-15-ex5.svg")

Z8 = {"A": (0.3, 2.6), "B": (2.8, 2.8), "C": (3.2, 0.6), "D": (1.0, 0.2)}
Z8E = [("A", "B", "7"), ("A", "D", "5"), ("B", "C", "6"), ("B", "D", "9"),
       ("C", "D", "3")]
fig, ax = plt.subplots(figsize=(5.6, 4.0))
board(ax, (-0.8, 4.1), (-0.6, 3.7))
for u, v, w in Z8E:
    edge(ax, Z8[u], Z8[v])
    wlabel(ax, Z8[u], Z8[v], w)
for k, p in Z8.items():
    node(ax, p, k)
fig.tight_layout()
save(fig, "ahl-3-15-ex8.svg")

print("figures written to", os.path.normpath(OUT))
