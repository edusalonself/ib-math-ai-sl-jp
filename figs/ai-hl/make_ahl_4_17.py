"""AHL 4.17 の図を作る。ラベルはすべて英語（日本語グリフは matplotlib に無い）。
   出力先: ai-hl/04-statistics-and-probability/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_4_17.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import math
import numpy as np
import matplotlib.pyplot as plt
from _graph import INK, GRID, LINE, ACC, GREEN, GREY, GOLD, BOX

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "04-statistics-and-probability", "img")
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True)
    plt.close(fig)
    print("wrote", name)


def pois(k, m):
    return math.exp(-m) * m ** k / math.factorial(k)


def tidy(ax):
    ax.grid(True, axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(GREY)
    ax.set_yticks([])


# ══════════════ 1. m が変わると形が変わる ══════════════
fig, axs = plt.subplots(1, 3, figsize=(13.2, 3.9))
for ax, (m, col) in zip(axs, ((1.0, GREEN), (3.4, LINE), (10.2, ACC))):
    ks = np.arange(0, 25)
    ps = [pois(int(k), m) for k in ks]
    ax.bar(ks, ps, width=0.72, color=col, alpha=0.85, zorder=3)
    ax.axvline(m, color=GOLD, lw=2.0, ls="--", zorder=4)
    ax.text(m + 0.4, max(ps) * 1.02, "mean $= %g$" % m, fontsize=10.5,
            ha="left", va="top", color=GOLD)
    ax.set_xlim(-0.8, 24)
    ax.set_ylim(0, max(ps) * 1.22)
    ax.set_xlabel("number of events $x$")
    ax.set_title("$X \\sim \\mathrm{Po}(%g)$" % m, fontsize=12.5, color=col,
                 pad=10)
    tidy(ax)
fig.text(0.5, -0.04,
         "the mean is always $m$, and so is the variance:   "
         "small $m$ gives a skewed shape, large $m$ looks almost normal",
         fontsize=11.5, ha="center", color=INK)
fig.tight_layout()
save(fig, "ahl-4-17-shapes.svg")


# ══════════════ 2. m は区間に比例する ══════════════
fig, axs = plt.subplots(1, 3, figsize=(13.2, 3.7), sharey=True)
RATE = 3.4
for ax, (hours, lab, col) in zip(
        axs, ((0.5, "$30$ minutes", GREEN), (1.0, "$1$ hour", LINE),
              (3.0, "$3$ hours", ACC))):
    m = RATE * hours
    ks = np.arange(0, 25)
    ps = [pois(int(k), m) for k in ks]
    ax.bar(ks, ps, width=0.72, color=col, alpha=0.85, zorder=3)
    ax.axvline(m, color=GOLD, lw=2.0, ls="--", zorder=4)
    ax.set_xlim(-0.8, 24)
    ax.set_ylim(0, 0.34)
    ax.set_xlabel("number of emails")
    ax.set_title("%s:   $m = %.4g \\times %.4g = %.4g$"
                 % (lab, RATE, hours, m), fontsize=11.5, color=col, pad=10)
    tidy(ax)
fig.text(0.5, -0.05,
         "$3.4$ emails per hour.   The RATE never changes — what changes is "
         "the length of the interval, and $m$ changes with it.",
         fontsize=11.5, ha="center", color=INK)
fig.tight_layout()
save(fig, "ahl-4-17-scaling.svg")


# ══════════════ 3. 3 つの分布の選び分け ══════════════
fig, axs = plt.subplots(1, 3, figsize=(13.2, 4.1))

# binomial B(20, 0.3)
ax = axs[0]
ks = np.arange(0, 21)
ps = [math.comb(20, int(k)) * 0.3 ** int(k) * 0.7 ** (20 - int(k)) for k in ks]
ax.bar(ks, ps, width=0.72, color=GREEN, alpha=0.85, zorder=3)
ax.set_xlim(-0.8, 20.8)
ax.set_ylim(0, max(ps) * 1.42)
ax.set_xlabel("$x$")
ax.set_title("binomial   $B(20,\\ 0.3)$", fontsize=12.5, color=GREEN, pad=10)
ax.text(10.0, max(ps) * 1.30, "$n$ trials, each a success or a failure",
        fontsize=10.5, ha="center", color=INK)
ax.text(10.0, max(ps) * 1.14, "mean $6$,  variance $4.2$",
        fontsize=10.5, ha="center", color=GREEN)
tidy(ax)

# Poisson Po(6)
ax = axs[1]
ps = [pois(int(k), 6.0) for k in ks]
ax.bar(ks, ps, width=0.72, color=LINE, alpha=0.85, zorder=3)
ax.set_xlim(-0.8, 20.8)
ax.set_ylim(0, max(ps) * 1.42)
ax.set_xlabel("$x$")
ax.set_title("Poisson   $\\mathrm{Po}(6)$", fontsize=12.5, color=LINE, pad=10)
ax.text(10.0, max(ps) * 1.30, "counts in an interval, no upper limit",
        fontsize=10.5, ha="center", color=INK)
ax.text(10.0, max(ps) * 1.14, "mean $6$,  variance $6$",
        fontsize=10.5, ha="center", color=LINE)
tidy(ax)

# normal
ax = axs[2]
xs = np.linspace(-1, 21, 600)
ys = np.exp(-0.5 * ((xs - 6) / 2.45) ** 2) / (2.45 * math.sqrt(2 * math.pi))
ax.fill_between(xs, ys, color=ACC, alpha=0.30, zorder=2)
ax.plot(xs, ys, color=ACC, lw=2.4, zorder=3)
ax.set_xlim(-0.8, 20.8)
ax.set_ylim(0, max(ys) * 1.42)
ax.set_xlabel("$x$")
ax.set_title("normal   $N(6,\\ 2.45^{2})$", fontsize=12.5, color=ACC, pad=10)
ax.text(10.0, max(ys) * 1.30, "a measurement, not a count",
        fontsize=10.5, ha="center", color=INK)
ax.text(10.0, max(ys) * 1.14, "any value, not just whole numbers",
        fontsize=10.5, ha="center", color=ACC)
tidy(ax)

fig.text(0.5, -0.03,
         "the first two are counts (whole numbers); the third is continuous.  "
         "Only Poisson has variance equal to the mean.",
         fontsize=11.5, ha="center", color=INK)
fig.tight_layout()
save(fig, "ahl-4-17-choosing.svg")

print("figures written to", os.path.normpath(OUT))
