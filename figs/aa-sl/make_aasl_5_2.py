"""AA SL 5.2 の図をつくる。

    python3 figs/aa-sl/make_aasl_5_2.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_2.py  … 目視用の PNG も

出力: aa-sl/05-calculus/img/aasl-5-2-idea.svg

(a) 上段: y = f(x)。上がるところ・水平なところ・下がるところ。
(b) 下段: y = f'(x) を x をそろえて置く。
    f' が x 軸より上 ⇔ f は上がる、下 ⇔ f は下がる、
    x 軸に触れるだけ（符号が変わらない）⇔ f は水平になるが向きは変わらない。

★ 数値は入れません。文字だけです（例題・演習と重ならないように）。

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
UP = "#d8e6f4"
DOWN = "#f6ddc4"

# f'(x) = -(x+2)(x-1)^2 * k をやめ、符号が変わる点と触れるだけの点を
# 1 つずつ持つ形にする: f'(x) = (x + 2)(x - 1)^2 / 6
A, B = -2.0, 1.0


def fp(t):
    return ((t + 2.0) * (t - 1.0) ** 2) / 6.0


def f(t):
    """fp の原始関数（手で積分した多項式）。
    fp = (x+2)(x-1)^2/6 = (x^3 - 3x + 2)/6  なので
    f  = (x^4/4 - 3x^2/2 + 2x)/6 + c
    """
    return (t ** 4 / 4.0 - 1.5 * t ** 2 + 2.0 * t) / 6.0 + 1.6


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10.6, 6.6),
                               gridspec_kw={"height_ratios": [1.35, 1.0]},
                               sharex=True)

T = np.linspace(-3.1, 2.6, 500)

# ══════════════════════════════════════════════════════════
# (a) y = f(x)
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) The graph of $y = f(x)$", fontsize=11, color=INK,
              loc="left", pad=10)
ax1.plot(T, f(T), color=ACCENT, linewidth=2.0)
ax1.set_xlim(-3.35, 3.15)
ax1.set_ylim(-0.55, 3.9)
ax1.axis("off")
ax1.plot([-3.2, 3.0], [0, 0], color=GREY, linewidth=1.0)

ax1.axvspan(-3.1, A, color=DOWN, alpha=0.55, zorder=0)
ax1.axvspan(A, 2.6, color=UP, alpha=0.55, zorder=0)

for _x, _lab in ((A, "$p$"), (B, "$q$")):
    ax1.plot([_x, _x], [0, f(_x)], color=GREY, linewidth=0.9,
             linestyle=(0, (3, 3)))
    ax1.plot([_x], [f(_x)], "o", color=WARM, markersize=6)
    _t = np.array([_x - 0.75, _x + 0.75])
    ax1.plot(_t, [f(_x)] * 2, color=WARM, linewidth=1.6)

ax1.text(A, -0.12, "$p$", fontsize=11, color=INK, ha="center", va="top")
ax1.text(B, -0.12, "$q$", fontsize=11, color=INK, ha="center", va="top")
ax1.text(-2.62, 3.25, "falling", fontsize=10, color=INK, ha="center")
ax1.text(0.55, 3.25, "rising", fontsize=10, color=INK, ha="center")
ax1.text(2.05, 3.25, "still rising", fontsize=10, color=INK, ha="center")
ax1.text(A, 1.18, "turns here", fontsize=9.5, color=WARM, ha="center")
ax1.text(B + 0.05, 0.42, "flat, but does not turn", fontsize=9.5, color=WARM,
         ha="left")

# ══════════════════════════════════════════════════════════
# (b) y = f'(x)
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) The graph of $y = f'(x)$, drawn under the same $x$-axis",
              fontsize=11, color=INK, loc="left", pad=10)
ax2.plot(T, fp(T), color=ACCENT, linewidth=2.0)
ax2.set_xlim(-3.35, 3.15)
ax2.set_ylim(-2.05, 1.85)
ax2.axis("off")
ax2.plot([-3.2, 3.0], [0, 0], color=GREY, linewidth=1.0)
ax2.text(3.05, 0.0, "$x$", fontsize=10, color=GREY, va="center")

ax2.fill_between(T, 0, fp(T), where=(fp(T) > 0), color=UP, alpha=0.9)
ax2.fill_between(T, 0, fp(T), where=(fp(T) < 0), color=DOWN, alpha=0.9)

for _x in (A, B):
    ax2.plot([_x, _x], [-1.15, 0], color=GREY, linewidth=0.9,
             linestyle=(0, (3, 3)))
    ax2.plot([_x], [0], "o", color=WARM, markersize=6)

ax2.text(A, -1.22, "$p$", fontsize=11, color=INK, ha="center", va="top")
ax2.text(B, -1.22, "$q$", fontsize=11, color=INK, ha="center", va="top")
ax2.text(-2.72, -0.62, "$f'(x) < 0$", fontsize=10.5, color=WARM, ha="center")
ax2.text(-0.55, 0.72, "$f'(x) > 0$", fontsize=10.5, color=ACCENT, ha="center")
ax2.text(2.28, 0.28, "$f'(x) > 0$", fontsize=10.5, color=ACCENT, ha="center")
ax2.annotate("", xy=(A - 0.06, -0.10), xytext=(-1.30, -1.42),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.text(-1.25, -1.52, "crosses the axis: sign changes", fontsize=9,
         color=GREY, ha="left", va="top")
ax2.annotate("", xy=(B + 0.06, -0.10), xytext=(1.55, -1.42),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.text(1.60, -1.52, "touches the axis:\nsign does not change", fontsize=9,
         color=GREY, ha="left", va="top", linespacing=1.5)

fig.tight_layout(h_pad=1.6)
path = os.path.join(OUT, "aasl-5-2-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))
print("  f'(p) =", round(fp(A), 6), "  f'(q) =", round(fp(B), 6))
print("  f'(-3) =", round(fp(-3.0), 6), "  f'(0) =", round(fp(0.0), 6),
      "  f'(2) =", round(fp(2.0), 6))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
