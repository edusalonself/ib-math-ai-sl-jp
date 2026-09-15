"""AA SL 4.3 の図をつくる。

    python3 figs/aa-sl/make_aasl_4_3.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_4_3.py  … 目視用の PNG も

出力: aa-sl/04-statistics-and-probability/img/aasl-4-3-idea.svg

(a) mid-interval value —— 階級の中の値を、まん中の 1 つの数で代表させる。
(b) 定数を足す・かけると、mean と標準偏差がどうなるか。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に例題・演習の数値を書かないこと（階級の目盛りは記号と一般の数）。
★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "04-statistics-and-probability", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
GREEN = "#15803d"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 4.6))

# ══════════════════════════════════════════════════════════
# (a) mid-interval value
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) The mid-interval value stands for the whole class",
              fontsize=11, color=INK, loc="left", pad=10)
ax1.set_xlim(-0.6, 10.6)
ax1.set_ylim(-1.7, 4.0)
ax1.axis("off")

# 階級の境目
EDGES = [0.6, 3.4, 6.2, 9.0]
Y = 1.05
ax1.plot([EDGES[0] - 0.6, EDGES[-1] + 0.6], [Y, Y], color=GREY, linewidth=1.0)
for _e in EDGES:
    ax1.plot([_e, _e], [Y - 0.22, Y + 0.22], color=GREY, linewidth=1.2)

rng = np.random.default_rng(11)
for _i in range(3):
    _a, _b = EDGES[_i], EDGES[_i + 1]
    _mid = (_a + _b) / 2
    # その階級の中に散らばっている値（★ まん中について対称に置く。
    #    片寄せて描くと、「まん中を使うのが公平」という本文の理由と食いちがう）
    _off = np.array([-0.40, -0.20, 0.0, 0.20, 0.40]) * (_b - _a - 0.56)
    _v = _mid + _off + rng.uniform(-0.04, 0.04, 5)
    ax1.scatter(_v, [Y + 0.75] * 5, s=26, color="#c7d7e8", zorder=2)
    ax1.plot([_mid], [Y + 0.75], marker="o", markersize=0)
    # まん中に集める矢印
    for _p in _v:
        ax1.annotate("", xy=(_mid, Y + 0.30), xytext=(_p, Y + 0.66),
                     arrowprops=dict(arrowstyle="->", color=GREY, linewidth=0.7,
                                     shrinkA=1, shrinkB=1))
    ax1.plot([_mid], [Y + 0.20], marker="o", markersize=8, color=ACCENT, zorder=3)
    ax1.plot([_mid, _mid], [Y - 0.30, Y + 0.20], color=ACCENT, linewidth=1.0,
             linestyle=(0, (2, 2)))

ax1.text(EDGES[0], Y - 0.46, "class edges", fontsize=9, color=GREY,
         ha="left", va="top")
ax1.annotate("mid-interval value",
             xy=((EDGES[0] + EDGES[1]) / 2, Y - 0.32),
             xytext=(4.4, Y - 1.30), fontsize=9.5, color=ACCENT, ha="left",
             arrowprops=dict(arrowstyle="->", color=ACCENT, linewidth=1.0))

ax1.text(0.0, 3.30, "the actual values in a class are not known",
         fontsize=9.5, color=GREY)
ax1.text(0.0, 2.80, "each one is replaced by the middle of its class",
         fontsize=9.5, color=ACCENT)

ax1.text(-0.6, -1.65, "so the mean found from a grouped table is an estimate",
         fontsize=9.5, color=INK, va="bottom")

# ══════════════════════════════════════════════════════════
# (b) 定数を足す・かける
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) Adding and multiplying by a constant", fontsize=11,
              color=INK, loc="left", pad=10)
ax2.set_xlim(-0.8, 15.2)
ax2.set_ylim(-1.9, 4.8)
ax2.axis("off")

BASE = np.array([1.0, 2.0, 2.6, 3.6])
ROWS = [
    (3.65, BASE, ACCENT, "original", None),
    (2.00, BASE + 3.2, GREEN, "add a constant", "the gaps are unchanged, so $\\sigma$ is unchanged"),
    (0.35, BASE * 2.2, WARM, "multiply by a constant", "the gaps are scaled, so $\\sigma$ is multiplied by $|a|$"),
]
for _y, _pts, _col, _lab, _note in ROWS:
    ax2.plot([0.2, 14.6], [_y, _y], color="#e5e7eb", linewidth=1.0, zorder=0)
    ax2.scatter(_pts, [_y] * len(_pts), s=42, color=_col, zorder=3)
    _mean = float(np.mean(_pts))
    ax2.plot([_mean, _mean], [_y - 0.30, _y + 0.30], color=_col, linewidth=1.6)
    ax2.text(_mean, _y + 0.38, "mean", fontsize=8.5, color=_col, ha="center")
    ax2.text(0.2, _y - 0.62, _lab, fontsize=9.5, color=_col)
    if _note:
        ax2.text(0.2, _y - 1.02, _note, fontsize=9, color=GREY)
    # となりあう 2 点のあいだの幅を示す
    ax2.annotate("", xy=(_pts[1], _y - 0.16), xytext=(_pts[0], _y - 0.16),
                 arrowprops=dict(arrowstyle="<->", color=_col, linewidth=0.9))

ax2.text(-0.8, -1.65, "the mean moves both times; the spread moves only when "
         "we multiply", fontsize=9.5, color=INK, va="bottom")

fig.tight_layout(w_pad=2.4)
path = os.path.join(OUT, "aasl-4-3-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
