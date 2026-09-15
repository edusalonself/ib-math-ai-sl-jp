"""AA SL 4.10 の図をつくる。

    python3 figs/aa-sl/make_aasl_4_10.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_4_10.py  … 目視用の PNG も

出力: aa-sl/04-statistics-and-probability/img/aasl-4-10-idea.svg

(a) 2 本の回帰直線。どちらも平均点を通るが、一致しない。
(b) 何を最小にしているか —— 縦のずれ（y on x）と横のずれ（x on y）。

★ 図のデータ (1..8, 3/6/4/5/9/7/11/8) は例題・演習で使っていません。
   図には直線の式の数値を書かず、形だけを見せます。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * \\le \\ge は読めない → \\leq \\geq を使う
  * 日本語のグリフがない → ラベルはすべて英語

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

XS = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=float)
YS = np.array([3, 6, 4, 5, 9, 7, 11, 8], dtype=float)
MX, MY = XS.mean(), YS.mean()
A = np.polyfit(XS, YS, 1)          # y on x
B = np.polyfit(YS, XS, 1)          # x on y

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.9))

# ══════════════════════════════════════════════════════════
# (a) 2 本の回帰直線
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Two different regression lines", fontsize=11, color=INK,
              loc="left", pad=12)
ax1.scatter(XS, YS, s=34, color=ACCENT, zorder=3)

_gx = np.linspace(0.4, 8.6, 100)
ax1.plot(_gx, A[0] * _gx + A[1], color=ACCENT, linewidth=1.6,
         label="$y$ on $x$")
_gy = np.linspace(2.2, 11.6, 100)
ax1.plot(B[0] * _gy + B[1], _gy, color=WARM, linewidth=1.6,
         linestyle=(0, (6, 3)), label="$x$ on $y$")

ax1.plot([MX], [MY], marker="o", markersize=9, markerfacecolor="white",
         markeredgecolor=INK, markeredgewidth=1.6, zorder=4)
ax1.annotate("mean point $(\\bar{x},\\ \\bar{y})$", xy=(MX + 0.18, MY - 0.15),
             xytext=(5.4, 4.0), fontsize=9.5, color=INK,
             arrowprops=dict(arrowstyle="->", color=INK, linewidth=1.0))

ax1.set_xlim(0.2, 9.0)
ax1.set_ylim(1.8, 12.2)
ax1.set_xlabel("$x$", fontsize=10, color=GREY)
ax1.set_ylabel("$y$", fontsize=10, color=GREY)
ax1.set_xticks([2, 4, 6, 8])
ax1.set_xticklabels(["$2$", "$4$", "$6$", "$8$"], fontsize=9.5)
ax1.set_yticks([4, 6, 8, 10, 12])
ax1.set_yticklabels(["$4$", "$6$", "$8$", "$10$", "$12$"], fontsize=9.5)
for _sp in ("top", "right"):
    ax1.spines[_sp].set_visible(False)
for _sp in ("left", "bottom"):
    ax1.spines[_sp].set_color(GREY)
ax1.tick_params(length=0, colors=GREY)
ax1.legend(loc="upper left", fontsize=9.5, frameon=False)

ax1.text(0.0, -0.20, "both lines pass through the mean point, but they are not "
         "the same line", fontsize=9, color=INK, transform=ax1.transAxes)
ax1.text(0.0, -0.28, "they agree only when every point lies exactly on one "
         "straight line", fontsize=9, color=WARM, transform=ax1.transAxes)

# ══════════════════════════════════════════════════════════
# (b) 何を最小にしているか
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) The two lines minimise different gaps", fontsize=11,
              color=INK, loc="left", pad=12)
ax2.scatter(XS, YS, s=34, color=ACCENT, zorder=3)
ax2.plot(_gx, A[0] * _gx + A[1], color=ACCENT, linewidth=1.4)
ax2.plot(B[0] * _gy + B[1], _gy, color=WARM, linewidth=1.4,
         linestyle=(0, (6, 3)))

for _x, _y in zip(XS, YS):
    ax2.plot([_x, _x], [_y, A[0] * _x + A[1]], color=ACCENT, linewidth=1.0,
             alpha=0.8)
    ax2.plot([_x, B[0] * _y + B[1]], [_y, _y], color=WARM, linewidth=1.0,
             alpha=0.9)

ax2.set_xlim(0.2, 9.0)
ax2.set_ylim(1.8, 12.2)
ax2.set_xlabel("$x$", fontsize=10, color=GREY)
ax2.set_ylabel("$y$", fontsize=10, color=GREY)
ax2.set_xticks([2, 4, 6, 8])
ax2.set_xticklabels(["$2$", "$4$", "$6$", "$8$"], fontsize=9.5)
ax2.set_yticks([4, 6, 8, 10, 12])
ax2.set_yticklabels(["$4$", "$6$", "$8$", "$10$", "$12$"], fontsize=9.5)
for _sp in ("top", "right"):
    ax2.spines[_sp].set_visible(False)
for _sp in ("left", "bottom"):
    ax2.spines[_sp].set_color(GREY)
ax2.tick_params(length=0, colors=GREY)

ax2.text(0.55, 11.2, "solid vertical gaps: $y$ on $x$", fontsize=9,
         color=ACCENT)
ax2.text(0.55, 10.3, "horizontal gaps: $x$ on $y$", fontsize=9,
         color=WARM)

ax2.text(0.0, -0.20, "the $y$ on $x$ line makes the vertical gaps as small as "
         "possible", fontsize=9, color=ACCENT, transform=ax2.transAxes)
ax2.text(0.0, -0.28, "the $x$ on $y$ line makes the horizontal gaps as small "
         "as possible", fontsize=9, color=WARM, transform=ax2.transAxes)

fig.tight_layout(w_pad=2.4)
path = os.path.join(OUT, "aasl-4-10-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))
print("  mean point = (%.4f, %.4f)" % (MX, MY))
print("  y on x slope %.5f, x on y slope %.5f, product %.5f"
      % (A[0], B[0], A[0] * B[0]))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
