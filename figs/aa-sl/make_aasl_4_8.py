"""AA SL 4.8 の図をつくる。

    python3 figs/aa-sl/make_aasl_4_8.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_4_8.py  … 目視用の PNG も

出力: aa-sl/04-statistics-and-probability/img/aasl-4-8-idea.svg

(a) 二項分布の形。棒の高さが P(X = x)。E(X) = np はつり合う点。
(b)「以下」は棒の足し算。「以上」は残り。

★ 数値は例題・演習と重ならないように選んであります。
   (a) は B(7, 0.4)。例題は B(8,0.25) / B(10,0.8) / B(15,0.8) / B(12,0.4)。
   (b) は B(6, 0.5)。演習は B(6,0.3) / B(20,0.15) / B(12,0.5) / B(25,0.04) /
       B(30,0.6) / B(10,0.25) / B(14,0.2)。
   確率の値は図に書きません（答えの先出しを避けるため）。

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

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "04-statistics-and-probability", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
FILL = "#cfe0f2"
SHADE = "#f6d9ad"


def binom(n, p, x):
    return math.comb(n, x) * p ** x * (1 - p) ** (n - x)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.7))

# ══════════════════════════════════════════════════════════
# (a) 二項分布の形と E(X) = np
# ══════════════════════════════════════════════════════════
N1, P1 = 7, 0.4
XS1 = list(range(N1 + 1))
YS1 = [binom(N1, P1, x) for x in XS1]
MEAN1 = N1 * P1

ax1.set_title("(a) $X \\sim B(7,\\ 0.4)$: the bars add to $1$", fontsize=11,
              color=INK, loc="left", pad=12)
ax1.bar(XS1, YS1, width=0.5, color=FILL, edgecolor=ACCENT, linewidth=1.2)
ax1.set_xlim(-0.8, 7.8)
ax1.set_ylim(-0.01, 0.40)
ax1.set_xticks(XS1)
ax1.set_xticklabels(["$%d$" % x for x in XS1], fontsize=9.5)
ax1.set_yticks([0, 0.1, 0.2, 0.3])
ax1.set_yticklabels(["$0$", "$0.1$", "$0.2$", "$0.3$"], fontsize=9.5)
ax1.set_xlabel("$x$", fontsize=10, color=GREY)
ax1.set_ylabel("$P(X = x)$", fontsize=10, color=GREY)
for _sp in ("top", "right"):
    ax1.spines[_sp].set_visible(False)
for _sp in ("left", "bottom"):
    ax1.spines[_sp].set_color(GREY)
ax1.tick_params(length=0, colors=GREY)

ax1.plot([MEAN1, MEAN1], [0, 0.35], color=WARM, linewidth=1.5,
         linestyle=(0, (5, 3)))
ax1.plot([MEAN1], [0.362], marker="v", markersize=10, color=WARM)
ax1.text(MEAN1 + 0.18, 0.352, "$E(X) = np = 2.8$", fontsize=10, color=WARM)

ax1.text(0.0, -0.20, "$x$ counts the successes in $7$ independent trials, each "
         "with success probability $0.4$", fontsize=9, color=INK,
         transform=ax1.transAxes)
ax1.text(0.0, -0.28, "the peak is near $np$, and the shape is not symmetric "
         "unless $p = 0.5$", fontsize=9, color=WARM, transform=ax1.transAxes)

# ══════════════════════════════════════════════════════════
# (b) 「以下」は棒の足し算
# ══════════════════════════════════════════════════════════
N2, P2 = 6, 0.5
XS2 = list(range(N2 + 1))
YS2 = [binom(N2, P2, x) for x in XS2]

ax2.set_title("(b) $X \\sim B(6,\\ 0.5)$: $P(X \\leq 2)$ adds the bars up "
              "to $x = 2$", fontsize=11, color=INK, loc="left", pad=12)
_cols = [SHADE if x <= 2 else FILL for x in XS2]
_edges = [WARM if x <= 2 else ACCENT for x in XS2]
for _x, _y, _c, _e in zip(XS2, YS2, _cols, _edges):
    ax2.bar([_x], [_y], width=0.5, color=_c, edgecolor=_e, linewidth=1.2)

ax2.set_xlim(-0.8, 6.8)
ax2.set_ylim(-0.01, 0.40)
ax2.set_xticks(XS2)
ax2.set_xticklabels(["$%d$" % x for x in XS2], fontsize=9.5)
ax2.set_yticks([0, 0.1, 0.2, 0.3])
ax2.set_yticklabels(["$0$", "$0.1$", "$0.2$", "$0.3$"], fontsize=9.5)
ax2.set_xlabel("$x$", fontsize=10, color=GREY)
for _sp in ("top", "right"):
    ax2.spines[_sp].set_visible(False)
for _sp in ("left", "bottom"):
    ax2.spines[_sp].set_color(GREY)
ax2.tick_params(length=0, colors=GREY)

ax2.annotate("", xy=(-0.30, 0.345), xytext=(2.30, 0.345),
             arrowprops=dict(arrowstyle="<->", color=WARM, linewidth=1.1))
ax2.text(-0.30, 0.358, "$P(X \\leq 2)$", fontsize=10, color=WARM)
ax2.annotate("", xy=(2.70, 0.345), xytext=(6.30, 0.345),
             arrowprops=dict(arrowstyle="<->", color=ACCENT, linewidth=1.1))
ax2.text(2.80, 0.358, "$P(X \\geq 3) = 1 - P(X \\leq 2)$", fontsize=10,
         color=ACCENT)

ax2.text(0.0, -0.20, "\"at most $2$\" means $x = 0, 1, 2$; \"at least $3$\" is "
         "everything else", fontsize=9, color=INK, transform=ax2.transAxes)
ax2.text(0.0, -0.28, "\"more than $2$\" is the same as \"at least $3$\" only "
         "because $x$ is a whole number", fontsize=9, color=WARM,
         transform=ax2.transAxes)

fig.tight_layout(w_pad=2.4)
path = os.path.join(OUT, "aasl-4-8-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))
print("  (a) sum =", round(sum(YS1), 12), " mean =", MEAN1)
print("  (b) sum =", round(sum(YS2), 12))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
