"""SL 5.8 の図を作る。ラベルはすべて英語（数式は共通）。
   出力先: ai-sl/05-calculus/img/*.svg
   再生成: python3 figs/ai-sl/make_sl_5_8.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from scipy.interpolate import make_interp_spline

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


def strips(ax, f, a, b, n, color=ACC, alpha=0.20, lw=1.6):
    xs = np.linspace(a, b, n + 1)
    for i in range(n):
        p = [(xs[i], 0), (xs[i], f(xs[i])), (xs[i + 1], f(xs[i + 1])),
             (xs[i + 1], 0)]
        ax.add_patch(Polygon(p, closed=True, facecolor=color, alpha=alpha,
                             edgecolor=color, lw=lw, zorder=3))
    return xs


HUMP = lambda t: 6 - 0.4 * (t - 3) ** 2

# ══════════════ 1. 台形でうめる ══════════════
fig, ax = plt.subplots(figsize=(7.2, 4.6))
axes(ax, (-0.8, 7.0), (-1.1, 8.3), 1, 2)
xs = np.linspace(-0.4, 6.6, 400)
ax.plot(xs, HUMP(xs), color=LINE, lw=2.8, zorder=6)
strips(ax, HUMP, 0, 6, 4)
for t in np.linspace(0, 6, 5):
    ax.plot([t, t], [0, HUMP(t)], color=ACC, lw=1.6, zorder=4)

ax.text(3.0, 7.6, "the tops of the trapezia are STRAIGHT,\n"
                  "so they miss a little of the curve",
        fontsize=11.5, ha="center", va="center", color=GOLD, zorder=10,
        bbox=BOX)
ax.text(3.0, 2.2, "$4$ trapezia", fontsize=14, ha="center", va="center",
        color=INK, zorder=10, bbox=BOX)
ax.text(6.7, 4.6, "$y=f(x)$", color=LINE, fontsize=12.5, ha="right",
        va="center", zorder=10, bbox=BOX)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-8-idea.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 2. 端は1回、中は2回 ══════════════
fig, ax = plt.subplots(figsize=(7.6, 4.8))
axes(ax, (-0.8, 7.0), (-2.4, 8.6), 1, 2)
xs = np.linspace(-0.4, 6.6, 400)
ax.plot(xs, HUMP(xs), color=LINE, lw=2.4, zorder=6)
pts = np.linspace(0, 6, 5)
strips(ax, HUMP, 0, 6, 4, color=GREY, alpha=0.10, lw=1.2)

for i, t in enumerate(pts):
    col = ACC if i in (0, 4) else GREEN
    ax.plot([t, t], [0, HUMP(t)], color=col, lw=3.2, zorder=7)
    ax.plot([t], [HUMP(t)], "o", color=col, ms=7, zorder=8)
    ax.text(t, HUMP(t) + 0.45, f"$y_{{{i}}}$", color=col, fontsize=12.5,
            ha="center", va="bottom", zorder=10, bbox=BOX)
    ax.text(t, -0.55, "$\\times 1$" if i in (0, 4) else "$\\times 2$",
            color=col, fontsize=12, ha="center", va="top", zorder=10)

ax.annotate("", xy=(1.5, 1.0), xytext=(0.0, 1.0),
            arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=1.4,
                            mutation_scale=11))
ax.text(0.75, 1.0, "$h$", fontsize=13, ha="center", va="center", color=INK,
        zorder=10, bbox=BOX)
ax.text(3.0, -1.75, "the two ENDS count once;  every MIDDLE counts twice",
        fontsize=12.5, ha="center", va="center", color=GOLD)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-8-count.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 3. 過大評価か過小評価か ══════════════
fig, axs = plt.subplots(1, 2, figsize=(10.2, 4.4))

ax = axs[0]
axes(ax, (-0.5, 4.5), (-1.2, 8.4), 1, 2)
g = lambda t: 7 - 0.7 * (t - 2) ** 2
xs = np.linspace(-0.2, 4.2, 300)
ax.plot(xs, g(xs), color=LINE, lw=2.8, zorder=6)
strips(ax, g, 0.5, 3.5, 2, color=GREEN, alpha=0.22)
ax.text(2.0, 2.4, "trapezia lie\nBELOW", fontsize=12, ha="center",
        va="center", color=GREEN, zorder=10, bbox=BOX)
ax.set_title("the curve bends like a hill  →  UNDER-estimate",
             fontsize=12, color=GREEN, pad=8)

ax = axs[1]
axes(ax, (-0.5, 4.5), (-1.2, 8.4), 1, 2)
u = lambda t: 0.55 * (t - 0.4) ** 2 + 0.6
xs = np.linspace(-0.2, 4.2, 300)
ax.plot(xs, u(xs), color=LINE, lw=2.8, zorder=6)
strips(ax, u, 0.5, 3.5, 2, color=ACC, alpha=0.22)
ax.text(1.55, 5.0, "trapezia lie\nABOVE", fontsize=12, ha="center",
        va="center", color=ACC, zorder=10, bbox=BOX)
ax.set_title("the curve bends like a valley  →  OVER-estimate",
             fontsize=12, color=ACC, pad=8)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-8-over-under.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 4. 関数がないとき（川・湖） ══════════════
fig, ax = plt.subplots(figsize=(8.0, 4.4))
blank(ax, (-4.0, 34.0), (-8.0, 9.6))

xd = np.array([0, 5, 10, 15, 20, 25, 30], float)
wd = np.array([0, 6, 9, 11, 10, 7, 0], float)
xf = np.linspace(0, 30, 400)
up = make_interp_spline(xd, 0.58 * wd, k=3)(xf)
lo = make_interp_spline(xd, -0.42 * wd, k=3)(xf)
ax.fill_between(xf, lo, up, color=LINE, alpha=0.20, zorder=2)
ax.plot(xf, up, color=LINE, lw=2.2, zorder=4)
ax.plot(xf, lo, color=LINE, lw=2.2, zorder=4)

for xv, wv in zip(xd, wd):
    yu, yl = 0.58 * wv, -0.42 * wv
    ax.plot([xv, xv], [yl, yu], color=ACC, lw=2.2, zorder=6)
    ax.text(xv, yu + 0.45, f"${wv:.0f}$", color=ACC, fontsize=11.5,
            ha="center", va="bottom", zorder=8)
    ax.plot([xv, xv], [-6.0, -5.4], color=GREY, lw=1.2, zorder=5)
    ax.text(xv, -6.4, f"${xv:.0f}$", color=GREY, fontsize=10, ha="center",
            va="top", zorder=8)
ax.plot([0, 30], [-5.7, -5.7], color=GREY, lw=1.4, zorder=5)
ax.text(15, -7.6, "distance along the lake (m)", fontsize=11.5, ha="center",
        va="center", color=GREY)
ax.text(-3.6, 8.6, "widths measured every $5$ m — there is NO formula here",
        fontsize=12.5, ha="left", va="center", color=GOLD)
ax.text(33.6, 6.4, "the trapezoidal rule\nstill works", fontsize=11.5,
        ha="right", va="center", color=INK, zorder=10, bbox=BOX)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-8-lake.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 5. n を増やすと近づく ══════════════
fig, axs = plt.subplots(1, 2, figsize=(10.2, 4.2), sharey=True)
sq = lambda t: t ** 2
for ax, n, T in zip(axs, (4, 8), (22, 21.5)):
    axes(ax, (-0.6, 4.6), (-2.6, 18.5), 1, 4,
         ylab="$y$" if n == 4 else "")
    xs = np.linspace(-0.3, 4.3, 300)
    strips(ax, sq, 0, 4, n, color=ACC, alpha=0.18, lw=1.2)
    ax.plot(xs, sq(xs), color=LINE, lw=2.8, zorder=6)
    ax.set_title(f"$n = {n}$   estimate $= {T}$", fontsize=12.5, color=INK,
                 pad=8)
    ax.text(0.25, 15.6, "exact area $=21.3$", fontsize=11.5, ha="left",
            va="center", color=GREEN, zorder=10, bbox=BOX)
    ax.text(2.0, -1.9, "more strips  →  smaller gaps" if n == 8 else
            "the gaps are the error", fontsize=11.5, ha="center",
            va="center", color=GOLD)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-8-n.svg"), bbox_inches="tight")
plt.close(fig)


# ══════════════ 自己チェック ══════════════
import sympy as sp
X = sp.Symbol('x')


def trap(ys, h):
    return sp.Rational(1, 2) * sp.nsimplify(h) * ((ys[0] + ys[-1])
                                                  + 2 * sum(ys[1:-1]))


print("x^2 [0,4] n=4 :", trap([0, 1, 4, 9, 16], 1),
      " exact", sp.integrate(X ** 2, (X, 0, 4)))
print("x^2 [0,4] n=8 :",
      trap([sp.Rational(i, 2) ** 2 for i in range(9)], sp.Rational(1, 2)))
print("river         :", trap([0, 6, 9, 11, 10, 7, 0], 5))
print("figures written to", os.path.normpath(OUT))


# ══════════════════════════════════════════════════════════
#  例題の図（問題文のところに置く）
#   例題の枠の中に入るので、背景は透明にする。
# ══════════════════════════════════════════════════════════
def we_fig(name, draw, figsize=(5.8, 4.0)):
    fig, ax = plt.subplots(figsize=figsize)
    draw(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True)
    plt.close(fig)


def label_ys(ax, xs, ys, fs=9.5, dy=0.04, color=ACC):
    """各分点に y_0, y_1, ... を書き入れる。"""
    span = max(ys) - min(0, min(ys))
    for i, (x, y) in enumerate(zip(xs, ys)):
        ax.plot([x, x], [0, y], color=color, lw=1.1, ls="--", zorder=4)
        ax.annotate(f"$y_{{{i}}}$", (x, y + dy * span), color=color,
                    fontsize=fs, ha="center", va="bottom", zorder=9)


# --- 例題1：y = x^2、0 から 4、n = 4 ---
def _w1(ax):
    f = lambda t: t ** 2
    axes(ax, (-0.6, 4.8), (-2.2, 19.0), 1, 4)
    xs = np.linspace(0, 4, 400)
    ax.plot(xs, f(xs), color=LINE, lw=2.4, zorder=6)
    px = strips(ax, f, 0, 4, 4)
    label_ys(ax, px, f(px))
    ax.annotate("$y = x^{2}$", (4.3, 16.5), color=LINE, fontsize=12,
                ha="left", va="center")
    ax.annotate("", xy=(1.0, -1.3), xytext=(0.0, -1.3),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=1.2))
    ax.annotate("$h$", (0.5, -2.0), color=INK, fontsize=11, ha="center")
    ax.set_title("$n = 4$ trapezia between $x = 0$ and $x = 4$",
                 fontsize=11.5, pad=8)


we_fig("sl-5-8-we1.svg", _w1, (5.8, 4.0))


# --- 例題3：y = 20/x、1 から 5、n = 4 ---
def _w3(ax):
    f = lambda t: 20.0 / t
    axes(ax, (-0.3, 6.0), (-3.0, 24.0), 1, 5)
    xs = np.linspace(0.85, 5.6, 400)
    ax.plot(xs, f(xs), color=LINE, lw=2.4, zorder=6)
    px = strips(ax, f, 1, 5, 4)
    label_ys(ax, px, f(px))
    ax.annotate(r"$y = \dfrac{20}{x}$", (5.2, 15.0), color=LINE, fontsize=12,
                ha="left", va="center")
    ax.annotate("", xy=(2.0, -1.8), xytext=(1.0, -1.8),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=1.2))
    ax.annotate("$h$", (1.5, -2.7), color=INK, fontsize=11, ha="center")
    ax.set_title("$n = 4$ trapezia between $x = 1$ and $x = 5$",
                 fontsize=11.5, pad=8)


we_fig("sl-5-8-we3.svg", _w3, (5.8, 4.0))


# --- 例題4：速さと時間（表の値だけ。式はない） ---
def _w4(ax):
    t = np.array([0, 2, 4, 6, 8, 10], dtype=float)
    v = np.array([0, 5, 12, 18, 21, 22], dtype=float)
    axes(ax, (-1.1, 11.6), (-4.8, 25.5), 2, 5,
         xlab="$t$  (s)", ylab="$v$", ypad=14)
    for i in range(len(t) - 1):
        p = [(t[i], 0), (t[i], v[i]), (t[i + 1], v[i + 1]), (t[i + 1], 0)]
        ax.add_patch(Polygon(p, closed=True, facecolor=ACC, alpha=0.20,
                             edgecolor=ACC, lw=1.6, zorder=3))
    ax.plot(t, v, color=LINE, lw=2.2, marker="o", ms=6, zorder=6)
    for i, (x, y) in enumerate(zip(t, v)):
        ax.annotate(f"$y_{{{i}}}$", (x, y + 1.0), color=ACC, fontsize=9.5,
                    ha="center", va="bottom", zorder=9)
    ax.annotate("", xy=(2.0, -2.2), xytext=(0.0, -2.2),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=1.2))
    ax.annotate("$h = 2$", (1.0, -4.0), color=INK, fontsize=11, ha="center")
    ax.annotate("speed  (m s$^{-1}$)", (-0.9, 24.6), color=INK, fontsize=10,
                ha="left", va="center")
    ax.set_title("Only the recorded points are known — no formula",
                 fontsize=11.5, pad=8)


we_fig("sl-5-8-we4.svg", _w4, (6.2, 4.0))


# --- 例題5：n = 4 と n = 8 をならべる ---
def _w5(ax):
    pass


fig, axs = plt.subplots(1, 2, figsize=(10.4, 3.9))
f = lambda t: t ** 2
for ax, n in zip(axs, (4, 8)):
    axes(ax, (-0.6, 4.6), (-1.6, 19.0), 1, 4)
    xs = np.linspace(0, 4, 400)
    ax.plot(xs, f(xs), color=LINE, lw=2.2, zorder=6)
    strips(ax, f, 0, 4, n)
    ax.set_title(f"$n = {n}$   ($h = {4/n:g}$)", fontsize=12, pad=8,
                 color=ACC if n == 8 else INK)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sl-5-8-we5.svg"), bbox_inches="tight",
            transparent=True)
plt.close(fig)

print("wrote sl-5-8-we1.svg, we3, we4, we5")
