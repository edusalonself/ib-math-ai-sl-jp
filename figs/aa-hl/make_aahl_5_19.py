"""AA HL 5.19（Maclaurin 級数）の図をつくる。

    python3 figs/aa-hl/make_aahl_5_19.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_5_19.py  … 目視用の PNG も

出力: aa-hl/05-calculus/img/aahl-5-19-idea-a.svg
      aa-hl/05-calculus/img/aahl-5-19-idea-b.svg

(a) sin x と、その Maclaurin 多項式（1 次・3 次・5 次・7 次）。
(b) 公式集の級数から、新しい級数を作る 4 つの道。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → 使わない
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
from matplotlib.patches import FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-hl", "05-calculus", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
GREEN = "#15803d"

# ══════════════════════════════════════════════════════════
# (a) sin x と部分和
# ══════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(5.8, 3.4))
ax1.set_title("more terms, a longer stretch that matches", fontsize=10.5,
              color=INK, loc="left", pad=10)

t = np.linspace(-5.2, 5.2, 800)
ax1.plot(t, np.sin(t), color=INK, linewidth=2.2, zorder=5)
P1 = t
P3 = t - t ** 3 / 6
P5 = P3 + t ** 5 / 120
P7 = P5 - t ** 7 / 5040
for _p, _col, _lab, _yl in ((P1, GREY, "degree $1$", 1.55),
                            (P3, ACCENT, "degree $3$", 0.95),
                            (P5, WARM, "degree $5$", 0.35),
                            (P7, GREEN, "degree $7$", -0.25)):
    ax1.plot(t, _p, color=_col, linewidth=1.4, linestyle=(0, (5, 3)),
             zorder=3)
    ax1.text(5.75, _yl, _lab, fontsize=9, color=_col)

ax1.text(5.75, 2.10, "$y = \\sin x$", fontsize=10, color=INK)
ax1.set_xlim(-5.7, 8.4)
ax1.set_ylim(-2.7, 2.3)
ax1.plot([-5.3, 5.3], [0, 0], color=GREY, linewidth=0.8, zorder=0)
ax1.set_xticks([-np.pi, 0, np.pi])
ax1.set_xticklabels(["$-\\pi$", "$0$", "$\\pi$"])
ax1.set_yticks([])
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.spines["left"].set_visible(False)
ax1.tick_params(labelsize=9, colors=GREY)

# ══════════════════════════════════════════════════════════
# (b) 新しい級数を作る 4 つの道
# ══════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(6.2, 3.0))
ax2.set_title("four ways to build a new series from a known one",
              fontsize=10.5, color=INK, loc="left", pad=10)


def box(x, y, w, h, text, col, fs=9.0):
    ax2.add_patch(FancyBboxPatch((x, y), w, h,
                                 boxstyle="round,pad=0.10,rounding_size=0.12",
                                 facecolor="white", edgecolor=col,
                                 linewidth=1.4, zorder=2))
    ax2.text(x + w / 2, y + h / 2, text, fontsize=fs, color=INK,
             ha="center", va="center", zorder=3)


def link(p, q):
    ax2.annotate("", xy=q, xytext=p,
                 arrowprops=dict(arrowstyle="-|>", color=GREY, linewidth=1.3,
                                 shrinkA=3, shrinkB=3))


box(3.1, 3.5, 3.8, 0.9, "a series from the booklet", ACCENT, fs=9.6)
box(0.0, 1.4, 2.2, 0.8, "substitute", WARM, fs=9.2)
box(2.6, 1.4, 2.2, 0.8, "multiply", WARM, fs=9.2)
box(5.2, 1.4, 2.2, 0.8, "differentiate", WARM, fs=9.2)
box(7.8, 1.4, 2.2, 0.8, "integrate", WARM, fs=9.2)
for _cx in (1.1, 3.7, 6.3, 8.9):
    link((5.0, 3.5), (_cx, 2.3))

ax2.text(0.0, 0.55, "the new series is valid where the original one is,"
         " after the same substitution", fontsize=9, color=GREY)
ax2.set_xlim(-0.3, 10.3)
ax2.set_ylim(0.1, 4.7)
ax2.axis("off")

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-5-19-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-5-19-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
