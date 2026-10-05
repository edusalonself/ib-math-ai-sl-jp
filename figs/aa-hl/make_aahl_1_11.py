"""AA HL 1.11（部分分数分解）の図をつくる。

    python3 figs/aa-hl/make_aahl_1_11.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_1_11.py  … 目視用の PNG も

出力: aa-hl/01-number-and-algebra/img/aahl-1-11-idea.svg

2/(x-3) と 1/(x+1) を足すと (3x-1)/(x^2-2x-3) になる、という図。
もとの分数は 2 つの簡単な曲線の和である、ということを見せる。
漸近線 x = -1, x = 3 の近くは、線がつながって見えないように切る。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert も読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に例題・演習の答えを書かないこと。
★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-hl", "01-number-and-algebra", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"

fig, ax = plt.subplots(figsize=(6.2, 4.4))

POLES = (-1.0, 3.0)
GAP = 0.18


def pieces(lo, hi):
    """漸近線をまたがないように、区間を切って返す。"""
    cuts = [lo]
    for _p in POLES:
        if lo < _p < hi:
            cuts += [_p - GAP, _p + GAP]
    cuts.append(hi)
    return [(cuts[_i], cuts[_i + 1]) for _i in range(0, len(cuts) - 1, 2)]


def draw(fn, color, style, width, label):
    first = True
    for _a, _b in pieces(-5.0, 7.0):
        _x = np.linspace(_a, _b, 400)
        ax.plot(_x, fn(_x), color=color, linestyle=style, linewidth=width,
                label=label if first else None, zorder=3)
        first = False


draw(lambda t: 2.0 / (t - 3.0), ACCENT, (0, (5, 3)), 1.6,
     "$y = \\dfrac{2}{x-3}$")
draw(lambda t: 1.0 / (t + 1.0), WARM, (0, (2, 2)), 1.6,
     "$y = \\dfrac{1}{x+1}$")
draw(lambda t: 2.0 / (t - 3.0) + 1.0 / (t + 1.0), INK, "-", 2.2,
     "their sum")

for _p in POLES:
    ax.axvline(_p, color=GREY, linewidth=1.0, linestyle=(0, (4, 4)), zorder=1)
ax.axhline(0.0, color="#d0d5db", linewidth=1.0, zorder=0)

ax.set_xlim(-5.0, 7.0)
ax.set_ylim(-5.0, 5.0)
ax.set_xlabel("$x$", fontsize=10)
ax.set_ylabel("$y$", fontsize=10)
ax.set_title("A single fraction, seen as a sum of two simple ones",
             fontsize=11, color=INK, loc="left", pad=10)
# 漸近線は、目盛りの数字で示す（曲線と重なる位置に文字を置かない）
ax.set_xticks([-4, -1, 0, 3, 6])
ax.legend(loc="lower right", fontsize=9.5, frameon=False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout()
_p = os.path.join(OUT, "aahl-1-11-idea.svg")
fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(_p))
if os.environ.get("FIG_PNG"):
    _q = _p[:-4] + ".png"
    fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(_q))
