"""SL 5.5 の図を作る。ラベルはすべて英語（数式は共通）。
   出力先: ai-sl/05-calculus/img/*.svg
   再生成: python3 figs/ai-sl/make_sl_5_5.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-sl", "05-calculus", "img")
os.makedirs(OUT, exist_ok=True)

INK, GRID, LINE, ACC, GREEN = "#1f2328", "#dfe3e8", "#2874a6", "#c0392b", "#1e8449"
GREY, GOLD = "#7a8592", "#b9770e"
plt.rcParams.update({"font.size": 11, "text.color": INK, "svg.fonttype": "path"})
BOX = dict(facecolor="white", edgecolor="none", pad=1.6, alpha=0.93)


def blank(ax, xlim=(0, 1), ylim=(0, 1)):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")


def axes(ax, xlim, ylim, xt=1, yt=1, xlab="$x$", ylab="$y$", ypad=12):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    for x in np.arange(np.ceil(xlim[0] / xt) * xt, xlim[1] + 1e-9, xt):
        ax.axvline(x, color=GRID, lw=0.7, zorder=0)
    for y in np.arange(np.ceil(ylim[0] / yt) * yt, ylim[1] + 1e-9, yt):
        ax.axhline(y, color=GRID, lw=0.7, zorder=0)
    ax.axhline(0, color=GREY, lw=1.2, zorder=1)
    ax.axvline(0, color=GREY, lw=1.2, zorder=1)
    ax.tick_params(labelsize=8.5, colors=GREY, length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xlabel(xlab, fontsize=11, color=INK, labelpad=1)
    ax.set_ylabel(ylab, fontsize=11, color=INK, labelpad=ypad, rotation=0)


def curved(ax, p, q, rad=0.35, color=ACC, lw=2.0):
    ax.add_patch(FancyArrowPatch(p, q, connectionstyle=f"arc3,rad={rad}",
                                 arrowstyle="-|>", mutation_scale=17,
                                 color=color, lw=lw, zorder=8))


# ══════════════ 1. 積分は微分の逆 ══════════════
fig, ax = plt.subplots(figsize=(7.2, 3.5))
blank(ax, ylim=(0.0, 1.0))

ax.text(0.22, 0.55, r"$x^{3}$", fontsize=32, ha="center", va="center")
ax.text(0.78, 0.55, r"$3x^{2}$", fontsize=32, ha="center", va="center")

curved(ax, (0.30, 0.68), (0.70, 0.68), rad=-0.32, color=ACC)
ax.text(0.50, 0.94, "differentiate  (SL 5.3)", color=ACC, fontsize=13,
        ha="center", va="center", zorder=9, bbox=BOX)

curved(ax, (0.70, 0.42), (0.30, 0.42), rad=-0.32, color=GREEN)
ax.text(0.50, 0.20, "integrate  (SL 5.5)", color=GREEN, fontsize=13,
        ha="center", va="center", zorder=9, bbox=BOX)
ax.text(0.50, 0.02, r"but $x^{3}+1$ and $x^{3}-5$ also differentiate to $3x^{2}$ ...",
        color=GOLD, fontsize=11.5, ha="center", va="center", zorder=9)

ax.set_xlim(0.06, 0.94)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-5-reverse.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 2. 公式：1 足して、その数で割る ══════════════
fig, ax = plt.subplots(figsize=(7.4, 3.9))
blank(ax)

ax.text(0.20, 0.62, r"$3x^{4}$", fontsize=32, ha="center", va="center")
ax.text(0.68, 0.62, r"$\dfrac{3x^{5}}{5}+C$", fontsize=30, ha="center",
        va="center")
ax.annotate("", xy=(0.46, 0.62), xytext=(0.31, 0.62),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.2))

curved(ax, (0.245, 0.78), (0.655, 0.83), rad=-0.36, color=ACC)
ax.text(0.44, 0.965, "1.  add $1$ to the power:  $4+1=5$",
        color=ACC, fontsize=12, ha="center", va="center", zorder=9, bbox=BOX)

curved(ax, (0.245, 0.47), (0.660, 0.47), rad=0.26, color=GREEN)
ax.text(0.45, 0.235, "2.  divide by the new power:  $\\div\\, 5$",
        color=GREEN, fontsize=12, ha="center", va="center", zorder=9, bbox=BOX)

ax.text(0.5, 0.06, r"$\int ax^{n}\,dx = \frac{a\,x^{\,n+1}}{n+1}+C, \quad n \neq -1$",
        fontsize=15, ha="center", va="center", color=INK)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-5-rule.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 3. +C と boundary condition ══════════════
fig, axs = plt.subplots(1, 2, figsize=(9.8, 4.3))

xs = np.linspace(-2.6, 2.6, 400)

ax = axs[0]
axes(ax, (-2.9, 2.9), (-3.4, 10.4), 1, 2)
for c, col in ((-3, GREY), (0, GREY), (3, GREY), (6, GREY)):
    ax.plot(xs, xs ** 2 + c, color=col, lw=1.9, zorder=4)
for a in (1.4,):
    for c in (-3, 0, 3, 6):
        ax.plot([a - 0.55, a + 0.55], [2 * a * (a - 0.55 - a) + a * a + c,
                                       2 * a * (a + 0.55 - a) + a * a + c],
                color=ACC, lw=2.0, zorder=6)
        ax.plot([a], [a * a + c], "o", color=INK, ms=4.5, zorder=8)
ax.text(-2.75, 9.4, "all have the same gradient\nat every $x$",
        color=ACC, fontsize=11.5, ha="left", va="center", zorder=10, bbox=BOX)
ax.text(-2.75, -2.5, r"$y=x^{2}+C$", fontsize=14, ha="left", va="center",
        zorder=10, bbox=BOX)
ax.set_title("without a condition: a whole family", fontsize=12, color=INK,
             pad=8)

ax = axs[1]
axes(ax, (-2.9, 2.9), (-3.4, 10.4), 1, 2)
for c in (-3, 0, 6):
    ax.plot(xs, xs ** 2 + c, color=GRID, lw=1.7, zorder=3)
ax.plot(xs, xs ** 2 + 3, color=LINE, lw=2.8, zorder=6)
ax.plot([2], [7], "o", color=ACC, ms=9, zorder=9)
ax.text(1.85, 8.3, "$(2,\\,7)$", color=ACC, fontsize=12.5, ha="right",
        va="bottom", zorder=10, bbox=BOX)
ax.text(-2.75, -2.5, r"$y=x^{2}+3$", color=LINE, fontsize=14, ha="left",
        va="center", zorder=10, bbox=BOX)
ax.text(-2.75, 9.4, "one point picks out\none curve", color=ACC,
        fontsize=11.5, ha="left", va="center", zorder=10, bbox=BOX)
ax.set_title("with $y=7$ when $x=2$: just one", fontsize=12, color=INK, pad=8)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-5-plusc.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 4. 定積分は面積 ══════════════
fig, ax = plt.subplots(figsize=(7.0, 4.9))
axes(ax, (-0.5, 4.0), (-1.2, 11.4), 1, 2)
xs = np.linspace(-0.3, 3.7, 400)
ax.plot(xs, xs ** 2 + 1, color=LINE, lw=2.8, zorder=6)

sh = np.linspace(1, 3, 200)
ax.fill_between(sh, 0, sh ** 2 + 1, color=LINE, alpha=0.18, zorder=2)
for a in (1, 3):
    ax.plot([a, a], [0, a * a + 1], color=ACC, lw=1.8, zorder=5)
    ax.plot([a], [0], "o", color=ACC, ms=6, zorder=8)
ax.text(1.0, -0.55, "$x=1$", color=ACC, fontsize=11.5, ha="center", va="top",
        zorder=10, bbox=BOX)
ax.text(3.0, -0.55, "$x=3$", color=ACC, fontsize=11.5, ha="center", va="top",
        zorder=10, bbox=BOX)
ax.text(2.0, 2.5, "area", fontsize=13.5, ha="center", va="center", color=INK,
        zorder=10, bbox=BOX)
ax.text(3.72, 10.6, "$y=f(x)$", color=LINE, fontsize=12.5, ha="right",
        va="center", zorder=10, bbox=BOX)
ax.text(0.55, 8.6, r"$A=\int_{1}^{3} f(x)\,dx$", fontsize=15, ha="left",
        va="center", color=INK, zorder=10, bbox=BOX)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-5-area.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 5. 変化率のグラフの面積＝合計 ══════════════
fig, ax = plt.subplots(figsize=(7.2, 4.6))
axes(ax, (-1.2, 21.5), (-1.6, 14.5), 2, 2,
     xlab="$t$ (minutes)", ylab="", ypad=6)
ts = np.linspace(0, 20, 300)
ax.plot(ts, 12 - 0.5 * ts, color=LINE, lw=2.8, zorder=6)

sh = np.linspace(0, 10, 200)
ax.fill_between(sh, 0, 12 - 0.5 * sh, color=GREEN, alpha=0.20, zorder=2)
ax.plot([10, 10], [0, 7], color=GREEN, lw=1.8, zorder=5)
ax.text(10, -0.7, "$t=10$", color=GREEN, fontsize=11.5, ha="center", va="top",
        zorder=10, bbox=BOX)
ax.text(4.6, 4.4, "area $=$ total litres\nin the first $10$ minutes",
        color=INK, fontsize=11.5, ha="center", va="center", zorder=10,
        bbox=BOX)
ax.text(20.9, 10.4, "rate of flow\n(litres per minute)", color=LINE,
        fontsize=11.5, ha="right", va="center", zorder=10, bbox=BOX)
ax.text(0.4, 13.4, "the graph shows a RATE; the area shows the TOTAL",
        fontsize=12, ha="left", va="center", color=GOLD, zorder=10, bbox=BOX)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-5-rate.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 自己チェック ══════════════
import sympy as sp
X, T = sp.Symbol('x'), sp.Symbol('t')
print("∫3x^4 =", sp.integrate(3*X**4, X))
print("∫(x^2+1) 1..3 =", sp.integrate(X**2 + 1, (X, 1, 3)))
print("∫(12-0.5t) 0..10 =", sp.integrate(12 - sp.Rational(1, 2)*T, (T, 0, 10)))
print("x^2+C through (2,7): C =", 7 - 2**2)
print("figures written to", os.path.normpath(OUT))
