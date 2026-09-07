"""AHL 5.16a（Euler's method）の図を作る。ラベルはすべて英語。
   ★ 4 枚組は 2 行 2 列にする（AHL 5.15 と同じ理由）。横 1 列に 4 枚並べると
     本文の幅（約 700px）では 1 枚 175px しかなく、折れ線と曲線の差が見えない。
   出力先: ai-hl/05-calculus/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_5_16a.py
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


def euler(f, x0, y0, h, n):
    """Euler 法。(x のリスト, y のリスト) を返す。"""
    xs, ys = [x0], [y0]
    x, y = x0, y0
    for _ in range(n):
        y = y + h * f(x, y)
        x = x + h
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)


def slopefield(ax, f, xs, ys, xr, yr, col=GREY, lw=1.5, frac=0.48, alpha=1.0,
               zorder=2):
    """AHL 5.15 と同じ描き方（線分の長さを画面上でそろえる）。"""
    dx_unit = (xr[1] - xr[0]) * frac / max(len(xs) - 1, 1)
    dy_unit = (yr[1] - yr[0]) * frac / max(len(ys) - 1, 1)
    for x in xs:
        for y in ys:
            m = f(x, y)
            mm = m * dx_unit / dy_unit
            norm = np.hypot(1.0, mm)
            hx = 0.5 * dx_unit / norm
            hy = 0.5 * dy_unit * mm / norm
            ax.plot([x - hx, x + hx], [y - hy, y + hy], color=col, lw=lw,
                    solid_capstyle="round", alpha=alpha, zorder=zorder)


# 主役の微分方程式  dy/dx = x + y,  y(0) = 1,  厳密解 y = 2e^x - x - 1
def F(x, y):
    return x + y


def EXACT(x):
    return 2 * np.exp(x) - x - 1


# ★ 表示範囲。x を 0.9 までにしてある。1.2 まで伸ばすと exact が 4.44 まで
#   上がり、最初の 1 歩がつぶれて見えなくなる。
XEND = 0.9
XR, YR = (-0.06, 0.98), (0.85, 3.25)
XT = [0, 0.3, 0.6, 0.9]
FINE = np.linspace(0, XEND, 400)


# ═════════════ 1. Euler の 1 歩 → 折れ線（2×2） ═════════════
fig, axs = plt.subplots(2, 2, figsize=(11.4, 9.2))
H = 0.3

# (a) 出発点と、そこでの傾き
ax = axs[0, 0]
frame(ax, XR, YR, xticks=XT)
ax.plot(FINE, EXACT(FINE), color=GREY, lw=2.0, alpha=0.45, zorder=3)
ax.plot([0], [1], "o", color=ACC, ms=9, zorder=6)
ax.plot([0, 0.42], [1, 1 + 0.42 * F(0, 1)], color=ACC, lw=2.6, zorder=5)
ax.text(0.05, 3.10, "at $(0,\\ 1)$ the equation gives\n"
                    "$\\dfrac{dy}{dx} = 0 + 1 = 1$",
        fontsize=12, color=ACC, bbox=BOX, zorder=7, va="top")
ax.set_title("(a)  start at the given point,\nread the slope off the equation",
             fontsize=12.5, color=ACC, pad=10)

# (b) 1 歩進む
ax = axs[0, 1]
frame(ax, XR, YR, xticks=XT)
ax.plot(FINE, EXACT(FINE), color=GREY, lw=2.0, alpha=0.45, zorder=3)
xe, ye = euler(F, 0.0, 1.0, H, 1)
ax.plot(xe, ye, "-o", color=ACC, lw=2.8, ms=8, zorder=6)
ax.plot([0, H], [1, 1], color=GOLD, lw=1.6, ls="--", zorder=4)
ax.plot([H, H], [1, ye[1]], color=GOLD, lw=1.6, ls="--", zorder=4)
ax.text(H / 2, 0.95, "$h = 0.3$", ha="center", va="top", fontsize=11.5,
        color=GOLD)
ax.text(H + 0.03, (1 + ye[1]) / 2, "$h \\times 1 = 0.3$", ha="left",
        va="center", fontsize=11.5, color=GOLD, bbox=BOX, zorder=7)
ax.text(0.40, 2.95, "new point $(0.3,\\ 1.3)$", fontsize=12, color=ACC,
        bbox=BOX, zorder=7)
ax.set_title("(b)  step along that slope by $h$", fontsize=12.5, color=ACC,
             pad=10)

# (c) 4 歩
ax = axs[1, 0]
frame(ax, XR, YR, xticks=XT)
ax.plot(FINE, EXACT(FINE), color=GREY, lw=2.0, alpha=0.45, zorder=3)
xe, ye = euler(F, 0.0, 1.0, H, 3)
ax.plot(xe, ye, "-o", color=ACC, lw=2.8, ms=8, zorder=6)
for xx, yy in zip(xe, ye):
    ax.plot([xx], [yy], "o", color=ACC, ms=8, zorder=7)
ax.set_title("(c)  repeat — the answer is a POLYGON,\nnot a curve",
             fontsize=12.5, color=ACC, pad=10)

# (d) 厳密解と重ねる
ax = axs[1, 1]
frame(ax, XR, YR, xticks=XT)
ax.plot(FINE, EXACT(FINE), color=LINE, lw=2.8, zorder=5,
        label="exact  $y = 2e^{x} - x - 1$")
ax.plot(xe, ye, "-o", color=ACC, lw=2.6, ms=7, zorder=6,
        label="Euler,  $h = 0.3$")
ax.plot([XEND, XEND], [ye[-1], EXACT(XEND)], color=GOLD, lw=2.6, zorder=7)
ax.annotate("the gap is the ERROR", xy=(XEND, (ye[-1] + EXACT(XEND)) / 2),
            xytext=(0.05, 3.05), fontsize=11.5, color=GOLD,
            arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.6), bbox=BOX,
            zorder=8, va="top")
# ★ 凡例は右下へ。左上は注記の場所なので、重ねると凡例の1行目が
#    注記に置きかわったように見える。
ax.legend(loc="lower right", fontsize=10.5, framealpha=0.92)
ax.set_title("(d)  the polygon always cuts the CORNERS",
             fontsize=12.5, color=INK, pad=10)

fig.suptitle("$\\dfrac{dy}{dx} = x + y$,   $y(0) = 1$", fontsize=16, y=0.995)
fig.text(0.5, -0.02,
         "Euler's method walks along the TANGENT for a short distance $h$, "
         "then reads a new slope and turns.   The result is a chain of "
         "straight pieces, so it is an APPROXIMATION.",
         fontsize=12.5, ha="center", color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.972))
save(fig, "ahl-5-16a-step.svg")


# ═════════════ 2. 歩幅 h を小さくすると（2×2） ═════════════
fig, axs = plt.subplots(2, 2, figsize=(11.4, 9.2))
for ax, (hh, nn, col) in zip(axs.ravel(),
                             ((0.45, 2, ACC), (0.3, 3, GOLD),
                              (0.15, 6, GREEN), (0.075, 12, LINE))):
    frame(ax, XR, YR, xticks=XT)
    ax.plot(FINE, EXACT(FINE), color=GREY, lw=2.6, alpha=0.75, zorder=4)
    xe, ye = euler(F, 0.0, 1.0, hh, nn)
    ax.plot(xe, ye, "-o", color=col, lw=2.6, ms=6, zorder=6)
    gap = EXACT(XEND) - ye[-1]
    ax.plot([XEND, XEND], [ye[-1], EXACT(XEND)], color=INK, lw=2.2, zorder=7)
    ax.set_title("$h = %g$   (%d steps)\nerror at $x = 0.9$:  $%.3f$"
                 % (hh, nn, gap), fontsize=12.5, color=col, pad=10)

fig.suptitle("Halving $h$ roughly halves the error", fontsize=15, y=0.995)
fig.text(0.5, -0.02,
         "The grey curve is the exact solution.   Smaller steps follow it more "
         "closely, but need more rows of working — that is why a spreadsheet "
         "or a calculator is used.",
         fontsize=12.5, ha="center", color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.972))
save(fig, "ahl-5-16a-h.svg")


# ═════════════ 3. 誤差の向きと大きさ（2×2） ═════════════
fig, axs = plt.subplots(2, 2, figsize=(11.4, 9.2))

# (a) convex → Euler は小さめ
ax = axs[0, 0]
frame(ax, XR, YR, xticks=XT)
ax.plot(FINE, EXACT(FINE), color=LINE, lw=2.8, zorder=5)
xe, ye = euler(F, 0.0, 1.0, 0.3, 3)
ax.plot(xe, ye, "-o", color=ACC, lw=2.6, ms=7, zorder=6)
ax.text(0.05, 3.10, "exact curve bends UPWARDS\n(convex)\n"
                    "→ tangents pass BELOW\n→ Euler UNDERestimates",
        fontsize=11.5, color=ACC, bbox=BOX, zorder=8, va="top")
ax.set_title("(a)  $\\dfrac{dy}{dx} = x + y$", fontsize=13, color=ACC, pad=10)

# (b) concave → Euler は大きめ
ax = axs[0, 1]
XR2, YR2 = (-0.12, 2.12), (-0.1, 2.35)


def F2(x, y):
    return 2 - y


fine2 = np.linspace(0, 2, 400)
frame(ax, XR2, YR2, xticks=[0, 0.5, 1.0, 1.5, 2.0])
ax.plot(fine2, 2 - 2 * np.exp(-fine2), color=LINE, lw=2.8, zorder=5)
xe2, ye2 = euler(F2, 0.0, 0.0, 0.5, 4)
ax.plot(xe2, ye2, "-o", color=GREEN, lw=2.6, ms=7, zorder=6)
ax.text(0.60, 0.78, "exact curve bends DOWNWARDS\n(concave)\n"
                    "→ tangents pass ABOVE\n→ Euler OVERestimates",
        fontsize=11.5, color=GREEN, bbox=BOX, zorder=8, va="top")
ax.set_title("(b)  $\\dfrac{dy}{dx} = 2 - y$", fontsize=13, color=GREEN,
             pad=10)

# (c) 誤差 vs h
ax = axs[1, 0]
hs = np.array([0.45, 0.3, 0.15, 0.075, 0.0375])
errs = []
for hh in hs:
    n = int(round(XEND / hh))
    _, yy = euler(F, 0.0, 1.0, hh, n)
    errs.append(EXACT(XEND) - yy[-1])
errs = np.array(errs)
ax.plot(hs, errs, "-o", color=GOLD, lw=2.6, ms=8, zorder=6)
ax.set_xlim(0, 0.50)
ax.set_ylim(0, max(errs) * 1.15)
ax.grid(True, color=GRID, lw=0.8)
ax.set_axisbelow(True)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
for sp in ("bottom", "left"):
    ax.spines[sp].set_color(GREY)
ax.set_xlabel("step length $h$", fontsize=12)
ax.set_ylabel("error at $x = 0.9$", fontsize=12)
ax.set_title("(c)  the error is roughly PROPORTIONAL to $h$",
             fontsize=12.5, color=GOLD, pad=10)

# (d) h を半分にすると誤差も半分（棒）
ax = axs[1, 1]
lbl = ["$h=0.45$", "$h=0.3$", "$h=0.15$", "$h=0.075$"]
ax.bar(range(4), errs[:4], width=0.6, color=[ACC, GOLD, GREEN, LINE],
       alpha=0.9, zorder=3)
for i, e in enumerate(errs[:4]):
    ax.text(i, e + max(errs) * 0.03, "%.3f" % e, ha="center", fontsize=11.5,
            color=INK)
ax.set_xticks(range(4))
ax.set_xticklabels(lbl, fontsize=11.5)
ax.set_ylim(0, max(errs) * 1.22)
ax.set_yticks([])
ax.grid(True, axis="y", color=GRID, lw=0.8)
ax.set_axisbelow(True)
for sp in ("top", "right", "left"):
    ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_color(GREY)
ax.set_title("(d)  halving $h$ cuts the error by about half\n($0.3 \\to 0.15 \\to 0.075$)",
             fontsize=12.5, color=INK, pad=10)

fig.suptitle("Which way is Euler's answer wrong, and by how much?",
             fontsize=15, y=0.995)
fig.text(0.5, -0.02,
         "The DIRECTION comes from the way the exact curve bends.   The SIZE "
         "comes from $h$.   Both panels (a) and (b) use the same method — only "
         "the curvature is different.",
         fontsize=12.5, ha="center", color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.972))
save(fig, "ahl-5-16a-error.svg")


# ═════════════ 4. slope field の上を歩く（AHL 5.15 とのつながり） ═════════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.9))
GXf = np.arange(0, 0.99, 0.15)
GYf = np.arange(0.9, 3.3, 0.25)
for ax, (hh, nn, col) in zip(axs, ((0.45, 2, ACC), (0.15, 6, GREEN))):
    frame(ax, XR, YR, xticks=XT)
    slopefield(ax, F, GXf, GYf, XR, YR, col=GREY, lw=1.4, alpha=0.5)
    ax.plot(FINE, EXACT(FINE), color=LINE, lw=2.4, alpha=0.85, zorder=5)
    xe, ye = euler(F, 0.0, 1.0, hh, nn)
    ax.plot(xe, ye, "-o", color=col, lw=2.6, ms=6, zorder=6)
    ax.set_title("Euler with $h = %g$" % hh, fontsize=13, color=col, pad=10)

fig.suptitle("Euler's method is a slope field, walked one step at a time",
             fontsize=14.5, y=1.02)
fig.text(0.5, -0.05,
         "AHL 5.15 draws the segments; AHL 5.16 follows them with numbers.   "
         "With a big $h$ the walk drifts off the segments it meets; with a "
         "small $h$ it stays on them.",
         fontsize=12.5, ha="center", color=INK)
fig.tight_layout()
save(fig, "ahl-5-16a-field.svg")

print("figures written to", os.path.normpath(OUT))
