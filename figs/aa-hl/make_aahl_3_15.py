"""AA HL 3.15（一致・平行・交わる・ねじれ）の図をつくる。

    python3 figs/aa-hl/make_aahl_3_15.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_3_15.py  … 目視用の PNG も

出力: aa-hl/03-geometry-and-trigonometry/img/aahl-3-15-idea-a.svg
      aa-hl/03-geometry-and-trigonometry/img/aahl-3-15-idea-b.svg

(a) 2 直線の 4 つの場合。
(b) 判定の手順（流れ図）。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → 使わない
  * \\lvert \\rvert も読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に例題・演習の答えを書かないこと。
★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-hl", "03-geometry-and-trigonometry",
                   "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"


def seg(ax, p, q, col, lw=2.0, ls="-", z=2):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=col, linewidth=lw,
            linestyle=ls, zorder=z, solid_capstyle="round")


# ══════════════════════════════════════════════════════════
# (a) 4 つの場合
# ══════════════════════════════════════════════════════════
fig1, axs = plt.subplots(2, 2, figsize=(6.4, 4.4))
fig1.suptitle("Two lines in three dimensions: four possibilities",
              fontsize=11, color=INK, x=0.02, ha="left", y=0.99)

# 左上: coincident
ax = axs[0][0]
seg(ax, (0.1, 0.9), (3.9, 2.6), ACCENT, lw=4.5)
seg(ax, (0.4, 1.03), (3.6, 2.47), WARM, lw=2.0, ls=(0, (4, 3)), z=3)
ax.set_title("coincident: the same line twice", fontsize=9.5, color=INK,
             loc="left", pad=4)
ax.text(0.1, 0.25, "directions parallel, and every point is shared",
        fontsize=8.2, color=GREY)

# 右上: parallel (distinct)
ax = axs[0][1]
seg(ax, (0.1, 0.7), (3.9, 2.4), ACCENT)
seg(ax, (0.1, 1.5), (3.9, 3.2), WARM)
ax.set_title("parallel, but not the same line", fontsize=9.5, color=INK,
             loc="left", pad=4)
ax.text(0.1, 0.25, "directions parallel, no point is shared",
        fontsize=8.2, color=GREY)

# 左下: intersecting
ax = axs[1][0]
seg(ax, (0.1, 0.7), (3.9, 3.0), ACCENT)
seg(ax, (0.3, 3.1), (3.7, 0.8), WARM)
P = np.array([2.02, 1.86])
ax.plot([P[0]], [P[1]], "o", color=INK, markersize=5.5, zorder=5)
ax.annotate("one shared point", xy=(P[0], P[1]), xytext=(1.00, 0.72),
            fontsize=8.2, color=INK,
            arrowprops=dict(arrowstyle="-", color=GREY, linewidth=0.9,
                            shrinkA=3, shrinkB=5))
ax.set_title("intersecting: they meet once", fontsize=9.5, color=INK,
             loc="left", pad=4)
ax.text(0.1, 0.25, "directions not parallel, the equations have a solution",
        fontsize=7.6, color=GREY)

# 右下: skew
ax = axs[1][1]
seg(ax, (0.1, 0.7), (3.9, 3.0), ACCENT)
seg(ax, (0.3, 3.1), (1.55, 2.25), WARM)
seg(ax, (2.45, 1.64), (3.7, 0.8), WARM)
ax.text(1.20, 2.74, "passes behind", fontsize=8.2, color=WARM,
        bbox=dict(facecolor="white", edgecolor="none", pad=1.0))
ax.set_title("skew: they never meet", fontsize=9.5, color=INK,
             loc="left", pad=4)
ax.text(0.1, 0.25, "directions not parallel, the equations have no solution",
        fontsize=7.6, color=GREY)

for _row in axs:
    for _ax in _row:
        _ax.set_xlim(0, 4.2)
        _ax.set_ylim(0, 3.6)
        _ax.axis("off")

# ══════════════════════════════════════════════════════════
# (b) 判定の手順
# ══════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(6.2, 3.8))
ax2.set_title("How to tell the four cases apart", fontsize=10.5, color=INK,
              loc="left", pad=10)


def box(x, y, w, h, text, col, fs=9):
    ax2.add_patch(FancyBboxPatch((x, y), w, h,
                                 boxstyle="round,pad=0.10,rounding_size=0.12",
                                 facecolor="white", edgecolor=col,
                                 linewidth=1.4, zorder=2))
    ax2.text(x + w / 2, y + h / 2, text, fontsize=fs, color=INK,
             ha="center", va="center", zorder=3)


def link(p, q, label="", dx=0.0, dy=0.12):
    ax2.annotate("", xy=q, xytext=p,
                 arrowprops=dict(arrowstyle="-|>", color=GREY, linewidth=1.3,
                                 shrinkA=2, shrinkB=2))
    if label:
        ax2.text((p[0] + q[0]) / 2 + dx, (p[1] + q[1]) / 2 + dy, label,
                 fontsize=8.5, color=GREY, ha="center",
                 bbox=dict(facecolor="white", edgecolor="none", pad=1.0))


box(3.0, 5.0, 4.0, 0.8, "are the directions parallel?", ACCENT, fs=9.5)
box(0.2, 3.0, 3.4, 0.8, "is a point of one line\non the other line?", ACCENT,
    fs=8.6)
box(6.4, 3.0, 3.4, 0.8, "solve two of the three\nequations", ACCENT, fs=8.6)
box(0.0, 1.0, 1.7, 0.8, "coincident", WARM, fs=9)
box(2.0, 1.0, 1.7, 0.8, "parallel", WARM, fs=9)
box(6.2, 1.0, 1.7, 0.8, "intersecting", WARM, fs=9)
box(8.2, 1.0, 1.7, 0.8, "skew", WARM, fs=9)

link((4.2, 5.0), (1.9, 3.9), "yes", dx=-0.25)
link((5.8, 5.0), (8.1, 3.9), "no", dx=0.25)
link((1.1, 3.0), (0.85, 1.9), "yes", dx=-0.32, dy=0.0)
link((2.7, 3.0), (2.85, 1.9), "no", dx=0.32, dy=0.0)
link((7.3, 3.0), (7.05, 1.9), "third one\nholds too", dx=-1.00, dy=-0.18)
link((8.9, 3.0), (9.05, 1.9), "it fails", dx=0.58, dy=0.0)

ax2.text(0.0, 0.1, "the two parameters need different letters:"
         " $\\lambda$ for one line, $\\mu$ for the other",
         fontsize=8.8, color=GREY)
ax2.set_xlim(-0.3, 10.2)
ax2.set_ylim(-0.2, 6.2)
ax2.axis("off")

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-3-15-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-3-15-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
