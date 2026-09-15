"""AA SL 2.5 の図をつくる。

    python3 figs/aa-sl/make_aasl_2_5.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_2_5.py  … 目視用の PNG も

出力: aa-sl/02-functions/img/aasl-2-5-idea.svg

(a) 合成関数は、2 台の機械を直列につないだもの。順番が大事。
(b) f のあとに f^{-1} を通すと、もとの x に戻る。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に演習の答えを書かないこと（具体的な式は書かない）。
★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "02-functions", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
PALE = "#e8f0f8"
PALEW = "#fbeee0"

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9.2, 5.0))


def box(ax, cx, cy, w, h, label, edge, face):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.06",
                                linewidth=1.6, edgecolor=edge,
                                facecolor=face, zorder=2))
    ax.text(cx, cy, label, ha="center", va="center", fontsize=13,
            color=edge, zorder=3)


def arrow(ax, x0, x1, y, label, colour=INK, dy=0.22):
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.4))
    ax.text((x0 + x1) / 2, y + dy, label, ha="center", va="bottom",
            fontsize=12, color=colour)


# ══════════════════════════════════════════════════════════
# (a) 合成関数
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) $(f \\circ g)(x) = f(g(x))$: $g$ acts first",
              fontsize=11.5, color=INK, loc="left", pad=8)
ax1.set_xlim(0, 10)
ax1.set_ylim(-0.2, 1.9)
ax1.axis("off")

box(ax1, 3.4, 0.8, 1.5, 0.9, "$g$", ACCENT, PALE)
box(ax1, 6.9, 0.8, 1.5, 0.9, "$f$", WARM, PALEW)
arrow(ax1, 0.9, 2.55, 0.8, "$x$")
arrow(ax1, 4.25, 6.05, 0.8, "$g(x)$")
arrow(ax1, 7.75, 9.5, 0.8, "$f(g(x))$")
ax1.text(5.0, -0.12, "the inner function is written next to $x$, "
         "so it is used first",
         ha="center", va="bottom", fontsize=10, color=INK)

# ══════════════════════════════════════════════════════════
# (b) 逆関数は、もとに戻す
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) $(f^{-1} \\circ f)(x) = x$: the inverse undoes $f$",
              fontsize=11.5, color=INK, loc="left", pad=8)
ax2.set_xlim(0, 10)
ax2.set_ylim(-0.2, 1.9)
ax2.axis("off")

box(ax2, 3.4, 0.8, 1.5, 0.9, "$f$", WARM, PALEW)
box(ax2, 6.9, 0.8, 1.6, 0.9, "$f^{-1}$", ACCENT, PALE)
arrow(ax2, 0.9, 2.55, 0.8, "$x$")
arrow(ax2, 4.25, 6.0, 0.8, "$f(x)$")
arrow(ax2, 7.8, 9.5, 0.8, "$x$ again")
ax2.text(5.0, -0.12, "the same holds the other way round: "
         "$(f \\circ f^{-1})(x) = x$",
         ha="center", va="bottom", fontsize=10, color=INK)

fig.tight_layout(h_pad=2.0)
path = os.path.join(OUT, "aasl-2-5-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
