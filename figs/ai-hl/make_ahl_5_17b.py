"""AHL 5.17b（複素・純虚の固有値の phase portrait）の図を作る。ラベルは英語。
   ★ 4 枚組は 2 行 2 列（AHL 5.15 / 5.16 / 5.17a と同じ理由）。
   出力先: ai-hl/05-calculus/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_5_17b.py
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
R = 4.0
TICKS = [-4, -2, 0, 2, 4]


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True)
    plt.close(fig)
    print("wrote", name)


def frame(ax, r=R):
    ax.set_xlim(-r, r)
    ax.set_ylim(-r, r)
    ax.set_aspect("equal")
    ax.grid(True, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.axhline(0, color=GREY, lw=1.0, alpha=0.6, zorder=1)
    ax.axvline(0, color=GREY, lw=1.0, alpha=0.6, zorder=1)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("bottom", "left"):
        ax.spines[sp].set_color(GREY)
    ax.set_xticks(TICKS)
    ax.set_yticks(TICKS)
    ax.set_xlabel("$x$", fontsize=12)
    ax.set_ylabel("$y$", fontsize=12)


def traj(ax, M, p0, col=LINE, lw=2.3, tmax=6.0, n=6000, zorder=5,
         arrows=(0.25, 0.6)):
    """dX/dt = M X を RK4 で前向きにたどる（図を描くためだけのもの）。"""
    M = np.array(M, dtype=float)
    h = tmax / n
    X = np.array(p0, dtype=float)
    pts = [X.copy()]
    for _ in range(n):
        k1 = M @ X
        k2 = M @ (X + h * k1 / 2)
        k3 = M @ (X + h * k2 / 2)
        k4 = M @ (X + h * k3)
        X = X + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        if np.max(np.abs(X)) > 1.4 * R:
            break
        pts.append(X.copy())
    P = np.array(pts)
    ax.plot(P[:, 0], P[:, 1], color=col, lw=lw, zorder=zorder)
    for a in arrows:
        i = int(len(P) * a)
        if 0 < i < len(P) - 4:
            ax.annotate("", xy=P[i + 4], xytext=P[i],
                        arrowprops=dict(arrowstyle="-|>", color=col,
                                        lw=lw + 0.4),
                        zorder=zorder + 1)
    return P


# 4 つの行列
M_IN = [[-1, -2], [2, -1]]      # lambda = -1 +- 2i   内向きの spiral
M_OUT = [[1, -2], [2, 1]]       # lambda =  1 +- 2i   外向きの spiral
M_CIR = [[0, -2], [2, 0]]       # lambda = +- 2i      円
M_ELL = [[0, -1], [4, 0]]       # lambda = +- 2i      楕円
M_CW = [[0, 2], [-2, 0]]        # lambda = +- 2i      円（時計回り）


# ═════════════ 1a. spiral の 2 つ（1×2） ═════════════
fig, axs = plt.subplots(1, 2, figsize=(11.0, 5.4))

ax = axs[0]
frame(ax)
traj(ax, M_IN, (3.8, 0.0), col=LINE, tmax=4.2, arrows=(0.15, 0.45))
traj(ax, M_IN, (-3.8, 0.0), col=GREEN, tmax=4.2, arrows=(0.15, 0.45))
ax.plot([0], [0], "o", color=INK, ms=9, zorder=9)
ax.set_title("(a)  $\\lambda = -1 \\pm 2i$\nreal part NEGATIVE  $\\rightarrow$  spirals IN",
             fontsize=12.5, color=LINE, pad=10)

ax = axs[1]
frame(ax)
traj(ax, M_OUT, (0.08, 0.0), col=ACC, tmax=3.9, arrows=(0.55, 0.85))
traj(ax, M_OUT, (-0.08, 0.0), col=GOLD, tmax=3.9, arrows=(0.55, 0.85))
ax.plot([0], [0], "o", color=INK, ms=9, zorder=9)
ax.set_title("(b)  $\\lambda = 1 \\pm 2i$\nreal part POSITIVE  $\\rightarrow$  spirals OUT",
             fontsize=12.5, color=ACC, pad=10)

fig.text(0.5, -0.05,
         "The IMAGINARY part makes the path go round.   The REAL part decides "
         "whether it also grows (out) or shrinks (in).",
         fontsize=12.5, ha="center", color=INK)
fig.tight_layout()
save(fig, "ahl-5-17b-spiral.svg")


# ═════════════ 1b. 純虚数の 2 つ（1×2） ═════════════
fig, axs = plt.subplots(1, 2, figsize=(11.0, 5.4))

ax = axs[0]
frame(ax)
for r, c in ((1.3, GREEN), (2.4, LINE), (3.4, GOLD)):
    traj(ax, M_CIR, (r, 0.0), col=c, tmax=3.3, arrows=(0.2, 0.7))
ax.plot([0], [0], "o", color=INK, ms=9, zorder=9)
ax.set_title("(a)  $\\lambda = \\pm 2i$  (purely imaginary)\nclosed CIRCLES",
             fontsize=12.5, color=GREEN, pad=10)

ax = axs[1]
frame(ax)
for r, c in ((0.8, GREEN), (1.4, LINE), (1.9, GOLD)):
    traj(ax, M_ELL, (r, 0.0), col=c, tmax=3.3, arrows=(0.2, 0.7))
ax.plot([0], [0], "o", color=INK, ms=9, zorder=9)
ax.set_title("(b)  $\\lambda = \\pm 2i$  as well\nclosed ELLIPSES",
             fontsize=12.5, color=GOLD, pad=10)

fig.text(0.5, -0.05,
         "The real part is ZERO, so the path neither grows nor shrinks.   "
         "Panels (a) and (b) have the SAME eigenvalues.",
         fontsize=12.5, ha="center", color=INK)
fig.tight_layout()
save(fig, "ahl-5-17b-closed.svg")


# ═════════════ 2. 回る向きの決め方（1×2） ═════════════
fig, axs = plt.subplots(1, 2, figsize=(11.0, 5.4))

for ax, (M, lab, col) in zip(
        axs,
        ((M_CIR, "$\\dfrac{dx}{dt} = -2y$,   $\\dfrac{dy}{dt} = 2x$", GREEN),
         (M_CW, "$\\dfrac{dx}{dt} = 2y$,   $\\dfrac{dy}{dt} = -2x$", ACC))):
    frame(ax)
    traj(ax, M, (2.6, 0.0), col=col, tmax=3.3, arrows=(0.15, 0.45, 0.75))
    v = np.array(M, dtype=float) @ np.array([1.0, 0.0])
    v = v / np.linalg.norm(v) * 1.5
    ax.plot([1.0], [0.0], "o", color=INK, ms=10, zorder=9)
    ax.annotate("", xy=(1.0 + v[0], v[1]), xytext=(1.0, 0.0),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=3.0), zorder=9)
    way = "ANTICLOCKWISE" if v[1] > 0 else "CLOCKWISE"
    ax.text(-3.8, 3.6,
            "put $(1,\\ 0)$ into the equations:\n"
            "$\\left(\\dfrac{dx}{dt},\\ \\dfrac{dy}{dt}\\right) = (%d,\\ %d)$\n"
            "the arrow points %s\n$\\Rightarrow$ %s"
            % (M[0][0], M[1][0], "UP" if v[1] > 0 else "DOWN", way),
            fontsize=11, color=INK, bbox=BOX, zorder=10, va="top", ha="left")
    ax.plot([0], [0], "o", color=GREY, ms=7, zorder=8)
    ax.set_title(lab, fontsize=12.5, color=col, pad=10)

fig.suptitle("Which way round? Test the single point $(1,\\ 0)$",
             fontsize=14.5, y=1.02)
fig.text(0.5, -0.06,
         "Both systems have $\\lambda = \\pm 2i$, so both give circles — but "
         "they go opposite ways.   The eigenvalues alone do NOT tell you the "
         "direction; one substituted point does.",
         fontsize=12.5, ha="center", color=INK)
fig.tight_layout()
save(fig, "ahl-5-17b-direction.svg")

print("figures written to", os.path.normpath(OUT))
