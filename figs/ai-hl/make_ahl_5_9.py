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


# 2026-09: 5.9a の図 2 枚（導関数のグラフ／radian の比較）は本文から削除
#          したため、生成もやめました。

# 2026-09: 5.9b の chain rule の図は本文から削除したため、生成もやめました。

# ══════════ 5.9b-2  product rule の面積の絵 ══════════
fig, ax = plt.subplots(figsize=(6.0, 4.9))
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
ax.set_title("the extra area is $v\\,\\delta u + u\\,\\delta v$",
             fontsize=12, color=INK, pad=10)

fig.tight_layout()
save(fig, "ahl-5-9b-product.svg")


# ══════════ 5.9c  related rates ══════════
# 2026-09: (a) の 3 つの箱の図は本文から削除。(b) の r-t グラフだけ残す。
fig, ax = plt.subplots(figsize=(6.4, 4.6))
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
ax.set_title("air goes in at a steady rate,\nbut $r$ grows more and "
             "more slowly", fontsize=12, color=INK, pad=10)
tidy(ax)

fig.tight_layout()
save(fig, "ahl-5-9c-rates.svg")

print("figures written to", os.path.normpath(OUT))
