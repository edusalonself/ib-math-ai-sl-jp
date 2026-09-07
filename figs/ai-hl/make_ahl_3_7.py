"""AHL 3.7（弧度法）の図を作る。ラベルは英語。
   出力先: ai-hl/03-geometry-and-trigonometry/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_3_7.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, FancyArrowPatch
from _graph import INK, GRID, LINE, ACC, GREEN, GREY, GOLD, BOX, FILL

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "03-geometry-and-trigonometry", "img")
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True)
    plt.close(fig)
    print("wrote", name)


def blank(ax, lim=1.42):
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.axis("off")


def circle(ax, R=1.0, **kw):
    t = np.linspace(0, 2 * np.pi, 600)
    ax.plot(R * np.cos(t), R * np.sin(t), **kw)


def arc(ax, a, b, R=1.0, **kw):
    t = np.linspace(a, b, 400)
    ax.plot(R * np.cos(t), R * np.sin(t), **kw)


# ══════════ fig 1: radian の定義 と 2π 本ぶん ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 5.3))

# ── (a) 1 radian
ax = axs[0]
circle(ax, color=GREY, lw=1.8)
ax.add_patch(Wedge((0, 0), 0.30, 0, np.degrees(1.0), fc=FILL, ec=GOLD, lw=1.6,
                   zorder=3))
ax.plot([0, 1], [0, 0], color=LINE, lw=2.6, zorder=4)
ax.plot([0, np.cos(1)], [0, np.sin(1)], color=LINE, lw=2.6, zorder=4)
arc(ax, 0, 1.0, color=ACC, lw=4.5, zorder=5, solid_capstyle="round")
ax.plot([0, 1, np.cos(1)], [0, 0, np.sin(1)], "o", color=INK, ms=6, zorder=7)
ax.text(0.5, -0.13, "$r$", fontsize=14, color=LINE, ha="center", va="top")
ax.text(0.5 * np.cos(1) - 0.11, 0.5 * np.sin(1) + 0.03, "$r$", fontsize=14,
        color=LINE, ha="right", va="bottom")
ax.text(1.10 * np.cos(0.5), 1.10 * np.sin(0.5),
        "arc length\n$= r$", fontsize=12.5, color=ACC, ha="left", va="center")
ax.text(0.40, 0.16, "$1$ radian", fontsize=12.5, color=GOLD, ha="left",
        va="center")
ax.text(0, -1.30, "the angle whose arc is one radius long\n"
                  "$1\\ \\mathrm{rad} \\approx 57.3^{\\circ}$",
        fontsize=12, color=INK, ha="center", va="center", bbox=BOX, zorder=8)
blank(ax, 1.55)
ax.set_title("(a)  what one radian is", fontsize=12.5, color=INK, pad=6)

# ── (b) 円周には半径が 2π 本ぶん
ax = axs[1]
circle(ax, color=GREY, lw=1.6)
cols = [LINE, ACC]
for i in range(6):
    arc(ax, i, i + 1, color=cols[i % 2], lw=5.0, solid_capstyle="butt",
        zorder=4)
arc(ax, 6, 2 * np.pi, color=GREEN, lw=5.0, solid_capstyle="butt", zorder=4)
for i in range(7):
    ax.plot([0.93 * np.cos(i), 1.07 * np.cos(i)],
            [0.93 * np.sin(i), 1.07 * np.sin(i)], color=INK, lw=1.4, zorder=6)
    ax.text(1.20 * np.cos(i), 1.20 * np.sin(i), f"${i}$", fontsize=12,
            color=INK, ha="center", va="center")
ax.plot([0, 1], [0, 0], color=GREY, lw=1.8, ls="--", zorder=3)
ax.text(0.5, 0.09, "$r$", fontsize=13, color=GREY, ha="center", va="bottom")
ax.text(np.cos(6.15) * 1.42, np.sin(6.15) * 1.42 - 0.10,
        "$0.28$ left over", fontsize=11.5, color=GREEN, ha="left", va="center")
ax.text(0, -1.42, "the circumference is $2\\pi r$,\n"
                  "so a full turn is $2\\pi = 6.28$ radians",
        fontsize=12, color=INK, ha="center", va="center", bbox=BOX, zorder=8)
blank(ax, 1.72)
ax.set_title("(b)  how many radii fit round the circle", fontsize=12.5,
             color=INK, pad=6)

fig.tight_layout(w_pad=1.4)
save(fig, "ahl-3-7-radian.svg")


# ══════════ fig 2: 弧と扇形 ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 5.1))

TH = 1.2

# ── (a) 記号
ax = axs[0]
ax.add_patch(Wedge((0, 0), 1.0, 0, np.degrees(TH), fc=FILL, ec="none",
                   zorder=2))
circle(ax, color=GREY, lw=1.4, ls="--")
ax.plot([0, 1], [0, 0], color=LINE, lw=2.6, zorder=4)
ax.plot([0, np.cos(TH)], [0, np.sin(TH)], color=LINE, lw=2.6, zorder=4)
arc(ax, 0, TH, color=ACC, lw=4.5, zorder=5, solid_capstyle="round")
ax.add_patch(Wedge((0, 0), 0.26, 0, np.degrees(TH), fc="none", ec=GOLD,
                   lw=1.8, zorder=6))
ax.text(0.34, 0.14, "$\\theta$", fontsize=15, color=GOLD, ha="left",
        va="center")
ax.text(0.52, -0.12, "$r$", fontsize=14, color=LINE, ha="center", va="top")
ax.text(0.52 * np.cos(TH) - 0.12, 0.52 * np.sin(TH), "$r$", fontsize=14,
        color=LINE, ha="right", va="center")
ax.text(1.10 * np.cos(TH / 2), 1.10 * np.sin(TH / 2), "$l$", fontsize=15,
        color=ACC, ha="left", va="center")
ax.text(0.42 * np.cos(TH / 2), 0.42 * np.sin(TH / 2) + 0.18, "$A$",
        fontsize=15, color=LINE, ha="center", va="center")
ax.text(0, -1.32, "$l = r\\theta$        $A = \\dfrac{1}{2}r^{2}\\theta$"
                  "\n$\\theta$ in radians",
        fontsize=13, color=INK, ha="center", va="center", bbox=BOX, zorder=8)
blank(ax, 1.62)
ax.set_title("(a)  the two formulas", fontsize=12.5, color=INK, pad=6)

# ── (b) 円全体の θ/(2π) 倍
ax = axs[1]
ax.add_patch(Wedge((0, 0), 1.0, 0, np.degrees(TH), fc=FILL, ec=LINE, lw=2.2,
                   zorder=3))
circle(ax, color=GREY, lw=1.8)
arc(ax, 0, TH, color=ACC, lw=4.5, zorder=5, solid_capstyle="round")
ax.annotate("", xy=(np.cos(TH) * 1.28, np.sin(TH) * 1.28),
            xytext=(1.28, 0.0),
            arrowprops=dict(arrowstyle="<->", color=GOLD, lw=1.6,
                            connectionstyle=f"angle3,angleA=90,angleB={np.degrees(TH)+90:.1f}"))
ax.text(1.30 * np.cos(TH / 2) + 0.10, 1.30 * np.sin(TH / 2),
        "$\\theta$ out of $2\\pi$", fontsize=12, color=GOLD, ha="left",
        va="center")
ax.text(0, -1.34,
        "$l = \\dfrac{\\theta}{2\\pi}\\times 2\\pi r = r\\theta$\n"
        "$A = \\dfrac{\\theta}{2\\pi}\\times \\pi r^{2} = \\dfrac{1}{2}r^{2}\\theta$",
        fontsize=12.5, color=INK, ha="center", va="center", bbox=BOX, zorder=8)
blank(ax, 1.72)
ax.set_title("(b)  a sector is a fraction of the whole circle", fontsize=12.5,
             color=INK, pad=6)

fig.tight_layout(w_pad=1.4)
save(fig, "ahl-3-7-sector.svg")

print("figures written to", os.path.normpath(OUT))
