"""AA SL 4.2 の図をつくる。

    python3 figs/aa-sl/make_aasl_4_2.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_4_2.py  … 目視用の PNG も

出力: aa-sl/04-statistics-and-probability/img/aasl-4-2-idea.svg

(a) 累積度数グラフの読み方（縦から入って、横に出る）。
(b) 箱ひげ図と、外れ値の × とひげの止まる位置。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に例題・演習の数値を書かないこと（軸の目盛りは n の分数と記号だけ）。
★ PNG は目視用です。確認が終わったら消してください。
"""
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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 4.6))

# ══════════════════════════════════════════════════════════
# (a) 累積度数グラフの読み方
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Reading a cumulative frequency graph", fontsize=11,
              color=INK, loc="left", pad=10)

# なめらかな S 字（ロジスティック）。数値そのものには意味を持たせない。
_x = np.linspace(0, 10, 400)
_y = 1.0 / (1.0 + np.exp(-(_x - 5.0) * 0.85))
_y = (_y - _y[0]) / (_y[-1] - _y[0])          # 0 から 1 に正規化
ax1.plot(_x, _y, color=ACCENT, linewidth=2.2)


def _xof(frac):
    return float(np.interp(frac, _y, _x))


ax1.set_xlim(-0.6, 11.4)
ax1.set_ylim(-0.20, 1.22)
ax1.set_yticks([0.25, 0.5, 0.75, 1.0])
ax1.set_yticklabels(["$\\frac{n}{4}$", "$\\frac{n}{2}$", "$\\frac{3n}{4}$", "$n$"],
                    fontsize=10)
ax1.set_xticks([])
for _sp in ("top", "right"):
    ax1.spines[_sp].set_visible(False)
ax1.spines["left"].set_color(GREY)
ax1.spines["bottom"].set_color(GREY)
ax1.tick_params(length=0, colors=GREY)

for _f, _lab in [(0.25, "$Q_1$"), (0.5, "median"), (0.75, "$Q_3$")]:
    _xx = _xof(_f)
    ax1.plot([0, _xx], [_f, _f], color=WARM, linewidth=1.1,
             linestyle=(0, (4, 3)))
    ax1.plot([_xx, _xx], [0, _f], color=WARM, linewidth=1.1,
             linestyle=(0, (4, 3)))
    ax1.plot([_xx], [_f], marker="o", markersize=5, color=INK, zorder=3)
    ax1.text(_xx, -0.115, _lab, fontsize=10, color=WARM, ha="center")

ax1.text(0.15, 1.10, "cumulative frequency", fontsize=9.5, color=GREY)
ax1.text(11.3, -0.115, "value", fontsize=9.5, color=GREY, ha="right")
ax1.annotate("", xy=(2.05, 0.60), xytext=(0.35, 0.60),
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=1.2))
ax1.text(0.35, 0.66, "in on the vertical axis", fontsize=9.5, color=WARM)
ax1.annotate("", xy=(_xof(0.5), -0.02), xytext=(_xof(0.5), 0.30),
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=1.2))
ax1.text(_xof(0.5) + 1.55, 0.24, "out on the\nhorizontal axis",
         fontsize=9.5, color=WARM)

# ══════════════════════════════════════════════════════════
# (b) 箱ひげ図
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) A box and whisker diagram with an outlier", fontsize=11,
              color=INK, loc="left", pad=10)
ax2.set_xlim(-0.8, 13.6)
ax2.set_ylim(-1.6, 3.6)
ax2.axis("off")

MN, Q1, MD, Q3, LAST = 0.6, 3.4, 4.8, 6.4, 8.2
Y = 1.20
H = 0.60

ax2.add_patch(plt.Rectangle((Q1, Y - H), Q3 - Q1, 2 * H, fill=True,
                            facecolor="#e8f0f8", edgecolor=ACCENT,
                            linewidth=1.7, zorder=2))
ax2.plot([MD, MD], [Y - H, Y + H], color=ACCENT, linewidth=2.0, zorder=3)
for _a, _b in [(MN, Q1), (Q3, LAST)]:
    ax2.plot([_a, _b], [Y, Y], color=ACCENT, linewidth=1.4, zorder=1)
for _p in (MN, LAST):
    ax2.plot([_p, _p], [Y - H * 0.62, Y + H * 0.62], color=ACCENT,
             linewidth=1.6)

for _p, _lab in [(MN, "minimum"), (Q1, "$Q_1$"), (MD, "median"), (Q3, "$Q_3$")]:
    ax2.text(_p, Y - H - 0.28, _lab, fontsize=9.5, color=ACCENT,
             ha="center", va="top")

FENCE = Q3 + 1.5 * (Q3 - Q1)
ax2.plot([FENCE, FENCE], [Y - H - 0.10, Y + H + 0.20], color=WARM,
         linewidth=1.5, linestyle=(0, (5, 3)))
ax2.text(FENCE, Y - H - 0.28, "$Q_3 + 1.5\\,IQR$", fontsize=9.5, color=WARM,
         ha="center", va="top")

CROSS = 12.4
ax2.plot([CROSS], [Y], marker="x", markersize=10, markeredgewidth=2.2,
         color=INK, zorder=4)
ax2.text(CROSS, Y + 0.34, "outlier", fontsize=9.5, color=INK, ha="center")

ax2.annotate("", xy=(LAST, Y + H * 0.62 + 0.08), xytext=(6.9, Y + H + 1.00),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.text(6.7, Y + H + 1.06, "the whisker stops at the last value\n"
         "that is not an outlier", fontsize=9.5, color=GREY, ha="left")

ax2.text(-0.8, -1.55, "the outlier is plotted as a cross and the whisker does "
         "not reach it", fontsize=9.5, color=INK, va="bottom")

fig.tight_layout(w_pad=2.4)
path = os.path.join(OUT, "aasl-4-2-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
