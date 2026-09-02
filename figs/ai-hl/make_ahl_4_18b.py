"""AHL 4.18b の図を作る。ラベルはすべて英語（日本語グリフは matplotlib に無い）。
   ★ matplotlib は markdown を解釈しないので、コマンド名にバッククォートは付けない。
   出力先: ai-hl/04-statistics-and-probability/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_4_18b.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from _graph import INK, LINE, ACC, GREEN, GREY, GOLD

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "04-statistics-and-probability", "img")
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True)
    plt.close(fig)
    print("wrote", name)


def box(ax, x, y, w, h, text, edge, fs=11.0, weight="normal", tcol=None):
    ax.add_patch(FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.10,rounding_size=0.14",
        linewidth=1.8, edgecolor=edge, facecolor="white", zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs,
            color=(tcol or INK), zorder=4, weight=weight, linespacing=1.6)


def arrow(ax, x1, y1, x2, y2, label=None, col=GREY, lx=None, ly=None,
          fs=10.0):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=14,
        linewidth=1.5, color=col, zorder=2, shrinkA=2, shrinkB=4))
    if label:
        ax.text(lx if lx is not None else (x1 + x2) / 2,
                ly if ly is not None else (y1 + y2) / 2,
                label, ha="center", va="center", fontsize=fs, color=col,
                zorder=5,
                bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none"))


fig, ax = plt.subplots(figsize=(12.6, 9.0))
ax.set_xlim(-0.25, 13.5)
ax.set_ylim(0, 10.4)
ax.axis("off")

# ── 出発点 ─────────────────────────────────────────────
box(ax, 6.7, 9.75, 7.2, 0.74,
    "What does $H_0$ say something about?", INK, fs=13.0, weight="bold")

# ── 4 つの枝 ───────────────────────────────────────────
Y1 = 8.15
BR = [(2.10, 3.6, "a population MEAN  $\\mu$", LINE),
      (5.95, 3.1, "a PROPORTION  $p$", GREEN),
      (9.10, 2.9, "a Poisson MEAN  $m$", GOLD),
      (12.00, 2.5, "a CORRELATION  $\\rho$", ACC)]
for x, w, txt, col in BR:
    box(ax, x, Y1, w, 0.70, txt, col, fs=11.5)
    arrow(ax, 6.7, 9.38, x, Y1 + 0.40, col=col)

# ── 平均の枝：σ で分かれる ─────────────────────────────
box(ax, 2.10, 6.55, 3.6, 0.70, "Is $\\sigma$ GIVEN in the question?", LINE,
    fs=11.0)
arrow(ax, 2.10, Y1 - 0.40, 2.10, 6.94, col=LINE)

box(ax, 1.00, 4.75, 1.70, 1.25, "z Test\n(normal)", LINE, fs=12.0,
    weight="bold", tcol=LINE)
box(ax, 3.20, 4.75, 1.90, 1.25, "t Test\n($t$-distribution)", LINE, fs=11.5,
    weight="bold", tcol=LINE)
arrow(ax, 1.70, 6.16, 1.00, 5.41, "yes", col=LINE, lx=0.82, ly=5.86)
arrow(ax, 2.50, 6.16, 3.20, 5.41, "no", col=LINE, lx=3.32, ly=5.86)

box(ax, 2.10, 2.85, 4.0, 0.92,
    "$\\sigma$ unknown $\\Rightarrow$ always $t$,\n"
    "REGARDLESS OF SAMPLE SIZE", GREY, fs=10.2, tcol=GREY)
arrow(ax, 3.20, 4.10, 2.55, 3.34, col=GREY)

# ── 割合・Poisson の枝 ─────────────────────────────────
box(ax, 6.05, 5.20, 2.9, 1.45, "Binomial Cdf\nby hand\n(ONE-TAILED only)",
    GREEN, fs=11.5, weight="bold", tcol=GREEN)
arrow(ax, 5.95, Y1 - 0.40, 6.05, 5.96, col=GREEN)

box(ax, 9.10, 5.20, 2.9, 1.45, "Poisson Cdf\nby hand\n(ONE-TAILED only)",
    GOLD, fs=11.5, weight="bold", tcol=GOLD)
arrow(ax, 9.10, Y1 - 0.40, 9.10, 5.96, col=GOLD)

box(ax, 7.55, 2.85, 5.6, 0.92,
    "these two are NOT in the Stat Tests menu —\n"
    "you build the $p$-value yourself", GREY, fs=10.2, tcol=GREY)
arrow(ax, 6.05, 4.45, 6.60, 3.34, col=GREY)
arrow(ax, 9.10, 4.45, 8.50, 3.34, col=GREY)

# ── 相関の枝 ───────────────────────────────────────────
box(ax, 12.00, 5.20, 2.5, 1.45, "Linear Reg\nt Test\n($H_0$: $\\rho = 0$)",
    ACC, fs=11.5, weight="bold", tcol=ACC)
arrow(ax, 12.00, Y1 - 0.40, 12.00, 5.96, col=ACC)

box(ax, 12.00, 2.85, 2.5, 0.92,
    "the data will be\nGIVEN in the question", GREY, fs=10.2, tcol=GREY)
arrow(ax, 12.00, 4.45, 12.00, 3.34, col=GREY)

# ── paired の注（いちばん下） ──────────────────────────
box(ax, 6.7, 0.95, 10.4, 0.92,
    "PAIRED data (before and after, on the same subjects):  "
    "take the DIFFERENCES first,\n"
    "then treat them as ONE sample and use the t Test",
    INK, fs=11.0)
arrow(ax, 2.10, 2.36, 3.60, 1.45, col=GREY)

fig.tight_layout()
save(fig, "ahl-4-18b-choose.svg")

print("figures written to", os.path.normpath(OUT))
