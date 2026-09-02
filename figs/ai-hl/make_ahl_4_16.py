"""AHL 4.16 の図を作る。ラベルはすべて英語（日本語グリフは matplotlib に無い）。
   出力先: ai-hl/04-statistics-and-probability/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_4_16.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from _graph import INK, GRID, LINE, ACC, GREEN, GREY, GOLD, BOX

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "04-statistics-and-probability", "img")
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True)
    plt.close(fig)
    print("wrote", name)


def tidy(ax):
    ax.grid(True, axis="x", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(GREY)
    ax.set_yticks([])


# ══════════════ 1. 「95%」が何を意味するのか ══════════════
# 同じ母集団から 100 回標本をとって、そのたびに区間を作る。
rng = np.random.default_rng(4165)
MU, SIG, N, K = 50.0, 8.0, 12, 100
d = rng.normal(MU, SIG, size=(K, N))
xb = d.mean(axis=1)
sd = d.std(axis=1, ddof=1)
t = float(stats.t.ppf(0.975, N - 1))
lo = xb - t * sd / math.sqrt(N)
hi = xb + t * sd / math.sqrt(N)
hit = (lo <= MU) & (MU <= hi)

fig, ax = plt.subplots(figsize=(9.0, 6.4))
for i in range(K):
    c = LINE if hit[i] else ACC
    ax.plot([lo[i], hi[i]], [i, i], color=c, lw=1.5,
            solid_capstyle="butt", zorder=3)
    ax.plot([xb[i]], [i], "o", ms=2.6, color=c, zorder=4)
ax.axvline(MU, color=GOLD, lw=2.2, zorder=5)
ax.text(MU + 0.35, K + 1.5, "the true mean  $\\mu = 50$", fontsize=11.5,
        ha="left", va="center", color=GOLD)
miss = int((~hit).sum())
ax.set_xlim(41, 59)
ax.set_ylim(-5.5, K + 4)
ax.set_xlabel("value")
ax.set_title("$100$ samples, $100$ different $95\\%$ intervals",
             fontsize=13, color=INK, pad=12)
ax.text(41.4, -3.6,
        "%d of the %d intervals contain $\\mu$   ·   %d miss (red)"
        % (K - miss, K, miss),
        fontsize=11.5, ha="left", va="center", color=INK)
tidy(ax)
fig.tight_layout()
save(fig, "ahl-4-16-meaning.svg")


# ══════════════ 2. 区間の幅を決める 3 つ ══════════════
def ci(xbar, s, n, conf, known):
    se = s / math.sqrt(n)
    q = (float(stats.norm.ppf(0.5 + conf / 2)) if known
         else float(stats.t.ppf(0.5 + conf / 2, n - 1)))
    return xbar - q * se, xbar + q * se


fig, axs = plt.subplots(1, 3, figsize=(13.6, 3.9), sharex=True)

# (a) 信頼水準
ax = axs[0]
rows = [(0.90, "$90\\%$", GREEN), (0.95, "$95\\%$", LINE),
        (0.99, "$99\\%$", ACC)]
for i, (c, lab, col) in enumerate(rows):
    a, b = ci(68.4, 5.2, 20, c, False)
    y = len(rows) - 1 - i
    ax.plot([a, b], [y, y], color=col, lw=6, solid_capstyle="butt", zorder=3)
    ax.plot([68.4], [y], "|", ms=16, color="white", mew=2, zorder=4)
    ax.text(63.2, y, lab, fontsize=12, ha="right", va="center", color=col)
    ax.text(73.6, y, "width $%.2f$" % (b - a), fontsize=10.5, ha="left",
            va="center", color=col)
ax.set_title("higher confidence  $\\rightarrow$  wider",
             fontsize=12, color=INK, pad=10)

# (b) 標本の大きさ
ax = axs[1]
rows = [(10, GREEN), (20, LINE), (40, ACC)]
for i, (n, col) in enumerate(rows):
    a, b = ci(68.4, 5.2, n, 0.95, False)
    y = len(rows) - 1 - i
    ax.plot([a, b], [y, y], color=col, lw=6, solid_capstyle="butt", zorder=3)
    ax.plot([68.4], [y], "|", ms=16, color="white", mew=2, zorder=4)
    ax.text(63.2, y, "$n = %d$" % n, fontsize=12, ha="right", va="center",
            color=col)
    ax.text(73.6, y, "width $%.2f$" % (b - a), fontsize=10.5, ha="left",
            va="center", color=col)
ax.set_title("larger sample  $\\rightarrow$  narrower",
             fontsize=12, color=INK, pad=10)

# (c) ばらつき
ax = axs[2]
rows = [(2.6, GREEN), (5.2, LINE), (7.8, ACC)]
for i, (s, col) in enumerate(rows):
    a, b = ci(68.4, s, 20, 0.95, False)
    y = len(rows) - 1 - i
    ax.plot([a, b], [y, y], color=col, lw=6, solid_capstyle="butt", zorder=3)
    ax.plot([68.4], [y], "|", ms=16, color="white", mew=2, zorder=4)
    ax.text(63.2, y, "$s = %.1f$" % s, fontsize=12, ha="right", va="center",
            color=col)
    ax.text(73.6, y, "width $%.2f$" % (b - a), fontsize=10.5, ha="left",
            va="center", color=col)
ax.set_title("more spread in the data  $\\rightarrow$  wider",
             fontsize=12, color=INK, pad=10)

for ax in axs:
    ax.axvline(68.4, color=GOLD, lw=1.6, ls="--", zorder=1)
    ax.set_xlim(62.0, 79.0)
    ax.set_ylim(-0.8, 2.8)
    tidy(ax)
    ax.set_xticks([64, 68, 72])
fig.tight_layout()
save(fig, "ahl-4-16-width.svg")


# ══════════════ 3. 2 つの区間が重なるとき ══════════════
fig, axs = plt.subplots(1, 2, figsize=(12.0, 3.6), sharex=True)

CASES = [
    ("the intervals overlap", [(51.2, 55.8, "brand A", LINE),
                               (54.1, 58.9, "brand B", GREEN)],
     "you cannot claim one mean is larger", ACC),
    ("the intervals do not overlap", [(51.0, 54.0, "brand A", LINE),
                                      (56.0, 59.0, "brand B", GREEN)],
     "here the evidence is much stronger", GREEN),
]
for ax, (title, bars, note, ncol) in zip(axs, CASES):
    for i, (a, b, lab, col) in enumerate(bars):
        y = 1 - i
        ax.plot([a, b], [y, y], color=col, lw=9, solid_capstyle="butt",
                zorder=3, alpha=0.85)
        ax.plot([(a + b) / 2], [y], "|", ms=20, color="white", mew=2.4,
                zorder=4)
        ax.text(50.3, y, lab, fontsize=12, ha="right", va="center", color=col)
        ax.text((a + b) / 2, y + 0.34, "$(%.1f,\\ %.1f)$" % (a, b),
                fontsize=10.5, ha="center", va="bottom", color=col)
    ov_lo, ov_hi = max(bars[0][0], bars[1][0]), min(bars[0][1], bars[1][1])
    if ov_lo < ov_hi:
        ax.axvspan(ov_lo, ov_hi, color="#fdeaea", zorder=1)
        ax.text((ov_lo + ov_hi) / 2, -0.62, "overlap", fontsize=10.5,
                ha="center", va="center", color=ACC)
    ax.set_title(title, fontsize=12.5, color=INK, pad=10)
    ax.text(54.8, -1.12, note, fontsize=11.5, ha="center", va="center",
            color=ncol)
    ax.set_xlim(48.5, 61.0)
    ax.set_ylim(-1.5, 1.75)
    tidy(ax)
fig.tight_layout()
save(fig, "ahl-4-16-overlap.svg")

print("figures written to", os.path.normpath(OUT))
