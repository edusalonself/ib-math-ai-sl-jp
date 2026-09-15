"""AA SL 5.11b の図をつくる。

    python3 figs/aa-sl/make_aasl_5_11b.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_11b.py

出力: aa-sl/05-calculus/img/aasl-5-11b-idea.svg

(a) x 軸をまたぐ曲線。定積分は A1 - A2、面積は A1 + A2。
(b) 2 曲線ではさまれた面積。上の式から下の式を引く。

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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.4, 5.2))

# ══════════════════════════════════════════════════════════
# (a) x 軸をまたぐ曲線
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) A curve that crosses the axis", fontsize=11, color=INK,
              loc="left", pad=12)

P, Q = 1.4, 3.2
XS = np.linspace(1.15, 3.9, 500)
YS = -(XS - P) * (XS - Q) * 1.25

ax1.plot(XS, YS, color=ACCENT, linewidth=2.2)
ax1.axhline(0, color=GREY, linewidth=1.1)

_m1 = (XS >= P) & (XS <= Q)
ax1.fill_between(XS[_m1], 0, YS[_m1], color=FILL)
_m2 = XS >= Q
ax1.fill_between(XS[_m2], 0, YS[_m2], color=SHADE)

ax1.set_xlim(0.95, 4.45)
ax1.set_ylim(-2.75, 2.4)
ax1.set_xticks([P, Q, 3.9])
ax1.set_xticklabels(["$a$", "$c$", "$b$"], fontsize=11)
ax1.set_yticks([])
for _s in ("top", "right", "left", "bottom"):
    ax1.spines[_s].set_visible(False)

for _x in (Q, 3.9):
    ax1.plot([_x, _x], [0, -(_x - P) * (_x - Q) * 1.25], color=GREY,
             linewidth=0.8, linestyle=(0, (2, 3)))

ax1.text(2.3, 0.42, "$A_{1}$", fontsize=13, color=ACCENT, ha="center")
ax1.text(3.62, -0.62, "$A_{2}$", fontsize=13, color=WARM, ha="center")

ax1.text(1.0, 2.15,
         "the integral from $a$ to $b$ gives $A_{1} - A_{2}$",
         fontsize=10.5, color=INK, ha="left", va="center")
ax1.text(1.0, 1.6,
         "the area is $A_{1} + A_{2}$, and both of these are positive",
         fontsize=10.5, color=WARM, ha="left", va="center")
ax1.text(1.0, -2.35,
         "$f(x) > 0$ from $a$ to $c$, and $f(x) < 0$ from $c$ to $b$",
         fontsize=10, color=INK, ha="left", va="center")

# ══════════════════════════════════════════════════════════
# (b) 2 曲線ではさまれた面積
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) Between two curves", fontsize=11, color=INK,
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
ax2.set_ylim(-1.75, 4.5)
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

ax2.text(-2.1, -0.95,
         "$f$ is the upper curve, $g$ is the lower curve on $a$ to $b$",
         fontsize=10, color=INK, ha="left", va="center")
ax2.text(-2.1, -1.5,
         "$a$ and $b$ come from solving $f(x) = g(x)$",
         fontsize=10, color=WARM, ha="left", va="center")

fig.tight_layout(w_pad=2.4, rect=(0, 0.16, 1, 1))
path = os.path.join(OUT, "aasl-5-11b-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
