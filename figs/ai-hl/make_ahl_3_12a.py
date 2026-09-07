"""AHL 3.12a（等速度の運動）の図を作る。ラベルは英語。
   出力先: ai-hl/03-geometry-and-trigonometry/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_3_12a.py
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


def grid(ax, xlim, ylim, step=1, equal=True):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    if equal:
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


def path(ax, r0, v, lo, hi, color=GREY, lw=1.8, ls="--", z=2):
    r0, v = np.array(r0, float), np.array(v, float)
    p, q = r0 + lo * v, r0 + hi * v
    ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw, ls=ls, zorder=z)


def dots(ax, r0, v, ts, color, ms=7, z=8):
    r0, v = np.array(r0, float), np.array(v, float)
    P = np.array([r0 + t * v for t in ts])
    ax.plot(P[:, 0], P[:, 1], "o", color=color, ms=ms, zorder=z)
    return P


# ══════════ fig 1: r = r0 + vt と、速さに意味があること ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.8))

R0 = np.array([1.0, 2.0])
VV = np.array([2.0, 1.0])

# ── (a) 1 秒ごとに v だけ進む
ax = axs[0]
path(ax, R0, VV, -0.6, 4.6, color=GREY)
P = dots(ax, R0, VV, range(5), INK)
for i, p in enumerate(P):
    ax.text(p[0] - 0.15, p[1] + 0.35, "$t = %d$" % i, fontsize=10.5, color=INK,
            ha="right", va="bottom")
arrow(ax, tuple(P[0]), tuple(P[1]), color=ACC, lw=3.0)
ax.text(2.0, 2.15, "$\\mathbf{v}$", fontsize=14, color=ACC, ha="center",
        va="top")
ax.text(5.6, -1.4, "$\\mathbf{r} = \\binom{1}{2} + t\\binom{2}{1}$\n"
                   "the dots are evenly spaced,\n"
                   "because $\\mathbf{v}$ is the SAME every second",
        fontsize=12, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
grid(ax, (-1.6, 11.4), (-3.4, 7.4))
ax.set_title("(a)  one step of $\\mathbf{v}$ per unit of time", fontsize=12.5,
             color=INK, pad=6)

# ── (b) 同じ道すじ、ちがう速さ
ax = axs[1]
path(ax, R0, VV, -0.6, 4.6, color=GREY)
QQ = dots(ax, R0, 2 * VV, range(3), GREEN, ms=13, z=7)
PP = dots(ax, R0, VV, range(5), LINE, ms=6.5, z=9)
for i, p in enumerate(PP):
    ax.text(p[0] - 0.12, p[1] + 0.3, "$%d$" % i, fontsize=10.5, color=LINE,
            ha="right", va="bottom")
for i, q in enumerate(QQ):
    ax.text(q[0] + 0.15, q[1] - 0.3, "$%d$" % i, fontsize=10.5, color=GREEN,
            ha="left", va="top")
ax.text(5.6, -0.7, "$P$: $\\mathbf{v} = \\binom{2}{1}$",
        fontsize=12, color=LINE, ha="center", va="center", zorder=10)
ax.text(5.6, -1.7, "$Q$: $\\mathbf{v} = \\binom{4}{2}$",
        fontsize=12, color=GREEN, ha="center", va="center", zorder=10)
ax.text(5.6, -2.8, "SAME path, but $Q$ is twice as fast\n"
                   "here the LENGTH of $\\mathbf{v}$ matters",
        fontsize=12, color=INK, ha="center", va="center", zorder=10)
grid(ax, (-1.6, 11.4), (-3.4, 7.4))
ax.set_title("(b)  same path, different speed\n"
             "(the numbers on the dots are the times)", fontsize=12.5,
             color=INK, pad=6)

fig.tight_layout(w_pad=1.8)
save(fig, "ahl-3-12a-idea.svg")


# ══════════ fig 2: 経路が交わる ≠ 衝突する ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 5.2))

Aa, Av = np.array([1.0, 2.0]), np.array([2.0, 3.0])

# ── (a) 交わるが、衝突しない
ax = axs[0]
Ba, Bv = np.array([13.0, 0.0]), np.array([-2.0, 1.0])
path(ax, Aa, Av, -0.4, 3.4, color=LINE, lw=1.6)
path(ax, Ba, Bv, -0.4, 6.4, color=GREEN, lw=1.6)
PA = dots(ax, Aa, Av, range(4), LINE, ms=7)
PB = dots(ax, Ba, Bv, range(6), GREEN, ms=7)
for i, p in enumerate(PA):
    ax.text(p[0] - 0.25, p[1] + 0.15, "$%d$" % i, fontsize=10, color=LINE,
            ha="right", va="bottom")
for i, p in enumerate(PB):
    ax.text(p[0] + 0.25, p[1] - 0.15, "$%d$" % i, fontsize=10, color=GREEN,
            ha="left", va="top")
ax.plot([3.0], [5.0], "o", color=ACC, ms=13, mfc="none", mew=2.5, zorder=10)
ax.plot([3.6, 8.4], [5.4, 7.6], color=ACC, lw=1.2, ls=":", zorder=4)
ax.text(10.6, 8.2, "paths cross at $(3,\\ 5)$", fontsize=11.5, color=ACC,
        ha="center", va="center", bbox=BOX, zorder=9)
ax.text(6.6, -3.4, "$A$ is there at $t = 1$, $B$ at $t = 5$\n"
                   "different times: no collision",
        fontsize=12, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
grid(ax, (-1.6, 15.4), (-5.4, 12.6))
ax.set_title("(a)  the paths cross, but the particles do not meet",
             fontsize=12.5, color=INK, pad=6)

# ── (b) 衝突する
ax = axs[1]
Ca, Cv = np.array([5.0, 4.0]), np.array([-2.0, 1.0])
path(ax, Aa, Av, -0.4, 3.4, color=LINE, lw=1.6)
path(ax, Ca, Cv, -0.4, 3.4, color=GREEN, lw=1.6)
PA = dots(ax, Aa, Av, range(4), LINE, ms=7)
PC = dots(ax, Ca, Cv, range(4), GREEN, ms=7)
for i, p in enumerate(PA):
    ax.text(p[0] - 0.25, p[1] + 0.15, "$%d$" % i, fontsize=10, color=LINE,
            ha="right", va="bottom")
for i, p in enumerate(PC):
    ax.text(p[0] + 0.25, p[1] - 0.15, "$%d$" % i, fontsize=10, color=GREEN,
            ha="left", va="top")
ax.plot([3.0], [5.0], "o", color=ACC, ms=13, zorder=10)
ax.plot([3.6, 8.4], [5.4, 7.6], color=ACC, lw=1.2, ls=":", zorder=4)
ax.text(10.6, 8.2, "both at $(3,\\ 5)$ when $t = 1$", fontsize=11.5, color=ACC,
        ha="center", va="center", bbox=BOX, zorder=9)
ax.text(6.6, -3.4, "same place at the SAME time:\ncollision at $t = 1$",
        fontsize=12, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
grid(ax, (-1.6, 15.4), (-5.4, 12.6))
ax.set_title("(b)  a real collision", fontsize=12.5, color=INK, pad=6)

fig.tight_layout(w_pad=1.8)
save(fig, "ahl-3-12a-cross.svg")


# ══════════ fig 3: 最接近 ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.8))

Sa, Sv = np.array([0.0, 0.0]), np.array([3.0, 0.0])
Ta, Tv = np.array([25.0, 0.0]), np.array([0.0, 4.0])

# ── (a) 2 隻の位置と、そのときの AB
ax = axs[0]
path(ax, Sa, Sv, -0.2, 6.4, color=LINE, lw=1.6)
path(ax, Ta, Tv, -0.2, 6.4, color=GREEN, lw=1.6)
for T in range(6):
    p, q = Sa + T * Sv, Ta + T * Tv
    dy = -2.6 if T == 0 else 0.0        # t=0 は x 軸と重なるので、少し下げて描く
    ax.plot([p[0], q[0]], [p[1] + dy, q[1] + dy],
            color=(ACC if T == 3 else (GOLD if T == 0 else GREY)),
            lw=(2.6 if T == 3 else (2.0 if T == 0 else 1.2)),
            ls=("-" if T == 3 else ":"), zorder=(6 if T in (0, 3) else 3))
ax.text(12.5, -3.2, "$25$ km at $t = 0$", fontsize=11, color=GOLD,
        ha="center", va="top")
PS = dots(ax, Sa, Sv, range(6), LINE, ms=6)
PT = dots(ax, Ta, Tv, range(6), GREEN, ms=6)
for T in (0, 3, 5):
    ax.text(PS[T][0], PS[T][1] - 1.4, "$t=%d$" % T, fontsize=10, color=LINE,
            ha="center", va="top")
    ax.text(PT[T][0] + 0.8, PT[T][1], "$t=%d$" % T, fontsize=10, color=GREEN,
            ha="left", va="center")
ax.text(13.6, 9.2, "$20$ km", fontsize=12.5, color=ACC, ha="right",
        va="center", bbox=BOX, zorder=9)
ax.text(13.0, -7.0, "$A$ goes east at $3$, $B$ goes north at $4$\n"
                    "the gap is smallest at $t = 3$",
        fontsize=12, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
grid(ax, (-3.4, 32.4), (-10.4, 22.4), step=5)
ax.set_title("(a)  two ships, and the gap between them", fontsize=12.5,
             color=INK, pad=6)

# ── (b) d(t) のグラフ
ax = axs[1]
tt = np.linspace(0, 6.4, 400)
dd = 5 * np.sqrt((tt - 3) ** 2 + 16)
ax.plot(tt, dd, color=LINE, lw=2.6, zorder=5)
ax.plot([3], [20], "o", color=ACC, ms=10, zorder=8)
ax.plot([3, 3], [0, 20], color=ACC, lw=1.4, ls=":", zorder=4)
ax.plot([0, 3], [20, 20], color=ACC, lw=1.4, ls=":", zorder=4)
ax.text(3.35, 20.6, "$(3,\\ 20)$", fontsize=12, color=ACC, ha="left",
        va="bottom")
ax.text(0.25, 25.4, "$d = 5\\sqrt{(t-3)^2+16}$", fontsize=12.5, color=LINE,
        ha="left", va="center")
ax.set_xlim(0, 6.4)
ax.set_ylim(0, 28.5)
ax.set_xticks(range(7))
ax.set_yticks(range(0, 29, 5))
ax.grid(True, color=GRID, lw=0.8)
ax.set_axisbelow(True)
for sp_ in ax.spines.values():
    sp_.set_visible(False)
ax.axhline(0, color=GREY, lw=1.2)
ax.axvline(0, color=GREY, lw=1.2)
ax.set_xlabel("$t$ (hours)", fontsize=11.5, color=INK)
ax.set_ylabel("$d$ (km)", fontsize=11.5, color=INK)
ax.tick_params(labelsize=10, colors=INK)
ax.set_title("(b)  the distance never reaches $0$\n"
             "least value $20$ km, at $t = 3$",
             fontsize=12.5, color=INK, pad=6)

fig.tight_layout(w_pad=2.4)
save(fig, "ahl-3-12a-closest.svg")

print("figures written to", os.path.normpath(OUT))
