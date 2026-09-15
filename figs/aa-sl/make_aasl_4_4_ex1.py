"""AA SL 4.4 の演習 1 の解答図（散布図と近似直線）。

    python3 figs/aa-sl/make_aasl_4_4_ex1.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_4_4_ex1.py

出力: aa-sl/04-statistics-and-probability/img/aasl-4-4-ex1.svg

★ これは演習 1の「解答例」の図です。生徒が自分のかいた図と見くらべます。

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


fig, ax = plt.subplots(figsize=(7.2, 5.2))

XS = np.array([1, 2, 3, 4, 5, 6], dtype=float)
YS = np.array([3, 5, 4, 7, 8, 9], dtype=float)

_line = np.linspace(0.4, 6.6, 50)
ax.plot(_line, 1.2 * _line + 1.8, color=ACCENT, linewidth=1.8)
ax.plot(XS, YS, linestyle="none", marker="o", markersize=7, color=INK)

ax.plot([3.5], [6.0], linestyle="none", marker="X", markersize=12,
        color=WARM, zorder=6)
ax.annotate("mean point $(3.5,\\ 6)$", (3.5, 6), textcoords="offset points",
            xytext=(10, -20), fontsize=11, color=WARM)

ax.set_xlim(0, 7)
ax.set_ylim(0, 10.6)
ax.set_xticks(range(0, 8))
ax.set_yticks(range(0, 11, 2))
ax.tick_params(labelsize=10)
ax.grid(True, color="#e5e7eb", linewidth=0.8)
ax.set_axisbelow(True)
for _s in ("top", "right"):
    ax.spines[_s].set_visible(False)
ax.set_xlabel("$x$", fontsize=12, color=INK)
ax.set_ylabel("$y$", fontsize=12, color=INK, rotation=0, labelpad=12)
ax.set_title("a line of best fit drawn by eye through the mean point",
             fontsize=10, color=INK, loc="left", pad=10)

fig.tight_layout()
path = os.path.join(OUT, "aasl-4-4-ex1.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
