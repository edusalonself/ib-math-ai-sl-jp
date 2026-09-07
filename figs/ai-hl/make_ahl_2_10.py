"""AHL 2.10（log-log と semi-log）の図を作る。ラベルは英語。
   出力先: ai-hl/02-functions/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_2_10.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from _graph import INK, GRID, LINE, ACC, GREEN, GREY, GOLD, BOX

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "02-functions", "img")
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True)
    plt.close(fig)
    print("wrote", name)


def tidy(ax):
    ax.grid(True, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("bottom", "left"):
        ax.spines[sp].set_color(GREY)


# ══════════ fig 1: どちらが直線になるか ══════════
fig, axs = plt.subplots(2, 2, figsize=(11.4, 8.2))

XE = np.arange(0, 5.0)
YE = 5 * 2.0 ** XE                       # 指数
XP = np.array([1.0, 2, 3, 4, 5])
YP = 2 * XP ** 3                         # 累乗

# ── (a) 指数のデータ、ふつうの軸
ax = axs[0][0]
XS = np.linspace(0, 4.3, 300)
ax.plot(XS, 5 * 2.0 ** XS, color=GREY, lw=1.8, ls="--")
ax.plot(XE, YE, "o", color=LINE, ms=9, zorder=6)
ax.set_xlim(-0.35, 4.5)
ax.set_ylim(-8, 95)
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
ax.text(0.15, 84, "$y = 5 \\times 2^{x}$", fontsize=12.5, color=LINE,
        ha="left", va="top", bbox=BOX, zorder=8)
ax.set_title("(a)  exponential data: a curve", fontsize=12, color=INK, pad=9)
tidy(ax)

# ── (b) 指数のデータ、semi-log
ax = axs[0][1]
LY = np.log10(YE)
ax.plot([-0.3, 4.4], [np.log10(5) + np.log10(2) * (-0.3),
                      np.log10(5) + np.log10(2) * 4.4],
        color=GREEN, lw=2.4)
ax.plot(XE, LY, "o", color=LINE, ms=9, zorder=6)
ax.annotate("", xy=(3, LY[2]), xytext=(2, LY[2]),
            arrowprops=dict(arrowstyle="->", color=ACC, lw=1.5))
ax.annotate("", xy=(3, LY[3]), xytext=(3, LY[2]),
            arrowprops=dict(arrowstyle="->", color=ACC, lw=1.5))
ax.text(3.12, (LY[2] + LY[3]) / 2, "gradient\n$= \\log 2 = 0.301$", fontsize=11,
        color=ACC, ha="left", va="center", bbox=BOX, zorder=8)
ax.plot([0], [np.log10(5)], "o", color=GOLD, ms=9, zorder=7)
ax.text(0.16, np.log10(5) - 0.06, "intercept $= \\log 5 = 0.699$", fontsize=11,
        color=GOLD, ha="left", va="top", bbox=BOX, zorder=8)
ax.set_xlim(-0.35, 4.6)
ax.set_ylim(0.35, 2.15)
ax.set_xlabel("$x$")
ax.set_ylabel("$\\log y$")
ax.set_title("(b)  semi-log: a straight line", fontsize=12, color=INK, pad=9)
tidy(ax)

# ── (c) 累乗のデータ、ふつうの軸
ax = axs[1][0]
XS2 = np.linspace(0.6, 5.3, 300)
ax.plot(XS2, 2 * XS2 ** 3, color=GREY, lw=1.8, ls="--")
ax.plot(XP, YP, "o", color=LINE, ms=9, zorder=6)
ax.set_xlim(0.3, 5.6)
ax.set_ylim(-25, 300)
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
ax.text(0.6, 265, "$y = 2x^{3}$", fontsize=12.5, color=LINE, ha="left",
        va="top", bbox=BOX, zorder=8)
ax.set_title("(c)  power data: also a curve", fontsize=12, color=INK, pad=9)
tidy(ax)

# ── (d) 累乗のデータ、log-log
ax = axs[1][1]
LX, LYP = np.log10(XP), np.log10(YP)
ax.plot([-0.08, 0.78], [np.log10(2) + 3 * (-0.08), np.log10(2) + 3 * 0.78],
        color=GREEN, lw=2.4)
ax.plot(LX, LYP, "o", color=LINE, ms=9, zorder=6)
ax.annotate("", xy=(LX[3], LYP[1]), xytext=(LX[1], LYP[1]),
            arrowprops=dict(arrowstyle="->", color=ACC, lw=1.5))
ax.annotate("", xy=(LX[3], LYP[3]), xytext=(LX[3], LYP[1]),
            arrowprops=dict(arrowstyle="->", color=ACC, lw=1.5))
ax.text(0.625, (LYP[1] + LYP[3]) / 2,
        "gradient\n$= \\dfrac{0.903}{0.301} = 3$", fontsize=11,
        color=ACC, ha="left", va="center", bbox=BOX, zorder=8)
ax.plot([0], [np.log10(2)], "o", color=GOLD, ms=9, zorder=7)
ax.text(0.035, np.log10(2) - 0.05, "intercept $= \\log 2 = 0.301$",
        fontsize=11, color=GOLD, ha="left", va="top", bbox=BOX, zorder=8)
ax.set_xlim(-0.09, 0.94)
ax.set_ylim(-0.05, 2.75)
ax.set_xlabel("$\\log x$")
ax.set_ylabel("$\\log y$")
ax.set_title("(d)  log-log: a straight line", fontsize=12, color=INK, pad=9)
tidy(ax)

fig.tight_layout(h_pad=2.4, w_pad=2.6)
save(fig, "ahl-2-10-which.svg")


# ══════════ fig 2: 目盛りの取り方 ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.9))

M = np.arange(0, 6.0)
V = 50 * 8.0 ** M            # 50, 400, 3200, 25600, 204800, 1638400

# ── (a) ふつうの目盛り
ax = axs[0]
ax.plot(M, V, "-o", color=LINE, lw=2.4, ms=9)
for i in (0, 1, 2, 3):
    ax.annotate("", xy=(M[i], V[i]), xytext=(M[i] + 0.75, 430000),
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.0))
ax.text(0.55, 470000, "the first four months are\nflattened onto the axis",
        fontsize=11, color=GREY, ha="left", va="bottom", bbox=BOX, zorder=8)
ax.set_xlim(-0.35, 5.5)
ax.set_ylim(-90000, 1900000)
ax.set_yticks([0, 500000, 1000000, 1500000])
ax.set_yticklabels(["$0$", "$500\,000$", "$1\,000\,000$", "$1\,500\,000$"])
ax.set_xlabel("month")
ax.set_ylabel("visits")
ax.set_title("(a)  an ordinary scale", fontsize=12, color=INK, pad=9)
tidy(ax)

# ── (b) 対数目盛り
ax = axs[1]
ax.plot(M, V, "-o", color=LINE, lw=2.4, ms=9)
ax.set_yscale("log")
ax.set_yticks([10, 100, 1000, 10000, 100000, 1000000])
ax.set_yticklabels(["$10$", "$100$", "$1000$", "$10^{4}$", "$10^{5}$",
                    "$10^{6}$"])
ax.annotate("", xy=(4, V[3]), xytext=(3, V[3]),
            arrowprops=dict(arrowstyle="->", color=ACC, lw=1.5))
ax.annotate("", xy=(4, V[4]), xytext=(4, V[3]),
            arrowprops=dict(arrowstyle="->", color=ACC, lw=1.5))
ax.text(0.15, 190000, "the same step up every month:\n$\\times 8$, so $\\log 8 = 0.903$",
        fontsize=11, color=ACC, ha="left", va="center", bbox=BOX, zorder=8)
ax.set_xlim(-0.35, 5.5)
ax.set_ylim(20, 6e6)
ax.set_xlabel("month")
ax.set_ylabel("visits (log scale)")
ax.set_title("(b)  a logarithmic scale", fontsize=12, color=INK, pad=9)
ax.grid(True, which="both", color=GRID, lw=0.8)
ax.set_axisbelow(True)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
for sp in ("bottom", "left"):
    ax.spines[sp].set_color(GREY)

fig.tight_layout(w_pad=2.6)
save(fig, "ahl-2-10-scale.svg")

print("figures written to", os.path.normpath(OUT))
