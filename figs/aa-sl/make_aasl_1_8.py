"""AA SL 1.8 の図をつくる。

    python3 figs/aa-sl/make_aasl_1_8.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_1_8.py  … 目視用の PNG も

出力: aa-sl/01-number-and-algebra/img/aasl-1-8-idea.svg

(a) 長さ 1 の棒を、毎回「残りの半分」で埋めていく。
    足しても棒からはみ出さない ＝ 部分和が 1 を超えない。
(b) r の大きさで、項のふるまいが分かれる。
    |r| < 1 なら 0 に向かい、|r| > 1 なら大きくなる。

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
    1, 2, figsize=(9.8, 4.0), gridspec_kw={"width_ratios": [1.15, 1.0]}
)

# ══════════════════════════════════════════════════════════
# (a) 長さ 1 の棒を、半分ずつ埋めていく
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Filling a bar of length $1$",
              fontsize=11, color=INK, loc="left", pad=10)
ax1.set_xlim(-0.04, 1.10)
ax1.set_ylim(-0.75, 1.05)
ax1.axis("off")

TOP, BOT = 0.55, 0.15
edges = [0.0]
x = 0.0
for k in range(1, 8):
    x += 0.5 ** k
    edges.append(x)

shades = ["#cfe3f7", "#a9cdef", "#83b7e7", "#5da1df", "#4a93d6",
          "#3f8ace", "#3782c7"]
for i in range(len(edges) - 1):
    ax1.fill_between([edges[i], edges[i + 1]], BOT, TOP,
                     color=shades[i], linewidth=0)
    ax1.plot([edges[i + 1], edges[i + 1]], [BOT, TOP],
             color="white", linewidth=1.0)
ax1.plot([0, 1, 1, 0, 0], [BOT, BOT, TOP, TOP, BOT], color=INK, linewidth=1.4)

LABELS = [(0.25, r"$\frac{1}{2}$"), (0.625, r"$\frac{1}{4}$"),
          (0.8125, r"$\frac{1}{8}$")]
for cx, lab in LABELS:
    ax1.text(cx, (TOP + BOT) / 2, lab, ha="center", va="center",
             fontsize=13, color="#0b2f52")
ax1.text(0.945, (TOP + BOT) / 2, r"$\cdots$", ha="center", va="center",
         fontsize=13, color="#0b2f52")

ax1.plot([1.0, 1.0], [TOP, TOP + 0.22], color=WARM, linewidth=1.2)
ax1.text(1.0, TOP + 0.30, "$1$", ha="center", va="bottom",
         fontsize=12, color=WARM)
ax1.text(0.5, TOP + 0.30, "the pieces never overflow",
         ha="center", va="bottom", fontsize=10, color=INK)

for i, lab in [(1, "$S_1$"), (2, "$S_2$"), (3, "$S_3$")]:
    ax1.plot([edges[i], edges[i]], [BOT - 0.10, BOT], color=GREY,
             linewidth=1.0)
    ax1.text(edges[i], BOT - 0.18, lab, ha="center", va="top",
             fontsize=9.5, color=GREY)

ax1.text(0.5, -0.58, "each new piece is half of what is left",
         ha="center", va="center", fontsize=10, color=INK)

# ══════════════════════════════════════════════════════════
# (b) r の大きさで、項のふるまいが分かれる
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) The terms of $r^{\\,n}$", fontsize=11, color=INK,
              loc="left", pad=10)
NS = list(range(0, 6))
small = [0.5 ** k for k in NS]
big = [2.0 ** k for k in NS]

ax2.plot(NS, small, marker="o", markersize=5, color=ACCENT, linewidth=1.7,
         label="$r = 0.5$")
ax2.plot(NS, big, marker="o", markersize=5, color=WARM, linewidth=1.7,
         label="$r = 2$")
ax2.set_ylim(-0.35, 4.4)
ax2.set_xlim(-0.25, 5.6)
ax2.set_xticks(NS)
ax2.set_yticks([0, 1, 2, 3, 4])
ax2.set_xlabel("$n$", fontsize=10, color=INK)
ax2.tick_params(labelsize=9, colors=INK)
for side in ("top", "right"):
    ax2.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax2.spines[side].set_color(INK)
ax2.grid(axis="y", color="#e5e7eb", linewidth=0.8)
ax2.set_axisbelow(True)
ax2.legend(fontsize=9.5, frameon=False, loc="upper left")
ax2.axhline(0.0, color=GREY, linewidth=1.0)
ax2.annotate("dies away to $0$", xy=(4, 0.0625), xytext=(2.3, 0.85),
             fontsize=9.5, color=ACCENT,
             arrowprops=dict(arrowstyle="->", color=ACCENT, linewidth=1.0))
ax2.annotate("off the top", xy=(2.15, 4.15), xytext=(3.1, 3.6),
             fontsize=9.5, color=WARM,
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=1.0))

fig.tight_layout(w_pad=2.4)
path = os.path.join(OUT, "aasl-1-8-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
