"""SL 4.3 の図を作る。ラベルはすべて英語。
   出力先: ai-sl/04-statistics-and-probability/img/*.svg
   再生成: python3 figs/ai-sl/make_sl_4_3.py
"""
import os
from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-sl", "04-statistics-and-probability", "img")
os.makedirs(OUT, exist_ok=True)

INK, GRID, DOT, ACC = "#1f2328", "#dfe3e8", "#3b82c4", "#c0392b"
plt.rcParams.update({
    "font.size": 11, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "text.color": INK, "xtick.color": INK, "ytick.color": INK,
    "svg.fonttype": "path",
})


def dots(ax, data, y, colour=DOT, step=0.13):
    """同じ値は縦に積む dot plot。"""
    for v, k in sorted(Counter(data).items()):
        for j in range(k):
            ax.plot(v, y + j * step, "o", color=colour, markersize=7,
                    markeredgecolor="white", markeredgewidth=0.8, zorder=3)


def mean_line(ax, m, y0, y1, label=None):
    ax.plot([m, m], [y0, y1], "--", color=ACC, linewidth=1.4, zorder=2)
    if label:
        ax.annotate(label, (m, y1), color=ACC, fontsize=10,
                    ha="center", va="bottom")


def finish(fig, ax, name):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), format="svg", bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


# ---------- 1. 平均は同じ、ばらつきが違う ----------
A = [46, 48, 49, 50, 51, 52, 54]
B = [38, 44, 47, 50, 53, 56, 62]

fig, ax = plt.subplots(figsize=(6.6, 3.0))
dots(ax, A, 1.0)
dots(ax, B, 0.0)
mean_line(ax, 50, -0.25, 1.45, "mean = 50")

ax.set_yticks([0.0, 1.0])
ax.set_yticklabels(["Set B\nsd = 7.35", "Set A\nsd = 2.45"], fontsize=10)
ax.tick_params(axis="y", length=0)
ax.set_xlim(35, 66)
ax.set_ylim(-0.45, 1.75)
ax.set_xlabel("Value")
ax.set_xticks(range(35, 70, 5))
ax.xaxis.grid(True, color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
finish(fig, ax, "sl-4-3-spread.svg")

# ---------- 2. 定数を足す・掛ける ----------
BASE = [2, 4, 4, 4, 5, 5, 7, 9]          # mean 5, sd 2
ADD = [v + 3 for v in BASE]              # mean 8, sd 2
MUL = [v * 2 for v in BASE]              # mean 10, sd 4

fig, ax = plt.subplots(figsize=(6.6, 3.6))
for data, y, m, lab in ((BASE, 2.0, 5, "mean 5, sd 2"),
                        (ADD, 1.0, 8, "mean 8, sd 2"),
                        (MUL, 0.0, 10, "mean 10, sd 4")):
    ax.plot([m, m], [y - 0.22, y + 0.62], "--", color=ACC, linewidth=1.3, zorder=1)
    dots(ax, data, y, step=0.11)
    ax.annotate(lab, (m + 0.35, y + 0.62), color=ACC, ha="left", va="top", fontsize=10)

ax.set_yticks([0.0, 1.0, 2.0])
ax.set_yticklabels(["multiply by 2", "add 3", "original"], fontsize=10, style="italic")
ax.tick_params(axis="y", length=0)
ax.set_xlim(0, 20)
ax.set_ylim(-0.45, 2.95)
ax.set_xlabel("Value")
ax.set_xticks(range(0, 21, 2))
ax.xaxis.grid(True, color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
finish(fig, ax, "sl-4-3-changes.svg")
