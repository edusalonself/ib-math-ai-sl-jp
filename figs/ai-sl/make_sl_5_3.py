"""SL 5.3 の図を作る。ラベルはすべて英語（数式は共通）。
   出力先: ai-sl/05-calculus/img/*.svg
   再生成: python3 figs/ai-sl/make_sl_5_3.py
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
GREY = "#7a8592"
GOLD = "#b9770e"
plt.rcParams.update({
    "font.size": 11, "text.color": INK, "svg.fonttype": "path",
})
BOX = dict(facecolor="white", edgecolor="none", pad=1.6, alpha=0.92)


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


def curved(ax, p, q, rad=0.35, color=ACC, lw=1.8):
    ax.add_patch(FancyArrowPatch(p, q, connectionstyle=f"arc3,rad={rad}",
                                 arrowstyle="->", mutation_scale=16,
                                 color=color, lw=lw, zorder=8))


# ══════════════ 1. べき乗の公式：下ろして、1 減らす ══════════════
fig, ax = plt.subplots(figsize=(8.6, 4.4))
blank(ax)

ax.text(0.20, 0.66, r"$3x^{5}$", fontsize=34, ha="center", va="center")
ax.text(0.66, 0.66, r"$15x^{4}$", fontsize=34, ha="center", va="center")
ax.annotate("", xy=(0.50, 0.66), xytext=(0.33, 0.66),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.2))

# 「下ろす」
curved(ax, (0.245, 0.80), (0.585, 0.80), rad=-0.45, color=ACC)
ax.text(0.415, 0.955, "1.  bring the power down\n     and multiply:  $3\\times 5 = 15$",
        color=ACC, fontsize=12, ha="center", va="center", zorder=9, bbox=BOX)

# 「1 減らす」
curved(ax, (0.245, 0.53), (0.715, 0.53), rad=0.26, color=GREEN)
ax.text(0.470, 0.29, "2.  take $1$ off the power:  $5 - 1 = 4$",
        color=GREEN, fontsize=12, ha="center", va="center", zorder=9, bbox=BOX)

ax.text(0.5, 0.10, r"$f(x)=ax^{n} \ \Rightarrow \ f'(x)=a\,n\,x^{\,n-1}$",
        fontsize=15, ha="center", va="center", color=INK)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-3-rule.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 2. 項ごとに微分する ══════════════
fig, ax = plt.subplots(figsize=(9.6, 3.8))
blank(ax)
top = [(0.12, r"$3x^{4}$"), (0.33, r"$-\,5x^{2}$"), (0.545, r"$+\,7x$"),
       (0.73, r"$-\,2$")]
bot = [(0.12, r"$12x^{3}$"), (0.33, r"$-\,10x$"), (0.545, r"$+\,7$"),
       (0.73, r"$+\,0$")]
for (px, tx), (qx, bx) in zip(top, bot):
    ax.text(px, 0.80, tx, fontsize=21, ha="center", va="center")
    ax.text(qx, 0.22, bx, fontsize=21, ha="center", va="center", color=ACC)
    ax.annotate("", xy=(qx, 0.35), xytext=(px, 0.67),
                arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.6))
ax.text(0.90, 0.80, r"$=f(x)$", fontsize=15, ha="left", va="center",
        color=GREY)
ax.text(0.90, 0.22, r"$=f'(x)$", fontsize=15, ha="left", va="center",
        color=ACC)
ax.text(0.53, 0.02, "differentiate each term on its own",
        fontsize=12, ha="center", va="center", color=INK)
ax.set_xlim(0.03, 1.03)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-3-terms.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 3. 特別な2つ：定数と1次 ══════════════
fig, axs = plt.subplots(1, 2, figsize=(11.0, 4.4))

ax = axs[0]
axes(ax, (-3.4, 3.4), (-1.4, 6.4), 1, 1)
for a in (-2, 0, 2):
    ax.plot([a - 0.75, a + 0.75], [4, 4], color=ACC, lw=7.0, alpha=0.35,
            solid_capstyle="butt", zorder=4)
ax.plot([-3.2, 3.2], [4, 4], color=LINE, lw=2.4, zorder=5)
for a in (-2, 0, 2):
    ax.plot([a], [4], "o", color=INK, ms=6, zorder=8)
ax.text(0, 5.4, "the line is flat everywhere", color=ACC, fontsize=11.5,
        ha="center", va="center", zorder=10, bbox=BOX)
ax.text(0, 1.5, r"$y = 4 \ \Rightarrow \ \dfrac{dy}{dx} = 0$", fontsize=15,
        ha="center", va="center", zorder=10, bbox=BOX)
ax.set_title("a constant", fontsize=12, color=INK, pad=8)

ax = axs[1]
axes(ax, (-3.4, 3.4), (-6.4, 6.4), 1, 2)
xs = np.array([-1.9, 2.2])
for a in (-1.5, 0, 1.5):
    t = np.array([a - 0.42, a + 0.42])
    ax.plot(t, 3 * t - 1, color=ACC, lw=7.0, alpha=0.35,
            solid_capstyle="butt", zorder=4)
ax.plot(xs, 3 * xs - 1, color=LINE, lw=2.4, zorder=5)
for a in (-1.5, 0, 1.5):
    ax.plot([a], [3 * a - 1], "o", color=INK, ms=6, zorder=8)
ax.text(-1.9, 4.6, "the gradient is $3$\nat every point", color=ACC,
        fontsize=11.5, ha="center", va="center", zorder=10, bbox=BOX)
ax.text(1.1, -4.4, r"$y = 3x-1 \ \Rightarrow \ \dfrac{dy}{dx} = 3$",
        fontsize=14, ha="center", va="center", zorder=10, bbox=BOX)
ax.set_title("a straight line", fontsize=12, color=INK, pad=8)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-3-special.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 4. 分数は、書き直してから ══════════════
fig, ax = plt.subplots(figsize=(10.6, 3.0))
blank(ax)
steps = [(0.11, r"$\dfrac{6}{x^{2}}$", INK, "the question"),
         (0.37, r"$6x^{-2}$", GREEN, "rewrite"),
         (0.62, r"$-12x^{-3}$", ACC, "differentiate"),
         (0.87, r"$-\dfrac{12}{x^{3}}$", ACC, "write it back")]
for i, (px, tx, col, lab) in enumerate(steps):
    ax.text(px, 0.62, tx, fontsize=26, ha="center", va="center", color=col)
    ax.text(px, 0.22, lab, fontsize=11.5, ha="center", va="center", color=col)
    if i:
        ax.annotate("", xy=(px - 0.075, 0.62), xytext=(steps[i-1][0] + 0.075, 0.62),
                    arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.8))
ax.set_xlim(0.0, 1.0)
ax.set_ylim(0.12, 0.85)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-3-rewrite.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 5. SL 5.1 の答え合わせ ══════════════
fig, ax = plt.subplots(figsize=(8.2, 5.4))
axes(ax, (-0.4, 3.6), (-0.8, 10.4), 0.5, 2)
xs = np.linspace(-0.3, 3.4, 400)
ax.plot(xs, xs ** 2, color=LINE, lw=2.6, zorder=5)
t = np.array([0.9, 3.4])
ax.plot(t, 4 * (t - 2) + 4, color=ACC, lw=2.6, zorder=6)
ax.plot([2], [4], "o", color=INK, ms=8, zorder=9)
ax.text(1.86, 3.55, "$P(2,4)$", ha="right", va="top", fontsize=11.5,
        zorder=10, bbox=BOX)
ax.text(0.15, 9.2, "SL 5.1:  chords gave about $4$",
        color=GREY, fontsize=11.5, ha="left", va="center", zorder=10, bbox=BOX)
ax.text(0.15, 8.0, r"SL 5.3:  $f'(x)=2x$,  so  $f'(2)=4$",
        color=ACC, fontsize=12.5, ha="left", va="center", zorder=10, bbox=BOX)
ax.text(3.45, 2.2, "the tangent at $P$\nhas gradient $4$", color=ACC,
        fontsize=11, ha="right", va="center", zorder=10, bbox=BOX)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-3-check.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 自己チェック ══════════════
import sympy as sp
X = sp.Symbol('x')
print("3x^5      ->", sp.diff(3*X**5, X))
print("3x^4-5x^2+7x-2 ->", sp.diff(3*X**4-5*X**2+7*X-2, X))
print("6/x^2     ->", sp.diff(6/X**2, X), " = -12x^-3 ?",
      sp.simplify(sp.diff(6/X**2, X) + 12*X**-3) == 0)
print("x^2 at 2  ->", sp.diff(X**2, X).subs(X, 2))
print("figures written to", os.path.normpath(OUT))
