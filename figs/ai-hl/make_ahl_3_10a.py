"""AHL 3.10a（ベクトルの基本）の図を作る。ラベルは英語。
   出力先: ai-hl/03-geometry-and-trigonometry/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_3_10a.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
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


# ══════════ fig 1: 成分と、同じベクトル ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.9))

# ── (a) 成分の読み方
ax = axs[0]
P, Q = (-3.0, -1.0), (1.0, 2.0)
arrow(ax, P, Q, color=LINE, lw=3.0)
ax.plot([P[0], Q[0]], [P[1], P[1]], color=GREEN, lw=3.2, zorder=5,
        solid_capstyle="butt")
ax.plot([Q[0], Q[0]], [P[1], Q[1]], color=ACC, lw=3.2, zorder=5,
        solid_capstyle="butt")
ax.plot([P[0], Q[0]], [P[1], Q[1]], "o", color=INK, ms=7, zorder=8)
ax.text(P[0] - 0.25, P[1] - 0.25, "$A$", fontsize=13, color=INK, ha="right",
        va="top")
ax.text(Q[0] + 0.1, Q[1] + 0.25, "$B$", fontsize=13, color=INK, ha="left",
        va="bottom")
ax.text((P[0] + Q[0]) / 2, P[1] - 0.30, "$4$ across", fontsize=12,
        color=GREEN, ha="center", va="top")
ax.text(Q[0] + 0.18, (P[1] + Q[1]) / 2, "$3$ up", fontsize=12, color=ACC,
        ha="left", va="center")
ax.text(-2.3, 1.5, "$\\overrightarrow{AB} = \\binom{4}{3} = 4\\mathbf{i} + 3\\mathbf{j}$",
        fontsize=13, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
grid(ax, (-4.6, 3.6), (-2.6, 3.4))
ax.set_title("(a)  the components are 'across' and 'up'", fontsize=12.5,
             color=INK, pad=6)

# ── (b) 同じベクトルは、どこに置いても同じ
ax = axs[1]
STARTS = [(-4.5, -2.0), (-1.5, 0.5), (0.5, -2.5), (-5.0, 1.5)]
COLS = [LINE, GREEN, GOLD, ACC]
for (sx, sy), c in zip(STARTS, COLS):
    arrow(ax, (sx, sy), (sx + 4, sy + 3), color=c, lw=2.6)
ax.text(0.4, -3.85, "only the 'across' and 'up' matter,\n"
                    "not where the arrow starts",
        fontsize=11.5, color=GREY, ha="center", va="center", bbox=BOX,
        zorder=9)
grid(ax, (-5.8, 5.8), (-4.8, 4.8))
ax.set_title("(b)  where you draw it does not matter\n"
             "all four arrows are the SAME vector $\\binom{4}{3}$",
             fontsize=12.5, color=INK, pad=6)

fig.tight_layout(w_pad=1.8)
save(fig, "ahl-3-10a-components.svg")


# ══════════ fig 2: 足し算と引き算 ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.9))

A = np.array([3.0, 1.0])
B = np.array([1.0, 3.0])
O = np.array([0.0, 0.0])

# ── (a) 三角形の法則
ax = axs[0]
arrow(ax, O, A, color=LINE, lw=3.0)
arrow(ax, A, A + B, color=GREEN, lw=3.0)
arrow(ax, O, A + B, color=ACC, lw=3.4)
arrow(ax, O, B, color=GREEN, lw=2.0, ls=":", z=4)
arrow(ax, B, A + B, color=LINE, lw=2.0, ls=":", z=4)
ax.text(1.5, 0.25, "$\\mathbf{a}$", fontsize=14, color=LINE, ha="center",
        va="top")
ax.text(4.0, 2.4, "$\\mathbf{b}$", fontsize=14, color=GREEN, ha="left",
        va="center")
ax.text(2.45, 2.75, "$\\mathbf{a}+\\mathbf{b}$", fontsize=14, color=ACC,
        ha="right", va="center", bbox=BOX, zorder=9)
ax.text(2.0, -1.35, "nose to tail: $\\mathbf{a}$ then $\\mathbf{b}$\n"
                    "$\\binom{3}{1} + \\binom{1}{3} = \\binom{4}{4}$",
        fontsize=12, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
grid(ax, (-1.4, 5.4), (-2.6, 4.8))
ax.set_title("(a)  adding: join them nose to tail", fontsize=12.5, color=INK,
             pad=6)

# ── (b) 引き算
ax = axs[1]
arrow(ax, O, A, color=LINE, lw=3.0)
arrow(ax, O, B, color=GREEN, lw=3.0)
OFF = np.array([0.28, 0.28])
arrow(ax, B, A, color=ACC, lw=3.4)
arrow(ax, A + OFF, B + OFF, color=GOLD, lw=2.4, ls="--")
ax.text(1.6, 0.25, "$\\mathbf{a}$", fontsize=14, color=LINE, ha="center",
        va="top")
ax.text(0.35, 1.9, "$\\mathbf{b}$", fontsize=14, color=GREEN, ha="right",
        va="center")
ax.text(3.15, 0.95, "$\\mathbf{a}-\\mathbf{b}$", fontsize=13, color=ACC,
        ha="left", va="top")
ax.text(1.4, 3.5, "$\\mathbf{b}-\\mathbf{a}$", fontsize=13, color=GOLD,
        ha="left", va="bottom")
ax.text(2.0, -1.35, "$\\mathbf{a}-\\mathbf{b}$ points FROM the tip of "
                    "$\\mathbf{b}$\nTO the tip of $\\mathbf{a}$; "
                    "$\\mathbf{b}-\\mathbf{a}$ is the other way\n"
                    "(drawn slightly to the side, so both can be seen)",
        fontsize=11.5, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
grid(ax, (-1.4, 5.4), (-2.6, 4.8))
ax.set_title("(b)  subtracting: same length, opposite way round",
             fontsize=12.5, color=INK, pad=6)

fig.tight_layout(w_pad=1.8)
save(fig, "ahl-3-10a-addsub.svg")


# ══════════ fig 3: スカラー倍と平行 ══════════
fig, ax = plt.subplots(figsize=(10.6, 4.6))

V = np.array([2.0, 1.0])
ROWS = [(1.0, "$\\mathbf{a}$", LINE, 0.0, "the vector itself"),
        (2.0, "$2\\mathbf{a}$", GREEN, -1.5,
         "$k = 2$: same direction, twice as long"),
        (0.5, "$0.5\\mathbf{a}$", GOLD, -3.0,
         "$0 < k < 1$: same direction, shorter"),
        (-1.5, "$-1.5\\mathbf{a}$", ACC, -4.5,
         "$k < 0$: OPPOSITE direction")]
for k, lab, col, dy, note in ROWS:
    s0 = np.array([0.0, dy])
    arrow(ax, s0, s0 + k * V, color=col, lw=3.0)
    ax.plot([s0[0]], [s0[1]], "o", color=col, ms=6, zorder=8)
    ax.text(-0.35, dy, lab, fontsize=14, color=col, ha="right", va="center")
    ax.text(5.2, dy, note, fontsize=11.5, color=col, ha="left", va="center")

ax.axvline(0, color=GREY, lw=1.0, ls=":", zorder=1)
ax.text(2.0, 1.55, "every $k\\mathbf{a}$ is parallel to $\\mathbf{a}$   "
                   "(for $\\mathbf{a} \\neq \\mathbf{0}$ and $k \\neq 0$)",
        fontsize=12.5, color=INK, ha="center", va="center", bbox=BOX,
        zorder=9)
ax.text(0.15, -5.6, "all four start from the dotted line", fontsize=10.5,
        color=GREY, ha="left", va="center")
ax.set_xlim(-4.6, 13.2)
ax.set_ylim(-6.2, 2.4)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("Multiplying by a scalar: the direction is kept, or reversed",
             fontsize=13, color=INK, pad=8)

fig.tight_layout()
save(fig, "ahl-3-10a-scalar.svg")

print("figures written to", os.path.normpath(OUT))
