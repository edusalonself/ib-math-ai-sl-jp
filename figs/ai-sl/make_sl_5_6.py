"""SL 5.6 の図を作る。ラベルはすべて英語（数式は共通）。
   出力先: ai-sl/05-calculus/img/*.svg
   再生成: python3 figs/ai-sl/make_sl_5_6.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ai-sl", "05-calculus", "img")
os.makedirs(OUT, exist_ok=True)

INK, GRID, LINE, ACC, GREEN = "#1f2328", "#dfe3e8", "#2874a6", "#c0392b", "#1e8449"
GREY, GOLD = "#7a8592", "#b9770e"
plt.rcParams.update({"font.size": 11, "text.color": INK, "svg.fonttype": "path"})
BOX = dict(facecolor="white", edgecolor="none", pad=1.6, alpha=0.93)

F = lambda x: x ** 3 - 6 * x ** 2 + 9 * x + 1
FD = lambda x: 3 * x ** 2 - 12 * x + 9


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


# ══════════════ 1. 停留点：山と谷 ══════════════
fig, ax = plt.subplots(figsize=(6.8, 4.8))
axes(ax, (-0.6, 4.6), (-2.4, 8.4), 1, 2)
xs = np.linspace(-0.45, 4.45, 400)
ax.plot(xs, F(xs), color=LINE, lw=2.8, zorder=5)

for a, y, lab, dy, va in ((1, 5, "local maximum  $(1,\\,5)$", 0.85, "bottom"),
                          (3, 1, "local minimum  $(3,\\,1)$", -1.55, "top")):
    ax.plot([a - 0.75, a + 0.75], [y, y], color=ACC, lw=2.6, zorder=6)
    ax.plot([a], [y], "o", color=INK, ms=9, zorder=9)
    ax.text(a, y + dy, lab, color=ACC, fontsize=12, ha="center", va=va,
            zorder=10, bbox=BOX)

ax.text(0.05, 7.7, "at both points the tangent is horizontal:  $f'(x)=0$",
        fontsize=12, ha="left", va="center", color=INK, zorder=10, bbox=BOX)
ax.text(4.5, 6.4, "$y=f(x)$", color=LINE, fontsize=12.5, ha="right",
        va="center", zorder=10, bbox=BOX)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-6-stationary.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 2. 符号で見分ける ══════════════
fig, ax = plt.subplots(figsize=(8.6, 3.9))
blank(ax, (-0.02, 1.02), (0.0, 1.0))

y0 = 0.30
ax.plot([0.06, 0.96], [y0, y0], color=INK, lw=1.6, zorder=4)
for px, lab in ((0.36, "$x=1$"), (0.68, "$x=3$")):
    ax.plot([px, px], [y0 - 0.045, y0 + 0.045], color=INK, lw=1.6, zorder=5)
    ax.text(px, y0 - 0.10, lab, fontsize=12, ha="center", va="top", zorder=6)
ax.text(0.99, y0, "$x$", fontsize=12, ha="left", va="center")

# sign row
for px, s, col in ((0.21, "$+$", GREEN), (0.52, "$-$", ACC), (0.82, "$+$", GREEN)):
    ax.text(px, y0 + 0.12, s, color=col, fontsize=20, ha="center", va="center")
for px in (0.36, 0.68):
    ax.text(px, y0 + 0.12, "$0$", color=INK, fontsize=15, ha="center",
            va="center", bbox=BOX, zorder=7)
ax.text(0.02, y0 + 0.12, "$f'(x)$", fontsize=13, ha="left", va="center")

# shape row
sh = 0.72
for px, kind, col in ((0.21, "up", GREEN), (0.52, "down", ACC), (0.82, "up", GREEN)):
    t = np.linspace(-0.055, 0.055, 20)
    ax.plot(px + t, sh + (t * 1.6 if kind == "up" else -t * 1.6),
            color=col, lw=3.0, solid_capstyle="round", zorder=6)
for px, lab in ((0.36, "peak"), (0.68, "valley")):
    ax.plot([px - 0.05, px + 0.05], [sh, sh], color=INK, lw=3.0,
            solid_capstyle="round", zorder=6)
    ax.text(px, sh + 0.10, lab, fontsize=11.5, ha="center", va="bottom",
            color=INK)
ax.text(0.02, sh, "shape", fontsize=13, ha="left", va="center")

ax.text(0.50, 0.03, "$+$ then $-$  $\\Rightarrow$  local maximum      "
                    "$-$ then $+$  $\\Rightarrow$  local minimum",
        fontsize=12.5, ha="center", va="center", color=GOLD)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-6-sign.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 3. f と f' を並べる ══════════════
fig, axs = plt.subplots(2, 1, figsize=(6.6, 7.0), sharex=True,
                        gridspec_kw=dict(hspace=0.22))
xs = np.linspace(-0.45, 4.45, 400)

ax = axs[0]
axes(ax, (-0.6, 4.6), (-2.4, 8.4), 1, 2, xlab="")
ax.plot(xs, F(xs), color=LINE, lw=2.8, zorder=5)
for a, y in ((1, 5), (3, 1)):
    ax.plot([a - 0.6, a + 0.6], [y, y], color=ACC, lw=2.2, zorder=6)
    ax.plot([a], [y], "o", color=INK, ms=7, zorder=9)
    ax.axvline(a, color=GOLD, lw=1.6, ls=(0, (6, 4)), zorder=3)
ax.set_title("$y=f(x)$", fontsize=13, color=LINE, pad=6)

ax = axs[1]
axes(ax, (-0.6, 4.6), (-4.5, 10.5), 1, 3)
ax.plot(xs, FD(xs), color=GREEN, lw=2.8, zorder=5)
for a in (1, 3):
    ax.axvline(a, color=GOLD, lw=1.6, ls=(0, (6, 4)), zorder=3)
    ax.plot([a], [0], "o", color=INK, ms=7, zorder=9)
ax.set_title("$y=f'(x)$", fontsize=13, color=GREEN, pad=6)
ax.text(2.0, 7.6, "$f'$ crosses the $x$-axis exactly\nwhere $f$ has a peak or a valley",
        fontsize=11.5, ha="center", va="center", color=INK, zorder=10, bbox=BOX)

fig.savefig(os.path.join(OUT, "sl-5-6-fdash.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 4. local は global とは限らない ══════════════
fig, ax = plt.subplots(figsize=(7.6, 5.4))
axes(ax, (-1.7, 5.7), (-18.5, 25.5), 1, 5)
xs = np.linspace(-1, 5, 400)
ax.plot(xs, F(xs), color=LINE, lw=2.8, zorder=5)

for a, y, lab, col, dy, va in (
        (1, 5, "local maximum $(1,\\,5)$", ACC, 3.2, "bottom"),
        (3, 1, "local minimum $(3,\\,1)$", ACC, -3.2, "top")):
    ax.plot([a], [y], "o", color=ACC, ms=8, zorder=9)
    ax.text(a, y + dy, lab, color=col, fontsize=11.5, ha="center", va=va,
            zorder=10, bbox=BOX)

for a, y, lab, ha, dx in ((-1, -15, "least value $-15$", "left", 0.22),
                          (5, 21, "greatest value $21$", "right", -0.22)):
    ax.plot([a], [y], "o", color=GREEN, ms=10, zorder=10)
    ax.text(a + dx, y, lab, color=GREEN, fontsize=12, ha=ha, va="center",
            zorder=11, bbox=BOX)

ax.axvline(-1, color=GREY, lw=1.4, ls=(0, (5, 4)), zorder=2)
ax.axvline(5, color=GREY, lw=1.4, ls=(0, (5, 4)), zorder=2)
ax.text(-1.55, 23.5, "on the domain $-1 \\leq x \\leq 5$", fontsize=12,
        ha="left", va="center", color=INK, zorder=10, bbox=BOX)
ax.text(1.3, -9.5, "the greatest and least values are at the ENDS,\n"
                   "not at the local maximum or minimum",
        fontsize=11.5, ha="left", va="center", color=GOLD, zorder=10, bbox=BOX)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-6-local-global.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 5. 文脈：利益が最大になるところ ══════════════
fig, ax = plt.subplots(figsize=(7.4, 4.8))
axes(ax, (-4, 64), (-380, 700), 10, 200,
     xlab="$x$  (items sold per week)", ylab="", ypad=6)
xs = np.linspace(0, 60, 300)
P = lambda x: -0.5 * x ** 2 + 40 * x - 300
ax.plot(xs, P(xs), color=LINE, lw=2.8, zorder=5)
ax.plot([40 - 8, 40 + 8], [500, 500], color=ACC, lw=2.6, zorder=6)
ax.plot([40], [500], "o", color=INK, ms=9, zorder=9)
ax.plot([40, 40], [0, 500], color=ACC, lw=1.4, ls=(0, (5, 4)), zorder=4)
ax.text(40, 585, "maximum profit  $\\$500$", color=ACC, fontsize=12.5,
        ha="center", va="center", zorder=10, bbox=BOX)
ax.text(40, -60, "$x=40$", color=ACC, fontsize=11.5, ha="center", va="top",
        zorder=10, bbox=BOX)
ax.text(2, 640, "profit $P$  (dollars)", color=LINE, fontsize=12,
        ha="left", va="center", zorder=10, bbox=BOX)
ax.text(2, -300, "$P'(x)=0$  gives the best number to sell", fontsize=12,
        ha="left", va="center", color=GOLD, zorder=10, bbox=BOX)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-6-context.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 自己チェック ══════════════
import sympy as sp
X = sp.Symbol('x')
f = X**3 - 6*X**2 + 9*X + 1
print("f' =", sp.factor(sp.diff(f, X)), " zeros", sp.solve(sp.diff(f, X), X))
for a in (-1, 1, 3, 5):
    print(f"  f({a}) =", f.subs(X, a))
p = -sp.Rational(1, 2)*X**2 + 40*X - 300
print("P' zero:", sp.solve(sp.diff(p, X), X), " P(40) =", p.subs(X, 40))
print("figures written to", os.path.normpath(OUT))
