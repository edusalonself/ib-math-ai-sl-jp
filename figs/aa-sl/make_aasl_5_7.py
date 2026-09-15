"""AA SL 5.7 の図をつくる。

    python3 figs/aa-sl/make_aasl_5_7.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_7.py

出力: aa-sl/05-calculus/img/aasl-5-7-idea.svg

(a) f、f'、f'' の 3 つのグラフを、x をそろえて縦に並べる。
(b) f'' の符号と f' の増減の対応。

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

fig = plt.figure(figsize=(11.2, 6.2))
gs = GridSpec(3, 2, figure=fig, width_ratios=[1.15, 1.0], hspace=0.55,
              wspace=0.30)

ax_a = [fig.add_subplot(gs[i, 0]) for i in range(3)]
ax_b = fig.add_subplot(gs[:, 1])

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

ax_a[0].set_title("(a) The same $x$ on all three graphs", fontsize=11,
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

# ══════════════════════════════════════════════════════════
# (b) f'' の符号と f' の増減
# ══════════════════════════════════════════════════════════
ax_b.set_title("(b) What the sign of $f''$ tells you", fontsize=11,
               color=INK, loc="left", pad=10)
ax_b.set_xlim(0, 10)
ax_b.set_ylim(0, 10)
ax_b.axis("off")

BOX1 = dict(boxstyle="round,pad=0.35", facecolor=SHADE, edgecolor=WARM,
            linewidth=1.2)
BOX2 = dict(boxstyle="round,pad=0.35", facecolor=FILL, edgecolor=ACCENT,
            linewidth=1.2)

ROWS = (("$f''(x) > 0$", "$f'$ is increasing there"),
        ("$f''(x) < 0$", "$f'$ is decreasing there"),
        ("$f''(a) = 0$", "the graph of $f'$ is flat at $x = a$"))
YS = (8.4, 6.8, 5.2)
for _y, (_l, _r) in zip(YS, ROWS):
    ax_b.text(1.7, _y, _l, fontsize=12.5, color=WARM, ha="center",
              va="center", bbox=BOX1)
    ax_b.annotate("", xy=(4.05, _y), xytext=(3.15, _y),
                  arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.3))
    ax_b.text(6.6, _y, _r, fontsize=11, color=ACCENT, ha="center",
              va="center", bbox=BOX2)

ax_b.plot([0.2, 9.8], [3.9, 3.9], color=GREY, linewidth=0.9)
ax_b.text(0.25, 3.00, "differentiate once to go from $f$ to $f'$,",
          fontsize=10, color=INK, va="center")
ax_b.text(0.25, 2.25, "and once more to go from $f'$ to $f''$",
          fontsize=10, color=INK, va="center")
ax_b.text(0.25, 1.35, "the same reading works between $f\'$ and $f\'\'$",
          fontsize=9.5, color=GREY, va="center")

path = os.path.join(OUT, "aasl-5-7-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
