"""AA SL 4.6b の図をつくる。

    python3 figs/aa-sl/make_aasl_4_6b.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_4_6b.py  … 目視用の PNG も

出力: aa-sl/04-statistics-and-probability/img/aasl-4-6b-idea.svg

(a) 条件付き確率 —— 分かったことで、標本空間がその行だけに狭まる。
(b) もどさない樹形図 —— 2 段目は分母も分子も変わる。

★ 数値は例題・演習と重ならないように選んであります。
   (a) は合計 100（例題1 は 80、演習1 は 50）。
   (b) は 2 と 3 の袋（例題3 は 5 と 3、演習3 は 4 と 6）。
       演習9 の箱 1 は 3 と 2 で構成が同じだが、あちらは 1 個しか取らないので、
       答え（P(R) = 2/5、P(box 1 | R) = 3/4）とは重ならない。

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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.6, 4.9))

# ══════════════════════════════════════════════════════════
# (a) 二元表と、狭まった標本空間
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Knowing $B$ narrows the sample space to one row",
              fontsize=11, color=INK, loc="left", pad=12)
ax1.set_xlim(-0.35, 4.6)
ax1.set_ylim(-2.5, 3.5)
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

ax1.text(-0.35, -0.10, "if you are told $B$ happened, only the shaded row "
         "is still possible", fontsize=9.5, color=WARM)
ax1.text(-0.35, -0.62, "$P(A \\mid B)$ uses that row as the whole of the "
         "sample space:", fontsize=9.5, color=INK)
ax1.text(-0.35, -1.22, "$P(A \\mid B) = \\frac{21}{30} = \\frac{7}{10}$",
         fontsize=11, color=ACCENT)
ax1.text(-0.35, -1.90, "but $P(A) = \\frac{55}{100} = \\frac{11}{20}$, so "
         "knowing $B$ changes the probability", fontsize=9.5, color=INK)

# ══════════════════════════════════════════════════════════
# (b) もどさない樹形図
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) Without replacement, the second stage changes",
              fontsize=11, color=INK, loc="left", pad=12)
ax2.set_xlim(-0.4, 6.6)
ax2.set_ylim(-2.5, 3.5)
ax2.axis("off")

ROOT = (0.10, 1.15)
L1 = {"W": (2.00, 2.25), "B": (2.00, 0.05)}
L2 = {("W", "W"): (4.05, 2.85), ("W", "B"): (4.05, 1.65),
      ("B", "W"): (4.05, 0.65), ("B", "B"): (4.05, -0.55)}

for _pt in L1.values():
    ax2.plot([ROOT[0], _pt[0]], [ROOT[1], _pt[1]], color=ACCENT, linewidth=1.3)
for (_a, _b), _pt in L2.items():
    ax2.plot([L1[_a][0], _pt[0]], [L1[_a][1], _pt[1]], color=ACCENT,
             linewidth=1.3)

_BOX = dict(facecolor="white", edgecolor="none", pad=1.4)
ax2.plot(*ROOT, "o", color=ACCENT, markersize=4)
ax2.text(0.10, 0.78, "start", fontsize=9.5, color=GREY, ha="center")
for _k, _pt in L1.items():
    ax2.plot(*_pt, "o", color=ACCENT, markersize=4)
    ax2.text(_pt[0], _pt[1], "$%s$" % _k, fontsize=11, color=INK,
             ha="center", va="center", bbox=_BOX)

ax2.text(0.92, 1.92, r"$\frac{2}{5}$", fontsize=10, color=GREY, ha="center")
ax2.text(0.92, 0.42, r"$\frac{3}{5}$", fontsize=10, color=GREY, ha="center")

_lab = {("W", "W"): (r"$\frac{1}{4}$", "$W$", r"$\frac{2}{5}\times\frac{1}{4}=\frac{2}{20}$"),
        ("W", "B"): (r"$\frac{3}{4}$", "$B$", r"$\frac{2}{5}\times\frac{3}{4}=\frac{6}{20}$"),
        ("B", "W"): (r"$\frac{2}{4}$", "$W$", r"$\frac{3}{5}\times\frac{2}{4}=\frac{6}{20}$"),
        ("B", "B"): (r"$\frac{2}{4}$", "$B$", r"$\frac{3}{5}\times\frac{2}{4}=\frac{6}{20}$")}
for _key, _pt in L2.items():
    _p, _name, _prod = _lab[_key]
    _mx = (L1[_key[0]][0] + _pt[0]) / 2
    _my = (L1[_key[0]][1] + _pt[1]) / 2
    ax2.text(_mx, _my + 0.15, _p, fontsize=9.5, color=WARM, ha="center")
    ax2.text(_pt[0] + 0.10, _pt[1], _name, fontsize=10.5, color=INK,
             va="center")
    ax2.text(_pt[0] + 0.48, _pt[1], _prod, fontsize=9.5, color=ACCENT,
             va="center")

ax2.text(-0.4, -1.15, "the bag starts with $2$ white and $3$ black; one is "
         "taken and kept", fontsize=9.5, color=INK)
ax2.text(-0.4, -1.62, "so the second denominator is $4$, not $5$, and the "
         "numerator depends on the first result", fontsize=9.5, color=WARM)
ax2.text(-0.4, -2.20, "the four ends still add to $1$:  "
         r"$\frac{2}{20}+\frac{6}{20}+\frac{6}{20}+\frac{6}{20}=1$",
         fontsize=9.5, color=INK)

fig.tight_layout(w_pad=2.0)
path = os.path.join(OUT, "aasl-4-6b-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))
print("  table: 21+9+34+36 =", 21 + 9 + 34 + 36,
      "  tree ends:", 2 / 20 + 6 / 20 + 6 / 20 + 6 / 20)

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
