"""AA SL 2.7a の図をつくる。

    python3 figs/aa-sl/make_aasl_2_7a.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_2_7a.py  … 目視用の PNG も

出力: aa-sl/02-functions/img/aasl-2-7a-idea.svg

(a) 2 次方程式を解く 3 つの道すじ。
(b) 2 次不等式は、グラフが軸の上か下かで決まる。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に演習の答えを書かないこと（具体的な数値は書かない）。
★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "02-functions", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
GREEN = "#15803d"
PALE = "#e8f0f8"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.6))

# ══════════════════════════════════════════════════════════
# (a) 3 つの道すじ
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Three routes to the solutions", fontsize=11, color=INK,
              loc="left", pad=10)
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis("off")

ax1.add_patch(FancyBboxPatch((1.2, 8.0), 7.6, 1.4,
                             boxstyle="round,pad=0.06,rounding_size=0.2",
                             linewidth=1.6, edgecolor=INK, facecolor=PALE))
ax1.text(5.0, 8.7, "make one side $0$", ha="center", va="center",
         fontsize=12, color=INK)

routes = [
    (2.0, "factorising", ACCENT, "when the factors\nare easy to see"),
    (5.0, "completing\nthe square", GREEN, "when the answer\nis wanted exactly"),
    (8.0, "the quadratic\nformula", WARM, "always works"),
]
for cx, name, col, note in routes:
    ax1.annotate("", xy=(cx, 6.4), xytext=(5.0, 7.9),
                 arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.2))
    ax1.add_patch(FancyBboxPatch((cx - 1.25, 4.9), 2.5, 1.5,
                                 boxstyle="round,pad=0.06,rounding_size=0.2",
                                 linewidth=1.6, edgecolor=col,
                                 facecolor="none"))
    ax1.text(cx, 5.65, name, ha="center", va="center", fontsize=11,
             color=col)
    ax1.text(cx, 4.3, note, ha="center", va="top", fontsize=9.5, color=INK)

ax1.annotate("", xy=(5.0, 2.1), xytext=(2.0, 3.2),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.2))
ax1.annotate("", xy=(5.0, 2.1), xytext=(5.0, 3.2),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.2))
ax1.annotate("", xy=(5.0, 2.1), xytext=(8.0, 3.2),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.2))
ax1.add_patch(FancyBboxPatch((2.6, 0.7), 4.8, 1.4,
                             boxstyle="round,pad=0.06,rounding_size=0.2",
                             linewidth=1.6, edgecolor=INK, facecolor=PALE))
ax1.text(5.0, 1.4, "the same solutions", ha="center", va="center",
         fontsize=12, color=INK)

# ══════════════════════════════════════════════════════════
# (b) 2 次不等式
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) Reading a quadratic inequality", fontsize=11, color=INK,
              loc="left", pad=10)
ax2.set_xlim(-3.6, 4.6)
ax2.set_ylim(-3.4, 5.8)
ax2.axis("off")

ax2.annotate("", xy=(4.4, 0), xytext=(-3.4, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.annotate("", xy=(0, 4.6), xytext=(0, -3.2),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.text(4.5, -0.36, "$x$", fontsize=11, color=GREY, ha="center")
ax2.text(-0.26, 4.7, "$y$", fontsize=11, color=GREY, va="center")

Pp, Qq = -1.6, 3.0
u = np.linspace(-3.0, 4.1, 300)
ax2.plot(u, 0.55 * (u - Pp) * (u - Qq), color=ACCENT, linewidth=2.2)
for px in (Pp, Qq):
    ax2.plot([px], [0], marker="o", markersize=6, color=INK, zorder=3)

ax2.plot([-3.3, Pp], [-2.6, -2.6], color=WARM, linewidth=4.0,
         solid_capstyle="butt")
ax2.plot([Qq, 4.3], [-2.6, -2.6], color=WARM, linewidth=4.0,
         solid_capstyle="butt")
ax2.plot([Pp, Qq], [-3.1, -3.1], color=GREEN, linewidth=4.0,
         solid_capstyle="butt")
ax2.text(-3.3, -2.25, "$f(x) > 0$ outside the roots", fontsize=10,
         color=WARM, ha="left")
ax2.text(4.3, -3.35, "$f(x) < 0$ between the roots", fontsize=10,
         color=GREEN, ha="right", va="top")
ax2.text(0.5, 5.7, "for $a > 0$: above the axis outside the roots,\n"
         "below the axis between them",
         fontsize=9.5, color=INK, va="top", ha="center")

fig.tight_layout(w_pad=2.2)
path = os.path.join(OUT, "aasl-2-7a-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
