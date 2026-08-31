"""SL 2.3 の図を作る。ラベルはすべて英語。
   出力先: ai-sl/02-functions/img/*.svg
   再生成: python3 figs/ai-sl/make_sl_2_3.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-sl", "02-functions", "img")
os.makedirs(OUT, exist_ok=True)

INK, GRID, LINE, ACC, GREEN = "#1f2328", "#dfe3e8", "#2874a6", "#c0392b", "#1e8449"
plt.rcParams.update({
    "font.size": 11, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "text.color": INK, "xtick.color": INK, "ytick.color": INK,
    "svg.fonttype": "path",
})


def origin_axes(ax, xlim, ylim, grid=True):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    if grid:
        ax.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


F = lambda x: x ** 2 - 4 * x + 3      # roots 1, 3 ; vertex (2, -1) ; y-int 3

# ---------- 1. Draw と Sketch の違い ----------
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.6))

# 左：Draw（正確・目盛りあり・点をプロット）
ax = axes[0]
xs = np.linspace(-0.6, 4.6, 300)
ax.plot(xs, F(xs), color=LINE, linewidth=2.0, zorder=4)
px = [0, 1, 2, 3, 4]
ax.scatter(px, [F(x) for x in px], s=48, color=LINE, edgecolor=INK,
           linewidth=0.9, zorder=6)
ax.set_xticks([1, 2, 3, 4])
ax.set_yticks([-1, 1, 2, 3])
ax.set_xlabel("$x$", loc="right")
ax.set_ylabel("$y$", loc="top", rotation=0)
origin_axes(ax, (-0.9, 4.9), (-1.9, 4.2), grid=True)
ax.set_title("Draw:  accurate, to scale, points plotted", fontsize=11.5, pad=10)

# 右：Sketch（形と特徴・ラベルあり・目盛りなし）
ax = axes[1]
ax.plot(xs, F(xs), color=GREEN, linewidth=2.4, zorder=4)
for (x, y, lab, dx, dy) in [(0, 3, "$(0,\\ 3)$", 6, 4),
                            (1, 0, "$(1,\\ 0)$", -46, 6),
                            (3, 0, "$(3,\\ 0)$", 10, 14),
                            (2, -1, "$(2,\\ -1)$\nminimum", -6, -34)]:
    ax.scatter([x], [y], s=48, color=GREEN, edgecolor=INK, linewidth=0.9, zorder=6)
    ax.annotate(lab, (x, y), textcoords="offset points", xytext=(dx, dy),
                fontsize=10.5, color=ACC)
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel("$x$", loc="right")
ax.set_ylabel("$y$", loc="top", rotation=0)
origin_axes(ax, (-0.9, 4.9), (-1.9, 4.2), grid=False)
ax.set_title("Sketch:  shape and key features, labelled", fontsize=11.5, pad=10)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-2-3-draw-sketch.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)

# ---------- 2. 何にラベルを付けるか ----------
fig, ax = plt.subplots(figsize=(7.6, 5.0))
xs = np.linspace(-0.7, 4.7, 300)
ax.plot(xs, F(xs), color=LINE, linewidth=2.4, zorder=4)

marks = [(0, 3, "$y$-intercept", 10, 6),
         (1, 0, "$x$-intercept", -78, 12),
         (3, 0, "$x$-intercept", 20, -26),
         (2, -1, "minimum", 8, -8)]
for (x, y, lab, dx, dy) in marks:
    ax.scatter([x], [y], s=56, color=ACC, edgecolor=INK, linewidth=0.9, zorder=6)
    ax.annotate(lab, (x, y), textcoords="offset points", xytext=(dx, dy),
                fontsize=10.5, color=ACC,
                ha="center" if dx == 0 else "left")

ax.annotate("$y = f(x)$", (4.15, 3.1), fontsize=12, color=LINE)
ax.annotate("label the axes", (5.25, -1.0), fontsize=10, color=GREEN,
            ha="right")
ax.annotate("", xy=(5.1, -0.06), xytext=(4.75, -0.85),
            arrowprops=dict(arrowstyle="->", color=GREEN, linewidth=1.3))
ax.annotate("give the domain used", (2.4, -1.75), fontsize=10, color=GREEN,
            ha="center")
ax.plot([-0.5, 4.5], [-1.55, -1.55], color=GREEN, linewidth=2.0,
        solid_capstyle="butt", zorder=5)
for xx in (-0.5, 4.5):
    ax.plot([xx], [-1.55], marker="|", color=GREEN, markersize=9, zorder=5)

ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel("$x$", loc="right")
ax.set_ylabel("$y$", loc="top", rotation=0)
origin_axes(ax, (-1.0, 5.3), (-2.1, 4.3), grid=False)
ax.set_title("What to label on a sketch", fontsize=12.5, pad=10)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-2-3-labels.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)

# ---------- 3. 和のグラフは、縦に足す ----------
f = lambda x: 0.5 * x ** 2
g = lambda x: 3 - x
h = lambda x: 0.5 * x ** 2 - x + 3

fig, ax = plt.subplots(figsize=(7.4, 5.0))
xs = np.linspace(-1.2, 4.4, 300)
ax.plot(xs, f(xs), color=LINE, linewidth=2.0, zorder=4)
ax.plot(xs, g(xs), color=GREEN, linewidth=2.0, zorder=4)
ax.plot(xs, h(xs), color=ACC, linewidth=2.6, zorder=5)

ax.annotate("$f(x) = 0.5x^{2}$", (-1.55, 1.4), color=LINE, fontsize=11.5)
ax.annotate("$g(x) = 3 - x$", (3.35, -1.75), color=GREEN, fontsize=11.5)
ax.annotate("$f(x) + g(x)$", (-1.55, 7.4), color=ACC, fontsize=11.5)

X = 2.0
ax.plot([X, X], [0, h(X)], color="#909aa4", linestyle=":", linewidth=1.4, zorder=3)
for yy, col in [(f(X), LINE), (g(X), GREEN), (h(X), ACC)]:
    ax.scatter([X], [yy], s=54, color=col, edgecolor=INK, linewidth=0.9, zorder=7)
BOX = dict(facecolor="white", edgecolor="none", pad=1.6, alpha=0.78)
ax.annotate("$f(2) = 2$", (X, f(X)), textcoords="offset points", xytext=(11, -4),
            color=LINE, fontsize=10.5, bbox=BOX, zorder=8)
ax.annotate("$g(2) = 1$", (X, g(X)), textcoords="offset points", xytext=(11, -14),
            color=GREEN, fontsize=10.5, bbox=BOX, zorder=8)
ax.annotate("$2 + 1 = 3$", (X, h(X)), textcoords="offset points", xytext=(11, 4),
            color=ACC, fontsize=11, bbox=BOX, zorder=8)

ax.set_xticks([-1, 1, 2, 3, 4])
ax.set_yticks([2, 4, 6, 8])
ax.set_xlabel("$x$", loc="right")
ax.set_ylabel("$y$", loc="top", rotation=0)
origin_axes(ax, (-1.9, 5.4), (-2.4, 9.6))
ax.set_title("The sum of two functions is added vertically",
             fontsize=12.5, pad=18)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-2-3-sum.svg"), format="svg", bbox_inches="tight")
plt.close(fig)

print("wrote sl-2-3-draw-sketch.svg, sl-2-3-labels.svg, sl-2-3-sum.svg")
print("check F: roots", F(1), F(3), " vertex", F(2), " y-int", F(0))
print("check sum at x=2:", f(2), "+", g(2), "=", h(2))
