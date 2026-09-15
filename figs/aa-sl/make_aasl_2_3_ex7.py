"""AA SL 2.3 の演習 7 の解答図（y = (x+2)(x-4)）。

    python3 figs/aa-sl/make_aasl_2_3_ex7.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_2_3_ex7.py

出力: aa-sl/02-functions/img/aasl-2-3-ex7.svg

★ これは演習 7の「解答例」の図です。生徒が自分のかいた図と見くらべます。

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
OUT = os.path.join(HERE, "..", "..", "aa-sl", "02-functions", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
FILL = "#dbe8f5"


fig, ax = plt.subplots(figsize=(7.6, 5.4))

_x = np.linspace(-3, 5, 400)
ax.plot(_x, (_x + 2) * (_x - 4), color=ACCENT, linewidth=2.2)

ax.axhline(0, color=GREY, linewidth=1.0)
ax.axvline(0, color=GREY, linewidth=1.0)

PTS = [(-2, 0, "$(-2,\\ 0)$", 8, 10),
       (4, 0, "$(4,\\ 0)$", 6, 10),
       (0, -8, "$(0,\\ -8)$", -52, -18),
       (1, -9, "$(1,\\ -9)$", 8, -18)]
for _px, _py, _lab, _dx, _dy in PTS:
    ax.plot([_px], [_py], marker="o", markersize=6, color=WARM, zorder=5)
    ax.annotate(_lab, (_px, _py), textcoords="offset points",
                xytext=(_dx, _dy), fontsize=11, color=WARM)

for _px, _py, _lab, _dx, _dy in [(-3, 7, "$(-3,\\ 7)$", -46, 6),
                                 (5, 7, "$(5,\\ 7)$", 6, 6)]:
    ax.plot([_px], [_py], marker="o", markersize=6, color=INK, zorder=5)
    ax.annotate(_lab, (_px, _py), textcoords="offset points",
                xytext=(_dx, _dy), fontsize=11, color=INK)

ax.set_xlim(-4.2, 6.4)
ax.set_ylim(-11.5, 10.5)
ax.set_xticks([])
ax.set_yticks([])
for _s in ("top", "right", "left", "bottom"):
    ax.spines[_s].set_visible(False)
ax.text(6.2, 0.5, "$x$", fontsize=12, color=GREY, ha="right")
ax.text(0.25, 10.2, "$y$", fontsize=12, color=GREY, va="top")
ax.text(-4.0, -11.0,
        "the sketch is drawn only for $-3 \\leq x \\leq 5$; the two endpoints "
        "are marked", fontsize=10, color=INK, ha="left", va="bottom")

fig.tight_layout()
path = os.path.join(OUT, "aasl-2-3-ex7.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
