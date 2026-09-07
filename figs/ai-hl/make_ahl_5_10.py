"""AHL 5.10（second derivative）の図を作る。ラベルは英語。
   出力先: ai-hl/05-calculus/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_5_10.py
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


# ══════════ 5.10-1  second derivative test ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.9))

# (a) f, f', f'' を重ねる
ax = axs[0]
X = np.linspace(-2.6, 4.6, 700)
F = X ** 3 - 3 * X ** 2 - 9 * X + 5
D1 = 3 * X ** 2 - 6 * X - 9
D2 = 6 * X - 6
ax.plot(X, F, color=LINE, lw=2.8, label="$f(x) = x^{3}-3x^{2}-9x+5$")
ax.plot(X, D1, color=ACC, lw=2.0, ls="--", label="$f'(x) = 3x^{2}-6x-9$")
ax.plot(X, D2, color=GREEN, lw=2.0, ls=":", label="$f''(x) = 6x-6$")
ax.axhline(0, color=GREY, lw=1.0, alpha=0.7)
ax.plot([-1], [10], "o", color=LINE, ms=8, zorder=6)
ax.plot([3], [-22], "o", color=LINE, ms=8, zorder=6)
ax.plot([-1], [-12], "o", color=GREEN, ms=7, zorder=6)
ax.plot([3], [12], "o", color=GREEN, ms=7, zorder=6)
ax.annotate("max $(-1, 10)$\n$f''(-1) = -12 < 0$", xy=(-1, 10),
            xytext=(-2.45, 22), fontsize=10.5, color=GOLD, bbox=BOX,
            arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.4))
ax.annotate("min $(3, -22)$\n$f''(3) = 12 > 0$", xy=(3, -22),
            xytext=(0.9, -34), fontsize=10.5, color=GOLD, bbox=BOX,
            arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.4))
ax.axvline(1, color=GREY, lw=1.2, ls="--", alpha=0.8)
ax.text(1.08, 30, "$f'' = 0$\nhere", fontsize=10, color=GREY, va="top")
ax.set_xlim(-2.6, 4.6)
ax.set_ylim(-38, 36)
ax.set_xlabel("$x$")
ax.legend(fontsize=9.5, frameon=False, loc="lower left")
ax.set_title("(a)  the sign of $f''$ at a stationary point",
             fontsize=12, color=INK, pad=10)
tidy(ax)

# (b) 山と谷の形
ax = axs[1]
XL = np.linspace(-2.9, -0.1, 300)
XR = np.linspace(0.1, 2.9, 300)
ax.plot(XL, -(XL + 1.5) ** 2 + 2.2, color=LINE, lw=3.0)
ax.plot(XR, (XR - 1.5) ** 2 - 2.2, color=LINE, lw=3.0)
ax.plot([-1.5], [2.2], "o", color=GOLD, ms=9, zorder=6)
ax.plot([1.5], [-2.2], "o", color=GOLD, ms=9, zorder=6)
ax.plot([-2.6, -0.4], [2.2, 2.2], color=ACC, lw=2.0, ls="--")
ax.plot([0.4, 2.6], [-2.2, -2.2], color=ACC, lw=2.0, ls="--")
ax.text(-1.5, 3.15, "maximum", fontsize=12.5, ha="center", color=INK,
        weight="bold")
ax.text(-1.5, -0.05, "bends DOWN\n$f'' < 0$\nconcave-down", fontsize=11,
        ha="center", va="top", color=ACC)
ax.text(1.5, -3.15, "minimum", fontsize=12.5, ha="center", va="top",
        color=INK, weight="bold")
ax.text(1.5, 0.05, "bends UP\n$f'' > 0$\nconcave-up", fontsize=11,
        ha="center", va="bottom", color=GREEN)
ax.text(0, 4.35, "at both points the tangent is flat:  $f' = 0$",
        fontsize=11, ha="center", color=GREY)
ax.set_xlim(-3.1, 3.1)
ax.set_ylim(-4.5, 4.9)
ax.axis("off")
ax.set_title("(b)  what the sign of $f''$ means", fontsize=12, color=INK,
             pad=10)

fig.tight_layout()
save(fig, "ahl-5-10-test.svg")


# ══════════ 5.10-2  f' と f'' の 4 つの組み合わせ ══════════
fig, axs = plt.subplots(2, 2, figsize=(11.0, 7.4))

panels = [
    (axs[0, 0], lambda u: np.exp(0.95 * u), (0.0, 2.0),
     "$f' > 0$  and  $f'' > 0$   (concave-up)",
     "going up, and getting STEEPER", GREEN),
    (axs[0, 1], lambda u: 2.6 * np.log(u + 1.0), (0.0, 2.0),
     "$f' > 0$  and  $f'' < 0$   (concave-down)",
     "going up, but FLATTENING OUT", ACC),
    (axs[1, 0], lambda u: 3.9 - 0.9 * u ** 2, (0.3, 2.0),
     "$f' < 0$  and  $f'' < 0$   (concave-down)",
     "going down, and getting STEEPER", ACC),
    (axs[1, 1], lambda u: 3.4 * np.exp(-1.1 * u), (0.0, 2.0),
     "$f' < 0$  and  $f'' > 0$   (concave-up)",
     "going down, but FLATTENING OUT", GREEN),
]
for ax, fn, (a, b), title, reading, col in panels:
    U = np.linspace(a, b, 400)
    ax.plot(U, fn(U), color=LINE, lw=3.2)
    ax.plot([a], [fn(np.array([a]))[0]], "o", color=GOLD, ms=7, zorder=6)
    ax.plot([b], [fn(np.array([b]))[0]], "o", color=GOLD, ms=7, zorder=6)
    ax.set_xlim(-0.15, 2.15)
    ax.set_ylim(-0.4, 7.0)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=12, color=INK, pad=8)
    ax.text(1.0, -0.05, reading, fontsize=11.5, ha="center", va="top",
            color=col)
    ax.grid(True, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("bottom", "left"):
        ax.spines[sp].set_color(GREY)

fig.suptitle("$f'$ says which way it is going.  $f''$ says whether that "
             "is speeding up or slowing down.", fontsize=13, y=1.0)
fig.tight_layout(rect=(0, 0, 1, 0.965))
save(fig, "ahl-5-10-four.svg")

print("figures written to", os.path.normpath(OUT))
