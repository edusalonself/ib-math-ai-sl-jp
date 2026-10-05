"""AA SL 4.12 の図をつくる。

    python3 figs/aa-sl/make_aasl_4_12.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_4_12.py  … 目視用の PNG も

出力: aa-sl/04-statistics-and-probability/img/aasl-4-12-idea-a.svg
      aa-sl/04-statistics-and-probability/img/aasl-4-12-idea-b.svg

(a) z 値は「平均から標準偏差いくつぶん」を数にしたもの。
    横軸に x の目もりと z の目もりを並べて置く。
(b) mu と sigma が未知のとき、2 つの面積から 2 つの z が出て、
    x = mu + z*sigma の形の式が 2 本できる。

★ 数値は入れません。文字だけです（例題・演習と重ならないように）。

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
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "04-statistics-and-probability",
                   "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
FILL = "#cfe0f2"
SHADE = "#f6d9b0"


def bell(t):
    return np.exp(-0.5 * t * t) / np.sqrt(2 * np.pi)


fig1, ax1 = plt.subplots(figsize=(5.8, 4.9))
fig2, ax2 = plt.subplots(figsize=(5.8, 4.9))
# ══════════════════════════════════════════════════════════
# (a) 同じ曲線を、2 通りの目もりで読む
# ══════════════════════════════════════════════════════════
ax1.set_title("The same curve read on two scales", fontsize=11,
              color=INK, loc="left", pad=12)
T = np.linspace(-3.6, 3.6, 400)
Y = bell(T)
ax1.plot(T, Y, color=ACCENT, linewidth=1.8)
ax1.fill_between(T, 0, Y, color=FILL, alpha=0.55)
ax1.set_xlim(-4.1, 4.1)
ax1.set_ylim(-0.235, 0.50)
ax1.axis("off")
ax1.plot([-3.9, 3.9], [0, 0], color=GREY, linewidth=1.0)

for _t in (-2, -1, 0, 1, 2):
    ax1.plot([_t, _t], [0, -0.012], color=GREY, linewidth=1.0)
    ax1.plot([_t, _t], [0, bell(_t)], color=GREY, linewidth=0.8,
             linestyle=(0, (3, 3)))

XLAB = {-2: r"$\mu - 2\sigma$", -1: r"$\mu - \sigma$", 0: r"$\mu$",
        1: r"$\mu + \sigma$", 2: r"$\mu + 2\sigma$"}
for _t, _s in XLAB.items():
    ax1.text(_t, -0.048, _s, fontsize=9.5, color=INK, ha="center", va="top")
for _t, _s in {-2: "$-2$", -1: "$-1$", 0: "$0$", 1: "$1$", 2: "$2$"}.items():
    ax1.text(_t, -0.118, _s, fontsize=9.5, color=WARM, ha="center", va="top")

ax1.text(-3.95, -0.048, "$x$", fontsize=10, color=INK, ha="left", va="top")
ax1.text(-3.95, -0.118, "$z$", fontsize=10, color=WARM, ha="left", va="top")

ax1.text(0.0, 0.435, r"$z = \frac{x - \mu}{\sigma}$", fontsize=12,
         color=WARM, ha="center", va="center")
ax1.text(0.0, -0.185, r"$x = \mu + z\sigma$ goes the other way",
         fontsize=10, color=ACCENT, ha="center", va="center")

# ══════════════════════════════════════════════════════════
# (b) 2 つの面積 → 2 つの z → 2 本の式
# ══════════════════════════════════════════════════════════
ax2.set_title("Two known areas give two equations", fontsize=11,
              color=INK, loc="left", pad=12)
ax2.plot(T, Y, color=ACCENT, linewidth=1.8)
LO, HI = -1.15, 0.95
ML = T <= LO
MR = T >= HI
ax2.fill_between(T[ML], 0, Y[ML], color=SHADE)
ax2.fill_between(T[MR], 0, Y[MR], color=SHADE)
ax2.set_xlim(-4.1, 4.1)
ax2.set_ylim(-0.30, 0.50)
ax2.axis("off")
ax2.plot([-3.9, 3.9], [0, 0], color=GREY, linewidth=1.0)

for _t, _s in ((LO, "$a$"), (HI, "$b$")):
    ax2.plot([_t, _t], [0, bell(_t)], color=WARM, linewidth=1.2)
    ax2.text(_t, -0.045, _s, fontsize=10.5, color=WARM, ha="center", va="top")

ax2.annotate("", xy=(-1.95, 0.028), xytext=(-2.95, 0.135),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.text(-3.0, 0.155, "given area", fontsize=9, color=GREY, ha="center")
ax2.annotate("", xy=(1.75, 0.032), xytext=(2.75, 0.135),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.text(2.8, 0.155, "given area", fontsize=9, color=GREY, ha="center")

ax2.text(0.0, -0.135, r"$a = \mu + z_1\sigma$    and    $b = \mu + z_2\sigma$",
         fontsize=11, color=ACCENT, ha="center", va="center")
ax2.text(0.0, -0.245, "two equations, two unknowns", fontsize=9.5,
         color=INK, ha="center", va="center")

for _fig, _name in ((fig1, "aasl-4-12-idea-a.svg"), (fig2, "aasl-4-12-idea-b.svg")):
    _fig.tight_layout()
    _p = os.path.join(OUT, _name)
    _fig.savefig(_p, format="svg", bbox_inches="tight", transparent=True)
    print("wrote", os.path.normpath(_p))
    if os.environ.get("FIG_PNG"):
        _q = _p[:-4] + ".png"
        _fig.savefig(_q, format="png", dpi=150, bbox_inches="tight",
                     facecolor="white")
        print("wrote", os.path.normpath(_q))
