"""AA HL 3.18（直線・平面の交わりと、なす角）の図をつくる。

    python3 figs/aa-hl/make_aahl_3_18.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_3_18.py  … 目視用の PNG も

出力: aa-hl/03-geometry-and-trigonometry/img/aahl-3-18-idea-a.svg
      aa-hl/03-geometry-and-trigonometry/img/aahl-3-18-idea-b.svg

(a) 直線と平面は 3 通り：1 点で交わる／平行で交わらない／平面の中。
(b) 2 平面は 1 本の直線で交わる。なす角は、法線どうしの角と同じ。

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
FILL = "#eef2f7"
FILL2 = "#fdf1e3"

E1 = np.array([2.3, -0.50])
E2 = np.array([1.3, 0.92])


def plane(ax, corner, s1=2.6, s2=2.0, fc=FILL, ec=GREY, z=1):
    pts = [corner, corner + s1 * E1, corner + s1 * E1 + s2 * E2,
           corner + s2 * E2]
    ax.add_patch(Polygon(pts, closed=True, facecolor=fc, edgecolor=ec,
                         linewidth=1.1, zorder=z))
    return pts


def arrow(ax, p, q, col, lw=1.8):
    ax.annotate("", xy=q, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=col, linewidth=lw,
                                shrinkA=0, shrinkB=0))


# ══════════════════════════════════════════════════════════
# (a) 直線と平面の 3 通り
# ══════════════════════════════════════════════════════════
fig1, axs = plt.subplots(1, 3, figsize=(7.4, 2.6))
fig1.suptitle("a line and a plane: three possibilities", fontsize=11,
              color=INK, x=0.01, ha="left", y=1.02)

C = np.array([0.2, 0.6])
mid = C + 1.3 * E1 + 1.0 * E2

# 1点で交わる
ax = axs[0]
plane(ax, C)
ax.plot([mid[0] - 0.5, mid[0] + 0.5], [mid[1] - 2.0, mid[1] + 2.0],
        color=ACCENT, linewidth=2.0, zorder=3)
ax.plot([mid[0]], [mid[1]], "o", color=INK, markersize=5.5, zorder=4)
ax.set_title("one point", fontsize=9.5, color=INK, loc="left", pad=4)
ax.text(0.0, -1.35, "$b \\cdot n \\neq 0$", fontsize=9.5, color=GREY)

# 平行で交わらない
ax = axs[1]
plane(ax, C)
off = np.array([0.0, 1.5])
ax.plot([mid[0] - 1.15 * E1[0] + off[0], mid[0] + 1.15 * E1[0] + off[0]],
        [mid[1] - 1.15 * E1[1] + off[1], mid[1] + 1.15 * E1[1] + off[1]],
        color=ACCENT, linewidth=2.0, zorder=3)
ax.set_title("no point: parallel", fontsize=9.5, color=INK, loc="left", pad=4)
ax.text(0.0, -1.35, "$b \\cdot n = 0$, point not in the plane",
        fontsize=8.6, color=GREY)

# 平面の中
ax = axs[2]
plane(ax, C)
ax.plot([mid[0] - 1.05 * E1[0], mid[0] + 1.05 * E1[0]],
        [mid[1] - 1.05 * E1[1], mid[1] + 1.05 * E1[1]],
        color=ACCENT, linewidth=2.0, zorder=3)
ax.set_title("every point: the line is in the plane", fontsize=8.6, color=INK,
             loc="left", pad=4)
ax.text(0.0, -1.35, "$b \\cdot n = 0$, point in the plane",
        fontsize=8.6, color=GREY)

for _ax in axs:
    _ax.set_xlim(-0.3, 7.4)
    _ax.set_ylim(-1.9, 4.4)
    _ax.set_aspect("equal")
    _ax.axis("off")

# ══════════════════════════════════════════════════════════
# (b) 2 平面のなす角
# ══════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(5.8, 3.4))
ax2.set_title("two planes meet in a line; their angle is the angle between"
              " the normals", fontsize=9.8, color=INK, loc="left", pad=10)

L0 = np.array([0.5, 1.6])
L1 = np.array([5.3, 1.6])
U1 = np.array([1.7, -1.35])
U2 = np.array([0.85, 2.05])
ax2.add_patch(Polygon([L0, L1, L1 + U1, L0 + U1], closed=True,
                      facecolor=FILL, edgecolor=GREY, linewidth=1.1, zorder=1))
ax2.add_patch(Polygon([L0, L1, L1 + U2, L0 + U2], closed=True,
                      facecolor=FILL2, edgecolor=GREY, linewidth=1.1,
                      zorder=1))
ax2.plot([L0[0], L1[0]], [L0[1], L1[1]], color=INK, linewidth=2.2, zorder=3)

B = (L0 + L1) / 2
V1 = np.array([1.35, 1.7])
V2 = np.array([-2.05, 0.88])
V1 = 1.7 * V1 / np.linalg.norm(V1)
V2 = 1.7 * V2 / np.linalg.norm(V2)
arrow(ax2, B, B + V1, WARM)
arrow(ax2, B, B + V2, ACCENT)
ax2.plot([B[0]], [B[1]], "o", color=INK, markersize=4.5, zorder=5)
ax2.text(B[0] + V1[0] + 0.12, B[1] + V1[1] - 0.06, "$n_{1}$", fontsize=11,
         color=WARM)
ax2.text(B[0] + V2[0] - 0.20, B[1] + V2[1] - 0.52, "$n_{2}$", fontsize=11,
         color=ACCENT)
_a1 = float(np.degrees(np.arctan2(V1[1], V1[0])))
_a2 = float(np.degrees(np.arctan2(V2[1], V2[0])))
ax2.add_patch(Arc(B, 1.7, 1.7, theta1=_a1, theta2=_a2, color=INK,
                  linewidth=1.1, zorder=4))
ax2.text(B[0] - 0.28, B[1] + 0.95, "$\\theta$", fontsize=11, color=INK)
ax2.text(L1[0] - 3.05, L1[1] - 0.52, "line of intersection", fontsize=9,
         color=INK)

ax2.text(-0.4, -1.1, "take the acute angle: use $|n_{1} \\cdot n_{2}|$ in"
         " the formula", fontsize=9, color=GREY)
ax2.set_xlim(-0.6, 8.0)
ax2.set_ylim(-1.6, 4.4)
ax2.set_aspect("equal")
ax2.axis("off")

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-3-18-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-3-18-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
