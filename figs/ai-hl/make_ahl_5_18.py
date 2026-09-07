"""AHL 5.18（2階微分方程式）の図を作る。ラベルは英語。
   出力先: ai-hl/05-calculus/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_5_18.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from _graph import INK, GRID, LINE, ACC, GREEN, GREY, GOLD, BOX

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "05-calculus", "img")
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
    for sp in ("bottom", "left"):
        ax.spines[sp].set_color(GREY)


def euler(a, b, x0, y0, h, n):
    """x'' + a x' + b x = 0 を y = dx/dt で連立にして Euler 法。"""
    ts, xs, ys = [0.0], [x0], [y0]
    x, y, t = x0, y0, 0.0
    for _ in range(n):
        xn = x + h * y
        yn = y + h * (-b * x - a * y)
        x, y, t = xn, yn, t + h
        ts.append(t)
        xs.append(x)
        ys.append(y)
    return np.array(ts), np.array(xs), np.array(ys)


def exact_over(t):
    """x'' + 3x' + 2x = 0, x(0)=1, x'(0)=0."""
    return 2 * np.exp(-t) - np.exp(-2 * t)


def exact_over_v(t):
    return -2 * np.exp(-t) + 2 * np.exp(-2 * t)


# ══════════════ 1. Euler 法と厳密解のくらべ方 ══════════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.6))

ax = axs[0]
tt = np.linspace(0, 3, 600)
ax.plot(tt, exact_over(tt), color=LINE, lw=2.6,
        label="exact  $x = 2e^{-t} - e^{-2t}$")
for h, col, mk in ((0.4, ACC, "o"), (0.1, GREEN, "s")):
    te, xe, _ = euler(3, 2, 1, 0, h, int(round(3 / h)))
    ax.plot(te, xe, color=col, lw=1.6, ls="--", marker=mk, ms=4.5,
            label="Euler, $h = %g$" % h)
ax.set_xlim(0, 3)
ax.set_ylim(0, 1.08)
ax.set_xlabel("$t$")
ax.set_ylabel("$x$")
ax.legend(fontsize=10.5, frameon=False, loc="upper right")
ax.set_title("a smaller step $h$ follows the exact curve more closely",
             fontsize=12, color=INK, pad=10)
tidy(ax)

ax = axs[1]
ax.plot(exact_over(tt), exact_over_v(tt), color=LINE, lw=2.6, label="exact")
te, xe, ye = euler(3, 2, 1, 0, 0.4, 8)
ax.plot(xe, ye, color=ACC, lw=1.6, ls="--", marker="o", ms=4.5,
        label="Euler, $h = 0.4$")
ax.plot([1], [0], "o", color=GOLD, ms=8, zorder=6)
ax.text(1.0, 0.055, "start $(1,\\ 0)$", fontsize=10.5, color=GOLD,
        ha="center", va="bottom")
ax.plot([0], [0], "o", color=INK, ms=7, zorder=6)
ax.set_xlim(-0.18, 1.25)
ax.set_ylim(-0.92, 0.18)
ax.set_xlabel("$x$")
ax.set_ylabel("$y = \\dfrac{dx}{dt}$")
ax.legend(fontsize=10.5, frameon=False, loc="lower left")
ax.set_title("the same run drawn in the $(x,\\ y)$ plane",
             fontsize=12, color=INK, pad=10)
tidy(ax)

fig.text(0.5, -0.04,
         "Both pictures show $\\frac{d^2x}{dt^2} + 3\\frac{dx}{dt} + 2x = 0$ with "
         "$x = 1$ and $\\dfrac{dx}{dt} = 0$ at $t = 0$, written as $\\dfrac{dx}{dt} = y$, "
         "$\\dfrac{dy}{dt} = -2x - 3y$.",
         fontsize=12, ha="center", color=INK)
fig.tight_layout()
save(fig, "ahl-5-18-euler.svg")


# ══════════════ 2. 固有値の型と動きの対応（3 行 2 列） ══════════════
def rk4(a, b, x0, y0, tmax, n=4000):
    h = tmax / n
    X = np.array([x0, y0], dtype=float)
    M = np.array([[0.0, 1.0], [-b, -a]])
    ts, P = [0.0], [X.copy()]
    for i in range(n):
        k1 = M @ X
        k2 = M @ (X + h * k1 / 2)
        k3 = M @ (X + h * k2 / 2)
        k4 = M @ (X + h * k3)
        X = X + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        ts.append((i + 1) * h)
        P.append(X.copy())
    P = np.array(P)
    return np.array(ts), P[:, 0], P[:, 1]


CASES = [
    (3.0, 2.0, "$\\frac{d^2x}{dt^2} + 3\\frac{dx}{dt} + 2x = 0$",
     "$\\lambda = -1,\\ -2$   (real, both negative)",
     "no oscillation: $x$ returns straight to $0$", ACC, 6.0),
    (2.0, 5.0, "$\\frac{d^2x}{dt^2} + 2\\frac{dx}{dt} + 5x = 0$",
     "$\\lambda = -1 \\pm 2i$   (complex, negative real part)",
     "oscillates, and the swings die away", GREEN, 6.0),
    (0.0, 4.0, "$\\frac{d^2x}{dt^2} + 4x = 0$",
     "$\\lambda = \\pm 2i$   (purely imaginary)",
     "oscillates for ever: the swings keep the same size", GOLD, 6.5),
]

fig, axs = plt.subplots(3, 2, figsize=(11.4, 12.4))
for row, (a, b, eqn, lam, note, col, tmax) in enumerate(CASES):
    ts, xs, ys = rk4(a, b, 1.0, 0.0, tmax)

    ax = axs[row, 0]
    ax.plot(ts, xs, color=col, lw=2.6)
    ax.axhline(0, color=GREY, lw=1.0, alpha=0.7)
    ylo = -1.48 if a == 0 else -1.15
    ax.set_xlim(0, tmax)
    ax.set_ylim(ylo, 1.18)
    ax.set_xlabel("$t$")
    ax.set_ylabel("$x$")
    ax.set_title("%s\n%s" % (eqn, lam), fontsize=12, color=INK, pad=10)
    ax.text(tmax * 0.98, ylo + 0.06, note, fontsize=11, ha="right",
            va="bottom", color=col, bbox=BOX)
    tidy(ax)

    ax = axs[row, 1]
    for x0, y0, c in ((1.0, 0.0, col), (0.0, 1.2, GREY), (-0.8, -0.6, GREY)):
        _, px, py = rk4(a, b, x0, y0, tmax * 1.6)
        ax.plot(px, py, color=c, lw=2.4 if c is col else 1.6,
                alpha=1.0 if c is col else 0.75)
        i = len(px) // 12
        ax.annotate("", xy=(px[i + 6], py[i + 6]), xytext=(px[i], py[i]),
                    arrowprops=dict(arrowstyle="-|>", color=c, lw=1.8))
    ax.plot([1], [0], "o", color=col, ms=7, zorder=6)
    ax.plot([0], [0], "o", color=INK, ms=7, zorder=6)
    ax.axhline(0, color=GREY, lw=1.0, alpha=0.6)
    ax.axvline(0, color=GREY, lw=1.0, alpha=0.6)
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-2.6, 2.6)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y = \\dfrac{dx}{dt}$")
    ax.set_title("phase portrait", fontsize=12, color=INK, pad=10)
    tidy(ax)

fig.suptitle("The eigenvalues decide what the motion looks like",
             fontsize=14.5, y=0.997)
fig.text(0.5, -0.012,
         "Left: the displacement $x$ against time.   "
         "Right: the same motion in the $(x,\\ y)$ plane, where "
         "$y = \\dfrac{dx}{dt}$ is the velocity.",
         fontsize=12, ha="center", color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.985))
save(fig, "ahl-5-18-cases.svg")

print("figures written to", os.path.normpath(OUT))
