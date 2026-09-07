"""AHL 3.13b（vector product）の図を作る。ラベルは英語。
   出力先: ai-hl/03-geometry-and-trigonometry/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_3_13b.py

   ★ matplotlib の mathtext は \\begin{pmatrix} も \\lvert も読めません。
      縦ベクトルは \\binom、絶対値は | を使います。
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Arc, Polygon
from mpl_toolkits.mplot3d.proj3d import proj_transform
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from _graph import INK, GRID, LINE, ACC, GREEN, GREY, GOLD, BOX, FILL

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "03-geometry-and-trigonometry", "img")
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True)
    plt.close(fig)
    print("wrote", name)


# ── 2 次元用の下ごしらえ ────────────────────────────────
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
    ax.tick_params(labelsize=10, colors=INK, length=3.5 if grid else 0)


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
    a1, a2 = ang_of(u), ang_of(w)
    if (a2 - a1) % 360 > 180:
        a1, a2 = a2, a1
    ax.add_patch(Arc(centre, 2 * r, 2 * r, angle=0, theta1=a1, theta2=a2,
                     color=color, lw=lw, zorder=z))


def right_angle(ax, corner, u, w, s=0.35, color=GREY, lw=1.4, z=7):
    u = np.array(u, float) / np.linalg.norm(u)
    w = np.array(w, float) / np.linalg.norm(w)
    p0 = np.array(corner, float)
    pts = [p0 + s * u, p0 + s * u + s * w, p0 + s * w]
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, lw=lw,
            zorder=z)


# ── 3 次元用の下ごしらえ ────────────────────────────────
def arrow3(ax, p, q, color=LINE, lw=2.6, z=6):
    p, q = np.array(p, float), np.array(q, float)
    d = q - p
    ax.quiver(p[0], p[1], p[2], d[0], d[1], d[2], color=color, lw=lw,
              arrow_length_ratio=0.16, zorder=z)


def text3(ax, p, s, color=INK, fontsize=13, ha="left", va="bottom", z=12):
    ax.text(p[0], p[1], p[2], s, color=color, fontsize=fontsize, ha=ha,
            va=va, zorder=z)


def frame3(ax, elev=20, azim=-60, zlim=(-3.4, 3.4)):
    """v と w が乗る平面を薄く敷いた、軸のない 3 次元の枠。
       座標軸は描かない（矢印と重なって読みにくくなるため）。"""
    ax.set_xlim(-1.6, 4.4)
    ax.set_ylim(-1.6, 4.4)
    ax.set_zlim(*zlim)
    try:
        ax.set_box_aspect((1, 1, 0.95), zoom=1.45)
    except TypeError:                       # 古い matplotlib
        ax.set_box_aspect((1, 1, 0.95))
    ax.view_init(elev=elev, azim=azim)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_axis_off()
    floor = [[(-1.4, -1.4, 0), (4.2, -1.4, 0), (4.2, 4.2, 0),
              (-1.4, 4.2, 0)]]
    ax.add_collection3d(Poly3DCollection(floor, facecolor=FILL,
                                         edgecolor=GRID, lw=0.8, alpha=0.25,
                                         zorder=0))


# ══════════ fig 1: v x w は、両方に垂直 ══════════
V = np.array([3.0, 0.0, 0.0])
W = np.array([1.0, 2.0, 0.0])
CR = np.cross(V, W)                      # (0, 0, 6)
SC = 0.45                                # 上向き矢印の縮尺（6 → 2.7）

fig = plt.figure(figsize=(11.4, 4.6))

for k, (cross, title, note) in enumerate([
        (CR, "(a)  $\\mathbf{v}\\times\\mathbf{w}$ points one way",
         "$\\mathbf{v} = \\binom{3}{0}$ and $\\mathbf{w} = \\binom{1}{2}$ in the"
         " plane (third component $0$).\n"
         "Right hand: fingers turn from $\\mathbf{v}$ to $\\mathbf{w}$, thumb"
         " gives $\\mathbf{v}\\times\\mathbf{w}$, at right angles to both\n"
         "(the upright arrow is drawn shorter than its true length)."),
        (-CR, "(b)  $\\mathbf{w}\\times\\mathbf{v}$ points the other way",
         "Turning from $\\mathbf{w}$ to $\\mathbf{v}$ instead points the thumb"
         " down.\n"
         "Same length, opposite direction:"
         " $\\mathbf{w}\\times\\mathbf{v} = -(\\mathbf{v}\\times\\mathbf{w})$.")]):
    ax = fig.add_subplot(1, 2, k + 1, projection="3d")
    frame3(ax)
    text3(ax, (-1.3, -1.2, 0), "the plane of\n$\\mathbf{v}$ and $\\mathbf{w}$",
          color=GREY, fontsize=10.5, ha="center", va="center")
    # v と w が張る平行四辺形は、塗らずに破線の 2 辺だけで示す
    # （塗ると、その下の矢印の色が薄く見えてしまうため）
    for p, q in [(V, V + W), (W, V + W)]:
        ax.plot([p[0], q[0]], [p[1], q[1]], [p[2], q[2]], color=GOLD,
                lw=1.4, ls=(0, (5, 4)), zorder=1)
    # 平行四辺形の塗りに埋もれないよう、面よりわずかに上に描く
    UP = np.array([0.0, 0.0, 0.06])
    arrow3(ax, UP, V + UP, color=LINE, lw=3.0)
    arrow3(ax, UP, W + UP, color=GREEN, lw=3.0)
    arrow3(ax, (0, 0, 0), cross * SC, color=ACC, lw=3.0)
    text3(ax, V + np.array([0.35, -0.55, 0.0]), "$\\mathbf{v}$", color=LINE,
          fontsize=15)
    text3(ax, W + np.array([-0.15, 0.55, 0.0]), "$\\mathbf{w}$", color=GREEN,
          fontsize=15, ha="right")
    lab = ("$\\mathbf{v}\\times\\mathbf{w}$" if k == 0
           else "$\\mathbf{w}\\times\\mathbf{v}$")
    text3(ax, cross * SC + np.array([0.2, 0.2, 0.35 if k == 0 else -0.55]),
          lab, color=ACC, fontsize=14)
    ax.set_title(title, fontsize=12.5, color=INK, pad=2)
    # 説明は 2 次元の座標で置く（3 次元だと位置が読みにくいため）
    ax.text2D(0.5, -0.02, note, transform=ax.transAxes, fontsize=11.5,
              color=INK, ha="center", va="top", bbox=BOX, zorder=20)

fig.subplots_adjust(left=0.0, right=1.0, top=0.99, bottom=0.20,
                    wspace=0.0)
save(fig, "ahl-3-13b-idea.svg")


# ══════════ fig 2: |v x w| は平行四辺形の面積 ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.6))

v2 = np.array([3.0, 0.0])
w2 = np.array([1.0, 2.0])

# ── (a) 平行四辺形
ax = axs[0]
ax.add_patch(Polygon([(0, 0), tuple(v2), tuple(v2 + w2), tuple(w2)],
                     closed=True, facecolor=GOLD, alpha=0.16,
                     edgecolor=GOLD, lw=1.6, zorder=2))
arrow(ax, (0, 0), v2, color=LINE, lw=2.8)
arrow(ax, (0, 0), w2, color=GREEN, lw=2.8)
ax.plot([w2[0], w2[0]], [0, w2[1]], color=ACC, lw=2.0, ls=":", zorder=5)
right_angle(ax, (w2[0], 0), (1, 0), (0, 1), s=0.22, color=ACC)
ax.text(w2[0] + 0.16, w2[1] / 2, "height\n$=|\\mathbf{w}|\\sin\\theta = 2$",
        fontsize=11.5, color=ACC, ha="left", va="center")
arc_between(ax, (0, 0), v2, w2, 0.75)
ax.text(0.95, 0.30, "$\\theta$", fontsize=13, color=GOLD, ha="left",
        va="bottom")
ax.text(1.5, -0.30, "base $=|\\mathbf{v}| = 3$", fontsize=11.5, color=LINE,
        ha="center", va="top")
ax.text(3.25, 2.1, "$\\mathbf{v} = \\binom{3}{0}$,  "
                   "$\\mathbf{w} = \\binom{1}{2}$", fontsize=12, color=INK,
        ha="left", va="center")
ax.text(2.0, -1.5, "$A = $ base $\\times$ height $= |\\mathbf{v}||\\mathbf{w}|"
                   "\\sin\\theta = |\\mathbf{v}\\times\\mathbf{w}| = 6$",
        fontsize=12, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
blank(ax, (-1.2, 6.4), (-2.6, 3.6), step=1, axes=False)
ax.set_title("(a)  the parallelogram", fontsize=12.5, color=INK, pad=6)

# ── (b) 三角形は、その半分
ax = axs[1]
ax.add_patch(Polygon([tuple(v2), tuple(v2 + w2), tuple(w2)], closed=True,
                     facecolor=GREY, alpha=0.10, edgecolor="none", zorder=2))
ax.add_patch(Polygon([(0, 0), tuple(v2), tuple(v2 + w2), tuple(w2)],
                     closed=True, facecolor="none", edgecolor=GREY, lw=1.2,
                     ls=(0, (5, 4)), zorder=3))
ax.add_patch(Polygon([(0, 0), tuple(v2), tuple(w2)], closed=True,
                     facecolor=GOLD, alpha=0.22, edgecolor=GOLD, lw=1.8,
                     zorder=3))
arrow(ax, (0, 0), v2, color=LINE, lw=2.8)
arrow(ax, (0, 0), w2, color=GREEN, lw=2.8)
ax.plot([v2[0], w2[0]], [v2[1], w2[1]], color=GOLD, lw=1.8, zorder=4)
ax.text(1.25, 0.62, "half", fontsize=12.5, color=GOLD, ha="center",
        va="center")
ax.text(2.67, 1.33, "the other\nhalf", fontsize=11.5, color=GREY,
        ha="center", va="center")
ax.text(2.0, -1.5, "triangle $= \\frac{1}{2}|\\mathbf{v}\\times\\mathbf{w}|"
                   " = 3$",
        fontsize=12, color=INK, ha="center", va="center", bbox=BOX, zorder=9)
blank(ax, (-1.2, 6.4), (-2.6, 3.6), step=1, axes=False)
ax.set_title("(b)  the triangle is half of it", fontsize=12.5, color=INK,
             pad=6)

fig.tight_layout(w_pad=2.0)
save(fig, "ahl-3-13b-area.svg")


# ══════════ fig 3: b に平行な成分と、垂直な成分 ══════════
fig, ax = plt.subplots(figsize=(8.6, 5.0))

a3 = np.array([-1.0, 6.0])
b3 = np.array([4.0, 3.0])
bh = b3 / np.linalg.norm(b3)
foot = float(a3 @ bh) * bh                 # 5.2 * b^

ts = np.linspace(-0.6, 1.75, 2)
ax.plot(ts * b3[0], ts * b3[1], color=GREY, lw=1.4, ls=(0, (6, 4)), zorder=3)
ax.add_patch(Polygon([(0, 0), tuple(foot), tuple(a3)], closed=True,
                     facecolor=GOLD, alpha=0.13, edgecolor="none", zorder=2))
arrow(ax, (0, 0), b3, color=GREEN, lw=2.8)
arrow(ax, (0, 0), a3, color=LINE, lw=2.8)
ax.plot([a3[0], foot[0]], [a3[1], foot[1]], color=ACC, lw=2.4, zorder=5)
right_angle(ax, foot, a3 - foot, -bh, s=0.34)
ax.plot([foot[0]], [foot[1]], "o", color=ACC, ms=7, zorder=9)
ax.plot([0], [0], "o", color=INK, ms=6, zorder=9)

nh = np.array([-bh[1], bh[0]])            # b に垂直な単位ベクトル
p0, p1 = -1.15 * nh, foot - 1.15 * nh
for base, tip in [((0, 0), p0), (tuple(foot), tuple(p1))]:
    ax.plot([base[0], tip[0]], [base[1], tip[1]], color=GREY, lw=1.0, ls=":",
            zorder=4)
arrow(ax, p0, p1, color=GREY, lw=2.2, z=7, scale=13)
mid = 0.5 * (p0 + p1) - 0.95 * nh
ax.text(mid[0], mid[1], "$\\frac{\\mathbf{a}\\cdot\\mathbf{b}}"
                        "{|\\mathbf{b}|} = 2.8$", fontsize=12.5, color=GREY,
        ha="center", va="center")

ax.text(0.5 * (a3[0] + foot[0]) + 0.30, 0.5 * (a3[1] + foot[1]) + 0.35,
        "$\\frac{|\\mathbf{a}\\times\\mathbf{b}|}{|\\mathbf{b}|} = 5.4$",
        fontsize=12.5, color=ACC, ha="left", va="bottom")
ax.text(a3[0] - 0.25, a3[1] + 0.25, "$\\mathbf{a} = \\binom{-1}{6}$",
        fontsize=13, color=LINE, ha="right", va="bottom")
ax.text(b3[0] + 0.10, b3[1] - 0.55, "$\\mathbf{b} = \\binom{4}{3}$",
        fontsize=13, color=GREEN, ha="left", va="top")
ax.text(-0.30, -0.30, "$O$", fontsize=12, color=INK, ha="right", va="top")
ax.text(3.0, -2.6, "the two parts make a right-angled triangle:\n"
                   "$2.8^2 + 5.4^2 = 37 = |\\mathbf{a}|^2$",
        fontsize=12, color=INK, ha="center", va="center", bbox=BOX, zorder=10)
blank(ax, (-3.0, 9.0), (-4.0, 7.6), step=1, axes=False)
ax.set_title("$\\mathbf{a}$ splits into a part along $\\mathbf{b}$\n"
             "and a part at right angles to $\\mathbf{b}$",
             fontsize=12.5, color=INK, pad=8)

fig.tight_layout()
save(fig, "ahl-3-13b-component.svg")

print("figures written to", os.path.normpath(OUT))
