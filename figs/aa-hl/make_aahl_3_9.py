"""AA HL 3.9（相反三角関数と逆三角関数）の図をつくる。

    python3 figs/aa-hl/make_aahl_3_9.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_3_9.py  … 目視用の PNG も

出力: aa-hl/03-geometry-and-trigonometry/img/aahl-3-9-idea-a.svg
      aa-hl/03-geometry-and-trigonometry/img/aahl-3-9-idea-b.svg

(a) y = cos x と y = sec x：cos の零点が sec の漸近線になる。
(b) arcsin・arccos・arctan のグラフと、それぞれの range。

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

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-hl", "03-geometry-and-trigonometry",
                   "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
PI = np.pi


def frame(ax):
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GREY)
    ax.spines["bottom"].set_color(GREY)


# ══════════════════════════════════════════════════════════
# (a) cos と sec
# ══════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(6.2, 4.0))
ax1.set_title("Where $\\cos x$ is zero, $\\sec x$ has an asymptote",
              fontsize=10.5, color=INK, loc="left", pad=10)
_t = np.linspace(-2.2 * PI, 2.2 * PI, 1200)
ax1.plot(_t, np.cos(_t), color=ACCENT, linewidth=1.6)
_breaks = [-1.5 * PI, -0.5 * PI, 0.5 * PI, 1.5 * PI]
_edges = [-2.2 * PI] + _breaks + [2.2 * PI]
for _a, _b in zip(_edges[:-1], _edges[1:]):
    _s = np.linspace(_a + 0.02, _b - 0.02, 400)
    _y = 1.0 / np.cos(_s)
    _m = np.abs(_y) <= 4.0
    ax1.plot(_s[_m], _y[_m], color=WARM, linewidth=1.8)
for _xa in _breaks:
    ax1.axvline(_xa, color=GREY, linestyle="--", linewidth=0.9)
ax1.set_xticks([-2 * PI, -PI, 0, PI, 2 * PI])
ax1.set_xticklabels(["$-2\\pi$", "$-\\pi$", "", "$\\pi$", "$2\\pi$"],
                    fontsize=9)
ax1.set_yticks([-1, 1])
ax1.set_yticklabels(["$-1$", "$1$"], fontsize=9)
ax1.text(-2.1 * PI, 3.4, "$y=\\sec x$", ha="left", va="center", fontsize=9.5,
         color=WARM)
ax1.text(0.35, 1.25, "$y=\\cos x$", ha="left", va="center", fontsize=9.5,
         color=ACCENT)
ax1.text(-2.1 * PI, -3.6, "$|\\sec x| \\geq 1$ always: it never enters the strip",
         ha="left", va="center", fontsize=9, color=GREY,
         bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
ax1.set_xlim(-2.3 * PI, 2.3 * PI)
ax1.set_ylim(-4.2, 4.2)
frame(ax1)

# ══════════════════════════════════════════════════════════
# (b) 3 つの逆三角関数
# ══════════════════════════════════════════════════════════
fig2, axes2 = plt.subplots(1, 3, figsize=(6.6, 2.5))
_u = np.linspace(-1.0, 1.0, 400)
_w = np.linspace(-6.0, 6.0, 500)

axes2[0].plot(_u, np.arcsin(_u), color=ACCENT, linewidth=1.8)
axes2[0].set_title("$y=\\arcsin x$", fontsize=10, color=ACCENT, pad=6)
axes2[0].set_xlim(-1.6, 1.6)
axes2[0].set_ylim(-2.4, 2.4)
axes2[0].set_yticks([-PI / 2, PI / 2])
axes2[0].set_yticklabels(["$-\\pi/2$", "$\\pi/2$"], fontsize=8)
axes2[0].set_xticks([-1, 1])
axes2[0].set_xticklabels(["$-1$", "$1$"], fontsize=8)

axes2[1].plot(_u, np.arccos(_u), color=ACCENT, linewidth=1.8)
axes2[1].set_title("$y=\\arccos x$", fontsize=10, color=ACCENT, pad=6)
axes2[1].set_xlim(-1.6, 1.6)
axes2[1].set_ylim(-0.6, 3.8)
axes2[1].set_yticks([0, PI])
axes2[1].set_yticklabels(["$0$", "$\\pi$"], fontsize=8)
axes2[1].set_xticks([-1, 1])
axes2[1].set_xticklabels(["$-1$", "$1$"], fontsize=8)

axes2[2].plot(_w, np.arctan(_w), color=ACCENT, linewidth=1.8)
for _ya in (-PI / 2, PI / 2):
    axes2[2].axhline(_ya, color=WARM, linestyle="--", linewidth=1.0)
axes2[2].set_title("$y=\\arctan x$", fontsize=10, color=ACCENT, pad=6)
axes2[2].set_xlim(-6.5, 6.5)
axes2[2].set_ylim(-2.4, 2.4)
axes2[2].set_yticks([-PI / 2, PI / 2])
axes2[2].set_yticklabels(["$-\\pi/2$", "$\\pi/2$"], fontsize=8)
axes2[2].set_xticks([])

for _ax in axes2:
    frame(_ax)
    _ax.tick_params(length=2, colors=GREY)
fig2.suptitle("The range is cut so that each input gives one output",
              fontsize=10.5, color=INK, x=0.02, ha="left", y=1.05)

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-3-9-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-3-9-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
