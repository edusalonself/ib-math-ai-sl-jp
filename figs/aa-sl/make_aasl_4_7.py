"""AA SL 4.7 の図をつくる。

    python3 figs/aa-sl/make_aasl_4_7.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_4_7.py  … 目視用の PNG も

出力: aa-sl/04-statistics-and-probability/img/aasl-4-7-idea.svg

(a) 確率分布の棒グラフ。E(X) は棒がつり合う点。
(b) ゲームの利得。E(X) = 0 が公平なゲーム。

★ 数値は例題・演習と重ならないように選んであります。
   (a) は 0.1 / 0.3 / 0.5 / 0.1（E = 1.6）。例題1 は E = 2.7、演習1 は E = 1.7。
       確率の並びも例題1（0.1 / 0.3 / 0.4 / 0.2）と別のものにしてある。
   (b) は +3 / -2（E = -1/3）と +4 / -2（E = 0）。例題3 は E = -1/2、
       例題4 の公平な賞金は 8、演習5 は E = -0.4、演習10 は 0 と 0.4。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ PNG は目視用です。確認が終わったら消してください。
"""
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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.8))

# ══════════════════════════════════════════════════════════
# (a) 確率分布と、つり合う点
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) $E(X)$ is where the distribution balances", fontsize=11,
              color=INK, loc="left", pad=12)

XS = [0, 1, 2, 3]
PS = [0.1, 0.3, 0.5, 0.1]
MEAN = sum(x * p for x, p in zip(XS, PS))

ax1.bar(XS, PS, width=0.42, color=FILL, edgecolor=ACCENT, linewidth=1.2)
for _x, _p in zip(XS, PS):
    ax1.text(_x, _p + 0.018, "$%.1f$" % _p, fontsize=9.5, color=ACCENT,
             ha="center")

ax1.set_xlim(-0.75, 3.75)
ax1.set_ylim(-0.02, 0.66)
ax1.set_xticks(XS)
ax1.set_xticklabels(["$%d$" % x for x in XS], fontsize=10)
ax1.set_yticks([0, 0.2, 0.4, 0.6])
ax1.set_yticklabels(["$0$", "$0.2$", "$0.4$", "$0.6$"],
                    fontsize=9.5)
ax1.set_xlabel("$x$", fontsize=10, color=GREY)
ax1.set_ylabel("$P(X = x)$", fontsize=10, color=GREY)
for _sp in ("top", "right"):
    ax1.spines[_sp].set_visible(False)
for _sp in ("left", "bottom"):
    ax1.spines[_sp].set_color(GREY)
ax1.tick_params(length=0, colors=GREY)

ax1.plot([MEAN, MEAN], [0, 0.60], color=WARM, linewidth=1.5,
         linestyle=(0, (5, 3)))
ax1.plot([MEAN], [-0.012], marker="^", markersize=11, color=WARM,
         clip_on=False)
ax1.text(MEAN + 0.10, 0.61, "$E(X) = 1.6$", fontsize=10, color=WARM)

ax1.text(0.0, -0.20, "the four probabilities add to $1$; $E(X)$ is each value "
         "weighted by its probability", fontsize=9, color=INK,
         transform=ax1.transAxes)
ax1.text(0.0, -0.28, "$1.6$ is not a value $X$ can take, and it does not have "
         "to be", fontsize=9, color=WARM, transform=ax1.transAxes)

# ══════════════════════════════════════════════════════════
# (b) ゲームの利得
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) A game is fair when $E(X) = 0$", fontsize=11, color=INK,
              loc="left", pad=12)
ax2.set_xlim(-3.6, 5.6)
ax2.set_ylim(-3.6, 3.4)
ax2.axis("off")


def _game(y, gains, probs, sizes, label, mean, colour):
    ax2.plot([-3.0, 5.0], [y, y], color=GREY, linewidth=1.0)
    for _t in (-2, 0, 2, 4):
        ax2.plot([_t, _t], [y - 0.08, y + 0.08], color=GREY, linewidth=1.0)
        ax2.text(_t, y - 0.50, "$%d$" % _t, fontsize=9, color=GREY,
                 ha="center")
    for _g, _p, _s in zip(gains, probs, sizes):
        ax2.plot([_g], [y], "o", color=ACCENT, markersize=5 + 9 * _s)
        ax2.text(_g, y + 0.30, _p, fontsize=9.5, color=ACCENT, ha="center")
    ax2.plot([mean], [y + 0.30], marker="v", markersize=10, color=colour,
             clip_on=False)
    ax2.text(-3.5, y + 1.05, label, fontsize=9.5, color=INK)


_game(1.6, [3, -2], [r"$\frac{1}{3}$", r"$\frac{2}{3}$"], [1 / 3, 2 / 3],
      "a losing game: gain $+3$ with probability $\\frac{1}{3}$, "
      "$-2$ with probability $\\frac{2}{3}$", -1 / 3, WARM)
ax2.text(-3.5, 0.55, r"$E(X) = 3\times\frac{1}{3}+(-2)\times\frac{2}{3}"
         r"=-\frac{1}{3}$: the player loses in the long run",
         fontsize=9.5, color=WARM)

_game(-1.5, [4, -2], [r"$\frac{1}{3}$", r"$\frac{2}{3}$"], [1 / 3, 2 / 3],
      "a fair game: gain $+4$ with probability $\\frac{1}{3}$, "
      "$-2$ with probability $\\frac{2}{3}$", 0.0, ACCENT)
ax2.text(-3.5, -2.55, r"$E(X) = 4\times\frac{1}{3}+(-2)\times\frac{2}{3}=0$: "
         "the game is fair", fontsize=9.5, color=ACCENT)
ax2.text(-3.5, -3.15, "the triangle marks $E(X)$; the dot sizes show the "
         "probabilities", fontsize=9, color=GREY)

fig.tight_layout(w_pad=2.4)
path = os.path.join(OUT, "aasl-4-7-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))
print("  (a) sum =", sum(PS), " mean =", MEAN)
print("  (b) game A mean =", 3 / 3 - 2 * 2 / 3, " game B mean =", 4 / 3 - 4 / 3)

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
