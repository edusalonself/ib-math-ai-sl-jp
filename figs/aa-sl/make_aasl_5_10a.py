"""AA SL 5.10a の図をつくる。

    python3 figs/aa-sl/make_aasl_5_10a.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_10a.py

出力: aa-sl/05-calculus/img/aasl-5-10a-idea.svg

(a) y = ln|x| の 2 本の枝。どちらの枝でも接線の傾きが 1/x なので、
    1/x の原始関数には絶対値が要る。
(b) ax + b との合成。微分すると a がかかるので、積分では 1/a で割る。

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
FILL = "#e8f0f9"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.4, 5.2))

# ══════════════════════════════════════════════════════════
# (a) y = ln|x| の 2 本の枝
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Why the integral of $1/x$ needs $|x|$", fontsize=11,
              color=INK, loc="left", pad=12)

XR = np.linspace(0.095, 3.4, 400)
XL = -XR[::-1]
ax1.plot(XR, np.log(np.abs(XR)), color=ACCENT, linewidth=2.2)
ax1.plot(XL, np.log(np.abs(XL)), color=ACCENT, linewidth=2.2)

ax1.axhline(0, color=GREY, linewidth=1.0)
ax1.plot([0, 0], [-3.0, 2.45], color=GREY, linewidth=1.0,
         linestyle=(0, (4, 4)))
ax1.set_xlim(-3.7, 3.7)
ax1.set_ylim(-3.85, 2.6)
ax1.set_xticks([])
ax1.set_yticks([])
for _s in ("top", "right", "left", "bottom"):
    ax1.spines[_s].set_visible(False)

# 接線を 2 本（左の枝と右の枝で、同じ |x|）
for _a in (2.0, -2.0):
    _y = np.log(abs(_a))
    _m = 1.0 / _a
    _t = np.linspace(_a - 0.95, _a + 0.95, 2)
    ax1.plot(_t, _y + _m * (_t - _a), color=WARM, linewidth=1.5)
    ax1.plot([_a], [_y], marker="o", markersize=4.5, color=WARM)

ax1.text(2.1, 1.62, "gradient $= 1/x > 0$", fontsize=10, color=WARM,
         ha="center")
ax1.text(-2.1, -1.15, "gradient $= 1/x < 0$", fontsize=10, color=WARM,
         ha="center")
ax1.text(3.6, 0.55, "$y = \\ln|x|$", fontsize=12, color=ACCENT, ha="right")
ax1.text(-3.55, 2.15, "$x < 0$", fontsize=10.5, color=GREY, ha="left")
ax1.text(3.55, 2.15, "$x > 0$", fontsize=10.5, color=GREY, ha="right")
ax1.text(0.0, -3.5, "$1/x$ is defined on both sides of $0$,\n"
                     "and $\\ln|x|$ has gradient $1/x$ on both sides",
         fontsize=10, color=INK, ha="center", va="center")

# ══════════════════════════════════════════════════════════
# (b) ax + b との合成
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) Integrating $f'(ax + b)$", fontsize=11, color=INK,
              loc="left", pad=12)
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis("off")

BOX = dict(boxstyle="round,pad=0.42", facecolor=FILL, edgecolor=ACCENT,
           linewidth=1.3)
ax2.text(2.3, 7.6, "$f(ax + b)$", fontsize=14, color=ACCENT, ha="center",
         va="center", bbox=BOX)
ax2.text(7.7, 7.6, "$a\\,f'(ax + b)$", fontsize=14, color=ACCENT,
         ha="center", va="center", bbox=BOX)

ax2.annotate("", xy=(6.05, 8.15), xytext=(3.95, 8.15),
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=1.4,
                             connectionstyle="arc3,rad=-0.28"))
ax2.annotate("", xy=(3.95, 7.05), xytext=(6.05, 7.05),
             arrowprops=dict(arrowstyle="->", color=INK, linewidth=1.4,
                             connectionstyle="arc3,rad=-0.28"))
ax2.text(5.0, 9.25, "differentiate: the chain rule\nmultiplies by $a$",
         fontsize=10, color=WARM, ha="center", va="center")
ax2.text(5.0, 5.85, "integrate: so divide by $a$",
         fontsize=10, color=INK, ha="center", va="center")

ax2.plot([0.2, 9.8], [4.75, 4.75], color=GREY, linewidth=0.9)
ax2.text(0.25, 3.95,
         "$\\int f'(ax + b)\\,dx = \\dfrac{1}{a}\\,f(ax + b) + C$",
         fontsize=13, color=ACCENT, va="center")
ax2.text(0.25, 2.55, "$a$ and $b$ are constants and $a \\neq 0$",
         fontsize=10.5, color=INK, va="center")
ax2.text(0.25, 1.75, "the inside must be linear: $ax + b$, nothing else",
         fontsize=10.5, color=WARM, va="center")
ax2.text(0.25, 0.95, "not printed in the formula booklet",
         fontsize=9.5, color=GREY, va="center")

fig.tight_layout(w_pad=2.4, rect=(0, 0.16, 1, 1))
path = os.path.join(OUT, "aasl-5-10a-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
