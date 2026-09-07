"""AHL 2.7（合成関数と逆関数）の図を作る。ラベルは英語。
   出力先: ai-hl/02-functions/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_2_7.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from _graph import INK, GRID, LINE, ACC, GREEN, GREY, GOLD, BOX, FILL

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "02-functions", "img")
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True)
    plt.close(fig)
    print("wrote", name)


def tidy(ax):
    ax.grid(True, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("bottom", "left"):
        ax.spines[sp].set_color(GREY)


# ══════════ fig 1: 機械の直列つなぎ / 順を変えると別の関数 ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.9))

ax = axs[0]
ax.set_xlim(0, 10.6)
ax.set_ylim(-0.4, 6.4)
ax.axis("off")


def machine(cx, cy, lab, col):
    ax.add_patch(FancyBboxPatch((cx - 0.72, cy - 0.55), 1.44, 1.10,
                                boxstyle="round,pad=0.14", fc="white",
                                ec=col, lw=2.2, zorder=4))
    ax.text(cx, cy, lab, fontsize=14, ha="center", va="center", color=col,
            zorder=5)


def flow(x0, x1, cy, lab, col):
    ax.add_patch(FancyArrowPatch((x0, cy), (x1, cy), arrowstyle="-|>",
                                 mutation_scale=16, color=col, lw=2.0,
                                 zorder=3))
    ax.text((x0 + x1) / 2, cy + 0.30, lab, fontsize=12.5, color=col,
            ha="center", va="bottom", zorder=6)


# 上の列: g のあとに f
flow(0.45, 2.55, 4.9, "$3$", GREEN)
machine(3.4, 4.9, "$g$", GREEN)
flow(4.25, 6.35, 4.9, "$9$", GREEN)
machine(7.2, 4.9, "$f$", GREEN)
flow(8.05, 10.1, 4.9, "$19$", GREEN)
ax.text(0.1, 5.95, "$(f \\circ g)(3) = f(g(3)) = 19$", fontsize=13,
        color=GREEN, ha="left", va="center")

# 下の列: f のあとに g
flow(0.45, 2.55, 1.5, "$3$", ACC)
machine(3.4, 1.5, "$f$", ACC)
flow(4.25, 6.35, 1.5, "$7$", ACC)
machine(7.2, 1.5, "$g$", ACC)
flow(8.05, 10.1, 1.5, "$49$", ACC)
ax.text(0.1, 2.55, "$(g \\circ f)(3) = g(f(3)) = 49$", fontsize=13,
        color=ACC, ha="left", va="center")

ax.text(5.3, 0.20, "same two machines, different order — different answer",
        fontsize=11.5, color=GREY, ha="center", va="center")
ax.text(0.1, 3.35, "$f(x) = 2x+1$,   $g(x) = x^{2}$", fontsize=12.5,
        color=INK, ha="left", va="center")
ax.set_title("(a)  a composite is two machines in a row", fontsize=12,
             color=INK, pad=10)

ax = axs[1]
X = np.linspace(-2.2, 2.2, 500)
ax.plot(X, 2 * X ** 2 + 1, color=GREEN, lw=2.8,
        label="$(f \\circ g)(x) = 2x^{2}+1$")
ax.plot(X, (2 * X + 1) ** 2, color=ACC, lw=2.8, ls="--",
        label="$(g \\circ f)(x) = (2x+1)^{2}$")
ax.plot([0], [1], "o", color=GREEN, ms=8, zorder=6)
ax.plot([0], [1], "o", color=ACC, ms=8, zorder=6, mfc="none", mew=2)
ax.plot([-0.5], [0], "o", color=ACC, ms=8, zorder=6)
ax.annotate("$(g \\circ f)$ is zero\nat $x = -0.5$",
            xy=(-0.5, 0.0), xytext=(0.85, 1.05), fontsize=11, color=ACC,
            ha="left", va="bottom", bbox=BOX, zorder=8,
            arrowprops=dict(arrowstyle="->", color=ACC, lw=1.4,
                            shrinkA=2, shrinkB=6))
ax.annotate("$(f \\circ g)$ is never\nbelow $1$", xy=(0.0, 1.0),
            xytext=(-2.15, 1.7), fontsize=11, color=GREEN,
            ha="left", va="bottom", bbox=BOX, zorder=8,
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.4,
                            shrinkA=2, shrinkB=6))
ax.axhline(0, color=GREY, lw=1.2)
ax.set_xlim(-2.3, 2.6)
ax.set_ylim(-1.4, 12.6)
ax.set_xlabel("$x$")
ax.legend(fontsize=11, frameon=False, loc="upper center")
ax.set_title("(b)  the two composites are different functions",
             fontsize=12, color=INK, pad=10)
tidy(ax)

fig.tight_layout()
save(fig, "ahl-2-7-composite.svg")


# ══════════ fig 2: なぜ domain restriction が要るか / 制限したあと ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 5.0))

ax = axs[0]
X = np.linspace(-0.6, 6.6, 500)
ax.plot(X, (X - 3) ** 2 - 2, color=LINE, lw=2.8)
ax.plot([-0.5, 6.9], [2, 2], color=ACC, lw=2.0, ls="--")
ax.plot([1, 5], [2, 2], "o", color=ACC, ms=9, zorder=6)
ax.plot([3], [-2], "o", color=GOLD, ms=8, zorder=6)
ax.plot([1, 1], [0, 2], color=GREY, lw=1.2, ls=":", zorder=3)
ax.plot([5, 5], [0, 2], color=GREY, lw=1.2, ls=":", zorder=3)
ax.text(7.05, 2, "$y = 2$", fontsize=12, color=ACC, va="center", ha="left")
ax.text(1, -0.75, "$x = 1$", fontsize=11.5, color=ACC, ha="center")
ax.text(5, -0.75, "$x = 5$", fontsize=11.5, color=ACC, ha="center")
ax.text(3, -2.75, "vertex $(3,\\ -2)$", fontsize=11.5, color=GOLD,
        ha="center", va="top")
ax.text(6.9, 8.6, "$f(x) = (x-3)^{2} - 2$", fontsize=12, color=LINE,
        ha="right", va="center", bbox=BOX, zorder=8)
ax.text(-0.4, 11.6, "one output, two inputs:\nthere is no way back",
        fontsize=12, color=INK, ha="left", va="top", bbox=BOX, zorder=8)
ax.axhline(0, color=GREY, lw=1.2)
ax.set_xlim(-0.9, 9.4)
ax.set_ylim(-3.8, 12.4)
ax.set_xlabel("$x$")
ax.set_title("(a)  without a restriction there is no inverse",
             fontsize=12, color=INK, pad=10)
tidy(ax)

ax = axs[1]
XR = np.linspace(3, 7.2, 400)
ax.plot(XR, (XR - 3) ** 2 - 2, color=LINE, lw=3.0,
        label="$f(x) = (x-3)^{2}-2$,  $x \\geq 3$")
XI = np.linspace(-2, 14.5, 500)
ax.plot(XI, 3 + np.sqrt(XI + 2), color=ACC, lw=3.0,
        label="$f^{-1}(x) = 3 + \\sqrt{x+2}$")
DD = np.linspace(-3.5, 14.5, 200)
ax.plot(DD, DD, color=GREY, lw=1.6, ls="--", label="$y = x$")
ax.plot([5, -2], [2, 3], "o", color=INK, ms=0)
ax.plot([5], [2], "o", color=LINE, ms=9, zorder=6)
ax.plot([2], [5], "o", color=ACC, ms=9, zorder=6)
ax.plot([5, 2], [2, 5], color=GREY, lw=1.1, ls=":", zorder=3)
ax.text(5.3, 1.7, "$(5,\\ 2)$", fontsize=11.5, color=LINE, ha="left",
        va="top")
ax.text(1.7, 5.4, "$(2,\\ 5)$", fontsize=11.5, color=ACC, ha="right",
        va="bottom")
ax.plot([3], [-2], "o", color=LINE, ms=8, zorder=6)
ax.plot([-2], [3], "o", color=ACC, ms=8, zorder=6)
ax.text(-3.3, 13.0, "the restricted branch and its\nreflection in $y = x$",
        fontsize=12, color=INK, ha="left", va="top", bbox=BOX, zorder=8)
ax.axhline(0, color=GREY, lw=1.2)
ax.axvline(0, color=GREY, lw=1.2)
ax.set_xlim(-3.5, 14.5)
ax.set_ylim(-3.5, 14.5)
ax.set_aspect("equal")
ax.set_xlabel("$x$")
ax.legend(fontsize=10, frameon=False, loc="lower right")
ax.set_title("(b)  restrict to $x \\geq 3$ and the inverse exists",
             fontsize=12, color=INK, pad=10)
tidy(ax)

fig.tight_layout()
save(fig, "ahl-2-7-inverse.svg")

print("figures written to", os.path.normpath(OUT))
