"""AA SL 4.2 の演習 3 の解答図（累積度数グラフ）。

    python3 figs/aa-sl/make_aasl_4_2_ex3.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_4_2_ex3.py

出力: aa-sl/04-statistics-and-probability/img/aasl-4-2-ex3.svg

★ これは演習 3の「解答例」の図です。生徒が自分のかいた図と見くらべます。

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


fig, ax = plt.subplots(figsize=(7.2, 5.0))

XS = [0, 5, 10, 15, 20]
CF = [0, 8, 28, 44, 50]

ax.plot(XS, CF, color=ACCENT, linewidth=2.0, marker="o", markersize=6)

ax.plot([0, 9.25], [25, 25], color=WARM, linewidth=1.4,
        linestyle=(0, (5, 4)))
ax.plot([9.25, 9.25], [25, 0], color=WARM, linewidth=1.4,
        linestyle=(0, (5, 4)))
ax.plot([9.25], [25], marker="o", markersize=7, color=WARM, zorder=6)
ax.annotate("median $\\approx 9.25$", (9.25, 0), textcoords="offset points",
            xytext=(8, 14), fontsize=11, color=WARM)
ax.text(0.3, 26.2, "$\\dfrac{n}{2} = 25$", fontsize=11, color=WARM)

ax.set_xlim(0, 21)
ax.set_ylim(0, 55)
ax.set_xticks(XS)
ax.set_xticklabels(["$%d$" % _v for _v in XS], fontsize=11)
ax.set_yticks(range(0, 55, 10))
ax.set_yticklabels(["$%d$" % _v for _v in range(0, 55, 10)], fontsize=11)
ax.grid(True, color="#e5e7eb", linewidth=0.8)
ax.set_axisbelow(True)
for _s in ("top", "right"):
    ax.spines[_s].set_visible(False)
ax.set_xlabel("time $t$ (minutes)", fontsize=11, color=INK)
ax.set_ylabel("cumulative frequency", fontsize=11, color=INK)
ax.set_title("the graph starts at $(0,\\ 0)$, the lower boundary of the "
             "first class", fontsize=10, color=INK, loc="left", pad=10)

fig.tight_layout()
path = os.path.join(OUT, "aasl-4-2-ex3.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
