"""AA SL 2.6 の図をつくる。

    python3 figs/aa-sl/make_aasl_2_6.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_2_6.py  … 目視用の PNG も

出力: aa-sl/02-functions/img/aasl-2-6-idea.svg

(a) 3 つの形は、それぞれちがう特徴をすぐ見せてくれる。
(b) a の符号と大きさが、形を決める。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に演習の答えを書かないこと（数値の座標は書かない）。
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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.6))

# ══════════════════════════════════════════════════════════
# (a) 3 つの形が見せてくれるもの
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Each form shows a different feature", fontsize=11,
              color=INK, loc="left", pad=10)
ax1.set_xlim(-3.4, 5.6)
ax1.set_ylim(-4.6, 5.2)
ax1.axis("off")

ax1.annotate("", xy=(5.4, 0), xytext=(-3.2, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax1.annotate("", xy=(0, 5.0), xytext=(0, -4.0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax1.text(5.5, -0.36, "$x$", fontsize=11, color=GREY, ha="center")
ax1.text(-0.26, 5.1, "$y$", fontsize=11, color=GREY, va="center")

P, Q, A = -2.0, 4.0, 0.42
xs = np.linspace(-2.9, 4.9, 300)
ax1.plot(xs, A * (xs - P) * (xs - Q), color=ACCENT, linewidth=2.2)

H = (P + Q) / 2
K = A * (H - P) * (H - Q)
ax1.plot([H, H], [-4.0, 5.0], color=GREY, linewidth=1.0,
         linestyle=(0, (5, 4)))

for px in (P, Q):
    ax1.plot([px], [0], marker="o", markersize=6, color=WARM, zorder=3)
ax1.plot([0], [A * (0 - P) * (0 - Q)], marker="o", markersize=6,
         color=GREEN, zorder=3)
ax1.plot([H], [K], marker="o", markersize=6, color=INK, zorder=3)

ax1.annotate("$a(x-p)(x-q)$\nshows the $x$-intercepts", xy=(P, 0),
             xytext=(-3.3, 3.2), fontsize=10, color=WARM,
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=0.9))
ax1.annotate("", xy=(Q, 0), xytext=(-0.9, 2.85),
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=0.9))
ax1.annotate("$ax^{2}+bx+c$\nshows the $y$-intercept",
             xy=(0, A * (0 - P) * (0 - Q)), xytext=(-3.3, -2.4), fontsize=10,
             color=GREEN, va="top",
             arrowprops=dict(arrowstyle="->", color=GREEN, linewidth=0.9))
ax1.annotate("$a(x-h)^{2}+k$\nshows the vertex", xy=(H, K),
             xytext=(2.6, 3.4), fontsize=10, color=INK,
             arrowprops=dict(arrowstyle="->", color=INK, linewidth=0.9))
ax1.text(H + 0.14, 4.9, "axis of\nsymmetry", fontsize=9.5, color=GREY,
         ha="left", va="top")

# ══════════════════════════════════════════════════════════
# (b) a の符号と大きさ
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) The sign and size of $a$", fontsize=11, color=INK,
              loc="left", pad=10)
ax2.set_xlim(-3.0, 3.6)
ax2.set_ylim(-5.2, 4.6)
ax2.axis("off")

ax2.annotate("", xy=(3.4, 0), xytext=(-2.8, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.annotate("", xy=(0, 4.4), xytext=(0, -4.2),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.text(3.5, -0.36, "$x$", fontsize=11, color=GREY, ha="center")
ax2.text(-0.26, 4.5, "$y$", fontsize=11, color=GREY, va="center")

u = np.linspace(-2.2, 2.2, 300)
ax2.plot(u, 2.0 * u ** 2, color=ACCENT, linewidth=2.2)
ax2.plot(u, 0.5 * u ** 2, color=GREEN, linewidth=2.2)
ax2.plot(u, -1.0 * u ** 2, color=WARM, linewidth=2.2)

ax2.text(1.05, 3.9, "large $a > 0$:\nnarrow", fontsize=10, color=ACCENT,
         va="top")
ax2.text(2.3, 2.1, "small $a > 0$:\nwide", fontsize=10, color=GREEN,
         va="top")
ax2.text(-2.9, -2.6, "$a < 0$:\nopens downwards", fontsize=10, color=WARM,
         va="top")
ax2.text(0.3, -5.1, "$a$ cannot be $0$: the graph would be a straight line",
         fontsize=9.5, color=INK, ha="center")

fig.tight_layout(w_pad=2.4)
path = os.path.join(OUT, "aasl-2-6-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
