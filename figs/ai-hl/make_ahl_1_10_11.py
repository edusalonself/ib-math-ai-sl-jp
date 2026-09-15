"""AHL 1.10（有理数の指数）と AHL 1.11（無限等比級数）の図を作る。
   ラベルは英語。出力先: ai-hl/01-number-and-algebra/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_1_10_11.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from _graph import INK, GRID, LINE, ACC, GREEN, GREY, GOLD, BOX, FILL

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "01-number-and-algebra", "img")
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


# ══════════ 1.10 (a)  整数の指数の間を埋める ══════════
fig, ax = plt.subplots(figsize=(6.6, 4.6))
X = np.linspace(0, 4, 500)
specs = [(0.5, GREEN, "$y = x^{\\frac{1}{2}} = \\sqrt{x}$", "-"),
         (1.0, GREY, "$y = x^{1}$", "--"),
         (1.5, ACC, "$y = x^{\\frac{3}{2}}$", "-"),
         (2.0, GOLD, "$y = x^{2}$", "--")]
for p, col, lab, ls in specs:
    ax.plot(X, X ** p, color=col, lw=2.6, ls=ls, label=lab)
ax.plot([4], [2], "o", color=GREEN, ms=8, zorder=6)
ax.plot([4], [8], "o", color=ACC, ms=8, zorder=6)
ax.text(4.12, 2.0, "$4^{\\frac{1}{2}} = 2$", fontsize=11.5, color=GREEN,
        ha="left", va="center", zorder=8)
ax.text(4.12, 8.0, "$4^{\\frac{3}{2}} = 8$", fontsize=11.5, color=ACC,
        ha="left", va="center", zorder=8)
ax.set_xlim(0, 6.3)
ax.set_ylim(0, 17.5)
ax.set_xlabel("$x$")
ax.legend(fontsize=10.5, frameon=False, loc="upper left")
ax.set_title("a rational exponent is still just a power",
             fontsize=12, color=INK, pad=10)
tidy(ax)

fig.tight_layout()
save(fig, "ahl-1-10-powers.svg")


# ══════════ 1.10 (b)  2 通りの道 ══════════
fig, ax = plt.subplots(figsize=(6.6, 4.6))
ax.set_xlim(0, 10)
ax.set_ylim(-0.9, 7.2)
ax.axis("off")


def box(cx, cy, w, h, txt, col, fs=12.5):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle="round,pad=0.16", fc="white",
                                ec=col, lw=2.0, zorder=4))
    ax.text(cx, cy, txt, fontsize=fs, ha="center", va="center", color=col,
            zorder=5)


def arrow(p, q, col, lab):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16,
                                 color=col, lw=2.0, zorder=3))
    ax.text(p[0] + 0.18, (p[1] + q[1]) / 2, lab, fontsize=11,
            color=col, ha="left", va="center", zorder=6)


box(2.0, 6.0, 2.4, 0.95, "$32^{\\frac{3}{5}}$", INK, 14)
box(2.0, 3.6, 2.6, 0.95, "$\\sqrt[5]{32} = 2$", GREEN)
box(2.0, 1.2, 2.4, 0.95, "$2^{3} = 8$", GREEN, 14)
arrow((2.0, 5.5), (2.0, 4.15), GREEN, "root first")
arrow((2.0, 3.1), (2.0, 1.75), GREEN, "then cube")

box(7.4, 6.0, 2.4, 0.95, "$32^{\\frac{3}{5}}$", INK, 14)
box(7.4, 3.6, 3.1, 0.95, "$32^{3} = 32768$", ACC)
box(7.4, 1.2, 3.3, 0.95, "$\\sqrt[5]{32768} = 8$", ACC)
arrow((7.4, 5.5), (7.4, 4.15), ACC, "cube first")
arrow((7.4, 3.1), (7.4, 1.75), ACC, "then root")

ax.text(4.7, -0.35, "same answer — but the left route keeps the numbers small",
        fontsize=11.5, color=GREY, ha="center", va="center", zorder=6)
ax.set_title("two routes to $32^{\\frac{3}{5}}$", fontsize=12, color=INK,
             pad=10)

fig.tight_layout()
save(fig, "ahl-1-10-routes.svg")


# ══════════ 1.11  (a) 部分和が近づく / (b) 弾むボール ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.9))

ax = axs[0]
N = np.arange(1, 15)
S1 = 12 * (1 - (1 / 3.0) ** N) / (1 - 1 / 3.0)
S2 = 24 * (1 - (-0.75) ** N) / (1 - (-0.75))
ax.plot(N, S1, "o-", color=LINE, lw=2.2, ms=6,
        label="$u_1 = 12,\\ r = \\dfrac{1}{3}$")
ax.plot(N, S2, "s--", color=ACC, lw=2.0, ms=6,
        label="$u_1 = 24,\\ r = -0.75$")
ax.axhline(18, color=LINE, lw=1.4, ls=":")
ax.axhline(24 / 1.75, color=ACC, lw=1.4, ls=":")
ax.text(14.6, 18, "$S_\\infty = 18$", fontsize=11.5, color=LINE,
        va="bottom", ha="left")
ax.text(14.6, 24 / 1.75, "$S_\\infty = 13.7$", fontsize=11.5, color=ACC,
        va="bottom", ha="left")
ax.text(1.2, 32.5, "the partial sums settle down\nwhen $|r| < 1$",
        fontsize=11.5, color=INK, ha="left", va="top", bbox=BOX, zorder=8)
ax.set_xlim(0.4, 18.4)
ax.set_ylim(0, 36)
ax.set_xlabel("$n$  (number of terms added)")
ax.set_ylabel("$S_n$")
ax.legend(fontsize=10.5, frameon=False, loc="lower right")
ax.set_title("(a)  partial sums approach a limit", fontsize=12, color=INK,
             pad=10)
tidy(ax)

ax = axs[1]
h0, k = 2.0, 0.6
xs, ys = [], []
x = 0.0
heights = [h0 * k ** i for i in range(6)]
# 最初の落下
t = np.linspace(0, 1, 60)
xs += list(x + 0.45 * t)
ys += list(h0 * (1 - t ** 2))
x += 0.45
for h in heights[1:]:
    w = 0.9 * np.sqrt(h / h0)
    t = np.linspace(-1, 1, 90)
    xs += list(x + w * (t + 1) / 2)
    ys += list(h * (1 - t ** 2))
    x += w
ax.plot(xs, ys, color=LINE, lw=2.4, zorder=5)
ax.axhline(0, color=GREY, lw=2.0)
for i, h in enumerate(heights[:4]):
    lab = "$2$" if i == 0 else ("$1.2$" if i == 1 else
                                ("$0.72$" if i == 2 else "$0.432$"))
    xi = 0.0 if i == 0 else (0.45 + sum(0.9 * np.sqrt(heights[j] / h0)
                                        for j in range(1, i)) +
                             0.45 * np.sqrt(heights[i] / h0))
    ax.plot([xi, xi], [0, h], color=GOLD, lw=1.4, ls=":", zorder=3)
    ax.text(xi, h + 0.09, lab, fontsize=11, color=GOLD, ha="center",
            va="bottom", zorder=7)
ax.text(0.06, 2.72, "drop $2$, then each bounce reaches\n"
        "$60\\%$ of the height before it",
        fontsize=11.5, color=INK, ha="left", va="top", bbox=BOX, zorder=8)
ax.text(2.90, 1.55, "total distance\n$= 2 + 2\\left(\\dfrac{1.2}{1-0.6}\\right)"
        " = 8$ m", fontsize=12, color=GREEN, ha="left", va="center",
        bbox=BOX, zorder=8)
ax.set_xlim(-0.15, 5.6)
ax.set_ylim(-0.12, 3.15)
ax.set_xlabel("horizontal position (not to scale)")
ax.set_ylabel("height (m)")
ax.set_title("(b)  a bouncing ball travels a finite distance",
             fontsize=12, color=INK, pad=10)
tidy(ax)

fig.tight_layout()
save(fig, "ahl-1-11-sum.svg")

print("figures written to", os.path.normpath(OUT))
