"""AA SL 4.11 の図をつくる。

    python3 figs/aa-sl/make_aasl_4_11.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_4_11.py  … 目視用の PNG も

出力: aa-sl/04-statistics-and-probability/img/aasl-4-11-idea.svg

(a) 独立の 3 つの言い方が同じことを表していること。
(b) 二元表で見ると、独立は「どの行でも割合が同じ」ということ。

★ (b) の表の数値（合計 100）は例題・演習と重なりません。
   例題1 は 0.4 / 0.5 / 0.2、演習4 の表は合計 200 です。

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
OUT = os.path.join(HERE, "..", "..", "aa-sl", "04-statistics-and-probability", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
FILL = "#e8f0f9"
SHADE = "#fdf0dc"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.6, 4.8))

# ══════════════════════════════════════════════════════════
# (a) 独立の 3 つの言い方
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Three ways of saying the same thing", fontsize=11,
              color=INK, loc="left", pad=12)
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis("off")

BOXES = [(5.0, 8.2, r"$P(A \cap B) = P(A)\,P(B)$"),
         (2.2, 3.6, r"$P(A \mid B) = P(A)$"),
         (7.8, 3.6, r"$P(A \mid B') = P(A)$")]
for _x, _y, _t in BOXES:
    ax1.text(_x, _y, _t, fontsize=11, color=ACCENT, ha="center", va="center",
             bbox=dict(boxstyle="round,pad=0.45", facecolor=FILL,
                       edgecolor=ACCENT, linewidth=1.2))

for _p, _q in [((4.2, 7.5), (2.7, 4.4)), ((5.8, 7.5), (7.3, 4.4)),
               ((3.6, 3.6), (6.4, 3.6))]:
    ax1.annotate("", xy=_q, xytext=_p,
                 arrowprops=dict(arrowstyle="<->", color=GREY, linewidth=1.2))

ax1.text(1.9, 6.0, "divide by\n$P(B)$", fontsize=9, color=GREY, ha="center",
         linespacing=1.5)
ax1.text(8.1, 6.0, "use\n$P(A) = P(A \\cap B)$\n$+ P(A \\cap B')$", fontsize=9,
         color=GREY, ha="center", linespacing=1.5)
ax1.text(5.0, 2.45, "when $0 < P(B) < 1$, each one implies the others",
         fontsize=9, color=GREY, ha="center")

ax1.text(0.0, 1.10, "showing any one of the three is enough to show "
         "independence", fontsize=9.5, color=INK)
ax1.text(0.0, 0.35, "only the first still makes sense when $P(B) = 0$ or "
         "$P(B) = 1$", fontsize=9.5, color=WARM)

# ══════════════════════════════════════════════════════════
# (b) 二元表で見た独立
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) In a table, independence means equal row proportions",
              fontsize=11, color=INK, loc="left", pad=12)
ax2.set_xlim(-0.4, 4.8)
ax2.set_ylim(-2.6, 3.4)
ax2.axis("off")

COLS = ["", "$A$", "$A'$", "total"]
ROWS = [["$B$", "$18$", "$12$", "$30$"],
        ["$B'$", "$42$", "$28$", "$70$"],
        ["total", "$60$", "$40$", "$100$"]]
CW, CH = 1.05, 0.62
for _j, _c in enumerate(COLS):
    ax2.text(_j * CW + CW / 2, 2.75, _c, fontsize=10.5, color=ACCENT,
             ha="center", va="center")
for _i, _row in enumerate(ROWS):
    _y = 2.05 - _i * CH
    if _i < 2:
        ax2.add_patch(plt.Rectangle((0.0, _y - CH / 2), CW * 4, CH,
                                    facecolor=SHADE,
                                    edgecolor="none", zorder=0))
    for _j, _v in enumerate(_row):
        ax2.text(_j * CW + CW / 2, _y, _v, fontsize=10.5, color=INK,
                 ha="center", va="center")
ax2.plot([0, CW * 4], [2.05 + CH / 2 + 0.10] * 2, color=GREY, linewidth=1.0)
ax2.plot([0, CW * 4], [2.05 - 2 * CH + CH / 2] * 2, color=GREY, linewidth=1.0)
ax2.plot([CW, CW], [2.05 + CH / 2 + 0.10, 2.05 - 2 * CH - CH / 2],
         color=GREY, linewidth=1.0)
ax2.plot([CW * 3, CW * 3], [2.05 + CH / 2 + 0.10, 2.05 - 2 * CH - CH / 2],
         color=GREY, linewidth=1.0)

ax2.text(-0.4, -0.10, "$P(A \\mid B) = \\frac{18}{30} = 0.6$ and "
         "$P(A \\mid B') = \\frac{42}{70} = 0.6$", fontsize=10, color=WARM)
ax2.text(-0.4, -0.80, "$P(A) = \\frac{60}{100} = 0.6$ as well, so $A$ and $B$ "
         "are independent", fontsize=10, color=ACCENT)
ax2.text(-0.4, -1.70, "if one row gave a different proportion, the events "
         "would not be", fontsize=9.5, color=INK)
ax2.text(-0.4, -2.20, "independent, however small the difference",
         fontsize=9.5, color=INK)

fig.tight_layout(w_pad=2.2)
path = os.path.join(OUT, "aasl-4-11-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))
print("  table total =", 18 + 12 + 42 + 28,
      "  18/30 =", 18 / 30, " 42/70 =", 42 / 70, " 60/100 =", 60 / 100)

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
