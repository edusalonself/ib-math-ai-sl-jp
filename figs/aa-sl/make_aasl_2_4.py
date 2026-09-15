"""AA SL 2.4 の図をつくる。

    python3 figs/aa-sl/make_aasl_2_4.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_2_4.py  … 目視用の PNG も

出力: aa-sl/02-functions/img/aasl-2-4-idea.svg

(a) 曲線の key features（切片・極大・極小）。
(b) 垂直漸近線と水平漸近線。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に演習の答えを書かないこと（数値の座標は一切書かない）。
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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.4))

# ══════════════════════════════════════════════════════════
# (a) key features
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Key features of a graph", fontsize=11, color=INK,
              loc="left", pad=10)
ax1.set_xlim(-3.4, 4.2)
ax1.set_ylim(-4.4, 5.0)
ax1.axis("off")

ax1.annotate("", xy=(4.0, 0), xytext=(-3.2, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax1.annotate("", xy=(0, 4.8), xytext=(0, -4.2),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax1.text(4.1, -0.36, "$x$", fontsize=11, color=GREY, ha="center")
ax1.text(-0.26, 4.9, "$y$", fontsize=11, color=GREY, va="center")


def cub(v):
    return 0.55 * (v + 2.0) * v * (v - 2.6)


xs = np.linspace(-2.7, 3.2, 300)
ax1.plot(xs, cub(xs), color=ACCENT, linewidth=2.2)
ax1.text(0.9, 4.2, "$y = f(x)$", fontsize=12, color=ACCENT)

for px in (-2.0, 0.0, 2.6):
    ax1.plot([px], [0], marker="o", markersize=6, color=WARM, zorder=3)

# 極大・極小（数値ではなく名前だけ）
lo = np.linspace(-2.0, 0.0, 400)
hi = np.linspace(0.0, 2.6, 400)
mx = lo[np.argmax(cub(lo))]
mn = hi[np.argmin(cub(hi))]
ax1.plot([mx], [cub(mx)], marker="o", markersize=6, color=INK, zorder=3)
ax1.plot([mn], [cub(mn)], marker="o", markersize=6, color=INK, zorder=3)

ax1.annotate("local maximum", xy=(mx, cub(mx)), xytext=(-3.3, 4.3),
             fontsize=10, color=INK,
             arrowprops=dict(arrowstyle="->", color=INK, linewidth=0.9))
ax1.annotate("local minimum", xy=(mn, cub(mn)), xytext=(1.5, -4.2),
             fontsize=10, color=INK,
             arrowprops=dict(arrowstyle="->", color=INK, linewidth=0.9))
ax1.annotate("zeros of $f$", xy=(-2.0, 0),
             xytext=(-3.1, 1.6), fontsize=10, color=WARM,
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=0.9))
ax1.annotate("", xy=(2.6, 0), xytext=(-1.7, 1.45),
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=0.9))

# ══════════════════════════════════════════════════════════
# (b) 漸近線
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) Vertical and horizontal asymptotes", fontsize=11,
              color=INK, loc="left", pad=10)
ax2.set_xlim(-2.6, 5.4)
ax2.set_ylim(-1.6, 6.4)
ax2.axis("off")

ax2.annotate("", xy=(5.2, 0), xytext=(-2.4, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.annotate("", xy=(0, 6.2), xytext=(0, -1.4),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.text(5.3, -0.36, "$x$", fontsize=11, color=GREY, ha="center")
ax2.text(-0.26, 6.3, "$y$", fontsize=11, color=GREY, va="center")

VA, HA = 2.0, 3.0
ax2.plot([VA, VA], [-1.3, 6.1], color=WARM, linewidth=1.4,
         linestyle=(0, (6, 4)))
ax2.plot([-2.3, 5.1], [HA, HA], color=WARM, linewidth=1.4,
         linestyle=(0, (6, 4)))

left = np.linspace(-2.3, VA - 0.13, 300)
right = np.linspace(VA + 0.13, 5.1, 300)
ax2.plot(left, 1.0 / (left - VA) + HA, color=ACCENT, linewidth=2.2)
ax2.plot(right, 1.0 / (right - VA) + HA, color=ACCENT, linewidth=2.2)

ax2.text(VA + 0.16, 6.0, "vertical asymptote", fontsize=10, color=WARM,
         ha="left", va="top")
ax2.text(5.1, HA - 0.22, "horizontal asymptote", fontsize=10, color=WARM,
         ha="right", va="top")
ax2.text(-2.3, 5.4, "the curve gets closer and closer\n"
         "to each dashed line as it runs out\nto the edges of the picture",
         fontsize=9.5, color=INK, va="top")

fig.tight_layout(w_pad=2.4)
path = os.path.join(OUT, "aasl-2-4-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
