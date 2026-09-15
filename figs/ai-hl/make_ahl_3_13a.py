"""AHL 3.13a（scalar product）の図を作る。ラベルは英語。
   出力先: ai-hl/03-geometry-and-trigonometry/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_3_13a.py

   ★ matplotlib の mathtext は \\begin{pmatrix} も \\lvert も読めません。
      縦ベクトルは \\binom、絶対値は | を使います。
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Arc
from _graph import INK, GRID, LINE, ACC, GREEN, GREY, GOLD, BOX, FILL

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "03-geometry-and-trigonometry", "img")
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True)
    plt.close(fig)
    print("wrote", name)


def plain(ax, xlim, ylim, xstep=1, ystep=1, equal=False, axes=True, grid=True):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    if equal:
        ax.set_aspect("equal")
    ax.set_xticks(np.arange(xlim[0], xlim[1] + 1e-9, xstep))
    ax.set_yticks(np.arange(ylim[0], ylim[1] + 1e-9, ystep))
    if grid:
        ax.grid(True, color=GRID, lw=0.8)
    else:
        ax.grid(False)
    ax.set_axisbelow(True)
    if axes:
        ax.axhline(0, color=GREY, lw=1.2)
        ax.axvline(0, color=GREY, lw=1.2)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(labelsize=10, colors=INK,
                   length=0 if not grid else 3.5)


def blank(ax, xlim, ylim, step=1, equal=True, axes=True, grid=True):
    plain(ax, xlim, ylim, step, step, equal, axes, grid)
    ax.set_xticklabels([])
    ax.set_yticklabels([])


def arrow(ax, p, q, color=LINE, lw=2.4, z=6, ls="-", scale=15):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=scale,
                                 lw=lw, color=color, zorder=z,
                                 linestyle=ls, shrinkA=0, shrinkB=0))


def ang_of(v):
    return np.degrees(np.arctan2(v[1], v[0]))


def arc_between(ax, centre, u, w, r, color=GOLD, lw=2.0, z=7):
    """centre を頂点として、向き u から向き w までの弧を描く。"""
    a1, a2 = ang_of(u), ang_of(w)
    if (a2 - a1) % 360 > 180:
        a1, a2 = a2, a1
    ax.add_patch(Arc(centre, 2 * r, 2 * r, angle=0, theta1=a1, theta2=a2,
                     color=color, lw=lw, zorder=z))


def right_angle(ax, corner, u, w, s=0.42, color=GREY, lw=1.4, z=7):
    """corner に直角の四角い印を描く。u, w は単位ベクトルでなくてよい。"""
    u = np.array(u, float) / np.linalg.norm(u)
    w = np.array(w, float) / np.linalg.norm(w)
    p0 = np.array(corner, float)
    pts = [p0 + s * u, p0 + s * u + s * w, p0 + s * w]
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, lw=lw,
            zorder=z)


# ══════════ fig 1a: 2 本のベクトルと、そのあいだの角 ══════════
fig, ax = plt.subplots(figsize=(6.0, 4.8))
v = np.array([3.0, 4.0])
w = np.array([2.0, -5.0])
arrow(ax, (0, 0), v, color=LINE, lw=2.8)
arrow(ax, (0, 0), w, color=GREEN, lw=2.8)
arc_between(ax, (0, 0), v, w, 1.5)
ax.text(1.55, -0.35, r"$\theta \approx 121^{\circ}$", fontsize=13, color=GOLD,
        ha="left", va="center")
ax.text(3.2, 4.2, r"$\mathbf{v} = \binom{3}{4}$", fontsize=13, color=LINE,
        ha="left", va="bottom")
ax.text(2.2, -5.2, r"$\mathbf{w} = \binom{2}{-5}$", fontsize=13, color=GREEN,
        ha="left", va="top")
ax.plot([0], [0], "o", color=INK, ms=6, zorder=9)
ax.text(0.0, -7.4, r"$\mathbf{v}\cdot\mathbf{w} = 3(2)+4(-5) = -14$"
                   "\n"
                   r"$\cos\theta = \frac{-14}{5\sqrt{29}}$",
        fontsize=12.5, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
blank(ax, (-6.0, 6.0), (-9.4, 6.2), step=2)
ax.set_title("the angle is measured between the two arrows,\n"
             "both drawn from the same point",
             fontsize=12.5, color=INK, pad=6)
fig.tight_layout()
save(fig, "ahl-3-13a-idea.svg")


# ══════════ fig 1b: 符号が語ること（3 組を横に並べる） ══════════
fig, ax = plt.subplots(figsize=(6.4, 4.4))
cases = [
    (-3.9, [1.0, 0.0], [0.85, 0.95], ACC, r"$\mathbf{v}\cdot\mathbf{w} > 0$",
     "acute"),
    (0.0, [1.0, 0.0], [0.0, 1.30], GREEN, r"$\mathbf{v}\cdot\mathbf{w} = 0$",
     r"$90^{\circ}$"),
    (3.9, [1.0, 0.0], [-0.85, 0.95], LINE, r"$\mathbf{v}\cdot\mathbf{w} < 0$",
     "obtuse"),
]
for cx, a, b, col, lab, note in cases:
    a = np.array(a) * 1.75
    b = np.array(b) * 1.75
    c = np.array([cx - 0.5, -0.9])
    arrow(ax, c, c + a, color=GREY, lw=2.4)
    arrow(ax, c, c + b, color=col, lw=2.6)
    if note == r"$90^{\circ}$":
        right_angle(ax, c, a, b, s=0.40)
    else:
        arc_between(ax, c, a, b, 0.80, color=GOLD)
    ax.text(cx, -1.75, lab, fontsize=12.5, color=col, ha="center", va="top")
    ax.text(cx, -2.65, note, fontsize=11.5, color=INK, ha="center", va="top")
ax.text(0.0, 2.85, r"the sign of $\mathbf{v}\cdot\mathbf{w}$ tells you"
                  " the kind of angle\n"
                  r"(both vectors non-zero)",
        fontsize=12.5, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
blank(ax, (-5.9, 5.9), (-3.9, 3.9), step=1, axes=False, grid=False)
ax.set_title("reading the sign", fontsize=12.5, color=INK, pad=6)
fig.tight_layout()
save(fig, "ahl-3-13a-sign.svg")


# ══════════ fig 2: 2 直線のあいだの acute angle ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.8))

P = np.array([5.0, 4.0])          # 交点
d1 = np.array([2.0, 3.0])
d2 = np.array([-4.0, 1.0])

# ── (a) 2 本の直線と、2 つの角
ax = axs[0]
for d, col in [(d1, LINE), (d2, GREEN)]:
    ts = np.linspace(-2.4, 2.4, 2)
    ax.plot(P[0] + ts * d[0], P[1] + ts * d[1], color=col, lw=2.6, zorder=5)
arc_between(ax, P, d1, d2, 2.0, color=GOLD)
arc_between(ax, P, -d1, d2, 1.25, color=ACC)
ax.text(3.05, 6.55, r"$109.7^{\circ}$", fontsize=12.5, color=GOLD, ha="right",
        va="center")
ax.text(3.15, 2.95, r"$70.3^{\circ}$", fontsize=12.5, color=ACC, ha="right",
        va="center")
ax.plot([P[0]], [P[1]], "o", color=INK, ms=7, zorder=9)
ax.text(10.3, 11.0, r"$L_1$", fontsize=13, color=LINE, ha="left", va="center")
ax.text(-5.1, 6.6, r"$L_2$", fontsize=13, color=GREEN, ha="right", va="center")
ax.text(3.4, -3.4, "two lines make two angles;\n"
                   "the answer wanted is the acute one",
        fontsize=12.5, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
blank(ax, (-7.5, 13.0), (-5.6, 12.6), step=2, axes=False)
ax.set_title("(a)  the two lines", fontsize=12.5, color=INK, pad=6)

# ── (b) 方向ベクトルだけを、同じ点から
ax = axs[1]
arrow(ax, (0, 0), d1, color=LINE, lw=2.8)
arrow(ax, (0, 0), d2, color=GREEN, lw=2.8)
arrow(ax, (0, 0), -d1, color=LINE, lw=2.2, ls=(0, (5, 3)))
arc_between(ax, (0, 0), d1, d2, 1.5, color=GOLD)
arc_between(ax, (0, 0), -d1, d2, 0.95, color=ACC)
ax.text(-0.30, 1.75, r"$109.7^{\circ}$", fontsize=12.5, color=GOLD, ha="right",
        va="bottom")
ax.text(-1.75, -0.65, r"$70.3^{\circ}$", fontsize=12.5, color=ACC, ha="right",
        va="top")
ax.text(2.15, 3.05, r"$\mathbf{d}_1 = \binom{2}{3}$", fontsize=12.5,
        color=LINE, ha="left", va="bottom")
ax.text(-4.15, 1.25, r"$\mathbf{d}_2 = \binom{-4}{1}$", fontsize=12.5,
        color=GREEN, ha="right", va="bottom")
ax.text(-1.85, -3.35, r"$-\mathbf{d}_1$", fontsize=12.5, color=LINE,
        ha="right", va="center")
ax.text(0.6, -5.9, r"$\mathbf{d}_1$ and $-\mathbf{d}_1$ give the same line."
                   "\n"
                   r"$\cos\theta = \frac{-5}{\sqrt{221}}$ gives"
                   r" $109.7^{\circ}$;" " the acute angle is\n"
                   r"$180^{\circ}-109.7^{\circ} = 70.3^{\circ}$"
                   " (do not round to $110^{\circ}$ first)",
        fontsize=12, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
blank(ax, (-6.8, 6.8), (-8.4, 5.2), step=1, axes=False)
ax.set_title("(b)  the direction vectors, drawn from one point",
             fontsize=12.5, color=INK, pad=6)

fig.tight_layout(w_pad=2.2)
save(fig, "ahl-3-13a-lines.svg")


# ══════════ fig 3: b の向きの成分 ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.8))


def component_panel(ax, a, b, comp_text, note, xlim, ylim, step, title,
                    off=1.15, lab_side=1.0, alab=(0.25, 0.25),
                    blab=(0.25, 0.25), lab_off=0.85, olab=(-0.30, "right")):
    """a を b の向きに落とす図。成分は b の線から少し離した
       寸法線として描く（b の矢印を隠さないため）。"""
    a = np.array(a, float)
    b = np.array(b, float)
    bh = b / np.linalg.norm(b)
    nh = np.array([-bh[1], bh[0]]) * lab_side      # b に垂直な向き
    foot = float(a @ bh) * bh

    ts = np.linspace(-1.6, 2.0, 2)
    ax.plot(ts * b[0], ts * b[1], color=GREY, lw=1.4, ls=(0, (6, 4)), zorder=3)
    arrow(ax, (0, 0), b, color=GREEN, lw=2.8)
    arrow(ax, (0, 0), a, color=LINE, lw=2.8)
    ax.plot([a[0], foot[0]], [a[1], foot[1]], color=GREY, lw=1.6, ls=":",
            zorder=4)
    right_angle(ax, foot, a - foot, -bh, s=0.40)
    ax.plot([foot[0]], [foot[1]], "o", color=ACC, ms=7, zorder=9)

    # 寸法線（b の線から off だけ離す）
    p0, p1 = off * nh, foot + off * nh
    for base, tip in [((0, 0), p0), (foot, p1)]:
        ax.plot([base[0], tip[0]], [base[1], tip[1]], color=ACC, lw=1.0,
                ls=":", zorder=5)
    arrow(ax, p0, p1, color=ACC, lw=2.6, z=7, scale=13)
    mid = 0.5 * (p0 + p1) + lab_off * nh
    ax.text(mid[0], mid[1], comp_text, fontsize=13, color=ACC, ha="center",
            va="center")
    ax.plot([0], [0], "o", color=INK, ms=6, zorder=9)
    ax.text(olab[0], -0.30, "$O$", fontsize=12, color=INK, ha=olab[1],
            va="top")

    ax.text(a[0] + alab[0], a[1] + alab[1], r"$\mathbf{a}$", fontsize=14,
            color=LINE, ha="left", va="bottom")
    ax.text(b[0] + blab[0], b[1] + blab[1], r"$\mathbf{b}$", fontsize=14,
            color=GREEN, ha="left", va="bottom")
    ax.text(*note[:2], note[2], fontsize=12, color=INK, ha="center",
            va="center", bbox=BOX, zorder=10)
    blank(ax, xlim, ylim, step=step, axes=False)
    ax.set_title(title, fontsize=12.5, color=INK, pad=6)


component_panel(
    axs[0], (-1, 6), (4, 3),
    r"$2.8$",
    (2.2, -3.9, r"$\mathbf{a}\cdot\mathbf{b} = 14$,  $|\mathbf{b}| = 5$"
                "\n"
                r"component $= \frac{14}{5} = 2.8$  (positive)"),
    (-3.0, 9.5), (-5.6, 8.2), 1,
    "(a)  acute angle: the shadow points along $\\mathbf{b}$",
    off=1.15, lab_side=-1.0, blab=(0.1, -0.9))

component_panel(
    axs[1], (4, 7), (3, -4),
    r"$-3.2$",
    (1.0, -7.6, r"$\mathbf{a}\cdot\mathbf{b} = -16$,  $|\mathbf{b}| = 5$"
                "\n"
                r"component $= \frac{-16}{5} = -3.2$  (negative)"),
    (-6.2, 8.0), (-9.4, 8.6), 1,
    "(b)  obtuse angle: the shadow points the other way",
    off=1.25, lab_side=-1.0, blab=(0.25, -0.9), lab_off=1.45,
    olab=(0.35, "left"))

fig.tight_layout(w_pad=2.2)
save(fig, "ahl-3-13a-component.svg")

print("figures written to", os.path.normpath(OUT))
