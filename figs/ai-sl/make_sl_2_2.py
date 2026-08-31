"""SL 2.2 の図を作る。ラベルはすべて英語。
   出力先: ai-sl/02-functions/img/*.svg
   再生成: python3 figs/ai-sl/make_sl_2_2.py
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


def axes_through_origin(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


# ---------- 1. domain and range:  f(x) = sqrt(2 - x) ----------
fig, ax = plt.subplots(figsize=(7.6, 4.6))
x = np.linspace(-7, 2, 400)
ax.plot(x, np.sqrt(2 - x), color=LINE, linewidth=2.4, zorder=5)
ax.scatter([2], [0], s=62, color=LINE, edgecolor=INK, linewidth=0.9, zorder=6)

# domain bar on the x-axis
ax.plot([-7.4, 2], [-0.42, -0.42], color=ACC, linewidth=3.0,
        solid_capstyle="butt", zorder=6, clip_on=False)
ax.plot([2], [-0.42], marker="o", color=ACC, markersize=7, zorder=7, clip_on=False)
ax.annotate("domain:  $x \\leq 2$", (-2.6, -0.72), color=ACC, fontsize=12.5,
            ha="center", annotation_clip=False)

# range bar on the y-axis
ax.plot([-7.9, -7.9], [0, 3.2], color=GREEN, linewidth=3.0,
        solid_capstyle="butt", zorder=6, clip_on=False)
ax.plot([-7.9], [0], marker="o", color=GREEN, markersize=7, zorder=7, clip_on=False)
ax.annotate("range:  $f(x) \\geq 0$", (-7.6, 2.05), color=GREEN, fontsize=12.5,
            rotation=90, va="center", annotation_clip=False)

ax.annotate("$f(x) = \\sqrt{2 - x}$", (-5.6, 1.5), color=LINE, fontsize=13.5)
ax.set_xticks([-6, -4, -2, 2])
ax.set_yticks([1, 2, 3])
axes_through_origin(ax, (-8.4, 3.4), (-0.95, 3.5))
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-2-2-domain-range.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)

# ---------- 2. is it a function?  (vertical line test) ----------
fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.2))

ax = axes[0]
xs = np.linspace(-2.6, 2.6, 300)
ax.plot(xs, 0.6 * xs ** 3 - 1.2 * xs, color=LINE, linewidth=2.4, zorder=5)
ax.axvline(1.3, color=ACC, linestyle="--", linewidth=1.6, zorder=4)
ax.scatter([1.3], [0.6 * 1.3 ** 3 - 1.2 * 1.3], s=62, color=ACC,
           edgecolor=INK, linewidth=0.9, zorder=6)
ax.set_title("a function:  one input, one output", fontsize=12, pad=10)
axes_through_origin(ax, (-3.0, 3.0), (-3.0, 3.0))
ax.set_xticks([-2, 2]); ax.set_yticks([-2, 2])

ax = axes[1]
ys = np.linspace(-2.4, 2.4, 300)
ax.plot(0.55 * ys ** 2 - 1.6, ys, color=GREEN, linewidth=2.4, zorder=5)
ax.axvline(1.3, color=ACC, linestyle="--", linewidth=1.6, zorder=4)
for s in (+1, -1):
    yy = s * np.sqrt((1.3 + 1.6) / 0.55)
    ax.scatter([1.3], [yy], s=62, color=ACC, edgecolor=INK, linewidth=0.9, zorder=6)
ax.annotate("two outputs", (1.45, 0.15), color=ACC, fontsize=11.5)
ax.set_title("not a function:  one input, two outputs", fontsize=12, pad=10)
axes_through_origin(ax, (-3.0, 3.0), (-3.0, 3.0))
ax.set_xticks([-2, 2]); ax.set_yticks([-2, 2])

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-2-2-function-test.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)

# ---------- 3. inverse as a reflection in y = x ----------
fig, ax = plt.subplots(figsize=(6.4, 6.0))
xs = np.linspace(-4.6, 4.6, 200)
ax.plot(xs, xs, color="#909aa4", linestyle="--", linewidth=1.6, zorder=3)
ax.plot(xs, 2 * xs + 1, color=LINE, linewidth=2.4, zorder=5)
ax.plot(xs, (xs - 1) / 2, color=GREEN, linewidth=2.4, zorder=5)

ax.scatter([1], [3], s=66, color=LINE, edgecolor=INK, linewidth=0.9, zorder=7)
ax.scatter([3], [1], s=66, color=GREEN, edgecolor=INK, linewidth=0.9, zorder=7)
ax.plot([1, 3], [3, 1], color=ACC, linestyle=":", linewidth=1.5, zorder=6)
ax.annotate("$(1,\\ 3)$", (1, 3), textcoords="offset points", xytext=(-52, 2),
            color=LINE, fontsize=11.5)
ax.annotate("$(3,\\ 1)$", (3, 1), textcoords="offset points", xytext=(8, -6),
            color=GREEN, fontsize=11.5)

ax.annotate("$y = f(x) = 2x + 1$", (-4.4, 3.55), color=LINE, fontsize=12)
ax.annotate("$y = f^{-1}(x) = \\dfrac{x - 1}{2}$", (0.9, -3.5), color=GREEN, fontsize=12)
ax.annotate("$y = x$", (3.5, 4.0), color="#5b656f", fontsize=12)

axes_through_origin(ax, (-4.6, 4.6), (-4.6, 4.6))
ax.set_xticks([-2, 2, 4]); ax.set_yticks([-2, 2, 4])
ax.set_aspect("equal", adjustable="box")
ax.set_title("$f^{-1}$ is the reflection of $f$ in the line $y = x$",
             fontsize=12.5, pad=10)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-2-2-inverse.svg"), format="svg", bbox_inches="tight")
plt.close(fig)

# ---------- 4. does it have an inverse?  (horizontal line test) ----------
fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.2))

ax = axes[0]
xs = np.linspace(-2.4, 2.4, 300)
ax.plot(xs, 0.25 * xs ** 3 + xs, color=LINE, linewidth=2.4, zorder=5)
ax.axhline(2.0, color=ACC, linestyle="--", linewidth=1.6, zorder=4)
# 0.25 x^3 + x = 2  の解
xr = np.roots([0.25, 0, 1, -2])
xr = float([r.real for r in xr if abs(r.imag) < 1e-9][0])
ax.scatter([xr], [2.0], s=62, color=ACC, edgecolor=INK, linewidth=0.9, zorder=6)
ax.annotate("one crossing", (xr + 0.25, 2.35), color=ACC, fontsize=11.5)
ax.set_title("one-to-one:  it HAS an inverse", fontsize=12, pad=10)
axes_through_origin(ax, (-3.0, 3.0), (-5.4, 5.4))
ax.set_xticks([-2, 2]); ax.set_yticks([-4, 4])

ax = axes[1]
xs = np.linspace(-2.5, 2.5, 300)
ax.plot(xs, xs ** 2, color=GREEN, linewidth=2.4, zorder=5)
ax.axhline(4.0, color=ACC, linestyle="--", linewidth=1.6, zorder=4)
for xv in (-2.0, 2.0):
    ax.scatter([xv], [4.0], s=62, color=ACC, edgecolor=INK, linewidth=0.9,
               zorder=6)
ax.annotate("two crossings", (-0.95, 4.45), color=ACC, fontsize=11.5)
ax.annotate("$f(-2) = f(2) = 4$", (1.05, -1.2), color=INK, fontsize=11.5,
            ha="center")
ax.set_title("not one-to-one:  NO inverse", fontsize=12, pad=10)
axes_through_origin(ax, (-3.0, 3.0), (-1.6, 6.6))
ax.set_xticks([-2, 2]); ax.set_yticks([2, 4, 6])

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-2-2-horizontal-test.svg"), format="svg",
            bbox_inches="tight")
plt.close(fig)

print("wrote sl-2-2-domain-range.svg, sl-2-2-function-test.svg,")
print("      sl-2-2-inverse.svg, sl-2-2-horizontal-test.svg")
print("check horizontal test: 0.25x^3+x=2 at x =", round(xr, 4),
      "  x^2=4 at x = -2, 2")
print("check f(-7) =", (2 - (-7)) ** 0.5, " f(2) =", (2 - 2) ** 0.5)
print("check (1,3) on f:", 2 * 1 + 1, "   (3,1) on f^-1:", (3 - 1) / 2)
