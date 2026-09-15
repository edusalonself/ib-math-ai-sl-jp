"""AA SL 2.7b の図をつくる。

    python3 figs/aa-sl/make_aasl_2_7b.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_2_7b.py  … 目視用の PNG も

出力: aa-sl/02-functions/img/aasl-2-7b-idea.svg

(a) 判別式の符号と、グラフが x 軸と交わる回数。
(b) 直線と曲線が接するのは、連立してできる 2 次方程式の判別式が 0 のとき。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に演習の答えを書かないこと（k の値などは書かない）。
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
# (a) 判別式の符号と交わる回数
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) The sign of the discriminant", fontsize=11, color=INK,
              loc="left", pad=10)
ax1.set_xlim(-1.2, 11.2)
ax1.set_ylim(-3.4, 4.6)
ax1.axis("off")

cases = [
    (1.6, -1.2, ACCENT, "$\\Delta > 0$", "two distinct\nreal roots"),
    (5.4, 0.0, GREEN, "$\\Delta = 0$", "two equal\nreal roots"),
    (9.2, 1.2, WARM, "$\\Delta < 0$", "no real\nroots"),
]
for cx, shift, col, lab, note in cases:
    ax1.plot([cx - 1.5, cx + 1.5], [0, 0], color=GREY, linewidth=1.0)
    t = np.linspace(-1.45, 1.45, 200)
    ax1.plot(cx + t, 1.35 * t ** 2 + shift, color=col, linewidth=2.2)
    if shift < 0:
        r = np.sqrt(-shift / 1.35)
        for sgn in (-1, 1):
            ax1.plot([cx + sgn * r], [0], marker="o", markersize=5.5,
                     color=INK, zorder=3)
    elif shift == 0:
        ax1.plot([cx], [0], marker="o", markersize=5.5, color=INK, zorder=3)
    ax1.text(cx, 3.6, lab, ha="center", va="center", fontsize=13, color=col)
    ax1.text(cx, -1.6, note, ha="center", va="top", fontsize=10, color=INK)

ax1.text(5.4, -3.3, "$\\Delta = b^{2} - 4ac$", ha="center", va="bottom",
         fontsize=12, color=INK)

# ══════════════════════════════════════════════════════════
# (b) 直線と曲線
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) A line and a curve", fontsize=11, color=INK,
              loc="left", pad=10)
ax2.set_xlim(-3.4, 3.4)
ax2.set_ylim(-3.0, 6.6)
ax2.axis("off")

ax2.annotate("", xy=(3.0, 0), xytext=(-2.6, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.annotate("", xy=(0, 6.4), xytext=(0, -2.8),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.text(3.1, -0.34, "$x$", fontsize=11, color=GREY, ha="center")
ax2.text(-0.26, 6.5, "$y$", fontsize=11, color=GREY, va="center")

v = np.linspace(-2.2, 2.2, 200)
ax2.plot(v, v ** 2 + 1, color=ACCENT, linewidth=2.2)
ax2.plot(v, 2 * v + 2.6, color=WARM, linewidth=2.0)
ax2.plot(v, 2 * v + 0.0, color=GREEN, linewidth=2.0)
ax2.plot(v, 2 * v - 1.0, color=GREY, linewidth=2.0, linestyle=(0, (5, 4)))
ax2.plot([1.0], [2.0], marker="o", markersize=6, color=GREEN, zorder=3)

ax2.text(-3.3, -1.1, "two points: $\\Delta > 0$", fontsize=10, color=WARM,
         va="top")
ax2.text(-3.3, -1.85, "tangent: $\\Delta = 0$", fontsize=10, color=GREEN,
         va="top")
ax2.text(-3.3, -2.6, "no point: $\\Delta < 0$", fontsize=10, color=GREY,
         va="top")
ax2.text(1.5, 6.4, "$y = f(x)$", fontsize=11, color=ACCENT, va="top")
ax2.annotate("", xy=(1.0, 2.0), xytext=(1.9, 1.0),
             arrowprops=dict(arrowstyle="->", color=GREEN, linewidth=0.9))

fig.tight_layout(w_pad=2.2)
path = os.path.join(OUT, "aasl-2-7b-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
