"""AA HL 3.17（平面のベクトル方程式）の図をつくる。

    python3 figs/aa-hl/make_aahl_3_17.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_3_17.py  … 目視用の PNG も

出力: aa-hl/03-geometry-and-trigonometry/img/aahl-3-17-idea-a.svg
      aa-hl/03-geometry-and-trigonometry/img/aahl-3-17-idea-b.svg

(a) r = a + λb + μc：平面の上の点は、2 つの向きの組み合わせで届く。
(b) 法線 n：平面の上のどの点でも (r - a)·n = 0。

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
from matplotlib.patches import Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-hl", "03-geometry-and-trigonometry",
                   "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
GREEN = "#15803d"
FILL = "#eef2f7"


def arrow(ax, p, q, col, lw=1.9, ls="-", sb=0):
    ax.annotate("", xy=q, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=col, linewidth=lw,
                                linestyle=ls, shrinkA=0, shrinkB=sb))


# 平面を「ゆがんだ平行四辺形」としてかく
E1 = np.array([2.6, -0.55])   # 紙の上での「奥行き」方向
E2 = np.array([1.5, 1.05])    # 紙の上での「横」方向
CORNER = np.array([1.1, 0.6])
PLANE = [CORNER, CORNER + 3.0 * E1, CORNER + 3.0 * E1 + 2.4 * E2,
         CORNER + 2.4 * E2]

# ══════════════════════════════════════════════════════════
# (a) r = a + λb + μc
# ══════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(5.8, 3.8))
ax1.set_title("$r = a + \\lambda b + \\mu c$: one point, two directions",
              fontsize=10.5, color=INK, loc="left", pad=10)
ax1.add_patch(Polygon(PLANE, closed=True, facecolor=FILL, edgecolor=GREY,
                      linewidth=1.1, zorder=1))

O = np.array([0.15, 0.15])
A = CORNER + 0.7 * E1 + 0.55 * E2
P = A + 1.4 * E1 + 1.0 * E2
arrow(ax1, O, A, ACCENT, lw=2.0)
arrow(ax1, A, A + 1.4 * E1, WARM, lw=1.8)
arrow(ax1, A, A + 1.0 * E2, GREEN, lw=1.8)
ax1.plot([A[0] + 1.4 * E1[0], P[0]], [A[1] + 1.4 * E1[1], P[1]],
         color=GREY, linewidth=1.0, linestyle=(0, (3, 3)), zorder=3)
ax1.plot([A[0] + 1.0 * E2[0], P[0]], [A[1] + 1.0 * E2[1], P[1]],
         color=GREY, linewidth=1.0, linestyle=(0, (3, 3)), zorder=3)

for _p, _lab, _dx, _dy, _col in (
        (O, "$O$", -0.30, -0.02, INK),
        (A, "$A$", -0.34, 0.06, INK),
        (P, "$P$", 0.14, 0.06, INK)):
    ax1.plot([_p[0]], [_p[1]], "o", color=_col, markersize=4.5, zorder=5)
    ax1.text(_p[0] + _dx, _p[1] + _dy, _lab, fontsize=10.5, color=_col)
ax1.text((O[0] + A[0]) / 2 - 0.45, (O[1] + A[1]) / 2 + 0.10, "$a$",
         fontsize=12, color=ACCENT)
ax1.text(A[0] + 0.9 * E1[0], A[1] + 0.9 * E1[1] - 0.42, "$\\lambda b$",
         fontsize=11, color=WARM)
ax1.text(A[0] + 0.55 * E2[0] - 0.55, A[1] + 0.55 * E2[1] + 0.08, "$\\mu c$",
         fontsize=11, color=GREEN)
ax1.text(0.0, -1.75, "$b$ and $c$ must lie in the plane and must not be"
         " parallel to each other", fontsize=9, color=GREY)
ax1.set_xlim(-0.7, 12.0)
ax1.set_ylim(-2.3, 4.6)
ax1.set_aspect("equal")
ax1.axis("off")

# ══════════════════════════════════════════════════════════
# (b) 法線 n
# ══════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(5.8, 3.6))
ax2.set_title("every point of the plane has the same scalar product"
              " with $n$", fontsize=10.5, color=INK, loc="left", pad=10)
ax2.add_patch(Polygon(PLANE, closed=True, facecolor=FILL, edgecolor=GREY,
                      linewidth=1.1, zorder=1))
A2 = CORNER + 1.1 * E1 + 1.0 * E2
R2 = CORNER + 2.2 * E1 + 1.7 * E2
N = np.array([0.0, 2.0])
arrow(ax2, A2, A2 + N, INK, lw=2.0)
ax2.text(A2[0] + 0.14, A2[1] + N[1] - 0.30, "$n$", fontsize=12, color=INK)
arrow(ax2, A2, R2, WARM, lw=1.8)
for _p, _lab, _dx, _dy in ((A2, "$A$", -0.36, -0.20), (R2, "$R$", 0.14, 0.02)):
    ax2.plot([_p[0]], [_p[1]], "o", color=INK, markersize=4.5, zorder=5)
    ax2.text(_p[0] + _dx, _p[1] + _dy, _lab, fontsize=10.5, color=INK)
ax2.text((A2[0] + R2[0]) / 2 - 0.30, (A2[1] + R2[1]) / 2 - 0.55,
         "$r - a$", fontsize=11, color=WARM)
# 直角の印
_d = (R2 - A2) / np.linalg.norm(R2 - A2)
_n = N / np.linalg.norm(N)
ax2.plot([A2[0] + 0.30 * _d[0], A2[0] + 0.30 * _d[0] + 0.30 * _n[0],
          A2[0] + 0.30 * _n[0]],
         [A2[1] + 0.30 * _d[1], A2[1] + 0.30 * _d[1] + 0.30 * _n[1],
          A2[1] + 0.30 * _n[1]], color=INK, linewidth=1.0, zorder=4)
ax2.text(0.0, -1.75, "$r - a$ lies in the plane, so $(r - a) \\cdot n = 0$,"
         " that is $r \\cdot n = a \\cdot n$", fontsize=9, color=GREY)
ax2.set_xlim(-0.7, 12.0)
ax2.set_ylim(-2.3, 5.2)
ax2.set_aspect("equal")
ax2.axis("off")

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-3-17-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-3-17-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
