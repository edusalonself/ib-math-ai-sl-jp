"""AA SL 5.2 の演習 2 の図をつくる（f' のグラフを読ませる問題）。

    python3 figs/aa-sl/make_aasl_5_2_ex.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_2_ex.py

出力: aa-sl/05-calculus/img/aasl-5-2-ex.svg

f'(x) = (x + 1)(x - 2)(x - 4) / 4 のグラフ。
x 軸を -1、2、4 の 3 か所で横切ります。
★ これは演習の問題文の一部なので、目もりの数字を入れます。
   （答えそのものは書きません。読み取るのは生徒です。）

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * \\le \\ge は読めない → \\leq \\geq を使う
  * 日本語のグリフがない → ラベルはすべて英語
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "05-calculus", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"

ROOTS = (-1.0, 2.0, 4.0)


def fp(t):
    return (t + 1.0) * (t - 2.0) * (t - 4.0) / 4.0


fig, ax = plt.subplots(figsize=(7.6, 4.6))

T = np.linspace(-2.15, 5.15, 600)
ax.plot(T, fp(T), color=ACCENT, linewidth=2.0)
ax.set_xlim(-2.6, 5.6)
ax.set_ylim(-4.6, 5.4)
ax.axis("off")

ax.plot([-2.45, 5.45], [0, 0], color=GREY, linewidth=1.1)
ax.plot([0, 0], [-4.4, 5.1], color=GREY, linewidth=1.1)
ax.text(5.52, -0.05, "$x$", fontsize=11, color=GREY, va="center")
ax.text(-0.12, 5.25, "$y$", fontsize=11, color=GREY, ha="right")

for _x in (-2, -1, 1, 2, 3, 4, 5):
    ax.plot([_x, _x], [-0.13, 0.13], color=GREY, linewidth=1.0)
    ax.text(_x, -0.34, "$%d$" % _x, fontsize=10, color=INK, ha="center",
            va="top")
for _y in (-4, -2, 2, 4):
    ax.plot([-0.10, 0.10], [_y, _y], color=GREY, linewidth=1.0)
    ax.text(-0.20, _y, "$%d$" % _y, fontsize=10, color=INK, ha="right",
            va="center")

for _x in ROOTS:
    ax.plot([_x], [0], "o", color=ACCENT, markersize=6.5, zorder=3)

ax.text(4.95, fp(4.95) + 0.45, "$y = f'(x)$", fontsize=11, color=ACCENT,
        ha="right")

fig.tight_layout()
path = os.path.join(OUT, "aasl-5-2-ex.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))
print("  roots:", ROOTS)
print("  f'(-2) =", fp(-2.0), " f'(0) =", fp(0.0), " f'(3) =", fp(3.0),
      " f'(5) =", fp(5.0))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
