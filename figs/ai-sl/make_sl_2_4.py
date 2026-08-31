"""SL 2.4 の図を作る。ラベルはすべて英語。
   出力先: ai-sl/02-functions/img/*.svg
   再生成: python3 figs/ai-sl/make_sl_2_4.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-sl", "02-functions", "img")
os.makedirs(OUT, exist_ok=True)

INK, GRID, LINE, ACC, GREEN = "#1f2328", "#dfe3e8", "#2874a6", "#c0392b", "#1e8449"
GREY = "#7a8592"
plt.rcParams.update({
    "font.size": 11, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "text.color": INK, "xtick.color": INK, "ytick.color": INK,
    "svg.fonttype": "path",
})
BOX = dict(facecolor="white", edgecolor="none", pad=1.6, alpha=0.78)


def origin_axes(ax, xlim, ylim, grid=False):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    if grid:
        ax.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_xlabel("$x$", loc="right")
    ax.set_ylabel("$y$", loc="top", rotation=0)


# ================= 1. key features =================
fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.8))

# --- 左：quadratic  f(x) = x^2 - 6x + 5 ---
ax = axes[0]
q = lambda x: x ** 2 - 6 * x + 5
xs = np.linspace(-0.7, 6.7, 400)
ax.plot(xs, q(xs), color=LINE, linewidth=2.4, zorder=5)

ax.plot([3, 3], [-4.6, 6.2], color=GREY, linestyle="--", linewidth=1.5, zorder=3)
ax.annotate("axis of symmetry\n$x = 3$", (3, 6.0), fontsize=10, color=GREY,
            ha="center", va="bottom", bbox=BOX, zorder=8)

for (x, y, lab, dx, dy, ha) in [
        (0, 5, "$y$-intercept\n$(0,\\ 5)$", -8, 4, "right"),
        (1, 0, "zero\n$x = 1$", -10, -34, "right"),
        (5, 0, "zero\n$x = 5$", 12, 10, "left"),
        (3, -4, "vertex / minimum\n$(3,\\ -4)$", 12, -6, "left")]:
    ax.scatter([x], [y], s=56, color=ACC, edgecolor=INK, linewidth=0.9, zorder=7)
    ax.annotate(lab, (x, y), textcoords="offset points", xytext=(dx, dy),
                fontsize=10, color=ACC, ha=ha, bbox=BOX, zorder=8)

ax.set_xticks([]); ax.set_yticks([])
origin_axes(ax, (-1.6, 8.4), (-6.4, 8.6))
ax.set_title("A quadratic:  symmetry, vertex, intercepts", fontsize=11.5, pad=10)

# --- 右：cubic  g(x) = x^3 - 3x^2 - x + 3 = (x-1)(x+1)(x-3) ---
ax = axes[1]
g = lambda x: x ** 3 - 3 * x ** 2 - x + 3
xs = np.linspace(-1.5, 3.5, 400)
ax.plot(xs, g(xs), color=GREEN, linewidth=2.4, zorder=5)

xmax = 1 - np.sqrt(48) / 6
xmin = 1 + np.sqrt(48) / 6
for (x, y, lab, dx, dy, ha) in [
        (-1, 0, "zero", -9, 10, "right"),
        (1, 0, "zero", 0, -26, "center"),
        (3, 0, "zero", 10, 10, "left"),
        (xmax, g(xmax), "local maximum", -14, 6, "right"),
        (xmin, g(xmin), "local minimum", 12, -6, "left")]:
    ax.scatter([x], [y], s=56, color=ACC, edgecolor=INK, linewidth=0.9, zorder=7)
    ax.annotate(lab, (x, y), textcoords="offset points", xytext=(dx, dy),
                fontsize=10, color=ACC, ha=ha, bbox=BOX, zorder=8)

ax.set_xticks([]); ax.set_yticks([])
origin_axes(ax, (-2.5, 4.4), (-6.2, 7.6))
ax.set_title("A cubic:  zeros, local maximum, local minimum",
             fontsize=11.5, pad=10)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-2-4-features.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)

# ================= 2. asymptotes =================
fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4))

# --- 左：horizontal asymptote  y = 22 ---
ax = axes[0]
T = lambda t: 65 * 0.93 ** t + 22
ts = np.linspace(0, 60, 400)
ax.plot(ts, T(ts), color=LINE, linewidth=2.4, zorder=5)
ax.plot([-2, 62], [22, 22], color=ACC, linestyle="--", linewidth=1.8, zorder=4)
ax.annotate("horizontal asymptote  $y = 22$", (66, 14), fontsize=10.5,
            color=ACC, ha="right", bbox=BOX, zorder=8)
ax.annotate("the curve gets closer and closer,\nbut never reaches it",
            (40, 42), fontsize=9.5, color=GREY, ha="center", bbox=BOX, zorder=8)
ax.scatter([0], [T(0)], s=52, color=LINE, edgecolor=INK, linewidth=0.9, zorder=7)
ax.annotate("$(0,\\ 87)$", (0, T(0)), textcoords="offset points", xytext=(9, 2),
            fontsize=10, color=LINE, bbox=BOX, zorder=8)
ax.set_xticks([20, 40, 60]); ax.set_yticks([22, 50, 80])
origin_axes(ax, (-6, 68), (-6, 100))
ax.set_title("Horizontal asymptote:  $y = 65(0.93)^{x} + 22$",
             fontsize=11.5, pad=10)

# --- 右：vertical asymptote  x = 0 ---
ax = axes[1]
h = lambda x: 12 / x + 3
xl = np.linspace(-9, -0.35, 400)
xr = np.linspace(0.35, 9, 400)
ax.plot(xl, h(xl), color=GREEN, linewidth=2.4, zorder=5)
ax.plot(xr, h(xr), color=GREEN, linewidth=2.4, zorder=5)
ax.plot([0, 0], [-22, 26], color=ACC, linestyle="--", linewidth=1.8, zorder=4)
ax.plot([-9.5, 9.5], [3, 3], color=LINE, linestyle="--", linewidth=1.8, zorder=4)
ax.annotate("vertical asymptote\n$x = 0$", (0.8, -16), fontsize=10.5, color=ACC,
            ha="left", bbox=BOX, zorder=8)
ax.annotate("horizontal asymptote  $y = 3$", (-9.2, 6.5), fontsize=10.5,
            color=LINE, ha="left", bbox=BOX, zorder=8)
ax.scatter([-4], [0], s=52, color=GREEN, edgecolor=INK, linewidth=0.9, zorder=7)
ax.annotate("$(-4,\\ 0)$", (-4, 0), textcoords="offset points", xytext=(0, -38),
            fontsize=10, color=GREEN, ha="center", bbox=BOX, zorder=8)
ax.set_xticks([-8, -4, 4, 8]); ax.set_yticks([3, 10, 20])
origin_axes(ax, (-10.5, 11.5), (-22, 27))
ax.set_title("Vertical asymptote:  $y = \\dfrac{12}{x} + 3$",
             fontsize=11.5, pad=10)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-2-4-asymptotes.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)

# ================= 3. intersection =================
fig, ax = plt.subplots(figsize=(7.2, 5.0))
f = lambda x: x ** 2 - 4 * x + 5
gg = lambda x: x + 1
xs = np.linspace(-0.6, 5.4, 400)
ax.plot(xs, f(xs), color=LINE, linewidth=2.4, zorder=5)
ax.plot(xs, gg(xs), color=GREEN, linewidth=2.2, zorder=5)

for (x, y) in [(1, 2), (4, 5)]:
    ax.scatter([x], [y], s=62, color=ACC, edgecolor=INK, linewidth=0.9, zorder=7)
ax.annotate("$(1,\\ 2)$", (1, 2), textcoords="offset points", xytext=(-10, 10),
            fontsize=11, color=ACC, ha="right", bbox=BOX, zorder=8)
ax.annotate("$(4,\\ 5)$", (4, 5), textcoords="offset points", xytext=(10, -4),
            fontsize=11, color=ACC, ha="left", bbox=BOX, zorder=8)
ax.annotate("$y = x^{2} - 4x + 5$", (4.55, 7.4), color=LINE, fontsize=11.5,
            ha="center", bbox=BOX, zorder=8)
ax.annotate("$y = x + 1$", (0.35, 3.4), color=GREEN, fontsize=11.5,
            ha="left", bbox=BOX, zorder=8)
ax.annotate("two curves can cross more than once",
            (2.6, -1.6), fontsize=10, color=GREY, ha="center", bbox=BOX, zorder=8)

ax.set_xticks([1, 2, 3, 4, 5]); ax.set_yticks([2, 4, 6, 8])
origin_axes(ax, (-1.2, 6.4), (-2.6, 9.4), grid=True)
ax.set_title("Points of intersection", fontsize=12.5, pad=10)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-2-4-intersection.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)

print("wrote sl-2-4-features.svg, sl-2-4-asymptotes.svg, sl-2-4-intersection.svg")
print("check quadratic: zeros", q(1), q(5), " vertex", q(3), " y-int", q(0))
print("check cubic: zeros", g(-1), g(1), g(3), " y-int", g(0))
print("check cubic turning points:", round(xmax, 4), round(g(xmax), 4),
      "/", round(xmin, 4), round(g(xmin), 4))
print("check T(0) =", T(0), " asymptote 22")
print("check h(-4) =", h(-4), " asymptotes x=0, y=3")
print("check intersection:", f(1), gg(1), "/", f(4), gg(4))
