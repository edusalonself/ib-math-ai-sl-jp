"""AHL 3.11（直線のベクトル方程式）の図を作る。ラベルは英語。
   出力先: ai-hl/03-geometry-and-trigonometry/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_3_11.py
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
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=17,
                                 lw=lw, color=color, zorder=z,
                                 linestyle=ls, shrinkA=0, shrinkB=0))


def full_line(ax, a, b, lo, hi, color=GREY, lw=1.8, ls="-", z=2):
    a, b = np.array(a, float), np.array(b, float)
    p, q = a + lo * b, a + hi * b
    ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw, ls=ls, zorder=z)


# ══════════ fig 1: r = a + λb と、書き方が 1 通りでないこと ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 5.2))

A0 = np.array([1.0, 2.0])
B0 = np.array([3.0, -1.0])

# ── (a) a で乗って、b で進む
ax = axs[0]
full_line(ax, A0, B0, -1.6, 3.0, color=GREY, lw=1.8, ls="--")
arrow(ax, (0, 0), tuple(A0), color=GREEN, lw=3.0)
arrow(ax, tuple(A0), tuple(A0 + B0), color=ACC, lw=3.0)
arrow(ax, tuple(A0 + B0), tuple(A0 + 2 * B0), color=ACC, lw=2.2, ls=":")
for lam, lab, dx, dy, ha, va in [
        (-1, "$\\lambda = -1$", -0.25, 0.30, "right", "bottom"),
        (0, "$\\lambda = 0$", -0.25, 0.30, "right", "bottom"),
        (1, "$\\lambda = 1$", 0.25, -0.30, "left", "top"),
        (2, "$\\lambda = 2$", 0.25, -0.30, "left", "top")]:
    P = A0 + lam * B0
    ax.plot([P[0]], [P[1]], "o", color=INK, ms=7, zorder=8)
    ax.text(P[0] + dx, P[1] + dy, lab, fontsize=10.5, color=INK,
            ha=ha, va=va)
ax.text(0.15, 1.15, "$\\mathbf{a}$", fontsize=14, color=GREEN, ha="right",
        va="center")
ax.text(2.9, 1.75, "$\\mathbf{b}$", fontsize=14, color=ACC, ha="left",
        va="bottom")
ax.text(3.6, -3.4, "$\\mathbf{r} = \\binom{1}{2} + \\lambda\\binom{3}{-1}$\n"
                   "get on at $\\mathbf{a}$, then walk $\\lambda$ steps of "
                   "$\\mathbf{b}$",
        fontsize=12, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
grid(ax, (-4.4, 8.6), (-4.6, 5.0))
ax.set_title("(a)  one point on the line, and one direction", fontsize=12.5,
             color=INK, pad=6)

# ── (b) 同じ直線を、別の a と別の b で
ax = axs[1]
full_line(ax, A0, B0, -1.6, 3.0, color=GREY, lw=1.8, ls="--")
A1 = np.array([7.0, 0.0])
B1 = np.array([-6.0, 2.0])
arrow(ax, (0, 0), tuple(A1), color=GOLD, lw=3.0)
arrow(ax, tuple(A1), tuple(A1 + B1), color=LINE, lw=3.0)
ax.plot([A1[0], (A1 + B1)[0]], [A1[1], (A1 + B1)[1]], "o", color=INK, ms=7,
        zorder=8)
ax.text(A1[0] + 0.2, A1[1] - 0.3, "$\\mu = 0$", fontsize=10.5, color=INK,
        ha="left", va="top")
ax.text((A1 + B1)[0] - 0.25, (A1 + B1)[1] + 0.3, "$\\mu = 1$", fontsize=10.5,
        color=INK, ha="right", va="bottom")
ax.text(3.6, -0.55, "new $\\mathbf{a}$", fontsize=12, color=GOLD, ha="center",
        va="top")
ax.text(4.0, 1.35, "new $\\mathbf{b}$", fontsize=12, color=LINE, ha="center",
        va="bottom")
ax.text(3.6, -3.4, "$\\mathbf{r} = \\binom{7}{0} + \\mu\\binom{-6}{2}$\n"
                   "different $\\mathbf{a}$, different $\\mathbf{b}$, "
                   "SAME line",
        fontsize=12, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
grid(ax, (-4.4, 8.6), (-4.6, 5.0))
ax.set_title("(b)  the equation of a line is not unique", fontsize=12.5,
             color=INK, pad=6)

fig.tight_layout(w_pad=1.8)
save(fig, "ahl-3-11-idea.svg")


# ══════════ fig 2: 2 点から作る／線上かどうかを調べる ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 5.0))

PA = np.array([2.0, -1.0])
PB = np.array([6.0, 1.0])
DIR = PB - PA                      # (4, 2)

# ── (a) 2 点から
ax = axs[0]
full_line(ax, PA, DIR, -1.2, 2.6, color=GREY, lw=1.8, ls="--")
arrow(ax, tuple(PA), tuple(PB), color=ACC, lw=3.2)
for P, lab, dy in [(PA, "$A$  $(\\lambda = 0)$", 0.35),
                   (PB, "$B$  $(\\lambda = 1)$", 0.35),
                   (PA + 2 * DIR, "$C$  $(\\lambda = 2)$", 0.35)]:
    ax.plot([P[0]], [P[1]], "o", color=INK, ms=7, zorder=8)
    ax.text(P[0] - 0.2, P[1] + dy, lab, fontsize=11, color=INK, ha="right",
            va="bottom")
ax.text(4.0, -0.55, "$\\overrightarrow{AB} = \\binom{4}{2}$", fontsize=12.5,
        color=ACC, ha="center", va="top")
ax.text(5.4, -3.6, "$\\mathbf{r} = \\binom{2}{-1} + "
                   "\\lambda\\binom{4}{2}$\n"
                   "$\\mathbf{a}$ is either point; "
                   "$\\mathbf{b}$ is $\\overrightarrow{AB}$",
        fontsize=12, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
grid(ax, (-1.6, 12.4), (-4.8, 5.0))
ax.set_title("(a)  through two points", fontsize=12.5, color=INK, pad=6)

# ── (b) 線上かどうか
ax = axs[1]
full_line(ax, PA, DIR, -1.2, 2.6, color=GREY, lw=1.8, ls="--")
ONP = PA + 1.5 * DIR               # (8, 2)  線上
OFFP = np.array([8.0, 3.0])        # 線から外れている
ax.plot([ONP[0]], [ONP[1]], "o", color=GREEN, ms=9, zorder=8)
ax.plot([OFFP[0]], [OFFP[1]], "o", color=ACC, ms=9, zorder=8)
ax.plot([OFFP[0], ONP[0]], [OFFP[1], ONP[1]], color=ACC, lw=2.0, ls=":",
        zorder=5)
ax.text(ONP[0] + 0.3, ONP[1] - 0.3, "$(8,\\ 2)$ is on the line\n"
                                    "$\\lambda = 1.5$ works for both",
        fontsize=11, color=GREEN, ha="left", va="top")
ax.text(OFFP[0] - 0.35, OFFP[1] + 0.25, "$D(8,\\ 3)$", fontsize=12, color=ACC,
        ha="right", va="bottom")
ax.text(5.4, -3.6, "for $D$: $x$ gives $\\lambda = 1.5$, "
                   "but then $y = 2$, not $3$\n"
                   "one $\\lambda$ must work in EVERY component",
        fontsize=12, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
grid(ax, (-1.6, 12.4), (-4.8, 5.0))
ax.set_title("(b)  testing whether a point is on the line", fontsize=12.5,
             color=INK, pad=6)

fig.tight_layout(w_pad=1.8)
save(fig, "ahl-3-11-point.svg")


# ══════════ fig 3: 交点と、平行 ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 5.0))

L1a, L1b = np.array([1.0, 2.0]), np.array([3.0, -1.0])
L2a, L2b = np.array([2.0, -3.0]), np.array([1.0, 2.0])
X = np.array([4.0, 1.0])

# ── (a) 交点
ax = axs[0]
full_line(ax, L1a, L1b, -1.4, 2.4, color=LINE, lw=2.2)
full_line(ax, L2a, L2b, -1.4, 3.2, color=GREEN, lw=2.2)
ax.plot([X[0]], [X[1]], "o", color=ACC, ms=11, zorder=9)
ax.plot([L1a[0], L2a[0]], [L1a[1], L2a[1]], "o", color=INK, ms=6, zorder=8)
ax.text(L1a[0] - 0.25, L1a[1] + 0.3, "$\\lambda = 0$", fontsize=10.5,
        color=LINE, ha="right", va="bottom")
ax.text(L2a[0] - 0.3, L2a[1] - 0.2, "$\\mu = 0$", fontsize=10.5, color=GREEN,
        ha="right", va="top")
ax.plot([4.6, 5.2], [0.6, -1.6], color=ACC, lw=1.2, ls=":", zorder=4)
ax.text(5.4, -2.6, "meeting point $(4,\\ 1)$\n"
                   "$\\lambda = 1$ on $L_1$\n"
                   "$\\mu = 2$ on $L_2$",
        fontsize=11, color=ACC, ha="center", va="center", bbox=BOX, zorder=9)
ax.text(-3.2, 3.6, "$L_1$", fontsize=13, color=LINE, ha="left", va="bottom")
ax.text(4.9, 3.2, "$L_2$", fontsize=13, color=GREEN, ha="center", va="center")
ax.text(3.0, -5.5, "the two parameters need NOT be equal\n"
                   "solve $\\mathbf{a}_1+\\lambda\\mathbf{b}_1 = "
                   "\\mathbf{a}_2+\\mu\\mathbf{b}_2$ for both",
        fontsize=12, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
grid(ax, (-3.4, 8.0), (-6.8, 5.4))
ax.set_title("(a)  where two lines meet", fontsize=12.5, color=INK, pad=6)

# ── (b) 平行
ax = axs[1]
full_line(ax, L1a, L1b, -1.4, 2.4, color=LINE, lw=2.2)
full_line(ax, np.array([1.0, -2.0]), np.array([-3.0, 1.0]), -1.4, 2.4,
          color=GOLD, lw=2.2)
ax.plot([1.0], [-2.0], "o", color=GOLD, ms=8, zorder=8)
ax.text(-3.2, 3.6, "$L_1$", fontsize=13, color=LINE, ha="left", va="bottom")
ax.text(-2.2, -1.5, "$L_3$", fontsize=13, color=GOLD, ha="left", va="top")
ax.text(1.5, -3.1, "$(1,\\ -2)$ is on $L_3$,\nbut not on $L_1$",
        fontsize=10.5, color=GOLD, ha="left", va="top", bbox=BOX, zorder=9)
ax.text(5.0, -1.2, "direction $\\binom{-3}{1} = -\\binom{3}{-1}$",
        fontsize=11, color=GOLD, ha="center", va="center")
ax.text(3.0, -5.5, "parallel directions, and $L_3$ has a point\n"
                   "that is not on $L_1$: they never meet",
        fontsize=12, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
grid(ax, (-3.4, 8.0), (-6.8, 5.4))
ax.set_title("(b)  parallel, and different: no meeting point", fontsize=12.5,
             color=INK, pad=6)

fig.tight_layout(w_pad=1.8)
save(fig, "ahl-3-11-intersect.svg")

print("figures written to", os.path.normpath(OUT))
