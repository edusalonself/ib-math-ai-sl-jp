"""SL 4.8 の図を作る。ラベルはすべて英語。
   出力先: 04-statistics-and-probability/img/*.svg
   再生成: python3 figs/make_sl_4_8.py
"""
import os
from math import comb
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "..", "04-statistics-and-probability", "img")
os.makedirs(OUT, exist_ok=True)

INK, GRID, BAR, ACC, HI = "#1f2328", "#dfe3e8", "#9dc3ea", "#c0392b", "#f0b27a"
plt.rcParams.update({
    "font.size": 11, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "text.color": INK, "xtick.color": INK, "ytick.color": INK,
    "svg.fonttype": "path",
})


def pdf(n, p, x):
    return comb(n, x) * p ** x * (1 - p) ** (n - x)


def tidy(ax):
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


# ---------- 1. p が変わると形が変わる ----------
n = 10
fig, axes = plt.subplots(1, 3, figsize=(10.6, 3.4), sharey=True)
for ax, p in zip(axes, (0.2, 0.5, 0.8)):
    xs = list(range(n + 1))
    ys = [pdf(n, p, x) for x in xs]
    ax.bar(xs, ys, width=0.72, color=BAR, edgecolor=INK, linewidth=0.9, zorder=3)
    ax.plot([n * p, n * p], [0, 0.33], "--", color=ACC, linewidth=1.4,
            zorder=5, alpha=0.9)
    ax.plot([n * p], [-0.016], marker="^", color=ACC, markersize=11,
            clip_on=False, zorder=6)
    ax.set_title(f"$B(10,\\ {p})$   $\\mathrm{{E}}(X) = {n * p:g}$",
                 fontsize=11.5, pad=9)
    ax.set_xlabel("$x$")
    ax.set_xticks([0, 2, 4, 6, 8, 10])
    ax.set_xlim(-0.8, 10.8)
    tidy(ax)
axes[0].set_ylabel("$\\mathrm{P}(X = x)$")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-4-8-shapes.svg"), format="svg", bbox_inches="tight")
plt.close(fig)

# ---------- 2. at most / at least は残りどうし ----------
n, p = 20, 0.15
xs = list(range(0, 13))
ys = [pdf(n, p, x) for x in xs]
lower = sum(pdf(n, p, k) for k in range(0, 4))
upper = 1 - lower

fig, axes = plt.subplots(1, 2, figsize=(10.6, 3.6), sharey=True)
for ax, (lo, hi, lab, val) in zip(
    axes,
    [(0, 3, "$\\mathrm{P}(X \\leq 3)$", lower),
     (4, 12, "$\\mathrm{P}(X \\geq 4)$", upper)],
):
    cols = [HI if lo <= x <= hi else "#eef2f6" for x in xs]
    edges = [INK if lo <= x <= hi else "#b9c2cc" for x in xs]
    ax.bar(xs, ys, width=0.72, color=cols, edgecolor=edges, linewidth=0.9, zorder=3)
    ax.set_title(f"{lab} $= {val:.3f}$", fontsize=12, pad=9)
    ax.set_xlabel("$x$")
    ax.set_xticks([0, 2, 4, 6, 8, 10, 12])
    ax.set_xlim(-0.8, 12.8)
    tidy(ax)
axes[0].set_ylabel("$\\mathrm{P}(X = x)$")
fig.suptitle("$X \\sim B(20,\\ 0.15)$    the two shaded parts add to $1$",
             fontsize=12, y=1.0)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-4-8-ranges.svg"), format="svg", bbox_inches="tight")
plt.close(fig)

print("wrote sl-4-8-shapes.svg, sl-4-8-ranges.svg")
print("P(X<=3) =", lower, "  P(X>=4) =", upper, "  sum =", lower + upper)
