"""AA SL 1.1 の図をつくる。

    python3 figs/aa-sl/make_aasl_1_1.py          … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_1_1.py  … 目視用の PNG も

出力: aa-sl/01-number-and-algebra/img/aasl-1-1-scale.svg

(a) 10 のべきの物差し。原子から太陽までを 1 本の線に並べる。
(b) 小数点をどちらへ何桁動かすか。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \begin{pmatrix} は読めない → \binom を使う
  * \lvert \rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に演習の答えを書かないこと。
★ PNG は目視用です。確認が終わったら消してください。
"""
import math
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

# ── (a) に並べるもの。(値, 表示する式, 名前, ラベルを上に出すか)
#    ★ 点を打つ位置は log10(値)。指数 k をそのまま使うと、
#      8×10^-6 が 10^-6 の目盛りに乗ってしまい、「1 目盛りで 10 倍」
#      という図の主張と食いちがいます。
#    ★ 何の長さなのかを、名前の側に必ず書くこと（単位はメートル）。
ITEMS = [
    (1e-10, r"$1 \times 10^{-10}$", "atom (width)", True),
    (8e-6, r"$8 \times 10^{-6}$", "red blood cell (width)", False),
    (1.7, r"$1.7 \times 10^{0}$", "person (height)", True),
    (1.3e7, r"$1.3 \times 10^{7}$", "Earth (diameter)", False),
    (1.5e11, r"$1.5 \times 10^{11}$", "Earth to Sun (distance)", True),
]

fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(9.0, 5.9), gridspec_kw={"height_ratios": [1.3, 1.0]}
)

# ══════════════════════════════════════════════════════════
# (a) 10 のべきの物差し
# ══════════════════════════════════════════════════════════
ax1.set_xlim(-11.8, 12.8)
ax1.set_ylim(-2.0, 1.9)
ax1.axis("off")
ax1.set_title(
    "(a) Lengths in metres — one step along the line is ten times bigger",
    fontsize=11, color=INK, loc="left", pad=8,
)

ax1.annotate(
    "", xy=(12.6, 0), xytext=(-11.6, 0),
    arrowprops=dict(arrowstyle="-|>", color=INK, linewidth=1.4),
)

for k in range(-10, 12):
    h = 0.15 if k % 5 else 0.26
    ax1.plot([k, k], [-h, h], color=GREY if k % 5 else INK,
             linewidth=0.9 if k % 5 else 1.3, solid_capstyle="butt")
for k in (-10, -5, 0, 5, 10):
    ax1.text(k, -0.38, r"$10^{%d}$" % k, ha="center", va="top",
             fontsize=10, color=INK)

for value_of, value, name, above in ITEMS:
    x = math.log10(value_of)
    y_text = 0.62 if above else -1.15
    va = "bottom" if above else "top"
    if above:
        ax1.plot([x, x], [0.0, 0.52], color=ACCENT,
                 linewidth=1.0, linestyle=(0, (3, 2)))
    else:
        # 10^k の目盛りラベルの帯（およそ -0.30 〜 -0.80）を避けて、
        # 破線を 2 本に分ける。ラベルの上に線が重なると読めなくなる。
        ax1.plot([x, x], [0.0, -0.28], color=ACCENT,
                 linewidth=1.0, linestyle=(0, (3, 2)))
        ax1.plot([x, x], [-0.84, -1.05], color=ACCENT,
                 linewidth=1.0, linestyle=(0, (3, 2)))
    ax1.plot([x], [0.0], marker="o", markersize=6.5, color=ACCENT, zorder=3)
    ax1.text(x, y_text, name + "\n" + value, ha="center", va=va,
             fontsize=9.5, color=ACCENT, linespacing=1.4)

# ══════════════════════════════════════════════════════════
# (b) 小数点の動かし方
# ══════════════════════════════════════════════════════════
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 3.5)
ax2.axis("off")
ax2.set_title(
    "(b) Move the decimal point until the first factor $a$ has $1 \\leq a < 10$",
    fontsize=11, color=INK, loc="left", pad=8,
)

X0, DX = 0.35, 0.30


def digits(chars, y):
    """1 文字ずつ等間隔に置く。戻り値は各文字の中心の x。"""
    xs = []
    for i, c in enumerate(chars):
        x = X0 + i * DX
        xs.append(x)
        ax2.text(x, y, c, fontsize=15, color=INK, ha="center", va="center",
                 family="monospace")
    return xs


def move(x_from, x_to, y, label, rad):
    ax2.add_patch(FancyArrowPatch(
        (x_from, y), (x_to, y), arrowstyle="-|>", mutation_scale=13,
        color=ACCENT, linewidth=1.3, connectionstyle="arc3,rad=%.2f" % rad,
    ))
    ax2.text((x_from + x_to) / 2, y - 0.50, label, fontsize=9.5,
             color=ACCENT, ha="center", va="center")


# 大きい数：小数点を左へ 6 桁
yA = 2.60
xs = digits(list("3200000."), yA)
move(xs[7], (xs[0] + xs[1]) / 2, yA - 0.40, "6 places to the left", -0.24)
ax2.text(3.35, yA, r"$= 3.2 \times 10^{6}$", fontsize=14, color=INK,
         va="center")
ax2.text(5.95, yA, "10 or bigger, so $k$ is positive", fontsize=9.5,
         color=GREY, va="center")

# 小さい数：小数点を右へ 5 桁
yB = 1.05
xs = digits(list("0.000047"), yB)
move(xs[1], (xs[6] + xs[7]) / 2, yB - 0.40, "5 places to the right", 0.24)
ax2.text(3.35, yB, r"$= 4.7 \times 10^{-5}$", fontsize=14, color=INK,
         va="center")
ax2.text(5.95, yB, "less than 1, so $k$ is negative", fontsize=9.5,
         color=GREY, va="center")

fig.tight_layout(h_pad=2.0)
path = os.path.join(OUT, "aasl-1-1-scale.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

# 目視用の PNG。確認が終わったら消すこと（リポジトリに入れません）。
if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
