"""AHL 4.12 の図を作る。ラベルはすべて英語（日本語グリフは matplotlib に無い）。
   出力先: ai-hl/04-statistics-and-probability/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_4_12.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
from _graph import INK, GRID, LINE, ACC, GREEN, GREY, GOLD, BOX

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "04-statistics-and-probability", "img")
os.makedirs(OUT, exist_ok=True)
PALE = "#dfe3e8"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True)
    plt.close(fig)
    print("wrote", name)


# ══════════════ 1. 質問のしかた（悪い例 → 直した例） ══════════════
PAIRS = [
    ("leading", "Don't you agree that\nthe new bus route is good?",
     "How would you rate\nthe new bus route?"),
    ("unstructured", "What do you think\nof the canteen?",
     "Rate the canteen:\nvery poor / poor / fair /\ngood / very good"),
    ("imprecise", "Do you exercise often?",
     "How many days last week\ndid you exercise for\n30 minutes or more?"),
]
fig, axs = plt.subplots(1, 3, figsize=(13.6, 4.4))
for ax, (label, bad, good) in zip(axs, PAIRS):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title(label, fontsize=12.5, color=ACC, pad=8)
    ax.add_patch(FancyBboxPatch((0.4, 6.0), 9.2, 3.2,
                                boxstyle="round,pad=0.0,rounding_size=0.30",
                                fc="#fdecea", ec=ACC, lw=1.8))
    ax.text(5.0, 7.6, bad, fontsize=11.5, ha="center", va="center",
            color=INK)
    ax.text(0.9, 8.85, "✗", fontsize=14, ha="center", va="center", color=ACC,
            weight="bold")
    ax.annotate("", xy=(5.0, 4.7), xytext=(5.0, 5.8),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=GREY))
    ax.add_patch(FancyBboxPatch((0.4, 0.9), 9.2, 3.6,
                                boxstyle="round,pad=0.0,rounding_size=0.30",
                                fc="#eaf6ef", ec=GREEN, lw=1.8))
    ax.text(5.0, 2.7, good, fontsize=11.5, ha="center", va="center",
            color=INK)
    ax.text(0.9, 4.1, "✓", fontsize=14, ha="center", va="center",
            color=GREEN, weight="bold")
fig.tight_layout()
save(fig, "ahl-4-12-questions.svg")

# ══════════════ 2. reliability と validity ══════════════
SHOTS = {
    "not reliable, not valid": [(-0.9, 0.7), (0.8, -0.5), (-0.2, -1.1),
                                (1.1, 0.9), (0.1, 0.4)],
    "reliable, not valid": [(1.05, 0.85), (1.2, 0.7), (0.95, 0.72),
                            (1.15, 0.95), (1.0, 0.68)],
    "valid, not reliable": [(-0.75, 0.15), (0.7, -0.2), (0.05, 0.8),
                                   (-0.1, -0.75), (0.15, 0.1)],
    "reliable and valid": [(0.14, 0.20), (-0.20, 0.10), (0.05, -0.24),
                           (0.26, -0.08), (-0.10, -0.15)],
}
fig, axs = plt.subplots(1, 4, figsize=(15.2, 4.2))
for ax, (title, pts) in zip(axs, SHOTS.items()):
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_aspect("equal")
    ax.axis("off")
    for r, c in ((1.4, PALE), (0.95, "#eef2f6"), (0.5, "#e2eaf2")):
        ax.add_patch(Circle((0, 0), r, fc=c, ec=GREY, lw=1.0, zorder=1))
    ax.add_patch(Circle((0, 0), 0.22, fc="none", ec=ACC, lw=2.0, zorder=2))
    ax.plot([0], [0], "+", ms=11, mew=2.0, color=ACC, zorder=3)
    col = GREEN if "and valid" in title else LINE
    for x, y in pts:
        ax.plot([x], [y], "o", ms=8, mfc=col, mec="white", mew=1.2, zorder=5)
    ax.set_title(title, fontsize=11.5, color=col, pad=8)
fig.text(0.5, 0.015, "the bullseye is the true value: "
                     "reliable = the shots agree with each other,   "
                     "valid = they are aimed at the right target",
         fontsize=11.5, ha="center", color=INK)
fig.tight_layout(rect=(0, 0.06, 1, 1))
save(fig, "ahl-4-12-target.svg")

# ══════════════ 3. 期待度数が 5 未満のクラスをまとめる ══════════════
LAB8 = ["under\n12", "12–16", "16–20", "20–24", "24–28", "28–32", "32–36",
        "36 and\nover"]
E8 = [3.41, 10.27, 24.19, 37.13, 37.13, 24.19, 10.27, 3.41]
LAB6 = ["under 16", "16–20", "20–24", "24–28", "28–32", "32 and over"]
E6 = [13.68, 24.19, 37.13, 37.13, 24.19, 13.68]

fig, axs = plt.subplots(1, 2, figsize=(14.4, 4.2),
                        gridspec_kw={"width_ratios": [1.2, 1.0]})
for ax, LAB, E, title, col in (
        (axs[0], LAB8, E8, "8 classes: two are below 5", ACC),
        (axs[1], LAB6, E6, "combine the tails: 6 classes, all above 5",
         GREEN)):
    xs = np.arange(len(E))
    cols = [ACC if e < 5 else LINE for e in E]
    ax.bar(xs, E, color=cols, width=0.66, zorder=3)
    ax.axhline(5, color=GOLD, lw=1.8, ls="--", zorder=4)
    ax.text(-0.45, 41.5, "the dashed line is expected frequency $=5$",
            fontsize=10.5, ha="left", va="center", color=GOLD)
    for x, e in zip(xs, E):
        ax.text(x, (7.0 if e < 5 else e + 1.1), f"{e:.2f}", fontsize=10,
                ha="center", va="bottom", color=(ACC if e < 5 else INK))
    ax.set_xticks(xs)
    ax.set_xticklabels(LAB, fontsize=10)
    ax.set_ylim(0, 45)
    ax.set_ylabel("expected frequency", fontsize=11)
    ax.set_title(title, fontsize=12.5, color=col, pad=8)
    ax.grid(True, axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
fig.tight_layout()
save(fig, "ahl-4-12-combine.svg")

# ══════════════ 4. 自由度の数え方 ══════════════
fig, ax = plt.subplots(figsize=(12.4, 2.9))
ax.set_xlim(0, 13.4)
ax.set_ylim(-1.15, 3.5)
ax.axis("off")
BOXES = [
    (0.3, 3.1, LINE, "classes\nAFTER combining", "$6$"),
    (4.3, 2.0, GREY, "always\nsubtract $1$", "$1$"),
    (7.6, 3.6, ACC, "parameters estimated\nfrom the data", "$2$"),
]
for x, w, col, label, val in BOXES:
    ax.add_patch(FancyBboxPatch((x, 0.9), w, 1.5,
                                boxstyle="round,pad=0.0,rounding_size=0.25",
                                fc="none", ec=col, lw=2.0))
    ax.text(x + w / 2, 1.95, label, fontsize=11, ha="center", va="center",
            color=col)
    ax.text(x + w / 2, 1.30, val, fontsize=15, ha="center", va="center",
            color=col, weight="bold")
ax.text(3.85, 1.65, "$-$", fontsize=17, ha="center", va="center", color=INK)
ax.text(7.15, 1.65, "$-$", fontsize=17, ha="center", va="center", color=INK)
ax.text(11.6, 1.65, "$= 3$", fontsize=16, ha="left", va="center",
        color=GREEN, weight="bold")
ax.text(6.0, 2.95, "$\\nu = k - 1 - q$", fontsize=15, ha="center",
        va="center", color=INK)
ax.text(6.0, -0.35, "count the classes you actually test, "
                    "not the classes you started with",
        fontsize=11.5, ha="center", va="center", color=ACC)
fig.tight_layout()
save(fig, "ahl-4-12-df.svg")
