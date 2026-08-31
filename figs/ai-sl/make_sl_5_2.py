"""SL 5.2 の図を作る。ラベルはすべて英語。
   出力先: ai-sl/05-calculus/img/*.svg
   再生成: python3 figs/ai-sl/make_sl_5_2.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from math import pi

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-sl", "05-calculus", "img")
os.makedirs(OUT, exist_ok=True)

INK, GRID, LINE, ACC, GREEN = "#1f2328", "#dfe3e8", "#2874a6", "#c0392b", "#1e8449"
GREY = "#7a8592"
GOLD = "#b9770e"
plt.rcParams.update({
    "font.size": 11, "text.color": INK, "svg.fonttype": "path",
})
BOX = dict(facecolor="white", edgecolor="none", pad=1.6, alpha=0.92)


def axes(ax, xlim, ylim, xt=1, yt=1, xlab="$x$", ylab="$y$", ypad=12):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    for x in np.arange(np.ceil(xlim[0] / xt) * xt, xlim[1] + 1e-9, xt):
        ax.axvline(x, color=GRID, lw=0.7, zorder=0)
    for y in np.arange(np.ceil(ylim[0] / yt) * yt, ylim[1] + 1e-9, yt):
        ax.axhline(y, color=GRID, lw=0.7, zorder=0)
    ax.axhline(0, color=GREY, lw=1.2, zorder=1)
    ax.axvline(0, color=GREY, lw=1.2, zorder=1)
    ax.tick_params(labelsize=8.5, colors=GREY, length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xlabel(xlab, fontsize=11, color=INK, labelpad=1)
    ax.set_ylabel(ylab, fontsize=11, color=INK, labelpad=ypad, rotation=0)


# ── 主役の曲線：f(x) = x^3/4 - 3x   停留点 (-2,4) と (2,-4) ──
f = lambda x: x ** 3 / 4 - 3 * x
fp = lambda x: 0.75 * x ** 2 - 3
XL, YL = (-4.4, 4.4), (-6.4, 6.4)


def curve(ax, lw=2.6):
    xs = np.linspace(XL[0] + 0.2, XL[1] - 0.2, 500)
    ax.plot(xs, f(xs), color=LINE, lw=lw, zorder=5)


# ══════════════ 1. 増加と減少 ══════════════
fig, ax = plt.subplots(figsize=(8.4, 5.8))
axes(ax, XL, YL, 1, 2)
seg = [((-4.2, -2.0), GREEN), ((-2.0, 2.0), GOLD), ((2.0, 4.2), GREEN)]
for (a, b), c in seg:
    xs = np.linspace(a, b, 300)
    ax.plot(xs, f(xs), color=c, lw=3.4, zorder=5)
for x0 in (-2.0, 2.0):
    ax.plot([x0], [f(x0)], "o", color=ACC, ms=8, zorder=9)
    ax.plot([x0 - 0.8, x0 + 0.8], [f(x0), f(x0)], color=ACC, lw=2.0, zorder=6)

ax.annotate("", xy=(-2.5, f(-2.5) + 0.9), xytext=(-3.5, f(-3.5) + 0.9),
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=2.0))
ax.annotate("", xy=(1.2, f(1.2) - 0.9), xytext=(-1.2, f(-1.2) - 0.9),
            arrowprops=dict(arrowstyle="->", color=GOLD, lw=2.0))
ax.annotate("", xy=(3.6, f(3.6) - 0.9), xytext=(2.6, f(2.6) - 0.9),
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=2.0))

ax.text(-3.6, 5.4, "increasing", color=GREEN, fontsize=12, ha="center",
        va="center", zorder=10, bbox=BOX)
ax.text(0.0, 1.6, "decreasing", color=GOLD, fontsize=12, ha="center",
        va="center", zorder=10, bbox=BOX)
ax.text(3.5, -5.2, "increasing", color=GREEN, fontsize=12, ha="center",
        va="center", zorder=10, bbox=BOX)
ax.text(-2.0, 4.9, "$f'(x)=0$", color=ACC, fontsize=11, ha="center",
        va="bottom", zorder=10, bbox=BOX)
ax.text(2.0, -4.9, "$f'(x)=0$", color=ACC, fontsize=11, ha="center",
        va="top", zorder=10, bbox=BOX)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-2-inc-dec.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 2. 答えは区間で書く ══════════════
fig, ax = plt.subplots(figsize=(8.4, 6.2))
axes(ax, XL, (-8.6, 6.4), 1, 2)
for (a, b), c in seg:
    xs = np.linspace(a, b, 300)
    ax.plot(xs, f(xs), color=c, lw=3.0, zorder=5)
for x0 in (-2.0, 2.0):
    ax.plot([x0], [f(x0)], "o", color=ACC, ms=7, zorder=9)
    ax.plot([x0, x0], [-7.4, f(x0)], color=ACC, lw=1.1, ls="--", zorder=4)

# 区間の帯
BAND = -6.6
for (a, b), c, lab in (((-4.2, -2.0), GREEN, "$x < -2$"),
                       ((-2.0, 2.0), GOLD, "$-2 < x < 2$"),
                       ((2.0, 4.2), GREEN, "$x > 2$")):
    ax.plot([a, b], [BAND, BAND], color=c, lw=5.0, solid_capstyle="butt",
            zorder=6)
    ax.text((a + b) / 2, BAND - 0.55, lab, color=c, fontsize=11,
            ha="center", va="top", zorder=10, bbox=BOX)
for x0 in (-2.0, 2.0):
    ax.plot([x0], [BAND], "o", color="white", markeredgecolor=ACC,
            markeredgewidth=2.0, ms=8, zorder=8)
    ax.text(x0, BAND + 0.5, f"${int(x0)}$", color=ACC, fontsize=10.5,
            ha="center", va="bottom", zorder=10, bbox=BOX)
ax.text(-4.25, BAND + 1.6, "the two values where $f'(x)=0$\nsplit the $x$-axis "
                           "into three intervals",
        color=INK, fontsize=10.5, ha="left", va="center", zorder=10, bbox=BOX)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-2-intervals.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 3. f のグラフと f' のグラフ ══════════════
fig, axs = plt.subplots(2, 1, figsize=(8.0, 8.4), sharex=True)

ax = axs[0]
axes(ax, XL, YL, 1, 2, xlab="")
for (a, b), c in seg:
    xs = np.linspace(a, b, 300)
    ax.plot(xs, f(xs), color=c, lw=3.0, zorder=5)
for x0 in (-2.0, 2.0):
    ax.plot([x0], [f(x0)], "o", color=ACC, ms=7, zorder=9)
    ax.axvline(x0, color=ACC, lw=1.1, ls="--", zorder=3)
ax.set_title("the graph of  $y=f(x)$", fontsize=12, color=INK, pad=8)
ax.text(-3.6, 5.4, "up", color=GREEN, fontsize=11, ha="center", va="center",
        zorder=10, bbox=BOX)
ax.text(0.0, 1.6, "down", color=GOLD, fontsize=11, ha="center", va="center",
        zorder=10, bbox=BOX)
ax.text(3.5, -5.2, "up", color=GREEN, fontsize=11, ha="center", va="center",
        zorder=10, bbox=BOX)

ax = axs[1]
axes(ax, XL, (-4.4, 6.4), 1, 2, ylab="$y$")
xs = np.linspace(XL[0] + 0.2, XL[1] - 0.2, 400)
ys = fp(xs)
ax.plot(xs, ys, color=ACC, lw=2.6, zorder=5)
ax.fill_between(xs, 0, ys, where=(ys > 0), color="#eafaef", zorder=2)
ax.fill_between(xs, 0, ys, where=(ys < 0), color="#fdf1e6", zorder=2)
for x0 in (-2.0, 2.0):
    ax.plot([x0], [0], "o", color=ACC, ms=7, zorder=9)
    ax.axvline(x0, color=ACC, lw=1.1, ls="--", zorder=3)
ax.text(-3.5, 3.4, "$f'(x)>0$", color=GREEN, fontsize=11.5, ha="center",
        va="center", zorder=10, bbox=BOX)
ax.text(0.0, -1.9, "$f'(x)<0$", color=GOLD, fontsize=11.5, ha="center",
        va="center", zorder=10, bbox=BOX)
ax.text(3.4, 3.4, "$f'(x)>0$", color=GREEN, fontsize=11.5, ha="center",
        va="center", zorder=10, bbox=BOX)
ax.set_title("the graph of  $y=f'(x)$", fontsize=12, color=INK, pad=8)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-2-fdash.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 4. 文脈：ある日の気温 ══════════════
fig, ax = plt.subplots(figsize=(8.6, 5.2))
axes(ax, (-0.8, 25.0), (7.5, 24.5), 2, 2,
     xlab="$t$ (hours after midnight)", ylab="$T$ ($^\\circ$C)", ypad=26)
T = lambda t: 16 - 6 * np.cos(pi * (t - 5) / 10)
ts = np.linspace(0, 24, 500)
for (a, b), c in (((0, 5), GOLD), ((5, 15), GREEN), ((15, 24), GOLD)):
    tt = np.linspace(a, b, 300)
    ax.plot(tt, T(tt), color=c, lw=3.2, zorder=5)
for t0 in (5, 15):
    ax.plot([t0], [T(t0)], "o", color=ACC, ms=8, zorder=9)
    ax.plot([t0 - 1.6, t0 + 1.6], [T(t0), T(t0)], color=ACC, lw=2.0, zorder=6)
    ax.axvline(t0, color=ACC, lw=1.0, ls="--", zorder=3)
ax.text(2.4, 12.2, "falling", color=GOLD, fontsize=11.5, ha="center",
        va="center", zorder=10, bbox=BOX)
ax.text(10.0, 14.0, "rising", color=GREEN, fontsize=11.5, ha="center",
        va="center", zorder=10, bbox=BOX)
ax.text(20.5, 18.4, "falling", color=GOLD, fontsize=11.5, ha="center",
        va="center", zorder=10, bbox=BOX)
ax.text(5, 8.9, "$t=5$", color=ACC, fontsize=10.5, ha="center", va="top",
        zorder=10, bbox=BOX)
ax.text(15, 23.4, "$t=15$", color=ACC, fontsize=10.5, ha="center",
        va="bottom", zorder=10, bbox=BOX)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-2-context.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 5. 演習用の曲線（停留点 -1 と 3）══════════════
fig, ax = plt.subplots(figsize=(8.4, 5.4))
g = lambda x: 0.2 * x ** 3 - 0.6 * x ** 2 - 1.8 * x + 2
GXL, GYL = (-3.4, 5.4), (-4.4, 4.4)
axes(ax, GXL, GYL, 1, 2)
xs = np.linspace(GXL[0] + 0.2, GXL[1] - 0.2, 500)
ax.plot(xs, g(xs), color=LINE, lw=2.8, zorder=5)
for x0 in (-1.0, 3.0):
    ax.plot([x0], [g(x0)], "o", color=ACC, ms=8, zorder=9)
    ax.plot([x0 - 0.8, x0 + 0.8], [g(x0), g(x0)], color=ACC, lw=2.0, zorder=6)
ax.text(-1.0, g(-1.0) + 0.42, "$(-1,\\,3)$", color=ACC, fontsize=11,
        ha="center", va="bottom", zorder=10, bbox=BOX)
ax.text(3.0, g(3.0) - 0.42, "$(3,\\,-3.4)$", color=ACC, fontsize=11,
        ha="center", va="top", zorder=10, bbox=BOX)
ax.text(-3.2, 3.6, "$y=f(x)$", color=LINE, fontsize=12, ha="left",
        va="center", zorder=10, bbox=BOX)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-2-exercise.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 自己チェック ══════════════
print("main curve f(x)=x^3/4-3x")
print("  stationary points:", [(x, f(x)) for x in (-2, 2)])
print("  f'(-3), f'(0), f'(3):", fp(-3), fp(0), fp(3))
print("exercise curve g(x)=0.2x^3-0.6x^2-1.8x+2")
print("  stationary points:", [(x, round(g(x), 4)) for x in (-1, 3)])
print("temperature T: min", T(5), "at t=5;  max", T(15), "at t=15")
print("figures written to", os.path.normpath(OUT))
