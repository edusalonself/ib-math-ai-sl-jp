"""AA SL 4.9 の例題（片側 5% の図）の解答図。

    python3 figs/aa-sl/make_aasl_4_9_tail.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_4_9_tail.py

出力: aa-sl/04-statistics-and-probability/img/aasl-4-9-tail.svg

★ これは例題 3 (b)の「解答例」の図です。生徒が自分のかいた図と見くらべます。

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


fig, ax = plt.subplots(figsize=(7.8, 4.2))

MU, SD = 500.0, 40.0
K = 565.79  # invNorm(0.95, 500, 40)

_x = np.linspace(MU - 4 * SD, MU + 4 * SD, 600)
_y = np.exp(-0.5 * ((_x - MU) / SD) ** 2) / (SD * np.sqrt(2 * np.pi))
ax.plot(_x, _y, color=ACCENT, linewidth=2.0)

_m = _x >= K
ax.fill_between(_x[_m], 0, _y[_m], color=ACCENT, alpha=0.35)

ax.plot([MU, MU], [0, np.exp(0) / (SD * np.sqrt(2 * np.pi))], color=GREY,
        linewidth=1.1, linestyle=(0, (5, 4)))
ax.plot([K, K], [0, np.exp(-0.5 * ((K - MU) / SD) ** 2)
                 / (SD * np.sqrt(2 * np.pi))], color=WARM, linewidth=1.4)

ax.axhline(0, color=GREY, linewidth=1.0)
ax.set_xlim(MU - 4 * SD, MU + 4 * SD)
ax.set_ylim(-0.0012, 0.0125)
ax.set_xticks([MU, K])
ax.set_xticklabels(["$500$", "$566$"], fontsize=11)
ax.set_yticks([])
for _s in ("top", "right", "left", "bottom"):
    ax.spines[_s].set_visible(False)

ax.annotate("area $= 0.05$", (K + 30, 0.0012), textcoords="offset points",
            xytext=(6, 26), fontsize=11, color=WARM,
            arrowprops=dict(arrowstyle="->", color=WARM, linewidth=1.1))
ax.text(MU - 155, 0.0115,
        "area to the left of the line is $0.95$, so the shaded tail is $0.05$",
        fontsize=10, color=INK, ha="left", va="top")

fig.tight_layout()
path = os.path.join(OUT, "aasl-4-9-tail.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
