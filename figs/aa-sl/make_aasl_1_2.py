"""AA SL 1.2 の図をつくる。

    python3 figs/aa-sl/make_aasl_1_2.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_1_2.py  … 目視用の PNG も

出力: aa-sl/01-number-and-algebra/img/aasl-1-2-idea.svg

(a) 等間隔のジャンプ。u_1 から u_n までで d を足すのは n-1 回。
(b) 和を「前から」と「うしろから」で組にすると、どの組も u_1+u_n。

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
from matplotlib.patches import FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "01-number-and-algebra", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"

fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(9.0, 5.6), gridspec_kw={"height_ratios": [1.0, 1.05]}
)

# ══════════════════════════════════════════════════════════
# (a) 等間隔のジャンプ： u_1 から u_5 まで、d を足すのは 4 回
# ══════════════════════════════════════════════════════════
ax1.set_xlim(-0.6, 5.4)
ax1.set_ylim(-1.15, 1.5)
ax1.axis("off")
ax1.set_title(
    "(a) From $u_1$ to $u_n$ the difference $d$ is added $n-1$ times",
    fontsize=11, color=INK, loc="left", pad=8,
)

XS = [0.2, 1.2, 2.2, 3.2, 4.2]
LABELS = ["$u_1$", "$u_2$", "$u_3$", "$u_4$", "$u_5$"]
ax1.plot([-0.2, 5.0], [0, 0], color=INK, linewidth=1.3)
for x, lab in zip(XS, LABELS):
    ax1.plot([x], [0], marker="o", markersize=7, color=ACCENT, zorder=3)
    ax1.text(x, -0.30, lab, ha="center", va="top", fontsize=12, color=ACCENT)

for i in range(4):
    a, b = XS[i], XS[i + 1]
    ax1.add_patch(FancyArrowPatch(
        (a, 0.10), (b, 0.10), arrowstyle="-|>", mutation_scale=12,
        color=WARM, linewidth=1.2, connectionstyle="arc3,rad=-0.45",
    ))
    ax1.text((a + b) / 2, 0.78, "$+d$", ha="center", va="center",
             fontsize=11, color=WARM)

ax1.text(2.2, -0.80, "4 jumps, not 5   $\\Rightarrow$   $u_5 = u_1 + 4d$",
         ha="center", va="center", fontsize=11, color=INK)

# ══════════════════════════════════════════════════════════
# (b) 和を折り返して組にする
# ══════════════════════════════════════════════════════════
ax2.set_xlim(-0.6, 5.4)
ax2.set_ylim(-1.5, 1.7)
ax2.axis("off")
ax2.set_title(
    "(b) Add the sum forwards and backwards: every pair makes $u_1+u_n$",
    fontsize=11, color=INK, loc="left", pad=8,
)

TOP = ["$u_1$", "$u_2$", "$u_3$", "$\\cdots$", "$u_n$"]
BOT = ["$u_n$", "$u_{n-1}$", "$u_{n-2}$", "$\\cdots$", "$u_1$"]
for i, x in enumerate(XS):
    ax2.text(x, 0.95, TOP[i], ha="center", va="center", fontsize=12,
             color=ACCENT)
    ax2.text(x, 0.05, BOT[i], ha="center", va="center", fontsize=12,
             color=ACCENT)
    if i != 3:
        ax2.plot([x, x], [0.72, 0.30], color=GREY, linewidth=0.9,
                 linestyle=(0, (3, 2)))
        ax2.text(x, -0.62, "$u_1+u_n$", ha="center", va="center",
                 fontsize=11, color=WARM)

ax2.text(XS[0] - 0.55, 0.95, "$S_n =$", ha="right", va="center",
         fontsize=12, color=INK)
ax2.text(XS[0] - 0.55, 0.05, "$S_n =$", ha="right", va="center",
         fontsize=12, color=INK)
ax2.plot([-0.45, 4.9], [-0.30, -0.30], color=INK, linewidth=1.0)
ax2.text(XS[0] - 0.55, -0.62, "$2S_n =$", ha="right", va="center",
         fontsize=12, color=INK)
ax2.text(2.2, -1.20, "$n$ pairs   $\\Rightarrow$   "
         "$2S_n = n(u_1+u_n)$   $\\Rightarrow$   "
         "$S_n = \\frac{n}{2}(u_1+u_n)$",
         ha="center", va="center", fontsize=12, color=INK)

fig.tight_layout(h_pad=2.0)
path = os.path.join(OUT, "aasl-1-2-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
