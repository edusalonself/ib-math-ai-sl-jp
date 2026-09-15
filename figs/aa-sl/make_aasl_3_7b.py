"""AA SL 3.7b の図をつくる。

    python3 figs/aa-sl/make_aasl_3_7b.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_3_7b.py  … 目視用の PNG も

出力: aa-sl/03-geometry/img/aasl-3-7b-idea.svg

(a) y = sin x と y = 3 sin 2x。縦に 3 倍、横に 1/2 倍。
(b) y = a sin(b(x+c)) + d の 4 つの数が、グラフのどこに出るか。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に例題・演習の答えを書かないこと（(b) は文字のまま）。
★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "03-geometry", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
GREEN = "#15803d"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 4.6))

# ══════════════════════════════════════════════════════════
# (a) 縦に伸ばし、横に縮める
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) A stretch in each direction", fontsize=11, color=INK,
              loc="left", pad=10)
x = np.linspace(0, 2 * np.pi, 600)
ax1.plot(x, np.sin(x), color=GREY, linewidth=1.8, linestyle=(0, (6, 3)),
         label="$y = \\sin x$")
ax1.plot(x, 3 * np.sin(2 * x), color=ACCENT, linewidth=2.2,
         label="$y = 3\\sin 2x$")
ax1.axhline(0, color=GREY, linewidth=1.0)
ax1.set_xlim(-0.3, 2 * np.pi + 0.3)
ax1.set_ylim(-4.4, 5.6)
ax1.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi])
ax1.set_xticklabels(["$0$", "$\\frac{\\pi}{2}$", "$\\pi$", "$\\frac{3\\pi}{2}$",
                     "$2\\pi$"], fontsize=9.5)
ax1.set_yticks([-3, -1, 0, 1, 3])
ax1.set_yticklabels(["$-3$", "$-1$", "$0$", "$1$", "$3$"], fontsize=9.5)
for _sp in ("top", "right", "left", "bottom"):
    ax1.spines[_sp].set_visible(False)
ax1.tick_params(length=0, colors=GREY)
ax1.legend(loc="upper right", frameon=False, fontsize=10)
ax1.text(-0.3, -4.3, "the same shape, stretched in one direction and squeezed in "
         "the other", fontsize=9.5, color=INK, va="bottom")

# ══════════════════════════════════════════════════════════
# (b) 4 つの数がどこに出るか
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) Where $a$, $b$, $c$ and $d$ show up", fontsize=11, color=INK,
              loc="left", pad=10)
A, D, SH = 2.0, 3.0, 0.7
xx = np.linspace(-0.6, 7.2, 700)
yy = A * np.sin(xx - SH) + D
ax2.plot(xx, yy, color=ACCENT, linewidth=2.2)
ax2.axhline(D, color=GREEN, linewidth=1.2, linestyle=(0, (5, 4)))
ax2.set_xlim(-0.9, 8.9)
ax2.set_ylim(-0.7, 7.4)
ax2.set_xticks([])
ax2.set_yticks([])
for _sp in ("top", "right", "left", "bottom"):
    ax2.spines[_sp].set_visible(False)

_top = SH + np.pi / 2
_bot = SH + 3 * np.pi / 2
ax2.annotate("", xy=(_top, D + A), xytext=(_top, D),
             arrowprops=dict(arrowstyle="<->", color=WARM, linewidth=1.3))
ax2.text(_top + 0.14, D + A / 2 - 0.12, "$|a|$", fontsize=11, color=WARM)
ax2.annotate("", xy=(SH + 2 * np.pi, 0.30), xytext=(SH, 0.30),
             arrowprops=dict(arrowstyle="<->", color=WARM, linewidth=1.3))
ax2.text((2 * SH + 2 * np.pi) / 2 - 0.62, 0.62,
         "one period $= \\frac{2\\pi}{|b|}$", fontsize=10, color=WARM)
ax2.text(7.30, D + 0.30, "midline $y = d$", fontsize=10, color=GREEN)
ax2.annotate("", xy=(SH, D), xytext=(0, D),
             arrowprops=dict(arrowstyle="->", color=INK, linewidth=1.3))
ax2.text(-0.85, D + 0.34, "shift by $c$", fontsize=10, color=INK)
ax2.plot([SH], [D], marker="o", markersize=5.0, color=INK, zorder=3)

ax2.text(-0.9, 7.1, "highest value $d + |a|$, lowest value $d - |a|$",
         fontsize=10, color=INK, va="top")
ax2.text(-0.9, -0.65, "the midline is halfway between the highest and the "
         "lowest", fontsize=9.5, color=INK, va="bottom")

fig.tight_layout(w_pad=2.4)
path = os.path.join(OUT, "aasl-3-7b-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
