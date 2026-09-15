"""AA SL 5.5 の図をつくる。

    python3 figs/aa-sl/make_aasl_5_5.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_5.py

出力: aa-sl/05-calculus/img/aasl-5-5-idea.svg

(a) 微分と積分が逆向きであること、+C が要ること
    （同じ導関数をもつ曲線が、縦にずれて何本もある）。
(b) f(x) > 0 のとき、曲線と x 軸ではさまれた部分の面積が定積分になること。

★ 数値の答えは入れません（例題・演習と重ならないように）。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * \\le \\ge は読めない → \\leq \\geq を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "05-calculus", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
FILL = "#cfe0f2"
LIGHT = "#9db8d4"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.8, 5.0))

# ══════════════════════════════════════════════════════════
# (a) 同じ導関数をもつ曲線は、縦にずれて何本もある
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Why the constant is needed", fontsize=11, color=INK,
              loc="left", pad=12)

T = np.linspace(-1.6, 1.6, 300)


def g(t):
    return t ** 3 - 2.0 * t


ax1.set_xlim(-2.15, 2.75)
ax1.set_ylim(-4.75, 3.35)
ax1.axis("off")
ax1.plot([-2.0, 2.45], [0, 0], color=GREY, linewidth=1.0)
ax1.plot([0, 0], [-3.15, 3.05], color=GREY, linewidth=1.0)
ax1.text(2.52, -0.05, "$x$", fontsize=10, color=GREY, va="center")
ax1.text(-0.08, 3.17, "$y$", fontsize=10, color=GREY, ha="right")

for _c, _col, _lw in ((1.5, LIGHT, 1.4), (0.0, ACCENT, 2.0),
                      (-1.5, LIGHT, 1.4)):
    ax1.plot(T, g(T) + _c, color=_col, linewidth=_lw)

_x0 = 1.25
_m = 3 * _x0 ** 2 - 2.0
for _c in (1.5, 0.0, -1.5):
    _tt = np.array([_x0 - 0.30, _x0 + 0.30])
    ax1.plot(_tt, g(_x0) + _c + _m * (_tt - _x0), color=WARM, linewidth=1.5)
    ax1.plot([_x0], [g(_x0) + _c], "o", color=WARM, markersize=4.5)

_xc = 2.05
for _lo, _hi in ((-1.5, 0.0), (0.0, 1.5)):
    ax1.annotate("", xy=(_xc, g(1.6) + _hi), xytext=(_xc, g(1.6) + _lo),
                 arrowprops=dict(arrowstyle="<->", color=GREY, linewidth=1.1))
ax1.text(_xc + 0.12, g(1.6), "$+C$", fontsize=11, color=GREY, ha="left",
         va="center")

ax1.text(-2.05, -3.75, "the curves differ only by a vertical shift",
         fontsize=10, color=INK)
ax1.text(-2.05, -4.40, "so they all have the same gradient at each $x$",
         fontsize=10, color=WARM)

# ══════════════════════════════════════════════════════════
# (b) 面積と定積分
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) Area under a curve that stays above the axis", fontsize=11,
              color=INK, loc="left", pad=12)

U = np.linspace(0.15, 4.6, 400)


def h(t):
    return 0.22 * (t - 1.1) ** 2 + 1.15


ax2.plot(U, h(U), color=ACCENT, linewidth=2.0)
ax2.set_xlim(-0.55, 5.3)
ax2.set_ylim(-1.55, 4.3)
ax2.axis("off")
ax2.plot([-0.35, 5.1], [0, 0], color=GREY, linewidth=1.0)
ax2.plot([0, 0], [0, 4.0], color=GREY, linewidth=1.0)
ax2.text(5.18, -0.05, "$x$", fontsize=10, color=GREY, va="center")
ax2.text(-0.08, 4.12, "$y$", fontsize=10, color=GREY, ha="right")

AA, BB = 1.3, 3.9
MK = (U >= AA) & (U <= BB)
ax2.fill_between(U[MK], 0, h(U[MK]), color=FILL, alpha=0.95)
for _x in (AA, BB):
    ax2.plot([_x, _x], [0, h(_x)], color=ACCENT, linewidth=1.3)
    ax2.plot([_x, _x], [0, -0.14], color=GREY, linewidth=1.0)

ax2.text(AA, -0.28, "$a$", fontsize=11, color=INK, ha="center", va="top")
ax2.text(BB, -0.28, "$b$", fontsize=11, color=INK, ha="center", va="top")
ax2.text(4.75, h(4.55) + 0.15, "$y = f(x)$", fontsize=10.5, color=ACCENT,
         ha="right")
ax2.text((AA + BB) / 2, 0.68, "area", fontsize=11, color=INK, ha="center")

ax2.text(-0.35, -0.92, r"$A = \int_{a}^{b} y \, dx$   when $f(x) > 0$ "
         "between $a$ and $b$", fontsize=11.5, color=ACCENT)
ax2.text(-0.35, -1.42, "write the expression first, then work out its value",
         fontsize=9.5, color=GREY)

fig.tight_layout(w_pad=2.2)
path = os.path.join(OUT, "aasl-5-5-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))
print("  gradients at x = %.2f:" % _x0,
      [round(3 * _x0 ** 2 - 2.0, 6) for _c in (1.5, 0.0, -1.5)])
print("  h(a) = %.3f  h(b) = %.3f  (both positive)" % (h(AA), h(BB)))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
