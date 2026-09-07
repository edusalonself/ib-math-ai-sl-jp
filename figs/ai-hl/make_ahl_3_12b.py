"""AHL 3.12b（速度が変わる運動）の図を作る。ラベルは英語。
   出力先: ai-hl/03-geometry-and-trigonometry/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_3_12b.py
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


def plain(ax, xlim, ylim, xstep=1, ystep=1, equal=False):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    if equal:
        ax.set_aspect("equal")
    ax.set_xticks(np.arange(xlim[0], xlim[1] + 1e-9, xstep))
    ax.set_yticks(np.arange(ylim[0], ylim[1] + 1e-9, ystep))
    ax.grid(True, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.axhline(0, color=GREY, lw=1.2)
    ax.axvline(0, color=GREY, lw=1.2)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(labelsize=10, colors=INK)


def blank(ax, xlim, ylim, step=1, equal=True):
    plain(ax, xlim, ylim, step, step, equal)
    ax.set_xticklabels([])
    ax.set_yticklabels([])


def arrow(ax, p, q, color=LINE, lw=2.4, z=6, ls="-", scale=15):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=scale,
                                 lw=lw, color=color, zorder=z,
                                 linestyle=ls, shrinkA=0, shrinkB=0))


# ══════════ fig 1: v(t) = (7, 6-4t) の速度と速さ ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.6))

# ── (a) 経路と、そのときどきの速度
ax = axs[0]
tt = np.linspace(0, 3, 300)
X, Y = 7 * tt, 6 * tt - 2 * tt ** 2
ax.plot(X, Y, color=GREY, lw=2.0, ls="--", zorder=2)
K = 0.55                                   # 矢印の縮尺
for T, col in [(0, LINE), (1, LINE), (1.5, ACC), (2, LINE), (3, LINE)]:
    px, py = 7 * T, 6 * T - 2 * T ** 2
    vx, vy = 7.0, 6 - 4 * T
    ax.plot([px], [py], "o", color=INK, ms=6, zorder=8)
    arrow(ax, (px, py), (px + K * vx, py + K * vy), color=col, lw=2.4)
ax.text(10.5, 5.3, "$t = 1.5$: the arrow is horizontal\n"
                   "(the highest point, and the least speed)",
        fontsize=11, color=ACC, ha="center", va="bottom")
ax.text(11.5, -3.4, "$\\mathbf{v} = \\binom{7}{6-4t}$,   "
                    "$\\mathbf{r} = \\binom{7t}{6t-2t^2}$\n"
                    "the across-part never changes; the up-part does",
        fontsize=12, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
for T in (0, 3):
    ax.text(7 * T, 6 * T - 2 * T ** 2 - 0.6, "$t=%d$" % T, fontsize=10,
            color=INK, ha="center", va="top")
blank(ax, (-2.0, 26.0), (-6.0, 9.0), step=2)
ax.set_title("(a)  the velocity arrow changes along the path",
             fontsize=12.5, color=INK, pad=6)

# ── (b) 速さのグラフ
ax = axs[1]
tt = np.linspace(0, 3, 400)
SP = np.sqrt(49 + (6 - 4 * tt) ** 2)
ax.plot(tt, SP, color=LINE, lw=2.6, zorder=5)
ax.plot([1.5], [7], "o", color=ACC, ms=10, zorder=8)
ax.plot([1.5, 1.5], [0, 7], color=ACC, lw=1.4, ls=":", zorder=4)
ax.plot([0, 1.5], [7, 7], color=ACC, lw=1.4, ls=":", zorder=4)
ax.text(1.75, 6.4, "$(1.5,\\ 7)$", fontsize=12, color=ACC, ha="left", va="top")
ax.text(0.15, 10.2, "$|\\mathbf{v}| = \\sqrt{7^2+(6-4t)^2}$",
        fontsize=12.5, color=LINE, ha="left", va="center")
plain(ax, (0, 3), (0, 11), xstep=0.5, ystep=2)
ax.set_xlabel("$t$ (s)", fontsize=11.5, color=INK)
ax.set_ylabel("speed (m s$^{-1}$)", fontsize=11.5, color=INK)
ax.set_title("(b)  the speed is never $0$ here\n"
             "least value $7$, at $t = 1.5$", fontsize=12.5, color=INK, pad=6)

fig.tight_layout(w_pad=2.4)
save(fig, "ahl-3-12b-idea.svg")


# ══════════ fig 2: projectile と circular が特別な場合 ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.6))

# ── (a) projectile
ax = axs[0]
tt = np.linspace(0, 4.0, 400)
X, Y = 15 * tt, 20 * tt - 5 * tt ** 2
ax.plot(X, Y, color=LINE, lw=2.6, zorder=5)
ax.plot([30.0], [20.0], "o", color=ACC, ms=10, zorder=8)
ax.plot([30.0, 30.0], [0, 20.0], color=ACC, lw=1.4, ls=":", zorder=4)
ax.plot([0, 60.0], [0, 0], color=GREY, lw=1.2, zorder=3)
ax.plot([0, 60.0], [0, 0], "o", color=INK, ms=6, zorder=8)
ax.text(30.0, 21.0, "highest point: $v_y = 0$ here", fontsize=11, color=ACC,
        ha="center", va="bottom")
ax.text(0, -1.8, "$t=0$", fontsize=10, color=INK, ha="center", va="top")
ax.text(60.0, -1.8, "back to $y=0$", fontsize=10, color=INK, ha="center",
        va="top")
ax.text(30.0, -8.5, "$\\mathbf{v} = \\binom{15}{20-10t}$:  "
                    "$\\mathbf{a} = \\binom{0}{-10}$ is constant",
        fontsize=12, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
blank(ax, (-6.0, 68.0), (-13.0, 30.0), step=5)
ax.set_title("(a)  projectile motion", fontsize=12.5, color=INK, pad=6)

# ── (b) circular
ax = axs[1]
th = np.linspace(0, 2 * np.pi, 400)
ax.plot(5 * np.cos(th), 5 * np.sin(th), color=GREY, lw=2.0, ls="--", zorder=2)
for a, lab, lx, ly, lha, lva, leader in [
        (0.0, "$t=0$", 6.8, -0.2, "left", "center", (5.4, -0.2)),
        (np.pi / 4, "$t=\\pi/8$", 6.8, 3.4, "left", "center", (4.1, 3.5)),
        (np.pi / 2, "$t=\\pi/4$", 0.6, 6.3, "left", "bottom", None)]:
    px, py = 5 * np.cos(a), 5 * np.sin(a)
    vx, vy = -10 * np.sin(a), 10 * np.cos(a)
    ax.plot([px], [py], "o", color=INK, ms=7, zorder=8)
    arrow(ax, (px, py), (px + 0.30 * vx, py + 0.30 * vy), color=ACC, lw=2.4)
    if leader is not None:
        ax.plot([leader[0], lx - 0.15], [leader[1], ly], color=GREY, lw=1.0,
                ls=":", zorder=4)
    ax.text(lx, ly, lab, fontsize=10.5, color=INK, ha=lha, va=lva)
# 半径は 1 本だけ描く（込み合わないように）
ax.plot([0, 5 * np.cos(np.pi / 4)], [0, 5 * np.sin(np.pi / 4)], color=GREEN,
        lw=1.6, ls=":", zorder=3)
ax.text(1.0, 2.5, "$|\\mathbf{r}| = 5$", fontsize=12,
        color=GREEN, ha="right", va="center")
ax.text(-4.4, 3.6, "$\\mathbf{v}$ is a tangent", fontsize=11, color=ACC,
        ha="center", va="center")
ax.text(1.5, -8.6, "$\\mathbf{r} = \\binom{5\\cos 2t}{5\\sin 2t}$:  "
                   "$|\\mathbf{v}| = 10$ is constant,\n"
                   "but $\\mathbf{v}$ keeps turning",
        fontsize=12, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
blank(ax, (-8.0, 11.5), (-10.5, 10.5), step=2)
ax.set_title("(b)  circular motion", fontsize=12.5, color=INK, pad=6)

fig.tight_layout(w_pad=1.8)
save(fig, "ahl-3-12b-special.svg")


# ══════════ fig 3: 時間のずらし f(t-a) ══════════
fig, ax = plt.subplots(figsize=(8.4, 4.4))

tt = np.linspace(0, 9, 400)
ax.plot(tt, 4 - 2 * tt, color=LINE, lw=2.6, zorder=5)
ax.plot(tt, 14 - 2 * tt, color=GREEN, lw=2.6, zorder=5)
ax.plot([2], [0], "o", color=LINE, ms=9, zorder=8)
ax.plot([7], [0], "o", color=GREEN, ms=9, zorder=8)
ax.annotate("", xy=(7, 1.4), xytext=(2, 1.4),
            arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=2.2))
ax.text(4.5, 2.0, "shift of $5$ seconds", fontsize=12, color=GOLD,
        ha="center", va="bottom", bbox=BOX, zorder=9)
ax.text(0.25, 5.4, "$P$: $v_y = 4-2t$", fontsize=12, color=LINE, ha="left",
        va="center")
ax.text(4.6, 6.2, "$Q$: $v_y = 4-2(t-5) = 14-2t$", fontsize=12, color=GREEN,
        ha="left", va="center")
ax.text(2, -1.0, "$t=2$", fontsize=10.5, color=LINE, ha="center", va="top")
ax.text(7, -1.0, "$t=7$", fontsize=10.5, color=GREEN, ha="center", va="top")
plain(ax, (0, 9), (-6, 8), xstep=1, ystep=2)
ax.set_xlabel("$t$ (s)", fontsize=11.5, color=INK)
ax.set_ylabel("$v_y$ (m s$^{-1}$)", fontsize=11.5, color=INK)
ax.set_title("$f(t-5)$: the same graph, slid $5$ to the right\n"
             "$Q$ does at $t = 7$ what $P$ did at $t = 2$",
             fontsize=12.5, color=INK, pad=8)

fig.tight_layout()
save(fig, "ahl-3-12b-shift.svg")

print("figures written to", os.path.normpath(OUT))
