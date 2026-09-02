"""AHL 4.14 の図を作る。ラベルはすべて英語（日本語グリフは matplotlib に無い）。
   出力先: ai-hl/04-statistics-and-probability/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_4_14.py
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


def tidy(ax):
    ax.grid(True, axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(GREY)
    ax.set_yticks([])


# ══════════════ 1. aX + b が分布に何をするか ══════════════
# もとの分布：値 1,2,3,4,5 に確率をつける
XS = np.array([1, 2, 3, 4, 5], float)
PS = np.array([0.1, 0.2, 0.4, 0.2, 0.1])
MU = float((XS * PS).sum())
VAR = float((((XS - MU) ** 2) * PS).sum())
SD = math.sqrt(VAR)

PANELS = [
    ("$X$", XS, LINE, ""),
    ("$X + 3$   (add $3$)", XS + 3, GREEN, "  — unchanged"),
    ("$2X$   (multiply by $2$)", 2 * XS, ACC, "  — doubled"),
]

fig, axs = plt.subplots(1, 3, figsize=(13.0, 3.9), sharey=True)
for ax, (title, vals, col, sub) in zip(axs, PANELS):
    ax.bar(vals, PS, width=0.42, color=col, alpha=0.85, zorder=3)
    m = float((vals * PS).sum())
    s = math.sqrt(float((((vals - m) ** 2) * PS).sum()))
    ax.axvline(m, color=GOLD, lw=2.0, ls="--", zorder=4)
    ax.annotate("", xy=(m - s, 0.455), xytext=(m + s, 0.455),
                arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.5),
                zorder=6)
    ax.text(m, 0.475, "$\\pm$ one sd", fontsize=10, ha="center",
            va="bottom", color=GREY)
    ax.text(m, -0.055, "mean", fontsize=10, ha="center", va="top",
            color=GOLD)
    ax.set_xlim(-0.6, 11.4)
    ax.set_ylim(0, 0.66)
    ax.set_title(title, fontsize=12.5, color=col, pad=10)
    ax.text(5.4, 0.60, "mean $= %.3g$,  sd $= %.3g$%s" % (m, s, sub),
            fontsize=10.5, ha="center", color=INK)
    tidy(ax)
fig.tight_layout()
save(fig, "ahl-4-14-transform.svg")


# ══════════════ 2. 2X と X1 + X2 は違う ══════════════
# X: 5kg の袋。値 4.6..5.4 を離散でつくる（sd = 0.2 に合わせる）
BV = np.array([4.6, 4.8, 5.0, 5.2, 5.4])
BP = np.array([0.05, 0.30, 0.30, 0.30, 0.05])
bm = float((BV * BP).sum())
bv = float((((BV - bm) ** 2) * BP).sum())

# 2X
TV, TP = 2 * BV, BP
# X1 + X2（独立な和：畳み込み）
sums = {}
for v1, p1 in zip(BV, BP):
    for v2, p2 in zip(BV, BP):
        k = round(v1 + v2, 6)
        sums[k] = sums.get(k, 0.0) + p1 * p2
SV = np.array(sorted(sums))
SP = np.array([sums[k] for k in SV])

fig, axs = plt.subplots(1, 2, figsize=(12.4, 4.2), sharex=True, sharey=True)

ax = axs[0]
ax.bar(TV, TP, width=0.22, color=ACC, alpha=0.85, zorder=3)
ax.axvline(10, color=GOLD, lw=2.0, ls="--", zorder=4)
sd2 = math.sqrt(float((((TV - 10) ** 2) * TP).sum()))
ax.annotate("", xy=(10 - sd2, 0.44), xytext=(10 + sd2, 0.44),
            arrowprops=dict(arrowstyle="<->", color=ACC, lw=1.8), zorder=6)
ax.text(10, 0.465, "sd $= %.3g$" % sd2, fontsize=11.5, ha="center",
        va="bottom", color=ACC, bbox=BOX, zorder=12)
ax.set_title("$2X$   —   weigh ONE bag, double the reading",
             fontsize=12, color=ACC, pad=10)
ax.set_xlabel("mass (kg)")
tidy(ax)

ax = axs[1]
ax.bar(SV, SP, width=0.14, color=GREEN, alpha=0.85, zorder=3)
ax.axvline(10, color=GOLD, lw=2.0, ls="--", zorder=4)
sds = math.sqrt(float((((SV - 10) ** 2) * SP).sum()))
ax.annotate("", xy=(10 - sds, 0.44), xytext=(10 + sds, 0.44),
            arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.8), zorder=6)
ax.text(10, 0.465, "sd $= %.3g$" % sds, fontsize=11.5, ha="center",
        va="bottom", color=GREEN, bbox=BOX, zorder=12)
ax.set_title("$X_{1} + X_{2}$   —   weigh TWO bags, add them",
             fontsize=12, color=GREEN, pad=10)
ax.set_xlabel("mass (kg)")
ax.set_xlim(8.8, 11.2)
ax.set_ylim(0, 0.56)
tidy(ax)

fig.text(0.5, -0.03,
         "same mean ($10$ kg), different spread:   two bags can cancel each "
         "other out, one doubled bag cannot",
         fontsize=11.5, ha="center", color=INK)
fig.tight_layout()
save(fig, "ahl-4-14-2x.svg")


# ══════════════ 3. なぜ n - 1 で割るのか ══════════════
rng = np.random.default_rng(7)
POPMU, POPSD = 50.0, 10.0
fig, axs = plt.subplots(1, 2, figsize=(12.4, 4.3))

# 左：同じ標本でも、x-bar から測ると μ から測るより必ず近い
ax = axs[0]
smp = np.array([53.0, 57.0, 62.0, 64.0])
sm = float(smp.mean())          # 59
SSmu = float(((smp - POPMU) ** 2).sum())     # 398
SSxb = float(((smp - sm) ** 2).sum())        # 74

for row, centre, col, lab, ss in (
        (1.72, POPMU, GREY, "measured from $\\mu = 50$", SSmu),
        (0.62, sm, ACC, "measured from $\\bar{x} = 59$", SSxb)):
    ax.axvline(centre, ymin=0.06, ymax=0.94, color=col, lw=2.0,
               ls="--", zorder=2)
    for v in smp:
        ax.annotate("", xy=(v, row), xytext=(centre, row),
                    arrowprops=dict(arrowstyle="-", color=col, lw=1.6),
                    zorder=4)
    ax.plot(smp, np.full_like(smp, row), "o", ms=11, mfc="white",
            mec=LINE, mew=2.0, zorder=5)
    ax.text(35.5, row, lab, fontsize=11, ha="left", va="center", color=col)
    ax.text(35.5, row - 0.30, "sum of squares $= %g$" % ss, fontsize=11,
            ha="left", va="center", color=col, weight="bold")

ax.text(52, -0.30, "the lower distances are shorter — and they are as\n"
                   "short as any centre could possibly make them",
        fontsize=10.5, ha="center", va="center", color=INK)
ax.set_xlim(34, 70)
ax.set_ylim(-0.72, 2.25)
ax.set_yticks([])
ax.set_title("the same sample, measured two ways",
             fontsize=12, color=INK, pad=10)
for sp in ("top", "right", "left"):
    ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_color(GREY)

# 右：標本を何度も取ると、n で割った分散は平均して小さすぎる
ax = axs[1]
NS = [2, 3, 4, 5, 8, 12, 20]
vn, vn1 = [], []
for n in NS:
    d = rng.normal(POPMU, POPSD, size=(60000, n))
    vn.append(float(np.var(d, axis=1, ddof=0).mean()))
    vn1.append(float(np.var(d, axis=1, ddof=1).mean()))
ax.axhline(POPSD ** 2, color=GREY, lw=2.0, ls="--", zorder=2)
ax.text(20, POPSD ** 2 + 5, "$\\sigma^{2} = 100$", fontsize=11.5,
        ha="right", va="bottom", color=GREY)
ax.plot(NS, vn, "o-", color=ACC, lw=2.2, ms=7,
        label="divide by $n$   — too small")
ax.plot(NS, vn1, "s-", color=GREEN, lw=2.2, ms=7,
        label="divide by $n-1$   — on target")
ax.set_xlabel("sample size $n$")
ax.set_ylabel("average value over many samples")
ax.set_ylim(0, 130)
ax.legend(fontsize=10.5, loc="lower right", frameon=False)
ax.set_title("what each formula gives, averaged over many samples",
             fontsize=12, color=INK, pad=10)
ax.grid(True, color=GRID, lw=0.8)
ax.set_axisbelow(True)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)

fig.tight_layout()
save(fig, "ahl-4-14-unbiased.svg")

print("figures written to", os.path.normpath(OUT))
