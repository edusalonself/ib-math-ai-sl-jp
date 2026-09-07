"""AHL 5.9a / 5.9b / 5.9c の図を作る。ラベルは英語。
   出力先: ai-hl/05-calculus/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_5_9.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
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


# ══════════ 5.9a-1  関数とその導関数（2 行 2 列） ══════════
fig, axs = plt.subplots(2, 2, figsize=(11.4, 8.2))

# (a) sin と cos
ax = axs[0, 0]
X = np.linspace(0, 2 * np.pi, 600)
ax.plot(X, np.sin(X), color=LINE, lw=2.6, label="$f(x) = \\sin x$")
ax.plot(X, np.cos(X), color=ACC, lw=2.2, ls="--",
        label="$f'(x) = \\cos x$")
for x0 in (0.0, np.pi / 2, np.pi):
    ax.plot([x0], [np.sin(x0)], "o", color=LINE, ms=6, zorder=6)
    ax.plot([x0], [np.cos(x0)], "o", color=ACC, ms=6, zorder=6)
ax.axhline(0, color=GREY, lw=1.0, alpha=0.7)
ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(-1.35, 1.55)
ax.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi])
ax.set_xticklabels(["$0$", "$\\frac{\\pi}{2}$", "$\\pi$",
                    "$\\frac{3\\pi}{2}$", "$2\\pi$"])
ax.set_xlabel("$x$  (radians)")
ax.legend(fontsize=10.5, frameon=False, loc="lower left")
ax.set_title("(a)  where $\\sin x$ is steepest, $\\cos x$ is largest",
             fontsize=12, color=INK, pad=10)
tidy(ax)

# (b) e^x は自分自身
ax = axs[0, 1]
X = np.linspace(-1.5, 2.0, 500)
ax.plot(X, np.exp(X), color=LINE, lw=2.8,
        label="$f(x) = e^{x}$  and  $f'(x) = e^{x}$")
x0 = 1.0
y0 = np.exp(x0)
XT = np.linspace(0.1, 1.9, 50)
ax.plot(XT, y0 + y0 * (XT - x0), color=ACC, lw=2.0, ls="--",
        label="tangent at $x = 1$")
ax.plot([x0], [y0], "o", color=GOLD, ms=8, zorder=6)
ax.text(x0 + 0.06, y0 - 1.4,
        "at $x = 1$:\nheight $= e$\ngradient $= e$", fontsize=10.5,
        color=GOLD, bbox=BOX, va="top")
ax.set_xlim(-1.5, 2.0)
ax.set_ylim(0, 7.6)
ax.set_xlabel("$x$")
ax.legend(fontsize=10.5, frameon=False, loc="upper left")
ax.set_title("(b)  $e^{x}$ is its own derivative", fontsize=12,
             color=INK, pad=10)
tidy(ax)

# (c) ln x と 1/x
ax = axs[1, 0]
X = np.linspace(0.12, 5.0, 600)
ax.plot(X, np.log(X), color=LINE, lw=2.6, label="$f(x) = \\ln x$")
ax.plot(X, 1 / X, color=ACC, lw=2.2, ls="--", label="$f'(x) = \\dfrac{1}{x}$")
ax.axhline(0, color=GREY, lw=1.0, alpha=0.7)
ax.plot([1], [0], "o", color=LINE, ms=6, zorder=6)
ax.plot([1], [1], "o", color=ACC, ms=6, zorder=6)
ax.set_xlim(0, 5)
ax.set_ylim(-2.2, 4.4)
ax.set_xlabel("$x > 0$")
ax.legend(fontsize=10.5, frameon=False, loc="upper right")
ax.set_title("(c)  $\\ln x$ flattens out, so $\\dfrac{1}{x}$ shrinks",
             fontsize=12, color=INK, pad=10)
tidy(ax)

# (d) sqrt(x) = x^{1/2}
ax = axs[1, 1]
X = np.linspace(0.05, 5.0, 600)
ax.plot(X, np.sqrt(X), color=LINE, lw=2.6,
        label="$f(x) = x^{\\frac{1}{2}}$")
ax.plot(X, 0.5 / np.sqrt(X), color=ACC, lw=2.2, ls="--",
        label="$f'(x) = \\dfrac{1}{2}x^{-\\frac{1}{2}}$")
ax.plot([4], [2], "o", color=LINE, ms=6, zorder=6)
ax.plot([4], [0.25], "o", color=ACC, ms=6, zorder=6)
ax.set_xlim(0, 5)
ax.set_ylim(0, 2.9)
ax.set_xlabel("$x \\geq 0$")
ax.legend(fontsize=10.5, frameon=False, loc="upper right")
ax.set_title("(d)  the power rule now allows $n = \\dfrac{1}{2}$",
             fontsize=12, color=INK, pad=10)
tidy(ax)

fig.suptitle("Three of the new derivatives, and the power rule with "
             "a fractional $n$", fontsize=14, y=0.995)
fig.tight_layout(rect=(0, 0, 1, 0.968))
save(fig, "ahl-5-9a-derivs.svg")


# ══════════ 5.9a-2  radian でないと成り立たない ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.4))

ax = axs[0]
X = np.linspace(-0.6, 6.9, 700)
ax.plot(X, np.sin(X), color=LINE, lw=2.6, label="$y = \\sin x$")
XT = np.linspace(-0.5, 1.15, 40)
ax.plot(XT, XT, color=ACC, lw=2.2, ls="--",
        label="tangent at $x = 0$:  gradient $= 1$")
ax.plot([0], [0], "o", color=GOLD, ms=8, zorder=6)
ax.axhline(0, color=GREY, lw=1.0, alpha=0.7)
ax.set_xlim(-0.6, 6.9)
ax.set_ylim(-1.3, 1.5)
ax.set_xlabel("$x$  measured in RADIANS")
ax.legend(fontsize=10.5, frameon=False, loc="lower left")
ax.set_title("in radians the gradient at $0$ is exactly $1$",
             fontsize=12, color=GREEN, pad=10)
tidy(ax)

ax = axs[1]
XD = np.linspace(-40, 400, 800)
ax.plot(XD, np.sin(np.radians(XD)), color=LINE, lw=2.6,
        label="$y = \\sin x^{\\circ}$")
XT = np.linspace(-35, 70, 40)
ax.plot(XT, np.radians(1) * XT, color=ACC, lw=2.2, ls="--",
        label="tangent at $x = 0$:  gradient $= \\frac{\\pi}{180} = 0.0175$")
ax.plot([0], [0], "o", color=GOLD, ms=8, zorder=6)
ax.axhline(0, color=GREY, lw=1.0, alpha=0.7)
ax.set_xlim(-40, 400)
ax.set_ylim(-1.3, 1.5)
ax.set_xlabel("$x$  measured in DEGREES")
ax.legend(fontsize=10.5, frameon=False, loc="lower left")
ax.set_title("in degrees the same curve is $57$ times flatter",
             fontsize=12, color=ACC, pad=10)
tidy(ax)

fig.text(0.5, -0.05,
         "$\\dfrac{d}{dx}\\sin x = \\cos x$ is true only when $x$ is in "
         "radians.   In degrees the gradient would be "
         "$\\dfrac{\\pi}{180}\\cos x^{\\circ}$.",
         fontsize=12.5, ha="center", color=INK)
fig.tight_layout()
save(fig, "ahl-5-9a-radian.svg")

# ══════════ 5.9b-1  chain rule = 中身の速さが倍率になる ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.6))

ax = axs[0]
X = np.linspace(-0.5, 3.4, 800)
ax.plot(X, np.sin(X), color=GREY, lw=2.2, label="$y = \\sin x$")
ax.plot(X, np.sin(4 * X), color=LINE, lw=2.6, label="$y = \\sin 4x$")
XT = np.linspace(-0.28, 0.28, 30)
ax.plot(XT, XT, color=GREY, lw=1.8, ls="--")
XT2 = np.linspace(-0.12, 0.12, 30)
ax.plot(XT2, 4 * XT2, color=ACC, lw=2.2, ls="--")
ax.plot([0], [0], "o", color=GOLD, ms=8, zorder=6)
ax.axhline(0, color=GREY, lw=1.0, alpha=0.7)
ax.set_xlim(-0.5, 3.4)
ax.set_ylim(-1.35, 1.75)
ax.set_xlabel("$x$  (radians)")
ax.legend(fontsize=10.5, frameon=False, loc="lower left")
ax.text(1.55, 1.38, "gradient at $0$:  $1 \\ \\to \\ 4$", fontsize=12,
        color=ACC, ha="center", bbox=BOX)
ax.set_title("(a)  the inside runs $4$ times faster,\nso the gradient is "
             "$4$ times bigger", fontsize=12, color=INK, pad=10)
tidy(ax)

ax = axs[1]
X = np.linspace(-1.2, 1.2, 600)
ax.plot(X, np.exp(X), color=GREY, lw=2.2, label="$y = e^{x}$")
ax.plot(X, np.exp(3 * X), color=LINE, lw=2.6, label="$y = e^{3x}$")
XT = np.linspace(-0.6, 0.6, 30)
ax.plot(XT, 1 + XT, color=GREY, lw=1.8, ls="--")
XT2 = np.linspace(-0.35, 0.35, 30)
ax.plot(XT2, 1 + 3 * XT2, color=ACC, lw=2.2, ls="--")
ax.plot([0], [1], "o", color=GOLD, ms=8, zorder=6)
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(0, 6.6)
ax.set_xlabel("$x$")
ax.legend(fontsize=10.5, frameon=False, loc="upper left")
ax.text(0.35, 5.2, "gradient at $0$:  $1 \\ \\to \\ 3$", fontsize=12,
        color=ACC, ha="center", bbox=BOX)
ax.set_title("(b)  the same idea with $e^{x}$:\nthe inside factor $3$ "
             "multiplies the gradient", fontsize=12, color=INK, pad=10)
tidy(ax)

fig.text(0.5, -0.07,
         "Chain rule:  differentiate the outside, then multiply by the "
         "derivative of the inside.",
         fontsize=12.5, ha="center", color=INK)
fig.tight_layout()
save(fig, "ahl-5-9b-chain.svg")


# ══════════ 5.9b-2  product rule の面積の絵 ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.9))

ax = axs[0]
u, v, du, dv = 3.0, 2.0, 0.9, 0.7
ax.add_patch(plt.Rectangle((0, 0), u, v, fc=FILL, ec=LINE, lw=2.2, zorder=2))
ax.add_patch(plt.Rectangle((u, 0), du, v, fc="#fdecea", ec=ACC, lw=2.0,
                           zorder=2))
ax.add_patch(plt.Rectangle((0, v), u, dv, fc="#fdecea", ec=ACC, lw=2.0,
                           zorder=2))
ax.add_patch(plt.Rectangle((u, v), du, dv, fc="#f2f3f5", ec=GREY, lw=1.6,
                           ls="--", zorder=2))
ax.text(u / 2, v / 2, "$uv$", fontsize=16, ha="center", va="center",
        color=LINE)
ax.text(u + du / 2, v / 2, "$v\\,\\delta u$", fontsize=12.5, ha="center",
        va="center", color=ACC)
ax.text(u / 2, v + dv / 2, "$u\\,\\delta v$", fontsize=12.5, ha="center",
        va="center", color=ACC)
ax.text(u + du / 2, v + dv + 0.55, "$\\delta u\\,\\delta v$\n(tiny)",
        fontsize=10.5, ha="center", va="center", color=GREY)
ax.annotate("", xy=(0, -0.32), xytext=(u, -0.32),
            arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.4))
ax.text(u / 2, -0.70, "$u$", fontsize=13, ha="center", color=GREY)
ax.annotate("", xy=(u, -0.32), xytext=(u + du, -0.32),
            arrowprops=dict(arrowstyle="<->", color=ACC, lw=1.4))
ax.text(u + du / 2, -0.70, "$\\delta u$", fontsize=12, ha="center", color=ACC)
ax.annotate("", xy=(-0.32, 0), xytext=(-0.32, v),
            arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.4))
ax.text(-0.70, v / 2, "$v$", fontsize=13, va="center", ha="center",
        color=GREY)
ax.annotate("", xy=(-0.32, v), xytext=(-0.32, v + dv),
            arrowprops=dict(arrowstyle="<->", color=ACC, lw=1.4))
ax.text(-0.78, v + dv / 2, "$\\delta v$", fontsize=12, va="center",
        ha="center", color=ACC)
ax.set_xlim(-1.3, 4.6)
ax.set_ylim(-1.2, 4.3)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("(a)  the extra area is $v\\,\\delta u + u\\,\\delta v$",
             fontsize=12, color=INK, pad=10)

ax = axs[1]
X = np.linspace(-4.2, 1.3, 700)
ax.plot(X, X ** 2 * np.exp(X), color=LINE, lw=2.8, label="$y = x^{2}e^{x}$")
ax.plot(X, X * np.exp(X) * (X + 2), color=ACC, lw=2.2, ls="--",
        label="$\\dfrac{dy}{dx} = xe^{x}(x + 2)$")
for x0 in (-2.0, 0.0):
    ax.plot([x0], [x0 ** 2 * np.exp(x0)], "o", color=LINE, ms=7, zorder=6)
    ax.plot([x0], [0], "o", color=ACC, ms=7, zorder=6)
ax.axhline(0, color=GREY, lw=1.0, alpha=0.7)
ax.set_xlim(-4.2, 1.3)
ax.set_ylim(-1.15, 3.9)
ax.set_xlabel("$x$")
ax.legend(fontsize=10.5, frameon=False, loc="upper left")
ax.text(-4.05, -0.88, "the derivative is $0$ where the curve is flat",
        fontsize=10.5, color=GREY, ha="left")
ax.set_title("(b)  checking the product rule on $x^{2}e^{x}$",
             fontsize=12, color=INK, pad=10)
tidy(ax)

fig.tight_layout()
save(fig, "ahl-5-9b-product.svg")


# ══════════ 5.9c  related rates ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.6))

ax = axs[0]
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")
boxes = [(1.6, "$\\dfrac{dV}{dt}$\ngiven"),
         (5.0, "$\\dfrac{dV}{dr}$\nfrom $V = \\frac{4}{3}\\pi r^{3}$"),
         (8.4, "$\\dfrac{dr}{dt}$\nwanted")]
for cx, txt in boxes:
    ax.add_patch(plt.Rectangle((cx - 1.4, 3.15), 2.8, 1.75, fc=FILL, ec=LINE,
                               lw=2.0, zorder=2))
    ax.text(cx, 4.02, txt, fontsize=12, ha="center", va="center", color=INK,
            zorder=3)
ax.text(5.0, 1.9,
        "$\\dfrac{dV}{dt} \\ = \\ \\dfrac{dV}{dr} \\ \\times \\ "
        "\\dfrac{dr}{dt}$", fontsize=17, ha="center", va="center", color=ACC)
ax.text(5.0, 0.6, "two of the three are known, so the third comes out",
        fontsize=11, ha="center", color=GREY)
ax.plot([3.0, 3.6], [4.02, 4.02], color=GREY, lw=1.6)
ax.plot([6.4, 7.0], [4.02, 4.02], color=GREY, lw=1.6)
ax.set_title("(a)  one chain links the two rates", fontsize=12, color=INK,
             pad=10)

ax = axs[1]
T = np.linspace(0, 60, 600)
Rr = (3 * (30 * T) / (4 * np.pi)) ** (1 / 3)
ax.plot(T, Rr, color=LINE, lw=2.8, label="$r$  (cm)")
t5 = 4 * np.pi * 5 ** 3 / 3 / 30
ax.plot([t5], [5.0], "o", color=GOLD, ms=9, zorder=6)
TT = np.linspace(t5 - 18, t5 + 22, 40)
ax.plot(TT, 5.0 + (30 / (100 * np.pi)) * (TT - t5), color=ACC, lw=2.2,
        ls="--", label="tangent:  gradient $= 0.0955$")
ax.text(t5 + 1.0, 2.75,
        "at $r = 5$:\n$\\dfrac{dr}{dt} = 0.0955$ cm s$^{-1}$",
        fontsize=11, color=GOLD, bbox=BOX, va="center", ha="center")
ax.set_xlim(0, 60)
ax.set_ylim(0, 6.9)
ax.set_xlabel("$t$  (seconds)")
ax.legend(fontsize=10.5, frameon=False, loc="lower right")
ax.set_title("(b)  air goes in at a steady rate,\nbut $r$ grows more and "
             "more slowly", fontsize=12, color=INK, pad=10)
tidy(ax)

fig.tight_layout()
save(fig, "ahl-5-9c-rates.svg")

print("figures written to", os.path.normpath(OUT))
