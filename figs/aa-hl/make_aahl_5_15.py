"""AA HL 5.15（さらに進んだ導関数と、その不定積分）の図をつくる。

    python3 figs/aa-hl/make_aahl_5_15.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_5_15.py  … 目視用の PNG も

出力: aa-hl/05-calculus/img/aahl-5-15-idea-a.svg
      aa-hl/05-calculus/img/aahl-5-15-idea-b.svg

(a) y = arcsin x の三角形：sin y = x なら cos y = sqrt(1 - x^2)。
(b) 不定積分は「曲線の族」。C がちがうだけで、傾きは同じ。

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
from matplotlib.patches import Arc

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-hl", "05-calculus", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"

# ══════════════════════════════════════════════════════════
# (a) arcsin の三角形
# ══════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(5.2, 3.2))
ax1.set_title("if $y = \\arcsin x$ then $\\sin y = x$, and the triangle"
              " gives $\\cos y$", fontsize=9.8, color=INK, loc="left", pad=10)

A = np.array([0.0, 0.0])
B = np.array([3.4, 0.0])
Cc = np.array([3.4, 2.2])
ax1.plot([A[0], B[0], Cc[0], A[0]], [A[1], B[1], Cc[1], A[1]],
         color=ACCENT, linewidth=2.0, zorder=3)
ax1.plot([B[0] - 0.26, B[0] - 0.26, B[0]], [0, 0.26, 0.26], color=INK,
         linewidth=1.0, zorder=4)
ax1.add_patch(Arc(A, 1.5, 1.5, theta1=0.0,
                  theta2=float(np.degrees(np.arctan2(2.2, 3.4))),
                  color=INK, linewidth=1.1, zorder=4))
ax1.text(0.82, 0.16, "$y$", fontsize=11, color=INK)
ax1.text(1.55, -0.45, "$\\sqrt{1-x^{2}}$", fontsize=11, color=GREY)
ax1.text(3.52, 1.05, "$x$", fontsize=11, color=GREY)
ax1.text(1.35, 1.45, "$1$", fontsize=11, color=GREY)
ax1.text(-0.1, -1.35, "so $\\cos y = \\sqrt{1-x^{2}}$, and"
         " $\\frac{dy}{dx} = \\frac{1}{\\cos y}$", fontsize=9.5, color=GREY)
ax1.set_xlim(-0.4, 6.4)
ax1.set_ylim(-1.9, 2.8)
ax1.set_aspect("equal")
ax1.set_xticks([])
ax1.set_yticks([])
for _s in ("top", "right", "bottom", "left"):
    ax1.spines[_s].set_visible(False)

# ══════════════════════════════════════════════════════════
# (b) 曲線の族
# ══════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(5.4, 3.2))
ax2.set_title("an indefinite integral is a family of curves, one for"
              " each $C$", fontsize=10.0, color=INK, loc="left", pad=10)

t = np.linspace(-4.0, 4.0, 600)
for _c, _col in ((-1.0, GREY), (0.0, ACCENT), (1.0, WARM), (2.0, GREY)):
    ax2.plot(t, np.arctan(t) + _c, color=_col, linewidth=1.8, zorder=3)
ax2.text(4.1, np.arctan(4.0) - 1.05, "$C = -1$", fontsize=9, color=GREY)
ax2.text(4.1, np.arctan(4.0) - 0.05, "$C = 0$", fontsize=9, color=ACCENT)
ax2.text(4.1, np.arctan(4.0) + 0.95, "$C = 1$", fontsize=9, color=WARM)
ax2.text(4.1, np.arctan(4.0) + 1.95, "$C = 2$", fontsize=9, color=GREY)
_x0 = 1.0
for _c in (-1.0, 0.0, 1.0, 2.0):
    _m = 1 / (1 + _x0 ** 2)
    ax2.plot([_x0 - 0.9, _x0 + 0.9],
             [np.arctan(_x0) + _c - 0.9 * _m, np.arctan(_x0) + _c + 0.9 * _m],
             color=INK, linewidth=0.9, linestyle=(0, (3, 3)), zorder=4)
ax2.text(-4.1, -3.05, "at the same $x$ the curves are parallel:"
         " same gradient", fontsize=9, color=GREY)
ax2.set_xlim(-4.3, 6.6)
ax2.set_ylim(-3.6, 3.7)
ax2.axhline(0, color=GREY, linewidth=0.8, zorder=0)
ax2.set_xticks([-2, 0, 2])
ax2.set_yticks([])
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax2.tick_params(labelsize=9, colors=GREY)

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-5-15-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-5-15-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
