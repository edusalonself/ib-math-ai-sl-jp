"""AA HL 3.14（直線のベクトル方程式）の図をつくる。

    python3 figs/aa-hl/make_aahl_3_14.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_3_14.py  … 目視用の PNG も

出力: aa-hl/03-geometry-and-trigonometry/img/aahl-3-14-idea-a.svg
      aa-hl/03-geometry-and-trigonometry/img/aahl-3-14-idea-b.svg

(a) r = a + λb：a が出発点、b が向き、λ が進んだ量。
(b) 2 直線のなす角は、方向ベクトルのなす角（鋭角のほうを取る）。

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
OUT = os.path.join(HERE, "..", "..", "aa-hl", "03-geometry-and-trigonometry",
                   "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
O = np.array([0.0, 0.0])


def arrow(ax, p, q, col, lw=1.8, ls="-"):
    ax.annotate("", xy=q, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=col, linewidth=lw,
                                linestyle=ls, shrinkA=0, shrinkB=0))


# ══════════════════════════════════════════════════════════
# (a) r = a + λb
# ══════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(5.8, 4.0))
ax1.set_title("$\\mathbf{r} = \\mathbf{a}+\\lambda\\mathbf{b}$: start at"
              " $\\mathbf{a}$, then slide along $\\mathbf{b}$",
              fontsize=10.5, color=INK, loc="left", pad=10)
A = np.array([1.2, 2.6])
B = np.array([1.6, -0.7])
_t = np.linspace(-0.9, 2.5, 50)
_pts = np.array([A + _l * B for _l in _t])
ax1.plot(_pts[:, 0], _pts[:, 1], color=GREY, linewidth=1.0)
arrow(ax1, O, A, ACCENT)
arrow(ax1, A, A + B, WARM)
for _l, _lab in ((1.0, "$\\lambda=1$"), (2.0, "$\\lambda=2$"),
                 (-1.0, "$\\lambda=-1$")):
    _p = A + _l * B
    ax1.plot([_p[0]], [_p[1]], "o", color=INK, markersize=4.5)
    ax1.text(_p[0] + 0.10, _p[1] + 0.12, _lab, fontsize=8.5, color=INK)
ax1.plot([A[0]], [A[1]], "o", color=ACCENT, markersize=6)
ax1.text(A[0] - 0.42, A[1] + 0.05, "$\\lambda=0$", fontsize=8.5, color=ACCENT)
ax1.plot([0.0], [0.0], "o", color=INK, markersize=4.5)
ax1.text(-0.30, -0.10, "$O$", fontsize=10.5, color=INK)
ax1.text(0.40, 1.35, "$\\mathbf{a}$", fontsize=11, color=ACCENT)
ax1.text(1.95, 2.30, "$\\mathbf{b}$", fontsize=11, color=WARM)
ax1.text(-0.55, -1.05, "any point of the line is reached by one value of"
         " $\\lambda$", fontsize=9, color=GREY)
ax1.set_xlim(-0.8, 5.2)
ax1.set_ylim(-1.35, 3.6)
ax1.set_aspect("equal")
ax1.axis("off")

# ══════════════════════════════════════════════════════════
# (b) 2 直線のなす角
# ══════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(5.6, 3.4))
ax2.set_title("The angle between two lines is the angle between their"
              " directions", fontsize=10, color=INK, loc="left", pad=10)
P = np.array([2.2, 1.0])
d1 = np.array([1.5, 0.45])
d2 = np.array([0.7, 1.45])
for _d, _col in ((d1, ACCENT), (d2, WARM)):
    _s = np.linspace(-1.5, 1.6, 20)
    _pts = np.array([P + _u * _d for _u in _s])
    ax2.plot(_pts[:, 0], _pts[:, 1], color=_col, linewidth=1.6)
arrow(ax2, P, P + d1, ACCENT, lw=1.6)
arrow(ax2, P, P + d2, WARM, lw=1.6)
_a1 = float(np.degrees(np.arctan2(d1[1], d1[0])))
_a2 = float(np.degrees(np.arctan2(d2[1], d2[0])))
ax2.add_patch(Arc(P, 1.5, 1.5, angle=0.0, theta1=_a1, theta2=_a2,
                  color=INK, linewidth=1.0))
ax2.text(P[0] + 0.85, P[1] + 0.52, "$\\theta$", fontsize=11, color=INK)
ax2.text(P[0] + 1.6, P[1] + 0.05, "$\\mathbf{b}_{1}$", fontsize=10.5,
         color=ACCENT)
ax2.text(P[0] + 0.40, P[1] + 1.50, "$\\mathbf{b}_{2}$", fontsize=10.5,
         color=WARM)
ax2.text(-0.1, -1.35, "take the acute angle: replace $\\theta$ by"
         " $\\pi-\\theta$ if it comes out obtuse", fontsize=9, color=GREY,
         bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
ax2.set_xlim(-0.3, 5.2)
ax2.set_ylim(-1.7, 3.4)
ax2.set_aspect("equal")
ax2.axis("off")

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-3-14-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-3-14-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
