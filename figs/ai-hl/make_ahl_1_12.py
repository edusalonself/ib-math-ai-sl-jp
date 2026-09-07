"""AHL 1.12a / 1.12b（complex numbers）の図を作る。ラベルは英語。
   出力先: ai-hl/01-number-and-algebra/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_1_12.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Arc
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


def plane(ax, xlim, ylim, xlab="Re", ylab="Im"):
    """複素平面の軸まわりをそろえる。"""
    ax.axhline(0, color=GREY, lw=1.4, zorder=1)
    ax.axvline(0, color=GREY, lw=1.4, zorder=1)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.set_xlabel(xlab + "  (real axis)", fontsize=11)
    ax.set_ylabel(ylab + "  (imaginary axis)", fontsize=11)
    tidy(ax)


# ══════════ 1.12a (a) 判別式と放物線 / (b) i の 4 周期 ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.9))

ax = axs[0]
X = np.linspace(-0.4, 4.4, 400)
specs = [(3, GREEN, "$\\Delta = 4 > 0$:  two real roots", "-"),
         (4, GOLD, "$\\Delta = 0$:  one repeated root", "-"),
         (5, ACC, "$\\Delta = -4 < 0$:  no $x$-intercepts", "-")]
for c, col, lab, ls in specs:
    ax.plot(X, X ** 2 - 4 * X + c, color=col, lw=2.6, ls=ls, label=lab)
ax.plot([1, 3], [0, 0], "o", color=GREEN, ms=8, zorder=6)
ax.plot([2], [0], "o", color=GOLD, ms=8, zorder=6)
ax.axhline(0, color=GREY, lw=1.4)
ax.text(3.75, 3.1, "roots  $2 \\pm i$", fontsize=12, color=ACC, ha="center",
        bbox=BOX, zorder=7)
ax.set_xlim(-0.4, 4.4)
ax.set_ylim(-1.9, 7.4)
ax.set_xlabel("$x$")
ax.legend(fontsize=10.5, frameon=False, loc="upper left")
ax.set_title("(a)  the same parabola moved up: what $\\Delta$ tells you",
             fontsize=12, color=INK, pad=10)
tidy(ax)

ax = axs[1]
ax.set_xlim(-2.35, 2.35)
ax.set_ylim(-3.05, 2.55)
ax.set_aspect("equal")
ax.axis("off")
pts = [("$1$", 0.0), ("$i$", 90.0), ("$-1$", 180.0), ("$-i$", 270.0)]
for name, deg in pts:
    a = np.radians(deg)
    p = (1.15 * np.cos(a), 1.15 * np.sin(a))
    ax.add_patch(Circle(p, 0.34, fc="white", ec=LINE, lw=2.2, zorder=6))
    ax.text(p[0], p[1], name, fontsize=14, ha="center", va="center",
            color=LINE, weight="bold", zorder=7)
RA = 1.72
for k in range(4):
    a0 = np.radians(pts[k][1] + 16)
    a1 = np.radians(pts[k][1] + 74)
    ax.add_patch(FancyArrowPatch(
        (RA * np.cos(a0), RA * np.sin(a0)),
        (RA * np.cos(a1), RA * np.sin(a1)),
        connectionstyle="arc3,rad=0.22", arrowstyle="-|>",
        mutation_scale=17, color=ACC, lw=2.0, zorder=4))
    am = np.radians(pts[k][1] + 45)
    ax.text(2.12 * np.cos(am), 2.12 * np.sin(am), "$\\times\\, i$",
            fontsize=11.5, color=ACC, ha="center", va="center", zorder=8)
ax.text(0, -2.35, "back to the start after $4$ steps", fontsize=11.5,
        color=GREY, ha="center", va="center", zorder=5)
ax.set_title("(b)  multiplying by $i$ four times returns you to $1$",
             fontsize=12, color=INK, pad=10)

fig.tight_layout()
save(fig, "ahl-1-12a-disc.svg")


# ══════════ 1.12b (a) modulus と argument / (b) 象限のわな ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 5.0))

ax = axs[0]
z = (3, 2)
ax.add_patch(FancyArrowPatch((0, 0), z, arrowstyle="-|>", mutation_scale=17,
                             color=LINE, lw=2.6, zorder=5))
ax.plot([z[0], z[0]], [0, z[1]], color=GREY, lw=1.4, ls="--", zorder=3)
ax.plot([0, z[0]], [0, 0], color=GOLD, lw=2.4, zorder=3)
ax.plot([z[0]], [z[1]], "o", color=LINE, ms=9, zorder=6)
ax.plot([3], [-2], "o", color=ACC, ms=9, zorder=6)
ax.plot([3, 3], [2, -2], color=ACC, lw=1.2, ls=":", zorder=3)
ax.text(3.18, 2.05, "$z = 3 + 2i$", fontsize=12.5, color=LINE, va="bottom")
ax.text(3.18, -2.05, "$z^{*} = 3 - 2i$", fontsize=12.5, color=ACC, va="top")
ax.add_patch(Arc((0, 0), 1.9, 1.9, theta1=0, theta2=33.69, color=GREEN,
                 lw=2.0, zorder=5))
ax.text(1.20, 0.30, "$\\theta$", fontsize=13, color=GREEN, zorder=7)
ax.text(-3.4, -1.55, "$|z| = \\sqrt{3^{2}+2^{2}} = \\sqrt{13}$", fontsize=12,
        color=LINE, ha="left", va="top", bbox=BOX, zorder=7)
ax.text(1.5, -0.42, "$3$", fontsize=12, color=GOLD, ha="center")
ax.text(3.12, 1.0, "$2$", fontsize=12, color=GREY, ha="left")
ax.text(-3.4, 3.25, "$\\theta = \\arg z = \\arctan\\dfrac{2}{3} = 0.588$",
        fontsize=12, color=GREEN, ha="left", va="top", bbox=BOX, zorder=7)
plane(ax, (-3.6, 5.4), (-3.2, 3.5))
ax.set_title("(a)  modulus is a length, argument is an angle",
             fontsize=12, color=INK, pad=10)

ax = axs[1]
w = (-3, 2)
ax.add_patch(FancyArrowPatch((0, 0), w, arrowstyle="-|>", mutation_scale=17,
                             color=LINE, lw=2.6, zorder=5))
ax.plot([w[0]], [w[1]], "o", color=LINE, ms=9, zorder=6)
ax.text(-3.15, 2.25, "$w = -3 + 2i$", fontsize=12.5, color=LINE,
        ha="left", va="bottom")
wrong = (3 * np.cos(-0.588003) * 1.15, 3 * np.sin(-0.588003) * 1.15)
ax.add_patch(FancyArrowPatch((0, 0), wrong, arrowstyle="-|>",
                             mutation_scale=15, color=ACC, lw=2.0, ls=":",
                             zorder=4))
ax.text(2.95, -2.20, "$\\arctan\\dfrac{2}{-3} = -0.588$\n"
        "points the wrong way", fontsize=11, color=ACC,
        ha="center", va="top", bbox=BOX, zorder=7)
ax.add_patch(Arc((0, 0), 2.6, 2.6, theta1=0, theta2=146.31, color=GREEN,
                 lw=2.0, zorder=5))
ax.text(0.30, 1.50, "$2.55$", fontsize=12, color=GREEN, zorder=7, bbox=BOX)
ax.add_patch(Arc((0, 0), 2.0, 2.0, theta1=-33.69, theta2=0, color=ACC,
                 lw=1.8, ls=":", zorder=5))
ax.text(-5.1, 4.05, "the point is in the second quadrant,\n"
        "so add $\\pi$:   $-0.588 + \\pi = 2.55$", fontsize=11.5,
        color=GREEN, ha="left", va="top", bbox=BOX, zorder=7)
plane(ax, (-5.3, 4.6), (-3.4, 4.3))
ax.set_title("(b)  the calculator angle needs checking against the picture",
             fontsize=12, color=INK, pad=10)

fig.tight_layout()
save(fig, "ahl-1-12b-argand.svg")


# ══════════ 1.12b (a) 共役な組 / (b) 交わらない放物線 ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.9))

ax = axs[0]
r = np.sqrt(10)
th = np.linspace(0, 2 * np.pi, 400)
ax.plot(r * np.cos(th), r * np.sin(th), color=GREY, lw=1.3, ls="--",
        zorder=2)
for pt, col, lab, va in (((1, 3), LINE, "$z = 1 + 3i$", "bottom"),
                         ((1, -3), ACC, "$z^{*} = 1 - 3i$", "top")):
    ax.add_patch(FancyArrowPatch((0, 0), pt, arrowstyle="-|>",
                                 mutation_scale=16, color=col, lw=2.4,
                                 zorder=5))
    ax.plot([pt[0]], [pt[1]], "o", color=col, ms=9, zorder=6)
    ax.text(pt[0] + 0.30, pt[1], lab, fontsize=12.5, color=col, va=va)
ax.plot([1, 1], [3, -3], color=GREY, lw=1.2, ls=":", zorder=3)
ax.text(-4.15, 4.35, "both roots of $x^{2}-2x+10=0$", fontsize=12,
        color=INK, ha="left", va="top", bbox=BOX, zorder=7)
ax.text(-4.15, -2.55, "same distance $\\sqrt{10} = 3.16$\nfrom the origin",
        fontsize=11.5, color=GREY, ha="left", va="top", bbox=BOX, zorder=7)
plane(ax, (-4.3, 4.6), (-4.3, 4.6))
ax.set_title("(a)  a conjugate pair is a mirror image in the real axis",
             fontsize=12, color=INK, pad=10)

ax = axs[1]
X = np.linspace(-2.2, 4.2, 400)
ax.plot(X, X ** 2 - 2 * X + 10, color=LINE, lw=2.8,
        label="$y = x^{2} - 2x + 10$")
ax.axhline(0, color=GREY, lw=1.4)
ax.plot([1], [9], "o", color=GOLD, ms=8, zorder=6)
ax.text(0.85, 9.0, "vertex $(1,\\ 9)$", fontsize=11.5, color=GOLD,
        ha="right", va="center", bbox=BOX, zorder=7)
ax.annotate("", xy=(2.9, 0), xytext=(2.9, 9.0),
            arrowprops=dict(arrowstyle="<->", color=ACC, lw=1.6))
ax.text(3.05, 4.5, "the curve never\nreaches the axis", fontsize=11,
        color=ACC, va="center", bbox=BOX, zorder=7)
ax.text(-2.0, 20.5, "$\\Delta = (-2)^{2} - 4(1)(10) = -36 < 0$", fontsize=12,
        color=INK, ha="left", va="top", bbox=BOX, zorder=7)
ax.set_xlim(-2.2, 4.6)
ax.set_ylim(-2.0, 22.5)
ax.set_xlabel("$x$")
ax.legend(fontsize=11, frameon=False, loc="upper right")
ax.set_title("(b)  no $x$-intercepts is the same information",
             fontsize=12, color=INK, pad=10)
tidy(ax)

fig.tight_layout()
save(fig, "ahl-1-12b-roots.svg")

print("figures written to", os.path.normpath(OUT))
