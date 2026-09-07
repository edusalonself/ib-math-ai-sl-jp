"""AHL 4.15 の図を作る。ラベルはすべて英語（日本語グリフは matplotlib に無い）。
   出力先: ai-hl/04-statistics-and-probability/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_4_15.py
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


def pdf(x, mu, sd):
    return np.exp(-0.5 * ((x - mu) / sd) ** 2) / (sd * math.sqrt(2 * math.pi))


def curve_ax(ax):
    ax.set_yticks([])
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(GREY)


# ══════════════ 1. 独立な normal を足すと、やはり normal ══════════════
fig, ax = plt.subplots(figsize=(9.6, 4.6))
xs = np.linspace(150, 480, 1200)
for mu, sd, col, ls, lab in (
        (250.0, 8.0, LINE, "-", "$M \\sim N(250,\\,8^{2})$"),
        (180.0, 6.0, GREEN, "-", "$S \\sim N(180,\\,6^{2})$"),
        (430.0, 10.0, ACC, "-", "$M+S \\sim N(430,\\,10^{2})$")):
    ax.plot(xs, pdf(xs, mu, sd), color=col, lw=2.5, ls=ls, label=lab)
    y = pdf(mu, mu, sd) * 0.42
    ax.annotate("", xy=(mu - sd, y), xytext=(mu + sd, y),
                arrowprops=dict(arrowstyle="<->", color=col, lw=1.5),
                zorder=6)
    ax.text(mu, y * 1.10, "sd $= %g$" % sd, fontsize=10, ha="center",
            va="bottom", color=col, bbox=BOX, zorder=12)
ax.set_xlim(150, 480)
ax.set_ylim(0, 0.082)
ax.set_xlabel("mass (g)")
ax.legend(fontsize=10.5, loc="upper center", frameon=False)
ax.set_title("adding two independent normals gives another normal",
             fontsize=12.5, color=INK, pad=10)
curve_ax(ax)
fig.tight_layout()
save(fig, "ahl-4-15-sum.svg")


# ══════════════ 2. 標本平均は、n が大きいほど細くなる ══════════════
fig, ax = plt.subplots(figsize=(9.6, 4.6))
MU, SD = 1000.0, 12.0
xs = np.linspace(955, 1045, 1200)
for n, col, lw in ((1, GREY, 2.0), (4, LINE, 2.2), (9, GREEN, 2.4),
                   (25, ACC, 2.6)):
    s = SD / math.sqrt(n)
    lab = ("one bag:  $X \\sim N(1000,\\,12^{2})$" if n == 1
           else "$n = %d$:  sd $= 12/\\sqrt{%d} = %.4g$" % (n, n, s))
    ax.plot(xs, pdf(xs, MU, s), color=col, lw=lw, label=lab)
ax.axvline(MU, color=GOLD, lw=1.8, ls="--", zorder=1)
ax.text(MU + 1.2, 0.178, "$\\mu = 1000$", fontsize=11, ha="left",
        va="center", color=GOLD)
ax.set_xlim(955, 1045)
ax.set_ylim(0, 0.190)
ax.set_xlabel("mass (g)")
ax.legend(fontsize=10.5, loc="upper right", frameon=False)
ax.set_title("$\\bar{X}$ keeps the same centre, but gets narrower as $n$ grows",
             fontsize=12.5, color=INK, pad=10)
curve_ax(ax)
fig.tight_layout()
save(fig, "ahl-4-15-xbar.svg")


# ══════════════ 3. 中心極限定理 ══════════════
rng = np.random.default_rng(415)
POP = rng.exponential(1.0, 400_000)      # 右に大きく歪んだ母集団
fig, axs = plt.subplots(1, 4, figsize=(14.2, 3.7))

# 母集団そのもの
ax = axs[0]
ax.hist(POP, bins=70, range=(0, 5), density=True, color=GREY, alpha=0.8)
ax.set_xlim(0, 5)
ax.set_title("the population itself\n(strongly skewed, NOT normal)",
             fontsize=11, color=INK, pad=8)
ax.set_xlabel("$x$")
curve_ax(ax)

for ax, n in zip(axs[1:], (2, 10, 40)):
    m = rng.exponential(1.0, size=(300_000, n)).mean(axis=1)
    ax.hist(m, bins=70, density=True, color=LINE, alpha=0.55)
    g = np.linspace(m.min(), m.max(), 400)
    ax.plot(g, pdf(g, 1.0, 1.0 / math.sqrt(n)), color=ACC, lw=2.4)
    ax.set_xlim(0, 2.6)
    ax.set_title("mean of $n = %d$" % n, fontsize=11.5,
                 color=ACC if n == 40 else INK, pad=8)
    ax.set_xlabel("$\\bar{x}$")
    curve_ax(ax)

fig.text(0.5, -0.04,
         "the red curve is the normal distribution with the same mean and "
         "standard deviation:   by $n = 40$ the histogram sits on it",
         fontsize=11.5, ha="center", color=INK)
fig.tight_layout()
save(fig, "ahl-4-15-clt.svg")

print("figures written to", os.path.normpath(OUT))
