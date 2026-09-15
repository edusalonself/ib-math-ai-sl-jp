"""AA SL 2.8 の演習 9 の解答図（y = (2x+1)/(x-1)）。

    python3 figs/aa-sl/make_aasl_2_8_ex9.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_2_8_ex9.py

出力: aa-sl/02-functions/img/aasl-2-8-ex9.svg

★ これは演習 9の「解答例」の図です。生徒が自分のかいた図と見くらべます。

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


fig, ax = plt.subplots(figsize=(7.4, 5.6))

for _lo, _hi in ((-6.0, 0.94), (1.06, 8.0)):
    _x = np.linspace(_lo, _hi, 600)
    _y = (2 * _x + 1) / (_x - 1)
    _m = np.abs(_y) <= 12
    ax.plot(_x[_m], _y[_m], color=ACCENT, linewidth=2.2)

ax.plot([1, 1], [-12, 12], color=GREY, linewidth=1.2, linestyle=(0, (5, 4)))
ax.plot([-6, 8], [2, 2], color=GREY, linewidth=1.2, linestyle=(0, (5, 4)))
ax.text(1.2, 9.6, "$x = 1$", fontsize=11, color=GREY)
ax.text(-5.6, 2.6, "$y = 2$", fontsize=11, color=GREY)

ax.axhline(0, color=GREY, linewidth=1.0)
ax.axvline(0, color=GREY, linewidth=1.0)

for _px, _py, _lab, _dx, _dy in [(-0.5, 0, "$\\left(-\\dfrac{1}{2},\\ 0\\right)$", -110, 6),
                                 (0, -1, "$(0,\\ -1)$", -70, -6)]:
    ax.plot([_px], [_py], marker="o", markersize=6, color=WARM, zorder=5)
    ax.annotate(_lab, (_px, _py), textcoords="offset points",
                xytext=(_dx, _dy), fontsize=11, color=WARM)

ax.set_xlim(-6, 8)
ax.set_ylim(-12, 12)
ax.set_xticks([])
ax.set_yticks([])
for _s in ("top", "right", "left", "bottom"):
    ax.spines[_s].set_visible(False)
ax.text(7.8, 0.6, "$x$", fontsize=12, color=GREY, ha="right")
ax.text(0.25, 11.6, "$y$", fontsize=12, color=GREY, va="top")
ax.text(-5.9, -11.6,
        "two branches, one on each side of $x = 1$; both approach $y = 2$",
        fontsize=10, color=INK, ha="left", va="bottom")

fig.tight_layout()
path = os.path.join(OUT, "aasl-2-8-ex9.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
