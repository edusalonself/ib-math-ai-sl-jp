"""AA SL 1.9 の図をつくる。

    python3 figs/aa-sl/make_aasl_1_9.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_1_9.py  … 目視用の PNG も

出力: aa-sl/01-number-and-algebra/img/aasl-1-9-idea.svg

(a) パスカルの三角形（n = 0 から 4 まで）。すぐ上の 2 つを足す。
(b) (a+b)^4 の一般項の読み方。a の指数は下がり、b の指数は上がり、
    和はいつも n。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に演習の答えを書かないこと（n = 5 以降の行は書かない）。
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
    1, 2, figsize=(10.2, 4.2), gridspec_kw={"width_ratios": [1.0, 1.3]}
)

# ══════════════════════════════════════════════════════════
# (a) パスカルの三角形（n = 0 から 4）
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Pascal's triangle", fontsize=11, color=INK,
              loc="left", pad=10)
ax1.set_xlim(-3.0, 3.0)
ax1.set_ylim(-1.5, 4.9)
ax1.axis("off")

ROWS = [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
STEP_X, STEP_Y = 0.92, 0.92


def pos(row, i):
    return (i - row / 2.0) * STEP_X, 4.2 - row * STEP_Y


for _row, vals in enumerate(ROWS):
    for _i, v in enumerate(vals):
        px, py = pos(_row, _i)
        hot = (_row == 4 and _i == 2)
        ax1.text(px, py, "$%d$" % v, ha="center", va="center",
                 fontsize=13, color=ACCENT if hot else INK)
    ax1.text(-2.85, 4.2 - _row * STEP_Y, "$n=%d$" % _row, ha="left",
             va="center", fontsize=9.5, color=GREY)

for _i in (1, 2):
    sx, sy = pos(3, _i)
    tx, ty = pos(4, 2)
    ax1.annotate("", xy=(tx, ty + 0.26), xytext=(sx, sy - 0.26),
                 arrowprops=dict(arrowstyle="->", color=ACCENT, linewidth=1.3))
ax1.text(0.0, -0.42, "$3 + 3 = 6$", ha="center", va="center",
         fontsize=11, color=ACCENT)
ax1.text(0.0, -1.10, "add the two entries above",
         ha="center", va="center", fontsize=10, color=INK)

# ══════════════════════════════════════════════════════════
# (b) 一般項の読み方
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) Reading a term of $(a+b)^{4}$", fontsize=11, color=INK,
              loc="left", pad=10)
ax2.set_xlim(0.0, 1.0)
ax2.set_ylim(0.0, 1.0)
ax2.axis("off")

TERMS = [(0.28, "$a^{4}$", 4, 0),
         (0.45, "$4a^{3}b$", 3, 1),
         (0.62, "$6a^{2}b^{2}$", 2, 2),
         (0.79, "$4ab^{3}$", 1, 3),
         (0.955, "$b^{4}$", 0, 4)]

Y_TERM, Y_A, Y_B, Y_SUM = 0.72, 0.50, 0.32, 0.14

ax2.plot([0.235, 0.995], [Y_A, Y_A], color="#e9eef4", linewidth=13,
         solid_capstyle="butt", zorder=0)
ax2.plot([0.235, 0.995], [Y_B, Y_B], color="#f6ede1", linewidth=13,
         solid_capstyle="butt", zorder=0)

for cx, term, ia, ib in TERMS:
    ax2.text(cx, Y_TERM, term, ha="center", va="center",
             fontsize=13, color=INK)
    ax2.text(cx, Y_A, "$%d$" % ia, ha="center", va="center",
             fontsize=12, color=ACCENT, zorder=2)
    ax2.text(cx, Y_B, "$%d$" % ib, ha="center", va="center",
             fontsize=12, color=WARM, zorder=2)
    ax2.text(cx, Y_SUM, "$%d$" % (ia + ib), ha="center", va="center",
             fontsize=12, color=GREY)

ax2.text(0.20, Y_A, "index of $a$", ha="right", va="center",
         fontsize=9.5, color=ACCENT)
ax2.text(0.20, Y_B, "index of $b$", ha="right", va="center",
         fontsize=9.5, color=WARM)
ax2.text(0.20, Y_SUM, "sum", ha="right", va="center",
         fontsize=9.5, color=GREY)

ax2.text(0.62, 0.92, "falls   $\\longrightarrow$   rises",
         ha="center", va="center", fontsize=10, color=INK)
ax2.text(0.55, 0.01, "the two indices always add up to $n$",
         ha="center", va="center", fontsize=10, color=INK)

fig.tight_layout(w_pad=2.0)
path = os.path.join(OUT, "aasl-1-9-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
