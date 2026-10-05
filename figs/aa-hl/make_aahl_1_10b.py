"""AA HL 1.10b（二項定理の拡張）の図をつくる。

    python3 figs/aa-hl/make_aahl_1_10b.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_1_10b.py  … 目視用の PNG も

出力: aa-hl/01-number-and-algebra/img/aahl-1-10b-idea-a.svg
      aa-hl/01-number-and-algebra/img/aahl-1-10b-idea-b.svg

(a) 係数のかけ算の鎖。n = 3 では 4 番目の因数が 0 になって止まるが、
    n = 1/2 では 0 になる因数が現れないので、いつまでも続く。
(b) (1+x)^(-1) と、その部分和 S1, S2, S3。|x| が小さいところでは重なり、
    x が -1 や 1 に近づくと離れていく。

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

fig1, ax1 = plt.subplots(figsize=(6.0, 3.2))
fig2, ax2 = plt.subplots(figsize=(6.0, 4.0))

# ══════════════════════════════════════════════════════════
# (a) 係数の鎖：止まる n と、止まらない n
# ══════════════════════════════════════════════════════════
ax1.set_title("The chain of factors $n,\\ n-1,\\ n-2,\\ \\ldots$",
              fontsize=11, color=INK, loc="left", pad=10)
ax1.set_xlim(0.0, 1.0)
ax1.set_ylim(0.0, 1.0)
ax1.axis("off")

TOP = [("$3$", INK), ("$2$", INK), ("$1$", INK), ("$0$", WARM)]
BOT = [("$\\frac{1}{2}$", INK), ("$-\\frac{1}{2}$", INK),
       ("$-\\frac{3}{2}$", INK), ("$-\\frac{5}{2}$", INK)]

ax1.text(0.02, 0.80, "$n = 3$", ha="left", va="center",
         fontsize=11, color=ACCENT)
ax1.text(0.02, 0.34, "$n = \\frac{1}{2}$", ha="left", va="center",
         fontsize=11, color=ACCENT)
for _k, (_s, _c) in enumerate(TOP):
    ax1.text(0.26 + 0.14 * _k, 0.80, _s, ha="center", va="center",
             fontsize=13, color=_c)
for _k, (_s, _c) in enumerate(BOT):
    ax1.text(0.26 + 0.14 * _k, 0.34, _s, ha="center", va="center",
             fontsize=13, color=_c)
for _k in range(3):
    for _y in (0.80, 0.34):
        ax1.annotate("", xy=(0.26 + 0.14 * (_k + 1) - 0.045, _y),
                     xytext=(0.26 + 0.14 * _k + 0.045, _y),
                     arrowprops=dict(arrowstyle="->", color=GREY,
                                     linewidth=1.0))
ax1.text(0.84, 0.80, "$\\cdots$", ha="left", va="center",
         fontsize=13, color=GREY)
ax1.text(0.84, 0.34, "$\\cdots$", ha="left", va="center",
         fontsize=13, color=GREY)
ax1.text(0.50, 0.60, "a factor of $0$ arrives, so the expansion stops",
         ha="center", va="center", fontsize=10, color=WARM)
ax1.text(0.50, 0.12, "no factor is ever $0$, so the expansion never stops",
         ha="center", va="center", fontsize=10, color=INK)

# ══════════════════════════════════════════════════════════
# (b) 部分和が、|x| < 1 でだけ近づく
# ══════════════════════════════════════════════════════════
ax2.set_title("$(1+x)^{-1}$ and its partial sums", fontsize=11,
              color=INK, loc="left", pad=10)
ax2.axvspan(-1.0, 1.0, color="#eef3f8", zorder=0)
_xl = np.linspace(-1.60, -1.04, 400)
_xr = np.linspace(-0.96, 1.60, 700)
ax2.plot(_xl, 1.0 / (1.0 + _xl), color=INK, linewidth=2.2, zorder=4)
ax2.plot(_xr, 1.0 / (1.0 + _xr), color=INK, linewidth=2.2,
         label="$(1+x)^{-1}$", zorder=4)
_xs = np.linspace(-1.60, 1.60, 900)
for _n, _sty, _col in ((1, (0, (5, 3)), ACCENT),
                       (2, (0, (2, 2)), WARM),
                       (3, (0, (1, 2)), GREY)):
    _y = np.zeros_like(_xs)
    for _r in range(_n + 1):
        _y = _y + (-_xs) ** _r
    ax2.plot(_xs, _y, linestyle=_sty, linewidth=1.6, color=_col,
             label="$S_{%d}$" % _n, zorder=3)
ax2.axvline(-1.0, color=GREY, linewidth=1.0, linestyle=(0, (4, 4)), zorder=1)
ax2.axvline(1.0, color=GREY, linewidth=1.0, linestyle=(0, (4, 4)), zorder=1)
ax2.set_xlim(-1.62, 1.62)
ax2.set_ylim(-2.2, 6.0)
ax2.set_xticks([-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5])
ax2.set_xlabel("$x$", fontsize=10)
ax2.set_ylabel("$y$", fontsize=10)
ax2.text(0.0, 5.45, "$|x| < 1$", ha="center", va="center",
         fontsize=10, color=ACCENT)
ax2.text(-1.36, 5.45, "outside", ha="center", va="center",
         fontsize=9.5, color=GREY)
ax2.text(1.36, 5.45, "outside", ha="center", va="center",
         fontsize=9.5, color=GREY)
ax2.legend(loc="lower left", fontsize=9, frameon=False)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

for _fig, _name in ((fig1, "aahl-1-10b-idea-a.svg"),
                    (fig2, "aahl-1-10b-idea-b.svg")):
    _fig.tight_layout()
    _p = os.path.join(OUT, _name)
    _fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
    print("wrote", os.path.normpath(_p))
    if os.environ.get("FIG_PNG"):
        _q = _p[:-4] + ".png"
        _fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                     facecolor="white")
        print("wrote", os.path.normpath(_q))
