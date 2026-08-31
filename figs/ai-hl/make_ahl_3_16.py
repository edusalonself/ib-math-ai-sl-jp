"""AHL 3.16 の図を作る。ラベルはすべて英語。
   出力先: ai-hl/03-geometry-and-trigonometry/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_3_16.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from _graph import (INK, GRID, LINE, ACC, GREEN, GREY, GOLD, BOX, R,
                    board, node, edge, arc_edge, wlabel, note)

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "03-geometry-and-trigonometry", "img")
os.makedirs(OUT, exist_ok=True)
PALE = "#dfe3e8"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True)
    plt.close(fig)


# ── この項目でずっと使う重み付きグラフ G ────────────────────
P = {"A": (0.4, 3.1), "B": (3.4, 3.1), "C": (0.4, 0.9), "D": (3.4, 0.9),
     "E": (5.9, 2.0)}
G = [("A", "B", 4), ("A", "C", 6), ("A", "D", 8), ("B", "C", 3),
     ("B", "D", 7), ("C", "D", 5), ("C", "E", 9), ("D", "E", 2)]


# 交差する 2 本の対角線などで重みラベルが重ならないよう、辺ごとに
# 「辺の何割の位置に置くか」を決めておく。
LPOS = {("A", "D"): 0.30, ("B", "C"): 0.30, ("C", "E"): 0.84,
        ("D", "E"): 0.36}


def draw_G(ax, pos=None, keep=None, hl=None, hlc=ACC, faint=PALE,
           labels=True, lw=2.0):
    """keep=None ならすべて通常色。hl にある辺だけ強調し、残りは薄く。"""
    pos = pos or P
    for u, v, w in G:
        on = hl is None or (u, v) in hl or (v, u) in hl
        col = (hlc if hl is not None and on else
               (GREY if hl is None else faint))
        edge(ax, pos[u], pos[v], color=col,
             lw=(lw + 1.0 if hl is not None and on else lw))
        if labels:
            wlabel(ax, pos[u], pos[v], f"${w}$",
                   color=(hlc if hl is not None and on else GOLD), fs=10.5,
                   t=LPOS.get((u, v), 0.5))
    for k, p in pos.items():
        node(ax, p, k)


# ══════════════ 1. 用語（walk / trail / path / cycle） ══════════════
S = {"A": (0.3, 2.5), "B": (2.5, 2.5), "C": (0.3, 0.4), "D": (2.5, 0.4)}
SE = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "D")]
WORDS = [
    ("walk", [("A", "B"), ("B", "C"), ("C", "A"), ("A", "B")],
     "$A \\to B \\to C \\to A \\to B$"),
    ("trail", [("C", "A"), ("A", "B"), ("B", "C"), ("C", "D")],
     "$C \\to A \\to B \\to C \\to D$"),
    ("path", [("A", "B"), ("B", "D")], "$A \\to B \\to D$"),
    ("cycle", [("A", "B"), ("B", "C"), ("C", "A")],
     "$A \\to B \\to C \\to A$"),
]
fig, axs = plt.subplots(1, 4, figsize=(13.4, 3.8))
for ax, (name, use, sub) in zip(axs, WORDS):
    board(ax, (-0.7, 3.5), (-1.1, 3.2))
    for u, v in SE:
        edge(ax, S[u], S[v], color=PALE, lw=1.8)
    for u, v in use:
        edge(ax, S[u], S[v], color=ACC, lw=3.0)
    for k, p in S.items():
        node(ax, p, k)
    ax.set_title(name, fontsize=12.5, color=INK, pad=6)
    note(ax, 1.4, -0.75, sub, GREY, 10)
fig.tight_layout()
save(fig, "ahl-3-16-words.svg")

# ══════════════ 2. 重み付きグラフ G ══════════════
DEG = {"A": 3, "B": 3, "C": 4, "D": 4, "E": 2}
OFF = {"A": (-0.05, 0.62), "B": (0.05, 0.62), "C": (-0.05, -0.62),
       "D": (0.05, -0.62), "E": (0.85, 0.0)}
fig, ax = plt.subplots(figsize=(8.0, 4.6))
board(ax, (-1.2, 7.4), (-0.8, 4.3))
draw_G(ax)
for k, p in P.items():
    dx, dy = OFF[k]
    note(ax, p[0] + dx, p[1] + dy, f"$\\deg = {DEG[k]}$", ACC, 10)
note(ax, 3.0, -0.45, "total weight $= 44$", INK, 11.5)
fig.tight_layout()
save(fig, "ahl-3-16-graph.svg")

# ══════════════ 3. Eulerian の判定 ══════════════
E3 = {"A": (0.3, 2.5), "B": (2.5, 2.5), "C": (0.3, 0.4), "D": (2.5, 0.4)}
CASES = [
    ("$0$ odd vertices", [("A", "B"), ("B", "D"), ("D", "C"), ("C", "A")],
     "Eulerian circuit", GREEN),
    ("$2$ odd vertices",
     [("A", "B"), ("B", "D"), ("D", "C"), ("C", "A"), ("A", "D")],
     "Eulerian trail", GOLD),
    ("$4$ odd vertices",
     [("A", "B"), ("B", "D"), ("D", "C"), ("C", "A"), ("A", "D"),
      ("B", "C")], "neither", ACC),
]
fig, axs = plt.subplots(1, 3, figsize=(12.0, 4.0))
for ax, (title, es, verdict, col) in zip(axs, CASES):
    board(ax, (-0.7, 3.5), (-1.0, 3.2))
    for u, v in es:
        edge(ax, E3[u], E3[v], color=GREY, lw=2.0)
    dd = {k: sum(1 for u, v in es if k in (u, v)) for k in E3}
    for k, p in E3.items():
        node(ax, p, k, color=(ACC if dd[k] % 2 else LINE))
        up = k in ("A", "B")
        ax.text(p[0], p[1] + (0.52 if up else -0.52), f"${dd[k]}$",
                fontsize=10.5, ha="center", va=("bottom" if up else "top"),
                color=(ACC if dd[k] % 2 else GREY), zorder=12)
    ax.set_title(title, fontsize=11.5, color=INK, pad=6)
    note(ax, 1.4, -0.72, verdict, col, 11.5)
fig.text(0.5, 0.015, "red = odd degree", fontsize=11, ha="center", color=GREY)
fig.tight_layout(rect=(0, 0.04, 1, 1))
save(fig, "ahl-3-16-euler.svg")

# ══════════════ 4. Hamiltonian cycle ══════════════
fig, ax = plt.subplots(figsize=(7.2, 4.2))
board(ax, (-0.9, 7.0), (-0.9, 4.2))
draw_G(ax, hl=[("A", "B"), ("B", "C"), ("C", "E"), ("E", "D"), ("D", "A")])
note(ax, 3.0, -0.55, "$A \\to B \\to C \\to E \\to D \\to A$  —  "
                     "every vertex once", ACC, 11.5)
fig.tight_layout()
save(fig, "ahl-3-16-hamilton.svg")

# ══════════════ 5. Kruskal ══════════════
KR = [("D", "E", 2), ("B", "C", 3), ("A", "B", 4), ("C", "D", 5)]
fig, axs = plt.subplots(1, 4, figsize=(13.6, 3.6))
for i, ax in enumerate(axs):
    board(ax, (-0.9, 7.0), (-1.0, 4.1))
    chosen = [(u, v) for u, v, w in KR[:i + 1]]
    draw_G(ax, hl=chosen, hlc=GREEN, labels=False)
    for u, v, w in KR[:i + 1]:
        wlabel(ax, P[u], P[v], f"${w}$", color=GREEN, fs=10.5)
    u, v, w = KR[i]
    ax.set_title(f"step {i + 1}:  add ${u}{v} = {w}$", fontsize=11.5,
                 color=GREEN, pad=6)
    note(ax, 3.0, -0.62, f"total $= {sum(x[2] for x in KR[:i + 1])}$",
         INK, 11)
fig.tight_layout()
save(fig, "ahl-3-16-kruskal.svg")

# ══════════════ 6. Prim（A から） ══════════════
PR = [("A", "B", 4), ("B", "C", 3), ("C", "D", 5), ("D", "E", 2)]
fig, axs = plt.subplots(1, 4, figsize=(13.6, 3.6))
for i, ax in enumerate(axs):
    board(ax, (-0.9, 7.0), (-1.0, 4.1))
    chosen = [(u, v) for u, v, w in PR[:i + 1]]
    draw_G(ax, hl=chosen, hlc=ACC, labels=False)
    for u, v, w in PR[:i + 1]:
        wlabel(ax, P[u], P[v], f"${w}$", color=ACC, fs=10.5)
    inT = {"A"}
    for u, v, w in PR[:i + 1]:
        inT |= {u, v}
    for k in inT:
        node(ax, P[k], k, color=ACC)
    u, v, w = PR[i]
    ax.set_title(f"step {i + 1}:  add ${u}{v} = {w}$", fontsize=11.5,
                 color=ACC, pad=6)
    note(ax, 3.0, -0.62, f"total $= {sum(x[2] for x in PR[:i + 1])}$",
         INK, 11)
fig.tight_layout()
save(fig, "ahl-3-16-prim.svg")

# ══════════════ 7. Prim の行列法 ══════════════
NAMES = list("ABCDE")
TAB = [["–", "4", "6", "8", "–"],
       ["4", "–", "3", "7", "–"],
       ["6", "3", "–", "5", "9"],
       ["8", "7", "5", "–", "2"],
       ["–", "–", "9", "2", "–"]]
PICK = {(0, 1): 1, (1, 2): 2, (2, 3): 3, (3, 4): 4}   # (row, col) → 順番
fig, ax = plt.subplots(figsize=(7.4, 5.2))
board(ax, (-1.1, 6.2), (-1.5, 6.0))
ax.set_aspect("auto")
cw, ch = 1.0, 0.85
x0, y0 = 0.2, 0.4
for c, nm in enumerate(NAMES):
    ax.text(x0 + (c + 0.5) * cw, y0 + 5 * ch + 0.22, nm, fontsize=12.5,
            ha="center", va="bottom", color=LINE, weight="bold")
for r, nm in enumerate(NAMES):
    ax.text(x0 - 0.22, y0 + (4.5 - r) * ch, nm, fontsize=12.5, ha="right",
            va="center", color=LINE, weight="bold")
for r in range(5):
    for c in range(5):
        X = x0 + (c + 0.5) * cw
        Y = y0 + (4.5 - r) * ch
        n = PICK.get((r, c))
        if n:
            ax.add_patch(plt.Circle((X, Y), 0.30, fc="#eaf6ef", ec=GREEN,
                                    lw=2.0, zorder=3))
            ax.text(X + 0.42, Y + 0.30, f"{n}", fontsize=10.5, color=GREEN,
                    ha="center", va="center", zorder=6, weight="bold")
        ax.text(X, Y, TAB[r][c], fontsize=13, ha="center", va="center",
                color=INK, zorder=5)
for i in range(6):
    ax.plot([x0, x0 + 5 * cw], [y0 + i * ch, y0 + i * ch], color="#e0e4e8",
            lw=1.0, zorder=1)
    ax.plot([x0 + i * cw, x0 + i * cw], [y0, y0 + 5 * ch], color="#e0e4e8",
            lw=1.0, zorder=1)
for c in range(4):
    X = x0 + (c + 0.5) * cw
    ax.plot([X - 0.42, X + 0.42], [y0 + 5 * ch + 0.10, y0 + 5 * ch + 0.10],
            color=ACC, lw=2.2, zorder=8)
note(ax, 2.7, -0.55, "cross out a column when its vertex joins the tree",
     ACC, 11)
note(ax, 2.7, -1.10, "circled: $4 + 3 + 5 + 2 = 14$", GREEN, 12)
fig.tight_layout()
save(fig, "ahl-3-16-prim-matrix.svg")

# ══════════════ 8. Chinese postman ══════════════
fig, ax = plt.subplots(figsize=(7.4, 4.4))
board(ax, (-0.9, 7.0), (-1.1, 4.3))
draw_G(ax)
arc_edge(ax, P["A"], P["B"], color=ACC, lw=3.0, rad=-0.24, arrow=False)
for k in ("A", "B"):
    node(ax, P[k], k, color=ACC)
note(ax, 1.9, 3.85, "repeat $AB$", ACC, 11.5)
note(ax, 3.0, -0.72, "$44 + 4 = 48$", INK, 12.5)
fig.tight_layout()
save(fig, "ahl-3-16-cpp.svg")

# ══════════════ 9. TSP の完全グラフ ══════════════
TP = {"P": (0.4, 2.9), "Q": (3.4, 2.9), "R": (3.4, 0.4), "S": (0.4, 0.4)}
TW = [("P", "Q", 5), ("P", "R", 9), ("P", "S", 7), ("Q", "R", 6),
      ("Q", "S", 8), ("R", "S", 4)]


# 交差する 2 本の対角線のラベルが重ならないようにする。
TPOS = {("P", "R"): 0.30, ("Q", "S"): 0.30}


def draw_T(ax, pos, tw, hl=None, hlc=ACC, faint=PALE):
    for u, v, w in tw:
        on = hl is None or (u, v) in hl or (v, u) in hl
        col = hlc if (hl is not None and on) else (GREY if hl is None
                                                   else faint)
        edge(ax, pos[u], pos[v], color=col,
             lw=3.0 if (hl is not None and on) else 2.0)
        wlabel(ax, pos[u], pos[v], f"${w}$",
               color=hlc if (hl is not None and on) else GOLD, fs=10.5,
               t=TPOS.get((u, v), 0.5))
    for k, p in pos.items():
        node(ax, p, k)


fig, axs = plt.subplots(1, 3, figsize=(12.6, 4.2))
board(axs[0], (-0.8, 4.4), (-0.8, 3.7))
draw_T(axs[0], TP, TW)
axs[0].set_title("the complete graph", fontsize=12, color=INK, pad=6)

board(axs[1], (-0.8, 4.4), (-0.8, 3.7))
draw_T(axs[1], TP, TW, hl=[("P", "Q"), ("Q", "R"), ("R", "S"), ("S", "P")])
axs[1].set_title("nearest neighbour from $P$:  $22$", fontsize=12, color=ACC,
                 pad=6)

board(axs[2], (-0.8, 4.4), (-0.8, 3.7))
for u, v, w in TW:
    if "P" in (u, v):
        edge(axs[2], TP[u], TP[v], color=PALE, lw=1.6)
        wlabel(axs[2], TP[u], TP[v], f"${w}$", color="#c8cdd3", fs=10,
               t=TPOS.get((u, v), 0.5))
    else:
        on = (u, v) in [("Q", "R"), ("R", "S")] or (v, u) in [("Q", "R"),
                                                              ("R", "S")]
        edge(axs[2], TP[u], TP[v], color=GREEN if on else PALE,
             lw=3.0 if on else 1.6)
        wlabel(axs[2], TP[u], TP[v], f"${w}$",
               color=GREEN if on else "#c8cdd3", fs=10.5,
               t=TPOS.get((u, v), 0.5))
for k, p in TP.items():
    node(axs[2], p, k, color="#c8cdd3" if k == "P" else GREEN,
         tc="#c8cdd3" if k == "P" else GREEN)
axs[2].set_title("delete $P$:  MST $= 10$", fontsize=12, color=GREEN, pad=6)
fig.tight_layout()
save(fig, "ahl-3-16-tsp.svg")

# ══════════════ 10. table of least distances ══════════════
LP = {"L": (0.4, 0.5), "M": (2.2, 2.4), "N": (4.0, 0.5)}
fig, axs = plt.subplots(1, 2, figsize=(10.2, 3.8))
board(axs[0], (-0.8, 4.8), (-0.9, 3.2))
for u, v, w, col in (("L", "M", 5, GREEN), ("M", "N", 6, GREEN),
                     ("L", "N", 12, ACC)):
    edge(axs[0], LP[u], LP[v], color=col, lw=2.4)
    wlabel(axs[0], LP[u], LP[v], f"${w}$", color=col, fs=11.5)
for k, p in LP.items():
    node(axs[0], p, k)
note(axs[0], 2.2, -0.60, "$L \\to M \\to N = 11 < 12$", GREEN, 12)
axs[0].set_title("the real roads", fontsize=12, color=INK, pad=6)

board(axs[1], (0, 5.0), (0, 3.4))
axs[1].set_aspect("auto")
NM = ["L", "M", "N"]
TAB2 = [["–", "5", "11"], ["5", "–", "6"], ["11", "6", "–"]]
cw2, ch2 = 1.0, 0.80
x1, y1 = 0.9, 0.6
for c, nm in enumerate(NM):
    axs[1].text(x1 + (c + 0.5) * cw2, y1 + 3 * ch2 + 0.18, nm, fontsize=12.5,
                ha="center", va="bottom", color=LINE, weight="bold")
for r, nm in enumerate(NM):
    axs[1].text(x1 - 0.20, y1 + (2.5 - r) * ch2, nm, fontsize=12.5,
                ha="right", va="center", color=LINE, weight="bold")
for r in range(3):
    for c in range(3):
        col = ACC if (r, c) in ((0, 2), (2, 0)) else INK
        axs[1].text(x1 + (c + 0.5) * cw2, y1 + (2.5 - r) * ch2, TAB2[r][c],
                    fontsize=13, ha="center", va="center", color=col,
                    zorder=5)
for i in range(4):
    axs[1].plot([x1, x1 + 3 * cw2], [y1 + i * ch2, y1 + i * ch2],
                color="#e0e4e8", lw=1.0)
    axs[1].plot([x1 + i * cw2, x1 + i * cw2], [y1, y1 + 3 * ch2],
                color="#e0e4e8", lw=1.0)
axs[1].set_title("table of least distances", fontsize=12, color=ACC, pad=6)
fig.tight_layout()
save(fig, "ahl-3-16-least.svg")

# ══════════════ 演習3〜5 のグラフ ══════════════
XP = {"A": (0.4, 3.0), "B": (3.2, 3.0), "C": (0.4, 0.8), "D": (3.2, 0.8),
      "E": (5.6, 1.9)}
XG = [("A", "B", 7), ("A", "C", 3), ("B", "C", 5), ("B", "D", 4),
      ("C", "D", 6), ("C", "E", 8), ("D", "E", 2)]
fig, ax = plt.subplots(figsize=(6.8, 4.0))
board(ax, (-0.8, 6.6), (-0.6, 4.0))
XPOS = {("C", "E"): 0.80, ("D", "E"): 0.40}
for u, v, w in XG:
    edge(ax, XP[u], XP[v], color=GREY, lw=2.0)
    wlabel(ax, XP[u], XP[v], f"${w}$", color=GOLD, fs=10.5,
           t=XPOS.get((u, v), 0.5))
for k, p in XP.items():
    node(ax, p, k)
fig.tight_layout()
save(fig, "ahl-3-16-ex3.svg")

# ══════════════ 演習6・7 の完全グラフ ══════════════
YP = {"F": (0.4, 2.9), "H": (3.4, 2.9), "J": (3.4, 0.4), "K": (0.4, 0.4)}
YW = [("F", "H", 19), ("F", "J", 5), ("F", "K", 13), ("H", "J", 11),
      ("H", "K", 2), ("J", "K", 10)]
YPOS = {("F", "J"): 0.30, ("H", "K"): 0.30}
fig, ax = plt.subplots(figsize=(5.6, 4.2))
board(ax, (-0.8, 4.4), (-0.8, 3.7))
for u, v, w in YW:
    edge(ax, YP[u], YP[v], color=GREY, lw=2.0)
    wlabel(ax, YP[u], YP[v], f"${w}$", color=GOLD, fs=10.5,
           t=YPOS.get((u, v), 0.5))
for k, p in YP.items():
    node(ax, p, k)
fig.tight_layout()
save(fig, "ahl-3-16-ex6.svg")

# ══════════════ 演習9（odd vertex が 4 個） ══════════════
ZP = {"A": (0.4, 3.0), "B": (3.2, 3.0), "C": (1.8, 1.9), "D": (3.2, 0.5),
      "E": (0.4, 0.5)}
ZG = [("A", "B", 8), ("A", "C", 5), ("B", "C", 6), ("B", "D", 7),
      ("C", "D", 4), ("C", "E", 9), ("D", "E", 3), ("A", "E", 6)]
ZODD = ("A", "B", "D", "E")
fig, ax = plt.subplots(figsize=(6.4, 4.2))
board(ax, (-0.9, 4.5), (-0.9, 4.2))
for u, v, w in ZG:
    edge(ax, ZP[u], ZP[v], color=GREY, lw=2.0)
    wlabel(ax, ZP[u], ZP[v], f"${w}$", color=GOLD, fs=10.5)
for k, p in ZP.items():
    node(ax, p, k)
fig.tight_layout()
save(fig, "ahl-3-16-ex9.svg")

# ══════════════ 12. odd vertex が 4 個の Chinese postman ══════════════
QP = {"W": (0.4, 2.9), "X": (3.4, 2.9), "Y": (3.4, 0.4), "Z": (0.4, 0.4)}
QW = [("W", "X", 3), ("X", "Y", 4), ("Y", "Z", 3), ("W", "Z", 4),
      ("W", "Y", 5), ("X", "Z", 6)]
QPOS = {("W", "Y"): 0.30, ("X", "Z"): 0.30}
PAIRS = [([("W", "X"), ("Y", "Z")], "$WX + YZ = 3 + 3 = 6$", GREEN),
         ([("W", "Z"), ("X", "Y")], "$WZ + XY = 4 + 4 = 8$", GREY),
         ([("W", "Y"), ("X", "Z")], "$WY + XZ = 5 + 6 = 11$", GREY)]
fig, axs = plt.subplots(1, 3, figsize=(12.6, 4.4))
for ax, (hl, sub, col) in zip(axs, PAIRS):
    board(ax, (-0.8, 4.4), (-1.3, 3.7))
    for u, v, w in QW:
        on = (u, v) in hl or (v, u) in hl
        edge(ax, QP[u], QP[v], color=col if on else PALE,
             lw=3.2 if on else 1.8)
        wlabel(ax, QP[u], QP[v], f"${w}$",
               color=col if on else "#c8cdd3", fs=10.5,
               t=QPOS.get((u, v), 0.5))
    for k, p in QP.items():
        node(ax, p, k, color=ACC, tc=ACC)
    note(ax, 1.9, -0.95, sub, col, 11.5)
fig.text(0.5, 0.015, "all four vertices have odd degree", fontsize=11,
         ha="center", color=ACC)
fig.tight_layout(rect=(0, 0.04, 1, 1))
save(fig, "ahl-3-16-cpp4.svg")

print("figures written to", os.path.normpath(OUT))
