"""AA SL 3.7a の演習 1 の解答図（y = cos x, 0 ≤ x ≤ 2π）。

    python3 figs/aa-sl/make_aasl_3_7a_ex1.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_3_7a_ex1.py

出力: aa-sl/03-geometry/img/aasl-3-7a-ex1.svg

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
OUT = os.path.join(HERE, "..", "..", "aa-sl", "03-geometry", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
FILL = "#dbe8f5"


fig, ax = plt.subplots(figsize=(8.4, 4.4))

_t = np.linspace(0, 2 * np.pi, 500)
ax.plot(_t, np.cos(_t), color=ACCENT, linewidth=2.2)

ax.axhline(0, color=GREY, linewidth=1.0)
for _yy in (-1, 1):
    ax.plot([0, 2 * np.pi], [_yy, _yy], color=GREY, linewidth=0.9,
            linestyle=(0, (4, 4)))

TABLE = [(0.0, 1.0), (np.pi / 2, 0.0), (np.pi, -1.0),
         (3 * np.pi / 2, 0.0), (2 * np.pi, 1.0)]
for _px, _py in TABLE:
    ax.plot([_px], [_py], marker="o", markersize=6, color=WARM, zorder=5)

ax.annotate("$(0,\\ 1)$", (0, 1), textcoords="offset points",
            xytext=(4, 10), fontsize=11, color=WARM)
ax.annotate("$(2\\pi,\\ 1)$", (2 * np.pi, 1), textcoords="offset points",
            xytext=(-14, 10), fontsize=11, color=WARM, ha="right")
ax.annotate("$(\\pi,\\ -1)$", (np.pi, -1), textcoords="offset points",
            xytext=(6, -18), fontsize=11, color=WARM)

ax.set_xlim(-0.35, 2 * np.pi + 0.45)
ax.set_ylim(-1.5, 1.85)
ax.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi])
ax.set_xticklabels(["$0$", "$\\dfrac{\\pi}{2}$", "$\\pi$",
                    "$\\dfrac{3\\pi}{2}$", "$2\\pi$"], fontsize=11)
ax.set_yticks([-1, 0, 1])
ax.set_yticklabels(["$-1$", "$0$", "$1$"], fontsize=11)
for _s in ("top", "right", "left"):
    ax.spines[_s].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.text(2.2, 1.8,
        "plot the five values, then join them smoothly;\nboth endpoints "
        "are maximum points", fontsize=10, color=INK,
        ha="left", va="top")

fig.tight_layout()
path = os.path.join(OUT, "aasl-3-7a-ex1.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
