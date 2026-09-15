"""AA SL 2.9 の演習 2 の解答図（y = (1/2)^x と y = log_(1/2) x）。

    python3 figs/aa-sl/make_aasl_2_9_ex2.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_2_9_ex2.py

出力: aa-sl/02-functions/img/aasl-2-9-ex2.svg

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
OUT = os.path.join(HERE, "..", "..", "aa-sl", "02-functions", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
FILL = "#dbe8f5"


fig, ax = plt.subplots(figsize=(6.6, 6.2))

_x = np.linspace(-4.2, 4.2, 500)
_e = 0.5 ** _x
_m = _e <= 4.6
ax.plot(_x[_m], _e[_m], color=ACCENT, linewidth=2.2)

_u = np.linspace(0.02, 4.6, 500)
_l = np.log(_u) / np.log(0.5)
_n = np.abs(_l) <= 4.6
ax.plot(_u[_n], _l[_n], color=WARM, linewidth=2.2)

_d = np.linspace(-4.4, 4.4, 20)
ax.plot(_d, _d, color=GREY, linewidth=1.0, linestyle=(0, (4, 4)))

ax.axhline(0, color=GREY, linewidth=1.0)
ax.axvline(0, color=GREY, linewidth=1.0)

for _px, _py, _c in [(0, 1, ACCENT), (1, 0, WARM)]:
    ax.plot([_px], [_py], marker="o", markersize=6, color=_c, zorder=5)
ax.annotate("$(0,\\ 1)$", (0, 1), textcoords="offset points",
            xytext=(-58, 8), fontsize=11, color=ACCENT)
ax.annotate("$(1,\\ 0)$", (1, 0), textcoords="offset points",
            xytext=(8, -20), fontsize=11, color=WARM)

ax.text(-3.9, 4.3, "$y = \\left(\\dfrac{1}{2}\\right)^{x}$", fontsize=12,
        color=ACCENT, va="top")
ax.text(3.4, -3.5, "$y = \\log_{\\frac{1}{2}} x$", fontsize=12, color=WARM,
        ha="right")
ax.text(3.9, 3.6, "$y = x$", fontsize=11, color=GREY, ha="right")

ax.set_xlim(-4.6, 4.6)
ax.set_ylim(-4.6, 4.9)
ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect("equal")
for _s in ("top", "right", "left", "bottom"):
    ax.spines[_s].set_visible(False)
ax.text(-4.5, -4.5,
        "each curve is the reflection of the other in $y = x$; both are "
        "decreasing", fontsize=10, color=INK, ha="left", va="bottom")

fig.tight_layout()
path = os.path.join(OUT, "aasl-2-9-ex2.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
