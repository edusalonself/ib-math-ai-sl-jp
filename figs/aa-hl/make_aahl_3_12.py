"""AA HL 3.12（ベクトルの基本）の図をつくる。

    python3 figs/aa-hl/make_aahl_3_12.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_3_12.py  … 目視用の PNG も

出力: aa-hl/03-geometry-and-trigonometry/img/aahl-3-12-idea-a.svg
      aa-hl/03-geometry-and-trigonometry/img/aahl-3-12-idea-b.svg

(a) 位置ベクトル a, b と、変位ベクトル AB = b - a。
(b) 和・差・スカラー倍の図（平行四辺形と、向きを変えない伸縮）。

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

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-hl", "03-geometry-and-trigonometry",
                   "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"


def arrow(ax, p, q, col, lw=1.8, ls="-", sb=0):
    ax.annotate("", xy=q, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=col, linewidth=lw,
                                linestyle=ls, shrinkA=0, shrinkB=sb))


# ══════════════════════════════════════════════════════════
# (a) 位置ベクトルと変位ベクトル
# ══════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(5.0, 4.2))
ax1.set_title("From $O$ to $A$ and to $B$, then across from $A$ to $B$",
              fontsize=10.5, color=INK, loc="left", pad=10)
O = np.array([0.0, 0.0])
A = np.array([3.0, 1.0])
B = np.array([1.4, 3.2])
arrow(ax1, O, A, ACCENT)
arrow(ax1, O, B, ACCENT)
arrow(ax1, A, B, WARM, sb=9)
ax1.plot(*zip(O, A, B), linestyle="none")
for _p, _lab, _dx, _dy in ((O, "$O$", -0.22, -0.22), (A, "$A$", 0.12, -0.16),
                           (B, "$B$", 0.10, 0.12)):
    ax1.text(_p[0] + _dx, _p[1] + _dy, _lab, fontsize=10.5, color=INK)
ax1.text(1.75, 0.30, "$\\mathbf{a}$", fontsize=11, color=ACCENT)
ax1.text(0.55, 1.85, "$\\mathbf{b}$", fontsize=11, color=ACCENT)
ax1.text(2.35, 2.35, "$\\mathbf{b}-\\mathbf{a}$", fontsize=11, color=WARM)
ax1.text(-0.35, 4.05, "go back along $\\mathbf{a}$, then out along $\\mathbf{b}$",
         fontsize=9, color=GREY)
ax1.set_xlim(-0.6, 4.0)
ax1.set_ylim(-0.6, 4.3)
ax1.set_aspect("equal")
ax1.axis("off")

# ══════════════════════════════════════════════════════════
# (b) 和・差・スカラー倍
# ══════════════════════════════════════════════════════════
fig2, axes2 = plt.subplots(1, 2, figsize=(6.6, 3.0))
u = np.array([2.6, 0.6])
w = np.array([0.9, 2.2])

ax = axes2[0]
arrow(ax, O, u, ACCENT)
arrow(ax, O, w, ACCENT)
arrow(ax, u, u + w, GREY, lw=1.2, ls="--")
arrow(ax, w, u + w, GREY, lw=1.2, ls="--")
arrow(ax, O, u + w, WARM)
ax.text(1.35, 0.06, "$\\mathbf{u}$", fontsize=10.5, color=ACCENT)
ax.text(0.26, 1.15, "$\\mathbf{w}$", fontsize=10.5, color=ACCENT)
ax.text(1.55, 1.75, "$\\mathbf{u}+\\mathbf{w}$", fontsize=10.5, color=WARM)
ax.set_title("the parallelogram rule", fontsize=10, color=INK, pad=6)
ax.set_xlim(-0.5, 4.2)
ax.set_ylim(-0.5, 3.4)

ax = axes2[1]
arrow(ax, O, u, ACCENT)
arrow(ax, O, 1.5 * u, WARM, lw=1.4)
arrow(ax, O, -0.8 * u, GREY, lw=1.4)
ax.text(1.25, 0.06, "$\\mathbf{u}$", fontsize=10.5, color=ACCENT)
ax.text(3.2, 1.25, "$1.5\\mathbf{u}$", fontsize=10.5, color=WARM)
ax.text(-1.9, -0.95, "$-0.8\\mathbf{u}$", fontsize=10.5, color=GREY)
ax.set_title("a scalar keeps the line, not the length",
             fontsize=10, color=INK, pad=6)
ax.set_xlim(-2.6, 4.6)
ax.set_ylim(-1.5, 2.2)

for _ax in axes2:
    _ax.set_aspect("equal")
    _ax.axis("off")

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-3-12-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-3-12-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
