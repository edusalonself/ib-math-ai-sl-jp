"""AA SL 4.9 の図をつくる。

    python3 figs/aa-sl/make_aasl_4_9.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_4_9.py  … 目視用の PNG も

出力: aa-sl/04-statistics-and-probability/img/aasl-4-9-idea.svg

(a) 正規分布の曲線と 68 / 95 / 99.7 のめやす。
(b) 確率は面積。逆に、面積から値を求めるのが inverse normal。

★ 図は μ と σ の記号だけで描き、例題・演習の数値は使いません。
   (b) の面積は 0.8 にしてあります（0.75 は演習3 の Q3 の面積と同じなので避けた）。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * \\le \\ge は読めない → \\leq \\geq を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ PNG は目視用です。確認が終わったら消してください。
"""
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "04-statistics-and-probability", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
FILL = "#cfe0f2"
SHADE = "#f6d9ad"


def pdf(z):
    return np.exp(-z ** 2 / 2) / math.sqrt(2 * math.pi)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.6, 4.8))
Z = np.linspace(-3.9, 3.9, 800)
Y = pdf(Z)

# ══════════════════════════════════════════════════════════
# (a) 曲線と 68 / 95 / 99.7
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) The normal curve and the $68$–$95$–$99.7$ guide",
              fontsize=11, color=INK, loc="left", pad=12)
ax1.plot(Z, Y, color=ACCENT, linewidth=1.6)
ax1.fill_between(Z, 0, Y, where=(Z >= -1) & (Z <= 1), color=FILL)
ax1.set_xlim(-4.2, 4.2)
ax1.set_ylim(-0.13, 0.52)
ax1.axis("off")

ax1.plot([-4.0, 4.0], [0, 0], color=GREY, linewidth=1.0)
for _i, (_z, _lab) in enumerate([(-3, r"$\mu-3\sigma$"), (-2, r"$\mu-2\sigma$"),
                                 (-1, r"$\mu-\sigma$"), (0, r"$\mu$"),
                                 (1, r"$\mu+\sigma$"), (2, r"$\mu+2\sigma$"),
                                 (3, r"$\mu+3\sigma$")]):
    ax1.plot([_z, _z], [0, pdf(_z)], color=GREY, linewidth=0.8,
             linestyle=(0, (2, 2)))
    ax1.text(_z, -0.050 if _i % 2 == 1 else -0.098, _lab, fontsize=8.5,
             color=GREY, ha="center")

ax1.annotate("", xy=(1, 0.435), xytext=(-1, 0.435),
             arrowprops=dict(arrowstyle="<->", color=ACCENT, linewidth=1.1))
ax1.text(0, 0.448, "about $68\\%$", fontsize=9.5, color=ACCENT, ha="center")
ax1.annotate("", xy=(2, 0.478), xytext=(-2, 0.478),
             arrowprops=dict(arrowstyle="<->", color=WARM, linewidth=1.1))
ax1.text(0, 0.491, "about $95\\%$", fontsize=9.5, color=WARM, ha="center")

ax1.text(0.0, -0.20, "the curve is symmetric about $\\mu$; the total area\n"
         "under it is $1$", fontsize=9, color=INK, transform=ax1.transAxes,
         linespacing=1.6)
ax1.text(0.0, -0.34, "about $99.7\\%$ of the values lie between\n"
         "$\\mu-3\\sigma$ and $\\mu+3\\sigma$", fontsize=9, color=WARM,
         transform=ax1.transAxes, linespacing=1.6)

# ══════════════════════════════════════════════════════════
# (b) 面積から値へ、値から面積へ
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) A probability is an area; the inverse goes the other way",
              fontsize=11, color=INK, loc="left", pad=12)
ax2.plot(Z, Y, color=ACCENT, linewidth=1.6)
K = 0.8416212335729144       # z with area 0.8 to the left
ax2.fill_between(Z, 0, Y, where=(Z <= K), color=SHADE)
ax2.set_xlim(-4.2, 4.2)
ax2.set_ylim(-0.13, 0.52)
ax2.axis("off")

ax2.plot([-4.0, 4.0], [0, 0], color=GREY, linewidth=1.0)
ax2.plot([K, K], [0, pdf(K)], color=WARM, linewidth=1.4)
ax2.text(K, -0.055, "$k$", fontsize=10, color=WARM, ha="center")
ax2.plot([0, 0], [0, pdf(0)], color=GREY, linewidth=0.8,
         linestyle=(0, (2, 2)))
ax2.text(0, -0.055, "$\\mu$", fontsize=9.5, color=GREY, ha="center")

ax2.text(-1.35, 0.07, "area $= 0.8$", fontsize=10, color=WARM)
ax2.annotate("", xy=(1.45, 0.055), xytext=(2.6, 0.16),
             arrowprops=dict(arrowstyle="->", color=ACCENT, linewidth=1.1))
ax2.text(2.35, 0.175, "the rest", fontsize=9.5, color=ACCENT)

ax2.text(0.0, -0.20, "given $k$, the shaded area is $P(X \\leq k)$: this is\n"
         "the normal probability calculation", fontsize=9, color=INK,
         transform=ax2.transAxes, linespacing=1.6)
ax2.text(0.0, -0.34, "given the area, finding $k$ is the inverse normal\n"
         "calculation: the area is given and $k$ is read off",
         fontsize=9, color=WARM, transform=ax2.transAxes, linespacing=1.6)

fig.tight_layout(w_pad=2.2)
path = os.path.join(OUT, "aasl-4-9-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))
print("  area to k =", round(0.5 * (1 + math.erf(K / math.sqrt(2))), 6),
      " (0.8 にしてある)")

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
