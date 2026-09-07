"""AHL 3.10b（大きさ・位置ベクトル・単位ベクトル）の図を作る。ラベルは英語。
   出力先: ai-hl/03-geometry-and-trigonometry/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_3_10b.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
from _graph import INK, GRID, LINE, ACC, GREEN, GREY, GOLD, BOX, FILL

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "03-geometry-and-trigonometry", "img")
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True)
    plt.close(fig)
    print("wrote", name)


def grid(ax, xlim, ylim, step=1):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.set_xticks(np.arange(int(np.ceil(xlim[0])), int(xlim[1]) + 1, step))
    ax.set_yticks(np.arange(int(np.ceil(ylim[0])), int(ylim[1]) + 1, step))
    ax.grid(True, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.axhline(0, color=GREY, lw=1.2)
    ax.axvline(0, color=GREY, lw=1.2)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    for sp in ax.spines.values():
        sp.set_visible(False)


def arrow(ax, p, q, color=LINE, lw=2.6, z=6, ls="-"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=18,
                                 lw=lw, color=color, zorder=z,
                                 linestyle=ls, shrinkA=0, shrinkB=0))


# ══════════ fig 1: 大きさは三平方の定理 ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 5.0))

# ── (a) 2 次元
ax = axs[0]
V = (3.0, 4.0)
ax.plot([0, V[0]], [0, 0], color=GREEN, lw=3.2, zorder=5, solid_capstyle="butt")
ax.plot([V[0], V[0]], [0, V[1]], color=ACC, lw=3.2, zorder=5,
        solid_capstyle="butt")
arrow(ax, (0, 0), V, color=LINE, lw=3.2)
ax.plot([0, V[0]], [0, V[1]], "o", color=INK, ms=6, zorder=8)
ax.text(V[0] / 2, -0.28, "$3$", fontsize=13, color=GREEN, ha="center", va="top")
ax.text(V[0] + 0.18, V[1] / 2, "$4$", fontsize=13, color=ACC, ha="left",
        va="center")
ax.text(0.75, 2.85, "$|\\mathbf{v}|$", fontsize=15, color=LINE,
        ha="center", va="center")
ax.text(1.6, -1.55, "$|\\mathbf{v}| = \\sqrt{3^2+4^2} = 5$",
        fontsize=13.5, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
grid(ax, (-1.4, 4.8), (-2.6, 5.0))
ax.set_title("(a)  in 2D it is just Pythagoras", fontsize=12.5, color=INK,
             pad=6)

# ── (b) 3 次元（直方体の対角線）
ax = axs[1]
ex = np.array([1.0, 0.0])            # x 方向（右）
ey = np.array([0.52, 0.40])          # y 方向（奥）
ez = np.array([0.0, 1.0])            # z 方向（上）
a, b, c = 2.0, 3.0, 6.0              # v = (2, 3, 6)


def P(i, j, k):
    return i * a * ex + j * b * ey + k * c * ez


corners = {(i, j, k): P(i, j, k) for i in (0, 1) for j in (0, 1)
           for k in (0, 1)}
edges = [((0, 0, 0), (1, 0, 0)), ((0, 0, 0), (0, 1, 0)), ((0, 0, 0), (0, 0, 1)),
         ((1, 0, 0), (1, 1, 0)), ((1, 0, 0), (1, 0, 1)),
         ((0, 1, 0), (1, 1, 0)), ((0, 1, 0), (0, 1, 1)),
         ((0, 0, 1), (1, 0, 1)), ((0, 0, 1), (0, 1, 1)),
         ((1, 1, 0), (1, 1, 1)), ((1, 0, 1), (1, 1, 1)),
         ((0, 1, 1), (1, 1, 1))]
for u, w in edges:
    p, q = corners[u], corners[w]
    ax.plot([p[0], q[0]], [p[1], q[1]], color=GREY, lw=1.4, zorder=3)
# 床の対角線
p0, p1 = corners[(0, 0, 0)], corners[(1, 1, 0)]
ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=GREEN, lw=3.0, zorder=5,
        linestyle="--")
# 立体の対角線
p2 = corners[(1, 1, 1)]
arrow(ax, tuple(p0), tuple(p2), color=LINE, lw=3.2)
# 高さ
ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=ACC, lw=3.0, zorder=5)
ax.text(1.0, -0.30, "$2$", fontsize=12.5, color=GREY, ha="center", va="top")
ax.text(2.95, 0.42, "$3$", fontsize=12.5, color=GREY, ha="left",
        va="top")
ax.text(p1[0] + 0.28, (p1[1] + p2[1]) / 2, "$6$", fontsize=12.5, color=ACC,
        ha="left", va="center")
ax.text(3.9, 0.55, "step 1:\nthe floor", fontsize=11, color=GREEN,
        ha="left", va="center")
ax.text(-3.0, 5.2, "step 2:\nfloor, then height", fontsize=11, color=LINE,
        ha="left", va="center")
ax.text(1.6, -1.95, "$|\\mathbf{v}| = "
                     "\\sqrt{\\left(\\sqrt{2^2+3^2}\\right)^2 + 6^2} = "
                     "\\sqrt{2^2+3^2+6^2} = 7$",
        fontsize=13, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
ax.set_xlim(-3.2, 6.4)
ax.set_ylim(-3.0, 7.6)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("(b)  in 3D you use Pythagoras twice\n"
             "the middle square root is never worked out",
             fontsize=12.5, color=INK, pad=6)

fig.tight_layout(w_pad=1.8)
save(fig, "ahl-3-10b-magnitude.svg")


# ══════════ fig 2: 位置ベクトルと AB ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 5.0))

A = np.array([1.0, 4.0])
B = np.array([7.0, -4.0])
O = np.array([0.0, 0.0])

# ── (a) AB = b - a
ax = axs[0]
arrow(ax, O, A, color=GREEN, lw=3.0)
arrow(ax, O, B, color=GOLD, lw=3.0)
arrow(ax, A, B, color=ACC, lw=3.4)
ax.plot([O[0], A[0], B[0]], [O[1], A[1], B[1]], "o", color=INK, ms=7, zorder=8)
ax.text(-0.3, -0.35, "$O$", fontsize=13, color=INK, ha="right", va="top")
ax.text(A[0] - 0.2, A[1] + 0.35, "$A$", fontsize=13, color=INK, ha="right",
        va="bottom")
ax.text(B[0] + 0.3, B[1] - 0.2, "$B$", fontsize=13, color=INK, ha="left",
        va="top")
ax.text(0.05, 2.5, "$\\mathbf{a}$", fontsize=14, color=GREEN, ha="right",
        va="center")
ax.text(4.2, -1.5, "$\\mathbf{b}$", fontsize=14, color=GOLD, ha="left",
        va="bottom")
ax.text(4.6, 1.1, "$\\overrightarrow{AB}$", fontsize=14, color=ACC,
        ha="left", va="center")
ax.text(3.0, -6.6, "go back along $\\mathbf{a}$, then out along $\\mathbf{b}$:\n"
                   "$\\overrightarrow{AB} = \\mathbf{b} - \\mathbf{a}$   "
                   "(finish $-$ start)",
        fontsize=12, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
grid(ax, (-2.0, 9.4), (-8.4, 6.2))
ax.set_title("(a)  position vectors, and the vector from $A$ to $B$",
             fontsize=12.5, color=INK, pad=6)

# ── (b) |AB| は 2 点間の距離
ax = axs[1]
arrow(ax, A, B, color=ACC, lw=3.4)
ax.plot([A[0], B[0]], [A[1], A[1]], color=GREEN, lw=3.0, zorder=5,
        solid_capstyle="butt")
ax.plot([B[0], B[0]], [A[1], B[1]], color=GOLD, lw=3.0, zorder=5,
        solid_capstyle="butt")
ax.plot([A[0], B[0]], [A[1], B[1]], "o", color=INK, ms=7, zorder=8)
ax.text(A[0] - 0.2, A[1] + 0.35, "$A$", fontsize=13, color=INK, ha="right",
        va="bottom")
ax.text(B[0] + 0.3, B[1] - 0.2, "$B$", fontsize=13, color=INK, ha="left",
        va="top")
ax.text((A[0] + B[0]) / 2, A[1] + 0.3, "$6$ across", fontsize=12, color=GREEN,
        ha="center", va="bottom")
ax.text(B[0] + 0.3, -2.2, "$8$ down", fontsize=12, color=GOLD,
        ha="left", va="center")
ax.text(3.0, -6.6, "$\\overrightarrow{AB} = \\binom{6}{-8}$,   "
                   "$|\\overrightarrow{AB}| = "
                   "\\sqrt{6^2+(-8)^2} = 10$\n"
                   "this is the distance from $A$ to $B$",
        fontsize=12, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
grid(ax, (-2.0, 9.4), (-8.4, 6.2))
ax.set_title("(b)  the length of that vector is the distance",
             fontsize=12.5, color=INK, pad=6)

fig.tight_layout(w_pad=1.8)
save(fig, "ahl-3-10b-position.svg")


# ══════════ fig 3: 単位ベクトルと、長さを付け替える ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.9))

W = np.array([3.0, 4.0])
U = W / 5.0

# ── (a) v / |v|
ax = axs[0]
ax.add_patch(Circle((0, 0), 1.0, fill=False, color=GREY, lw=1.4, ls="--",
                    zorder=3))
arrow(ax, O, W, color=LINE, lw=2.8)
arrow(ax, O, U, color=ACC, lw=3.4, z=7)
ax.text(2.5, 1.85, "$\\mathbf{v} = \\binom{3}{4}$,   "
                   "$|\\mathbf{v}| = 5$",
        fontsize=12.5, color=LINE, ha="left", va="center", bbox=BOX, zorder=9)
ax.text(0.88, 0.48, "$\\hat{\\mathbf{v}}$", fontsize=14, color=ACC,
        ha="left", va="top")
ax.text(1.4, -1.35, "$\\dfrac{\\mathbf{v}}{|\\mathbf{v}|} = "
                    "\\dfrac{1}{5}\\binom{3}{4} = \\binom{0.6}{0.8}$\n"
                    "same direction, length exactly $1$",
        fontsize=12, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
grid(ax, (-1.6, 5.0), (-2.6, 5.0))
ax.set_title("(a)  dividing by the length lands you on the unit circle",
             fontsize=12.5, color=INK, pad=6)

# ── (b) speed x unit vector
ax = axs[1]
OFFB = np.array([-0.40, 0.30])
arrow(ax, tuple(OFFB), tuple(W + OFFB), color=GREY, lw=2.2, ls=":", z=8)
arrow(ax, O, U, color=ACC, lw=3.0, z=7)
arrow(ax, O, 7 * U, color=GREEN, lw=3.2, z=6)
ax.text(0.55, 3.75, "$3\\mathbf{i}+4\\mathbf{j}$\n(length $5$, not $7$)",
        fontsize=11, color=GREY, ha="right", va="center")
ax.text(0.88, 0.48, "$\\hat{\\mathbf{v}}$", fontsize=13, color=ACC,
        ha="left", va="top")
ax.text(4.45, 5.95, "$7\\hat{\\mathbf{v}}$", fontsize=14, color=GREEN,
        ha="left", va="center")
ax.text(2.6, -1.6, "speed $7$ in the direction $3\\mathbf{i}+4\\mathbf{j}$:\n"
                   "$7 \\times \\binom{0.6}{0.8} = \\binom{4.2}{5.6}$",
        fontsize=12, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
grid(ax, (-1.6, 7.0), (-2.8, 6.8))
ax.set_title("(b)  put the length you want back on\n"
             "$3\\mathbf{i}+4\\mathbf{j}$ has length $5$, not $7$",
             fontsize=12.5, color=INK, pad=6)

fig.tight_layout(w_pad=1.8)
save(fig, "ahl-3-10b-unit.svg")

print("figures written to", os.path.normpath(OUT))
