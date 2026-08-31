"""AHL 4.19 の図を作る。ラベルはすべて英語。
   出力先: ai-hl/04-statistics-and-probability/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_4_19.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
from _graph import (INK, GRID, LINE, ACC, GREEN, GREY, GOLD, BOX, R,
                    board, node, arc_edge, note)
from _matrix import matrix as mtx

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "04-statistics-and-probability", "img")
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True)
    plt.close(fig)


def selfloop(ax, p, text, angle=90, size=0.40, color=GREY, tcolor=GOLD,
             fs=11):
    """自己ループと、その確率のラベル。"""
    th = np.radians(angle)
    c = (p[0] + size * 1.15 * np.cos(th), p[1] + size * 1.15 * np.sin(th))
    ax.add_patch(Circle(c, size, fc="none", ec=color, lw=2.0, zorder=3))
    ax.text(c[0] + size * 1.5 * np.cos(th), c[1] + size * 1.5 * np.sin(th),
            text, fontsize=fs, ha="center", va="center", color=tcolor,
            zorder=12, bbox=BOX)


def plabel(ax, p, q, text, rad=0.0, margin=0.24, color=GOLD, fs=11):
    """arc3(rad) で描いた矢印の、ふくらんだ側にラベルを置く。"""
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = np.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    off = -(abs(rad) * L / 2 + margin) * (1 if rad >= 0 else -1)
    ax.text(mx + nx * off, my + ny * off, text, fontsize=fs, ha="center",
            va="center", color=color, zorder=12, bbox=BOX)


def labelled_matrix(ax, cx, cy, rows, cols_hdr, rows_hdr, cw=0.86, ch=0.62,
                    fs=13, cell_color=None):
    centres, (x0, y0, w, h) = mtx(ax, cx, cy, rows, cw=cw, ch=ch, fs=fs,
                                  color=INK, cell_color=cell_color)
    for c, nm in enumerate(cols_hdr):
        X = x0 + (c + 0.5) * cw
        ax.text(X, y0 + h + 0.26, nm, fontsize=11, ha="center", va="bottom",
                color=LINE, weight="bold")
    for r, nm in enumerate(rows_hdr):
        Y = y0 + h - (r + 0.5) * ch
        ax.text(x0 - 0.30, Y, nm, fontsize=11, ha="right", va="center",
                color=LINE, weight="bold")
    return centres, (x0, y0, w, h)


# ── この項目でずっと使う 2 状態のモデル ────────────────────────
PA, PB = (0.6, 1.6), (3.6, 1.6)
T2 = [["$0.8$", "$0.3$"], ["$0.2$", "$0.7$"]]

# ══════════════ 1. transition diagram ══════════════
fig, ax = plt.subplots(figsize=(7.2, 4.0))
board(ax, (-0.7, 4.9), (-0.9, 3.3))
arc_edge(ax, PA, PB, rad=0.28)
arc_edge(ax, PB, PA, rad=0.28)
plabel(ax, PA, PB, "$0.2$", rad=0.28)
plabel(ax, PB, PA, "$0.3$", rad=0.28)
selfloop(ax, PA, "$0.8$", angle=180)
selfloop(ax, PB, "$0.7$", angle=0)
node(ax, PA, "A")
node(ax, PB, "B")
note(ax, 2.1, -0.55, "the four numbers are probabilities", GREY, 11)
fig.tight_layout()
save(fig, "ahl-4-19-diagram.svg")

# ══════════════ 2. diagram → transition matrix ══════════════
fig, axs = plt.subplots(1, 2, figsize=(10.6, 4.2))
board(axs[0], (-0.7, 4.9), (-0.6, 3.3))
arc_edge(axs[0], PA, PB, rad=0.28)
arc_edge(axs[0], PB, PA, rad=0.28)
plabel(axs[0], PA, PB, "$0.2$", rad=0.28)
plabel(axs[0], PB, PA, "$0.3$", rad=0.28)
selfloop(axs[0], PA, "$0.8$", angle=180)
selfloop(axs[0], PB, "$0.7$", angle=0)
node(axs[0], PA, "A")
node(axs[0], PB, "B")
axs[0].set_title("transition diagram", fontsize=12.5, color=LINE, pad=6)

board(axs[1], (0, 5.2), (0, 4.2))
labelled_matrix(axs[1], 2.5, 2.0, T2, ["from A", "from B"], ["to A", "to B"])
axs[1].set_title("transition matrix $T$", fontsize=12.5, color=ACC, pad=6)
axs[1].text(2.5, 0.55, "each column adds up to $1$", fontsize=11.5,
            ha="center", va="center", color=GOLD)
fig.tight_layout()
save(fig, "ahl-4-19-matrix.svg")

# ══════════════ 3. s0 → s1 → s2 ══════════════
fig, ax = plt.subplots(figsize=(9.4, 2.6))
board(ax, (0, 9.4), (0.2, 2.4))
ax.set_aspect("auto")
STEPS = [("$s_0$", [["$1$"], ["$0$"]]), ("$s_1$", [["$0.8$"], ["$0.2$"]]),
         ("$s_2$", [["$0.7$"], ["$0.3$"]]), ("$s_3$", [["$0.65$"], ["$0.35$"]])]
xs = [1.1, 3.4, 5.7, 8.0]
for i, ((nm, rows), x) in enumerate(zip(STEPS, xs)):
    mtx(ax, x, 1.35, rows, cw=0.90, ch=0.52, fs=13,
        color=ACC if i else INK)
    ax.text(x, 2.15, nm, fontsize=13, ha="center", va="center",
            color=ACC if i else INK)
    if i:
        ax.annotate("", xy=(x - 0.72, 1.35), xytext=(xs[i - 1] + 0.72, 1.35),
                    arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.8))
        ax.text((xs[i - 1] + x) / 2, 1.72, r"$\times T$", fontsize=12,
                ha="center", va="center", color=GREY)
fig.tight_layout()
save(fig, "ahl-4-19-steps.svg")

# ══════════════ 4. 収束のようす ══════════════
Tm = np.array([[0.8, 0.3], [0.2, 0.7]])
fig, ax = plt.subplots(figsize=(7.6, 4.4))
ns = np.arange(0, 13)
for start, col, lab in (([1.0, 0.0], ACC, "starting at $A$"),
                        ([0.0, 1.0], GREEN, "starting at $B$"),
                        ([0.5, 0.5], LINE, "starting half and half")):
    v = np.array(start)
    ys = []
    for _ in ns:
        ys.append(v[0])
        v = Tm @ v
    ax.plot(ns, ys, "o-", color=col, lw=2.0, ms=4.5, label=lab, zorder=5)
ax.axhline(0.6, color=GOLD, lw=1.8, ls=(0, (5, 4)), zorder=3)
ax.text(0.15, 0.645, "the steady state $0.6$", fontsize=11.5, color=GOLD,
        ha="left", va="center")
ax.set_xlim(-0.4, 13.4)
ax.set_ylim(-0.03, 1.05)
ax.set_xlabel("number of steps $n$", fontsize=11.5)
ax.set_ylabel("proportion at $A$", fontsize=11.5)
for y in np.arange(0, 1.01, 0.2):
    ax.axhline(y, color=GRID, lw=0.7, zorder=0)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.spines["left"].set_color(GREY)
ax.spines["bottom"].set_color(GREY)
ax.legend(frameon=False, fontsize=10.5, loc="center right")
fig.tight_layout()
save(fig, "ahl-4-19-converge.svg")

# ══════════════ 5. steady state：2 つの出し方 ══════════════
fig, axs = plt.subplots(1, 2, figsize=(10.6, 3.4))
for ax in axs:
    board(ax, (0, 5.2), (0, 3.2))
    ax.set_aspect("auto")
axs[0].text(2.6, 2.55, "keep multiplying", fontsize=12.5, ha="center",
            color=ACC)
axs[0].text(2.6, 1.55, r"$s_1,\ s_2,\ s_3,\ \ldots$" "\n"
                       r"until the numbers stop changing",
            fontsize=12, ha="center", va="center", color=INK)
axs[0].text(2.6, 0.45, "quick on the GDC, but only approximate",
            fontsize=10.5, ha="center", color=GREY)
axs[1].text(2.6, 2.55, "solve the equations", fontsize=12.5, ha="center",
            color=GREEN)
axs[1].text(2.6, 1.55, r"$Ts = s$   together with   $a + b = 1$",
            fontsize=12, ha="center", va="center", color=INK)
axs[1].text(2.6, 0.45, "slower, but gives the exact answer",
            fontsize=10.5, ha="center", color=GREY)
fig.tight_layout()
save(fig, "ahl-4-19-steady.svg")

# ══════════════ 6. 例題4：3 状態 ══════════════
Q = {"A": (0.5, 2.9), "B": (4.1, 2.9), "C": (2.3, 0.3)}
ARCS = [("A", "B", "$0.1$"), ("B", "A", "$0.1$"), ("A", "C", "$0.3$"),
        ("C", "A", "$0.1$"), ("B", "C", "$0.3$"), ("C", "B", "$0.2$")]
fig, ax = plt.subplots(figsize=(7.0, 4.6))
board(ax, (-1.3, 5.9), (-1.3, 4.4))
for u, v, w in ARCS:
    arc_edge(ax, Q[u], Q[v], rad=0.22)
    plabel(ax, Q[u], Q[v], w, rad=0.22)
selfloop(ax, Q["A"], "$0.6$", angle=135)
selfloop(ax, Q["B"], "$0.6$", angle=45)
selfloop(ax, Q["C"], "$0.7$", angle=-90)
for k, p in Q.items():
    node(ax, p, k)
fig.tight_layout()
save(fig, "ahl-4-19-we4.svg")

# ══════════════ 演習2（2 状態） ══════════════
EA, EB = (0.6, 1.6), (3.6, 1.6)
fig, ax = plt.subplots(figsize=(6.8, 3.8))
board(ax, (-0.7, 4.9), (-0.5, 3.3))
arc_edge(ax, EA, EB, rad=0.28)
arc_edge(ax, EB, EA, rad=0.28)
plabel(ax, EA, EB, "$0.1$", rad=0.28)
plabel(ax, EB, EA, "$0.4$", rad=0.28)
selfloop(ax, EA, "$0.9$", angle=180)
selfloop(ax, EB, "$0.6$", angle=0)
node(ax, EA, "P")
node(ax, EB, "Q")
fig.tight_layout()
save(fig, "ahl-4-19-ex2.svg")

# ══════════════ 演習5（3 状態） ══════════════
Z = {"X": (0.5, 2.9), "Y": (4.1, 2.9), "Z": (2.3, 0.3)}
ZARCS = [("X", "Y", "$0.4$"), ("Y", "X", "$0.3$"), ("X", "Z", "$0.1$"),
         ("Z", "X", "$0.2$"), ("Y", "Z", "$0.1$"), ("Z", "Y", "$0.2$")]
fig, ax = plt.subplots(figsize=(7.0, 4.6))
board(ax, (-1.3, 5.9), (-1.3, 4.4))
for u, v, w in ZARCS:
    arc_edge(ax, Z[u], Z[v], rad=0.22)
    plabel(ax, Z[u], Z[v], w, rad=0.22)
selfloop(ax, Z["X"], "$0.5$", angle=135)
selfloop(ax, Z["Y"], "$0.6$", angle=45)
selfloop(ax, Z["Z"], "$0.6$", angle=-90)
for k, p in Z.items():
    node(ax, p, k)
fig.tight_layout()
save(fig, "ahl-4-19-ex5.svg")

print("figures written to", os.path.normpath(OUT))
