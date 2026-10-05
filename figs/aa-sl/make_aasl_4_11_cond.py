"""AA SL 4.11（条件付き確率）の図をつくる。

    python3 figs/aa-sl/make_aasl_4_11_cond.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_4_11_cond.py  … 目視用の PNG も

出力: aa-sl/04-statistics-and-probability/img/aasl-4-11-idea-c.svg
      aa-sl/04-statistics-and-probability/      aa-sl/04-statistics-and-probability/img/aasl-4-11-idea-d.svg

(c) 条件付き確率 —— 分かったことで、標本空間がその行だけに狭まる。
    式は本文にある（方針 第 21 節）。図は表だけ。
(d) かけ算の形 —— 枝に沿ってかけると P(A∩B) になる。

★ 数値は例題・演習と重ならないように選んであります。
   (a) は合計 100（例題1 は 80、演習1 は 50）。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
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
FILL = "#fdf0dc"

fig1, ax1 = plt.subplots(figsize=(5.7, 2.7))
fig3, ax3 = plt.subplots(figsize=(5.7, 3.6))
# ══════════════════════════════════════════════════════════
# (a) 二元表と、狭まった標本空間
# ══════════════════════════════════════════════════════════
ax1.set_title("Knowing $B$ narrows the sample space to one row",
              fontsize=11, color=INK, loc="left", pad=12)
ax1.set_xlim(-0.35, 4.6)
ax1.set_ylim(0.2, 3.1)
ax1.axis("off")

COLS = ["", "$A$", "$A'$", "total"]
ROWS = [["$B$", "$21$", "$9$", "$30$"],
        ["$B'$", "$34$", "$36$", "$70$"],
        ["total", "$55$", "$45$", "$100$"]]

CW, CH = 1.05, 0.62
for _j, _c in enumerate(COLS):
    ax1.text(_j * CW + CW / 2, 2.75, _c, fontsize=10.5, color=ACCENT,
             ha="center", va="center")
for _i, _row in enumerate(ROWS):
    _y = 2.05 - _i * CH
    if _i == 0:
        ax1.add_patch(plt.Rectangle((CW * 0.0, _y - CH / 2), CW * 4, CH,
                                    facecolor=FILL, edgecolor="none",
                                    zorder=0))
    for _j, _v in enumerate(_row):
        ax1.text(_j * CW + CW / 2, _y, _v, fontsize=10.5,
                 color=WARM if _i == 0 and _j > 0 else INK,
                 ha="center", va="center")
ax1.plot([0, CW * 4], [2.05 + CH / 2 + 0.10] * 2, color=GREY, linewidth=1.0)
ax1.plot([0, CW * 4], [2.05 - 2 * CH + CH / 2] * 2, color=GREY, linewidth=1.0)
ax1.plot([CW, CW], [2.05 + CH / 2 + 0.10, 2.05 - 2 * CH - CH / 2],
         color=GREY, linewidth=1.0)
ax1.plot([CW * 3, CW * 3], [2.05 + CH / 2 + 0.10, 2.05 - 2 * CH - CH / 2],
         color=GREY, linewidth=1.0)


# ══════════════════════════════════════════════════════════
# (c) かけ算の形：枝に沿ってかける
# ══════════════════════════════════════════════════════════
ax3.set_title("Multiplying along two branches", fontsize=11, color=INK,
              loc="left", pad=12)
ax3.set_xlim(-0.45, 6.2)
ax3.set_ylim(-1.55, 1.75)
ax3.axis("off")

R3 = (0.10, 0.10)
N1 = {"B": (1.95, 1.05), "Bp": (1.95, -0.85)}
N2 = {("B", "A"): (3.95, 1.45), ("B", "Ap"): (3.95, 0.55),
      ("Bp", "A"): (3.95, -0.45), ("Bp", "Ap"): (3.95, -1.25)}
LAB1 = {"B": "$B$", "Bp": "$B'$"}
LAB2 = {"A": "$A$", "Ap": "$A'$"}

for _k, _pt in N1.items():
    _w = 2.4 if _k == "B" else 1.1
    ax3.plot([R3[0], _pt[0]], [R3[1], _pt[1]], color=ACCENT, linewidth=_w)
for (_a, _b), _pt in N2.items():
    _w = 2.4 if (_a, _b) == ("B", "A") else 1.1
    ax3.plot([N1[_a][0], _pt[0]], [N1[_a][1], _pt[1]], color=ACCENT,
             linewidth=_w)

_BOX3 = dict(facecolor="white", edgecolor="none", pad=1.4)
ax3.plot(*R3, "o", color=ACCENT, markersize=4)
for _k, _pt in N1.items():
    ax3.plot(*_pt, "o", color=ACCENT, markersize=4)
    ax3.text(_pt[0], _pt[1], LAB1[_k], fontsize=11, color=INK,
             ha="center", va="center", bbox=_BOX3)
for (_a, _b), _pt in N2.items():
    ax3.plot(*_pt, "o", color=ACCENT, markersize=4)
    ax3.text(_pt[0] + 0.13, _pt[1], LAB2[_b], fontsize=11, color=INK,
             va="center")

ax3.text(0.86, 0.80, r"$\frac{1}{3}$", fontsize=10.5, color=WARM, ha="center")
ax3.text(0.86, -0.68, r"$\frac{2}{3}$", fontsize=10.5, color=GREY, ha="center")
ax3.text(2.88, 1.42, r"$\frac{3}{5}$", fontsize=10.5, color=WARM, ha="center")
ax3.text(2.88, 0.62, r"$\frac{2}{5}$", fontsize=10.5, color=GREY, ha="center")
ax3.text(2.88, -0.44, r"$\frac{1}{4}$", fontsize=10.5, color=GREY, ha="center")
ax3.text(2.88, -1.22, r"$\frac{3}{4}$", fontsize=10.5, color=GREY, ha="center")

ax3.text(4.42, 1.45, r"$\frac{1}{3}\times\frac{3}{5}=\frac{1}{5}$",
         fontsize=10.5, color=WARM, va="center")


for _fig, _name in ((fig1, "aasl-4-11-idea-c.svg"),
                    (fig3, "aasl-4-11-idea-d.svg")):
    _fig.tight_layout()
    _p = os.path.join(OUT, _name)
    _fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
    print("wrote", os.path.normpath(_p))
    if os.environ.get("FIG_PNG"):
        _q = _p[:-4] + ".png"
        _fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                     facecolor="white")
        print("wrote", os.path.normpath(_q))
