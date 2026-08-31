"""AHL 3.9 の図を作る。ラベルはすべて英語（数式は共通）。
   出力先: ai-hl/03-geometry-and-trigonometry/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_3_9.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch, Arc
from _matrix import (INK, GRID, LINE, ACC, GREEN, GREY, GOLD, FILL, BOX,
                     blank, matrix, label, arrow)

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "03-geometry-and-trigonometry", "img")
os.makedirs(OUT, exist_ok=True)

PALE = "#fdece9"          # 像（image）のうすい塗り


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True)
    plt.close(fig)


def plane(ax, xlim, ylim, step=1, ticks=True, tick_step=None):
    """方眼と座標軸。"""
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    for x in np.arange(np.ceil(xlim[0] / step) * step, xlim[1] + 1e-9, step):
        ax.axvline(x, color=GRID, lw=0.7, zorder=0)
    for y in np.arange(np.ceil(ylim[0] / step) * step, ylim[1] + 1e-9, step):
        ax.axhline(y, color=GRID, lw=0.7, zorder=0)
    ax.axhline(0, color=GREY, lw=1.3, zorder=1)
    ax.axvline(0, color=GREY, lw=1.3, zorder=1)
    ts = tick_step or (step if (xlim[1] - xlim[0]) <= 12 else 2 * step)
    if ticks:
        for x in np.arange(np.ceil(xlim[0] / ts) * ts, xlim[1] + 1e-9, ts):
            if abs(x) > 1e-9:
                ax.text(x, -0.16 * ts, f"{x:g}", fontsize=8.5, color=GREY,
                        ha="center", va="top", zorder=2)
        for y in np.arange(np.ceil(ylim[0] / ts) * ts, ylim[1] + 1e-9, ts):
            if abs(y) > 1e-9:
                ax.text(-0.14 * ts, y, f"{y:g}", fontsize=8.5, color=GREY,
                        ha="right", va="center", zorder=2)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])


def shape(ax, pts, color=LINE, fc=FILL, lw=2.2, z=4, alpha=1.0, ls="-"):
    ax.add_patch(Polygon(np.array(pts), closed=True, fc=fc, ec=color, lw=lw,
                         zorder=z, alpha=alpha, linestyle=ls))


def dot(ax, p, color=INK, ms=7, z=9):
    ax.plot([p[0]], [p[1]], "o", color=color, ms=ms, zorder=z)


def tag(ax, p, text, color=INK, dx=0.22, dy=0.22, fs=11.5, ha="left",
        va="bottom"):
    ax.text(p[0] + dx, p[1] + dy, text, fontsize=fs, color=color, ha=ha,
            va=va, zorder=11, bbox=BOX)


def apply(M, pts, t=(0, 0)):
    A = np.array(M, dtype=float)
    return [tuple(A @ np.array(p, dtype=float) + np.array(t, dtype=float))
            for p in pts]


def curved(ax, p, q, color=GOLD, rad=0.28, lw=1.7):
    ax.add_patch(FancyArrowPatch(p, q, connectionstyle=f"arc3,rad={rad}",
                                 arrowstyle="-|>", mutation_scale=14,
                                 color=color, lw=lw, zorder=8))


FSHAPE = [(0, 0), (1, 0), (1, 2), (2, 2), (2, 3), (1, 3), (1, 4), (3, 4),
          (3, 5), (0, 5)]

# ══════════════ 1. The idea：object と image ══════════════
fig, axes_ = plt.subplots(1, 2, figsize=(9.6, 4.3))
tri = [(0, 0), (4, 0), (0, 2)]
Mid = [[3, 1], [1, 2]]
img = apply(Mid, tri)

plane(axes_[0], (-1.2, 5.6), (-1.2, 5.6))
shape(axes_[0], tri, LINE, FILL)
for p, nm in zip(tri, ["O", "A", "B"]):
    dot(axes_[0], p)
    tag(axes_[0], p, nm)
axes_[0].set_title("object", fontsize=13, color=LINE, pad=8)

plane(axes_[1], (-1.2, 14.5), (-1.2, 9.5), step=2, tick_step=2)
shape(axes_[1], img, ACC, PALE)
for p, nm in zip(img, ["O'", "A'", "B'"]):
    dot(axes_[1], p, ACC)
    tag(axes_[1], p, nm, ACC, dx=0.35, dy=0.35)
axes_[1].set_title("image", fontsize=13, color=ACC, pad=8)
fig.text(0.5, 0.03, "every point is multiplied by the same "
                    "$2 \\times 2$ matrix", fontsize=13, ha="center",
         color=INK)
fig.tight_layout(rect=(0, 0.06, 1, 1))
save(fig, "ahl-3-9-idea.svg")

# ══════════════ 2. Why it works：列は i と j の行き先 ══════════════
fig, ax = plt.subplots(figsize=(7.6, 5.4))
plane(ax, (-0.9, 5.4), (-0.9, 4.4))
sq = [(0, 0), (1, 0), (1, 1), (0, 1)]
shape(ax, sq, LINE, FILL)
par = apply(Mid, sq)
shape(ax, par, ACC, PALE)

for v, col, nm in (((1, 0), LINE, "i"), ((0, 1), LINE, "j")):
    ax.add_patch(FancyArrowPatch((0, 0), v, arrowstyle="-|>",
                                 mutation_scale=15, color=col, lw=2.6,
                                 zorder=7))
ax.text(0.52, -0.30, "$i$", fontsize=13, color=LINE, ha="center", va="top")
ax.text(-0.20, 0.52, "$j$", fontsize=13, color=LINE, ha="right", va="center")

for v, nm, dx, dy in (((3, 1), "first column $(3,1)$", 0.25, 0.10),
                      ((1, 2), "second column $(1,2)$", 0.25, 0.20)):
    ax.add_patch(FancyArrowPatch((0, 0), v, arrowstyle="-|>",
                                 mutation_scale=15, color=ACC, lw=2.6,
                                 zorder=7))
    ax.text(v[0] + dx, v[1] + dy, nm, fontsize=11.5, color=ACC, ha="left",
            va="bottom", zorder=11, bbox=BOX)

ax.text(0.42, 3.85, "the unit square goes to the parallelogram\n"
                    "made by the two columns", fontsize=11.5, color=INK,
        ha="left", va="center", zorder=11, bbox=BOX)
fig.tight_layout()
save(fig, "ahl-3-9-columns.svg")

# ══════════════ 3. 公式集の 6 つ ══════════════
SIX = [
    ("reflection in $y=x$", [[0, 1], [1, 0]]),
    ("horizontal stretch, $k=2$", [[2, 0], [0, 1]]),
    ("vertical stretch, $k=2$", [[1, 0], [0, 2]]),
    ("enlargement, $k=2$", [[2, 0], [0, 2]]),
    ("rotation $90^\\circ$ anticlockwise", [[0, -1], [1, 0]]),
    ("rotation $90^\\circ$ clockwise", [[0, 1], [-1, 0]]),
]
small = [(0.4 * x, 0.4 * y) for x, y in FSHAPE]      # 小さな F の形

fig, axs = plt.subplots(2, 3, figsize=(11.4, 7.6))
for ax, (name, Mx) in zip(axs.ravel(), SIX):
    im_ = apply(Mx, small)
    xs = [p[0] for p in small + im_]
    ys = [p[1] for p in small + im_]
    r = max(max(map(abs, xs)), max(map(abs, ys))) + 0.9
    plane(ax, (-r, r), (-r, r), ticks=False)
    if name.startswith("reflection"):
        ax.plot([-r * 0.96, r * 0.96], [-r * 0.96, r * 0.96], color=GOLD,
                lw=1.5, ls=(0, (5, 4)), zorder=2)
    shape(ax, im_, ACC, PALE, lw=2.0)
    shape(ax, small, LINE, "none", lw=1.7, ls=(0, (4, 3)), z=6)
    ax.set_title(name, fontsize=11.5, color=INK, pad=6)
fig.text(0.5, 0.015, "dashed blue = object,   solid red = image",
         fontsize=11.5, ha="center", color=GREY)
fig.tight_layout(rect=(0, 0.035, 1, 1))
save(fig, "ahl-3-9-six.svg")

# ══════════════ 4. translation は行列だけでは書けない ══════════════
fig, axs = plt.subplots(1, 2, figsize=(10.0, 4.6))
plane(axs[0], (-2.8, 3.2), (-1.6, 3.4))
shape(axs[0], apply([[0, -1], [1, 0]], small), ACC, PALE, lw=2.0)
shape(axs[0], small, LINE, "none", lw=1.7, ls=(0, (4, 3)), z=6)
dot(axs[0], (0, 0), ACC, ms=8)
axs[0].text(0.28, -1.05, "the origin never moves", fontsize=11.5, color=ACC,
            ha="left", va="center", zorder=11, bbox=BOX)
axs[0].set_title("a matrix on its own", fontsize=12.5, color=INK, pad=8)

plane(axs[1], (-1.4, 5.0), (-1.6, 3.4))
shape(axs[1], small, LINE, FILL, lw=2.0)
mv = apply([[1, 0], [0, 1]], small, t=(3, 1))
shape(axs[1], mv, GREEN, "#e9f6ee", lw=2.0)
curved(axs[1], (1.0, 1.0), (3.9, 2.0), GREEN, rad=-0.25)
axs[1].text(0.9, 3.0, "add $(3,1)$ to every point", fontsize=11.5,
            color=GREEN, ha="left", va="center", zorder=11, bbox=BOX)
axs[1].set_title("translation", fontsize=12.5, color=GREEN, pad=8)
fig.tight_layout()
save(fig, "ahl-3-9-translation.svg")

# ══════════════ 5. 図形は頂点を並べて 1 つの行列に ══════════════
fig, ax = plt.subplots(figsize=(8.2, 3.1))
blank(ax, (0, 8.2), (0, 3.1))
ax.set_aspect("auto")
matrix(ax, 1.5, 1.55, [["0", "-1"], ["1", "0"]], cw=0.62, ch=0.5, color=ACC)
matrix(ax, 3.5, 1.55, [["1", "4", "1"], ["1", "1", "3"]], cw=0.62, ch=0.5,
       color=LINE)
label(ax, 4.85, 1.55, "$=$", fs=15)
matrix(ax, 6.3, 1.55, [["-1", "-1", "-3"], ["1", "4", "1"]], cw=0.72, ch=0.5,
       color=GREEN)
label(ax, 1.5, 2.62, "transformation", color=ACC, fs=11.5)
label(ax, 3.5, 2.62, "$A$    $B$    $C$", color=LINE, fs=11.5)
label(ax, 6.3, 2.62, "$A'$    $B'$    $C'$", color=GREEN, fs=11.5)
label(ax, 3.5, 0.48, "one column for each vertex", color=GREY, fs=11)
fig.tight_layout()
save(fig, "ahl-3-9-shape.svg")

# ══════════════ 6. 合成は順番が大事 ══════════════
Prefl = [[1, 0], [0, -1]]
Q90 = [[0, -1], [1, 0]]
fig, axs = plt.subplots(1, 3, figsize=(11.6, 4.3))
plane(axs[0], (-5.4, 5.4), (-5.4, 5.4), ticks=False)
shape(axs[0], FSHAPE, LINE, FILL, lw=1.9)
axs[0].set_title("object", fontsize=12.5, color=LINE, pad=6)

plane(axs[1], (-5.4, 5.4), (-5.4, 5.4), ticks=False)
shape(axs[1], FSHAPE, GREY, "none", lw=1.2, ls=(0, (4, 3)))
shape(axs[1], apply(np.array(Q90) @ np.array(Prefl), FSHAPE), ACC, PALE,
      lw=1.9)
axs[1].plot([-5.2, 5.2], [-5.2, 5.2], color=GOLD, lw=1.4, ls=(0, (5, 4)),
            zorder=2)
axs[1].set_title("$QP$ : reflect first, then rotate", fontsize=11.5,
                 color=ACC, pad=6)

plane(axs[2], (-5.4, 5.4), (-5.4, 5.4), ticks=False)
shape(axs[2], FSHAPE, GREY, "none", lw=1.2, ls=(0, (4, 3)))
shape(axs[2], apply(np.array(Prefl) @ np.array(Q90), FSHAPE), GREEN,
      "#e9f6ee", lw=1.9)
axs[2].plot([-5.2, 5.2], [5.2, -5.2], color=GOLD, lw=1.4, ls=(0, (5, 4)),
            zorder=2)
axs[2].set_title("$PQ$ : rotate first, then reflect", fontsize=11.5,
                 color=GREEN, pad=6)
fig.tight_layout()
save(fig, "ahl-3-9-compose.svg")

# ══════════════ 7. determinant と面積 ══════════════
fig, axs = plt.subplots(1, 2, figsize=(9.8, 4.4))
plane(axs[0], (-1.2, 5.4), (-1.2, 3.4))
shape(axs[0], tri, LINE, FILL)
axs[0].text(1.0, 0.55, "area $=4$", fontsize=12, color=LINE, ha="center",
            va="center", zorder=11, bbox=BOX)
axs[0].set_title("object", fontsize=12.5, color=LINE, pad=8)

plane(axs[1], (-1.6, 14.5), (-1.6, 9.5), step=2, tick_step=2)
shape(axs[1], img, ACC, PALE)
axs[1].text(4.6, 2.6, "area $=20$", fontsize=12, color=ACC, ha="center",
            va="center", zorder=11, bbox=BOX)
axs[1].set_title("image", fontsize=12.5, color=ACC, pad=8)
fig.text(0.5, 0.03, r"$\det A = 5$,   so   $20 = 5 \times 4$", fontsize=13,
         ha="center", color=INK)
fig.tight_layout(rect=(0, 0.06, 1, 1))
save(fig, "ahl-3-9-det.svg")

# ══════════════ 8. Sierpinski triangle ══════════════
def sierp(pts, n):
    if n == 0:
        return [pts]
    (ax_, ay), (bx, by), (cx, cy) = pts
    ab = ((ax_ + bx) / 2, (ay + by) / 2)
    bc = ((bx + cx) / 2, (by + cy) / 2)
    ca = ((cx + ax_) / 2, (cy + ay) / 2)
    out = []
    for sub in (((ax_, ay), ab, ca), (ab, (bx, by), bc), (ca, bc, (cx, cy))):
        out += sierp(sub, n - 1)
    return out


base = [(0, 0), (4, 0), (2, 3.464)]
fig, axs = plt.subplots(1, 4, figsize=(12.0, 3.4))
for k, ax in enumerate(axs):
    ax.set_xlim(-0.35, 4.35)
    ax.set_ylim(-0.35, 3.85)
    ax.set_aspect("equal")
    ax.axis("off")
    for t3 in sierp(base, k):
        ax.add_patch(Polygon(np.array(t3), closed=True, fc=FILL, ec=LINE,
                             lw=1.1))
    ax.set_title(f"stage {k}", fontsize=11.5, color=INK, pad=4)
    ax.text(2.0, -0.30, "area $=A$" if k == 0 else
            f"area $= \\left(\\frac{{3}}{{4}}\\right)^{{{k}}}A$",
            fontsize=11.5, color=ACC, ha="center", va="top")
fig.tight_layout()
save(fig, "ahl-3-9-sierpinski.svg")

# ══════════════ 9. Koch snowflake ══════════════
def koch(p, q, n):
    p, q = np.array(p, float), np.array(q, float)
    if n == 0:
        return [p]
    d = (q - p) / 3.0
    a = p + d
    b = p + 2 * d
    ang = np.radians(-60)
    R = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
    peak = a + R @ d
    return koch(p, a, n - 1) + koch(a, peak, n - 1) + \
        koch(peak, b, n - 1) + koch(b, q, n - 1)


tri0 = [np.array([0, 0]), np.array([4, 0]), np.array([2, 3.464])]
fig, axs = plt.subplots(1, 4, figsize=(12.0, 3.4))
for k, ax in enumerate(axs):
    ax.set_xlim(-1.0, 5.0)
    ax.set_ylim(-1.5, 4.4)
    ax.set_aspect("equal")
    ax.axis("off")
    pts = []
    for i in range(3):
        pts += koch(tri0[i], tri0[(i + 1) % 3], k)
    ax.add_patch(Polygon(np.array(pts), closed=True, fc=FILL, ec=LINE,
                         lw=1.1))
    ax.set_title(f"stage {k}", fontsize=11.5, color=INK, pad=4)
    ax.text(2.0, -1.35, "perimeter $=P$" if k == 0 else
            f"perimeter $= \\left(\\frac{{4}}{{3}}\\right)^{{{k}}}P$",
            fontsize=11.5, color=ACC, ha="center", va="bottom")
fig.tight_layout()
save(fig, "ahl-3-9-koch.svg")

# ══════════════ 例題1 ══════════════
fig, ax = plt.subplots(figsize=(6.6, 5.0))
plane(ax, (-3.6, 5.4), (-1.4, 5.4))
dot(ax, (4, 2), LINE)
tag(ax, (4, 2), "$P(4,2)$", LINE)
dot(ax, (-2, 4), ACC)
tag(ax, (-2, 4), "$P'$", ACC, dx=-0.30, ha="right")
ax.plot([0, 4], [0, 2], color=LINE, lw=1.6, ls=(0, (5, 4)), zorder=3)
ax.plot([0, -2], [0, 4], color=ACC, lw=1.6, ls=(0, (5, 4)), zorder=3)
ax.add_patch(Arc((0, 0), 4.4, 4.4, angle=0, theta1=26.6, theta2=116.6,
                 color=GOLD, lw=1.8, zorder=6))
ax.text(1.3, 3.4, "$90^\\circ$", fontsize=12.5, color=GOLD, ha="center",
        va="center", zorder=11, bbox=BOX)
fig.tight_layout()
save(fig, "ahl-3-9-we1.svg")

# ══════════════ 例題2 ══════════════
fig, axs = plt.subplots(1, 2, figsize=(9.8, 4.4))
t2 = [(0, 0), (4, 0), (0, 3)]
i2 = apply([[2, 1], [0, 3]], t2)
plane(axs[0], (-1.2, 5.4), (-1.2, 4.4))
shape(axs[0], t2, LINE, FILL)
for p, nm in zip(t2, ["O", "A", "B"]):
    dot(axs[0], p)
    tag(axs[0], p, nm)
axs[0].set_title("object", fontsize=12.5, color=LINE, pad=8)
plane(axs[1], (-1.6, 10.5), (-1.6, 10.5), step=2, tick_step=2)
shape(axs[1], i2, ACC, PALE)
for p, nm in zip(i2, ["O", "A'", "B'"]):
    dot(axs[1], p, ACC)
    tag(axs[1], p, nm, ACC, dx=0.35, dy=0.35)
axs[1].set_title("image", fontsize=12.5, color=ACC, pad=8)
fig.tight_layout()
save(fig, "ahl-3-9-we2.svg")

# ══════════════ 例題5（Sierpinski の面積） ══════════════
fig, ax = plt.subplots(figsize=(7.4, 2.3))
blank(ax, (0, 7.4), (0.8, 2.9))
ax.set_aspect("auto")
xs = [0.9, 2.5, 4.1, 5.7]
vals = ["$A$", r"$\frac{3}{4}A$", r"$\left(\frac{3}{4}\right)^{2}A$",
        r"$\left(\frac{3}{4}\right)^{3}A$"]
for i, (x, v) in enumerate(zip(xs, vals)):
    ax.text(x, 2.0, v, fontsize=15, ha="center", va="center", color=INK)
    ax.text(x, 1.15, f"stage {i}", fontsize=11, ha="center", va="center",
            color=GREY)
    if i:
        arrow(ax, (xs[i - 1] + 0.55, 2.0), (x - 0.55, 2.0), color=ACC)
        ax.text((xs[i - 1] + x) / 2, 2.45, r"$\times \frac{3}{4}$",
                fontsize=12, ha="center", va="center", color=ACC)
ax.text(6.9, 2.0, r"$\cdots$", fontsize=15, ha="center", va="center",
        color=GREY)
fig.tight_layout()
save(fig, "ahl-3-9-we5.svg")

print("figures written to", os.path.normpath(OUT))
