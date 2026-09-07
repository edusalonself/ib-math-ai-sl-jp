"""AHL 1.13a / 1.13b（polar・exponential form と正弦波の合成）の図を作る。
   ラベルは英語。出力先: ai-hl/01-number-and-algebra/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_1_13.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Arc, Polygon
from _graph import INK, GRID, LINE, ACC, GREEN, GREY, GOLD, BOX, FILL

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "01-number-and-algebra", "img")
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


def plane(ax, xlim, ylim):
    ax.axhline(0, color=GREY, lw=1.4, zorder=1)
    ax.axvline(0, color=GREY, lw=1.4, zorder=1)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.set_xlabel("Re", fontsize=11)
    ax.set_ylabel("Im", fontsize=11)
    tidy(ax)


def vec(ax, p, q, color, lw=2.6, z=5, ls="-"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=17,
                                 color=color, lw=lw, zorder=z, ls=ls))


# ══════════ 1.13a fig 1: 3 つの form / polar → Cartesian ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 5.0))

ax = axs[0]
z = (1.0, np.sqrt(3))
vec(ax, (0, 0), z, LINE)
ax.plot([z[0]], [z[1]], "o", color=LINE, ms=9, zorder=6)
ax.plot([z[0], z[0]], [0, z[1]], color=GREY, lw=1.4, ls="--", zorder=3)
ax.plot([0, z[0]], [0, 0], color=GOLD, lw=2.6, zorder=3)
ax.add_patch(Arc((0, 0), 1.15, 1.15, theta1=0, theta2=60, color=GREEN,
                 lw=2.0, zorder=5))
ax.text(0.74, 0.28, "$\\theta = \\dfrac{\\pi}{3}$", fontsize=12.5,
        color=GREEN, zorder=7, bbox=BOX)
ax.text(0.30, 1.30, "$r = 2$", fontsize=12.5, color=LINE, zorder=7, bbox=BOX)
ax.text(0.5, -0.30, "$a = 2\\cos\\theta = 1$", fontsize=11, color=GOLD,
        ha="center", zorder=7, bbox=BOX)
ax.text(1.12, 0.90, "$b = 2\\sin\\theta = \\sqrt{3}$", fontsize=11,
        color=GREY, ha="left", zorder=7, bbox=BOX)
ax.text(1.10, 1.80, "$z = 1 + \\sqrt{3}\\,i$", fontsize=12.5, color=LINE,
        ha="left", va="bottom")
ax.text(-2.05, -1.35, "$z = 1 + \\sqrt{3}\\,i$\n"
        "$z = 2\\left(\\cos\\dfrac{\\pi}{3} + i\\sin\\dfrac{\\pi}{3}\\right)$\n"
        "$z = 2\\,\\mathrm{cis}\\,\\dfrac{\\pi}{3} = 2e^{i\\pi/3}$",
        fontsize=11.5, color=INK, ha="left", va="top", bbox=BOX, zorder=8)
plane(ax, (-2.2, 3.0), (-2.9, 2.6))
ax.set_title("(a)  one point, three ways of writing it",
             fontsize=12, color=INK, pad=10)

ax = axs[1]
w = (-2.0, 2 * np.sqrt(3))
vec(ax, (0, 0), w, ACC)
ax.plot([w[0]], [w[1]], "o", color=ACC, ms=9, zorder=6)
ax.plot([w[0], w[0]], [0, w[1]], color=GREY, lw=1.4, ls="--", zorder=3)
ax.plot([0, w[0]], [0, 0], color=GOLD, lw=2.6, zorder=3)
ax.add_patch(Arc((0, 0), 3.6, 3.6, theta1=0, theta2=120, color=GREEN,
                 lw=2.0, zorder=5))
ax.text(0.98, 1.62, "$\\dfrac{2\\pi}{3}$", fontsize=12.5, color=GREEN,
        zorder=7, bbox=BOX)
ax.text(-1.05, -0.42, "$a = 4\\cos\\dfrac{2\\pi}{3} = -2$", fontsize=11,
        color=GOLD, ha="center", zorder=7, bbox=BOX)
ax.text(-4.45, 2.15, "$b = 4\\sin\\dfrac{2\\pi}{3} = 2\\sqrt{3}$",
        fontsize=11, color=GREY, ha="left", zorder=7, bbox=BOX)
ax.text(-2.15, 3.75, "$4\\,\\mathrm{cis}\\,\\dfrac{2\\pi}{3}"
        " = -2 + 2\\sqrt{3}\\,i$", fontsize=12.5, color=ACC, ha="left",
        va="bottom", bbox=BOX, zorder=8)
plane(ax, (-4.6, 4.0), (-2.2, 5.0))
ax.set_title("(b)  going back: $a = r\\cos\\theta$,  $b = r\\sin\\theta$",
             fontsize=12, color=INK, pad=10)

fig.tight_layout()
save(fig, "ahl-1-13a-forms.svg")


# ══════════ 1.13a fig 2: かけ算＝回転と拡大 / 足し算＝ベクトル ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 5.0))

ax = axs[0]
z = np.array([3.0, 1.0])
iz = np.array([-1.0, 3.0])
tz = np.array([6.0, 2.0])
vec(ax, (0, 0), tz, GOLD, lw=2.2)
vec(ax, (0, 0), z, LINE)
vec(ax, (0, 0), iz, ACC)
for p, col, lab, dx, dy, ha, va in (
        (z, LINE, "$z = 3 + i$", 0.20, -0.30, "left", "top"),
        (iz, ACC, "$iz = -1 + 3i$", 0.20, 0.28, "left", "bottom"),
        (tz, GOLD, "$2z = 6 + 2i$", 0.20, 0.28, "left", "bottom")):
    ax.plot([p[0]], [p[1]], "o", color=col, ms=8, zorder=6)
    ax.text(p[0] + dx, p[1] + dy, lab, fontsize=12, color=col, ha=ha,
            va=va)
ax.add_patch(Arc((0, 0), 3.0, 3.0, theta1=18.43, theta2=108.43, color=ACC,
                 lw=1.8, ls=":", zorder=4))
ax.text(0.30, 1.75, "$\\times\\, i$: turn by $\\dfrac{\\pi}{2}$,\n"
        "same length", fontsize=11, color=ACC, ha="left", va="center",
        bbox=BOX, zorder=8)
ax.text(2.9, -1.35, "$\\times\\, 2$: same direction,\ntwice as long",
        fontsize=11, color=GOLD, ha="center", va="top", bbox=BOX, zorder=8)
plane(ax, (-2.6, 7.4), (-2.9, 4.4))
ax.set_title("(a)  multiplying turns and stretches", fontsize=12,
             color=INK, pad=10)

ax = axs[1]
z1 = np.array([4.0, 1.0])
z2 = np.array([1.0, 3.0])
s = z1 + z2
ax.add_patch(Polygon([(0, 0), tuple(z1), tuple(s), tuple(z2)], closed=True,
                     fc=FILL, ec="none", zorder=1))
vec(ax, (0, 0), z1, LINE)
vec(ax, (0, 0), z2, ACC)
vec(ax, (0, 0), s, GREEN, lw=3.0)
vec(ax, z1, s, ACC, lw=1.6, ls=":", z=4)
vec(ax, z2, s, LINE, lw=1.6, ls=":", z=4)
for p, col, lab in ((z1, LINE, "$z_1 = 4 + i$"), (z2, ACC, "$z_2 = 1 + 3i$"),
                    (s, GREEN, "$z_1 + z_2 = 5 + 4i$")):
    ax.plot([p[0]], [p[1]], "o", color=col, ms=8, zorder=6)
ax.text(4.15, 0.75, "$z_1 = 4 + i$", fontsize=12, color=LINE, ha="left")
ax.text(0.80, 3.30, "$z_2 = 1 + 3i$", fontsize=12, color=ACC, ha="right",
        va="bottom")
ax.text(5.15, 4.10, "$z_1 + z_2 = 5 + 4i$", fontsize=12, color=GREEN,
        ha="left", va="bottom")
ax.text(-1.85, -1.10, "the diagonal is never longer than\n"
        "the two sides added:  $|z_1+z_2| \\leq |z_1| + |z_2|$",
        fontsize=11, color=GREY, ha="left", va="top", bbox=BOX, zorder=8)
plane(ax, (-2.0, 8.6), (-2.3, 5.4))
ax.set_title("(b)  adding follows the parallelogram", fontsize=12,
             color=INK, pad=10)

fig.tight_layout()
save(fig, "ahl-1-13a-mult.svg")


# ══════════ 1.13b fig 1: 合成波と phasor 三角形 ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.9))

ax = axs[0]
T = np.linspace(0, 0.26, 900)
w = 50.0
ax.plot(T, 3 * np.cos(w * T), color=LINE, lw=2.0,
        label="$3\\cos 50t$")
ax.plot(T, 4 * np.cos(w * T + np.pi / 2), color=ACC, lw=2.0, ls="--",
        label="$4\\cos\\left(50t + \\dfrac{\\pi}{2}\\right)$")
B = np.arctan2(4, 3)
ax.plot(T, 5 * np.cos(w * T + B), color=GREEN, lw=3.0,
        label="sum $= 5\\cos(50t + 0.927)$")
ax.axhline(0, color=GREY, lw=1.2)
ax.axhline(5, color=GREEN, lw=1.0, ls=":")
ax.axhline(-5, color=GREEN, lw=1.0, ls=":")
ax.text(0.262, 5.0, "$5$", fontsize=11, color=GREEN, va="center")
ax.set_xlim(0, 0.275)
ax.set_ylim(-6.4, 8.6)
ax.set_xlabel("$t$")
ax.legend(fontsize=10, frameon=False, loc="upper right", ncol=1)
ax.set_title("(a)  the sum is a sine wave of the same period",
             fontsize=12, color=INK, pad=10)
tidy(ax)

ax = axs[1]
p1 = np.array([3.0, 0.0])
p2 = np.array([0.0, 4.0])
s = p1 + p2
ax.add_patch(Polygon([(0, 0), tuple(p1), tuple(s)], closed=True, fc=FILL,
                     ec="none", zorder=1))
vec(ax, (0, 0), p1, LINE)
vec(ax, p1, s, ACC)
vec(ax, (0, 0), s, GREEN, lw=3.0)
ax.plot([s[0]], [s[1]], "o", color=GREEN, ms=9, zorder=6)
ax.add_patch(Arc((0, 0), 2.2, 2.2, theta1=0, theta2=np.degrees(B),
                 color=GOLD, lw=2.0, zorder=5))
ax.text(1.32, 0.52, "$B = 0.927$", fontsize=12, color=GOLD, zorder=7,
        bbox=BOX)
ax.text(1.5, -0.42, "$3$", fontsize=12.5, color=LINE, ha="center")
ax.text(3.16, 2.0, "$4$", fontsize=12.5, color=ACC, ha="left")
ax.text(1.05, 2.75, "$A = 5$", fontsize=13, color=GREEN, ha="center",
        bbox=BOX, zorder=7)
ax.text(-1.85, -1.30, "phasors:  $3\\,\\mathrm{cis}\\,0 = 3$\n"
        "$4\\,\\mathrm{cis}\\,\\dfrac{\\pi}{2} = 4i$\n"
        "sum $= 3 + 4i$", fontsize=11.5, color=INK, ha="left", va="top",
        bbox=BOX, zorder=8)
plane(ax, (-2.0, 5.6), (-3.4, 5.2))
ax.set_title("(b)  the same sum, drawn as phasors", fontsize=12,
             color=INK, pad=10)

fig.tight_layout()
save(fig, "ahl-1-13b-add.svg")


# ══════════ 1.13b fig 2: 振幅は足し算ではない ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.9))

ax = axs[0]
q1 = 5 * np.array([np.cos(np.pi / 3), np.sin(np.pi / 3)])
q2 = 5 * np.array([np.cos(-np.pi / 3), np.sin(-np.pi / 3)])
s = q1 + q2
ax.add_patch(Polygon([(0, 0), tuple(q1), tuple(s), tuple(q2)], closed=True,
                     fc=FILL, ec="none", zorder=1))
vec(ax, (0, 0), q1, LINE)
vec(ax, (0, 0), q2, ACC)
vec(ax, (0, 0), s, GREEN, lw=3.2)
ax.plot([s[0]], [s[1]], "o", color=GREEN, ms=9, zorder=6)
ax.text(2.7, 4.55, "$5\\,\\mathrm{cis}\\,\\dfrac{\\pi}{3}$", fontsize=12,
        color=LINE, ha="left", va="bottom")
ax.text(2.7, -4.55, "$5\\,\\mathrm{cis}\\left(-\\dfrac{\\pi}{3}\\right)$",
        fontsize=12, color=ACC, ha="left", va="top")
ax.text(5.15, 0.60, "sum $= 5$", fontsize=13, color=GREEN, ha="center",
        bbox=BOX, zorder=7)
ax.text(-5.6, -4.75, "the imaginary parts cancel:\n"
        "$(2.5 + 4.33i) + (2.5 - 4.33i) = 5$", fontsize=11.5, color=GREY,
        ha="left", va="top", bbox=BOX, zorder=8)
plane(ax, (-5.8, 8.4), (-6.6, 6.6))
ax.set_title("(a)  two amplitudes of $5$ give $5$, not $10$",
             fontsize=12, color=INK, pad=10)

ax = axs[1]
T = np.linspace(0, 0.33, 900)
w = 40.0
ax.plot(T, 5 * np.cos(w * T + np.pi / 3), color=LINE, lw=2.0,
        label="$5\\cos\\left(40t + \\dfrac{\\pi}{3}\\right)$")
ax.plot(T, 5 * np.cos(w * T - np.pi / 3), color=ACC, lw=2.0, ls="--",
        label="$5\\cos\\left(40t - \\dfrac{\\pi}{3}\\right)$")
ax.plot(T, 5 * np.cos(w * T), color=GREEN, lw=3.0,
        label="sum $= 5\\cos 40t$")
ax.axhline(0, color=GREY, lw=1.2)
ax.axhline(10, color=GREY, lw=1.0, ls=":")
ax.text(0.004, 10.35, "$10$: the two amplitudes simply added",
        fontsize=10.5, color=GREY, ha="left", va="bottom")
ax.set_xlim(0, 0.35)
ax.set_ylim(-7.2, 16.0)
ax.set_xlabel("$t$")
ax.legend(fontsize=10, frameon=False, loc="upper right")
ax.set_title("(b)  the sum never reaches $10$", fontsize=12, color=INK,
             pad=10)
tidy(ax)

fig.tight_layout()
save(fig, "ahl-1-13b-cancel.svg")

print("figures written to", os.path.normpath(OUT))
