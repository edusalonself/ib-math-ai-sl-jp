"""AA SL 4.6a の演習 6 の解答図（4 領域の確率を書いた Venn 図）。

    python3 figs/aa-sl/make_aasl_4_6a_ex6.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_4_6a_ex6.py

出力: aa-sl/04-statistics-and-probability/img/aasl-4-6a-ex6.svg

★ これは演習 6の「解答例」の図です。生徒が自分のかいた図と見くらべます。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * \\le \\ge は読めない → \\leq \\geq を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "04-statistics-and-probability", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
FILL = "#dbe8f5"


fig, ax = plt.subplots(figsize=(6.6, 4.4))

ax.set_xlim(-0.5, 6.5)
ax.set_ylim(-0.5, 4.4)
ax.set_aspect("equal", adjustable="datalim")
ax.axis("off")

ax.add_patch(plt.Rectangle((-0.3, -0.3), 6.6, 4.4, facecolor="white",
                           edgecolor=GREY, linewidth=1.1))
ax.text(6.05, 3.85, "$U$", fontsize=11, color=GREY, ha="right", va="top")

ax.add_patch(plt.Circle((2.35, 1.9), 1.7, facecolor=FILL, alpha=0.55,
                        edgecolor=ACCENT, linewidth=1.4))
ax.add_patch(plt.Circle((3.85, 1.9), 1.7, facecolor=FILL, alpha=0.55,
                        edgecolor=ACCENT, linewidth=1.4))
ax.text(1.05, 3.45, "$A$", fontsize=12, color=ACCENT)
ax.text(5.05, 3.45, "$B$", fontsize=12, color=ACCENT)

ax.text(1.55, 1.85, "$0.3$", fontsize=13, color=INK, ha="center")
ax.text(3.10, 1.85, "$0.2$", fontsize=13, color=WARM, ha="center")
ax.text(4.65, 1.85, "$0.2$", fontsize=13, color=INK, ha="center")
ax.text(0.35, 0.15, "$0.3$", fontsize=13, color=INK, ha="center")

ax.text(-0.3, -0.75,
        "the four probabilities add to $1$; the overlap $0.2$ is counted once",
        fontsize=10, color=INK, ha="left", va="top")

fig.tight_layout()
path = os.path.join(OUT, "aasl-4-6a-ex6.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
