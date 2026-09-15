"""AHL 5.11a / 5.11b（further integration）の図を作る。ラベルは英語。
   出力先: ai-hl/05-calculus/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_5_11.py
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


# ══════════ 5.11a-1  1/x と ln|x|（modulus の理由）══════════
#  本文の「modulus が付く理由」の節に置く図。
fig, ax = plt.subplots(figsize=(6.3, 4.9))
XR = np.linspace(0.16, 4.0, 500)
XL = np.linspace(-4.0, -0.16, 500)
ax.plot(XR, 1 / XR, color=ACC, lw=2.4, ls="--",
        label="$f'(x) = \\dfrac{1}{x}$")
ax.plot(XL, 1 / XL, color=ACC, lw=2.4, ls="--")
ax.plot(XR, np.log(np.abs(XR)), color=LINE, lw=2.8,
        label="$f(x) = \\ln|x|$")
ax.plot(XL, np.log(np.abs(XL)), color=LINE, lw=2.8)
ax.axhline(0, color=GREY, lw=1.0, alpha=0.7)
ax.axvline(0, color=GREY, lw=1.0, alpha=0.7)
ax.plot([1], [0], "o", color=LINE, ms=7, zorder=6)
ax.plot([-1], [0], "o", color=LINE, ms=7, zorder=6)
ax.text(-3.9, 2.35, "the modulus lets the same\nantiderivative work on\n"
        "BOTH sides of $0$", fontsize=10.5, color=GOLD, va="top", bbox=BOX)
ax.set_xlim(-4.0, 4.0)
ax.set_ylim(-3.4, 3.4)
ax.set_xlabel("$x$")
ax.legend(fontsize=11, frameon=False, loc="lower right")
ax.set_title("why $\\int \\frac{1}{x}\\,dx = \\ln|x| + C$",
             fontsize=12, color=INK, pad=10)
tidy(ax)

fig.tight_layout()
save(fig, "ahl-5-11a-lnabs.svg")


# ══════════ 5.11a-2  定積分＝面積 ══════════
#  本文の「定積分」の節に置く図。
fig, ax = plt.subplots(figsize=(6.3, 4.5))
X = np.linspace(0.35, 4.2, 500)
ax.plot(X, 1 / X, color=LINE, lw=2.8, label="$y = \\dfrac{1}{x}$")
XS = np.linspace(1, 3, 300)
ax.fill_between(XS, 0, 1 / XS, color=FILL, edgecolor=LINE, lw=1.2, zorder=2)
ax.axhline(0, color=GREY, lw=1.0, alpha=0.7)
ax.text(1.95, 0.36, "area $= \\ln 3 = 1.10$", fontsize=12,
        ha="center", va="center", color=INK, zorder=5, bbox=BOX)
ax.annotate("", xy=(1, -0.16), xytext=(3, -0.16),
            arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.4))
ax.text(2, -0.30, "from $x = 1$ to $x = 3$", fontsize=10.5, ha="center",
        color=GREY)
ax.set_xlim(0, 4.2)
ax.set_ylim(-0.42, 2.6)
ax.set_xticks([0, 1, 2, 3, 4])
ax.set_xlabel("$x$")
ax.legend(fontsize=11, frameon=False, loc="upper right")
ax.set_title("$\\int_{1}^{3}\\frac{1}{x}\\,dx = "
             "[\\ln|x|]_{1}^{3} = \\ln 3$", fontsize=12, color=INK, pad=10)
tidy(ax)

fig.tight_layout()
save(fig, "ahl-5-11a-area.svg")


# ══════════ 5.11b-1  inspection の流れ図 ══════════
#  本文の「chain rule を逆から読みます」の節に置く図。
fig, ax = plt.subplots(figsize=(6.2, 4.4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 7.4)
ax.axis("off")
rows = [
    (5.85, "guess:  $-\\cos(2x+5)$", FILL, LINE),
    (3.75, "differentiate it:  $2\\sin(2x+5)$", "#fdecea", ACC),
    (1.65, "answer:  $-\\dfrac{1}{2}\\cos(2x+5) + C$", "#eafaf1", GREEN),
]
for cy, txt, fc, ec in rows:
    ax.add_patch(plt.Rectangle((0.6, cy - 0.72), 8.8, 1.44, fc=fc, ec=ec,
                               lw=2.0, zorder=2))
    ax.text(5.0, cy, txt, fontsize=13, ha="center", va="center", color=INK,
            zorder=3)
ax.annotate("", xy=(5.0, 4.55), xytext=(5.0, 5.1),
            arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.8,
                            mutation_scale=17))
ax.annotate("", xy=(5.0, 2.45), xytext=(5.0, 3.0),
            arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.8,
                            mutation_scale=17))
ax.text(5.15, 4.83, "  $2$ times too big", fontsize=11, color=ACC,
        va="center", ha="left")
ax.text(5.15, 2.73, "  so divide by $2$", fontsize=11, color=GREEN,
        va="center", ha="left")
ax.text(5.0, 7.0, "to integrate $\\sin(2x+5)$", fontsize=12.5, ha="center",
        color=GREY)
ax.set_title("inspection:  guess, differentiate, fix the constant",
             fontsize=12, color=INK, pad=10)

fig.tight_layout()
save(fig, "ahl-5-11b-inspect.svg")


# ══════════ 5.11b-2  置換で面積は変わらない ══════════
#  本文の「定積分では端も u に直します」の節に置く図。
fig, ax = plt.subplots(figsize=(6.4, 4.9))
X = np.linspace(0, 1, 400)
ax.plot(X, 2 * X * np.exp(X ** 2), color=LINE, lw=2.8,
        label="$y = 2x\\,e^{x^{2}}$   (in $x$)")
ax.fill_between(X, 0, 2 * X * np.exp(X ** 2), color=FILL, edgecolor="none",
                zorder=2, alpha=0.95)
U = np.linspace(0, 1, 400)
ax.plot(U, np.exp(U), color=GREEN, lw=2.8, ls="--",
        label="$y = e^{u}$   (in $u$)")
ax.fill_between(U, 0, np.exp(U), facecolor="none", edgecolor=GREEN,
                hatch="///", lw=0.0, zorder=3)
ax.axhline(0, color=GREY, lw=1.0, alpha=0.7)
ax.text(0.52, 4.35, "different shapes,\nbut both areas $= e - 1 = 1.72$",
        fontsize=12, ha="center", color=INK, bbox=BOX)
ax.text(0.03, 3.05, "$u = x^{2}$ turns one into the other,\n"
        "and the limits $0 \\to 1$ stay $0 \\to 1$", fontsize=10.5,
        ha="left", va="top", color=GREY, bbox=BOX)
ax.set_xlim(0, 1.05)
ax.set_ylim(-0.12, 6.6)
ax.set_xlabel("$x$   or   $u$")
ax.legend(fontsize=10.5, frameon=False, loc="upper left")
ax.set_title("substitution: the area does not change",
             fontsize=12, color=INK, pad=10)
tidy(ax)

fig.tight_layout()
save(fig, "ahl-5-11b-sub.svg")

print("figures written to", os.path.normpath(OUT))
