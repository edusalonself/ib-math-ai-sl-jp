"""AA SL 4.11 の図をつくる。

    python3 figs/aa-sl/make_aasl_4_11.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_4_11.py  … 目視用の PNG も

出力: aa-sl/04-statistics-and-probability/img/aasl-4-11-idea-b.svg

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

fig2, ax2 = plt.subplots(figsize=(5.7, 4.0))
# ══════════════════════════════════════════════════════════
ax2.set_title("In a table, independence means equal row proportions",
              fontsize=11, color=INK, loc="left", pad=12)
ax2.set_xlim(-0.4, 4.8)
ax2.set_ylim(0.2, 3.1)
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


for _fig, _name in ((fig2, "aasl-4-11-idea-b.svg"),):
    _fig.tight_layout()
    _p = os.path.join(OUT, _name)
    _fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
    print("wrote", os.path.normpath(_p))
    if os.environ.get("FIG_PNG"):
        _q = _p[:-4] + ".png"
        _fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                     facecolor="white")
        print("wrote", os.path.normpath(_q))
