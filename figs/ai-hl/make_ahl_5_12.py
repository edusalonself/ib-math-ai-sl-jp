"""AHL 5.12a / 5.12b（areas and volumes of revolution）の図を作る。ラベルは英語。
   出力先: ai-hl/05-calculus/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_5_12.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from _graph import INK, GRID, LINE, ACC, GREEN, GREY, GOLD, BOX, FILL

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


# ══════════ 5.12a-1  軸の下と上 ══════════
#  本文の「軸の下に入ると、定積分は負になります」の節に置く図。
fig, ax = plt.subplots(figsize=(6.3, 4.9))
X = np.linspace(-0.2, 3.3, 500)
ax.plot(X, X ** 2 - 4, color=LINE, lw=2.8, label="$y = x^{2} - 4$")
XB = np.linspace(0, 2, 300)
ax.fill_between(XB, 0, XB ** 2 - 4, color="#fdecea", edgecolor=ACC, lw=1.2,
                zorder=2)
XA = np.linspace(2, 3, 200)
ax.fill_between(XA, 0, XA ** 2 - 4, color="#eafaf1", edgecolor=GREEN, lw=1.2,
                zorder=2)
ax.axhline(0, color=GREY, lw=1.2)
ax.plot([2], [0], "o", color=GOLD, ms=8, zorder=6)
ax.text(1.0, -2.1, "integral gives\n$-\\dfrac{16}{3}$", fontsize=11.5,
        ha="center", va="center", color=ACC, zorder=5)
ax.text(2.62, 0.9, "integral gives\n$+\\dfrac{7}{3}$", fontsize=11.5,
        ha="center", va="center", color=GREEN, zorder=5)
ax.text(0.05, 4.35, "definite integral $= -3$        area $= \\dfrac{23}{3}$",
        fontsize=12.5, ha="left", va="top", color=INK, bbox=BOX)
ax.set_xlim(-0.2, 3.3)
ax.set_ylim(-4.8, 5.6)
ax.set_xlabel("$x$")
ax.legend(fontsize=11, frameon=False, loc="lower right")
ax.set_title("below the axis the integral is negative",
             fontsize=12, color=INK, pad=10)
tidy(ax)

fig.tight_layout()
save(fig, "ahl-5-12a-below.svg")


# ══════════ 5.12a-2  y 軸ではさまれた面積 ══════════
#  本文の「y 軸ではさまれた面積」の節に置く図。
fig, ax = plt.subplots(figsize=(5.8, 4.9))
Y = np.linspace(0, 4.6, 400)
ax.plot(np.sqrt(Y), Y, color=LINE, lw=2.8, label="$y = x^{2}$")
YS = np.linspace(0, 4, 300)
ax.fill_betweenx(YS, 0, np.sqrt(YS), color=FILL, edgecolor=LINE, lw=1.2,
                 zorder=2)
for yv in (0.55, 1.55, 2.55, 3.55):
    ax.plot([0, np.sqrt(yv)], [yv, yv], color=GREY, lw=1.0, alpha=0.85,
            zorder=3)
ax.axhline(0, color=GREY, lw=1.2)
ax.axvline(0, color=GREY, lw=1.2)
ax.plot([2], [4], "o", color=GOLD, ms=8, zorder=6)
ax.text(0.42, 2.0, "area $= \\int_{0}^{4} x\\,dy$",
        fontsize=12.5, ha="left", va="center", color=INK, zorder=5, bbox=BOX)
ax.text(1.30, 0.95, "strips are HORIZONTAL:\nwidth $x$, thickness $dy$",
        fontsize=10.5, ha="left", va="top", color=GREY, bbox=BOX, zorder=6)
ax.set_xlim(-0.15, 2.6)
ax.set_ylim(-0.3, 5.3)
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
ax.legend(fontsize=11, frameon=False, loc="upper left")
ax.set_title("the region between the curve and the $y$-axis",
             fontsize=12, color=INK, pad=10)
tidy(ax)

fig.tight_layout()
save(fig, "ahl-5-12a-yaxis.svg")


# ══════════ 5.12b  回転体 ══════════
fig, ax = plt.subplots(figsize=(6.3, 4.9))

# (a) 薄い円板
X = np.linspace(0, 2.05, 400)
ax.plot(X, X ** 2, color=LINE, lw=2.8, label="$y = x^{2}$")
ax.plot(X, -(X ** 2), color=LINE, lw=1.6, ls=":", alpha=0.75)
ax.fill_between(X, 0, X ** 2, color=FILL, edgecolor="none", zorder=1)
x0, dx = 1.35, 0.20
ax.add_patch(plt.Rectangle((x0, -x0 ** 2), dx, 2 * x0 ** 2, fc="#fdecea",
                           ec=ACC, lw=2.0, zorder=4))
ax.add_patch(Ellipse((x0 + dx, 0), 0.16, 2 * x0 ** 2, fc="#fdecea", ec=ACC,
                     lw=2.0, zorder=5))
ax.annotate("", xy=(x0 + dx / 2, 0), xytext=(x0 + dx / 2, x0 ** 2),
            arrowprops=dict(arrowstyle="<->", color=ACC, lw=1.6), zorder=6)
ax.text(x0 - 0.10, 1.0, "radius $= y$", fontsize=11.5, color=ACC, ha="right",
        va="center", zorder=7, bbox=BOX)
ax.annotate("", xy=(x0, -x0 ** 2 - 0.45), xytext=(x0 + dx, -x0 ** 2 - 0.45),
            arrowprops=dict(arrowstyle="<->", color=ACC, lw=1.6))
ax.text(x0 + dx / 2, -x0 ** 2 - 1.05, "thickness $= dx$", fontsize=11,
        color=ACC, ha="center", bbox=BOX, zorder=7)
ax.axhline(0, color=GREY, lw=1.4)
ax.text(0.06, 3.85, "one thin disc:\n$\\pi y^{2}\\,dx$", fontsize=12.5,
        ha="left", va="top", color=INK, bbox=BOX)
ax.text(0.06, 2.35, "stack them all up:\n"
        "$V = \\int_{0}^{2}\\pi y^{2}\\,dx$", fontsize=12,
        ha="left", va="top", color=GREEN)
ax.set_xlim(-0.1, 2.3)
ax.set_ylim(-4.4, 4.4)
ax.set_xlabel("$x$")
ax.legend(fontsize=11, frameon=False, loc="lower right")
ax.set_title("the solid is a stack of thin discs", fontsize=12,
             color=INK, pad=10)
tidy(ax)

fig.tight_layout()
save(fig, "ahl-5-12b-disc.svg")


# ══════════ 5.12b  円錐で確かめる ══════════
fig, ax = plt.subplots(figsize=(6.0, 4.9))
X = np.linspace(0, 6, 200)
ax.plot(X, X / 2, color=LINE, lw=2.8, label="$y = \\dfrac{x}{2}$")
ax.plot(X, -X / 2, color=LINE, lw=1.6, ls=":", alpha=0.75)
ax.fill_between(X, -X / 2, X / 2, color=FILL, edgecolor="none", zorder=1)
ax.add_patch(Ellipse((6, 0), 0.72, 6.0, fc="none", ec=LINE, lw=2.4, zorder=4))
ax.plot([6, 6], [-3, 3], color=GREY, lw=1.0, ls="--", zorder=3)
ax.axhline(0, color=GREY, lw=1.4)
ax.annotate("", xy=(6.55, 0), xytext=(6.55, 3),
            arrowprops=dict(arrowstyle="<->", color=GOLD, lw=1.6))
ax.text(6.75, 1.5, "$r = 3$", fontsize=12, color=GOLD, va="center")
ax.annotate("", xy=(0, -3.75), xytext=(6, -3.75),
            arrowprops=dict(arrowstyle="<->", color=GOLD, lw=1.6))
ax.text(3, -4.35, "$h = 6$", fontsize=12, color=GOLD, ha="center")
ax.text(0.15, 3.9, "$V = \\int_{0}^{6}\\pi\\left("
        "\\dfrac{x}{2}\\right)^{2}dx = 18\\pi$", fontsize=12.5, ha="left",
        va="top", color=INK, bbox=BOX)
ax.text(0.15, 2.05, "cone formula:  $\\dfrac{1}{3}\\pi r^{2}h "
        "= \\dfrac{1}{3}\\pi(9)(6) = 18\\pi$   ✓", fontsize=11.5,
        ha="left", va="top", color=GREEN)
ax.set_xlim(-0.3, 7.9)
ax.set_ylim(-4.9, 4.9)
ax.set_xlabel("$x$")
ax.legend(fontsize=11, frameon=False, loc="lower right")
ax.set_title("a check: rotating a line gives a cone", fontsize=12,
             color=INK, pad=10)
tidy(ax)

fig.tight_layout()
save(fig, "ahl-5-12b-cone.svg")

print("figures written to", os.path.normpath(OUT))
