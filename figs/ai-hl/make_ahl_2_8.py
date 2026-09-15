"""AHL 2.8（グラフの変換）の図を作る。ラベルは英語。
   出力先: ai-hl/02-functions/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_2_8.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
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
    ax.axhline(0, color=GREY, lw=1.2)
    ax.axvline(0, color=GREY, lw=1.2)


# 2 つのこぶを持つ非対称な関数。式は本文に出さず、y = f(x) とだけ呼ぶ。
def f(x):
    return 3.0 * np.exp(-(x - 1.0) ** 2) + 1.5 * np.exp(-4.0 * (x - 3.2) ** 2)


# ══════════ 4 つの基本変換（1 枚ずつ）══════════
XS = np.linspace(-4.5, 7.0, 900)
BASE = dict(color=GREY, lw=2.0, ls="--", label="$y = f(x)$")


def frame(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xlabel("$x$")
    tidy(ax)


# ── translation
fig, ax = plt.subplots(figsize=(6.4, 4.6))
ax.plot(XS, f(XS), **BASE)
ax.plot(XS, f(XS - 2) + 1, color=LINE, lw=2.8, label="$y = f(x-2)+1$")
ax.add_patch(FancyArrowPatch((1.0, 3.0), (3.0, 4.0), arrowstyle="-|>",
                             mutation_scale=15, color=ACC, lw=2.0,
                             connectionstyle="arc3,rad=0.18", zorder=6))
ax.plot([1.0, 3.0], [3.0, 4.0], "o", color=ACC, ms=7, zorder=7)
ax.text(2.05, 4.35, "right $2$, up $1$", fontsize=11.5, color=ACC,
        ha="center", va="bottom", bbox=BOX, zorder=8)
frame(ax, (-2.6, 6.6), (-0.7, 5.6))
ax.legend(fontsize=10.5, frameon=False, loc="upper left")
ax.set_title("translation  $\\binom{2}{1}$", fontsize=12, color=INK, pad=9)
fig.tight_layout()
save(fig, "ahl-2-8-translation.svg")

# ── reflections
fig, ax = plt.subplots(figsize=(6.4, 4.6))
ax.plot(XS, f(XS), **BASE)
ax.plot(XS, -f(XS), color=ACC, lw=2.8, label="$y = -f(x)$")
ax.plot(XS, f(-XS), color=GREEN, lw=2.8, ls=":", label="$y = f(-x)$")
ax.text(1.0, -3.55, "in the $x$ axis", fontsize=11, color=ACC, ha="center",
        va="top", bbox=BOX, zorder=8)
ax.text(-4.7, 3.9, "in the $y$ axis", fontsize=11, color=GREEN, ha="left",
        va="top", bbox=BOX, zorder=8)
frame(ax, (-5.0, 5.0), (-4.4, 4.5))
ax.legend(fontsize=10.5, frameon=False, loc="lower right")
ax.set_title("reflections", fontsize=12, color=INK, pad=9)
fig.tight_layout()
save(fig, "ahl-2-8-reflection.svg")

# ── vertical stretch
fig, ax = plt.subplots(figsize=(6.4, 4.6))
ax.plot(XS, f(XS), **BASE)
ax.plot(XS, 2 * f(XS), color=LINE, lw=2.8, label="$y = 2f(x)$")
ax.add_patch(FancyArrowPatch((1.0, 3.0), (1.0, 6.0), arrowstyle="-|>",
                             mutation_scale=15, color=ACC, lw=2.0, zorder=6))
ax.text(1.25, 4.5, "$\\times 2$", fontsize=12.5, color=ACC, ha="left",
        va="center")
ax.plot(XS[(XS > -2.4) & (XS < 6.4)], np.zeros_like(XS[(XS > -2.4) & (XS < 6.4)]),
        color=GOLD, lw=3.0, zorder=5)
ax.text(4.6, -0.55, "the $x$ axis does not move", fontsize=10.5, color=GOLD,
        ha="right", va="top")
frame(ax, (-2.6, 6.6), (-1.4, 7.0))
ax.legend(fontsize=10.5, frameon=False, loc="upper left")
ax.set_title("vertical stretch, scale factor $2$", fontsize=12,
             color=INK, pad=9)
fig.tight_layout()
save(fig, "ahl-2-8-vstretch.svg")

# ── horizontal stretch
fig, ax = plt.subplots(figsize=(6.4, 4.6))
ax.plot(XS, f(XS), **BASE)
ax.plot(XS, f(2 * XS), color=LINE, lw=2.8, label="$y = f(2x)$")
ax.add_patch(FancyArrowPatch((1.0, 3.15), (0.5, 3.15), arrowstyle="-|>",
                             mutation_scale=15, color=ACC, lw=2.0, zorder=6))
ax.text(1.15, 3.55, "$x$ halved", fontsize=11.5, color=ACC, ha="left",
        va="bottom", bbox=BOX, zorder=8)
ax.text(2.9, 2.35, "$y = f(2x)$ is a stretch\nof scale factor $\\frac{1}{2}$,\nnot $2$",
        fontsize=11, color=ACC, ha="left", va="top", bbox=BOX, zorder=8)
ax.plot([0, 0], [-0.35, 4.3], color=GOLD, lw=2.4, zorder=5)
ax.text(-3.3, -0.5, "the $y$ axis does not move", fontsize=10.5, color=GOLD,
        ha="left", va="center")
frame(ax, (-3.5, 6.8), (-1.0, 4.7))
ax.legend(fontsize=10.5, frameon=False, loc="upper left")
ax.set_title("horizontal stretch, scale factor $\\frac{1}{2}$",
             fontsize=12, color=INK, pad=9)
fig.tight_layout()
save(fig, "ahl-2-8-hstretch.svg")


# ══════════ 順序 / 2 つの stretch（1 枚ずつ）══════════
fig, ax = plt.subplots(figsize=(6.6, 4.9))
X = np.linspace(-2.4, 2.4, 500)
ax.plot(X, X ** 2, color=GREY, lw=2.0, ls="--", label="$y = x^{2}$")
ax.plot(X, 3 * X ** 2 + 2, color=GREEN, lw=2.8,
        label="stretch, then translate:  $y = 3x^{2}+2$")
ax.plot(X, 3 * X ** 2 + 6, color=ACC, lw=2.8, ls="-.",
        label="translate, then stretch:  $y = 3x^{2}+6$")
# 縦の差は x によらず 4 —— 2 か所で示す
for _x in (0.0, 1.5):
    _lo, _hi = 3 * _x ** 2 + 2, 3 * _x ** 2 + 6
    ax.plot([_x, _x], [_lo, _hi], "o", color=INK, ms=6, zorder=7)
    ax.annotate("", xy=(_x, _hi), xytext=(_x, _lo),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.6))
    ax.text(_x + 0.16, (_lo + _hi) / 2, "$4$", fontsize=11.5, color=INK,
            ha="left", va="center", bbox=BOX, zorder=8)
ax.text(2.4, 0.4, "vertical gap $= 4$ at every $x$",
        fontsize=10.5, color=INK, ha="right", va="bottom", bbox=BOX, zorder=8)
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-1.2, 16.5)
ax.set_xlabel("$x$")
ax.legend(fontsize=9.8, frameon=False, loc="upper center")
ax.set_title("the same two transformations, two orders",
             fontsize=12, color=INK, pad=9)
tidy(ax)
fig.tight_layout()
save(fig, "ahl-2-8-order.svg")

fig, ax = plt.subplots(figsize=(6.6, 4.9))
T = np.linspace(-0.35, 2 * np.pi + 0.35, 700)
ax.plot(T, np.sin(T), color=GREY, lw=2.0, ls="--", label="$y = \\sin x$")
ax.plot(T, 4 * np.sin(2 * T), color=LINE, lw=2.8, label="$y = 4\\sin 2x$")
ax.annotate("", xy=(np.pi / 4, 4), xytext=(np.pi / 4, 0),
            arrowprops=dict(arrowstyle="<->", color=ACC, lw=1.6))
ax.text(np.pi / 4 + 0.12, 2.0, "amplitude $4$", fontsize=11, color=ACC,
        ha="left", va="center", bbox=BOX, zorder=8)
ax.annotate("", xy=(np.pi, -4.9), xytext=(0, -4.9),
            arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.6))
ax.text(np.pi / 2, -5.15, "period $\\pi$", fontsize=11, color=GREEN,
        ha="center", va="top", bbox=BOX, zorder=8)
ax.set_xlim(-0.45, 2 * np.pi + 0.45)
ax.set_ylim(-6.6, 5.6)
ax.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi])
ax.set_xticklabels(["$0$", "$\\frac{\\pi}{2}$", "$\\pi$",
                    "$\\frac{3\\pi}{2}$", "$2\\pi$"])
ax.set_xlabel("$x$")
ax.legend(fontsize=10.5, frameon=False, loc="upper right")
ax.set_title("two stretches at once", fontsize=12, color=INK, pad=9)
tidy(ax)

fig.tight_layout()
save(fig, "ahl-2-8-sine.svg")

print("figures written to", os.path.normpath(OUT))
