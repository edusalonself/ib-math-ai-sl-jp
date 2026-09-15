"""AA SL 5.11a の図をつくる。

    python3 figs/aa-sl/make_aasl_5_11a.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_11a.py

出力: aa-sl/05-calculus/img/aasl-5-11a-idea.svg

(a) 原始関数を 2 本（F と F + C）かき、a から b までの縦の差が同じであること。
    だから定積分に +C は要らない。
(b) 定積分の性質。区間を分ける、上下を入れかえると符号が変わる、同じなら 0。

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
# (a) F と F + C の縦の差は同じ
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Why $+C$ cancels", fontsize=11, color=INK,
              loc="left", pad=12)

A, B = 1.2, 3.6
XS = np.linspace(0.3, 3.9, 400)


def _F(t):
    return 0.14 * t ** 3 - 0.7 * t ** 2 + 1.6 * t + 0.6


F = _F(XS)
SHIFT = 1.1

ax1.plot(XS, F, color=ACCENT, linewidth=2.2)
ax1.plot(XS, F + SHIFT, color=GREY, linewidth=1.8, linestyle=(0, (5, 4)))

FA, FB = _F(A), _F(B)

for _x, _y in ((A, FA), (B, FB)):
    ax1.plot([_x, _x], [0, _y + SHIFT], color=GREY, linewidth=0.8,
             linestyle=(0, (2, 3)))
    ax1.plot([_x], [_y], marker="o", markersize=5, color=ACCENT)
    ax1.plot([_x], [_y + SHIFT], marker="o", markersize=5, color=GREY)

# 縦の差を 2 本（曲線の右がわに出す）
G1, G2 = 4.15, 4.8
ax1.annotate("", xy=(G1, FB), xytext=(G1, FA),
             arrowprops=dict(arrowstyle="<->", color=WARM, linewidth=1.4))
ax1.annotate("", xy=(G2, FB + SHIFT), xytext=(G2, FA + SHIFT),
             arrowprops=dict(arrowstyle="<->", color=WARM, linewidth=1.4))
for _y, _x0 in ((FA, B), (FB, B), (FA + SHIFT, G2 - 0.35),
                (FB + SHIFT, G2 - 0.35)):
    ax1.plot([_x0, G2 + 0.2], [_y, _y], color=WARM, linewidth=0.7)

ax1.axhline(0, color=GREY, linewidth=1.0)
ax1.set_xlim(0.1, 5.55)
ax1.set_ylim(-0.5, 7.0)
ax1.set_xticks([A, B])
ax1.set_xticklabels(["$a$", "$b$"], fontsize=11)
ax1.set_yticks([])
for _s in ("top", "right", "left", "bottom"):
    ax1.spines[_s].set_visible(False)

ax1.text(0.45, 0.55, "$y = F(x)$", fontsize=11, color=ACCENT,
         ha="left")
ax1.text(0.45, 3.8, "$y = F(x) + C$", fontsize=11, color=GREY,
         ha="left")
ax1.text(0.25, 6.6, "both vertical gaps are $F(b) - F(a)$",
         fontsize=11, color=WARM, ha="left")
ax1.text(0.25, 5.85, "shifting the curve up by $C$\ndoes not change the gap",
         fontsize=10, color=INK, ha="left", va="top")

# ══════════════════════════════════════════════════════════
# (b) 定積分の性質
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) Three properties of the limits", fontsize=11, color=INK,
              loc="left", pad=12)
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis("off")

# split
ax2.plot([0.7, 9.0], [8.3, 8.3], color=INK, linewidth=1.4)
for _x, _lab in ((0.7, "$a$"), (4.4, "$c$"), (9.0, "$b$")):
    ax2.plot([_x], [8.3], marker="|", markersize=13, color=INK,
             markeredgewidth=1.6)
    ax2.text(_x, 7.75, _lab, fontsize=11.5, color=INK, ha="center")
ax2.text(2.55, 8.75, "$a$ to $c$", fontsize=10.5, color=ACCENT, ha="center")
ax2.text(6.7, 8.75, "$c$ to $b$", fontsize=10.5, color=ACCENT, ha="center")
ax2.text(0.7, 6.7,
         "splitting: $\\int_{a}^{b} = \\int_{a}^{c} + \\int_{c}^{b}$",
         fontsize=12.5, color=ACCENT, ha="left", va="center",
         bbox=dict(boxstyle="round,pad=0.35", facecolor=FILL,
                   edgecolor=ACCENT, linewidth=1.2))

ax2.text(0.7, 4.6,
         "swapping: $\\int_{b}^{a} = -\\int_{a}^{b}$",
         fontsize=12.5, color=ACCENT, ha="left", va="center",
         bbox=dict(boxstyle="round,pad=0.35", facecolor=FILL,
                   edgecolor=ACCENT, linewidth=1.2))

ax2.text(0.7, 2.5,
         "equal limits: $\\int_{a}^{a} = 0$",
         fontsize=12.5, color=ACCENT, ha="left", va="center",
         bbox=dict(boxstyle="round,pad=0.35", facecolor=FILL,
                   edgecolor=ACCENT, linewidth=1.2))

ax2.plot([0.2, 9.8], [1.25, 1.25], color=GREY, linewidth=0.9)
ax2.text(0.25, 0.55, "the value of a definite integral can be negative",
         fontsize=10.5, color=WARM, va="center")

fig.tight_layout(w_pad=2.4, rect=(0, 0.16, 1, 1))
path = os.path.join(OUT, "aasl-5-11a-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
