"""AHL 3.8（単位円と三角比の恒等式）の図を作る。ラベルは英語。
   出力先: ai-hl/03-geometry-and-trigonometry/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_3_8.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from _graph import INK, GRID, LINE, ACC, GREEN, GREY, GOLD, BOX, FILL

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "03-geometry-and-trigonometry", "img")
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True)
    plt.close(fig)
    print("wrote", name)


def circle(ax, R=1.0, **kw):
    t = np.linspace(0, 2 * np.pi, 720)
    ax.plot(R * np.cos(t), R * np.sin(t), **kw)


def arc(ax, a, b, R=1.0, **kw):
    t = np.linspace(a, b, 400)
    ax.plot(R * np.cos(t), R * np.sin(t), **kw)


def axes_box(ax, lim=1.45):
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.axhline(0, color=GREY, lw=1.1, zorder=1)
    ax.axvline(0, color=GREY, lw=1.1, zorder=1)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)


# ══════════ fig 1a: cos, sin は点の座標 ══════════
fig, ax = plt.subplots(figsize=(5.9, 5.4))
TH = 2.2
CX, CY = np.cos(TH), np.sin(TH)
circle(ax, color=GREY, lw=1.8)
ax.add_patch(Wedge((0, 0), 0.30, 0, np.degrees(TH), fc=FILL, ec=GOLD, lw=1.6,
                   zorder=3))
ax.plot([0, CX], [0, CY], color=LINE, lw=2.4, zorder=4)
# 座標そのものを、太い線分で見せる
ax.plot([0, CX], [0, 0], color=GREEN, lw=4.0, zorder=5,
        solid_capstyle="butt")
ax.plot([CX, CX], [0, CY], color=ACC, lw=4.0, zorder=5,
        solid_capstyle="butt")
ax.plot([CX, 0], [CY, CY], color=GREY, lw=1.2, ls=":", zorder=3)
ax.plot([CX], [CY], "o", color=INK, ms=8, zorder=7)
ax.plot([1], [0], "o", color=GREY, ms=6, zorder=7)

ax.text(CX - 0.02, CY + 0.14, "$P(\\cos\\theta,\\ \\sin\\theta)$", fontsize=13,
        color=INK, ha="center", va="bottom", bbox=BOX, zorder=9)
ax.text(CX / 2, -0.10, "$\\cos\\theta$", fontsize=13, color=GREEN,
        ha="center", va="top")
ax.text(CX - 0.08, CY / 2, "$\\sin\\theta$", fontsize=13, color=ACC,
        ha="right", va="center")
ax.text(0.38, 0.16, "$\\theta$", fontsize=14, color=GOLD, ha="left",
        va="center")
ax.text(-0.10, 0.66, "radius $= 1$", fontsize=11.5, color=LINE, ha="center",
        va="center", bbox=BOX, zorder=8)
ax.text(1.06, -0.10, "start here", fontsize=10.5, color=GREY, ha="left",
        va="top")
ax.text(0, -1.36, "the angle is measured from the positive $x$-axis,\n"
                  "anticlockwise; $\\cos\\theta$ and $\\sin\\theta$ are the\n"
                  "coordinates of $P$",
        fontsize=11.5, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
axes_box(ax, 1.58)
ax.set_title("what $\\cos\\theta$ and $\\sin\\theta$ mean", fontsize=12.5,
             color=INK, pad=6)
fig.tight_layout()
save(fig, "ahl-3-8-unit-circle.svg")


# ══════════ fig 1b: 象限ごとの符号 ══════════
fig, ax = plt.subplots(figsize=(5.9, 5.4))
circle(ax, color=GREY, lw=1.8)
QUAD = [(np.pi / 4, "I", "$\\cos +$\n$\\sin +$\n$\\tan +$", GREEN),
        (3 * np.pi / 4, "II", "$\\cos -$\n$\\sin +$\n$\\tan -$", ACC),
        (5 * np.pi / 4, "III", "$\\cos -$\n$\\sin -$\n$\\tan +$", LINE),
        (7 * np.pi / 4, "IV", "$\\cos +$\n$\\sin -$\n$\\tan -$", GOLD)]
for a, name, txt, col in QUAD:
    ax.add_patch(Wedge((0, 0), 1.0, np.degrees(a) - 45, np.degrees(a) + 45,
                       fc=col, ec="none", alpha=0.07, zorder=1))
    ax.text(0.62 * np.cos(a), 0.62 * np.sin(a) - 0.05, txt, fontsize=11.5,
            color=col, ha="center", va="center", linespacing=1.45, zorder=6)
    ax.text(1.24 * np.cos(a), 1.24 * np.sin(a), name, fontsize=12.5,
            color=GREY, ha="center", va="center")
ax.text(0, -1.34, "$\\tan\\theta = \\dfrac{\\sin\\theta}{\\cos\\theta}$, so its "
                  "sign is\nthe two signs divided",
        fontsize=11.5, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
axes_box(ax, 1.52)
ax.set_title("the signs in each quadrant", fontsize=12.5, color=INK,
             pad=6)
fig.tight_layout()
save(fig, "ahl-3-8-quadrants.svg")


# ══════════ fig 2: 単位円からグラフへ ══════════
fig = plt.figure(figsize=(11.6, 5.0))
gs = fig.add_gridspec(2, 2, width_ratios=[1.0, 2.0], hspace=0.55, wspace=0.22)

MARKS = [0.6, 2.2, 3.9, 5.4]
COLS = [GREEN, ACC, LINE, GOLD]

# ── 左上: 単位円（sin 用）
ax = fig.add_subplot(gs[0, 0])
circle(ax, color=GREY, lw=1.6)
for t, c in zip(MARKS, COLS):
    ax.plot([0, np.cos(t)], [0, np.sin(t)], color=c, lw=1.6, zorder=3)
    ax.plot([np.cos(t), np.cos(t)], [0, np.sin(t)], color=c, lw=2.2, zorder=4)
    ax.plot([np.cos(t)], [np.sin(t)], "o", color=c, ms=5.5, zorder=6)
axes_box(ax, 1.25)
ax.set_title("height $=\\sin\\theta$", fontsize=11.5, color=INK, pad=4)

# ── 右上: sin グラフ
ax = fig.add_subplot(gs[0, 1])
t = np.linspace(0, 2 * np.pi, 600)
ax.plot(t, np.sin(t), color=INK, lw=2.4, zorder=4)
for m, c in zip(MARKS, COLS):
    ax.plot([m, m], [0, np.sin(m)], color=c, lw=2.2, zorder=5)
    ax.plot([m], [np.sin(m)], "o", color=c, ms=5.5, zorder=6)
ax.axhline(0, color=GREY, lw=1.1)
ax.set_xlim(-0.25, 2 * np.pi + 0.25)
ax.set_ylim(-1.45, 1.45)
ax.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi])
ax.set_xticklabels(["$0$", "$\\dfrac{\\pi}{2}$", "$\\pi$",
                    "$\\dfrac{3\\pi}{2}$", "$2\\pi$"])
ax.set_yticks([-1, 0, 1])
ax.grid(True, color=GRID, lw=0.8)
ax.set_axisbelow(True)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
for sp in ("bottom", "left"):
    ax.spines[sp].set_color(GREY)
ax.set_title("$y = \\sin x$: the height, unrolled", fontsize=11.5, color=INK,
             pad=4)

# ── 左下: 単位円（cos 用）
ax = fig.add_subplot(gs[1, 0])
circle(ax, color=GREY, lw=1.6)
for t_, c in zip(MARKS, COLS):
    ax.plot([0, np.cos(t_)], [0, np.sin(t_)], color=c, lw=1.6, zorder=3)
    ax.plot([0, np.cos(t_)], [np.sin(t_), np.sin(t_)], color=c, lw=2.2,
            zorder=4)
    ax.plot([np.cos(t_)], [np.sin(t_)], "o", color=c, ms=5.5, zorder=6)
axes_box(ax, 1.25)
ax.set_title("across $=\\cos\\theta$", fontsize=11.5, color=INK, pad=4)

# ── 右下: cos グラフ
ax = fig.add_subplot(gs[1, 1])
ax.plot(t, np.cos(t), color=INK, lw=2.4, zorder=4)
for m, c in zip(MARKS, COLS):
    ax.plot([m, m], [0, np.cos(m)], color=c, lw=2.2, zorder=5)
    ax.plot([m], [np.cos(m)], "o", color=c, ms=5.5, zorder=6)
ax.axhline(0, color=GREY, lw=1.1)
ax.set_xlim(-0.25, 2 * np.pi + 0.25)
ax.set_ylim(-1.45, 1.45)
ax.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi])
ax.set_xticklabels(["$0$", "$\\dfrac{\\pi}{2}$", "$\\pi$",
                    "$\\dfrac{3\\pi}{2}$", "$2\\pi$"])
ax.set_yticks([-1, 0, 1])
ax.grid(True, color=GRID, lw=0.8)
ax.set_axisbelow(True)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
for sp in ("bottom", "left"):
    ax.spines[sp].set_color(GREY)
ax.set_title("$y = \\cos x$: the across, unrolled", fontsize=11.5, color=INK,
             pad=4)

fig.suptitle("One trip round the circle is one period of the graph",
             fontsize=13.5, y=1.0)
save(fig, "ahl-3-8-graphs.svg")


# ══════════ fig 3: ambiguous case ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.6))

# ── (a) 同じ sin を与える 2 つの角
ax = axs[0]
t = np.linspace(0, np.pi, 500)
ax.plot(t, np.sin(t), color=INK, lw=2.4, zorder=4)
S = 0.7949
t1 = np.arcsin(S)
t2 = np.pi - t1
ax.axhline(S, color=ACC, lw=1.8, ls="--", zorder=3)
for tt, lab, col in ((t1, "$\\theta$", GREEN), (t2, "$\\pi - \\theta$", GOLD)):
    ax.plot([tt, tt], [0, S], color=col, lw=2.2, zorder=5)
    ax.plot([tt], [S], "o", color=col, ms=8, zorder=6)
    ax.text(tt, -0.09, lab, fontsize=12.5, color=col, ha="center", va="top")
ax.text(np.pi / 2, S + 0.05, "$\\sin\\theta = \\sin(\\pi - \\theta)$",
        fontsize=12.5, color=ACC, ha="center", va="bottom", bbox=BOX, zorder=8)
ax.axhline(0, color=GREY, lw=1.1)
ax.set_xlim(-0.15, np.pi + 0.15)
ax.set_ylim(-0.28, 1.28)
ax.set_xticks([0, np.pi / 2, np.pi])
ax.set_xticklabels(["$0$", "$\\dfrac{\\pi}{2}$", "$\\pi$"])
ax.set_yticks([0, 1])
ax.grid(True, color=GRID, lw=0.8)
ax.set_axisbelow(True)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
for sp in ("bottom", "left"):
    ax.spines[sp].set_color(GREY)
ax.set_title("(a)  two angles share one sine", fontsize=12.5, color=INK,
             pad=8)

# ── (b) 2 つの三角形
ax = axs[1]
A = np.radians(32.0)
a_len, b_len = 5.4, 8.1
Ax, Ay = 0.0, 0.0
Cx, Cy = b_len * np.cos(A), b_len * np.sin(A)     # AC = b
B1 = 10.1457
B2 = 3.5926
# C を中心とする半径 a の円の、下側の弧だけを描く（弧が底辺と 2 回交わる）
th = np.linspace(np.pi + 0.35, 2 * np.pi - 0.35, 400)
ax.plot(Cx + a_len * np.cos(th), Cy + a_len * np.sin(th), color=GREY, lw=1.3,
        ls=":", zorder=2)
for cval, col, lab in ((B1, GREEN, "$c = 10.1$"), (B2, GOLD, "$c = 3.59$")):
    Bx, By = cval, 0.0
    ax.plot([Ax, Bx], [Ay, By], color=col, lw=2.2, zorder=4)
    ax.plot([Bx, Cx], [By, Cy], color=col, lw=2.2, zorder=4)
    ax.plot([Bx], [By], "o", color=col, ms=7, zorder=6)
    ax.text(Bx, -0.45, lab, fontsize=11.5, color=col, ha="center", va="top")
    mx, my = (Bx + Cx) / 2, (By + Cy) / 2
    ax.text(mx + 0.42, my, "$a = 5.4$", fontsize=10.5, color=col, ha="left",
            va="center", bbox=BOX, zorder=8)
ax.plot([Ax, Cx], [Ay, Cy], color=LINE, lw=2.6, zorder=5)
ax.plot([Ax, Cx], [Ay, Cy], "o", color=INK, ms=7, zorder=7)
ax.text(Ax - 0.30, Ay - 0.18, "$A$", fontsize=12.5, color=INK, ha="right",
        va="top")
ax.text(Cx - 0.15, Cy + 0.30, "$C$", fontsize=12.5, color=INK, ha="center",
        va="bottom")
ax.text(Cx / 2 - 0.30, Cy / 2 + 0.55, "$b = 8.1$", fontsize=11.5, color=LINE,
        ha="center", va="center", bbox=BOX, zorder=8)
ax.add_patch(Wedge((Ax, Ay), 1.30, 0, 32, fc="none", ec=ACC, lw=1.6,
                   zorder=6))
ax.text(1.55, 0.34, "$A = 32^{\\circ}$", fontsize=11.5, color=ACC, ha="left",
        va="bottom")
ax.text(6.2, -1.65, "swinging $a = 5.4$ from $C$ meets the base line twice",
        fontsize=11, color=GREY, ha="center", va="center", bbox=BOX, zorder=8)
ax.set_xlim(-1.5, 13.0)
ax.set_ylim(-2.3, 5.7)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("(b)  so two different triangles fit", fontsize=12.5, color=INK,
             pad=8)

fig.tight_layout(w_pad=1.8)
save(fig, "ahl-3-8-ambiguous.svg")

print("figures written to", os.path.normpath(OUT))
