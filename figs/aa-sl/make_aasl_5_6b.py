"""AA SL 5.6b の図をつくる。

    python3 figs/aa-sl/make_aasl_5_6b.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_6b.py

出力: aa-sl/05-calculus/img/aasl-5-6b-idea.svg

(a) 積の微分法を「片方ずつ微分して足す」として見る。
(b) 商の微分法の形（分子の順番・マイナス・分母の 2 乗）。

★ 数値の答えは入れません（例題・演習と重ならないように）。

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

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "05-calculus", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
FILL = "#e8f0f9"
SHADE = "#fdf0dc"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 5.2))

# ══════════════════════════════════════════════════════════
# (a) 積の微分法
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) The product rule: one factor at a time", fontsize=11,
              color=INK, loc="left", pad=12)
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis("off")

BOXU = dict(boxstyle="round,pad=0.40", facecolor=SHADE, edgecolor=WARM,
            linewidth=1.3)
BOXV = dict(boxstyle="round,pad=0.40", facecolor=FILL, edgecolor=ACCENT,
            linewidth=1.3)

ax1.text(1.15, 8.9, "$y =$", fontsize=13, color=INK, ha="center", va="center")
ax1.text(2.75, 8.9, "$u$", fontsize=13.5, color=WARM, ha="center",
         va="center", bbox=BOXU)
ax1.text(4.35, 8.9, r"$\times$", fontsize=13, color=INK, ha="center",
         va="center")
ax1.text(5.75, 8.9, "$v$", fontsize=13.5, color=ACCENT, ha="center",
         va="center", bbox=BOXV)

ax1.plot([0.2, 9.8], [7.9, 7.9], color=GREY, linewidth=0.9)

ax1.text(0.35, 6.75, "keep $u$, differentiate $v$", fontsize=10.5,
         color=GREY, va="center")
ax1.text(6.85, 6.75, r"$u\,\frac{dv}{dx}$", fontsize=15, color=WARM,
         ha="center", va="center")

ax1.text(0.35, 4.85, "keep $v$, differentiate $u$", fontsize=10.5,
         color=GREY, va="center")
ax1.text(6.85, 4.85, r"$v\,\frac{du}{dx}$", fontsize=15, color=ACCENT,
         ha="center", va="center")

ax1.text(0.35, 3.30, "then add the two:", fontsize=10.5, color=INK,
         va="center")
ax1.text(0.55, 1.75, r"$\frac{dy}{dx} = u\,\frac{dv}{dx} + v\,\frac{du}{dx}$",
         fontsize=16, color=INK, va="center")
ax1.text(0.35, 0.35, "the order of the two terms does not matter here",
         fontsize=9.5, color=GREY, va="center")

# ══════════════════════════════════════════════════════════
# (b) 商の微分法
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) The quotient rule: the order does matter", fontsize=11,
              color=INK, loc="left", pad=12)
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis("off")

ax2.text(1.15, 8.9, "$y =$", fontsize=13, color=INK, ha="center", va="center")
ax2.text(2.85, 8.9, r"$\frac{u}{v}$", fontsize=16, color=INK, ha="center",
         va="center")
ax2.text(4.35, 9.25, "$u$ is the top", fontsize=10, color=WARM, ha="left",
         va="center")
ax2.text(4.35, 8.45, "$v$ is the bottom", fontsize=10, color=ACCENT,
         ha="left", va="center")

ax2.plot([0.2, 9.8], [7.5, 7.5], color=GREY, linewidth=0.9)

ax2.text(0.35, 5.25,
         r"$\frac{dy}{dx} = \frac{v\,\frac{du}{dx} - u\,\frac{dv}{dx}}{v^{2}}$",
         fontsize=19, color=INK, va="center")

ax2.annotate("", xy=(1.88, 5.98), xytext=(5.50, 7.00),
             arrowprops=dict(arrowstyle="->", color=ACCENT, linewidth=1.2))
ax2.text(5.65, 7.00, "this term comes first", fontsize=9.5, color=ACCENT,
         ha="left", va="center")

ax2.annotate("", xy=(2.36, 5.32), xytext=(5.50, 4.55),
             arrowprops=dict(arrowstyle="->", color=INK, linewidth=1.2,
                             shrinkB=9))
ax2.text(5.65, 4.55, "minus, not plus", fontsize=9.5, color=INK,
         ha="left", va="center")

ax2.annotate("", xy=(2.30, 4.72), xytext=(5.50, 2.95),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.2,
                             shrinkB=9))
ax2.text(5.65, 2.95, "the bottom, squared", fontsize=9.5, color=GREY,
         ha="left", va="center")

ax2.plot([0.2, 9.8], [1.35, 1.35], color=GREY, linewidth=0.9)
ax2.text(0.35, 0.60, "swapping the two terms on top changes every sign",
         fontsize=9.5, color=INK, va="center")

fig.tight_layout(w_pad=2.4)
path = os.path.join(OUT, "aasl-5-6b-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
