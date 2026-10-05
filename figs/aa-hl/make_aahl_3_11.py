"""AA HL 3.11（三角関数の関係式とグラフの対称性）の図をつくる。

    python3 figs/aa-hl/make_aahl_3_11.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_3_11.py  … 目視用の PNG も

出力: aa-hl/03-geometry-and-trigonometry/img/aahl-3-11-idea-a.svg
      aa-hl/03-geometry-and-trigonometry/img/aahl-3-11-idea-b.svg

(a) 単位円で θ と π − θ：高さが同じ、横が逆。
(b) y = sin x の x = π/2 についての線対称と、y = cos x の点対称。

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

# ══════════════════════════════════════════════════════════
# (a) 単位円
# ══════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(4.8, 4.4))
ax1.set_title("$\\theta$ and $\\pi-\\theta$: same height, opposite across",
              fontsize=10.5, color=INK, loc="left", pad=10)
_c = np.linspace(0.0, 2.0 * PI, 400)
ax1.plot(np.cos(_c), np.sin(_c), color=GREY, linewidth=1.1)
TH = np.radians(55.0)
P = (np.cos(TH), np.sin(TH))
Q = (-np.cos(TH), np.sin(TH))
for _p, _col, _lab in ((P, ACCENT, "$\\theta$"), (Q, WARM, "$\\pi-\\theta$")):
    ax1.plot([0.0, _p[0]], [0.0, _p[1]], color=_col, linewidth=1.7)
    ax1.plot([_p[0]], [_p[1]], "o", color=_col, markersize=6)
    ax1.plot([_p[0], _p[0]], [0.0, _p[1]], color=_col, linestyle=":",
             linewidth=1.0)
ax1.plot([Q[0], P[0]], [P[1], P[1]], color=GREY, linestyle="--",
         linewidth=0.9)
ax1.axhline(0.0, color=GREY, linewidth=0.9)
ax1.axvline(0.0, color=GREY, linewidth=0.9)
ax1.text(P[0] + 0.06, P[1] + 0.06, "$(\\cos\\theta,\\ \\sin\\theta)$",
         fontsize=9, color=ACCENT)
ax1.text(Q[0] - 0.06, Q[1] + 0.10, "$(-\\cos\\theta,\\ \\sin\\theta)$",
         ha="right", fontsize=9, color=WARM)
ax1.text(0.30, 0.13, "$\\theta$", fontsize=10, color=ACCENT)
ax1.text(-0.42, 0.13, "$\\pi-\\theta$", fontsize=10, color=WARM)
ax1.text(0.0, -1.32, "the $y$-values agree, the $x$-values are negatives",
         ha="center", fontsize=9, color=GREY)
ax1.set_xlim(-1.45, 1.45)
ax1.set_ylim(-1.45, 1.45)
ax1.set_aspect("equal")
ax1.axis("off")

# ══════════════════════════════════════════════════════════
# (b) グラフの対称性
# ══════════════════════════════════════════════════════════
fig2, axes2 = plt.subplots(1, 2, figsize=(6.6, 2.6))
_x = np.linspace(-0.4, 2.4 * PI, 700)

axes2[0].plot(_x, np.sin(_x), color=ACCENT, linewidth=1.7)
axes2[0].axvline(PI / 2, color=WARM, linestyle="--", linewidth=1.1)
axes2[0].plot([PI / 2 - 1.0, PI / 2 + 1.0],
              [np.sin(PI / 2 - 1.0), np.sin(PI / 2 + 1.0)], "o",
              color=WARM, markersize=5)
axes2[0].set_title("$y=\\sin x$ folds about $x=\\dfrac{\\pi}{2}$",
                   fontsize=10, color=INK, pad=8)
axes2[0].text(PI / 2 + 0.15, -1.45, "$x=\\dfrac{\\pi}{2}$", fontsize=9,
              color=WARM)

axes2[1].plot(_x, np.cos(_x), color=ACCENT, linewidth=1.7)
axes2[1].plot([PI / 2], [0.0], "o", color=WARM, markersize=6)
axes2[1].plot([PI / 2 - 1.0, PI / 2 + 1.0],
              [np.cos(PI / 2 - 1.0), np.cos(PI / 2 + 1.0)], "o",
              color=WARM, markersize=5)
axes2[1].set_title("$y=\\cos x$ turns about $\\left(\\dfrac{\\pi}{2},\\ 0\\right)$",
                   fontsize=10, color=INK, pad=8)
axes2[1].text(PI / 2 + 0.2, 0.35, "half turn", fontsize=9, color=WARM)

for _ax in axes2:
    _ax.set_xlim(-0.6, 2.4 * PI)
    _ax.set_ylim(-1.7, 1.7)
    _ax.set_xticks([0, PI, 2 * PI])
    _ax.set_xticklabels(["$0$", "$\\pi$", "$2\\pi$"], fontsize=8)
    _ax.set_yticks([-1, 1])
    _ax.set_yticklabels(["$-1$", "$1$"], fontsize=8)
    _ax.spines["left"].set_position("zero")
    _ax.spines["bottom"].set_position("zero")
    _ax.spines["top"].set_visible(False)
    _ax.spines["right"].set_visible(False)
    _ax.spines["left"].set_color(GREY)
    _ax.spines["bottom"].set_color(GREY)
    _ax.tick_params(length=2, colors=GREY)

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-3-11-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-3-11-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
