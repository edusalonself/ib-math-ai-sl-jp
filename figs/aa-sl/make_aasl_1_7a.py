"""AA SL 1.7a の図をつくる。

    python3 figs/aa-sl/make_aasl_1_7a.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_1_7a.py  … 目視用の PNG も

出力: aa-sl/01-number-and-algebra/img/aasl-1-7a-idea.svg

(a) 27^(2/3) への 2 つの道。先に 3 乗根をとると数が小さいままで済む。
(b) 指数を 1/2 きざみで動かすと、値は毎回 3 倍になる（底 9）。

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
    1, 2, figsize=(10.0, 4.0), gridspec_kw={"width_ratios": [1.1, 1.0]}
)

# ══════════════════════════════════════════════════════════
# (a) 27^(2/3) への 2 つの道
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Two routes to $27^{\\frac{2}{3}}$",
              fontsize=11, color=INK, loc="left", pad=10)
ax1.set_xlim(0.0, 1.0)
ax1.set_ylim(0.0, 1.0)
ax1.axis("off")


def route(y, mid, step1, step2, note, colour):
    ax1.text(0.06, y, "$27$", ha="center", va="center", fontsize=13, color=INK)
    ax1.text(0.45, y, mid, ha="center", va="center", fontsize=13, color=colour)
    ax1.text(0.86, y, "$9$", ha="center", va="center", fontsize=13, color=INK)
    ax1.annotate("", xy=(0.34, y), xytext=(0.14, y),
                 arrowprops=dict(arrowstyle="->", color=colour, linewidth=1.4))
    ax1.annotate("", xy=(0.78, y), xytext=(0.56, y),
                 arrowprops=dict(arrowstyle="->", color=colour, linewidth=1.4))
    ax1.text(0.24, y + 0.075, step1, ha="center", va="bottom",
             fontsize=9.5, color=colour)
    ax1.text(0.67, y + 0.075, step2, ha="center", va="bottom",
             fontsize=9.5, color=colour)
    ax1.text(0.50, y - 0.16, note, ha="center", va="center",
             fontsize=9.5, color=colour)


route(0.72, "$3$", "cube root", "square", "small numbers all the way", ACCENT)
route(0.26, "$729$", "square", "cube root", "a hard root to do by hand", WARM)

ax1.plot([0.0, 1.0], [0.49, 0.49], color="#e5e7eb", linewidth=1.0)

# ══════════════════════════════════════════════════════════
# (b) 指数を 1/2 きざみで動かす（底 9）
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) Half-steps in the exponent, base $9$",
              fontsize=11, color=INK, loc="left", pad=10)
ax2.set_xlim(-0.45, 2.45)
ax2.set_ylim(-1.35, 1.55)
ax2.axis("off")

POINTS = [(0.0, "$9^{0}$", "$1$"),
          (0.5, "$9^{\\frac{1}{2}}$", "$3$"),
          (1.0, "$9^{1}$", "$9$"),
          (1.5, "$9^{\\frac{3}{2}}$", "$27$"),
          (2.0, "$9^{2}$", "$81$")]

ax2.plot([-0.15, 2.15], [0.0, 0.0], color=GREY, linewidth=1.3)
for t, lab, val in POINTS:
    half = (t * 2) % 2 == 1
    col = ACCENT if half else INK
    ax2.plot([t], [0.0], marker="o", markersize=8 if half else 6, color=col,
             zorder=3)
    ax2.text(t, 0.34, lab, ha="center", va="center", fontsize=11, color=col)
    ax2.text(t, -0.36, val, ha="center", va="center", fontsize=12, color=col)

for i in range(len(POINTS) - 1):
    a, b = POINTS[i][0], POINTS[i + 1][0]
    ax2.annotate("", xy=(b - 0.06, -0.72), xytext=(a + 0.06, -0.72),
                 arrowprops=dict(arrowstyle="->", color=WARM, linewidth=1.1))
    ax2.text((a + b) / 2, -0.93, r"$\times 3$", ha="center", va="center",
             fontsize=9, color=WARM)

ax2.text(1.0, -1.25, "the half-steps are the square roots",
         ha="center", va="center", fontsize=9.5, color=INK)
ax2.text(1.0, 1.25, "exponent", ha="center", va="center",
         fontsize=9.5, color=GREY)

fig.tight_layout(w_pad=2.4)
path = os.path.join(OUT, "aasl-1-7a-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
