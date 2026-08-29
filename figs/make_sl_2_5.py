"""SL 2.5 の図を作る。ラベルはすべて英語。
   出力先: 02-functions/img/*.svg
   再生成: python3 figs/make_sl_2_5.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "..", "02-functions", "img")
os.makedirs(OUT, exist_ok=True)

INK, GRID, LINE, ACC, GREEN = "#1f2328", "#dfe3e8", "#2874a6", "#c0392b", "#1e8449"
GREY = "#7a8592"
plt.rcParams.update({
    "font.size": 11, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "text.color": INK, "xtick.color": INK, "ytick.color": INK,
    "svg.fonttype": "path",
})
BOX = dict(facecolor="white", edgecolor="none", pad=1.6, alpha=0.8)


def bare(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_axisbelow(True)


# ================= 1. 6つのモデルの形 =================
fig, axes = plt.subplots(2, 3, figsize=(11.4, 6.4))

# linear
ax = axes[0][0]
xs = np.linspace(-1.2, 4.2, 200)
ax.plot(xs, 0.9 * xs + 1.2, color=LINE, linewidth=2.4)
bare(ax, (-1.8, 4.8), (-1.6, 5.6))
ax.set_title("Linear\n$f(x) = mx + c$", fontsize=11)

# quadratic
ax = axes[0][1]
xs = np.linspace(-0.8, 4.8, 300)
ax.plot(xs, 0.8 * (xs - 2) ** 2 - 2, color=LINE, linewidth=2.4)
bare(ax, (-1.6, 5.6), (-3.4, 5.2))
ax.set_title("Quadratic\n$f(x) = ax^{2} + bx + c$", fontsize=11)

# exponential
ax = axes[0][2]
xs = np.linspace(-1.6, 3.4, 300)
ax.plot(xs, 1.4 * 2.0 ** xs + 1, color=LINE, linewidth=2.4)
ax.plot([-2.2, 4.2], [1, 1], color=ACC, linestyle="--", linewidth=1.5)
ax.annotate("$y = c$", (4.0, 1.35), color=ACC, fontsize=10, ha="right")
bare(ax, (-2.4, 4.4), (-1.4, 12.0))
ax.set_title("Exponential\n$f(x) = ka^{x} + c$", fontsize=11)

# variation (n < 0)
ax = axes[1][0]
xr = np.linspace(0.42, 4.4, 300)
xl = np.linspace(-4.4, -0.42, 300)
ax.plot(xr, 2.0 / xr, color=GREEN, linewidth=2.4)
ax.plot(xl, 2.0 / xl, color=GREEN, linewidth=2.4)
ax.plot([0, 0], [-5.2, 5.2], color=ACC, linestyle="--", linewidth=1.5)
bare(ax, (-4.8, 4.8), (-5.4, 5.4))
ax.set_title("Direct / inverse variation\n$f(x) = ax^{n}$", fontsize=11)

# cubic
ax = axes[1][1]
xs = np.linspace(-1.5, 3.5, 300)
ax.plot(xs, xs ** 3 - 3 * xs ** 2 - xs + 3, color=GREEN, linewidth=2.4)
bare(ax, (-2.4, 4.4), (-6.0, 7.2))
ax.set_title("Cubic\n$f(x) = ax^{3} + bx^{2} + cx + d$", fontsize=11)

# sinusoidal
ax = axes[1][2]
ts = np.linspace(0, 760, 600)
ax.plot(ts, 2.2 * np.sin(np.radians(ts)) + 2.6, color=GREEN, linewidth=2.4)
ax.plot([-40, 800], [2.6, 2.6], color=ACC, linestyle="--", linewidth=1.5)
ax.annotate("$y = d$", (780, 2.95), color=ACC, fontsize=10, ha="right")
bare(ax, (-90, 830), (-1.0, 6.4))
ax.set_title("Sinusoidal\n$f(x) = a\\sin(bx) + d$", fontsize=11)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-2-5-models.svg"), format="svg", bbox_inches="tight")
plt.close(fig)

# ================= 2. piecewise linear（プールの深さ） =================
fig, ax = plt.subplots(figsize=(7.6, 4.4))
x1 = np.linspace(0, 6, 100)
x2 = np.linspace(6, 14, 100)
ax.plot(x1, np.full_like(x1, 1.0), color=LINE, linewidth=2.6, zorder=5)
ax.plot(x2, 1.0 + 0.2 * (x2 - 6), color=GREEN, linewidth=2.6, zorder=5)
ax.scatter([6], [1.0], s=58, color=ACC, edgecolor=INK, linewidth=0.9, zorder=7)

ax.annotate("flat:  $d = 1.0$", (3.0, 1.16), color=LINE, fontsize=11,
            ha="center", bbox=BOX, zorder=8)
ax.annotate("sloping:  $d = 1.0 + 0.2(x - 6)$", (10.6, 1.55), color=GREEN,
            fontsize=11, ha="center", bbox=BOX, zorder=8)
ax.annotate("the rule changes here\n$x = 6$", (6, 0.72), color=ACC, fontsize=10,
            ha="center", va="top", bbox=BOX, zorder=8)
ax.plot([6, 6], [0, 1.0], color=ACC, linestyle=":", linewidth=1.4, zorder=3)

ax.set_xlim(-0.6, 15.4)
ax.set_ylim(0, 3.1)
ax.set_xticks([2, 4, 6, 8, 10, 12, 14])
ax.set_yticks([1, 2, 3])
ax.set_xlabel("horizontal distance $x$ (m)")
ax.set_ylabel("depth $d$ (m)")
ax.grid(True, color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.set_title("A piecewise linear model:  the depth of a swimming pool",
             fontsize=12, pad=10)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-2-5-piecewise.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)

# ================= 3. exponential growth と decay =================
fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4))

# growth
ax = axes[0]
xs = np.linspace(0, 12, 300)
G = lambda t: 30 * 1.25 ** t + 10
ax.plot(xs, G(xs), color=LINE, linewidth=2.4, zorder=5)
ax.plot([-0.8, 12.8], [10, 10], color=ACC, linestyle="--", linewidth=1.8, zorder=4)
ax.scatter([0], [G(0)], s=54, color=LINE, edgecolor=INK, linewidth=0.9, zorder=7)
ax.annotate("$f(0) = k + c = 40$", xy=(0, 40), xytext=(1.8, 260),
            color=LINE, fontsize=11, ha="left", zorder=8,
            arrowprops=dict(arrowstyle="->", color=LINE, linewidth=1.3))
ax.annotate("$y = c = 10$", (12.4, 15), color=ACC, fontsize=11, ha="right",
            bbox=BOX, zorder=8)
ax.set_xticks([4, 8, 12]); ax.set_yticks([40, 200, 400])
ax.set_xlim(-1.4, 13.6); ax.set_ylim(-40, 480)
ax.spines["left"].set_position("zero"); ax.spines["bottom"].set_position("zero")
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.set_title("Growth:  $f(x) = 30(1.25)^{x} + 10$", fontsize=11.5, pad=10)

# decay
ax = axes[1]
xs = np.linspace(0, 60, 400)
D = lambda t: 180 * 0.94 ** t + 20
ax.plot(xs, D(xs), color=GREEN, linewidth=2.4, zorder=5)
ax.plot([-4, 64], [20, 20], color=ACC, linestyle="--", linewidth=1.8, zorder=4)
ax.scatter([0], [D(0)], s=54, color=GREEN, edgecolor=INK, linewidth=0.9, zorder=7)
ax.annotate("$f(0) = k + c = 200$", (3, 196), color=GREEN, fontsize=11,
            ha="left", bbox=BOX, zorder=8)
ax.annotate("$y = c = 20$", (62, 6), color=ACC, fontsize=11, ha="right",
            bbox=BOX, zorder=8)
ax.set_xticks([20, 40, 60]); ax.set_yticks([20, 100, 200])
ax.set_xlim(-7, 68); ax.set_ylim(-24, 240)
ax.spines["left"].set_position("zero"); ax.spines["bottom"].set_position("zero")
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.set_title("Decay:  $f(x) = 180(0.94)^{x} + 20$", fontsize=11.5, pad=10)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-2-5-exponential.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)

# ================= 4. sinusoidal のラベル =================
fig, ax = plt.subplots(figsize=(9.6, 4.8))
ts = np.linspace(0, 26, 800)
S = lambda t: 4 * np.sin(np.radians(30 * t)) + 7
ax.plot(ts, S(ts), color=LINE, linewidth=2.6, zorder=5)
ax.plot([-1, 26.6], [7, 7], color=ACC, linestyle="--", linewidth=1.8, zorder=4)
ax.plot([-1, 26.6], [11, 11], color=GREY, linestyle=":", linewidth=1.3, zorder=3)
ax.plot([-1, 26.6], [3, 3], color=GREY, linestyle=":", linewidth=1.3, zorder=3)

# amplitude arrow
ax.annotate("", xy=(3, 11), xytext=(3, 7),
            arrowprops=dict(arrowstyle="<->", color=GREEN, linewidth=1.6))
ax.annotate("amplitude $= |a| = 4$", (3.5, 9.0), color=GREEN, fontsize=11,
            ha="left", bbox=BOX, zorder=8)

# period arrow
ax.annotate("", xy=(15, 1.3), xytext=(3, 1.3),
            arrowprops=dict(arrowstyle="<->", color=GREEN, linewidth=1.6))
ax.annotate("period $= \\dfrac{360}{b} = 12$", (9, 0.15), color=GREEN,
            fontsize=11, ha="center", bbox=BOX, zorder=8)

ax.annotate("principal axis\n$y = d = 7$", (26.9, 7), color=ACC, fontsize=11,
            ha="left", va="center", zorder=8)
ax.annotate("maximum $= d + |a| = 11$", (26.9, 11), color=GREY, fontsize=10,
            ha="left", va="center", zorder=8)
ax.annotate("minimum $= d - |a| = 3$", (26.9, 3), color=GREY, fontsize=10,
            ha="left", va="center", zorder=8)

ax.set_xticks([3, 6, 9, 12, 15, 18, 21, 24])
ax.set_yticks([3, 7, 11])
ax.set_xlim(-1.2, 38.0); ax.set_ylim(-0.6, 13.6)
ax.spines["left"].set_position("zero"); ax.spines["bottom"].set_position("zero")
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.grid(True, color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
ax.set_title("$y = 4\\sin(30x) + 7$   (degrees)", fontsize=12.5, pad=10)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-2-5-sinusoid.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)

print("wrote sl-2-5-models.svg, sl-2-5-piecewise.svg, sl-2-5-exponential.svg, "
      "sl-2-5-sinusoid.svg")
print("check pool: d(6) =", 1.0, " d(14) =", 1.0 + 0.2 * 8)
print("check growth f(0) =", 30 * 1.25 ** 0 + 10, " decay f(0) =", 180 + 20)
print("check sinusoid: max", 7 + 4, " min", 7 - 4, " period", 360 / 30,
      " S(3) =", round(float(S(3)), 6))
