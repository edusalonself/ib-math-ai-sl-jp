"""AA SL 4.4 の図をつくる。

    python3 figs/aa-sl/make_aasl_4_4.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_4_4.py  … 目視用の PNG も

出力: aa-sl/04-statistics-and-probability/img/aasl-4-4-idea.svg

(a) 相関の向きと強さ。r が 0 に近くても、曲線の関係はありうる。
(b) 回帰直線は mean point を通る。データの範囲の外は外挿。

★ 点はすべて固定のリストにしてあります（乱数を使わない）。
   チェッカーが同じデータから r を計算し直せるようにするためです。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に例題・演習の答えを書かないこと。
★ PNG は目視用です。確認が終わったら消してください。
"""
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "04-statistics-and-probability", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"

XS = [1, 2, 3, 4, 5, 6, 7, 8]
PANELS = [
    ("strong positive", [2, 3, 3, 5, 6, 6, 8, 9]),
    ("weak positive", [4, 2, 6, 3, 7, 4, 6, 5]),   # r = 0.43（表の weak の側）
    ("on a curve", [12.25, 6.25, 2.25, 0.25, 0.25, 2.25, 6.25, 12.25]),
    ("strong negative", [9, 8, 8, 6, 5, 5, 3, 2]),
]


def corr(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    return sxy / math.sqrt(sxx * syy)


fig = plt.figure(figsize=(10.0, 4.8))
gs = GridSpec(2, 4, figure=fig, wspace=0.35, hspace=0.55,
              left=0.04, right=0.98, top=0.84, bottom=0.13)

# ══════════════════════════════════════════════════════════
# (a) 4 つの散布図
# ══════════════════════════════════════════════════════════
for _i, (_lab, _ys) in enumerate(PANELS):
    ax = fig.add_subplot(gs[_i // 2, _i % 2])
    ax.scatter(XS, _ys, s=20, color=ACCENT, zorder=3)
    ax.set_xticks([])
    ax.set_yticks([])
    for _sp in ("top", "right"):
        ax.spines[_sp].set_visible(False)
    for _sp in ("left", "bottom"):
        ax.spines[_sp].set_color(GREY)
    _r = corr(XS, _ys)
    ax.set_title(f"{_lab}   $r = {_r:.2f}$", fontsize=9, color=INK,
                 loc="left", pad=4)
    ax.margins(0.14)
    if _i == 0:
        ax.text(-0.06, 1.62, "(a) Direction and strength", fontsize=11,
                color=INK, transform=ax.transAxes)
    if _i == 2:
        ax.text(0.0, -0.30, "a value of $r$ near $0$ does not mean there is "
                "no relationship", fontsize=9, color=WARM,
                transform=ax.transAxes)

# ══════════════════════════════════════════════════════════
# (b) 回帰直線・mean point・外挿
# ══════════════════════════════════════════════════════════
ax2 = fig.add_subplot(gs[:, 2:])
ax2.set_title("(b) Where the line can be trusted", fontsize=11, color=INK,
              loc="left", pad=10)

DX = [2.2, 3.0, 3.8, 4.6, 5.4, 6.2, 7.0, 7.8]
DY = [3.4, 3.2, 4.4, 4.2, 5.4, 5.6, 6.2, 6.8]
A = corr(DX, DY) * (sum((y - sum(DY) / 8) ** 2 for y in DY)
                    / sum((x - sum(DX) / 8) ** 2 for x in DX)) ** 0.5
MX = sum(DX) / 8
MY = sum(DY) / 8
B = MY - A * MX

ax2.axvspan(DX[0], DX[-1], color="#eef4fa", zorder=0)
ax2.scatter(DX, DY, s=26, color=ACCENT, zorder=3)
_xl = [0.4, 10.4]
ax2.plot(_xl, [A * _xl[0] + B, A * _xl[1] + B], color=WARM, linewidth=1.8,
         zorder=2)
ax2.plot([DX[0], DX[-1]], [A * DX[0] + B, A * DX[-1] + B], color=WARM,
         linewidth=3.4, zorder=2, solid_capstyle="butt")
ax2.plot([MX], [MY], marker="o", markersize=9, color=INK, zorder=4)
ax2.annotate("mean point $(\\bar{x}, \\bar{y})$", xy=(MX, MY),
             xytext=(MX - 3.2, MY + 1.5), fontsize=9.5, color=INK,
             arrowprops=dict(arrowstyle="->", color=INK, linewidth=1.0))

ax2.text((DX[0] + DX[-1]) / 2, 1.35, "range of the data", fontsize=9.5,
         color=ACCENT, ha="center")
for _x, _ha in [(1.3, "center"), (9.3, "center")]:
    ax2.text(_x, 1.35, "extrapolation", fontsize=9.5, color=WARM, ha=_ha)

ax2.set_xlim(0.4, 10.4)
ax2.set_ylim(1.0, 9.2)
ax2.set_xticks([])
ax2.set_yticks([])
for _sp in ("top", "right"):
    ax2.spines[_sp].set_visible(False)
for _sp in ("left", "bottom"):
    ax2.spines[_sp].set_color(GREY)
ax2.text(0.0, -0.10, "outside the range of the data, nothing has been "
         "measured", fontsize=9, color=WARM, transform=ax2.transAxes)

path = os.path.join(OUT, "aasl-4-4-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))
for _lab, _ys in PANELS:
    print(f"  {_lab}: r = {corr(XS, _ys):.3f}")

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
