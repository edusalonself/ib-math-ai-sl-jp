"""AA SL 4.2 の演習 5 の解答図（外れ値を含む箱ひげ図）。

    python3 figs/aa-sl/make_aasl_4_2_ex5.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_4_2_ex5.py

出力: aa-sl/04-statistics-and-probability/img/aasl-4-2-ex5.svg

★ これは演習 5の「解答例」の図です。生徒が自分のかいた図と見くらべます。

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


fig, ax = plt.subplots(figsize=(7.6, 3.2))

MIN, Q1, MED, Q3, WHIS, OUTLIER = 12, 20, 26, 30, 33, 48
YC, HH = 0.0, 0.34

ax.add_patch(plt.Rectangle((Q1, YC - HH), Q3 - Q1, 2 * HH, facecolor=FILL,
                           edgecolor=ACCENT, linewidth=1.6))
ax.plot([MED, MED], [YC - HH, YC + HH], color=ACCENT, linewidth=2.0)
ax.plot([MIN, Q1], [YC, YC], color=ACCENT, linewidth=1.6)
ax.plot([Q3, WHIS], [YC, YC], color=ACCENT, linewidth=1.6)
for _v in (MIN, WHIS):
    ax.plot([_v, _v], [YC - 0.18, YC + 0.18], color=ACCENT, linewidth=1.6)

ax.plot([OUTLIER], [YC], marker="x", markersize=11, markeredgewidth=2.2,
        color=WARM)
ax.annotate("outlier $48$", (OUTLIER, YC), textcoords="offset points",
            xytext=(-14, 22), fontsize=11, color=WARM, ha="center")

for _v, _lab in [(MIN, "$12$"), (Q1, "$20$"), (MED, "$26$"), (Q3, "$30$"),
                 (WHIS, "$33$")]:
    ax.text(_v, YC - HH - 0.30, _lab, fontsize=11, color=INK, ha="center")

ax.set_xlim(8, 52)
ax.set_ylim(-1.15, 1.05)
ax.set_xticks(range(10, 51, 10))
ax.set_xticklabels(["$%d$" % _v for _v in range(10, 51, 10)], fontsize=11)
ax.set_yticks([])
for _s in ("top", "right", "left"):
    ax.spines[_s].set_visible(False)
ax.set_title("the whisker stops at $33$, the largest value that is not an "
             "outlier; $48$ is plotted as a cross", fontsize=10, color=INK,
             loc="left", pad=10)

fig.tight_layout()
path = os.path.join(OUT, "aasl-4-2-ex5.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
