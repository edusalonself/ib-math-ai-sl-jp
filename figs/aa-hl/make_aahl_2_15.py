"""AA HL 2.15（g(x) >= f(x) を解く）の図をつくる。

    python3 figs/aa-hl/make_aahl_2_15.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-hl/make_aahl_2_15.py  … 目視用の PNG も

出力: aa-hl/02-functions/img/aahl-2-15-idea-a.svg
      aa-hl/02-functions/img/aahl-2-15-idea-b.svg

(a) 2 つのグラフのどちらが上かで、不等式の答えが読める。
(b) 符号の表（sign diagram）：3 つの因数の符号と、積の符号。

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

# ══════════════════════════════════════════════════════════
# (a) どちらが上か
# ══════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(6.0, 4.0))
ax1.set_title("The answer is the stretch where one graph is above the other",
              fontsize=10.5, color=INK, loc="left", pad=10)
_t = np.linspace(-2.6, 3.4, 400)
ax1.plot(_t, _t ** 2, color=ACCENT, linewidth=1.8)
ax1.plot(_t, _t + 2.0, color=WARM, linewidth=1.8)
_m = (_t >= -1.0) & (_t <= 2.0)
ax1.fill_between(_t[_m], _t[_m] ** 2, _t[_m] + 2.0, color=WARM, alpha=0.14)
for _r in (-1.0, 2.0):
    ax1.plot([_r], [_r ** 2], "o", color=INK, markersize=5)
    ax1.plot([_r, _r], [-1.2, _r ** 2], color=GREY, linestyle=":", linewidth=0.9)
ax1.text(-1.0, -1.7, "$x=-1$", ha="center", va="center", fontsize=9.5, color=GREY)
ax1.text(2.0, -1.7, "$x=2$", ha="center", va="center", fontsize=9.5, color=GREY)
ax1.text(-2.4, 7.4, "$y=f(x)$", ha="left", va="center", fontsize=9.5,
         color=ACCENT)
ax1.text(3.3, 4.6, "$y=g(x)$", ha="right", va="center", fontsize=9.5,
         color=WARM)
ax1.text(0.5, 1.2, "$g(x) \\geq f(x)$", ha="center", va="center", fontsize=9.5,
         color=WARM)
ax1.text(-2.4, -2.6, "the ends of the shaded stretch are the crossing points",
         ha="left", va="center", fontsize=9, color=GREY)
ax1.set_xlim(-2.8, 3.6)
ax1.set_ylim(-3.2, 8.4)
ax1.set_xticks([])
ax1.set_yticks([])
ax1.spines["left"].set_position("zero")
ax1.spines["bottom"].set_position(("data", -1.2))
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.spines["left"].set_color(GREY)
ax1.spines["bottom"].set_color(GREY)

# ══════════════════════════════════════════════════════════
# (b) 符号の表
# ══════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(6.2, 3.0))
ax2.set_title("A sign diagram: multiply the signs down each column",
              fontsize=10.5, color=INK, loc="left", pad=10)
ax2.set_xlim(-0.6, 4.4)
ax2.set_ylim(-0.4, 4.1)
ax2.axis("off")
ROOTS = [(1.0, "$-2$"), (2.0, "$0$"), (3.0, "$2$")]
ROWS = [
    ("$x+2$", 3.2, ["$-$", "$+$", "$+$", "$+$"]),
    ("$x$", 2.4, ["$-$", "$-$", "$+$", "$+$"]),
    ("$x-2$", 1.6, ["$-$", "$-$", "$-$", "$+$"]),
    ("product", 0.6, ["$-$", "$+$", "$-$", "$+$"]),
]
CENTRES = [0.55, 1.5, 2.5, 3.65]
for _lab, _yy, _signs in ROWS:
    _col = INK if _lab != "product" else ACCENT
    ax2.text(-0.55, _yy, _lab, ha="left", va="center", fontsize=10,
             color=_col)
    for _cx, _s in zip(CENTRES, _signs):
        ax2.text(_cx, _yy, _s, ha="center", va="center", fontsize=11,
                 color=_col)
    if _lab == "product":
        ax2.plot([0.2, 4.2], [1.15, 1.15], color=GREY, linewidth=0.9)
ax2.annotate("", xy=(4.3, 0.0), xytext=(0.2, 0.0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.0))
for _rx, _rl in ROOTS:
    ax2.plot([_rx, _rx], [0.1, 3.6], color=GREY, linestyle=":", linewidth=0.9)
    ax2.plot([_rx], [0.0], "o", color=WARM, markersize=5)
    ax2.text(_rx, -0.3, _rl, ha="center", va="center", fontsize=9.5,
             color=WARM)
ax2.text(4.35, 0.32, "$x$", ha="right", va="center", fontsize=9.5,
         color=GREY)

for _fig, _name in ((fig1, "a"), (fig2, "b")):
    _fig.tight_layout()
    _fig.savefig(os.path.join(OUT, "aahl-2-15-idea-%s.svg" % _name),
                 format="svg", bbox_inches="tight")
    if os.environ.get("FIG_PNG"):
        _fig.savefig(os.path.join(OUT, "aahl-2-15-idea-%s.png" % _name),
                     format="png", dpi=150, bbox_inches="tight")
print("wrote", OUT)
