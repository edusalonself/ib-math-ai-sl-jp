"""AHL 5.15（slope fields）の図を作る。ラベルはすべて英語。
   ★ 4 枚組は 2 行 2 列にする。横 1 列に 4 枚並べると、本文の幅（約 700px）では
     1 枚が 175px しかなく、線分が潰れて読めない。2×2 なら 1 枚 340px 前後で、
     線分の向きがはっきり見える。
   出力先: ai-hl/05-calculus/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_5_15.py
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


def frame(ax, xr, yr, xlab="$x$", ylab="$y$", xticks=None, yticks=None):
    ax.set_xlim(*xr)
    ax.set_ylim(*yr)
    ax.grid(True, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.axhline(0, color=GREY, lw=0.9, alpha=0.55, zorder=1)
    ax.axvline(0, color=GREY, lw=0.9, alpha=0.55, zorder=1)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("bottom", "left"):
        ax.spines[sp].set_color(GREY)
    ax.set_xlabel(xlab, fontsize=12)
    ax.set_ylabel(ylab, fontsize=12)
    if xticks is not None:
        ax.set_xticks(xticks)
    if yticks is not None:
        ax.set_yticks(yticks)


def slopefield(ax, f, xs, ys, xr, yr, col=GREY, lw=1.9, frac=0.48, alpha=1.0,
               zorder=3):
    """各点で dy/dx = f(x, y) の向きに、長さのそろった短い線分を引く。
       ★ 線分の長さは画面上で一定にする（傾きが大きいと長く見えるのを防ぐ）。"""
    dx_unit = (xr[1] - xr[0]) * frac / max(len(xs) - 1, 1)
    dy_unit = (yr[1] - yr[0]) * frac / max(len(ys) - 1, 1)
    for x in xs:
        for y in ys:
            m = f(x, y)
            # 画面の縦横比に合わせて正規化する
            mm = m * dx_unit / dy_unit
            norm = np.hypot(1.0, mm)
            hx = 0.5 * dx_unit / norm
            hy = 0.5 * dy_unit * mm / norm
            ax.plot([x - hx, x + hx], [y - hy, y + hy],
                    color=col, lw=lw, solid_capstyle="round", alpha=alpha,
                    zorder=zorder)


def curve(ax, f, x0, y0, xr, col=ACC, lw=2.6, n=4000, zorder=6):
    """RK4 で解曲線を前後にたどる（図を描くためだけのもの）。"""
    def march(direction):
        h = direction * (xr[1] - xr[0]) / n
        x, y = x0, y0
        px, py = [x], [y]
        for _ in range(n):
            k1 = f(x, y)
            k2 = f(x + h / 2, y + h * k1 / 2)
            k3 = f(x + h / 2, y + h * k2 / 2)
            k4 = f(x + h, y + h * k3)
            y = y + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
            x = x + h
            if not (xr[0] - 1e-9 <= x <= xr[1] + 1e-9) or abs(y) > 1e4:
                break
            px.append(x)
            py.append(y)
        return px, py
    ax_, ay_ = march(-1)
    bx_, by_ = march(+1)
    ax.plot(ax_[::-1] + bx_[1:], ay_[::-1] + by_[1:], color=col, lw=lw,
            zorder=zorder)


# ═══════════════════ 1. slope field の作り方（2×2） ═══════════════════
def F1(x, y):
    return x - y


XR, YR = (-3.2, 3.2), (-3.2, 3.2)
GX = np.arange(-3, 3.5, 1.0)
GY = np.arange(-3, 3.5, 1.0)
TICKS = [-3, -2, -1, 0, 1, 2, 3]

fig, axs = plt.subplots(2, 2, figsize=(11.4, 10.0))

# (a) 1 点だけ
ax = axs[0, 0]
frame(ax, XR, YR, xticks=TICKS, yticks=TICKS)
slopefield(ax, F1, [1.0], [2.0], XR, YR, col=ACC, lw=3.0)
ax.plot([1], [2], "o", color=ACC, ms=8, zorder=5)
ax.annotate("at $(1,\\ 2)$:\n$\\dfrac{dy}{dx} = 1 - 2 = -1$",
            xy=(1, 2), xytext=(-2.9, 2.5), fontsize=12, color=ACC,
            arrowprops=dict(arrowstyle="->", color=ACC, lw=1.6),
            bbox=BOX, zorder=7, va="top")
ax.set_title("(a)  one point:  compute the slope,\ndraw a SHORT segment",
             fontsize=13, color=ACC, pad=10)

# (b) 数点
ax = axs[0, 1]
frame(ax, XR, YR, xticks=TICKS, yticks=TICKS)
few_x = [-2.0, -1.0, 0.0, 1.0, 2.0]
few_y = [-2.0, 0.0, 2.0]
slopefield(ax, F1, few_x, few_y, XR, YR, col=ACC, lw=2.4)
ax.set_title("(b)  repeat at a few more points", fontsize=13, color=ACC,
             pad=10)

# (c) 全体
ax = axs[1, 0]
frame(ax, XR, YR, xticks=TICKS, yticks=TICKS)
slopefield(ax, F1, GX, GY, XR, YR, col=GREY, lw=1.7)
ax.set_title("(c)  fill the grid — this is the SLOPE FIELD", fontsize=13,
             color=GREY, pad=10)

# (d) 解曲線
ax = axs[1, 1]
frame(ax, XR, YR, xticks=TICKS, yticks=TICKS)
slopefield(ax, F1, GX, GY, XR, YR, col=GREY, lw=1.5, alpha=0.55)
for y0, c in ((1.0, ACC), (-1.0, LINE), (3.0, GREEN)):
    curve(ax, F1, 0.0, y0, XR, col=c)
    ax.plot([0], [y0], "o", color=c, ms=7, zorder=7)
ax.set_title("(d)  follow the segments — a SOLUTION CURVE", fontsize=13,
             color=INK, pad=10)

fig.suptitle("$\\dfrac{dy}{dx} = x - y$", fontsize=16, y=0.995)
fig.text(0.5, -0.015,
         "The differential equation gives a SLOPE at every point.   "
         "Draw a short segment with that slope at each grid point, and a "
         "solution curve is the curve that stays tangent to them.",
         fontsize=12.5, ha="center", color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.975))
save(fig, "ahl-5-15-build.svg")


# ═══════════════════ 2. 同じ場から、いくつもの解曲線 ═══════════════════
fig, axs = plt.subplots(2, 2, figsize=(11.4, 10.0))
STARTS = [((0.0, 1.0), ACC, "$(0,\\ 1)$"),
          ((0.0, -2.0), LINE, "$(0,\\ -2)$"),
          ((-2.0, 2.0), GREEN, "$(-2,\\ 2)$"),
          ((2.0, -3.0), GOLD, "$(2,\\ -3)$")]
for ax, ((x0, y0), col, lab) in zip(axs.ravel(), STARTS):
    frame(ax, XR, YR, xticks=TICKS, yticks=TICKS)
    slopefield(ax, F1, GX, GY, XR, YR, col=GREY, lw=1.5, alpha=0.55)
    curve(ax, F1, x0, y0, XR, col=col)
    ax.plot([x0], [y0], "o", color=col, ms=9, zorder=8)
    ax.set_title("through " + lab, fontsize=13.5, color=col, pad=10)

fig.suptitle("the SAME slope field, four different starting points",
             fontsize=15, y=0.995)
fig.text(0.5, -0.015,
         "One starting point picks out ONE curve.   "
         "All four curves bend towards the same line $y = x - 1$ as $x$ "
         "increases — that line is itself a solution.",
         fontsize=12.5, ha="center", color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.975))
save(fig, "ahl-5-15-follow.svg")


# ═══════════════════ 3. 式と場を対応させる（2×2） ═══════════════════
EQS = [("A", lambda x, y: x, "$\\dfrac{dy}{dx} = x$", LINE),
       ("B", lambda x, y: y, "$\\dfrac{dy}{dx} = y$", GREEN),
       ("C", lambda x, y: x - y, "$\\dfrac{dy}{dx} = x - y$", ACC),
       ("D", lambda x, y: x * y, "$\\dfrac{dy}{dx} = xy$", GOLD)]

fig, axs = plt.subplots(2, 2, figsize=(11.4, 10.0))
for ax, (lab, f, _txt, col) in zip(axs.ravel(), EQS):
    frame(ax, XR, YR, xticks=TICKS, yticks=TICKS)
    slopefield(ax, f, GX, GY, XR, YR, col=col, lw=1.8)
    ax.set_title("field " + lab, fontsize=14, color=col, pad=10)

fig.suptitle("Which slope field goes with which equation?", fontsize=15,
             y=0.995)
fig.text(0.5, -0.015,
         "Look for where the segments are HORIZONTAL, and ask whether the "
         "picture changes as you move ACROSS (so the slope depends on $x$) "
         "or UP (so it depends on $y$).",
         fontsize=12.5, ha="center", color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.975))
save(fig, "ahl-5-15-match.svg")


# ═══════════════════ 4. 場から読み取れること（2×2） ═══════════════════
fig, axs = plt.subplots(2, 2, figsize=(11.4, 10.0))

# (a) depends on x only -> columns identical
ax = axs[0, 0]
frame(ax, XR, YR, xticks=TICKS, yticks=TICKS)
slopefield(ax, lambda x, y: x, GX, GY, XR, YR, col=LINE, lw=1.8)
ax.axvline(0, color=ACC, lw=2.2, ls="--", zorder=4)
ax.text(0.22, -2.55, "horizontal all\nalong $x = 0$", fontsize=11,
        color=ACC, bbox=BOX, zorder=6, va="top")
ax.set_title("(a)  slope depends on $x$ only:\nevery ROW looks the same",
             fontsize=12.5, color=LINE, pad=10)

# (b) depends on y only -> rows identical
ax = axs[0, 1]
frame(ax, XR, YR, xticks=TICKS, yticks=TICKS)
slopefield(ax, lambda x, y: y, GX, GY, XR, YR, col=GREEN, lw=1.8)
ax.axhline(0, color=ACC, lw=2.2, ls="--", zorder=4)
ax.text(-3.0, 0.9, "horizontal all along $y = 0$", fontsize=11, color=ACC,
        bbox=BOX, zorder=6)
ax.set_title("(b)  slope depends on $y$ only:\nevery COLUMN looks the same",
             fontsize=12.5, color=GREEN, pad=10)

# (c) equilibrium / asymptote  dP/dt = 0.4P(1 - P/50)
ax = axs[1, 0]
PR, TR = (0.0, 62.0), (0.0, 12.0)
TX = np.arange(0, 12.5, 1.5)
PY = np.arange(0, 62.5, 5.0)


def FLOG(t, P):
    return 0.4 * P * (1 - P / 50)


ax.set_xlim(*TR)
ax.set_ylim(*PR)
ax.grid(True, color=GRID, lw=0.8)
ax.set_axisbelow(True)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
for sp in ("bottom", "left"):
    ax.spines[sp].set_color(GREY)
ax.set_xlabel("$t$", fontsize=12)
ax.set_ylabel("$P$", fontsize=12)
slopefield(ax, FLOG, TX, PY, TR, PR, col=GREY, lw=1.5, alpha=0.55)
ax.axhline(50, color=ACC, lw=1.4, ls="--", alpha=0.55, zorder=2)
ax.axhline(0, color=ACC, lw=1.4, ls="--", alpha=0.55, zorder=2)
# 平衡解の高さ（P = 0 と P = 50）の線分だけ、赤で上から描き直す
slopefield(ax, FLOG, TX, [0.0, 50.0], TR, PR, col=ACC, lw=2.6, zorder=9)
ax.text(12.25, 50.0, "$P = 50$\nhorizontal", fontsize=10.5, color=ACC,
        ha="left", va="center")
ax.text(12.25, 0.0, "$P = 0$\nhorizontal", fontsize=10.5, color=ACC,
        ha="left", va="center")
for P0, c in ((5.0, GOLD), (30.0, LINE), (60.0, GREEN)):
    curve(ax, FLOG, 0.0, P0, TR, col=c, lw=2.4)
    ax.plot([0], [P0], "o", color=c, ms=7, zorder=8)
ax.set_title("(c)  $\\dfrac{dP}{dt} = 0.4P\\left(1 - \\dfrac{P}{50}\\right)$:\n"
             "curves level off at $P = 50$", fontsize=12.5, color=INK, pad=10)

# (d) curves never cross
ax = axs[1, 1]
frame(ax, XR, YR, xticks=TICKS, yticks=TICKS)


def FY(x, y):
    return y


slopefield(ax, FY, GX, GY, XR, YR, col=GREY, lw=1.5, alpha=0.55)
for y0, c in ((-1.2, LINE), (0.0, GREY), (0.5, GREEN), (1.5, GOLD)):
    curve(ax, FY, 0.0, y0, XR, col=c, lw=2.4)
ax.text(-3.0, 0.35, "$y = 0$ is a solution too", fontsize=10.5, color=GREY,
        bbox=BOX, zorder=8)
ax.set_title("(d)  $\\dfrac{dy}{dx} = y$:  solution curves never CROSS\n"
             "(there is only ONE slope at each point)", fontsize=12.5,
             color=INK, pad=10)

fig.suptitle("What a slope field tells you at a glance", fontsize=15, y=0.995)
fig.text(0.5, -0.015,
         "Horizontal segments mark where $\\dfrac{dy}{dx} = 0$.   "
         "A whole horizontal LINE of them is an equilibrium solution, and "
         "nearby curves level off towards it.",
         fontsize=12.5, ha="center", color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.975))
save(fig, "ahl-5-15-features.svg")

# ═══════════════════ 5. 演習で使う 4 つの場（2×2） ═══════════════════
fig, axs = plt.subplots(2, 2, figsize=(11.4, 10.0))

# (P) dy/dx = 2 - y : equilibrium at y = 2
ax = axs[0, 0]
frame(ax, XR, YR, xticks=TICKS, yticks=TICKS)
slopefield(ax, lambda x, y: 2 - y, GX, GY, XR, YR, col=LINE, lw=1.8)
ax.set_title("field P", fontsize=14, color=LINE, pad=10)

# (Q) dy/dx = x + y : horizontal along y = -x
ax = axs[0, 1]
frame(ax, XR, YR, xticks=TICKS, yticks=TICKS)
slopefield(ax, lambda x, y: x + y, GX, GY, XR, YR, col=GREEN, lw=1.8)
ax.set_title("field Q", fontsize=14, color=GREEN, pad=10)

# (R) dy/dx = y(4 - y) : equilibria at y = 0 and y = 4
ax = axs[1, 0]
RXR, RYR = (-3.2, 3.2), (-1.2, 5.2)
RGY = np.arange(-1, 5.5, 1.0)
ax.set_xlim(*RXR)
ax.set_ylim(*RYR)
ax.grid(True, color=GRID, lw=0.8)
ax.set_axisbelow(True)
ax.axhline(0, color=GREY, lw=0.9, alpha=0.55, zorder=1)
ax.axvline(0, color=GREY, lw=0.9, alpha=0.55, zorder=1)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
for sp in ("bottom", "left"):
    ax.spines[sp].set_color(GREY)
ax.set_xlabel("$x$", fontsize=12)
ax.set_ylabel("$y$", fontsize=12)
ax.set_xticks(TICKS)
ax.set_yticks([-1, 0, 1, 2, 3, 4, 5])
slopefield(ax, lambda x, y: y * (4 - y), GX, RGY, RXR, RYR, col=ACC, lw=1.8)
ax.set_title("field R", fontsize=14, color=ACC, pad=10)

# (S) dy/dx = x^2 : depends on x only, never negative
ax = axs[1, 1]
frame(ax, XR, YR, xticks=TICKS, yticks=TICKS)
slopefield(ax, lambda x, y: x ** 2, GX, GY, XR, YR, col=GOLD, lw=1.8)
ax.set_title("field S", fontsize=14, color=GOLD, pad=10)

fig.suptitle("Slope fields for the exercises", fontsize=15, y=0.995)
fig.text(0.5, -0.015,
         "Note that field R uses a different $y$-scale from the others.",
         fontsize=12.5, ha="center", color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.975))
save(fig, "ahl-5-15-exercises.svg")


print("figures written to", os.path.normpath(OUT))
