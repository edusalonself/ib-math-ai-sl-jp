"""AA SL 2.8 の図をつくる。

    python3 figs/aa-sl/make_aasl_2_8.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_2_8.py  … 目視用の PNG も

出力: aa-sl/02-functions/img/aasl-2-8-idea.svg

(a) y = 1/x のグラフ。2 本の漸近線と、y = x についての対称性。
(b) y = (ax+b)/(cx+d) のグラフ。垂直漸近線 x = -d/c と水平漸近線 y = a/c。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に例題・演習の答えを書かないこと（具体的な漸近線の値は書かない）。
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
# (a) y = 1/x
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) The reciprocal function", fontsize=11, color=INK,
              loc="left", pad=10)
ax1.set_xlim(-4.2, 4.6)
ax1.set_ylim(-4.2, 4.6)
ax1.set_aspect("equal")
ax1.axis("off")

ax1.annotate("", xy=(4.2, 0), xytext=(-4.0, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax1.annotate("", xy=(0, 4.2), xytext=(0, -4.0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax1.text(4.3, -0.42, "$x$", fontsize=11, color=GREY, ha="center")
ax1.text(-0.42, 4.3, "$y$", fontsize=11, color=GREY, va="center")

t = np.linspace(0.25, 4.0, 300)
ax1.plot(t, 1 / t, color=ACCENT, linewidth=2.3)
ax1.plot(-t, -1 / t, color=ACCENT, linewidth=2.3)

d = np.linspace(-3.6, 3.6, 2)
ax1.plot(d, d, color=GREEN, linewidth=1.2, linestyle=(0, (5, 4)))
ax1.text(2.6, 3.2, "$y = x$", fontsize=10, color=GREEN)

ax1.text(2.5, 1.05, "$y = \\dfrac{1}{x}$", fontsize=12, color=ACCENT)
ax1.text(0.28, -2.7, "asymptote $x = 0$", fontsize=9.5, color=WARM)
ax1.text(-4.0, 0.3, "asymptote $y = 0$", fontsize=9.5, color=WARM)
ax1.text(-4.0, 4.0, "two branches;\nits own reflection in $y = x$",
         fontsize=9.5, color=INK, va="top")

# ══════════════════════════════════════════════════════════
# (b) y = (ax+b)/(cx+d)
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) A rational function", fontsize=11, color=INK,
              loc="left", pad=10)
ax2.set_xlim(-3.4, 7.4)
ax2.set_ylim(-4.4, 6.4)
ax2.axis("off")

VA, HA = 2.0, 1.0
ax2.annotate("", xy=(7.0, 0), xytext=(-3.0, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.annotate("", xy=(0, 6.0), xytext=(0, -4.0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.text(7.1, -0.45, "$x$", fontsize=11, color=GREY, ha="center")
ax2.text(-0.45, 6.1, "$y$", fontsize=11, color=GREY, va="center")

ax2.plot([VA, VA], [-4.0, 6.0], color=WARM, linewidth=1.3,
         linestyle=(0, (5, 4)))
ax2.plot([-3.0, 7.0], [HA, HA], color=WARM, linewidth=1.3,
         linestyle=(0, (5, 4)))

u = np.linspace(VA + 0.28, 7.0, 300)
ax2.plot(u, HA + 3.5 / (u - VA), color=ACCENT, linewidth=2.3)
v = np.linspace(-3.0, VA - 0.28, 300)
ax2.plot(v, HA + 3.5 / (v - VA), color=ACCENT, linewidth=2.3)

ax2.text(VA + 0.30, 5.6, "$x = -\\dfrac{d}{c}$", fontsize=11.5, color=WARM)
ax2.text(5.0, HA + 0.35, "$y = \\dfrac{a}{c}$", fontsize=11.5, color=WARM)
ax2.text(2.9, -3.9, "the two asymptotes and both axis\nintercepts must appear on a sketch",
         fontsize=9.5, color=INK, va="bottom")

for px, py in [(-1.5, HA + 3.5 / (-1.5 - VA)), (0, HA + 3.5 / (0 - VA))]:
    ax2.plot([px], [py], marker="o", markersize=5.5, color=INK, zorder=3)
ax2.text(-3.3, -2.6, "axis intercepts", fontsize=9.5, color=INK)
for px, py in [(-1.5, HA + 3.5 / (-1.5 - VA)), (0, HA + 3.5 / (0 - VA))]:
    ax2.annotate("", xy=(px, py), xytext=(-1.9, -2.4),
                 arrowprops=dict(arrowstyle="->", color=INK, linewidth=0.8))

fig.tight_layout(w_pad=2.2)
path = os.path.join(OUT, "aasl-2-8-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
