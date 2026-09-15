"""AA SL 1.4 の図をつくる。

    python3 figs/aa-sl/make_aasl_1_4.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_1_4.py  … 目視用の PNG も

出力: aa-sl/01-number-and-algebra/img/aasl-1-4-idea.svg

(a) 単利はまっすぐ、複利は上に曲がる（$1000、年 10%）。
(b) k を大きくすると、1 回あたりの利率は小さく、回数は多くなる。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \begin{pmatrix} は読めない → \binom を使う
  * \lvert \rvert は読めない → | を使う
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
    1, 2, figsize=(9.4, 4.0), gridspec_kw={"width_ratios": [1.15, 1.0]}
)

# ══════════════════════════════════════════════════════════
# (a) 単利と複利（$1000、年 10%、10 年）
# ══════════════════════════════════════════════════════════
YEARS = list(range(0, 11))
SIMPLE = [1000 + 100 * n for n in YEARS]
COMP = [1000 * 1.1 ** n for n in YEARS]

ax1.set_title("(a) $\\$1000$ at $10\\%$ per year",
              fontsize=11, color=INK, loc="left", pad=8)
ax1.plot(YEARS, SIMPLE, marker="o", markersize=4, color=GREY, linewidth=1.6,
         label="simple interest")
ax1.plot(YEARS, COMP, marker="o", markersize=4, color=ACCENT, linewidth=1.8,
         label="compound interest")
ax1.set_xlabel("years", fontsize=10, color=INK)
ax1.set_ylabel("value (\\$)", fontsize=10, color=INK)
ax1.set_xticks(range(0, 11, 2))
ax1.set_yticks([1000, 1500, 2000, 2500])
ax1.tick_params(labelsize=9, colors=INK)
for side in ("top", "right"):
    ax1.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax1.spines[side].set_color(INK)
ax1.grid(axis="y", color="#e5e7eb", linewidth=0.8)
ax1.set_axisbelow(True)
ax1.legend(fontsize=9.5, frameon=False, loc="upper left")
ax1.annotate("same after 1 year ($k=1$)", xy=(1, 1100), xytext=(2.55, 1180),
             fontsize=9, color=WARM,
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=1.0))
ax1.annotate("the gap widens", xy=(10, 2300), xytext=(4.6, 2380),
             fontsize=9, color=WARM,
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=1.0))

# ══════════════════════════════════════════════════════════
# (b) k を変えると、1 回あたりの利率と回数の両方が変わる
# ══════════════════════════════════════════════════════════
ax2.set_xlim(-0.1, 1.32)
ax2.set_ylim(-0.35, 3.35)
ax2.axis("off")
ax2.set_title("(b) One year, split into $k$ periods (nominal $12\\%$)",
              fontsize=11, color=INK, loc="left", pad=8)

# 1 期あたりの倍率は、12% を k 等分したもの
ROWS = [(2.7, 1, "$k=1$", "$\\times 1.12$", "once"),
        (1.6, 2, "$k=2$", "$\\times 1.06$", "twice"),
        (0.5, 4, "$k=4$", "$\\times 1.03$", "four times")]
for y, k, klab, fac, note in ROWS:
    ax2.plot([0.0, 1.0], [y, y], color=INK, linewidth=1.4)
    for j in range(k + 1):
        x = j / k
        ax2.plot([x, x], [y - 0.12, y + 0.12], color=INK, linewidth=1.2)
    for j in range(k):
        ax2.text((j + 0.5) / k, y + 0.20, fac, ha="center", va="bottom",
                 fontsize=9.5 if k < 4 else 8.5, color=ACCENT)
    ax2.text(-0.06, y, klab, ha="right", va="center", fontsize=11, color=INK)
    ax2.text(1.06, y, note, ha="left", va="center", fontsize=9.5, color=WARM)

ax2.text(0.5, -0.18, "smaller rate, more times $\\Rightarrow$ "
         "index $kn$, denominator $100k$",
         ha="center", va="center", fontsize=9.5, color=INK)

fig.tight_layout(w_pad=2.4)
path = os.path.join(OUT, "aasl-1-4-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
