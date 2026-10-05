"""AA SL 5.8 の図をつくる。

    python3 figs/aa-sl/make_aasl_5_8.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_8.py

出力: aa-sl/05-calculus/img/aasl-5-8-idea-a.svg
      aa-sl/05-calculus/img/aasl-5-8-concavity.svg
      aa-sl/05-calculus/img/aasl-5-8-box.svg

(a) 極大・極小・変曲点と、concave-up / concave-down の範囲。
(concavity) 接線を 3 本ならべて、傾きの変わり方を見せる。
(box) 正方形の板の四隅を切り取って、ふたのない箱を作る。

★ 使う関数 f(x) = x^3/3 - 2x^2 + 3x は、例題・演習では使いません。
★ 数値の答えは入れません。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * \\le \\ge は読めない → \\leq \\geq を使う
  * \\bigl \\bigr \\Box は読めない → ふつうの ( ) と文字を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "05-calculus", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
FILL = "#e8f0f9"
SHADE = "#fdf0dc"

# f(x) = x^3/3 - 2x^2 + 3x
X = np.linspace(-0.5, 4.5, 500)
F = X ** 3 / 3 - 2 * X ** 2 + 3 * X

fig1, ax1 = plt.subplots(figsize=(6.1, 5.4))
# ══════════════════════════════════════════════════════════
# (a) 極大・極小・変曲点
# ══════════════════════════════════════════════════════════
ax1.set_title("Maximum, minimum and point of inflexion", fontsize=11,
              color=INK, loc="left", pad=12)
ax1.plot(X, F, color=ACCENT, linewidth=2.2)
ax1.axhline(0, color=GREY, linewidth=0.9)
ax1.set_xlim(-0.6, 4.6)
ax1.set_ylim(-2.6, 3.6)
ax1.set_xticks([1, 2, 3])
ax1.set_yticks([])
for _s in ("top", "right", "left", "bottom"):
    ax1.spines[_s].set_visible(False)
ax1.tick_params(axis="x", colors=GREY, labelsize=9, length=0)
ax1.set_xlabel("$x$", fontsize=10, color=GREY, labelpad=2)

PTS = ((1.0, 4.0 / 3.0), (2.0, 2.0 / 3.0), (3.0, 0.0))
for _px, _py in PTS:
    ax1.plot([_px], [_py], "o", color=INK, markersize=6, zorder=5)
    ax1.plot([_px, _px], [-2.6, _py], color=GREY, linewidth=0.7,
             linestyle=(0, (3, 3)), alpha=0.75)

AR = dict(arrowstyle="->", linewidth=1.0)
ax1.annotate("local maximum", xy=(0.95, 1.50), xytext=(-0.45, 2.95),
             fontsize=9.5, color=INK, arrowprops=dict(color=GREY, **AR))
ax1.annotate("point of inflexion", xy=(2.05, 0.50), xytext=(2.35, 2.20),
             fontsize=9.5, color=WARM, arrowprops=dict(color=WARM, **AR))
ax1.annotate("local minimum", xy=(3.0, -0.18), xytext=(3.25, -1.35),
             fontsize=9.5, color=INK, arrowprops=dict(color=GREY, **AR))

# concavity の帯
ax1.plot([-0.5, 2.0], [-2.15, -2.15], color=WARM, linewidth=3.0,
         solid_capstyle="butt")
ax1.plot([2.0, 4.5], [-2.15, -2.15], color=ACCENT, linewidth=3.0,
         solid_capstyle="butt")
ax1.text(0.75, -2.30, "concave-down", fontsize=9, color=WARM, ha="center",
         va="top")
ax1.text(3.25, -2.30, "concave-up", fontsize=9, color=ACCENT, ha="center",
         va="top")

# ══════════════════════════════════════════════════════════
# (concavity) concave-up と concave-down
# ══════════════════════════════════════════════════════════
figC, axC = plt.subplots(1, 2, figsize=(7.4, 2.9))


def _panel(ax, up):
    _t = np.linspace(-1.6, 1.6, 300)
    _a = 0.42 if up else -0.42
    _col = ACCENT if up else WARM
    ax.plot(_t, _a * _t ** 2, color=_col, linewidth=2.3)
    for _x0 in (-1.1, 0.0, 1.1):
        _g = 2 * _a * _x0
        _h = 0.40
        ax.plot([_x0 - _h, _x0 + _h],
                [_a * _x0 ** 2 - _g * _h, _a * _x0 ** 2 + _g * _h],
                color=INK, linewidth=1.6)
        ax.plot([_x0], [_a * _x0 ** 2], "o", color=INK, markersize=4)
    ax.set_xlim(-2.0, 2.0)
    ax.set_ylim(-1.55, 1.55)
    ax.axis("off")
    ax.set_title("concave-up:  $f'' > 0$" if up
                 else "concave-down:  $f'' < 0$",
                 fontsize=11, color=INK, pad=8)
    ax.text(0, -1.42, "the tangents turn anticlockwise" if up
            else "the tangents turn clockwise",
            fontsize=9, color=GREY, ha="center")


_panel(axC[0], True)
_panel(axC[1], False)
figC.tight_layout()

figB, axB = plt.subplots(figsize=(6.1, 5.6))
# ══════════════════════════════════════════════════════════
# (box) ふたのない箱
# ══════════════════════════════════════════════════════════
axB.set_title("An open box made from a square sheet", fontsize=11,
              color=INK, loc="left", pad=12)
axB.set_xlim(-1.3, 11.3)
axB.set_ylim(-2.6, 10.0)
axB.axis("off")
axB.set_aspect("equal", adjustable="box")

S = 8.0     # 板の 1 辺
C = 1.7     # 切り取る正方形の 1 辺
X0, Y0 = 0.0, 0.6

axB.add_patch(Rectangle((X0, Y0), S, S, facecolor="none", edgecolor=INK,
                        linewidth=1.6))
for _cx, _cy in ((X0, Y0), (X0 + S - C, Y0), (X0, Y0 + S - C),
                 (X0 + S - C, Y0 + S - C)):
    axB.add_patch(Rectangle((_cx, _cy), C, C, facecolor=SHADE,
                            edgecolor=WARM, linewidth=1.3))

# 折り目
for _v in (X0 + C, X0 + S - C):
    axB.plot([_v, _v], [Y0 + C, Y0 + S - C], color=GREY, linewidth=0.9,
             linestyle=(0, (4, 3)))
    axB.plot([X0 + C, X0 + S - C], [Y0 + _v - X0, Y0 + _v - X0], color=GREY,
             linewidth=0.9, linestyle=(0, (4, 3)))

# 寸法
axB.annotate("", xy=(X0, Y0 - 0.55), xytext=(X0 + C, Y0 - 0.55),
             arrowprops=dict(arrowstyle="<->", color=WARM, linewidth=1.1))
axB.text(X0 + C / 2, Y0 - 1.15, "$x$", fontsize=12, color=WARM, ha="center",
         va="center")
axB.annotate("", xy=(X0 + C, Y0 - 0.55), xytext=(X0 + S - C, Y0 - 0.55),
             arrowprops=dict(arrowstyle="<->", color=ACCENT, linewidth=1.1))
axB.text(X0 + S / 2, Y0 - 1.15, "$a - 2x$", fontsize=12, color=ACCENT,
         ha="center", va="center")
axB.annotate("", xy=(X0 - 0.55, Y0), xytext=(X0 - 0.55, Y0 + S),
             arrowprops=dict(arrowstyle="<->", color=INK, linewidth=1.1))
axB.text(X0 - 1.05, Y0 + S / 2, "$a$", fontsize=12, color=INK, ha="center",
         va="center")

axB.text(X0 + S + 0.55, Y0 + S - C / 2, "cut off", fontsize=9.5, color=WARM,
         ha="left", va="center")
axB.text(X0 + S + 0.55, Y0 + S / 2, "fold up", fontsize=9.5, color=GREY,
         ha="left", va="center")

axB.text(-1.2, -1.95, "base $(a - 2x)$ by $(a - 2x)$, height $x$",
         fontsize=10, color=INK, ha="left", va="center")

for _fig, _name in ((fig1, "aasl-5-8-idea-a.svg"),
                    (figC, "aasl-5-8-concavity.svg"),
                    (figB, "aasl-5-8-box.svg")):
    _fig.tight_layout()
    _p = os.path.join(OUT, _name)
    _fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
    print("wrote", os.path.normpath(_p))
    if os.environ.get("FIG_PNG"):
        _q = _p[:-4] + ".png"
        _fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                     facecolor="white")
        print("wrote", os.path.normpath(_q))
