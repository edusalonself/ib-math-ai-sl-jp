"""AHL 5.16b（連立系の Euler 法）の図を作る。ラベルはすべて英語。
   ★ 4 枚組は 2 行 2 列（AHL 5.15 / 5.16a と同じ理由）。
   出力先: ai-hl/05-calculus/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_5_16b.py
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


def tidy(ax, xlab, ylab):
    ax.grid(True, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("bottom", "left"):
        ax.spines[sp].set_color(GREY)
    ax.set_xlabel(xlab, fontsize=12)
    ax.set_ylabel(ylab, fontsize=12)


# ── predator–prey（Lotka–Volterra）。x は餌となる動物、y は捕食者 ──
#    dx/dt =  0.4x - 0.002xy
#    dy/dt = -0.3y + 0.001xy
#    平衡点は (300, 200)
def F1(t, x, y):
    return 0.4 * x - 0.002 * x * y


def F2(t, x, y):
    return -0.3 * y + 0.001 * x * y


EQX, EQY = 0.3 / 0.001, 0.4 / 0.002       # = (300, 200)


def ceuler(h, n, x0=400.0, y0=100.0):
    """連立系の Euler 法。★ x と y は【同時に】更新する。"""
    t, x, y = 0.0, x0, y0
    ts, xs, ys = [t], [x], [y]
    for _ in range(n):
        a, b = F1(t, x, y), F2(t, x, y)     # 古い x, y で両方を計算してから
        x, y = x + h * a, y + h * b         # まとめて更新する
        t = t + h
        ts.append(t)
        xs.append(x)
        ys.append(y)
    return np.array(ts), np.array(xs), np.array(ys)


TF, XF, YF = ceuler(0.005, 8000)           # t = 0 .. 40（細かい）
TC, XC, YC = ceuler(1.0, 20)               # t = 0 .. 20（粗い）


# ═════════════ 1. 連立系を Euler で解く（2×2） ═════════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.9))

# (a) 粗い h の折れ線
ax = axs[0]
ax.plot(TC, XC, "-o", color=ACC, lw=2.4, ms=5, label="$x$  (prey)")
ax.plot(TC, YC, "-o", color=LINE, lw=2.4, ms=5, label="$y$  (predator)")
tidy(ax, "$t$", "population")
ax.set_xlim(0, 20)
ax.legend(fontsize=10.5, loc="upper right")
ax.set_title("(a)  $h = 1$  —  a chain of straight pieces",
             fontsize=12.5, color=INK, pad=10)

# (b) 細かい h
ax = axs[1]
m = TF <= 40
ax.plot(TF[m], XF[m], color=ACC, lw=2.6, label="$x$  (prey)")
ax.plot(TF[m], YF[m], color=LINE, lw=2.6, label="$y$  (predator)")
ax.axhline(EQY, color=GREY, lw=1.3, ls="--", zorder=1)
ax.axhline(EQX, color=GREY, lw=1.3, ls="--", zorder=1)
tidy(ax, "$t$", "population")
ax.set_xlim(0, 40)
ax.legend(fontsize=10.5, loc="upper right")
ax.set_title("(b)  $h = 0.005$  —  the cycle appears",
             fontsize=12.5, color=INK, pad=10)

fig.suptitle("$\\dfrac{dx}{dt} = 0.4x - 0.002xy$,   "
             "$\\dfrac{dy}{dt} = -0.3y + 0.001xy$", fontsize=15, y=1.0)
fig.text(0.5, -0.05,
         "Two quantities that feed into each other.   Each Euler step uses the "
         "OLD $x$ and the OLD $y$ to work out both new values, then updates "
         "them together.",
         fontsize=12.5, ha="center", color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.94))
save(fig, "ahl-5-16b-time.svg")


# ═════════════ 1b. 位相図 ═════════════
fig, ax = plt.subplots(figsize=(6.0, 4.9))
ax.plot(XF[m], YF[m], color=GREEN, lw=2.6, zorder=5)
ax.plot([400], [100], "o", color=GOLD, ms=10, zorder=7)
ax.text(408, 92, "start $(400,\\ 100)$", fontsize=11, color=GOLD, zorder=8)
ax.plot([EQX], [EQY], "o", color=ACC, ms=10, zorder=7)
ax.text(EQX + 10, EQY + 14, "equilibrium\n$(300,\\ 200)$", fontsize=11,
        color=ACC, bbox=BOX, zorder=8)
tidy(ax, "$x$  (prey)", "$y$  (predator)")
ax.set_title("the same run, plotted as $(x,\\ y)$", fontsize=12.5,
             color=GREEN, pad=10)

fig.tight_layout()
save(fig, "ahl-5-16b-phase.svg")


# ═════════════ 1c. h が大きいと外へずれる ═════════════
fig, ax = plt.subplots(figsize=(6.0, 4.9))
ax.plot(XF[m], YF[m], color=GREEN, lw=2.6, zorder=5, label="$h = 0.005$")
_, XB, YB = ceuler(0.5, 80)
ax.plot(XB, YB, "-", color=ACC, lw=2.2, zorder=6, label="$h = 0.5$")
ax.plot([EQX], [EQY], "o", color=INK, ms=8, zorder=7)
tidy(ax, "$x$  (prey)", "$y$  (predator)")
ax.legend(fontsize=10.5, loc="upper right")
ax.set_title("a big $h$ spirals OUTWARDS\n(the method adds energy)",
             fontsize=12.5, color=ACC, pad=10)

fig.tight_layout()
save(fig, "ahl-5-16b-spiral.svg")


# ═════════════ 2. どちらが先にピークを迎えるか ═════════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.9))

sel = (TF >= 10) & (TF <= 32)
tt, xx, yy = TF[sel], XF[sel], YF[sel]
ix, iy = int(np.argmax(xx)), int(np.argmax(yy))

ax = axs[0]
ax.plot(tt, xx, color=ACC, lw=2.8, label="$x$  (prey)")
ax.plot(tt, yy, color=LINE, lw=2.8, label="$y$  (predator)")
ax.axvline(tt[ix], color=ACC, lw=1.5, ls="--", zorder=2)
ax.axvline(tt[iy], color=LINE, lw=1.5, ls="--", zorder=2)
ax.plot([tt[ix]], [xx[ix]], "o", color=ACC, ms=9, zorder=6)
ax.plot([tt[iy]], [yy[iy]], "o", color=LINE, ms=9, zorder=6)
ax.annotate("", xy=(tt[iy], 560), xytext=(tt[ix], 560),
            arrowprops=dict(arrowstyle="<->", color=GOLD, lw=1.8))
ax.text((tt[ix] + tt[iy]) / 2, 575, "prey peaks FIRST", ha="center",
        fontsize=11.5, color=GOLD, bbox=BOX, zorder=8)
tidy(ax, "$t$", "population")
ax.set_xlim(10, 32)
ax.set_ylim(0, 680)
ax.legend(fontsize=10.5, loc="upper left")
ax.set_title("the predator peak comes AFTER the prey peak", fontsize=12.5,
             color=INK, pad=10)

ax = axs[1]
ax.plot(XF[m], YF[m], color=GREEN, lw=2.4, zorder=5)
for i in (600, 2200, 3800, 5400):
    ax.annotate("", xy=(XF[i + 90], YF[i + 90]), xytext=(XF[i], YF[i]),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.4),
                zorder=6)
ax.plot([EQX], [EQY], "o", color=ACC, ms=9, zorder=7)
ax.text(EQX + 10, EQY + 14, "$(300,\\ 200)$", fontsize=11, color=ACC,
        bbox=BOX, zorder=8)
tidy(ax, "$x$  (prey)", "$y$  (predator)")
ax.set_title("the path goes ANTICLOCKWISE round the equilibrium",
             fontsize=12.5, color=GREEN, pad=10)

fig.text(0.5, -0.05,
         "More prey means the predators eat well and increase; more predators "
         "then cut the prey down; fewer prey starve the predators; and the "
         "cycle repeats.",
         fontsize=12.5, ha="center", color=INK)
fig.tight_layout()
save(fig, "ahl-5-16b-cycle.svg")

print("figures written to", os.path.normpath(OUT))
