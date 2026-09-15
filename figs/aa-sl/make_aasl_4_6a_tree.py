"""AA SL 4.6a の例題 4 の解答図（もどす場合の樹形図）。

    python3 figs/aa-sl/make_aasl_4_6a_tree.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_4_6a_tree.py

出力: aa-sl/04-statistics-and-probability/img/aasl-4-6a-tree.svg

★ これは例題 4の「解答例」の図です。生徒が自分のかいた図と見くらべます。

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


fig, ax = plt.subplots(figsize=(8.2, 5.0))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")

X0, X1, X2 = 0.7, 3.6, 6.9
Y0 = 3.0
Y1 = (4.4, 1.6)
Y2 = ((5.3, 3.6), (2.4, 0.7))

FIRST = (("$G$", "$\\dfrac{2}{5}$"), ("$Y$", "$\\dfrac{3}{5}$"))
SECOND = (("$G$", "$\\dfrac{2}{5}$"), ("$Y$", "$\\dfrac{3}{5}$"))
ENDS = (("$GG$", "$\\dfrac{4}{25}$"), ("$GY$", "$\\dfrac{6}{25}$"),
        ("$YG$", "$\\dfrac{6}{25}$"), ("$YY$", "$\\dfrac{9}{25}$"))

ax.plot([X0], [Y0], marker="o", markersize=6, color=INK)
_k = 0
for _i, _y1 in enumerate(Y1):
    ax.plot([X0, X1], [Y0, _y1], color=ACCENT, linewidth=1.6)
    ax.text((X0 + X1) / 2, (Y0 + _y1) / 2 + 0.22, FIRST[_i][1], fontsize=12,
            color=ACCENT, ha="center")
    ax.text(X1 + 0.12, _y1, FIRST[_i][0], fontsize=12, color=INK,
            va="center")
    for _j, _y2 in enumerate(Y2[_i]):
        ax.plot([X1 + 0.45, X2], [_y1, _y2], color=ACCENT, linewidth=1.6)
        ax.text((X1 + 0.45 + X2) / 2, (_y1 + _y2) / 2 + 0.22,
                SECOND[_j][1], fontsize=12, color=ACCENT, ha="center")
        ax.text(X2 + 0.12, _y2, SECOND[_j][0], fontsize=12, color=INK,
                va="center")
        ax.text(X2 + 0.75, _y2, ENDS[_k][0], fontsize=12, color=INK,
                va="center")
        ax.text(X2 + 1.75, _y2, ENDS[_k][1], fontsize=12, color=WARM,
                va="center")
        _k += 1

ax.text(0.0, 0.15,
        "the second branches repeat the first, because the counter is "
        "returned; the four end probabilities add to $1$",
        fontsize=10, color=INK, ha="left", va="bottom")

fig.tight_layout()
path = os.path.join(OUT, "aasl-4-6a-tree.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
