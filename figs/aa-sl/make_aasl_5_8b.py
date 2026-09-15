"""AA SL 5.8b の図をつくる。

    python3 figs/aa-sl/make_aasl_5_8b.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_8b.py

出力: aa-sl/05-calculus/img/aasl-5-8b-idea.svg

(a) 最適化の手順（6 歩）。
(b) 正方形の板から作る、ふたのない箱（文字は a と x だけ。数値は入れません）。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * \\le \\ge は読めない → \\leq \\geq を使う
  * \\bigl \\bigr \\Box は読めない → ふつうの ( ) と文字を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ PNG は目視用です。確認が終わったら消してください。
"""
import os

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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.4, 5.6))

# ══════════════════════════════════════════════════════════
# (a) 手順
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) The six steps", fontsize=11, color=INK, loc="left", pad=12)
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis("off")

BOX = dict(boxstyle="round,pad=0.34", facecolor=FILL, edgecolor=ACCENT,
           linewidth=1.1)
STEPS = ("draw a picture and name the variables",
         "write down the quantity to be optimised",
         "use the constraint to leave one variable",
         "state the domain",
         "solve $f'(x) = 0$, then justify max or min",
         "answer in context, with units")
YS = (9.0, 7.5, 6.0, 4.5, 3.0, 1.5)
for _i, (_y, _t) in enumerate(zip(YS, STEPS), 1):
    ax1.text(0.55, _y, "$%d$" % _i, fontsize=11, color=WARM, ha="center",
             va="center")
    ax1.text(5.35, _y, _t, fontsize=10, color=ACCENT, ha="center",
             va="center", bbox=BOX)
    if _i < len(STEPS):
        ax1.annotate("", xy=(5.35, _y - 1.12), xytext=(5.35, _y - 0.42),
                     arrowprops=dict(arrowstyle="->", color=GREY,
                                     linewidth=1.1))

ax1.text(0.15, 0.35, "steps $4$ and $5$ are the ones most often left out",
         fontsize=9.5, color=WARM, va="center")

# ══════════════════════════════════════════════════════════
# (b) ふたのない箱
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) An open box made from a square sheet", fontsize=11,
              color=INK, loc="left", pad=12)
ax2.set_xlim(-1.3, 11.3)
ax2.set_ylim(-2.6, 10.0)
ax2.axis("off")
ax2.set_aspect("equal", adjustable="box")

S = 8.0     # 板の 1 辺
C = 1.7     # 切り取る正方形の 1 辺
X0, Y0 = 0.0, 0.6

ax2.add_patch(Rectangle((X0, Y0), S, S, facecolor="none", edgecolor=INK,
                        linewidth=1.6))
for _cx, _cy in ((X0, Y0), (X0 + S - C, Y0), (X0, Y0 + S - C),
                 (X0 + S - C, Y0 + S - C)):
    ax2.add_patch(Rectangle((_cx, _cy), C, C, facecolor=SHADE,
                            edgecolor=WARM, linewidth=1.3))

# 折り目
for _v in (X0 + C, X0 + S - C):
    ax2.plot([_v, _v], [Y0 + C, Y0 + S - C], color=GREY, linewidth=0.9,
             linestyle=(0, (4, 3)))
    ax2.plot([X0 + C, X0 + S - C], [Y0 + _v - X0, Y0 + _v - X0], color=GREY,
             linewidth=0.9, linestyle=(0, (4, 3)))

# 寸法
ax2.annotate("", xy=(X0, Y0 - 0.55), xytext=(X0 + C, Y0 - 0.55),
             arrowprops=dict(arrowstyle="<->", color=WARM, linewidth=1.1))
ax2.text(X0 + C / 2, Y0 - 1.15, "$x$", fontsize=12, color=WARM, ha="center",
         va="center")
ax2.annotate("", xy=(X0 + C, Y0 - 0.55), xytext=(X0 + S - C, Y0 - 0.55),
             arrowprops=dict(arrowstyle="<->", color=ACCENT, linewidth=1.1))
ax2.text(X0 + S / 2, Y0 - 1.15, "$a - 2x$", fontsize=12, color=ACCENT,
         ha="center", va="center")
ax2.annotate("", xy=(X0 - 0.55, Y0), xytext=(X0 - 0.55, Y0 + S),
             arrowprops=dict(arrowstyle="<->", color=INK, linewidth=1.1))
ax2.text(X0 - 1.05, Y0 + S / 2, "$a$", fontsize=12, color=INK, ha="center",
         va="center")

ax2.text(X0 + S + 0.55, Y0 + S - C / 2, "cut off", fontsize=9.5, color=WARM,
         ha="left", va="center")
ax2.text(X0 + S + 0.55, Y0 + S / 2, "fold up", fontsize=9.5, color=GREY,
         ha="left", va="center")

ax2.text(-1.2, -1.95, "base $(a - 2x)$ by $(a - 2x)$, height $x$",
         fontsize=10, color=INK, ha="left", va="center")
ax2.text(-1.2, -2.55, "the base disappears when $2x$ reaches $a$",
         fontsize=9.5, color=WARM, ha="left", va="center")

fig.tight_layout(w_pad=2.2)
path = os.path.join(OUT, "aasl-5-8b-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
