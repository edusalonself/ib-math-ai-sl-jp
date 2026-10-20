"""AA HL 3.16（ベクトル積と面積）の図をつくる。

    python3 figs/aa-hl/make_aahl_3_16.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_3_16.py  … 目視用の PNG も

出力: aa-hl/03-geometry-and-trigonometry/img/aahl-3-16-idea-a.svg
      aa-hl/03-geometry-and-trigonometry/img/aahl-3-16-idea-b.svg

(a) 平行四辺形の面積は、底辺 |v| × 高さ |w| sin θ。
(b) 三角形は平行四辺形の半分。
(c) 右ねじの規則：v から w へ回すと、v×w の向きになる。

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
from matplotlib.patches import Arc, Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-hl", "03-geometry-and-trigonometry",
                   "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
FILL = "#dbeafe"
O = np.array([0.0, 0.0])
V = np.array([4.0, 0.0])
W = np.array([1.5, 2.3])


def arrow(ax, p, q, col, lw=1.9, ls="-"):
    ax.annotate("", xy=q, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=col, linewidth=lw,
                                linestyle=ls, shrinkA=0, shrinkB=0))


# ══════════════════════════════════════════════════════════
# (a) 平行四辺形の面積
# ══════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(5.6, 3.1))

ax1.add_patch(Polygon([O, V, V + W, W], closed=True, facecolor=FILL,
                      edgecolor="none", zorder=1))
ax1.plot([V[0], (V + W)[0], W[0]], [V[1], (V + W)[1], W[1]],
         color=GREY, linewidth=1.2, linestyle=(0, (4, 3)), zorder=2)
arrow(ax1, O, V, ACCENT)
arrow(ax1, O, W, WARM)
ax1.text(V[0] / 2 - 0.05, -0.36, "$v$", fontsize=12, color=ACCENT)
ax1.text(W[0] / 2 - 0.42, W[1] / 2, "$w$", fontsize=12, color=WARM)

# 高さ
ax1.plot([W[0], W[0]], [0.0, W[1]], color=GREY, linewidth=1.1,
         linestyle=(0, (2, 2)), zorder=3)
ax1.plot([W[0], W[0] + 0.22, W[0] + 0.22], [0.22, 0.22, 0.0],
         color=GREY, linewidth=1.0, zorder=3)
ax1.text(W[0] + 0.16, W[1] / 2 - 0.12, "height $= |w|\\sin\\theta$",
         fontsize=9.5, color=GREY)
ax1.add_patch(Arc(O, 1.5, 1.5, theta1=0.0,
                  theta2=float(np.degrees(np.arctan2(W[1], W[0]))),
                  color=INK, linewidth=1.1, zorder=4))
ax1.text(0.82, 0.24, "$\\theta$", fontsize=11, color=INK)

ax1.plot([3.75], [1.78], "o", color=INK, markersize=9, markerfacecolor="white",
         markeredgewidth=1.4, zorder=5)
ax1.plot([3.75], [1.78], "o", color=INK, markersize=2.6, zorder=6)
ax1.text(3.98, 1.68, "$v \\times w$", fontsize=11, color=INK)

ax1.set_xlim(-0.4, 5.8)
ax1.set_ylim(-0.7, 2.7)
ax1.set_aspect("equal")
ax1.axis("off")

# ══════════════════════════════════════════════════════════
# (b) 三角形は半分
# ══════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(5.8, 3.2))

ax2.add_patch(Polygon([O, V, W], closed=True, facecolor=FILL,
                      edgecolor="none", zorder=1))
ax2.add_patch(Polygon([O, V, V + W, W], closed=True, facecolor="none",
                      edgecolor=GREY, linewidth=1.2, linestyle=(0, (4, 3)),
                      zorder=2))
ax2.plot([V[0], W[0]], [V[1], W[1]], color=INK, linewidth=1.4, zorder=3)
arrow(ax2, O, V, ACCENT)
arrow(ax2, O, W, WARM)
ax2.text(V[0] / 2 - 0.05, -0.40, "$v$", fontsize=12, color=ACCENT)
ax2.text(W[0] / 2 - 0.42, W[1] / 2, "$w$", fontsize=12, color=WARM)
ax2.text(1.35, 0.55, "half", fontsize=10, color=INK)
ax2.text(3.55, 1.85, "other half", fontsize=10, color=GREY)

ax2.set_xlim(-0.6, 6.6)
ax2.set_ylim(-1.8, 3.0)
ax2.set_aspect("equal")
ax2.axis("off")


# ══════════════════════════════════════════════════════════
# (c) 右ねじの規則：v から w へ回すと、v×w は上を向く
# ══════════════════════════════════════════════════════════
from matplotlib.patches import FancyArrowPatch
fig3, ax3 = plt.subplots(figsize=(5.2, 4.2))
VX = np.array([3.0, -0.35])      # v（手前右）
WY = np.array([1.35, 1.05])      # w（奥）
ax3.add_patch(Polygon([O - 0.25 * VX - 0.3 * WY, 1.25 * VX - 0.3 * WY,
                       1.25 * VX + 1.35 * WY, -0.25 * VX + 1.35 * WY],
                      closed=True, facecolor=FILL, edgecolor="none", zorder=1))
arrow(ax3, O, VX, ACCENT)
arrow(ax3, O, WY, WARM)
ax3.text(VX[0] + 0.12, VX[1] - 0.12, "$v$", fontsize=13, color=ACCENT)
ax3.text(WY[0] + 0.1, WY[1] + 0.05, "$w$", fontsize=13, color=WARM)
# 指を曲げる向き（v から w へ）
ax3.add_patch(FancyArrowPatch(0.42 * VX, 0.62 * WY,
                              connectionstyle="arc3,rad=0.45",
                              arrowstyle="-|>", mutation_scale=13,
                              color=INK, linewidth=1.4, zorder=4))
# 親指の向き
arrow(ax3, O, np.array([0.0, 2.9]), INK, lw=2.2)
ax3.text(0.15, 2.75, "$v \\times w$", fontsize=13, color=INK)
arrow(ax3, O, np.array([0.0, -1.7]), GREY, lw=1.6, ls=(0, (4, 3)))
ax3.text(0.15, -1.75, "$w \\times v$", fontsize=13, color=GREY)
ax3.set_xlim(-1.2, 5.3)
ax3.set_ylim(-2.1, 3.3)
ax3.set_aspect("equal")
ax3.axis("off")

for _fig, _name in ((fig1, "a"), (fig2, "b"), (fig3, "c")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-3-16-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-3-16-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
