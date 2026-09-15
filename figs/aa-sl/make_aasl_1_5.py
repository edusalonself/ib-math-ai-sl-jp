"""AA SL 1.5 の図をつくる。

    python3 figs/aa-sl/make_aasl_1_5.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_1_5.py  … 目視用の PNG も

出力: aa-sl/01-number-and-algebra/img/aasl-1-5-idea.svg

(a) 2 の累乗のはしご。1 段下りるたびに 2 で割る。
    だから 2^0 = 1、2^(-1) = 1/2、2^(-2) = 1/4 と決まってしまう。
(b) 同じ 1 つの事実を、累乗の形と対数の形で書き分ける。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に演習の答えを書かないこと。
★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "01-number-and-algebra", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(9.6, 4.3), gridspec_kw={"width_ratios": [1.0, 1.15]}
)

# ══════════════════════════════════════════════════════════
# (a) 2 の累乗のはしご
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Each step down divides by $2$",
              fontsize=11, color=INK, loc="left", pad=10)
ax1.set_xlim(0.0, 1.0)
ax1.set_ylim(-0.6, 5.6)
ax1.axis("off")

RUNGS = [(5, "$2^{3}$", "$8$"),
         (4, "$2^{2}$", "$4$"),
         (3, "$2^{1}$", "$2$"),
         (2, "$2^{0}$", "$1$"),
         (1, "$2^{-1}$", r"$\frac{1}{2}$"),
         (0, "$2^{-2}$", r"$\frac{1}{4}$")]

for y, power, value in RUNGS:
    col = ACCENT if y <= 2 else INK
    ax1.text(0.30, y, power, ha="right", va="center", fontsize=13, color=col)
    ax1.text(0.40, y, "$=$", ha="center", va="center", fontsize=12, color=GREY)
    ax1.text(0.50, y, value, ha="left", va="center", fontsize=13, color=col)

for y, _, _ in RUNGS[:-1]:
    ax1.annotate("", xy=(0.78, y - 1 + 0.14), xytext=(0.78, y - 0.14),
                 arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
    ax1.text(0.82, y - 0.5, r"$\div 2$", ha="left", va="center",
             fontsize=9.5, color=GREY)

ax1.plot([0.16, 0.16], [-0.35, 2.5], color=WARM, linewidth=1.6)
ax1.text(0.12, 1.0, "forced,\nnot chosen", ha="right", va="center",
         fontsize=9.5, color=WARM)

# ══════════════════════════════════════════════════════════
# (b) 1 つの事実を、2 通りに書く
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) One fact, written two ways",
              fontsize=11, color=INK, loc="left", pad=10)
ax2.set_xlim(0.0, 1.0)
ax2.set_ylim(0.0, 1.0)
ax2.axis("off")

ax2.text(0.50, 0.80, "$2^{3} = 8$", ha="center", va="center",
         fontsize=20, color=INK)
ax2.text(0.50, 0.30, r"$\log_{2} 8 = 3$", ha="center", va="center",
         fontsize=20, color=INK)
ax2.annotate("", xy=(0.50, 0.40), xytext=(0.50, 0.70),
             arrowprops=dict(arrowstyle="<->", color=ACCENT, linewidth=1.6))
ax2.text(0.535, 0.55, "same statement", ha="left", va="center",
         fontsize=10, color=ACCENT)

ax2.annotate("base", xy=(0.415, 0.755), xytext=(0.20, 0.60),
             fontsize=9.5, color=WARM, ha="center",
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=1.0))
ax2.annotate("exponent", xy=(0.455, 0.865), xytext=(0.24, 0.965),
             fontsize=9.5, color=WARM, ha="center",
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=1.0))
ax2.annotate("value", xy=(0.575, 0.80), xytext=(0.80, 0.955),
             fontsize=9.5, color=WARM, ha="center",
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=1.0))

ax2.text(0.50, 0.10,
         "a logarithm is the exponent you are looking for",
         ha="center", va="center", fontsize=10, color=INK)

fig.tight_layout(w_pad=2.2)
path = os.path.join(OUT, "aasl-1-5-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
