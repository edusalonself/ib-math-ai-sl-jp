"""AHL 2.9a（半減期・自然対数モデル・正弦モデル）の図を作る。ラベルは英語。
   出力先: ai-hl/02-functions/img/*.svg
   再生成: python3 figs/ai-hl/make_ahl_2_9a.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from _graph import INK, GRID, LINE, ACC, GREEN, GREY, GOLD, BOX

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-hl",
                   "02-functions", "img")
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


# ══════════ fig 1: 半減期 と 自然対数モデル ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.9))

# ── (a) 半減期は毎回おなじ長さ
ax = axs[0]
T = np.log(2) / 0.12                       # 5.7762...
X = np.linspace(0, 24, 600)
ax.plot(X, 500 * np.exp(-0.12 * X), color=LINE, lw=2.8,
        label="$M = 500e^{-0.12t}$")
for i in range(4):
    ti = i * T
    mi = 500 / 2 ** i
    ax.plot([ti, ti], [0, mi], color=GREY, lw=1.1, ls=":", zorder=3)
    ax.plot([0, ti], [mi, mi], color=GREY, lw=1.1, ls=":", zorder=3)
    ax.plot([ti], [mi], "o", color=ACC, ms=8, zorder=6)
for i in range(3):
    ax.annotate("", xy=((i + 1) * T, 40), xytext=(i * T, 40),
                arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.6))
ax.text(1.5 * T, 74, "the same $5.78$ years each time",
        fontsize=11, color=GREEN, ha="center", va="bottom", bbox=BOX, zorder=8)
for i, lab in enumerate(["$500$", "$250$", "$125$", "$62.5$"]):
    ax.text(-0.7, 500 / 2 ** i, lab, fontsize=10.5, color=ACC, ha="right",
            va="center")
ax.axhline(0, color=GREY, lw=1.2)
ax.set_xlim(-4.2, 24.5)
ax.set_ylim(-30, 560)
ax.set_xlabel("$t$ (years)")
ax.set_xticks([0, T, 2 * T, 3 * T])
ax.set_xticklabels(["$0$", "$5.78$", "$11.6$", "$17.3$"])
ax.legend(fontsize=11, frameon=False, loc="upper right")
ax.set_title("(a)  half-life: equal steps, equal halving", fontsize=12,
             color=INK, pad=9)
tidy(ax)

# ── (b) 自然対数モデル
ax = axs[1]
XL = np.linspace(0.06, 22, 900)
bb = 6 / np.log(4)
aa = 7 - bb * np.log(2)
ax.plot(XL, aa + bb * np.log(XL), color=LINE, lw=2.8,
        label="$f(x) = 4 + 4.33\\ln x$")
ax.plot([2, 8], [7, 13], "o", color=ACC, ms=8, zorder=6)
ax.text(2.15, 6.4, "$(2,\\ 7)$", fontsize=11, color=ACC, ha="left", va="top")
ax.text(8.2, 12.4, "$(8,\\ 13)$", fontsize=11, color=ACC, ha="left", va="top")
ax.axvline(0, color=GOLD, lw=2.4, zorder=4)
ax.text(0.4, -7.0, "$x = 0$ is a vertical asymptote:\nthe model needs $x > 0$",
        fontsize=11, color=GOLD, ha="left", va="center", bbox=BOX, zorder=8)
ax.annotate("growth never stops,\nbut it keeps slowing",
            xy=(18, aa + bb * np.log(18)), xytext=(11.5, 6.5), fontsize=11,
            color=GREEN, ha="left", va="center", bbox=BOX, zorder=8,
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.4,
                            shrinkA=2, shrinkB=4))
ax.axhline(0, color=GREY, lw=1.2)
ax.set_xlim(-1.6, 22.5)
ax.set_ylim(-11, 20)
ax.set_xlabel("$x$")
ax.legend(fontsize=11, frameon=False, loc="upper left")
ax.set_title("(b)  a natural logarithmic model", fontsize=12, color=INK, pad=9)
tidy(ax)

fig.tight_layout(w_pad=2.4)
save(fig, "ahl-2-9a-decay.svg")


# ══════════ fig 2: 正弦モデルの 4 文字 と c の位置 ══════════
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.9))

# ── (a) a, b, c, d
ax = axs[0]
TT = np.linspace(-0.4, 24.4, 900)
ax.plot(TT, 8 * np.sin(np.pi / 6 * (TT - 2)) + 12, color=LINE, lw=2.8,
        label="$h = 8\\sin\\!\\left(\\frac{\\pi}{6}(t-2)\\right)+12$")
ax.plot([-0.6, 23.8], [12, 12], color=GOLD, lw=2.0, ls="--")
ax.text(24.2, 12, "$y = d = 12$", fontsize=11, color=GOLD, va="center",
        ha="left", bbox=BOX, zorder=8)
# amplitude
ax.annotate("", xy=(5, 20), xytext=(5, 12),
            arrowprops=dict(arrowstyle="<->", color=ACC, lw=1.6))
ax.text(5.35, 16, "$a = 8$", fontsize=11.5, color=ACC, ha="left", va="center",
        bbox=BOX, zorder=8)
# period
ax.annotate("", xy=(17, 22.4), xytext=(5, 22.4),
            arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.6))
ax.text(11, 22.9, "period $= \\dfrac{2\\pi}{b} = 12$", fontsize=11,
        color=GREEN, ha="center", va="bottom", bbox=BOX, zorder=8)
# phase shift
ax.annotate("", xy=(2, 12), xytext=(0, 12),
            arrowprops=dict(arrowstyle="->", color=INK, lw=1.8))
ax.plot([2], [12], "o", color=INK, ms=8, zorder=7)
ax.text(2.3, 9.2, "$c = 2$: the wave starts\nits rise $2$ later", fontsize=11,
        color=INK, ha="left", va="top", bbox=BOX, zorder=8)
ax.plot([5, 17], [20, 20], "o", color=GREEN, ms=7, zorder=7)
ax.set_xlim(-0.6, 28.0)
ax.set_ylim(1.0, 26.5)
ax.set_xlabel("$t$")
ax.set_xticks([0, 5, 11, 17, 23])
ax.legend(fontsize=10.5, frameon=False, loc="lower right")
ax.set_title("(a)  what $a$, $b$, $c$, $d$ do", fontsize=12, color=INK, pad=9)
tidy(ax)

# ── (b) b(t-c) と bt-c は別もの
ax = axs[1]
T2 = np.linspace(-0.4, 14.4, 900)
ax.plot(T2, 8 * np.sin(np.pi / 6 * (T2 - 2)) + 12, color=LINE, lw=2.8,
        label="$8\\sin\\!\\left(\\frac{\\pi}{6}(t-2)\\right)+12$")
ax.plot(T2, 8 * np.sin(np.pi / 6 * T2 - 2) + 12, color=ACC, lw=2.8, ls="-.",
        label="$8\\sin\\!\\left(\\frac{\\pi}{6}t-2\\right)+12$")
ax.axhline(12, color=GOLD, lw=1.6, ls="--")
s2 = 2 / (np.pi / 6)
ax.plot([2, s2], [12, 12], "o", color=INK, ms=8, zorder=7)
ax.annotate("shift $2$", xy=(2, 12), xytext=(0.2, 17.6), fontsize=11,
            color=LINE, ha="left", va="center", bbox=BOX, zorder=8,
            arrowprops=dict(arrowstyle="->", color=LINE, lw=1.4,
                            shrinkA=2, shrinkB=5))
ax.annotate("shift $\\dfrac{2}{\\pi/6} = 3.82$", xy=(s2, 12),
            xytext=(5.4, 6.2), fontsize=11, color=ACC, ha="left", va="center",
            bbox=BOX, zorder=8,
            arrowprops=dict(arrowstyle="->", color=ACC, lw=1.4,
                            shrinkA=2, shrinkB=5))
ax.set_xlim(-0.6, 14.6)
ax.set_ylim(1.0, 24.0)
ax.set_xlabel("$t$")
ax.legend(fontsize=10.5, frameon=False, loc="upper right")
ax.set_title("(b)  $b(t-c)$ and $bt-c$ are not the same", fontsize=12,
             color=INK, pad=9)
tidy(ax)

fig.tight_layout(w_pad=2.4)
save(fig, "ahl-2-9a-sine.svg")

print("figures written to", os.path.normpath(OUT))
