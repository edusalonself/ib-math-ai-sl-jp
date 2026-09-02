"""AHL 4.18c の図を作る。ラベルはすべて英語（日本語グリフは matplotlib に無い）。
   出力先: ai-hl/04-statistics-and-probability/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_4_18c.py
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

Z10, Z05, Z01 = 1.2815515655, 1.6448536270, 2.3263478740


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True)
    plt.close(fig)
    print("wrote", name)


def phi(x, mu, sd):
    return np.exp(-0.5 * ((x - mu) / sd) ** 2) / (sd * math.sqrt(2 * math.pi))


def binom(k, n, p):
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


def tidy(ax):
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(GREY)
    ax.set_yticks([])


# ══════════════ 1. 2 つの誤りは、2 つの分布の上にある ══════════════
MU0, MU1, SE = 100.0, 106.0, 3.0
CRIT = MU0 + Z05 * SE

fig, ax = plt.subplots(figsize=(11.6, 5.0))
xs = np.linspace(88, 120, 1200)
y0 = phi(xs, MU0, SE)
y1 = phi(xs, MU1, SE)

# alpha：H0 の分布の、境目より右
m = xs >= CRIT
ax.fill_between(xs[m], y0[m], color=ACC, alpha=0.55, zorder=3)
# beta：H1 の分布の、境目より左
m = xs <= CRIT
ax.fill_between(xs[m], y1[m], color=LINE, alpha=0.45, zorder=3)

ax.plot(xs, y0, color=INK, lw=2.2, zorder=5)
ax.plot(xs, y1, color=INK, lw=2.2, ls="--", zorder=5)
ax.axvline(CRIT, color=GOLD, lw=2.2, zorder=6)

top = max(y0.max(), y1.max())
ax.text(MU0, top * 1.06, "if $H_0$ is TRUE\n$\\bar{X} \\sim N(100,\\ 3^2)$",
        ha="center", va="bottom", fontsize=11, color=INK)
ax.text(MU1 + 3.4, top * 1.06,
        "if the TRUE mean is $106$\n$\\bar{X} \\sim N(106,\\ 3^2)$",
        ha="center", va="bottom", fontsize=11, color=INK)
ax.text(CRIT, -top * 0.115, "$104.9$", ha="center", va="top", fontsize=11.5,
        color=GOLD)
ax.text(CRIT, top * 1.30, "critical value", ha="center", va="bottom",
        fontsize=11, color=GOLD)

ax.annotate("$\\alpha = P(\\text{Type I}) = 0.05$",
            xy=(106.6, phi(106.6, MU0, SE) * 0.45), xytext=(112.5, top * 0.62),
            fontsize=12, color=ACC, ha="left",
            arrowprops=dict(arrowstyle="->", color=ACC, lw=1.5),
            bbox=BOX, zorder=8)
ax.annotate("$\\beta = P(\\text{Type II}) = 0.361$",
            xy=(102.6, phi(102.6, MU1, SE) * 0.45), xytext=(88.4, top * 0.62),
            fontsize=12, color=LINE, ha="left",
            arrowprops=dict(arrowstyle="->", color=LINE, lw=1.5),
            bbox=BOX, zorder=8)

ax.set_xlim(88, 120)
ax.set_ylim(0, top * 1.52)
ax.set_xlabel("sample mean $\\bar{x}$", labelpad=18)
ax.set_xticks([94, 100, 106, 112, 118])
tidy(ax)

fig.text(0.5, -0.06,
         "$\\alpha$ is measured under the SOLID curve ($H_0$ true).   "
         "$\\beta$ is measured under the DASHED curve (the true mean is "
         "$106$).   They live on DIFFERENT distributions, "
         "which is why $\\beta \\neq 1 - \\alpha$.",
         fontsize=11.5, ha="center", color=INK)
fig.tight_layout()
save(fig, "ahl-4-18c-two-errors.svg")


# ══════════════ 2. α を小さくすると β は大きくなる ══════════════
fig, axs = plt.subplots(3, 1, figsize=(8.4, 8.6), sharex=True)
xs = np.linspace(88, 120, 1200)
y0 = phi(xs, MU0, SE)
y1 = phi(xs, MU1, SE)
top = max(y0.max(), y1.max())

for ax, (lab, z, a) in zip(
        axs, (("$10\\%$", Z10, 0.10), ("$5\\%$", Z05, 0.05),
              ("$1\\%$", Z01, 0.01))):
    c = MU0 + z * SE
    beta = float(0.5 * (1 + math.erf((c - MU1) / (SE * math.sqrt(2)))))
    m = xs >= c
    ax.fill_between(xs[m], y0[m], color=ACC, alpha=0.55, zorder=3)
    m = xs <= c
    ax.fill_between(xs[m], y1[m], color=LINE, alpha=0.45, zorder=3)
    ax.plot(xs, y0, color=INK, lw=1.9, zorder=5)
    ax.plot(xs, y1, color=INK, lw=1.9, ls="--", zorder=5)
    ax.axvline(c, color=GOLD, lw=2.0, zorder=6)
    ax.set_title("significance level %s:   critical value $= %.1f$,   "
                 "$\\alpha = %.2f$,   $\\beta = %.3f$" % (lab, c, a, beta),
                 fontsize=12.0, color=INK, pad=8)
    ax.set_xlim(88, 120)
    ax.set_ylim(0, top * 1.14)
    tidy(ax)

axs[2].set_xlabel("sample mean $\\bar{x}$")
axs[2].set_xticks([94, 100, 106, 112, 118])

fig.text(0.5, -0.035,
         "As $\\alpha$ goes DOWN, the boundary moves RIGHT — "
         "and $\\beta$ goes UP.   You cannot make both small at once "
         "with the same sample size.",
         fontsize=11.5, ha="center", color=INK)
fig.tight_layout()
save(fig, "ahl-4-18c-tradeoff.svg")


# ══════════════ 3. 離散分布でも、同じ 2 枚の絵 ══════════════
N = 20
ks = np.arange(0, 21)
K = 15  # critical region X >= 15

fig, axs = plt.subplots(2, 1, figsize=(8.8, 6.4), sharex=True)

for ax, (p, is_h0) in zip(axs, ((0.5, True), (0.8, False))):
    ps = [binom(int(k), N, p) for k in ks]
    if is_h0:
        cols = [ACC if k >= K else GREY for k in ks]
        tot = sum(ps[K:])
        title = ("if $H_0$ is TRUE:   $X \\sim B(20,\\ 0.5)$      "
                 "$\\alpha = P(X \\geq 15) = %.4f$" % tot)
        col = ACC
    else:
        cols = [LINE if k < K else GREY for k in ks]
        tot = sum(ps[:K])
        title = ("if the TRUE $p$ is $0.8$:   $X \\sim B(20,\\ 0.8)$      "
                 "$\\beta = P(X \\leq 14) = %.4f$" % tot)
        col = LINE
    ax.bar(ks, ps, width=0.72, color=cols, alpha=0.9, zorder=3)
    ax.axvline(K - 0.5, color=GOLD, lw=2.0, ls="--", zorder=6)
    ax.set_title(title, fontsize=11.8, color=col, pad=8)
    ax.set_ylim(0, max(ps) * 1.18)
    ax.grid(True, axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    tidy(ax)

axs[1].set_xlim(-0.8, 20.8)
axs[1].set_xticks(range(0, 21, 5))
axs[1].set_xlabel("number of successes $x$")

fig.text(0.5, -0.04,
         "SAME critical region $X \\geq 15$, TWO different distributions.  "
         "$\\alpha$ is the shaded part of the top picture; "
         "$\\beta$ is the shaded part of the bottom one.",
         fontsize=11.5, ha="center", color=INK)
fig.tight_layout()
save(fig, "ahl-4-18c-discrete.svg")

print("figures written to", os.path.normpath(OUT))
