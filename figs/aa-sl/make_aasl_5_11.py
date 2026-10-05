"""AA SL 5.11 の図をつくる。

    python3 figs/aa-sl/make_aasl_5_11.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_11.py

出力: aa-sl/05-calculus/img/aasl-5-11-area.svg
      aa-sl/05-calculus/img/aasl-5-11-below.svg
      aa-sl/05-calculus/img/aasl-5-11-cross.svg
      aa-sl/05-calculus/img/aasl-5-11-between.svg

(area) x 軸より上にある曲線と x 軸ではさまれた部分。
(below) y = x^2 - 4。-2 から 2 まで、ずっと x 軸の下。
(cross) y = 2x - x^2。定積分は A1 - A2、面積は A1 + A2。
(between) 2 曲線ではさまれた面積。上の式から下の式を引く。

★ 具体的な数値や答えは入れません。ラベルはすべて英語です。

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

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "05-calculus", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
FILL = "#cfe0f2"
SHADE = "#fbe3c2"

fig0, ax0 = plt.subplots(figsize=(6.1, 3.3))
fig1, ax1 = plt.subplots(figsize=(6.1, 3.6))
fig2, ax2 = plt.subplots(figsize=(6.1, 4.3))
fig3, ax3 = plt.subplots(figsize=(6.1, 3.4))
# ══════════════════════════════════════════════════════════
# (area) x 軸より上にあるとき
# ══════════════════════════════════════════════════════════
ax0.set_title("A curve above the axis", fontsize=11, color=INK,
              loc="left", pad=10)

A0, B0 = 1.3, 3.8
X0 = np.linspace(0.75, 4.45, 500)
Y0 = 1.25 + 0.95 * np.sin(0.8 * X0 + 0.4) + 0.12 * X0

ax0.plot(X0, Y0, color=ACCENT, linewidth=2.2)
ax0.axhline(0, color=GREY, linewidth=1.1)

_m0 = (X0 >= A0) & (X0 <= B0)
ax0.fill_between(X0[_m0], 0, Y0[_m0], color=FILL)
for _x in (A0, B0):
    _y = 1.25 + 0.95 * np.sin(0.8 * _x + 0.4) + 0.12 * _x
    ax0.plot([_x, _x], [0, _y], color=GREY, linewidth=1.0)

ax0.set_xlim(0.6, 4.6)
ax0.set_ylim(-0.45, 3.3)
ax0.set_xticks([A0, B0])
ax0.set_xticklabels(["$a$", "$b$"], fontsize=11)
ax0.set_yticks([])
for _s in ("top", "right", "left", "bottom"):
    ax0.spines[_s].set_visible(False)

ax0.text(2.55, 0.85, "area", fontsize=12, color=INK, ha="center")
ax0.text(4.12, 2.55, "$y = f(x)$", fontsize=11, color=ACCENT, ha="center")

# ══════════════════════════════════════════════════════════
# (a) x 軸をまたぐ曲線
# ══════════════════════════════════════════════════════════
ax1.set_title("$y = 2x - x^2$", fontsize=11, color=INK,
              loc="left", pad=10)

XS = np.linspace(-0.35, 3.35, 500)
YS = 2 * XS - XS ** 2

ax1.plot(XS, YS, color=ACCENT, linewidth=2.2)
ax1.axhline(0, color=GREY, linewidth=1.1)

_m1 = (XS >= 0) & (XS <= 2)
ax1.fill_between(XS[_m1], 0, YS[_m1], color=FILL)
_m2 = (XS >= 2) & (XS <= 3)
ax1.fill_between(XS[_m2], 0, YS[_m2], color=SHADE)

ax1.set_xlim(-0.5, 3.6)
ax1.set_ylim(-3.5, 1.95)
ax1.set_xticks([0, 2, 3])
ax1.set_xticklabels(["$0$", "$2$", "$3$"], fontsize=11)
ax1.set_yticks([])
for _s in ("top", "right", "left", "bottom"):
    ax1.spines[_s].set_visible(False)

ax1.plot([3, 3], [0, -3], color=GREY, linewidth=0.8, linestyle=(0, (2, 3)))

ax1.text(1.0, 0.38, "$A_{1}$", fontsize=13, color=ACCENT, ha="center")
ax1.text(2.62, -0.78, "$A_{2}$", fontsize=13, color=WARM, ha="center")

# ══════════════════════════════════════════════════════════
# (b) 2 曲線ではさまれた面積
# ══════════════════════════════════════════════════════════
ax2.set_title("Between two curves", fontsize=11, color=INK,
              loc="left", pad=12)

XT = np.linspace(-1.75, 2.6, 500)
UP = 1.9 + 0.45 * XT
LOW = 0.55 * XT ** 2 + 0.15

ax2.plot(XT, UP, color=ACCENT, linewidth=2.2)
ax2.plot(XT, LOW, color=WARM, linewidth=2.2)

_r = np.roots([0.55, -0.45, 0.15 - 1.9])
_r = np.sort(_r.real)
_mm = (XT >= _r[0]) & (XT <= _r[1])
ax2.fill_between(XT[_mm], LOW[_mm], UP[_mm], color=FILL)

ax2.axhline(0, color=GREY, linewidth=1.1)
for _x in _r:
    ax2.plot([_x, _x], [0, 0.55 * _x ** 2 + 0.15], color=GREY,
             linewidth=0.8, linestyle=(0, (2, 3)))

ax2.set_xlim(-2.15, 4.15)
ax2.set_ylim(-0.6, 4.5)
ax2.set_xticks(list(_r))
ax2.set_xticklabels(["$a$", "$b$"], fontsize=11)
ax2.set_yticks([])
for _s in ("top", "right", "left", "bottom"):
    ax2.spines[_s].set_visible(False)

ax2.text(1.6, 2.95, "$y = f(x)$", fontsize=11, color=ACCENT,
         ha="center")
ax2.text(1.7, 0.8, "$y = g(x)$", fontsize=11, color=WARM,
         ha="center")
ax2.text(0.4, 1.55, "area", fontsize=11.5, color=INK, ha="center")


# ══════════════════════════════════════════════════════════
# (below) すっかり x 軸の下にある曲線
# ══════════════════════════════════════════════════════════
ax3.set_title("$y = x^2 - 4$", fontsize=11, color=INK, loc="left", pad=10)

XB = np.linspace(-2.75, 2.75, 500)
YB = XB ** 2 - 4

ax3.plot(XB, YB, color=ACCENT, linewidth=2.2)
ax3.axhline(0, color=GREY, linewidth=1.1)

_mb = (XB >= -2) & (XB <= 2)
ax3.fill_between(XB[_mb], 0, YB[_mb], color=SHADE)

ax3.set_xlim(-3.0, 3.0)
ax3.set_ylim(-4.9, 1.7)
ax3.set_xticks([-2, 2])
ax3.set_xticklabels(["$-2$", "$2$"], fontsize=11)
ax3.set_yticks([])
for _s in ("top", "right", "left", "bottom"):
    ax3.spines[_s].set_visible(False)

ax3.text(0.0, -2.15, "$A$", fontsize=13, color=WARM, ha="center")

for _fig, _name in ((fig0, "aasl-5-11-area.svg"),
                    (fig3, "aasl-5-11-below.svg"),
                    (fig1, "aasl-5-11-cross.svg"),
                    (fig2, "aasl-5-11-between.svg")):
    _fig.tight_layout()
    _p = os.path.join(OUT, _name)
    _fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
    print("wrote", os.path.normpath(_p))
    if os.environ.get("FIG_PNG"):
        _q = _p[:-4] + ".png"
        _fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                     facecolor="white")
        print("wrote", os.path.normpath(_q))
