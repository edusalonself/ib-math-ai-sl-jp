"""AHL 4.18a の図を作る。ラベルはすべて英語（日本語グリフは matplotlib に無い）。
   出力先: ai-hl/04-statistics-and-probability/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_4_18a.py
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

Z05, Z025, Z01 = 1.6448536270, 1.9599639845, 2.3263478740


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True)
    plt.close(fig)
    print("wrote", name)


def phi(x, mu=0.0, sd=1.0):
    return np.exp(-0.5 * ((x - mu) / sd) ** 2) / (sd * math.sqrt(2 * math.pi))


def pois(k, m):
    return math.exp(-m) * m ** k / math.factorial(k)


def binom(k, n, p):
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


def tidy(ax):
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(GREY)
    ax.set_yticks([])


# ══════════════ 1. 片側・両側の critical region ══════════════
fig, axs = plt.subplots(1, 3, figsize=(13.2, 3.9))
xs = np.linspace(-3.6, 3.6, 800)
ys = phi(xs)

panels = [
    ("upper one-tailed,  $5\\%$", [(Z05, 3.6)], [("$1.645$", Z05)], ACC),
    ("lower one-tailed,  $5\\%$", [(-3.6, -Z05)], [("$-1.645$", -Z05)], LINE),
    ("two-tailed,  $5\\%$", [(-3.6, -Z025), (Z025, 3.6)],
     [("$-1.96$", -Z025), ("$1.96$", Z025)], GREEN),
]

for ax, (title, regions, marks, col) in zip(axs, panels):
    ax.plot(xs, ys, color=INK, lw=2.0, zorder=4)
    for a, b in regions:
        m = (xs >= a) & (xs <= b)
        ax.fill_between(xs[m], ys[m], color=col, alpha=0.55, zorder=3)
    for lab, v in marks:
        ax.axvline(v, color=col, lw=1.6, ls="--", zorder=5)
        ax.text(v, -0.033, lab, ha="center", va="top", fontsize=11, color=col)
    share = "$2.5\\%$ each side" if len(regions) == 2 else "area $= 0.05$"
    ax.text(0.0, 0.20, share, ha="center", fontsize=10.5, color=col)
    ax.set_title(title, fontsize=12.5, color=col, pad=10)
    ax.set_xlim(-3.6, 3.6)
    ax.set_ylim(0, 0.47)
    ax.set_xticks([])
    ax.set_xlabel("$z$", labelpad=16)
    tidy(ax)

fig.text(0.5, -0.07,
         "the shaded part is the CRITICAL REGION: its area is the "
         "significance level.   A two-tailed test splits the same $5\\%$ "
         "into two, so each side gets $2.5\\%$ and the value moves out to "
         "$1.96$.",
         fontsize=11.5, ha="center", color=INK)
fig.tight_layout()
save(fig, "ahl-4-18a-tails.svg")


# ══════════════ 2. z のことばから x-bar のことばへ ══════════════
MU, SE = 500.0, 1.6
CRIT = MU - Z05 * SE
fig, axs = plt.subplots(1, 2, figsize=(12.6, 3.9))

# left: z scale
ax = axs[0]
ax.plot(xs, ys, color=INK, lw=2.0, zorder=4)
m = xs <= -Z05
ax.fill_between(xs[m], ys[m], color=LINE, alpha=0.55, zorder=3)
ax.axvline(-Z05, color=LINE, lw=1.6, ls="--", zorder=5)
ax.text(-Z05, -0.033, "$-1.645$", ha="center", va="top", fontsize=11,
        color=LINE)
ax.set_title("in $z$:   reject when $z < -1.645$", fontsize=12.5, color=LINE,
             pad=10)
ax.set_xlim(-3.6, 3.6)
ax.set_ylim(0, 0.47)
ax.set_xticks([])
ax.set_xlabel("$z$", labelpad=16)
tidy(ax)

# right: xbar scale
ax = axs[1]
xb = np.linspace(MU - 3.6 * SE, MU + 3.6 * SE, 800)
yb = phi(xb, MU, SE)
ax.plot(xb, yb, color=INK, lw=2.0, zorder=4)
m = xb <= CRIT
ax.fill_between(xb[m], yb[m], color=LINE, alpha=0.55, zorder=3)
ax.axvline(CRIT, color=LINE, lw=1.6, ls="--", zorder=5)
ax.text(CRIT, -max(yb) * 0.075, "$497.37\\ldots$", ha="center", va="top",
        fontsize=11, color=LINE)
ax.axvline(MU, color=GOLD, lw=1.6, zorder=5)
ax.text(MU + 0.18, max(yb) * 0.55, "$\\mu_0 = 500$", ha="left", va="center",
        fontsize=10.5, color=GOLD, bbox=BOX, zorder=6)
ax.set_title("in $\\bar{x}$:   reject when $\\bar{x} < 497.37\\ldots$",
             fontsize=12.5, color=LINE, pad=10)
ax.set_xlim(MU - 3.6 * SE, MU + 3.6 * SE)
ax.set_ylim(0, max(yb) * 1.18)
ax.set_xticks([495, CRIT, 500, 503, 505])
ax.set_xticklabels(["$495$", "", "$500$", "$503$", "$505$"])
ax.set_xlabel("sample mean $\\bar{x}$  (g)", labelpad=16)
tidy(ax)

fig.text(0.5, -0.07,
         "$\\sigma = 8$, $n = 25$, so the standard error is "
         "$8 \\div \\sqrt{25} = 1.6$, and "
         "$500 - 1.645 \\times 1.6 = 497.368\\ldots$   "
         "The SAME picture, measured in grams instead of in $z$.   "
         "The shaded area is EXACTLY $5\\%$, because the boundary is the "
         "unrounded value.   Write $\\bar{x} < 497.4$ (1 d.p.) as the answer, "
         "but keep $497.368\\ldots$ for calculations.",
         fontsize=11.5, ha="center", color=INK)
fig.tight_layout()
save(fig, "ahl-4-18a-xbar.svg")


# ══════════════ 3. 離散分布では「ちょうど 5%」にできない ══════════════
N, P = 25, 0.4
ks = np.arange(0, 26)
ps = [binom(int(k), N, P) for k in ks]
tail14 = sum(ps[14:])
tail15 = sum(ps[15:])

fig, axs = plt.subplots(2, 1, figsize=(9.6, 6.6), sharex=True)

for ax, (kmin, tot, ok) in zip(
        axs, ((14, tail14, False), (15, tail15, True))):
    cols = [ACC if k >= kmin else GREY for k in ks]
    ax.bar(ks, ps, width=0.72, color=cols, alpha=0.9, zorder=3)
    ax.axvline(kmin - 0.5, color=INK, lw=1.6, ls="--", zorder=5)
    verdict = ("$\\leq 0.05$ — this region is allowed" if ok
               else "$> 0.05$ — TOO BIG, not allowed")
    ax.set_title("$X \\geq %d$:   $P = %.4f$   %s" % (kmin, tot, verdict),
                 fontsize=12.5, color=(GREEN if ok else ACC), pad=8)
    ax.set_ylim(0, max(ps) * 1.20)
    ax.grid(True, axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    tidy(ax)

axs[1].set_xlim(-0.8, 25.8)
axs[1].set_xticks(range(0, 26, 5))
axs[1].set_xlabel("number of successes $x$   ($X \\sim B(25,\\ 0.4)$ "
                  "under $H_0$)")

fig.text(0.5, -0.04,
         "The bars are whole numbers, so no region has area exactly $0.05$.  "
         "Take the BIGGEST region whose probability is still at most $0.05$: "
         "here that is $X \\geq 15$.",
         fontsize=11.5, ha="center", color=INK)
fig.tight_layout()
save(fig, "ahl-4-18a-discrete.svg")

print("figures written to", os.path.normpath(OUT))
