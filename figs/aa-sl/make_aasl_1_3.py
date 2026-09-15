"""AA SL 1.3 の図をつくる。

    python3 figs/aa-sl/make_aasl_1_3.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_1_3.py  … 目視用の PNG も

出力: aa-sl/01-number-and-algebra/img/aasl-1-3-idea.svg

(a) 同じ数を掛けていく。u_1 から u_5 までで r を掛けるのは 4 回。
(b) S_n と r S_n を並べて引くと、まん中が消える。

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
    2, 1, figsize=(9.0, 5.8), gridspec_kw={"height_ratios": [1.0, 1.1]}
)

# ══════════════════════════════════════════════════════════
# (a) 掛ける回数は n-1
# ══════════════════════════════════════════════════════════
ax1.set_xlim(-0.6, 5.4)
ax1.set_ylim(-1.15, 1.5)
ax1.axis("off")
ax1.set_title(
    "(a) From $u_1$ to $u_n$ the ratio $r$ is used $n-1$ times",
    fontsize=11, color=INK, loc="left", pad=8,
)

XS = [0.2, 1.2, 2.2, 3.2, 4.2]
LABELS = ["$u_1$", "$u_1r$", "$u_1r^2$", "$u_1r^3$", "$u_1r^4$"]
ax1.plot([-0.2, 5.0], [0, 0], color=INK, linewidth=1.3)
for x, lab in zip(XS, LABELS):
    ax1.plot([x], [0], marker="o", markersize=7, color=ACCENT, zorder=3)
    ax1.text(x, -0.32, lab, ha="center", va="top", fontsize=12, color=ACCENT)

for i in range(4):
    a, b = XS[i], XS[i + 1]
    ax1.add_patch(FancyArrowPatch(
        (a, 0.10), (b, 0.10), arrowstyle="-|>", mutation_scale=12,
        color=WARM, linewidth=1.2, connectionstyle="arc3,rad=-0.45",
    ))
    ax1.text((a + b) / 2, 0.78, "$\\times r$", ha="center", va="center",
             fontsize=11, color=WARM)

ax1.text(2.2, -0.85, "4 multiplications, not 5   $\\Rightarrow$   "
         "$u_5 = u_1r^4$",
         ha="center", va="center", fontsize=11, color=INK)

# ══════════════════════════════════════════════════════════
# (b) S_n と r S_n を並べて引く
# ══════════════════════════════════════════════════════════
ax2.set_xlim(-0.2, 10.2)
ax2.set_ylim(-1.7, 1.8)
ax2.axis("off")
ax2.set_title(
    "(b) Write $S_n$ and $rS_n$ one above the other: the middle terms cancel",
    fontsize=11, color=INK, loc="left", pad=8,
)

COLS = [2.05, 3.35, 4.65, 6.05, 7.55]
TOP = ["$u_1$", "$u_1r$", "$u_1r^2$", "$\\cdots$", "$u_1r^{n-1}$"]
BOT = ["", "$u_1r$", "$u_1r^2$", "$\\cdots$", "$u_1r^{n-1}$"]

ax2.text(1.55, 1.05, "$S_n =$", ha="right", va="center", fontsize=12,
         color=INK)
ax2.text(1.55, 0.15, "$rS_n =$", ha="right", va="center", fontsize=12,
         color=INK)
for i, x in enumerate(COLS):
    ax2.text(x, 1.05, TOP[i], ha="center", va="center", fontsize=12,
             color=ACCENT if i in (0,) else GREY)
    if BOT[i]:
        ax2.text(x, 0.15, BOT[i], ha="center", va="center", fontsize=12,
                 color=GREY)
    if i in (1, 2, 3, 4):
        ax2.plot([x - 0.42, x + 0.42], [0.60, 0.60], color=WARM,
                 linewidth=1.1)
ax2.text(8.95, 0.15, "$u_1r^{n}$", ha="center", va="center", fontsize=12,
         color=ACCENT)

ax2.text(9.9, 0.60, "these cancel", ha="right", va="bottom", fontsize=9.5,
         color=WARM)

ax2.plot([1.0, 9.6], [-0.35, -0.35], color=INK, linewidth=1.0)
ax2.text(1.55, -0.72, "$rS_n - S_n =$", ha="right", va="center",
         fontsize=12, color=INK)
ax2.text(2.05, -0.72, "$u_1r^{n} - u_1$", ha="left", va="center",
         fontsize=12, color=ACCENT)
ax2.text(5.0, -1.35, "$S_n(r-1) = u_1(r^{n}-1)$   $\\Rightarrow$   "
         "$S_n = \\frac{u_1(r^{n}-1)}{r-1}$   (needs $r \\neq 1$)",
         ha="center", va="center", fontsize=12, color=INK)

fig.tight_layout(h_pad=2.0)
path = os.path.join(OUT, "aasl-1-3-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
