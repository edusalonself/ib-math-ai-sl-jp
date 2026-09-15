"""AA SL 2.9 の図をつくる。

    python3 figs/aa-sl/make_aasl_2_9.py            … SVG だけ
    FIG_PNG=1 python3 figs/aa-sl/make_aasl_2_9.py  … 目視用の PNG も

出力: aa-sl/02-functions/img/aasl-2-9-idea.svg

(a) 指数関数 y = a^x。a > 1 は増える、0 < a < 1 は減る。どれも (0, 1) を通る。
(b) y = e^x と y = ln x は、y = x について互いの折り返し。

matplotlib の mathtext には次の制限があります（tools/README.md）。
  * \\begin{pmatrix} は読めない → \\binom を使う
  * \\lvert \\rvert は読めない → | を使う
  * 日本語のグリフがない → ラベルはすべて英語

★ 図に例題・演習の答えを書かないこと。
★ PNG は目視用です。確認が終わったら消してください。
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "aa-sl", "02-functions", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"
ACCENT = "#0b5cad"
GREY = "#6b7280"
WARM = "#b45309"
GREEN = "#15803d"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.8))

# ══════════════════════════════════════════════════════════
# (a) y = a^x
# ══════════════════════════════════════════════════════════
ax1.set_title("(a) Exponential functions", fontsize=11, color=INK,
              loc="left", pad=10)
ax1.set_xlim(-3.4, 3.4)
ax1.set_ylim(-1.6, 7.4)
ax1.axis("off")

ax1.annotate("", xy=(3.1, 0), xytext=(-3.1, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax1.annotate("", xy=(0, 7.1), xytext=(0, -1.3),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax1.text(3.2, -0.45, "$x$", fontsize=11, color=GREY, ha="center")
ax1.text(-0.34, 7.2, "$y$", fontsize=11, color=GREY, va="center")

t = np.linspace(-3.0, 3.0, 300)
ax1.plot(t, 2.0 ** t, color=ACCENT, linewidth=2.2)
ax1.plot(t, np.exp(t), color=GREEN, linewidth=2.0, linestyle=(0, (5, 3)))
ax1.plot(t, 0.5 ** t, color=WARM, linewidth=2.2)
ax1.plot([-3.1, 3.1], [0, 0], color=GREY, linewidth=1.1)

ax1.plot([0], [1], marker="o", markersize=6, color=INK, zorder=3)
ax1.text(0.16, 1.35, "$(0,\\ 1)$", fontsize=10, color=INK)

ax1.text(2.05, 5.2, "$y = 2^{x}$", fontsize=11, color=ACCENT)
ax1.text(1.05, 5.9, "$y = e^{x}$", fontsize=11, color=GREEN)
ax1.text(-3.3, 2.4, "$y = \\left(\\frac{1}{2}\\right)^{x}$", fontsize=11,
         color=WARM)
ax1.text(-3.2, -1.5, "asymptote $y = 0$; the value is never $0$ or negative",
         fontsize=9.5, color=INK, va="bottom")

# ══════════════════════════════════════════════════════════
# (b) y = e^x と y = ln x
# ══════════════════════════════════════════════════════════
ax2.set_title("(b) Inverse of each other", fontsize=11, color=INK,
              loc="left", pad=10)
ax2.set_xlim(-3.4, 5.4)
ax2.set_ylim(-3.4, 5.4)
ax2.set_aspect("equal")
ax2.axis("off")

ax2.annotate("", xy=(5.0, 0), xytext=(-3.1, 0),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.annotate("", xy=(0, 5.0), xytext=(0, -3.1),
             arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.1))
ax2.text(5.1, -0.5, "$x$", fontsize=11, color=GREY, ha="center")
ax2.text(-0.45, 5.1, "$y$", fontsize=11, color=GREY, va="center")

u = np.linspace(-3.0, 1.6, 300)
ax2.plot(u, np.exp(u), color=ACCENT, linewidth=2.2)
w = np.linspace(0.05, 5.0, 300)
ax2.plot(w, np.log(w), color=WARM, linewidth=2.2)
dd = np.linspace(-3.0, 5.0, 2)
ax2.plot(dd, dd, color=GREEN, linewidth=1.2, linestyle=(0, (5, 4)))

ax2.plot([0], [1], marker="o", markersize=5.5, color=INK, zorder=3)
ax2.plot([1], [0], marker="o", markersize=5.5, color=INK, zorder=3)
ax2.text(-1.55, 1.25, "$(0,\\ 1)$", fontsize=10, color=INK)
ax2.text(1.15, -0.85, "$(1,\\ 0)$", fontsize=10, color=INK)

ax2.text(1.7, 4.6, "$y = e^{x}$", fontsize=11, color=ACCENT)
ax2.text(3.6, 1.6, "$y = \\ln x$", fontsize=11, color=WARM)
ax2.text(3.75, 4.55, "$y = x$", fontsize=10, color=GREEN)
ax2.text(-3.3, -3.3, "each is the reflection of the other in $y = x$",
         fontsize=9.5, color=INK, va="bottom")

fig.tight_layout(w_pad=2.2)
path = os.path.join(OUT, "aasl-2-9-idea.svg")
fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
print("wrote", os.path.normpath(path))

if os.environ.get("FIG_PNG"):
    png = path[:-4] + ".png"
    fig.savefig(png, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.path.normpath(png))
