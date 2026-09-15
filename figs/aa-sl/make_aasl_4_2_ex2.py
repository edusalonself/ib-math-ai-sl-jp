"""AA SL 4.2 の演習 2 の解答図（ヒストグラム）。

    python3 figs/aa-sl/make_aasl_4_2_ex2.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_4_2_ex2.py

出力: aa-sl/04-statistics-and-probability/img/aasl-4-2-ex2.svg

★ これは演習 2の「解答例」の図です。生徒が自分のかいた図と見くらべます。

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


fig, ax = plt.subplots(figsize=(7.2, 4.6))

EDGES = [40, 50, 60, 70, 80, 90]
FREQ = [6, 14, 22, 12, 6]

for _i, _f in enumerate(FREQ):
    ax.bar(EDGES[_i], _f, width=10, align="edge", facecolor=FILL,
           edgecolor=ACCENT, linewidth=1.4)
    ax.text(EDGES[_i] + 5, _f + 0.6, "$%d$" % _f, fontsize=11, color=INK,
            ha="center")

ax.set_xlim(35, 95)
ax.set_ylim(0, 26)
ax.set_xticks(EDGES)
ax.set_xticklabels(["$%d$" % _e for _e in EDGES], fontsize=11)
ax.set_yticks(range(0, 26, 5))
ax.set_yticklabels(["$%d$" % _v for _v in range(0, 26, 5)], fontsize=11)
for _s in ("top", "right"):
    ax.spines[_s].set_visible(False)
ax.set_xlabel("mass $m$ (g)", fontsize=11, color=INK)
ax.set_ylabel("frequency", fontsize=11, color=INK)
ax.set_title("the bars touch, because the data are continuous; all five "
             "classes have width $10$", fontsize=10, color=INK, loc="left",
             pad=10)

fig.tight_layout()
path = os.path.join(OUT, "aasl-4-2-ex2.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
