"""AA SL 1.7b の図をつくる。

    python3 figs/aa-sl/make_aasl_1_7b.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_1_7b.py  … 目視用の PNG も

出力: aa-sl/01-number-and-algebra/img/aasl-1-7b-idea.svg

(a) 値の世界の掛け算が、指数の世界の足し算になる（底 2）。
    8 x 4 = 32 の下に 3 + 2 = 5 が並ぶ。
(b) 底の変換。25 も 125 も 5 の累乗なので、b = 5 を選ぶと上下が整数になる。

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
    1, 2, figsize=(10.0, 4.0), gridspec_kw={"width_ratios": [1.2, 1.0]}
)

# ══════════════════════════════════════════════════════════
# (a) 掛け算 → 足し算
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Multiplying below, adding above (base $2$)",
              fontsize=11, color=INK, loc="left", pad=10)
ax1.set_xlim(0.0, 1.0)
ax1.set_ylim(0.0, 1.0)
ax1.axis("off")

COLS = [(0.14, "$8$", "$3$"), (0.50, "$4$", "$2$"), (0.86, "$32$", "$5$")]

ax1.text(0.32, 0.24, r"$\times$", ha="center", va="center",
         fontsize=15, color=GREY)
ax1.text(0.68, 0.24, "$=$", ha="center", va="center",
         fontsize=15, color=GREY)
ax1.text(0.32, 0.76, "$+$", ha="center", va="center",
         fontsize=15, color=GREY)
ax1.text(0.68, 0.76, "$=$", ha="center", va="center",
         fontsize=15, color=GREY)

for cx, val, expo in COLS:
    ax1.text(cx, 0.24, val, ha="center", va="center", fontsize=16, color=INK)
    ax1.text(cx, 0.76, expo, ha="center", va="center", fontsize=16,
             color=ACCENT)
    ax1.annotate("", xy=(cx, 0.66), xytext=(cx, 0.36),
                 arrowprops=dict(arrowstyle="->", color=ACCENT, linewidth=1.2))

ax1.text(0.02, 0.24, "values", ha="left", va="center", fontsize=9.5,
         color=GREY, rotation=90)
ax1.text(0.02, 0.76, "$\\log_{2}$", ha="left", va="center", fontsize=9.5,
         color=ACCENT, rotation=90)
ax1.text(0.50, 0.03, "a product becomes a sum",
         ha="center", va="center", fontsize=10, color=INK)

# ══════════════════════════════════════════════════════════
# (b) 底の変換
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) Change of base: pick $b$ you can do by hand",
              fontsize=11, color=INK, loc="left", pad=10)
ax2.set_xlim(0.0, 1.0)
ax2.set_ylim(0.0, 1.0)
ax2.axis("off")

ax2.text(0.50, 0.82, r"$\log_{25} 125$", ha="center", va="center",
         fontsize=17, color=INK)
ax2.annotate("", xy=(0.50, 0.60), xytext=(0.50, 0.72),
             arrowprops=dict(arrowstyle="->", color=ACCENT, linewidth=1.5))
ax2.text(0.53, 0.66, "take $b = 5$", ha="left", va="center",
         fontsize=9.5, color=ACCENT)

ax2.text(0.50, 0.44, r"$\dfrac{\log_{5} 125}{\log_{5} 25}$",
         ha="center", va="center", fontsize=17, color=INK)
ax2.text(0.78, 0.50, r"$125 = 5^{3}$", ha="left", va="center",
         fontsize=10, color=WARM)
ax2.text(0.78, 0.38, r"$25 = 5^{2}$", ha="left", va="center",
         fontsize=10, color=WARM)

ax2.annotate("", xy=(0.50, 0.19), xytext=(0.50, 0.29),
             arrowprops=dict(arrowstyle="->", color=ACCENT, linewidth=1.5))
ax2.text(0.50, 0.10, r"$\dfrac{3}{2}$", ha="center", va="center",
         fontsize=17, color=ACCENT)

fig.tight_layout(w_pad=2.4)
path = os.path.join(OUT, "aasl-1-7b-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
