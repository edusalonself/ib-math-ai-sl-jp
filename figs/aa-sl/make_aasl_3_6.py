"""AA SL 3.6 の図をつくる。

    python3 figs/aa-sl/make_aasl_3_6.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_3_6.py  … 目視用の PNG も

出力: aa-sl/03-geometry/img/aasl-3-6-idea-a.svg
      aa-sl/03-geometry/img/aasl-3-6-idea-b.svg

(a) ピタゴラスの恒等式。単位円の中の直角三角形から。
(b) cos 2θ の 3 つの形。入れかえで移り合う。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
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
OUT = os.path.join(HERE, "..", "..", "aa-sl", "03-geometry", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
GREEN = "#15803d"

fig1, ax1 = plt.subplots(figsize=(5.3, 4.9))
fig2, ax2 = plt.subplots(figsize=(5.3, 4.9))
# ══════════════════════════════════════════════════════════
# (a) ピタゴラスの恒等式
# ══════════════════════════════════════════════════════════
ax1.set_title("The Pythagorean identity", fontsize=11, color=INK,
              loc="left", pad=10)
ax1.set_xlim(-1.55, 1.85)
ax1.set_ylim(-1.30, 1.55)
ax1.set_aspect("equal")
ax1.axis("off")

t = np.linspace(0, 2 * np.pi, 400)
ax1.plot(np.cos(t), np.sin(t), color=GREY, linewidth=1.1)
ax1.annotate("", xy=(1.5, 0), xytext=(-1.35, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.0))
ax1.annotate("", xy=(0, 1.4), xytext=(0, -1.25),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.0))

th = 1.0
Px, Py = np.cos(th), np.sin(th)
ax1.plot([0, Px], [0, Py], color=ACCENT, linewidth=2.2)
ax1.plot([Px, Px], [0, Py], color=WARM, linewidth=2.0)
ax1.plot([0, Px], [0, 0], color=GREEN, linewidth=2.4, solid_capstyle="butt")
ax1.plot([Px], [Py], marker="o", markersize=5.2, color=INK, zorder=3)
ax1.plot([Px - 0.13, Px - 0.13, Px], [0, 0.13, 0.13], color=GREY,
         linewidth=1.0)

ta = np.linspace(0, th, 60)
ax1.plot(0.25 * np.cos(ta), 0.25 * np.sin(ta), color=INK, linewidth=1.2)
ax1.text(0.29, 0.09, "$\\theta$", fontsize=12, color=INK)

ax1.text(Px * 0.42 - 0.10, -0.28, "$\\cos\\theta$", fontsize=10.5, color=GREEN)
ax1.text(Px + 0.08, Py * 0.42, "$\\sin\\theta$", fontsize=10.5, color=WARM)
ax1.text(0.12, 0.62, "$1$", fontsize=11, color=ACCENT)


# ══════════════════════════════════════════════════════════
# (b) cos 2θ の 3 つの形
# ══════════════════════════════════════════════════════════
ax2.set_title("Three forms of $\\cos 2\\theta$", fontsize=11, color=INK,
              loc="left", pad=10)
ax2.set_xlim(0, 10)
ax2.set_ylim(-1.72, 2.05)
ax2.axis("off")

BOX = dict(boxstyle="round,pad=0.42", facecolor="#eef4fb", edgecolor=ACCENT,
           linewidth=1.2)
ax2.text(5.0, 1.45, "$\\cos^{2}\\theta - \\sin^{2}\\theta$", fontsize=12,
         color=INK, ha="center", va="center", bbox=BOX)
ax2.text(5.0, 0.15, "$2\\cos^{2}\\theta - 1$", fontsize=12, color=INK,
         ha="center", va="center", bbox=BOX)
ax2.text(5.0, -1.15, "$1 - 2\\sin^{2}\\theta$", fontsize=12, color=INK,
         ha="center", va="center", bbox=BOX)

ax2.annotate("", xy=(3.4, 0.35), xytext=(3.4, 1.25),
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=1.4))
ax2.annotate("", xy=(3.4, -0.95), xytext=(3.4, -0.05),
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=1.4))
ax2.text(3.15, 0.80, "put $\\sin^{2}\\theta = 1 - \\cos^{2}\\theta$",
         fontsize=9.5, color=WARM, ha="right", va="center")
ax2.text(3.15, -0.50, "put $\\cos^{2}\\theta = 1 - \\sin^{2}\\theta$",
         fontsize=9.5, color=WARM, ha="right", va="center")

ax2.text(0, 1.95, "the same value, written three ways", fontsize=10,
         color=INK, va="top")

for _fig, _name in ((fig1, "aasl-3-6-idea-a.svg"), (fig2, "aasl-3-6-idea-b.svg")):
    _fig.tight_layout()
    _p = os.path.join(OUT, _name)
    _fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
    print("wrote", os.path.normpath(_p))
    if os.environ.get("FIG_PNG"):
        _q = _p[:-4] + ".png"
        _fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                     facecolor="white")
        print("wrote", os.path.normpath(_q))
