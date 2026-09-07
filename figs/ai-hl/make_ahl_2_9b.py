"""AHL 2.9b（ロジスティックモデル・区分モデル）の図を作る。ラベルは英語。
   出力先: ai-hl/02-functions/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_2_9b.py
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


def logistic(t, L=2000.0, C=9.0, k=0.3):
    return L / (1 + C * np.exp(-k * t))


# ══════════ fig 1: logistic ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.9))

# ── (a) L, C, k の読み方
ax = axs[0]
T = np.linspace(0, 30, 700)
ax.plot(T, logistic(T), color=LINE, lw=2.8,
        label="$P = \\dfrac{2000}{1+9e^{-0.3t}}$")
ax.axhline(2000, color=GOLD, lw=2.0, ls="--")
ax.text(29.6, 2000, "carrying capacity  $L = 2000$", fontsize=11, color=GOLD,
        ha="right", va="bottom")
ax.axhline(0, color=GREY, lw=1.2)
th = np.log(9) / 0.3
ax.plot([0], [200], "o", color=ACC, ms=8, zorder=6)
ax.plot([th], [1000], "o", color=GREEN, ms=9, zorder=6)
ax.plot([th, th], [0, 1000], color=GREY, lw=1.1, ls=":", zorder=3)
ax.plot([0, th], [1000, 1000], color=GREY, lw=1.1, ls=":", zorder=3)
ax.annotate("$P(0) = \\dfrac{L}{1+C} = 200$", xy=(0, 200), xytext=(3.2, 430),
            fontsize=11, color=ACC, ha="left", va="center", bbox=BOX, zorder=8,
            arrowprops=dict(arrowstyle="->", color=ACC, lw=1.4,
                            shrinkA=2, shrinkB=5))
ax.annotate("steepest at $\\dfrac{L}{2} = 1000$,\nhere $t = 7.32$",
            xy=(th, 1000), xytext=(11.5, 780), fontsize=11, color=GREEN,
            ha="left", va="center", bbox=BOX, zorder=8,
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.4,
                            shrinkA=2, shrinkB=6))
ax.set_xlim(-1.2, 30.5)
ax.set_ylim(-120, 2320)
ax.set_xlabel("$t$")
ax.legend(fontsize=11, frameon=False, loc="center right")
ax.set_title("(a)  reading $L$, $C$ and $k$", fontsize=12, color=INK, pad=9)
tidy(ax)

# ── (b) logistic と exponential のちがい
ax = axs[1]
T2 = np.linspace(0, 12, 600)
ax.plot(T2, logistic(T2), color=LINE, lw=2.8, label="logistic")
ax.plot(T2, 200 * np.exp(0.3 * T2), color=ACC, lw=2.8, ls="-.",
        label="exponential $200e^{0.3t}$")
ax.axhline(2000, color=GOLD, lw=1.8, ls="--")
ax.text(0.2, 2080, "$L = 2000$", fontsize=11, color=GOLD, ha="left",
        va="bottom")
ax.annotate("the same at first", xy=(2.0, logistic(2.0)), xytext=(0.3, 1450),
            fontsize=11, color=INK, ha="left", va="center", bbox=BOX, zorder=8,
            arrowprops=dict(arrowstyle="->", color=INK, lw=1.4,
                            shrinkA=2, shrinkB=6))
ax.annotate("the logistic bends over;\nthe exponential does not",
            xy=(9.5, logistic(9.5)), xytext=(4.6, 700), fontsize=11,
            color=LINE, ha="left", va="center", bbox=BOX, zorder=8,
            arrowprops=dict(arrowstyle="->", color=LINE, lw=1.4,
                            shrinkA=2, shrinkB=6))
ax.axhline(0, color=GREY, lw=1.2)
ax.set_xlim(-0.5, 12.5)
ax.set_ylim(-160, 3400)
ax.set_xlabel("$t$")
ax.legend(fontsize=11, frameon=False, loc="upper left")
ax.set_title("(b)  a ceiling, or no ceiling", fontsize=12, color=INK, pad=9)
tidy(ax)

fig.tight_layout(w_pad=2.4)
save(fig, "ahl-2-9b-logistic.svg")


# ══════════ fig 2: piecewise ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.9))

# ── (a) continuity: a を選ぶ
ax = axs[0]
X1 = np.linspace(0, 2, 200)   # 区間は 0 <= x < 2。端の x=2 は白丸で示す
ax.plot(X1, 1 + X1, color=LINE, lw=2.8, label="$y = 1+x$,  $0 \\leq x < 2$")
X2 = np.linspace(2, 6, 300)
ax.plot(X2, X2 ** 2 / 4 + X2, color=GREEN, lw=2.8,
        label="$y = \\frac{1}{4}x^{2}+x$,  $x \\geq 2$")
X3 = np.linspace(2, 3.5, 200)
ax.plot(X3, X3 ** 2 + X3, color=ACC, lw=2.6, ls="-.",
        label="$y = x^{2}+x$  (wrong $a$)")
ax.plot([2], [3], "o", mfc="white", mec=LINE, mew=2.2, ms=13, zorder=6)
ax.plot([2], [3], "o", color=GREEN, ms=8, zorder=7)
ax.plot([2], [6], "o", color=ACC, ms=9, zorder=7)
ax.annotate("", xy=(2, 6), xytext=(2, 3),
            arrowprops=dict(arrowstyle="<->", color=ACC, lw=1.6))
ax.text(2.2, 4.5, "a jump of $3$", fontsize=11, color=ACC, ha="left",
        va="center", bbox=BOX, zorder=8)
ax.text(0.25, 12.4, "$a = \\dfrac{1}{4}$ makes the two pieces\nmeet at $(2,\\ 3)$",
        fontsize=11, color=GREEN, ha="left", va="top", bbox=BOX, zorder=8)
ax.axhline(0, color=GREY, lw=1.2)
ax.axvline(0, color=GREY, lw=1.2)
ax.set_xlim(-0.4, 6.4)
ax.set_ylim(-1.2, 16.5)
ax.set_xlabel("$x$")
ax.legend(fontsize=10, frameon=False, loc="lower right")
ax.set_title("(a)  choosing $a$ so the graph joins up", fontsize=12,
             color=INK, pad=9)
tidy(ax)

# ── (b) 文脈の piecewise
ax = axs[1]
Y1 = np.linspace(0, 5, 120)
ax.plot(Y1, np.full_like(Y1, 20), color=LINE, lw=3.0,
        label="$C = 20$,  $0 \\leq x \\leq 5$")
Y2 = np.linspace(5, 12, 200)
ax.plot(Y2, 20 + 3 * (Y2 - 5), color=GREEN, lw=3.0,
        label="$C = 20+3(x-5)$,  $x > 5$")
ax.plot([5], [20], "o", color=INK, ms=9, zorder=7)
ax.plot([3, 9], [20, 32], "o", color=ACC, ms=8, zorder=7)
ax.text(3, 17.6, "$C(3) = 20$", fontsize=11, color=ACC, ha="center", va="top")
ax.text(8.7, 33.4, "$C(9) = 32$", fontsize=11, color=ACC, ha="right",
        va="bottom")
ax.annotate("the pieces meet here,\nso the cost has no jump",
            xy=(5, 20), xytext=(5.6, 13.0), fontsize=11, color=INK,
            ha="left", va="center", bbox=BOX, zorder=8,
            arrowprops=dict(arrowstyle="->", color=INK, lw=1.4,
                            shrinkA=2, shrinkB=6))
ax.axhline(0, color=GREY, lw=1.2)
ax.axvline(0, color=GREY, lw=1.2)
ax.set_xlim(-0.6, 12.6)
ax.set_ylim(-2.5, 46)
ax.set_xlabel("$x$ (GB of data)")
ax.set_ylabel("cost")
ax.legend(fontsize=10.5, frameon=False, loc="upper left")
ax.set_title("(b)  a piecewise model in context", fontsize=12, color=INK,
             pad=9)
tidy(ax)

fig.tight_layout(w_pad=2.6)
save(fig, "ahl-2-9b-piecewise.svg")

print("figures written to", os.path.normpath(OUT))
