"""AA SL 4.5 の図をつくる。

    python3 figs/aa-sl/make_aasl_4_5.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_4_5.py  … 目視用の PNG も

出力: aa-sl/04-statistics-and-probability/img/aasl-4-5-idea.svg

(a) さいころ 2 個の標本空間を表にする。事象はマス目の集まり。
(b) 相対度数は、回数を増やすと理論値のまわりに落ち着いていく。

★ (a) で色を付ける事象は「和が 7」です。例題・演習では和が 5 を使っているので、
   答えは漏れません。(b) の p = 0.4 も、例題・演習では使っていません。

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
# (a) さいころ 2 個の標本空間
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) The sample space as a table", fontsize=11, color=INK,
              loc="left", pad=10)
ax1.set_xlim(-1.1, 6.4)
ax1.set_ylim(-1.9, 7.3)
ax1.set_aspect("equal")
ax1.axis("off")

SHADED = [(a, b) for a in range(1, 7) for b in range(1, 7) if a + b == 7]
for _a in range(1, 7):
    for _b in range(1, 7):
        _x, _y = _b - 1, 6 - _a
        _fill = "#dbe8f5" if (_a, _b) in SHADED else "white"
        ax1.add_patch(plt.Rectangle((_x, _y), 1, 1, facecolor=_fill,
                                    edgecolor=GREY, linewidth=0.8))
for _i in range(6):
    ax1.text(_i + 0.5, 6.22, f"${_i + 1}$", fontsize=9.5, color=ACCENT,
             ha="center")
    ax1.text(-0.25, 5.5 - _i, f"${_i + 1}$", fontsize=9.5, color=ACCENT,
             ha="center", va="center")
ax1.text(2.5, 6.95, "second die", fontsize=9.5, color=ACCENT, ha="center")
ax1.text(-0.95, 3.0, "first die", fontsize=9.5, color=ACCENT, rotation=90,
         va="center")

ax1.text(-1.1, -0.55, "the number of cells is $n(U)$", fontsize=10, color=INK)
ax1.text(-1.1, -1.16, "shaded event: the two numbers add to $7$. It has $6$ "
         "cells, so $\\frac{6}{36} = \\frac{1}{6}$", fontsize=9.5, color=ACCENT)
ax1.text(-1.1, -1.62, "$(2,5)$ and $(5,2)$ are both shaded, and are counted "
         "separately", fontsize=9.5, color=WARM)

# ══════════════════════════════════════════════════════════
# (b) 相対度数の落ち着き方
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) Relative frequency as trials are added", fontsize=11,
              color=INK, loc="left", pad=10)

P = 0.4
N = 400
rng = np.random.default_rng(22)   # ★ 終盤が理論値の近くに落ち着く系列を選んだ
_hits = (rng.random(N) < P).astype(int)
_run = np.cumsum(_hits) / np.arange(1, N + 1)

ax2.plot(np.arange(1, N + 1), _run, color=ACCENT, linewidth=1.3)
ax2.axhline(P, color=WARM, linewidth=1.6, linestyle=(0, (6, 3)))
ax2.text(N * 0.99, P + 0.035, "theoretical probability", fontsize=9.5,
         color=WARM, ha="right")

ax2.set_xlim(0, N)
ax2.set_ylim(0, 1)
ax2.set_yticks([0, 0.5, 1])
ax2.set_yticklabels(["$0$", "$0.5$", "$1$"], fontsize=9.5)
ax2.set_xticks([0, 100, 200, 300, 400])
ax2.set_xticklabels(["$0$", "$100$", "$200$", "$300$", "$400$"], fontsize=9.5)
ax2.set_xlabel("number of trials", fontsize=9.5, color=GREY)
for _sp in ("top", "right"):
    ax2.spines[_sp].set_visible(False)
for _sp in ("left", "bottom"):
    ax2.spines[_sp].set_color(GREY)
ax2.tick_params(length=0, colors=GREY)

ax2.annotate("", xy=(40, 0.93), xytext=(2, 0.93),
             arrowprops=dict(arrowstyle="<->", color=GREY, linewidth=1.0))
ax2.text(46, 0.90, "wide swings at the start", fontsize=9, color=GREY)
ax2.annotate("", xy=(N - 2, 0.79), xytext=(N - 120, 0.79),
             arrowprops=dict(arrowstyle="<->", color=GREY, linewidth=1.0))
ax2.text(N - 128, 0.76, "narrow later", fontsize=9, color=GREY, ha="right")

ax2.text(0.0, -0.22, "the relative frequency settles towards the theoretical "
         "value, but never has to reach it exactly", fontsize=9, color=INK,
         transform=ax2.transAxes)

fig.tight_layout(w_pad=2.4)
path = os.path.join(OUT, "aasl-4-5-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))
print(f"  shaded cells: {len(SHADED)}   final relative frequency: {_run[-1]:.3f}")

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
