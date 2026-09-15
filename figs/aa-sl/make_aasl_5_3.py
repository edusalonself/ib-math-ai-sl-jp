"""AA SL 5.3 の図をつくる。

    python3 figs/aa-sl/make_aasl_5_3.py
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_5_3.py

出力: aa-sl/05-calculus/img/aasl-5-3-idea.svg

(a) べき乗の微分の規則を、2 つの動きに分けて見せる。
(b) axⁿ の和の形に直してから微分する、という手順の流れ図。

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

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "05-calculus", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
FILL = "#e8f0f9"
SHADE = "#fdf0dc"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.8, 5.0))

# ══════════════════════════════════════════════════════════
# (a) べき乗の微分の 2 つの動き
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Two things happen to the power", fontsize=11, color=INK,
              loc="left", pad=12)
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis("off")

ax1.text(2.4, 7.6, r"$x^{n}$", fontsize=20, color=ACCENT, ha="center",
         va="center",
         bbox=dict(boxstyle="round,pad=0.5", facecolor=FILL,
                   edgecolor=ACCENT, linewidth=1.3))
ax1.text(7.6, 7.6, r"$n\,x^{\,n-1}$", fontsize=20, color=ACCENT, ha="center",
         va="center",
         bbox=dict(boxstyle="round,pad=0.5", facecolor=FILL,
                   edgecolor=ACCENT, linewidth=1.3))
ax1.annotate("", xy=(6.2, 7.6), xytext=(3.8, 7.6),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.6))
ax1.text(5.0, 8.5, "differentiate", fontsize=9.5, color=GREY, ha="center")

ax1.text(0.2, 5.4, "1. the old power comes down and multiplies",
         fontsize=10.5, color=WARM)
ax1.text(0.2, 4.3, "2. the power drops by one", fontsize=10.5, color=WARM)

ax1.text(0.2, 2.9, "a constant multiple just comes along:", fontsize=10,
         color=INK)
ax1.text(0.5, 1.9, r"$a\,x^{n} \ \longrightarrow \ a\,n\,x^{\,n-1}$",
         fontsize=13, color=ACCENT)
ax1.text(0.2, 0.7, "and a constant on its own differentiates to zero",
         fontsize=10, color=INK)

# ══════════════════════════════════════════════════════════
# (b) まず和の形に直す
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) Get it into a sum of powers first", fontsize=11, color=INK,
              loc="left", pad=12)
ax2.set_xlim(-0.3, 11.6)
ax2.set_ylim(0, 10)
ax2.axis("off")

BOX = dict(boxstyle="round,pad=0.40", facecolor=SHADE, edgecolor=WARM,
           linewidth=1.2)
OKBOX = dict(boxstyle="round,pad=0.45", facecolor=FILL, edgecolor=ACCENT,
             linewidth=1.3)

ROWS = ((9.05, "a product of brackets", "expand it"),
        (7.75, "a fraction over one term", "split it up"),
        (6.45, "a power under a fraction bar", "use a negative power"))
for _y, _what, _do in ROWS:
    ax2.text(0.15, _y, _what, fontsize=10.2, color=INK, ha="left",
             va="center", bbox=BOX)
    ax2.text(6.55, _y, r"$\longrightarrow$", fontsize=13, color=GREY,
             ha="center", va="center")
    ax2.text(7.35, _y, _do, fontsize=10.2, color=WARM, ha="left", va="center")

ax2.annotate("", xy=(5.0, 4.35), xytext=(5.0, 5.55),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.6))

ax2.text(5.0, 3.75, r"$a\,x^{n} + b\,x^{m} + \ldots$", fontsize=15,
         color=ACCENT, ha="center", va="center", bbox=OKBOX)
ax2.annotate("", xy=(5.0, 1.95), xytext=(5.0, 2.95),
             arrowprops=dict(arrowstyle="->", color=ACCENT, linewidth=1.6))
ax2.text(5.0, 1.40, "now differentiate one term at a time", fontsize=10.8,
         color=ACCENT, ha="center", va="center")
ax2.text(5.0, 0.45, "there is no rule yet for a product or a quotient",
         fontsize=9.5, color=GREY, ha="center", va="center")

fig.tight_layout(w_pad=2.4)
path = os.path.join(OUT, "aasl-5-3-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
