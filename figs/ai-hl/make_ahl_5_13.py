"""AHL 5.13（kinematics）の図を作る。ラベルは英語。
   出力先: ai-hl/05-calculus/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_5_13.py
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


def tidy(ax):
    ax.grid(True, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("bottom", "left"):
        ax.spines[sp].set_color(GREY)


# 走らせる例：v = t^2 - 4t + 3、s(0) = 0
def vf(t):
    return t ** 2 - 4 * t + 3


def sf(t):
    return t ** 3 / 3 - 2 * t ** 2 + 3 * t


def af(t):
    return 2 * t - 4


T = np.linspace(0, 4, 800)

# ══════════════ 1. s, v, a はつながっている ══════════════
fig, axs = plt.subplots(2, 2, figsize=(11.4, 8.4))

ax = axs[0, 0]
ax.plot(T, sf(T), color=LINE, lw=2.6)
for tv, c in ((1.0, ACC), (3.0, ACC)):
    ax.plot([tv], [sf(tv)], "o", color=c, ms=7, zorder=6)
ax.axhline(0, color=GREY, lw=1.0, alpha=0.7)
ax.set_xlim(0, 4)
ax.set_ylim(-0.3, 1.9)
ax.set_xlabel("$t$")
ax.set_ylabel("$s$")
ax.set_title("(a)  displacement $s = \\dfrac{t^{3}}{3} - 2t^{2} + 3t$",
             fontsize=12.5, color=LINE, pad=10)
ax.text(2.0, 1.62, "flat where $v = 0$", fontsize=11, ha="center",
        color=ACC, bbox=BOX)
tidy(ax)

ax = axs[0, 1]
ax.plot(T, vf(T), color=GREEN, lw=2.6)
ax.axhline(0, color=GREY, lw=1.0, alpha=0.7)
for tv in (1.0, 3.0):
    ax.plot([tv], [0], "o", color=ACC, ms=7, zorder=6)
ax.plot([2.0], [vf(2.0)], "o", color=GOLD, ms=7, zorder=6)
ax.set_xlim(0, 4)
ax.set_ylim(-1.6, 3.4)
ax.set_xlabel("$t$")
ax.set_ylabel("$v$")
ax.set_title("(b)  velocity $v = \\dfrac{ds}{dt} = t^{2} - 4t + 3$",
             fontsize=12.5, color=GREEN, pad=10)
ax.text(2.0, 2.75, "$v = 0$ at $t = 1$ and $t = 3$", fontsize=11,
        ha="center", color=ACC, bbox=BOX)
ax.text(2.0, -1.42, "lowest $v$ where $a = 0$", fontsize=11, ha="center",
        color=GOLD, bbox=BOX)
tidy(ax)

ax = axs[1, 0]
ax.plot(T, af(T), color=GOLD, lw=2.6)
ax.axhline(0, color=GREY, lw=1.0, alpha=0.7)
ax.plot([2.0], [0], "o", color=GOLD, ms=7, zorder=6)
ax.set_xlim(0, 4)
ax.set_ylim(-4.6, 4.6)
ax.set_xlabel("$t$")
ax.set_ylabel("$a$")
ax.set_title("(c)  acceleration $a = \\dfrac{dv}{dt} = 2t - 4$",
             fontsize=12.5, color=GOLD, pad=10)
ax.text(2.05, 3.4, "$a = 0$ at $t = 2$", fontsize=11, ha="center",
        color=GOLD, bbox=BOX)
tidy(ax)

# (d) 実際にどこにいるか
ax = axs[1, 1]
ax.set_xlim(-0.35, 1.75)
ax.set_ylim(-1.05, 1.55)
ax.axis("off")
ax.annotate("", xy=(1.72, 0), xytext=(-0.32, 0),
            arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.6))
ax.text(1.72, -0.16, "$s$", fontsize=12, color=GREY, ha="right", va="top")
for pos, lab in ((0.0, "$0$"), (4 / 3, "$\\dfrac{4}{3}$")):
    ax.plot([pos], [0], "|", color=GREY, ms=14, mew=2)
    ax.text(pos, -0.20, lab, fontsize=11.5, ha="center", va="top", color=GREY)
LEGS = [(0.0, 4 / 3, 0.30, GREEN, "$t: 0 \\to 1$", "forwards"),
        (4 / 3, 0.0, 0.72, ACC, "$t: 1 \\to 3$", "backwards"),
        (0.0, 4 / 3, 1.14, GREEN, "$t: 3 \\to 4$", "forwards")]
for x0, x1, y, col, lab, note in LEGS:
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=2.6))
    ax.text((x0 + x1) / 2, y + 0.11, "%s  %s" % (lab, note), fontsize=11,
            ha="center", va="bottom", color=col)
ax.text(0.7, -0.78,
        "moved $\\dfrac{4}{3} + \\dfrac{4}{3} + \\dfrac{4}{3} = 4$,   "
        "but ended only $\\dfrac{4}{3}$ from the start",
        fontsize=11.5, ha="center", va="center", color=INK, bbox=BOX)
ax.set_title("(d)  where the particle actually is",
             fontsize=12.5, color=INK, pad=10)

fig.suptitle("One motion, three graphs: differentiate to go down, "
             "integrate to go back up", fontsize=14, y=0.995)
fig.tight_layout(rect=(0, 0, 1, 0.97))
save(fig, "ahl-5-13-links.svg")


# ══════════════ 2. displacement と total distance ══════════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.4))
PARTS = [(0.0, 1.0, GREEN, "$+\\dfrac{4}{3}$"),
         (1.0, 3.0, ACC, "$-\\dfrac{4}{3}$"),
         (3.0, 4.0, GREEN, "$+\\dfrac{4}{3}$")]

ax = axs[0]
ax.plot(T, vf(T), color=INK, lw=2.4)
for x0, x1, col, lab in PARTS:
    xs = np.linspace(x0, x1, 300)
    ax.fill_between(xs, vf(xs), color=col, alpha=0.28)
    ax.text((x0 + x1) / 2, vf((x0 + x1) / 2) / 2, lab, fontsize=12,
            ha="center", va="center", color=col)
ax.axhline(0, color=GREY, lw=1.2)
ax.set_xlim(0, 4)
ax.set_ylim(-1.7, 3.4)
ax.set_xlabel("$t$")
ax.set_ylabel("$v$")
ax.set_title("displacement $= \\int_{0}^{4} v \\, dt = \\dfrac{4}{3}$",
             fontsize=12.5, color=INK, pad=10)
ax.text(2.0, 2.8, "areas below the axis count as NEGATIVE",
        fontsize=11, ha="center", color=ACC, bbox=BOX)
tidy(ax)

ax = axs[1]
ax.plot(T, np.abs(vf(T)), color=INK, lw=2.4)
for x0, x1, col, lab in PARTS:
    xs = np.linspace(x0, x1, 300)
    ax.fill_between(xs, np.abs(vf(xs)), color=GREEN, alpha=0.28)
    ax.text((x0 + x1) / 2, abs(vf((x0 + x1) / 2)) / 2,
            lab.replace("-", "+"), fontsize=12, ha="center", va="center",
            color=GREEN)
ax.axhline(0, color=GREY, lw=1.2)
ax.set_xlim(0, 4)
ax.set_ylim(-1.7, 3.4)
ax.set_xlabel("$t$")
ax.set_ylabel("$|v|$")
ax.set_title("total distance $= \\int_{0}^{4} |v| \\, dt = 4$",
             fontsize=12.5, color=INK, pad=10)
ax.text(2.0, 2.8, "taking $|v|$ folds them all ABOVE the axis",
        fontsize=11, ha="center", color=GREEN, bbox=BOX)
tidy(ax)

fig.text(0.5, -0.05,
         "Same $v = t^{2} - 4t + 3$ in both pictures.   The only difference is "
         "the modulus sign, and it changes $\\dfrac{4}{3}$ into $4$.",
         fontsize=12.5, ha="center", color=INK)
fig.tight_layout()
save(fig, "ahl-5-13-area.svg")

print("figures written to", os.path.normpath(OUT))
