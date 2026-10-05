"""AA HL 1.16（連立 1 次方程式）の図をつくる。

    python3 figs/aa-hl/make_aahl_1_16.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_1_16.py  … 目視用の PNG も

出力: aa-hl/01-number-and-algebra/img/aahl-1-16-idea-a.svg
      aa-hl/01-number-and-algebra/img/aahl-1-16-idea-b.svg

(a) row reduction のあと、最後の行がどうなるかで 3 つに分かれる。
(b) 2 変数で見た 3 つの形：交わる・重なる・平行。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → 文字で並べる
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
OUT = os.path.join(HERE, "..", "..", "aa-hl", "01-number-and-algebra", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"

fig1, ax1 = plt.subplots(figsize=(6.4, 4.0))
fig2, axes2 = plt.subplots(1, 3, figsize=(6.4, 2.6))

# ══════════════════════════════════════════════════════════
# (a) row reduction のあとの 3 つの形
# ══════════════════════════════════════════════════════════
ax1.set_title("After row reduction, the last row decides everything",
              fontsize=10.5, color=INK, loc="left", pad=10)
ax1.set_xlim(0.0, 1.0)
ax1.set_ylim(0.0, 1.0)
ax1.axis("off")

ROWS = [
    ("one solution", ACCENT,
     [("1", "1", "1", "6"), ("0", "1", "1", "5"), ("0", "0", "1", "3")],
     "the last row gives $z$"),
    ("infinitely many", GREY,
     [("1", "1", "1", "6"), ("0", "1", "1", "5"), ("0", "0", "0", "0")],
     "the last row says $0=0$"),
    ("no solution", WARM,
     [("1", "1", "1", "6"), ("0", "1", "1", "5"), ("0", "0", "0", "4")],
     "the last row says $0=4$"),
]

_y0 = 0.86
for _name, _col, _mat, _note in ROWS:
    ax1.text(0.02, _y0, _name, ha="left", va="center", fontsize=10,
             color=_col, fontweight="bold")
    _bx, _by = 0.30, _y0 - 0.115
    ax1.add_patch(FancyBboxPatch((_bx, _by), 0.30, 0.23,
                                 boxstyle="round,pad=0.012",
                                 linewidth=1.2, edgecolor=_col,
                                 facecolor="none"))
    for _i, _row in enumerate(_mat):
        _ry = _y0 + 0.068 - _i * 0.068
        for _j, _v in enumerate(_row[:3]):
            ax1.text(_bx + 0.045 + _j * 0.060, _ry, _v, ha="center",
                     va="center", fontsize=9.5, color=INK)
        ax1.text(_bx + 0.262, _ry, _row[3], ha="center", va="center",
                 fontsize=9.5, color=INK)
    ax1.plot([_bx + 0.225, _bx + 0.225], [_by + 0.018, _by + 0.212],
             color=GREY, linewidth=0.9)
    ax1.text(0.64, _y0, _note, ha="left", va="center", fontsize=9.5,
             color=INK)
    _y0 -= 0.30

ax1.text(0.02, 0.03,
         "the left of the line is the coefficients, the right is the constants",
         ha="left", va="center", fontsize=9, color=GREY)

# ══════════════════════════════════════════════════════════
# (b) 2 変数で見た 3 つの形
# ══════════════════════════════════════════════════════════
_t = np.linspace(-1.0, 4.0, 200)
PANELS = [
    ("one solution", ACCENT,
     [(1.0, 0.4), (-0.8, 3.2)], True, "they cross once"),
    ("infinitely many", GREY,
     [(0.6, 1.0), (0.6, 1.0)], False, "the two lines coincide"),
    ("no solution", WARM,
     [(0.6, 0.6), (0.6, 2.2)], False, "parallel, never meet"),
]
for _ax, (_name, _col, _lines, _mark, _note) in zip(axes2, PANELS):
    _ax.set_title(_name, fontsize=9.5, color=_col, pad=6)
    for _idx, (_m, _c) in enumerate(_lines):
        if _idx == 0:
            _ax.plot(_t, _m * _t + _c, "-", color=_col, linewidth=3.4,
                     alpha=0.35)
        else:
            _ax.plot(_t, _m * _t + _c, "--", color=_col, linewidth=1.6)
    if _mark:
        _xs = (3.2 - 0.4) / (1.0 + 0.8)
        _ax.plot([_xs], [_xs + 0.4], "o", color=_col, markersize=6)
    _ax.text(1.5, -0.35, _note, ha="center", va="center", fontsize=8.5,
             color=GREY)
    _ax.set_xlim(-1.0, 4.0)
    _ax.set_ylim(-0.6, 4.4)
    _ax.set_xticks([])
    _ax.set_yticks([])
    for _sp in ("top", "right"):
        _ax.spines[_sp].set_visible(False)
    _ax.spines["left"].set_color(GREY)
    _ax.spines["bottom"].set_color(GREY)

fig2.suptitle("Two equations in two unknowns: the same three cases",
              fontsize=10.5, color=INK, x=0.02, ha="left", y=0.99)

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-1-16-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-1-16-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
