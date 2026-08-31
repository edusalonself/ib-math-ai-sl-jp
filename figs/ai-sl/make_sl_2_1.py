"""SL 2.1 の図を作る。ラベルはすべて英語。
   出力先: ai-sl/02-functions/img/*.svg
   再生成: python3 figs/ai-sl/make_sl_2_1.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-sl", "02-functions", "img")
os.makedirs(OUT, exist_ok=True)

INK, GRID, LINE, ACC, FILL = "#1f2328", "#dfe3e8", "#2874a6", "#c0392b", "#f0b27a"
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


# ---------- 1. gradient = rise / run ----------
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.3))

ax = axes[0]
x = np.linspace(-1, 7.5, 200)
ax.plot(x, 2 * x + 1, color=LINE, linewidth=2.2, zorder=4)
P, Q = (2, 5), (6, 13)
ax.scatter(*zip(P, Q), s=60, color=LINE, edgecolor=INK, linewidth=0.9, zorder=6)
ax.annotate("$A(2,\\ 5)$", P, textcoords="offset points", xytext=(-52, -4), fontsize=11)
ax.annotate("$B(6,\\ 13)$", Q, textcoords="offset points", xytext=(-10, 10), fontsize=11)
# rise / run triangle
ax.plot([2, 6], [5, 5], color=ACC, linewidth=1.8, zorder=5)
ax.plot([6, 6], [5, 13], color=ACC, linewidth=1.8, zorder=5)
ax.annotate("run $= 4$", (4, 5), textcoords="offset points", xytext=(-24, -18),
            color=ACC, fontsize=11.5)
ax.annotate("rise $= 8$", (6, 9), textcoords="offset points", xytext=(8, -6),
            color=ACC, fontsize=11.5)
ax.annotate("$m = \\dfrac{8}{4} = 2$", (0.4, 12.2), color=ACC, fontsize=13)
ax.set_title("gradient $=$ rise $\\div$ run", fontsize=12, pad=10)
axes_through_origin(ax, (-1.4, 8.2), (-1.5, 15.5))
ax.set_xticks([2, 4, 6, 8])
ax.set_yticks([5, 10, 15])

ax = axes[1]
xs = np.linspace(-4.2, 4.2, 100)
for mm, col, lab, ypos in [(1, "#2874a6", "$m > 0$", 4.2),
                           (-1, "#1e8449", "$m < 0$", -4.2),
                           (0, "#8a4b12", "$m = 0$", 0.0)]:
    ax.plot(xs, mm * xs, color=col, linewidth=2.2, zorder=4)
    ax.annotate(lab, (4.35, ypos), color=col, fontsize=12,
                va="center", annotation_clip=False)
ax.plot([2.2, 2.2], [-4.3, 4.3], color=ACC, linewidth=2.2, linestyle="--", zorder=4)
ax.annotate("undefined\n(vertical)", (2.1, -3.3), color=ACC, fontsize=11,
            ha="right")
ax.set_title("the four cases", fontsize=12, pad=10)
axes_through_origin(ax, (-4.6, 7.0), (-4.9, 4.9))
ax.set_xticks([-2, 2, 4])
ax.set_yticks([-2, 2, 4])

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-2-1-gradient.svg"), format="svg", bbox_inches="tight")
plt.close(fig)

# ---------- 2. parallel and perpendicular ----------
fig, axes = plt.subplots(1, 2, figsize=(10.4, 5.2))

ax = axes[0]
xs = np.linspace(-4.6, 4.6, 100)
ax.plot(xs, 2 * xs + 1, color=LINE, linewidth=2.2, zorder=4)
ax.plot(xs, 2 * xs - 3, color="#5dade2", linewidth=2.2, zorder=4)
ax.annotate("$y = 2x + 1$", (-4.45, -2.7), color=LINE, fontsize=11.5)
ax.annotate("$y = 2x - 3$", (0.6, -3.7), color="#2e86c1", fontsize=11.5)
ax.annotate("$m_1 = m_2 = 2$", (-4.45, 3.9), color=ACC, fontsize=13)
ax.set_title("parallel:   $m_1 = m_2$", fontsize=12.5, pad=10)
axes_through_origin(ax, (-4.6, 4.6), (-4.6, 4.6))
ax.set_xticks([-2, 2, 4]); ax.set_yticks([-2, 2, 4])
ax.set_aspect("equal", adjustable="box")

ax = axes[1]
xs = np.linspace(-4.6, 4.6, 100)
ax.plot(xs, 2 * xs, color=LINE, linewidth=2.2, zorder=4)
ax.plot(xs, -0.5 * xs, color="#1e8449", linewidth=2.2, zorder=4)
ax.annotate("$m_1 = 2$", (2.45, 4.05), color=LINE, fontsize=12)
ax.annotate("$m_2 = -\\frac{1}{2}$", (2.85, -3.05), color="#1e8449", fontsize=12)
# rise/run triangle on the blue line (down-left, so the two do not overlap)
ax.plot([0, -1], [0, 0], color=ACC, linewidth=1.8, zorder=5)
ax.plot([-1, -1], [0, -2], color=ACC, linewidth=1.8, zorder=5)
ax.annotate("$1$", (-0.5, 0), textcoords="offset points", xytext=(-4, 7),
            color=ACC, fontsize=11.5)
ax.annotate("$2$", (-1, -1), textcoords="offset points", xytext=(-20, -5),
            color=ACC, fontsize=11.5)
# rise/run triangle on the green line (right)
ax.plot([0, 2], [0, 0], color="#8a4b12", linewidth=1.8, zorder=5)
ax.plot([2, 2], [0, -1], color="#8a4b12", linewidth=1.8, zorder=5)
ax.annotate("$2$", (1, 0), textcoords="offset points", xytext=(-4, 7),
            color="#8a4b12", fontsize=11.5)
ax.annotate("$-1$", (2, -0.5), textcoords="offset points", xytext=(8, -5),
            color="#8a4b12", fontsize=11.5)
ax.annotate("$2 \\times \\left(-\\frac{1}{2}\\right) = -1$", (-4.45, 3.9),
            color=ACC, fontsize=13)
ax.set_title("perpendicular:   $m_1 \\times m_2 = -1$", fontsize=12.5, pad=10)
axes_through_origin(ax, (-4.6, 4.6), (-4.6, 4.6))
ax.set_xticks([-2, 2, 4]); ax.set_yticks([-2, 2, 4])
ax.set_aspect("equal", adjustable="box")

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-2-1-perp.svg"), format="svg", bbox_inches="tight")
plt.close(fig)

# ---------- 3. gradient of a real incline ----------
fig, ax = plt.subplots(figsize=(7.8, 3.6))
ax.fill_between([0, 1500], [0, 120], color=FILL, alpha=0.45, zorder=2)
ax.plot([0, 1500], [0, 120], color=INK, linewidth=2.4, zorder=4)
ax.plot([0, 1500], [0, 0], color=ACC, linewidth=1.8, zorder=4)
ax.plot([1500, 1500], [0, 120], color=ACC, linewidth=1.8, zorder=4)
ax.annotate("horizontal distance $= 1500$ m", (750, 0),
            textcoords="offset points", xytext=(-88, -22), color=ACC, fontsize=11.5)
ax.annotate("rise $= 120$ m", (1500, 60),
            textcoords="offset points", xytext=(-118, 0), color=ACC, fontsize=11.5)
ax.annotate("$m = \\dfrac{120}{1500} = 0.08 = 8\\%$", (60, 92),
            color=INK, fontsize=13)
ax.set_xlim(-90, 1720)
ax.set_ylim(-34, 150)
ax.set_xticks([])
ax.set_yticks([])
for sp in ("top", "right", "left", "bottom"):
    ax.spines[sp].set_visible(False)
ax.set_title("The gradient of a mountain road  (not to scale)", fontsize=12.5, pad=8)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-2-1-incline.svg"), format="svg", bbox_inches="tight")
plt.close(fig)

print("wrote sl-2-1-gradient.svg, sl-2-1-perp.svg, sl-2-1-incline.svg")
print("check m(A,B) =", (13 - 5) / (6 - 2), " perp product =", 2 * (-0.5),
      " road =", 120 / 1500)
