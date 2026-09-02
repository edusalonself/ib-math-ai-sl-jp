"""AHL 5.14 の図を作る。ラベルはすべて英語（日本語グリフは matplotlib に無い）。
   ★ matplotlib は markdown を解釈しないので、バッククォートは付けない。
   出力先: ai-hl/05-calculus/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_5_14.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from _graph import INK, GRID, LINE, ACC, GREEN, GREY, GOLD, BOX

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "05-calculus", "img")
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


# ══════════════ 1. ことば → 式 ══════════════
def box(ax, x, y, w, h, text, edge, fs=11.5, weight="normal", tcol=None):
    ax.add_patch(FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.10,rounding_size=0.14",
        linewidth=1.8, edgecolor=edge, facecolor="white", zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs,
            color=(tcol or INK), zorder=4, weight=weight, linespacing=1.55)


fig, ax = plt.subplots(figsize=(12.4, 6.4))
ax.set_xlim(0, 12.4)
ax.set_ylim(0.2, 7.0)
ax.axis("off")

ax.text(2.9, 6.75, "what the question SAYS", ha="center", fontsize=13,
        color=INK, weight="bold")
ax.text(9.3, 6.75, "what you WRITE", ha="center", fontsize=13,
        color=INK, weight="bold")

ROWS = [
    (5.55, "\"$P$ grows at a rate\nproportional to $P$\"",
     "$\\dfrac{dP}{dt} = kP$", LINE),
    (4.10, "\"$G$ grows at a rate\nproportional to $\\sqrt{G}$\"",
     "$\\dfrac{dG}{dt} = k\\sqrt{G}$", GREEN),
    (2.65, "\"$m$ DECREASES at a rate\nproportional to $m$\"",
     "$\\dfrac{dm}{dt} = -km$", ACC),
    (1.15, "\"$\\theta$ cools at a rate proportional\n"
           "to $(\\theta - 20)$, the excess over $20$\"",
     "$\\dfrac{d\\theta}{dt} = -k(\\theta - 20)$", GOLD),
]
for y, left, right, col in ROWS:
    box(ax, 2.9, y, 5.0, 1.14, left, col, fs=11.5)
    box(ax, 9.3, y, 3.4, 1.14, right, col, fs=13.5, weight="bold", tcol=col)
    ax.add_patch(FancyArrowPatch(
        (5.5, y), (7.5, y), arrowstyle="-|>", mutation_scale=16,
        linewidth=1.8, color=col, zorder=2))

fig.text(0.5, -0.01,
         "\"at a rate\" always means a DERIVATIVE.   "
         "\"proportional to ...\" means \"$= k \\times$ ...\".   "
         "\"decreases\" puts a MINUS sign in front of $k$.",
         fontsize=12, ha="center", color=INK)
fig.tight_layout()
save(fig, "ahl-5-14-words.svg")


# ══════════════ 2. general solution は曲線の族 ══════════════
fig, axs = plt.subplots(1, 2, figsize=(12.4, 4.4))

xs = np.linspace(0, 6, 400)

# left: the family
ax = axs[0]
for A, a in zip((0.4, 0.8, 1.4, 2.2, 3.2), (0.5,) * 5):
    ax.plot(xs, A * np.exp(0.35 * xs), color=GREY, lw=1.6, alpha=0.9,
            zorder=3)
ax.set_title("GENERAL solution   $y = Ae^{0.35x}$", fontsize=13, color=GREY,
             pad=10)
ax.text(0.25, 22.0, "every value of $A$\ngives a curve", fontsize=11.5,
        color=GREY, va="top")
ax.set_xlim(0, 6)
ax.set_ylim(0, 26)
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
tidy(ax)

# right: one curve picked out
ax = axs[1]
for A in (0.4, 0.8, 2.2, 3.2):
    ax.plot(xs, A * np.exp(0.35 * xs), color=GRID, lw=1.4, zorder=2)
ax.plot(xs, 1.4 * np.exp(0.35 * xs), color=ACC, lw=2.8, zorder=5)
ax.plot([0], [1.4], "o", color=ACC, ms=9, zorder=6)
ax.annotate("$y = 1.4$ when $x = 0$", xy=(0, 1.4), xytext=(1.3, 8.0),
            fontsize=11.5, color=ACC,
            arrowprops=dict(arrowstyle="->", color=ACC, lw=1.5),
            bbox=BOX, zorder=7)
ax.set_title("PARTICULAR solution   $y = 1.4e^{0.35x}$", fontsize=13,
             color=ACC, pad=10)
ax.set_xlim(0, 6)
ax.set_ylim(0, 26)
ax.set_xlabel("$x$")
tidy(ax)

fig.text(0.5, -0.05,
         "The general solution is a WHOLE FAMILY of curves — one for each "
         "value of $A$.   One extra piece of information "
         "(a starting value) picks out exactly one of them.",
         fontsize=12, ha="center", color=INK)
fig.tight_layout()
save(fig, "ahl-5-14-family.svg")


# ══════════════ 3. 3 つのモデルの解の形 ══════════════
fig, axs = plt.subplots(1, 3, figsize=(13.2, 4.0))

# (a) dG/dt = 2 sqrt(G), G = (t+2)^2
ax = axs[0]
t = np.linspace(0, 8, 400)
ax.plot(t, (t + 2) ** 2, color=GREEN, lw=2.6, zorder=4)
ax.plot([0], [4], "o", color=GREEN, ms=8, zorder=5)
ax.set_title("$\\dfrac{dG}{dt} = 2\\sqrt{G}$\n$G = (t+2)^2$", fontsize=12.5,
             color=GREEN, pad=10)
ax.set_xlim(0, 8)
ax.set_ylim(0, 105)
ax.set_xlabel("$t$")
tidy(ax)

# (b) dP/dt = 0.15 P
ax = axs[1]
t = np.linspace(0, 12, 400)
ax.plot(t, 500 * np.exp(0.15 * t), color=LINE, lw=2.6, zorder=4)
ax.plot([0], [500], "o", color=LINE, ms=8, zorder=5)
ax.set_title("$\\dfrac{dP}{dt} = 0.15P$\n$P = 500e^{0.15t}$", fontsize=12.5,
             color=LINE, pad=10)
ax.set_xlim(0, 12)
ax.set_ylim(0, 3200)
ax.set_xlabel("$t$")
tidy(ax)

# (c) cooling
ax = axs[2]
t = np.linspace(0, 30, 400)
K = math.log(1.5) / 5
ax.plot(t, 20 + 60 * np.exp(-K * t), color=GOLD, lw=2.6, zorder=4)
ax.axhline(20, color=ACC, lw=1.8, ls="--", zorder=3)
ax.text(15.5, 22.4, "room temperature $20$", fontsize=10.5, color=ACC)
ax.plot([0], [80], "o", color=GOLD, ms=8, zorder=5)
ax.set_title("$\\dfrac{d\\theta}{dt} = -k(\\theta - 20)$\n"
             "$\\theta = 20 + 60e^{-kt}$", fontsize=12.5, color=GOLD, pad=10)
ax.set_xlim(0, 30)
ax.set_ylim(0, 92)
ax.set_xlabel("$t$")
tidy(ax)

fig.text(0.5, -0.06,
         "Different right-hand sides give different SHAPES.   "
         "$k\\sqrt{G}$ gives a parabola, $kP$ gives an exponential, and "
         "$-k(\\theta - 20)$ gives an exponential that levels off at $20$ "
         "instead of at $0$.",
         fontsize=11.5, ha="center", color=INK)
fig.tight_layout()
save(fig, "ahl-5-14-models.svg")

print("figures written to", os.path.normpath(OUT))
