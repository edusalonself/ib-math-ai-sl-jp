"""AA HL 3.13（内積）の図をつくる。

    python3 figs/aa-hl/make_aahl_3_13.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_3_13.py  … 目視用の PNG も

出力: aa-hl/03-geometry-and-trigonometry/img/aahl-3-13-idea-a.svg
      aa-hl/03-geometry-and-trigonometry/img/aahl-3-13-idea-b.svg

(a) 2 つのベクトルのなす角と、片方をもう片方に落とした影。
(b) なす角と内積の符号：鋭角なら正、直角なら 0、鈍角なら負。

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
# (a) なす角と影
# ══════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(5.4, 3.8))
ax1.set_title("The angle between two vectors, and the shadow of one on the other",
              fontsize=10, color=INK, loc="left", pad=10)
v = np.array([4.0, 0.0])
w = np.array([2.2, 2.4])
arrow(ax1, O, v, ACCENT)
arrow(ax1, O, w, WARM)
ax1.plot([w[0], w[0]], [0.0, w[1]], color=GREY, linestyle=":", linewidth=1.1)
ax1.plot([0.0, w[0]], [-0.28, -0.28], color=GREY, linewidth=1.4)
ax1.plot([0.0, 0.0], [-0.38, -0.18], color=GREY, linewidth=1.0)
ax1.plot([w[0], w[0]], [-0.38, -0.18], color=GREY, linewidth=1.0)
ax1.add_patch(Arc(O, 1.5, 1.5, angle=0.0, theta1=0.0,
                  theta2=float(np.degrees(np.arctan2(w[1], w[0]))),
                  color=INK, linewidth=1.0))
ax1.text(0.95, 0.30, "$\\theta$", fontsize=11, color=INK)
ax1.text(3.0, 0.14, "$\\mathbf{v}$", fontsize=11, color=ACCENT)
ax1.text(1.05, 1.55, "$\\mathbf{w}$", fontsize=11, color=WARM)
ax1.text(1.1, -0.72, "$|\\mathbf{w}|\\cos\\theta$", fontsize=9.5, color=GREY)
ax1.text(-0.15, 3.1, "$\\mathbf{v}\\cdot\\mathbf{w} = |\\mathbf{v}|"
         " \\times (\\,\\text{this shadow}\\,)$", fontsize=9.5, color=INK)
ax1.set_xlim(-0.5, 4.8)
ax1.set_ylim(-1.1, 3.4)
ax1.set_aspect("equal")
ax1.axis("off")

# ══════════════════════════════════════════════════════════
# (b) 内積の符号
# ══════════════════════════════════════════════════════════
fig2, axes2 = plt.subplots(1, 3, figsize=(6.6, 2.4))
PANELS = [
    (35.0, "acute: $\\mathbf{v}\\cdot\\mathbf{w} > 0$", ACCENT),
    (90.0, "right: $\\mathbf{v}\\cdot\\mathbf{w} = 0$", WARM),
    (135.0, "obtuse: $\\mathbf{v}\\cdot\\mathbf{w} < 0$", GREY),
]
for _ax, (_deg, _lab, _col) in zip(axes2, PANELS):
    _u = np.array([2.2, 0.0])
    _r = np.radians(_deg)
    _w = 2.0 * np.array([np.cos(_r), np.sin(_r)])
    arrow(_ax, O, _u, ACCENT, lw=1.6)
    arrow(_ax, O, _w, _col, lw=1.6)
    _ax.add_patch(Arc(O, 1.0, 1.0, angle=0.0, theta1=0.0, theta2=_deg,
                      color=INK, linewidth=0.9))
    _ax.set_title(_lab, fontsize=9.5, color=_col, pad=6)
    _ax.set_xlim(-2.4, 2.6)
    _ax.set_ylim(-0.6, 2.6)
    _ax.set_aspect("equal")
    _ax.axis("off")
fig2.suptitle("The sign of the scalar product tells you the kind of angle",
              fontsize=10.5, color=INK, x=0.02, ha="left", y=1.04)

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-3-13-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-3-13-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
