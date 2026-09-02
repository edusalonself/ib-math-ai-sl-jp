"""AHL 1.9 の図を作る。ラベルはすべて英語（日本語グリフは matplotlib に無い）。
   出力先: ai-hl/01-number-and-algebra/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_1_9.py
"""
import os
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "01-number-and-algebra", "img")
os.makedirs(OUT, exist_ok=True)

INK, GRID, LINE, ACC = "#1f2328", "#dfe3e8", "#2874a6", "#c0392b"
GREEN, GREY, GOLD = "#1e8449", "#7a8592", "#b9770e"
FILL, PALE = "#eaf2fb", "#fdecea"
BOX = dict(facecolor="white", edgecolor="none", pad=2.0, alpha=0.95)

plt.rcParams.update({
    "font.size": 11, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "text.color": INK, "xtick.color": INK, "ytick.color": INK,
    "svg.fonttype": "path",
})


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), format="svg",
                bbox_inches="tight", transparent=True)
    plt.close(fig)
    print("wrote", name)


def blank(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")


# ══════════════ 1. 3 つの法則を並べる ══════════════
fig, axs = plt.subplots(1, 3, figsize=(12.6, 2.4))
CARDS = [
    ("multiply  $\\longrightarrow$  add",
     "$\\log_a xy = \\log_a x + \\log_a y$", GREEN),
    ("divide  $\\longrightarrow$  subtract",
     "$\\log_a \\dfrac{x}{y} = \\log_a x - \\log_a y$", LINE),
    ("power  $\\longrightarrow$  move to the front",
     "$\\log_a x^{m} = m \\log_a x$", ACC),
]
for ax, (title, formula, col) in zip(axs, CARDS):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.2)
    ax.axis("off")
    ax.add_patch(plt.Rectangle((0.3, 0.4), 9.4, 3.4, fc="white",
                               ec=col, lw=1.8, zorder=1))
    ax.text(5.0, 3.05, title, fontsize=12, ha="center", va="center",
            color=col, zorder=3)
    ax.text(5.0, 1.6, formula, fontsize=15, ha="center", va="center",
            color=INK, zorder=3)
fig.text(0.5, 0.015, "for  $a,\\ x,\\ y > 0$", fontsize=12,
         ha="center", color=GOLD)
fig.tight_layout(rect=(0, 0.05, 1, 1))
save(fig, "ahl-1-9-three-laws.svg")

# ══════════════ 2. なぜ「掛けたら足す」なのか ══════════════
fig, ax = plt.subplots(figsize=(9.0, 3.6))
blank(ax, (-0.4, 13.4), (-1.5, 3.2))

ax.text(0.2, 2.4, "$10^{\\,p} = x$", fontsize=14, ha="left", va="center",
        color=LINE)
ax.text(0.2, 1.4, "$10^{\\,q} = y$", fontsize=14, ha="left", va="center",
        color=LINE)
ax.annotate("", xy=(4.9, 1.9), xytext=(3.1, 1.9),
            arrowprops=dict(arrowstyle="-|>", lw=2.0, color=GREY))
ax.text(4.0, 2.25, "multiply", fontsize=11, ha="center", va="bottom",
        color=GREY)
ax.text(5.2, 1.9, "$xy = 10^{\\,p} \\times 10^{\\,q} = 10^{\\,p+q}$",
        fontsize=14, ha="left", va="center", color=INK)
ax.annotate("", xy=(6.6, 0.6), xytext=(6.6, 1.4),
            arrowprops=dict(arrowstyle="-|>", lw=2.0, color=GREY))
ax.text(6.85, 1.0, "read the exponent", fontsize=11, ha="left",
        va="center", color=GREY)
ax.text(6.6, 0.0, "$\\log xy = p + q = \\log x + \\log y$",
        fontsize=14, ha="center", va="center", color=GREEN)
ax.text(6.7, -1.1, "the exponent rule  $10^{\\,p} \\times 10^{\\,q} "
                   "= 10^{\\,p+q}$  is doing all the work",
        fontsize=11.5, ha="center", va="center", color=INK, bbox=BOX)
fig.tight_layout()
save(fig, "ahl-1-9-why.svg")

# ══════════════ 3. 指数から x を降ろす ══════════════
fig, ax = plt.subplots(figsize=(8.4, 4.0))
blank(ax, (-0.5, 11.5), (-2.4, 3.4))

STEPS = [
    ("$3(1.4)^{t} = 20$", 2.6, INK, "the unknown is stuck in the exponent"),
    ("$(1.4)^{t} = \\dfrac{20}{3}$", 1.4, INK, "divide by 3 first"),
    ("$\\log (1.4)^{t} = \\log \\dfrac{20}{3}$", 0.1, INK,
     "take $\\log$ of both sides"),
    ("$t \\log 1.4 = \\log \\dfrac{20}{3}$", -1.2, ACC,
     "the power law brings $t$ down"),
]
for text, y, col, note in STEPS:
    ax.text(0.2, y, text, fontsize=14, ha="left", va="center", color=col)
    ax.text(5.4, y, note, fontsize=11, ha="left", va="center", color=GREY)
ax.text(0.2, -2.1, "$t = \\dfrac{\\log (20/3)}{\\log 1.4} = 5.64$",
        fontsize=14, ha="left", va="center", color=GREEN)
fig.tight_layout()
save(fig, "ahl-1-9-solve.svg")

# ══════════════ 4. log は掛け算を足し算に変える（グラフ） ══════════════
fig, axs = plt.subplots(1, 2, figsize=(11.0, 4.0))

ax = axs[0]
xs = np.linspace(0.15, 12, 600)
ax.plot(xs, np.log10(xs), color=LINE, lw=2.2)
for v, lab, col in ((2, "$2$", GREY), (3, "$3$", GREY), (6, "$6$", ACC)):
    ax.plot([v, v], [0, math.log10(v)], ls="--", lw=1.1, color=col)
    ax.plot([0, v], [math.log10(v)] * 2, ls="--", lw=1.1, color=col)
    ax.plot([v], [math.log10(v)], "o", color=col, ms=5)
ax.text(2.15, 0.10, "$\\log 2 = 0.301$", fontsize=10.5, color=GREY)
ax.text(3.15, 0.36, "$\\log 3 = 0.477$", fontsize=10.5, color=GREY)
ax.text(6.15, 0.66, "$\\log 6 = 0.778$", fontsize=10.5, color=ACC)
ax.set_xlim(0, 12)
ax.set_ylim(-0.45, 1.15)
ax.set_xlabel("$x$")
ax.set_ylabel("$\\log_{10} x$")
ax.grid(True, color=GRID, lw=0.8)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_title("$y = \\log_{10} x$", fontsize=12, color=INK, pad=8)

ax = axs[1]
ax.axis("off")
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.text(5.0, 8.3, "$2 \\times 3 = 6$", fontsize=15, ha="center",
        color=INK)
ax.annotate("", xy=(5.0, 6.0), xytext=(5.0, 7.5),
            arrowprops=dict(arrowstyle="-|>", lw=2.0, color=GREY))
ax.text(5.35, 6.75, "take $\\log$", fontsize=11.5, ha="left",
        va="center", color=GREY)
ax.text(5.0, 5.2, "$0.301 + 0.477 = 0.778$", fontsize=15,
        ha="center", color=GREEN)
ax.text(5.0, 3.4, "multiplying the numbers\nadds the logarithms",
        fontsize=12.5, ha="center", va="center", color=INK)
ax.text(5.0, 1.5, "this is why $\\log$ turns\n$\\times$ into $+$",
        fontsize=12, ha="center", va="center", color=ACC)
fig.tight_layout()
save(fig, "ahl-1-9-graph.svg")

# ══════════════ 5. 成り立たない形 ══════════════
fig, ax = plt.subplots(figsize=(9.4, 3.4))
blank(ax, (-0.4, 13.0), (-2.6, 2.6))

BAD = [
    ("$\\log (x + y) \\neq \\log x + \\log y$", 1.7),
    ("$\\log (xy) \\neq \\log x \\times \\log y$", 0.5),
    ("$\\dfrac{\\log x}{\\log y} \\neq \\log x - \\log y$", -1.0),
]
for text, y in BAD:
    ax.text(0.3, y, text, fontsize=14, ha="left", va="center", color=ACC)
ax.text(7.4, 0.4, "the laws work on\n$\\times$, $\\div$ and powers\n"
                  "$-$ never on $+$ or $-$",
        fontsize=12, ha="center", va="center", color=INK, bbox=BOX)
ax.text(6.5, -2.2, "check with numbers: $\\log(3+4) = 0.845$,"
                   "  but  $\\log 3 + \\log 4 = 1.079$",
        fontsize=11.5, ha="center", va="center", color=GOLD)
fig.tight_layout()
save(fig, "ahl-1-9-not-laws.svg")
