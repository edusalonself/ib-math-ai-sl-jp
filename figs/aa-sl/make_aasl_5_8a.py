"""AA SL 5.8a の図をつくる。

    python3 figs/aa-sl/make_aasl_5_8a.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_8a.py

出力: aa-sl/05-calculus/img/aasl-5-8a-idea.svg

(a) 極大・極小・変曲点と、concave-up / concave-down の範囲。
(b) 判定のしかたのまとめ。

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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.4, 5.4))

# ══════════════════════════════════════════════════════════
# (a) 極大・極小・変曲点
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Maximum, minimum and point of inflexion", fontsize=11,
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
# (b) 判定のしかた
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) How to decide", fontsize=11, color=INK, loc="left", pad=12)
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis("off")

BOXL = dict(boxstyle="round,pad=0.32", facecolor=SHADE, edgecolor=WARM,
            linewidth=1.1)
BOXR = dict(boxstyle="round,pad=0.32", facecolor=FILL, edgecolor=ACCENT,
            linewidth=1.1)

ROWS = (("$f'(a) = 0$ and $f''(a) < 0$", "local maximum at $x = a$"),
        ("$f'(a) = 0$ and $f''(a) > 0$", "local minimum at $x = a$"),
        ("$f'(a) = 0$ and $f''(a) = 0$", "no conclusion yet"),
        ("$f''(a) = 0$ and $f''$ changes sign", "point of inflexion at $x = a$"))
YS = (8.6, 7.0, 5.4, 3.8)
for _y, (_l, _r) in zip(YS, ROWS):
    ax2.text(2.55, _y, _l, fontsize=10.5 if len(_l) < 32 else 9.2,
             color=WARM, ha="center", va="center", bbox=BOXL)
    ax2.annotate("", xy=(5.45, _y), xytext=(4.85, _y),
                 arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.2))
    ax2.text(7.7, _y, _r, fontsize=10, color=ACCENT, ha="center",
             va="center", bbox=BOXR)

ax2.plot([0.2, 9.8], [2.7, 2.7], color=GREY, linewidth=0.9)
ax2.text(0.25, 1.95, "if the second derivative gives no conclusion,",
         fontsize=10, color=INK, va="center")
ax2.text(0.25, 1.20, "look at the sign of $f'$ on each side instead",
         fontsize=10, color=INK, va="center")
ax2.text(0.25, 0.40, "$f''(a) = 0$ on its own is never enough",
         fontsize=9.5, color=WARM, va="center")

fig.tight_layout(w_pad=2.2)
path = os.path.join(OUT, "aasl-5-8a-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
