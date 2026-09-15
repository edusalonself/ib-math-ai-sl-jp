"""AA SL 2.10 の図をつくる。

    python3 figs/aa-sl/make_aasl_2_10.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_2_10.py  … 目視用の PNG も

出力: aa-sl/02-functions/img/aasl-2-10-idea.svg

(a) f(x) = g(x) の解は、2 つのグラフの交点の x 座標。差 f - g の零点でもある。
(b) e^x = sin x のように、習った方法では解けない方程式もある。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に例題・演習の答えを書かないこと（解は x1, x2 と文字で書く）。
★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "02-functions", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
GREEN = "#15803d"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.8))

# ══════════════════════════════════════════════════════════
# (a) 交点として見る／差の零点として見る
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Two ways to see a solution", fontsize=11, color=INK,
              loc="left", pad=10)
ax1.set_xlim(-3.6, 4.4)
ax1.set_ylim(-6.9, 9.4)
ax1.axis("off")

ax1.annotate("", xy=(4.1, 0), xytext=(-3.3, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax1.annotate("", xy=(0, 9.1), xytext=(0, -6.6),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax1.text(4.2, -0.7, "$x$", fontsize=11, color=GREY, ha="center")
ax1.text(-0.5, 9.2, "$y$", fontsize=11, color=GREY, va="center")

t = np.linspace(-3.1, 3.5, 300)
FX = 0.7 * t ** 2 - 1.0
GX = 1.0 * t + 3.5
ax1.plot(t, FX, color=ACCENT, linewidth=2.2)
ax1.plot(t, GX, color=WARM, linewidth=2.0)
ax1.plot(t, FX - GX, color=GREEN, linewidth=1.8, linestyle=(0, (5, 3)))

# 交点（0.7x^2 - 1 = x + 1.4  ->  0.7x^2 - x - 2.4 = 0）
r = np.roots([0.7, -1.0, -4.5])
for xr in sorted(r):
    yr = 0.7 * xr ** 2 - 1.0
    ax1.plot([xr], [yr], marker="o", markersize=6, color=INK, zorder=3)
    ax1.plot([xr], [0], marker="o", markersize=5, color=GREEN, zorder=3)
    ax1.plot([xr, xr], [0, yr], color=GREY, linewidth=0.9,
             linestyle=(0, (2, 3)))
ax1.text(sorted(r)[0] - 0.18, -1.15, "$x_{1}$", fontsize=11, color=INK)
ax1.text(sorted(r)[1] - 0.18, -1.15, "$x_{2}$", fontsize=11, color=INK)

ax1.text(1.35, 8.4, "$y = f(x)$", fontsize=10.5, color=ACCENT)
ax1.text(-3.5, 1.2, "$y = g(x)$", fontsize=10.5, color=WARM)
ax1.text(1.15, -5.3, "$y = f(x) - g(x)$", fontsize=10.5, color=GREEN)
ax1.text(-3.5, -6.8, "the crossings of $f$ and $g$ sit above the zeros of $f - g$",
         fontsize=9.5, color=INK, va="bottom")

# ══════════════════════════════════════════════════════════
# (b) e^x = sin x
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) When no method reaches it", fontsize=11, color=INK,
              loc="left", pad=10)
ax2.set_xlim(-9.6, 3.2)
ax2.set_ylim(-1.9, 3.1)
ax2.axis("off")

ax2.annotate("", xy=(2.9, 0), xytext=(-9.3, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.annotate("", xy=(0, 2.9), xytext=(0, -1.7),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.text(3.0, -0.32, "$x$", fontsize=11, color=GREY, ha="center")
ax2.text(-0.45, 3.0, "$y$", fontsize=11, color=GREY, va="center")

v = np.linspace(-9.3, 1.05, 700)
ax2.plot(v, np.exp(v), color=ACCENT, linewidth=2.2)
ax2.plot(v, np.sin(v), color=WARM, linewidth=2.0)

# 交点を数値で拾って印だけ付ける（値は書かない）
prev = np.exp(v) - np.sin(v)
for i in range(len(v) - 1):
    if prev[i] * prev[i + 1] < 0:
        xm = 0.5 * (v[i] + v[i + 1])
        ax2.plot([xm], [np.sin(xm)], marker="o", markersize=5, color=INK,
                 zorder=3)

ax2.text(1.2, 2.45, "$y = e^{x}$", fontsize=10.5, color=ACCENT)
ax2.text(-4.6, 1.25, "$y = \\sin x$", fontsize=10.5, color=WARM)
ax2.text(-9.5, -1.88, "at SL, these crossings are found with technology",
         fontsize=9.5, color=INK, va="bottom")

fig.tight_layout(w_pad=2.2)
path = os.path.join(OUT, "aasl-2-10-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
