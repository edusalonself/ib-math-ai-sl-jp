"""SL 2.6 の図を作る。ラベルはすべて英語。
   出力先: 02-functions/img/*.svg
   再生成: python3 figs/make_sl_2_6.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = os.path.join(os.path.dirname(__file__), "..", "02-functions", "img")
os.makedirs(OUT, exist_ok=True)

INK, GRID, LINE, ACC, GREEN = "#1f2328", "#dfe3e8", "#2874a6", "#c0392b", "#1e8449"
GREY, FILL = "#7a8592", "#e8f1fb"
plt.rcParams.update({
    "font.size": 11, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "text.color": INK, "xtick.color": INK, "ytick.color": INK,
    "svg.fonttype": "path",
})
BOX = dict(facecolor="white", edgecolor="none", pad=1.6, alpha=0.82)


# ================= 1. the modelling cycle =================
fig, ax = plt.subplots(figsize=(8.6, 5.4))

CARDS = [
    (0.50, 0.86, "1.  Pose a real-world problem", GREY),
    (0.84, 0.52, "2.  Develop and fit\nthe model", LINE),
    (0.50, 0.16, "3.  Test and reflect\nupon the model", ACC),
    (0.16, 0.52, "4.  Use the model", GREEN),
]
W, H = 0.30, 0.16
for (cx, cy, text, col) in CARDS:
    ax.add_patch(FancyBboxPatch((cx - W / 2, cy - H / 2), W, H,
                                boxstyle="round,pad=0.012,rounding_size=0.02",
                                facecolor="white", edgecolor=col, linewidth=1.8,
                                zorder=4))
    ax.annotate(text, (cx, cy), ha="center", va="center", fontsize=10.5,
                color=col, zorder=6)


def arc(p0, p1, rad, color=INK, style="-|>", lw=1.7, ls="-"):
    ax.add_patch(FancyArrowPatch(p0, p1, connectionstyle=f"arc3,rad={rad}",
                                 arrowstyle=style, color=color, linewidth=lw,
                                 linestyle=ls, mutation_scale=15, zorder=3))


arc((0.645, 0.83), (0.83, 0.615), -0.28)
arc((0.83, 0.425), (0.645, 0.205), -0.28)
arc((0.355, 0.205), (0.17, 0.425), -0.28)
arc((0.17, 0.615), (0.355, 0.83), -0.28)

# reject loop: test -> develop
arc((0.62, 0.19), (0.79, 0.44), 0.42, color=ACC, ls="--", lw=1.5)
ax.annotate("reject:\ngo back and change it", (0.90, 0.30), fontsize=9.5,
            color=ACC, ha="center", zorder=6)

ax.annotate("accept", (0.37, 0.30), fontsize=9.5, color=GREEN,
            ha="left", zorder=6)
ax.annotate("extend the problem", (0.37, 0.72), fontsize=9.5, color=GREY,
            ha="left", zorder=6)

ax.set_xlim(0, 1.06)
ax.set_ylim(0.02, 1.0)
ax.axis("off")
ax.set_title("The modelling process", fontsize=13, pad=6)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-2-6-cycle.svg"), format="svg", bbox_inches="tight")
plt.close(fig)

# ================= 2. good fit と bad fit =================
DX = np.array([1, 2, 3, 4, 5, 6])
DY = np.array([6.0, 8.6, 10.0, 9.7, 7.6, 4.0])

fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4))

# bad: linear
ax = axes[0]
ax.scatter(DX, DY, s=60, color=INK, zorder=6)
xs = np.linspace(0.4, 6.6, 200)
m, cc = np.polyfit(DX, DY, 1)
ax.plot(xs, m * xs + cc, color=ACC, linewidth=2.4, zorder=5)
ax.annotate("a linear model\ndoes not follow the shape", (3.5, 12.4),
            color=ACC, fontsize=11, ha="center", zorder=8)
ax.set_xlim(0, 7); ax.set_ylim(0, 14.6)
ax.set_xticks([1, 2, 3, 4, 5, 6]); ax.set_yticks([4, 8, 12])
ax.grid(True, color=GRID, linewidth=0.8); ax.set_axisbelow(True)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.set_title("Not appropriate", fontsize=11.5, pad=10)

# good: quadratic
ax = axes[1]
ax.scatter(DX, DY, s=60, color=INK, zorder=6)
q = np.polyfit(DX, DY, 2)
ax.plot(xs, np.polyval(q, xs), color=GREEN, linewidth=2.4, zorder=5)
ax.annotate("a quadratic model rises\nthen falls, like the data", (3.5, 12.4),
            color=GREEN, fontsize=11, ha="center", zorder=8)
ax.set_xlim(0, 7); ax.set_ylim(0, 14.6)
ax.set_xticks([1, 2, 3, 4, 5, 6]); ax.set_yticks([4, 8, 12])
ax.grid(True, color=GRID, linewidth=0.8); ax.set_axisbelow(True)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.set_title("Appropriate", fontsize=11.5, pad=10)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-2-6-fit.svg"), format="svg", bbox_inches="tight")
plt.close(fig)

# ================= 3. interpolation と extrapolation =================
fig, ax = plt.subplots(figsize=(8.6, 4.8))
h = lambda t: 6 * t + 76
ts = np.array([2, 4, 6, 8, 10])
ax.axvspan(2, 10, color=FILL, zorder=1)

xs = np.linspace(0, 42, 200)
ax.plot(xs, h(xs), color=GREY, linestyle="--", linewidth=1.8, zorder=3)
xin = np.linspace(2, 10, 100)
ax.plot(xin, h(xin), color=LINE, linewidth=2.8, zorder=5)
ax.scatter(ts, h(ts), s=62, color=INK, zorder=7)

ax.annotate("the data covers\nonly this range", (6, 300), fontsize=10.5,
            color=LINE, ha="center", zorder=8)
ax.annotate("interpolation\n(inside the data)", (6, 200), fontsize=10.5,
            color=LINE, ha="center", zorder=8)
ax.annotate("extrapolation\n(outside the data)", (27, 130), fontsize=10.5,
            color=ACC, ha="center", zorder=8)

ax.scatter([40], [h(40)], s=70, color=ACC, zorder=7)
ax.annotate("the model says 316 cm\nat age 40", xy=(40, h(40)), xytext=(30, 355),
            fontsize=10.5, color=ACC, ha="center", zorder=8,
            arrowprops=dict(arrowstyle="->", color=ACC, linewidth=1.4))

ax.set_xlim(0, 46); ax.set_ylim(0, 420)
ax.set_xticks([2, 10, 20, 30, 40]); ax.set_yticks([100, 200, 300, 400])
ax.set_xlabel("age $t$ (years)")
ax.set_ylabel("height $h$ (cm)")
ax.grid(True, color=GRID, linewidth=0.8); ax.set_axisbelow(True)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.set_title("The danger of extrapolation:  $h(t) = 6t + 76$", fontsize=12.5,
             pad=10)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-2-6-extrapolation.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)

print("wrote sl-2-6-cycle.svg, sl-2-6-fit.svg, sl-2-6-extrapolation.svg")
print("check h(2), h(10), h(40) =", h(2), h(10), h(40))
print("check data used for fit figure:", list(zip(DX, DY)))
