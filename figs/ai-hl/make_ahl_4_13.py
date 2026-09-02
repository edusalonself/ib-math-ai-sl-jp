"""AHL 4.13 の図を作る。ラベルはすべて英語（日本語グリフは matplotlib に無い）。
   出力先: ai-hl/04-statistics-and-probability/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_4_13.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from _graph import INK, GRID, LINE, ACC, GREEN, GREY, GOLD, BOX

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "04-statistics-and-probability", "img")
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True)
    plt.close(fig)
    print("wrote", name)


def tidy(ax):
    ax.grid(True, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)


# ══════════════ 1. 試験に出る 6 つの形 ══════════════
xs = np.linspace(0.35, 4.0, 300)
MODELS = [
    ("linear", "$y = ax + b$", 1.1 * xs + 0.6),
    ("quadratic", "$y = ax^{2} + bx + c$", -0.75 * (xs - 2.2) ** 2 + 4.2),
    ("cubic", "$y = ax^{3} + bx^{2} + cx + d$",
     0.55 * (xs - 2.2) ** 3 - 0.9 * (xs - 2.2) + 2.6),
    ("exponential", "$y = k a^{x}$", 0.55 * 1.75 ** xs),
    ("power", "$y = a x^{n}$", 1.5 * xs ** 0.6),
    ("sine", "$y = a\\sin(bx + c) + d$", 1.4 * np.sin(1.9 * xs - 0.6) + 2.6),
]
fig, axs = plt.subplots(2, 3, figsize=(12.6, 6.0))
for ax, (name, eqn, ys) in zip(axs.ravel(), MODELS):
    ax.plot(xs, ys, color=LINE, lw=2.4)
    ax.set_xlim(0, 4.3)
    ax.set_ylim(0, 5.6)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(name, fontsize=13, color=ACC, pad=6)
    ax.text(2.15, 0.42, eqn, fontsize=12.5, ha="center", va="bottom",
            color=INK)
    tidy(ax)
fig.tight_layout()
save(fig, "ahl-4-13-shapes.svg")

# ══════════════ 2. residual と SS_res ══════════════
X = np.array([1, 2, 3, 4, 5], float)
Y = np.array([4, 4, 8, 9, 10], float)
M = 2 * X + 1

fig, axs = plt.subplots(1, 2, figsize=(12.4, 4.4))

ax = axs[0]
gx = np.linspace(0.6, 5.4, 100)
ax.plot(gx, 2 * gx + 1, color=LINE, lw=2.2, zorder=3)
for x, y, m in zip(X, Y, M):
    ax.plot([x, x], [m, y], color=ACC, lw=2.4, zorder=4)
    ax.text(x + 0.13, (y + m) / 2, f"${y - m:+.0f}$", fontsize=11,
            ha="left", va="center", color=ACC, zorder=6)
ax.plot(X, Y, "o", mfc="white", mec=INK, mew=1.8, ms=9, zorder=5)
ax.text(4.6, 3.2, "$\\hat{y} = 2x + 1$", fontsize=12.5, color=LINE,
        ha="right", va="center")
ax.set_xlim(0.4, 5.8)
ax.set_ylim(1.5, 12)
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
ax.set_title("residual $= y - \\hat{y}$", fontsize=12.5, color=ACC, pad=8)
tidy(ax)

ax = axs[1]
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")
ax.text(5.0, 8.7, "square each residual, then add", fontsize=12.5,
        ha="center", color=INK)
ax.text(5.0, 6.9, "$SS_{\\mathrm{res}} = \\sum (y - \\hat{y})^{2}$",
        fontsize=15, ha="center", color=ACC)
ax.text(5.0, 4.9, "$= 1^{2} + (-1)^{2} + 1^{2} + 0^{2} + (-1)^{2}$",
        fontsize=13, ha="center", color=INK)
ax.text(5.0, 3.3, "$= 4$", fontsize=16, ha="center", color=GREEN,
        weight="bold")
ax.text(5.0, 1.4, "squaring removes the signs, so the pluses\n"
                  "and minuses cannot cancel out",
        fontsize=11.5, ha="center", va="center", color=GREY)
fig.tight_layout()
save(fig, "ahl-4-13-residuals.svg")

# ══════════════ 3. R^2 は SS_tot のうち説明できた割合 ══════════════
fig, axs = plt.subplots(1, 2, figsize=(12.4, 4.4))
ybar = Y.mean()

ax = axs[0]
ax.axhline(ybar, color=GOLD, lw=2.2, ls="--", zorder=3)
for x, y in zip(X, Y):
    ax.plot([x, x], [ybar, y], color=GOLD, lw=2.4, zorder=4)
ax.plot(X, Y, "o", mfc="white", mec=INK, mew=1.8, ms=9, zorder=5)
ax.text(5.6, ybar + 0.35, "$\\bar{y} = 7$", fontsize=12, color=GOLD,
        ha="right")
ax.set_xlim(0.4, 5.8)
ax.set_ylim(1.5, 12)
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
ax.set_title("$SS_{\\mathrm{tot}} = \\sum (y - \\bar{y})^{2} = 32$",
             fontsize=12.5, color=GOLD, pad=8)
tidy(ax)

ax = axs[1]
ax.plot(gx, 2 * gx + 1, color=LINE, lw=2.2, zorder=3)
for x, y, m in zip(X, Y, M):
    ax.plot([x, x], [m, y], color=ACC, lw=2.4, zorder=4)
ax.plot(X, Y, "o", mfc="white", mec=INK, mew=1.8, ms=9, zorder=5)
ax.set_xlim(0.4, 5.8)
ax.set_ylim(1.5, 12)
ax.set_xlabel("$x$")
ax.set_title("$SS_{\\mathrm{res}} = \\sum (y - \\hat{y})^{2} = 4$",
             fontsize=12.5, color=ACC, pad=8)
tidy(ax)
fig.text(0.5, -0.02, "$R^{2} = 1 - \\dfrac{SS_{\\mathrm{res}}}"
                     "{SS_{\\mathrm{tot}}} = 1 - \\dfrac{4}{32} = 0.875$"
                     "     — the model accounts for $87.5\\%$ of the spread",
         fontsize=13, ha="center", color=GREEN)
fig.tight_layout()
save(fig, "ahl-4-13-r2.svg")

# ══════════════ 4. R^2 が大きいほうがよいとはかぎらない ══════════════
T = np.array([0, 1, 2, 3, 4, 5], float)
V = np.array([24400, 20000, 15700, 12700, 10800, 8200], float)
cL = np.polyfit(T, V, 1)
be, ae = np.polyfit(T, np.log(V), 1)
A, B = np.exp(ae), np.exp(be)
cC = np.polyfit(T, V, 3)
gt = np.linspace(0, 10, 300)

fig, axs = plt.subplots(1, 2, figsize=(12.8, 4.6))

ax = axs[0]
ax.plot(gt, np.polyval(cL, gt), color=ACC, lw=2.2,
        label="linear   $R^{2} = 0.975$")
ax.plot(gt, A * B ** gt, color=GREEN, lw=2.2,
        label="exponential   $R^{2} = 0.998$")
ax.plot(T, V, "o", mfc="white", mec=INK, mew=1.8, ms=9, zorder=5)
ax.axhline(0, color=GREY, lw=1.2)
ax.axvspan(5, 10, color="#f4f6f8", zorder=0)
ax.text(7.5, 22000, "outside the data", fontsize=11, ha="center",
        color=GREY)
ax.set_xlim(0, 10)
ax.set_ylim(-11000, 27000)
ax.set_xlabel("$t$ (years)")
ax.set_ylabel("value ($)")
ax.legend(fontsize=10.5, loc="lower left", frameon=False)
ax.set_title("the straight line gives a negative value",
             fontsize=12.5, color=ACC, pad=8)
tidy(ax)

ax = axs[1]
cQ = np.polyfit(T, V, 2)
ax.plot(gt, np.polyval(cC, gt), color=ACC, lw=2.2,
        label="cubic   $R^{2} = 0.99824$")
ax.plot(gt, np.polyval(cQ, gt), color=GREEN, lw=2.2,
        label="quadratic   $R^{2} = 0.99759$")
ax.plot(T, V, "o", mfc="white", mec=INK, mew=1.8, ms=9, zorder=5)
ax.axhline(0, color=GREY, lw=1.2)
ax.axvspan(5, 10, color="#f4f6f8", zorder=0)
ax.text(7.5, 22000, "outside the data", fontsize=11, ha="center",
        color=GREY)
ax.set_xlim(0, 10)
ax.set_ylim(-11000, 27000)
ax.set_xlabel("$t$ (years)")
ax.legend(fontsize=10.5, loc="lower left", frameon=False)
ax.set_title("the HIGHER $R^{2}$ is the worse model here",
             fontsize=12.5, color=ACC, pad=8)
tidy(ax)
fig.tight_layout()
save(fig, "ahl-4-13-compare.svg")
