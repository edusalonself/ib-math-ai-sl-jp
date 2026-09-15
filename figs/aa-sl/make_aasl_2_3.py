"""AA SL 2.3 の図をつくる。

    python3 figs/aa-sl/make_aasl_2_3.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_2_3.py  … 目視用の PNG も

出力: aa-sl/02-functions/img/aasl-2-3-idea.svg

(a) sketch にラベルする key features。
(b) 和のグラフは、同じ x での y の値を足したもの。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に演習の答えを書かないこと（座標の数値は書かない）。
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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.4))

# ══════════════════════════════════════════════════════════
# (a) sketch にラベルするもの
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) What a sketch must show", fontsize=11, color=INK,
              loc="left", pad=10)
ax1.set_xlim(-3.8, 4.6)
ax1.set_ylim(-3.4, 4.6)
ax1.axis("off")

ax1.annotate("", xy=(4.4, 0), xytext=(-2.8, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax1.annotate("", xy=(0, 4.4), xytext=(0, -3.2),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax1.text(4.5, -0.32, "$x$", fontsize=11, color=GREY, ha="center")
ax1.text(-0.28, 4.5, "$y$", fontsize=11, color=GREY, va="center")

xs = np.linspace(-1.9, 3.6, 200)
ys = (xs + 1.4) * (xs - 3.0) * 0.55
ax1.plot(xs, ys, color=ACCENT, linewidth=2.2)
ax1.text(2.4, 3.0, "$y = f(x)$", fontsize=12, color=ACCENT)

for px in (-1.4, 3.0):
    ax1.plot([px], [0], marker="o", markersize=6, color=WARM, zorder=3)
ax1.plot([0], [(0 + 1.4) * (0 - 3.0) * 0.55], marker="o", markersize=6,
         color=WARM, zorder=3)
vx = (3.0 - 1.4) / 2
ax1.plot([vx], [(vx + 1.4) * (vx - 3.0) * 0.55], marker="o", markersize=6,
         color=WARM, zorder=3)

ax1.annotate("$x$-intercepts", xy=(-1.4, 0), xytext=(-2.9, 1.5),
             fontsize=10, color=WARM,
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=0.9))
ax1.annotate("", xy=(3.0, 0), xytext=(-1.55, 1.35),
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=0.9))
ax1.annotate("$y$-intercept", xy=(0, -2.31), xytext=(-2.9, -2.5),
             fontsize=10, color=WARM,
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=0.9))
ax1.annotate("minimum point", xy=(vx, (vx + 1.4) * (vx - 3.0) * 0.55),
             xytext=(1.7, -3.15), fontsize=10, color=WARM,
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=0.9))

ax1.text(-3.7, 4.5, "label the axes, every intercept,\n"
         "every maximum and minimum,\nand the curve itself",
         fontsize=9.5, color=INK, va="top")

# ══════════════════════════════════════════════════════════
# (b) 和のグラフ
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) Adding two graphs", fontsize=11, color=INK,
              loc="left", pad=10)
ax2.set_xlim(-0.6, 4.4)
ax2.set_ylim(-0.9, 5.4)
ax2.axis("off")

ax2.annotate("", xy=(4.2, 0), xytext=(-0.4, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.annotate("", xy=(0, 5.2), xytext=(0, -0.7),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.text(4.3, -0.32, "$x$", fontsize=11, color=GREY, ha="center")
ax2.text(-0.28, 5.3, "$y$", fontsize=11, color=GREY, va="center")

u = np.linspace(0.05, 3.9, 120)
fv = 0.35 * u + 0.6
gv = 2.6 - 0.42 * u
ax2.plot(u, fv, color=ACCENT, linewidth=2.0)
ax2.plot(u, gv, color=GREEN, linewidth=2.0)
ax2.plot(u, fv + gv, color=WARM, linewidth=2.2)

ax2.text(3.95, 0.35 * 3.9 + 0.78, "$y = f(x)$", fontsize=10, color=ACCENT,
         ha="right", va="bottom")
ax2.text(0.1, 2.85, "$y = g(x)$", fontsize=10, color=GREEN)
ax2.text(2.05, 3.65, "$y = f(x) + g(x)$", fontsize=11, color=WARM)

p = 1.6
fp, gp = 0.35 * p + 0.6, 2.6 - 0.42 * p
ax2.plot([p, p], [0, fp + gp], color=GREY, linewidth=1.0,
         linestyle=(0, (3, 3)))
for hv, col in [(fp, ACCENT), (gp, GREEN), (fp + gp, WARM)]:
    ax2.plot([p], [hv], marker="o", markersize=5.5, color=col, zorder=3)
ax2.text(p + 0.16, (fp + gp) / 2, "heights add", fontsize=10, color=INK,
         ha="left", va="center")
ax2.text(2.0, -0.8, "at each $x$, add the two $y$-values", fontsize=9.5,
         color=INK, ha="center")

fig.tight_layout(w_pad=2.4)
path = os.path.join(OUT, "aasl-2-3-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
