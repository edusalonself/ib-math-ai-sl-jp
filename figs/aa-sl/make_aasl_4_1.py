"""AA SL 4.1 の図をつくる。

    python3 figs/aa-sl/make_aasl_4_1.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_4_1.py  … 目視用の PNG も

出力: aa-sl/04-statistics-and-probability/img/aasl-4-1-idea.svg

(a) population と sample の関係。
(b) 外れ値の境目（Q1 - 1.5 IQR と Q3 + 1.5 IQR）。
★ (a) の標本は散らばらせること。かたまりで描くと convenience sampling の絵になる。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に例題・演習の答えを書かないこと（(b) は記号だけ）。
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
PALE = "#c7d7e8"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 4.4))

# ══════════════════════════════════════════════════════════
# (a) population と sample
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Population and sample", fontsize=11, color=INK,
              loc="left", pad=10)
ax1.set_xlim(-0.4, 10.4)
ax1.set_ylim(-1.5, 7.9)
ax1.axis("off")

rng = np.random.default_rng(7)
_pts = []
for _r in range(6):
    for _c in range(11):
        _pts.append((0.35 + _c * 0.86 + rng.uniform(-0.12, 0.12),
                     1.55 + _r * 0.72 + rng.uniform(-0.10, 0.10)))
_pts = np.array(_pts)
# ★ 標本は散らばって選ばれる（かたまりで取ると、それ自体が convenience の絵になる）
_inside = sorted(rng.choice(len(_pts), 13, replace=False).tolist())
_outside = [i for i in range(len(_pts)) if i not in _inside]

ax1.add_patch(plt.Rectangle((-0.05, 1.05), 9.9, 4.9, fill=False,
                            edgecolor=GREY, linewidth=1.2))
ax1.scatter(_pts[_outside, 0], _pts[_outside, 1], s=17, color=PALE, zorder=2)
ax1.scatter(_pts[_inside, 0], _pts[_inside, 1], s=52, color=ACCENT, zorder=3,
            marker="o", edgecolors="white", linewidths=0.8)

ax1.text(0.05, 6.15, "population: everyone we want to know about",
         fontsize=10, color=INK)
_top = max(_inside, key=lambda i: (_pts[i][1], _pts[i][0]))
ax1.annotate("sample: spread over the whole population",
             xy=(_pts[_top, 0], _pts[_top, 1] + 0.16),
             xytext=(1.7, 6.95), fontsize=10, color=ACCENT, ha="left",
             arrowprops=dict(arrowstyle="->", color=ACCENT, linewidth=1.1,
                             shrinkB=2))

ax1.text(0.05, 0.62, "measure the sample", fontsize=9.5, color=WARM)
ax1.annotate("", xy=(6.5, 0.55), xytext=(4.4, 0.55),
             arrowprops=dict(arrowstyle="->", color=WARM, linewidth=1.5))
ax1.text(6.7, 0.62, "say something about the population",
         fontsize=9.5, color=WARM)

ax1.text(-0.4, -1.45, "if the sample is chosen badly, the answer about the "
         "population is wrong", fontsize=9.5, color=INK, va="bottom")

# ══════════════════════════════════════════════════════════
# (b) 外れ値の境目
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) The two outlier boundaries", fontsize=11, color=INK,
              loc="left", pad=10)
ax2.set_xlim(-0.6, 13.6)
ax2.set_ylim(-1.5, 4.2)
ax2.axis("off")

Q1, Q3 = 4.6, 7.0
ax2.plot([0.4, 13.0], [1.6, 1.6], color=GREY, linewidth=1.0)

# 箱
ax2.add_patch(plt.Rectangle((Q1, 1.12), Q3 - Q1, 0.96, fill=True,
                            facecolor="#e8f0f8", edgecolor=ACCENT,
                            linewidth=1.6, zorder=2))
ax2.text((Q1 + Q3) / 2, 2.32, "IQR", fontsize=10.5, color=ACCENT, ha="center")
ax2.annotate("", xy=(Q3, 2.18), xytext=(Q1, 2.18),
             arrowprops=dict(arrowstyle="<->", color=ACCENT, linewidth=1.2))
ax2.text(Q1, 0.72, "$Q_1$", fontsize=10.5, color=ACCENT, ha="center")
ax2.text(Q3, 0.72, "$Q_3$", fontsize=10.5, color=ACCENT, ha="center")

# 境目
LO, HI = Q1 - 1.5 * (Q3 - Q1), Q3 + 1.5 * (Q3 - Q1)
for _p in (LO, HI):
    ax2.plot([_p, _p], [1.0, 2.2], color=WARM, linewidth=1.6,
             linestyle=(0, (5, 3)))
ax2.text(LO, 0.72, "$Q_1 - 1.5\\,IQR$", fontsize=9.5, color=WARM, ha="center")
ax2.text(HI, 0.72, "$Q_3 + 1.5\\,IQR$", fontsize=9.5, color=WARM, ha="center")

ax2.annotate("", xy=(LO, 3.05), xytext=(Q1, 3.05),
             arrowprops=dict(arrowstyle="<->", color=WARM, linewidth=1.1))
ax2.annotate("", xy=(HI, 3.05), xytext=(Q3, 3.05),
             arrowprops=dict(arrowstyle="<->", color=WARM, linewidth=1.1))
ax2.text((LO + Q1) / 2, 3.22, "$1.5\\,IQR$", fontsize=9.5, color=WARM,
         ha="center")
ax2.text((Q3 + HI) / 2, 3.22, "$1.5\\,IQR$", fontsize=9.5, color=WARM,
         ha="center")

# 外れ値の印
ax2.plot([12.2], [1.6], marker="x", markersize=9, markeredgewidth=2.0,
         color=INK, zorder=4)
ax2.text(12.2, 1.95, "outlier", fontsize=9.5, color=INK, ha="center")
ax2.text(12.2, 0.40, "marked with\na cross", fontsize=9.0, color=GREY,
         ha="center", va="top")

ax2.text(-0.6, -1.45, "a value beyond a boundary is an outlier; the "
         "boundary itself is not", fontsize=9.5, color=INK, va="bottom")

fig.tight_layout(w_pad=2.2)
path = os.path.join(OUT, "aasl-4-1-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
