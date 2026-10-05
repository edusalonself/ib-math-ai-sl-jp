"""AA HL 2.12（多項式関数・因数定理・解の和と積）の図をつくる。

    python3 figs/aa-hl/make_aahl_2_12.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_2_12.py  … 目視用の PNG も

出力: aa-hl/02-functions/img/aahl-2-12-idea-a.svg
      aa-hl/02-functions/img/aahl-2-12-idea-b.svg

(a) 3 次関数のグラフと、x 軸との交点・因数の対応。
(b) 重解の重さで、x 軸での形が変わる（またぐ・接する・寝てまたぐ）。

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
OUT = os.path.join(HERE, "..", "..", "aa-hl", "02-functions", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"


def frame(ax):
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GREY)
    ax.spines["bottom"].set_color(GREY)


# ══════════════════════════════════════════════════════════
# (a) 3 次関数と、交点 ↔ 因数
# ══════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(6.2, 4.0))
_x = np.linspace(-2.8, 3.8, 400)
_y = _x ** 3 - 2 * _x ** 2 - 5 * _x + 6
ax1.plot(_x, _y, color=ACCENT, linewidth=1.8)
ax1.set_title("Each crossing of the $x$-axis is one factor",
              fontsize=10.5, color=INK, loc="left", pad=10)
for _r, _lab in ((-2.0, "$x+2$"), (1.0, "$x-1$"), (3.0, "$x-3$")):
    ax1.plot([_r], [0.0], "o", color=WARM, markersize=6)
    ax1.annotate(_lab, xy=(_r, 0.0), xytext=(_r, -7.0), ha="center",
                 fontsize=10, color=WARM,
                 arrowprops=dict(arrowstyle="-", color=WARM, linewidth=0.8))
    ax1.text(_r, 1.4, "$%d$" % int(_r), ha="center", va="bottom",
             fontsize=9.5, color=GREY)
ax1.text(-2.6, 13.0, "$y = x^{3}-2x^{2}-5x+6$", fontsize=10, color=ACCENT)
ax1.text(3.0, -13.5, "three zeros, three linear factors",
         ha="right", va="center", fontsize=9, color=GREY)
ax1.set_xlim(-3.2, 4.0)
ax1.set_ylim(-15.0, 16.0)
ax1.set_xticks([])
ax1.set_yticks([])
frame(ax1)

# ══════════════════════════════════════════════════════════
# (b) 重解の重さと、x 軸での形
# ══════════════════════════════════════════════════════════
fig2, axes2 = plt.subplots(1, 3, figsize=(6.4, 2.5))
_t = np.linspace(-1.6, 1.6, 300)
PANELS = [
    ("$(x-a)$", _t, "crosses straight through", ACCENT),
    ("$(x-a)^{2}$", _t ** 2, "touches and turns back", WARM),
    ("$(x-a)^{3}$", _t ** 3, "flattens, then crosses", GREY),
]
for _ax, (_lab, _yv, _note, _col) in zip(axes2, PANELS):
    _ax.plot(_t, _yv, color=_col, linewidth=1.8)
    _ax.plot([0.0], [0.0], "o", color=_col, markersize=5)
    _ax.set_title(_lab, fontsize=10.5, color=_col, pad=6)
    _ax.text(0.0, -3.4, _note, ha="center", va="center", fontsize=8.5,
             color=GREY)
    _ax.set_xlim(-1.8, 1.8)
    _ax.set_ylim(-2.8, 2.8)
    _ax.set_xticks([])
    _ax.set_yticks([])
    frame(_ax)
fig2.suptitle("How many times the factor appears decides the shape at $x=a$",
              fontsize=10.5, color=INK, x=0.02, ha="left", y=1.02)

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-2-12-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-2-12-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
