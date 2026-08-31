"""SL 4.10 の図を作る。ラベルはすべて英語。
   出力先: ai-sl/04-statistics-and-probability/img/*.svg
   再生成: python3 figs/ai-sl/make_sl_4_10.py
"""
import os
from statistics import mean
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-sl", "04-statistics-and-probability", "img")
os.makedirs(OUT, exist_ok=True)

INK, GRID, DOT, ACC = "#1f2328", "#dfe3e8", "#2874a6", "#c0392b"
plt.rcParams.update({
    "font.size": 11, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "text.color": INK, "xtick.color": INK, "ytick.color": INK,
    "svg.fonttype": "path",
})


def ranks(v):
    n = len(v)
    out = [0.0] * n
    order = sorted(range(n), key=lambda i: v[i])
    i = 0
    while i < n:
        j = i
        while j + 1 < n and v[order[j + 1]] == v[order[i]]:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            out[order[k]] = r
        i = j + 1
    return out


def pearson(x, y):
    mx, my = mean(x), mean(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    return sxy / (sxx * syy) ** 0.5


def spear(x, y):
    return pearson(ranks(x), ranks(y))


def tidy(ax):
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def panel(ax, x, y, title, xlab, ylab, mark=None):
    ax.scatter(x, y, s=52, color=DOT, edgecolor=INK, linewidth=0.8, zorder=4)
    if mark is not None:
        ax.scatter([x[mark]], [y[mark]], s=190, facecolor="none",
                   edgecolor=ACC, linewidth=2.0, zorder=5)
    r, rs = pearson(x, y), spear(x, y)
    ax.set_title(f"{title}\n$r = {r:.3f}$    $r_s = {rs:.3f}$", fontsize=11.5, pad=10)
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    tidy(ax)
    return r, rs


# ---------- 1. linear vs monotonic-but-curved ----------
xa = [1, 2, 3, 4, 5, 6, 7, 8]
ya = [5, 8, 11, 14, 17, 20, 23, 26]          # exactly linear
xb = [1, 2, 3, 4, 5, 6, 7, 8]
yb = [2, 3, 5, 9, 16, 28, 50, 90]            # increasing, strongly curved

fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.2))
v1 = panel(axes[0], xa, ya, "Linear", "$x$", "$y$")
v2 = panel(axes[1], xb, yb, "Curved, but always increasing", "$x$", "$y$")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-4-10-monotonic.svg"), format="svg", bbox_inches="tight")
plt.close(fig)

# ---------- 2. the effect of one outlier ----------
xc = [1, 2, 3, 4, 5, 6, 7, 8]
yc = [3, 5, 6, 8, 9, 11, 12, 14]
yd = [3, 5, 6, 8, 9, 11, 40, 14]             # 7th point moved far up

fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.2))
v3 = panel(axes[0], xc, yc, "No outlier", "$x$", "$y$")
v4 = panel(axes[1], xc, yd, "One outlier", "$x$", "$y$", mark=6)
axes[0].set_ylim(0, 44)
axes[1].set_ylim(0, 44)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-4-10-outlier.svg"), format="svg", bbox_inches="tight")
plt.close(fig)

print("wrote sl-4-10-monotonic.svg, sl-4-10-outlier.svg")
for name, (r, rs) in [("linear", v1), ("curved", v2), ("no outlier", v3), ("outlier", v4)]:
    print(f"  {name:11s} r = {r:.6f}   r_s = {rs:.6f}")
