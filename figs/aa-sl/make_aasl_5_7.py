"""AA SL 5.7 の図をつくる。

    python3 figs/aa-sl/make_aasl_5_7.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_7.py

出力: aa-sl/05-calculus/img/aasl-5-7-idea-a.svg

(a) f、f'、f'' の 3 つのグラフを、x をそろえて縦に並べる。

★ 式は書きません（例題・演習と重ならないように）。曲線の形だけを見せます。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * \\le \\ge は読めない → \\leq \\geq を使う
  * \\bigl \\bigr \\Box は読めない → ふつうの ( ) と文字を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "05-calculus", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
FILL = "#e8f0f9"
SHADE = "#fdf0dc"

# f(x) = x^3 - 3x^2   （例題・演習では使わない関数）
X = np.linspace(-0.9, 3.1, 400)
F = X ** 3 - 3 * X ** 2
F1 = 3 * X ** 2 - 6 * X
F2 = 6 * X - 6

fig1 = plt.figure(figsize=(6.2, 6.2))
gs = GridSpec(3, 1, figure=fig1, hspace=0.55,
              left=0.10, right=0.97, top=0.90, bottom=0.07)

ax_a = [fig1.add_subplot(gs[i, 0]) for i in range(3)]

TITLES = ("$y = f(x)$", "$y = f'(x)$", "$y = f''(x)$")
CURVES = (F, F1, F2)
COLS = (INK, ACCENT, WARM)
YLIMS = ((-4.6, 1.6), (-4.6, 12.5), (-12.5, 14.0))

for _ax, _y, _t, _c, _lim in zip(ax_a, CURVES, TITLES, COLS, YLIMS):
    _ax.plot(X, _y, color=_c, linewidth=2.0)
    _ax.axhline(0, color=GREY, linewidth=0.9)
    _ax.set_xlim(-0.9, 3.1)
    _ax.set_ylim(*_lim)
    _ax.set_xticks([0, 1, 2])
    _ax.set_yticks([])
    for _s in ("top", "right", "left", "bottom"):
        _ax.spines[_s].set_visible(False)
    _ax.tick_params(axis="x", colors=GREY, labelsize=9, length=0)
    _ax.text(0.0, 1.04, _t, transform=_ax.transAxes, fontsize=11.5,
             color=_c, ha="left", va="bottom")
    for _v in (0, 1, 2):
        _ax.axvline(_v, color=GREY, linewidth=0.7, linestyle=(0, (3, 3)),
                    alpha=0.75)

ax_a[0].set_title("The same $x$ on all three graphs", fontsize=11,
                  color=INK, loc="left", pad=26)

AR = dict(arrowstyle="->", linewidth=1.0)
ax_a[0].annotate("steepest downwards", xy=(1.0, -2.1), xytext=(-0.85, -3.9),
                 fontsize=9, color=GREY,
                 arrowprops=dict(color=GREY, **AR))
ax_a[0].annotate("flat", xy=(2.03, -3.85), xytext=(2.45, -1.2),
                 fontsize=9, color=GREY,
                 arrowprops=dict(color=GREY, **AR))
ax_a[1].annotate("lowest here", xy=(1.0, -2.6), xytext=(1.12, 3.2),
                 fontsize=9, color=ACCENT,
                 arrowprops=dict(color=ACCENT, **AR))
ax_a[1].annotate("zero here", xy=(2.02, -0.3), xytext=(2.30, -3.4),
                 fontsize=9, color=ACCENT,
                 arrowprops=dict(color=ACCENT, **AR))
ax_a[2].annotate("zero here", xy=(1.02, -0.4), xytext=(1.30, -8.0),
                 fontsize=9, color=WARM,
                 arrowprops=dict(color=WARM, **AR))
ax_a[2].set_xlabel("$x$", fontsize=10, color=GREY, labelpad=2)

for _fig, _name in ((fig1, "aasl-5-7-idea-a.svg"),):
    _p = os.path.join(OUT, _name)
    _fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
    print("wrote", os.path.normpath(_p))
    if os.environ.get("FIG_PNG"):
        _q = _p[:-4] + ".png"
        _fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                     facecolor="white")
        print("wrote", os.path.normpath(_q))
